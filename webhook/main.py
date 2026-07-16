"""Phase-1 Retell custom-function webhooks for overnight gate attendant."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("gate-webhook")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"

GUEST_LIST_PATH = Path(os.getenv("GUEST_LIST_PATH", str(DATA_DIR / "guest-list.json")))
EVENTS_PATH = Path(os.getenv("EVENTS_PATH", str(DATA_DIR / "events.jsonl")))
GUEST_LIST_JSON = os.getenv("GUEST_LIST_JSON", "").strip()  # serverless override
SERVERLESS = os.getenv("SERVERLESS", "false").lower() in {"1", "true", "yes"}

RETELL_API_KEY = os.getenv("RETELL_API_KEY", "")
ONCALL_PHONE = os.getenv("ONCALL_PHONE", "")
DEFAULT_COMMUNITY = os.getenv("DEFAULT_COMMUNITY", "Pilot HOA")
VERIFY_SIGNATURES = os.getenv("VERIFY_RETELL_SIGNATURES", "true").lower() == "true"
IGNORE_VALIDITY_WINDOW = os.getenv("IGNORE_VALIDITY_WINDOW", "false").lower() in {
    "1",
    "true",
    "yes",
}

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

app = FastAPI(
    title="Virtual Gate Guard — Retell tools",
    version="0.2.0",
    description="Mid-call tools: check_guest_list, open_gate, escalate_to_oncall",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _names_match(a: str, b: str) -> bool:
    na, nb = _normalize(a), _normalize(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    return na in nb or nb in na


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _entry_active(entry: dict[str, Any], now: datetime, tz_name: str) -> bool:
    if IGNORE_VALIDITY_WINDOW or entry.get("always_active"):
        return True
    start = _parse_dt(entry.get("valid_from"))
    end = _parse_dt(entry.get("valid_until"))
    # No window set → treat as always active (pilot-friendly)
    if start is None and end is None:
        return True
    if start and now < start:
        return False
    if end and now > end:
        return False
    # Optional: if only one bound set, still respect it
    _ = tz_name
    return True


def _load_guest_list() -> dict[str, Any]:
    if GUEST_LIST_JSON:
        return json.loads(GUEST_LIST_JSON)
    if not GUEST_LIST_PATH.exists():
        example = DATA_DIR / "guest-list.example.json"
        raise FileNotFoundError(
            f"Missing guest list at {GUEST_LIST_PATH}. "
            f"Copy {example} → guest-list.json, or set GUEST_LIST_JSON."
        )
    with GUEST_LIST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _append_event(event: dict[str, Any]) -> None:
    event = {**event, "ts": datetime.now(timezone.utc).isoformat()}
    line = json.dumps(event, default=str)
    if SERVERLESS:
        log.info("event %s", line)
        return
    try:
        EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        log.info("event(fallback) %s", line)


def _send_sms(body: str) -> dict[str, Any]:
    if not ONCALL_PHONE:
        log.warning("ONCALL_PHONE not set — SMS: %s", body)
        return {"channel": "log", "status": "logged", "body": body}

    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER:
        try:
            from twilio.rest import Client

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            msg = client.messages.create(
                body=body, from_=TWILIO_FROM_NUMBER, to=ONCALL_PHONE
            )
            return {
                "channel": "twilio",
                "status": "sent",
                "sid": msg.sid,
                "to": ONCALL_PHONE,
            }
        except Exception as exc:  # noqa: BLE001
            log.exception("Twilio send failed")
            return {"channel": "twilio", "status": "error", "error": str(exc)}

    log.info("SMS (log-only) → %s | %s", ONCALL_PHONE, body)
    return {
        "channel": "log",
        "status": "logged",
        "to": ONCALL_PHONE,
        "body": body,
    }


def _verify_retell(raw_body: str, signature: str | None) -> None:
    if not VERIFY_SIGNATURES:
        return
    if not RETELL_API_KEY:
        log.warning("RETELL_API_KEY unset — skipping signature verify")
        return
    if not signature:
        raise HTTPException(status_code=401, detail="Missing X-Retell-Signature")
    try:
        from retell import Retell

        client = Retell(api_key=RETELL_API_KEY)
        ok = client.verify(
            raw_body,
            api_key=RETELL_API_KEY,
            signature=signature,
        )
    except Exception as exc:  # noqa: BLE001
        log.exception("Signature verify error")
        raise HTTPException(status_code=401, detail=f"Verify failed: {exc}") from exc
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid Retell signature")


def _extract_args(payload: dict[str, Any]) -> dict[str, Any]:
    if "args" in payload and isinstance(payload["args"], dict):
        return payload["args"]
    return {k: v for k, v in payload.items() if k not in {"name", "call"}}


async def _read_verified_json(
    request: Request, signature: str | None
) -> dict[str, Any]:
    raw = (await request.body()).decode("utf-8")
    _verify_retell(raw, signature)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}") from exc


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "virtual-gate-guard-retell-webhooks",
        "version": "0.2.0",
        "endpoints": [
            "GET /health",
            "POST /tools/check_guest_list",
            "POST /tools/open_gate",
            "POST /tools/escalate_to_oncall",
            "POST /retell/webhook",
        ],
    }


@app.get("/health")
def health() -> dict[str, Any]:
    guest_ok = bool(GUEST_LIST_JSON) or GUEST_LIST_PATH.exists()
    return {
        "status": "ok",
        "community_default": DEFAULT_COMMUNITY,
        "guest_list_ready": guest_ok,
        "oncall_configured": bool(ONCALL_PHONE),
        "twilio_configured": bool(
            TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER
        ),
        "verify_signatures": VERIFY_SIGNATURES,
        "serverless": SERVERLESS,
    }


@app.post("/tools/check_guest_list")
async def check_guest_list(
    request: Request,
    x_retell_signature: str | None = Header(default=None),
) -> JSONResponse:
    payload = await _read_verified_json(request, x_retell_signature)
    args = _extract_args(payload)

    community = (args.get("community_name") or DEFAULT_COMMUNITY).strip()
    visitor = (args.get("visitor_name") or "").strip()
    host = (args.get("host_name_or_address") or "").strip()
    visit_type = (args.get("visit_type") or "").strip().lower()

    if not visitor or not host:
        result = {
            "decision": "escalate",
            "confidence": "low",
            "message": "Need both visitor name and host name or address before deciding.",
        }
        _append_event({"tool": "check_guest_list", "args": args, "result": result})
        return JSONResponse(result)

    try:
        book = _load_guest_list()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        result = {
            "decision": "escalate",
            "confidence": "low",
            "message": str(exc),
        }
        _append_event({"tool": "check_guest_list", "args": args, "result": result})
        return JSONResponse(result)

    tz_name = book.get("timezone") or "America/New_York"
    try:
        now = datetime.now(ZoneInfo(tz_name)).astimezone(timezone.utc)
    except Exception:  # noqa: BLE001
        now = datetime.now(timezone.utc)

    matches: list[dict[str, Any]] = []
    for entry in book.get("entries", []):
        if not _entry_active(entry, now, tz_name):
            continue
        visitor_ok = _names_match(visitor, entry.get("visitor_name", ""))
        host_ok = _names_match(host, entry.get("host_name", "")) or _names_match(
            host, entry.get("host_address", "")
        )
        if visitor_ok and host_ok:
            matches.append(entry)

    if len(matches) == 1:
        m = matches[0]
        if visit_type == "delivery" and m.get("visit_type") != "delivery":
            decision, confidence = "escalate", "medium"
            message = "Possible match but visit type differs — escalate to on-call."
        else:
            decision, confidence = "approve", "high"
            message = (
                f"Approved: {m.get('visitor_name')} visiting "
                f"{m.get('host_name')} ({m.get('host_address')}). "
                f"Notes: {m.get('notes') or 'none'}. Call open_gate next."
            )
        result = {
            "decision": decision,
            "confidence": confidence,
            "matched_entry": {
                "visitor_name": m.get("visitor_name"),
                "host_name": m.get("host_name"),
                "host_address": m.get("host_address"),
                "visit_type": m.get("visit_type"),
            },
            "message": message,
            "community_name": community,
        }
    elif len(matches) > 1:
        result = {
            "decision": "escalate",
            "confidence": "low",
            "message": (
                f"Multiple guest-list matches ({len(matches)}). "
                "Escalate; do not open."
            ),
            "community_name": community,
        }
    else:
        result = {
            "decision": "deny",
            "confidence": "high",
            "message": (
                "No guest-list match. Deny open. Tell visitor the host must add a "
                "myQ guest pass, then they may call back."
            ),
            "community_name": community,
        }

    _append_event({"tool": "check_guest_list", "args": args, "result": result})
    return JSONResponse(result)


@app.post("/tools/open_gate")
async def open_gate(
    request: Request,
    x_retell_signature: str | None = Header(default=None),
) -> JSONResponse:
    payload = await _read_verified_json(request, x_retell_signature)
    args = _extract_args(payload)

    community = (args.get("community_name") or DEFAULT_COMMUNITY).strip()
    visitor = (args.get("visitor_name") or "unknown").strip()
    host = (args.get("host_name_or_address") or "unknown").strip()
    reason = (args.get("reason") or "").strip()
    entrance = (args.get("entrance") or "main").strip()

    sms_body = (
        f"[{community}] OPEN {visitor} visiting {host} @ {entrance}. "
        f"{reason or 'guest list approve'} — unlock myQ NOW."
    )
    sms = _send_sms(sms_body)

    if sms.get("status") == "error":
        result = {
            "status": "failed",
            "phase": 1,
            "message": (
                "Could not notify on-call. Tell visitor to wait and escalate. "
                f"Error: {sms.get('error')}"
            ),
            "sms": sms,
        }
    else:
        result = {
            "status": "pending_human_open",
            "phase": 1,
            "message": (
                "On-call notified to unlock in myQ. Tell visitor to wait for the "
                "gate to move. Do not claim it is already open until they see motion."
            ),
            "sms": sms,
        }

    _append_event({"tool": "open_gate", "args": args, "result": result})
    return JSONResponse(result)


@app.post("/tools/escalate_to_oncall")
async def escalate_to_oncall(
    request: Request,
    x_retell_signature: str | None = Header(default=None),
) -> JSONResponse:
    payload = await _read_verified_json(request, x_retell_signature)
    args = _extract_args(payload)

    community = (args.get("community_name") or DEFAULT_COMMUNITY).strip()
    visitor = (args.get("visitor_name") or "").strip()
    host = (args.get("host_name_or_address") or "").strip()
    summary = (args.get("summary") or "escalation").strip()
    urgency = (args.get("urgency") or "normal").strip()

    sms_body = (
        f"[{community}] ESCALATE ({urgency}) {visitor or 'n/a'} / "
        f"{host or 'n/a'}: {summary}"
    )
    sms = _send_sms(sms_body)

    result = {
        "status": "escalated" if sms.get("status") != "error" else "failed",
        "message": (
            "On-call notified. Tell visitor you are checking with the attendant. "
            "Do not open the gate."
        ),
        "sms": sms,
    }
    _append_event({"tool": "escalate_to_oncall", "args": args, "result": result})
    return JSONResponse(result)


@app.post("/retell/webhook")
async def retell_call_webhook(
    request: Request,
    x_retell_signature: str | None = Header(default=None),
) -> JSONResponse:
    payload = await _read_verified_json(request, x_retell_signature)
    _append_event({"tool": "retell_webhook", "payload": payload})
    return JSONResponse({"ok": True})
