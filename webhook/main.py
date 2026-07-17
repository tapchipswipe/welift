"""Autonomous overnight gate webhooks for Retell.

Product mode: AI verifies against guest list / post orders, then opens via myQ
Partner API — no human awake overnight.

- approve + open_gate → myQ remote unlock
- deny / ambiguous → refuse; log only (no SMS wake)
- escalate_to_oncall → audit log only; tell visitor to use myQ guest pass
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.error
import urllib.request
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
GUEST_LIST_JSON = os.getenv("GUEST_LIST_JSON", "").strip()
SERVERLESS = os.getenv("SERVERLESS", "false").lower() in {"1", "true", "yes"}

RETELL_API_KEY = os.getenv("RETELL_API_KEY", "")
DEFAULT_COMMUNITY = os.getenv("DEFAULT_COMMUNITY", "The Inlets")
VERIFY_SIGNATURES = os.getenv("VERIFY_RETELL_SIGNATURES", "true").lower() == "true"
IGNORE_VALIDITY_WINDOW = os.getenv("IGNORE_VALIDITY_WINDOW", "false").lower() in {
    "1",
    "true",
    "yes",
}

# Autonomous product mode (default). Human SMS wake is off unless explicitly enabled.
AUTONOMOUS = os.getenv("AUTONOMOUS", "true").lower() in {"1", "true", "yes"}
# Local / cell demos only — pretend unlock succeeded without myQ API
SIMULATE_MYQ_OPEN = os.getenv("SIMULATE_MYQ_OPEN", "false").lower() in {
    "1",
    "true",
    "yes",
}
# Deprecated: overnight SMS to a human. Off by default.
HUMAN_SMS_FALLBACK = os.getenv("HUMAN_SMS_FALLBACK", "false").lower() in {
    "1",
    "true",
    "yes",
}
ONCALL_PHONE = os.getenv("ONCALL_PHONE", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

MYQ_API_BASE = os.getenv("MYQ_API_BASE", "").rstrip("/")
MYQ_API_KEY = os.getenv("MYQ_API_KEY", "")
MYQ_FACILITY_ID = os.getenv("MYQ_FACILITY_ID", "")
MYQ_ENTRANCE_ID = os.getenv("MYQ_ENTRANCE_ID", "")
MYQ_UNLOCK_PATH = os.getenv(
    "MYQ_UNLOCK_PATH", "/v1/facilities/{facility_id}/entrances/{entrance_id}/unlock"
)

VERSION = "0.4.0"

app = FastAPI(
    title="We Lift — Autonomous gate tools",
    version=VERSION,
    description="AI verify + myQ unlock. No overnight human attendant.",
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


def _tokens(text: str) -> set[str]:
    return {
        t
        for t in _normalize(text).split()
        if t and t not in {"the", "a", "an", "of"}
    }


def _names_match(a: str, b: str) -> bool:
    """Substring match, then token overlap (handles 'Jordan Lee' vs 'Lee, Jordan')."""
    na, nb = _normalize(a), _normalize(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    shorter, longer = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    return shorter.issubset(longer)


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
    if start is None and end is None:
        return True
    if start and now < start:
        return False
    if end and now > end:
        return False
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
    """Optional legacy path only — not used in autonomous default."""
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


def _myq_configured() -> bool:
    return bool(MYQ_API_BASE and MYQ_API_KEY and MYQ_FACILITY_ID and MYQ_ENTRANCE_ID)


def _try_myq_unlock(entrance: str) -> dict[str, Any] | None:
    """Attempt Partner API unlock. Returns None if not configured."""
    if SIMULATE_MYQ_OPEN:
        return {
            "channel": "simulate",
            "status": "opened",
            "entrance_id": entrance or MYQ_ENTRANCE_ID or "main",
            "note": "SIMULATE_MYQ_OPEN=true — demo only, no physical unlock",
        }

    if not _myq_configured():
        return None

    entrance_id = (entrance or "").strip()
    if not entrance_id or entrance_id.lower() in {"main", "default"}:
        entrance_id = MYQ_ENTRANCE_ID

    path = MYQ_UNLOCK_PATH.format(
        facility_id=MYQ_FACILITY_ID,
        entrance_id=entrance_id,
    )
    url = f"{MYQ_API_BASE}{path}"
    payload = json.dumps({"reason": "welift_verified_open"}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MYQ_API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body) if body else {}
            except json.JSONDecodeError:
                parsed = {"raw": body}
            return {
                "channel": "myq_api",
                "status": "opened",
                "http_status": resp.status,
                "entrance_id": entrance_id,
                "response": parsed,
            }
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        log.warning("myQ unlock HTTP %s: %s", exc.code, err_body)
        return {
            "channel": "myq_api",
            "status": "error",
            "http_status": exc.code,
            "entrance_id": entrance_id,
            "error": err_body or str(exc),
        }
    except Exception as exc:  # noqa: BLE001
        log.exception("myQ unlock failed")
        return {
            "channel": "myq_api",
            "status": "error",
            "entrance_id": entrance_id,
            "error": str(exc),
        }


def _deny_message(detail: str) -> str:
    return (
        f"{detail} Do not open. Tell the visitor the host must add a myQ guest pass, "
        "then they may try again or call back. No human attendant is available on this line."
    )


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
        "service": "welift-autonomous-gate-webhooks",
        "version": VERSION,
        "mode": "autonomous" if AUTONOMOUS else "legacy_human_sms",
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
    unlock_ready = _myq_configured() or SIMULATE_MYQ_OPEN
    return {
        "status": "ok" if (guest_ok and (unlock_ready or not AUTONOMOUS)) else "degraded",
        "version": VERSION,
        "autonomous": AUTONOMOUS,
        "community_default": DEFAULT_COMMUNITY,
        "guest_list_ready": guest_ok,
        "myq_api_configured": _myq_configured(),
        "simulate_myq_open": SIMULATE_MYQ_OPEN,
        "unlock_ready": unlock_ready,
        "human_sms_fallback": HUMAN_SMS_FALLBACK,
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
    company = (args.get("company_name") or "").strip()
    visit_type = (args.get("visit_type") or "").strip().lower()

    # Autonomous night policy: ambiguous / ops → deny (log), never wake a human.
    if visit_type == "ops":
        result = {
            "decision": "deny",
            "confidence": "high",
            "message": _deny_message(
                "Ops / management call logged. Overnight AI does not open for ops."
            ),
            "community_name": community,
            "logged_for_daytime_review": True,
        }
        _append_event({"tool": "check_guest_list", "args": args, "result": result})
        return JSONResponse(result)

    # Residents should use keypad code or RFID sticker — AI is for vendors/workers.
    if visit_type == "resident":
        result = {
            "decision": "deny",
            "confidence": "high",
            "message": (
                "Caller claims to be a resident. Do not open via AI. Tell them to use "
                "their gate code on the keypad or their resident sticker/transponder. "
                "If those fail, they must contact management during business hours."
            ),
            "community_name": community,
        }
        _append_event({"tool": "check_guest_list", "args": args, "result": result})
        return JSONResponse(result)

    # Vendors/workers: person or company + where they're working. Social guests: name + host.
    is_vendorish = visit_type in {"vendor", "delivery", "worker"} or bool(company)
    if is_vendorish:
        if not visitor and not company:
            result = {
                "decision": "deny",
                "confidence": "low",
                "message": (
                    "Need worker name and/or company name for vendor entry. "
                    "Ask once more; if still incomplete, deny — do not open."
                ),
                "community_name": community,
            }
            _append_event({"tool": "check_guest_list", "args": args, "result": result})
            return JSONResponse(result)
        if not host:
            host = "association"
    elif not visitor or not host:
        result = {
            "decision": "deny",
            "confidence": "low",
            "message": (
                "Need both visitor name and host name or address. "
                "Ask once more; if still incomplete, deny — do not open."
            ),
            "community_name": community,
        }
        _append_event({"tool": "check_guest_list", "args": args, "result": result})
        return JSONResponse(result)

    try:
        book = _load_guest_list()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        result = {
            "decision": "deny",
            "confidence": "low",
            "message": _deny_message(f"Guest list unavailable ({exc})."),
            "community_name": community,
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
        visitor_ok = bool(visitor) and _names_match(
            visitor, entry.get("visitor_name", "")
        )
        company_ok = bool(company) and (
            _names_match(company, entry.get("company_name", ""))
            or _names_match(company, entry.get("visitor_name", ""))
        )
        # Vendor lists often authorize a company (any crew) or a named tech.
        identity_ok = visitor_ok or company_ok
        if is_vendorish and company and entry.get("company_name"):
            identity_ok = company_ok or (
                visitor_ok and _names_match(company, entry.get("company_name", ""))
            )
        host_ok = (
            _names_match(host, entry.get("host_name", ""))
            or _names_match(host, entry.get("host_address", ""))
            or (
                is_vendorish
                and _normalize(host)
                in {"association", "hoa", "community", "common areas", "commons"}
                and (entry.get("visit_type") or "").lower()
                in {"vendor", "delivery", "worker", ""}
            )
        )
        if identity_ok and host_ok:
            matches.append(entry)

    if len(matches) == 1:
        m = matches[0]
        entry_type = (m.get("visit_type") or "").lower()
        type_conflict = bool(
            visit_type
            and entry_type
            and visit_type != entry_type
            and (
                visit_type in {"delivery", "vendor"}
                or entry_type in {"delivery", "vendor"}
            )
        )
        if type_conflict:
            result = {
                "decision": "deny",
                "confidence": "medium",
                "message": _deny_message(
                    "Possible name match but visit type conflicts with the list."
                ),
                "matched_entry": {
                    "visitor_name": m.get("visitor_name"),
                    "company_name": m.get("company_name"),
                    "host_name": m.get("host_name"),
                    "host_address": m.get("host_address"),
                    "visit_type": m.get("visit_type"),
                },
                "community_name": community,
            }
        else:
            result = {
                "decision": "approve",
                "confidence": "high",
                "matched_entry": {
                    "visitor_name": m.get("visitor_name"),
                    "company_name": m.get("company_name"),
                    "host_name": m.get("host_name"),
                    "host_address": m.get("host_address"),
                    "visit_type": m.get("visit_type"),
                },
                "message": (
                    f"Approved: {m.get('company_name') or m.get('visitor_name')} "
                    f"({m.get('visitor_name')}) for "
                    f"{m.get('host_name')} ({m.get('host_address')}). "
                    f"Notes: {m.get('notes') or 'none'}. Call open_gate next."
                ),
                "community_name": community,
            }
    elif len(matches) > 1:
        result = {
            "decision": "deny",
            "confidence": "low",
            "message": _deny_message(
                f"Multiple guest-list matches ({len(matches)}) — too ambiguous."
            ),
            "community_name": community,
        }
    else:
        result = {
            "decision": "deny",
            "confidence": "high",
            "message": _deny_message("No guest-list match."),
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

    myq = _try_myq_unlock(entrance)
    if myq and myq.get("status") == "opened":
        result = {
            "status": "opened",
            "autonomous": True,
            "message": (
                "Gate unlock commanded. Tell visitor to wait for the gate to move. "
                "Do not mention a human attendant."
            ),
            "myq": myq,
        }
        _append_event({"tool": "open_gate", "args": args, "result": result})
        return JSONResponse(result)

    # Autonomous default: no human wake. Fail closed.
    if AUTONOMOUS and not HUMAN_SMS_FALLBACK:
        detail = (
            "myQ unlock failed."
            if myq and myq.get("status") == "error"
            else "myQ Partner API is not configured (set MYQ_* env vars)."
        )
        result = {
            "status": "failed",
            "autonomous": True,
            "message": (
                f"{detail} Do NOT claim the gate is opening. Do NOT say a human is "
                "coming. Apologize briefly and tell the visitor the host must send a "
                "myQ guest pass, then try the tablet again or call back."
            ),
            "myq": myq,
            "community_name": community,
            "visitor_name": visitor,
            "host_name_or_address": host,
            "reason": reason,
        }
        _append_event({"tool": "open_gate", "args": args, "result": result})
        return JSONResponse(result)

    # Legacy human SMS path (explicit opt-in only)
    sms_body = (
        f"[{community}] OPEN {visitor} visiting {host} @ {entrance}. "
        f"{reason or 'guest list approve'} — unlock myQ NOW."
    )
    sms = _send_sms(sms_body)
    result = {
        "status": "pending_human_open",
        "autonomous": False,
        "message": (
            "Legacy SMS fallback: on-call notified. Prefer disabling HUMAN_SMS_FALLBACK."
        ),
        "sms": sms,
        "myq": myq,
    }
    _append_event({"tool": "open_gate", "args": args, "result": result})
    return JSONResponse(result)


@app.post("/tools/escalate_to_oncall")
async def escalate_to_oncall(
    request: Request,
    x_retell_signature: str | None = Header(default=None),
) -> JSONResponse:
    """Kept for Retell tool compatibility. Autonomous: log + deny — no SMS wake."""
    payload = await _read_verified_json(request, x_retell_signature)
    args = _extract_args(payload)

    community = (args.get("community_name") or DEFAULT_COMMUNITY).strip()
    visitor = (args.get("visitor_name") or "").strip()
    host = (args.get("host_name_or_address") or "").strip()
    summary = (args.get("summary") or "escalation").strip()
    urgency = (args.get("urgency") or "normal").strip()

    log_entry = {
        "community": community,
        "visitor": visitor,
        "host": host,
        "summary": summary,
        "urgency": urgency,
    }

    if AUTONOMOUS and not HUMAN_SMS_FALLBACK:
        result = {
            "status": "logged_deny",
            "autonomous": True,
            "decision": "deny",
            "message": (
                "Logged for daytime review. Do not open. Do not say a human is on the "
                "way. Tell the visitor you cannot verify the visit right now and the "
                "host must add a myQ guest pass (or authorized vendor list)."
            ),
            "log": log_entry,
        }
        _append_event({"tool": "escalate_to_oncall", "args": args, "result": result})
        return JSONResponse(result)

    sms_body = (
        f"[{community}] ESCALATE ({urgency}) {visitor or 'n/a'} / "
        f"{host or 'n/a'}: {summary}"
    )
    sms = _send_sms(sms_body)
    result = {
        "status": "escalated" if sms.get("status") != "error" else "failed",
        "autonomous": False,
        "message": "Legacy SMS escalation sent.",
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
