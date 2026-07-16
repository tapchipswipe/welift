"""We Lift credential engine — mint, SMS, revoke, verify proof PINs.

Persistent JSON store (migrate to Postgres later). One active code per
community × company per day window. Plaintext code returned only at mint/send time;
store keeps code_hash + last4.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("welift-credentials")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"

CREDENTIALS_PATH = Path(
    os.getenv("CREDENTIALS_PATH", str(DATA_DIR / "credentials.json"))
)
VENDORS_PATH = Path(os.getenv("VENDORS_PATH", str(DATA_DIR / "vendors.seed.json")))

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

# Allow log-only SMS when Twilio unset (local/dev); still mints real codes
SMS_LOG_ONLY = os.getenv("SMS_LOG_ONLY", "false").lower() in {"1", "true", "yes"}

_CODE_RE = re.compile(r"^\d{4,8}$")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _normalize_company(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _mask_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) < 4:
        return "····"
    return f"···{digits[-4:]}"


def _ensure_e164(phone: str) -> str:
    raw = (phone or "").strip()
    if not raw:
        raise ValueError("Phone number required")
    digits = re.sub(r"\D", "", raw)
    if raw.startswith("+") and len(digits) >= 10:
        return "+" + digits
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    if raw.startswith("+"):
        return raw
    raise ValueError("Phone must be E.164 or 10-digit US number")


def _empty_store() -> dict[str, Any]:
    return {"credentials": [], "deliveries": []}


def load_store() -> dict[str, Any]:
    if not CREDENTIALS_PATH.exists():
        return _empty_store()
    with CREDENTIALS_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("credentials", [])
    data.setdefault("deliveries", [])
    return data


def save_store(store: dict[str, Any]) -> None:
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = CREDENTIALS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)
        f.write("\n")
    tmp.replace(CREDENTIALS_PATH)


def load_vendors() -> dict[str, Any]:
    if not VENDORS_PATH.exists():
        return {
            "community_name": "The Inlets",
            "timezone": "America/New_York",
            "vendors": [],
        }
    with VENDORS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def find_vendor(company_name: str) -> dict[str, Any] | None:
    book = load_vendors()
    target = _normalize_company(company_name)
    if not target:
        return None
    for v in book.get("vendors", []):
        if _normalize_company(v.get("company_name", "")) == target:
            return v
        # fuzzy contains
        cn = _normalize_company(v.get("company_name", ""))
        if target in cn or cn in target:
            return v
    return None


def _end_of_local_day(tz_name: str = "America/New_York") -> datetime:
    try:
        from zoneinfo import ZoneInfo

        local = datetime.now(ZoneInfo(tz_name))
        end = local.replace(hour=23, minute=59, second=59, microsecond=0)
        return end.astimezone(timezone.utc)
    except Exception:  # noqa: BLE001
        return _now() + timedelta(hours=12)


def mint_credential(
    *,
    community: str,
    company_name: str,
    hours_valid: float | None = None,
    actor: str = "system",
) -> dict[str, Any]:
    """Create or rotate today's credential. Returns dict including plaintext `code` once."""
    community = (community or "The Inlets").strip()
    company_name = (company_name or "").strip()
    if not company_name:
        raise ValueError("company_name required")

    vendor = find_vendor(company_name)
    display_company = vendor["company_name"] if vendor else company_name

    code = f"{secrets.randbelow(1_000_000):06d}"
    now = _now()
    if hours_valid is not None:
        expires = now + timedelta(hours=hours_valid)
    else:
        expires = _end_of_local_day(
            (load_vendors().get("timezone") or "America/New_York")
        )

    store = load_store()
    # Revoke prior active for same community×company
    norm = _normalize_company(display_company)
    for cred in store["credentials"]:
        if (
            cred.get("status") == "active"
            and cred.get("community") == community
            and _normalize_company(cred.get("company_name", "")) == norm
        ):
            cred["status"] = "rotated"
            cred["revoked_at"] = _iso(now)

    record = {
        "id": secrets.token_hex(8),
        "community": community,
        "company_name": display_company,
        "company_key": norm,
        "code_hash": _hash_code(code),
        "last4": code[-4:],
        "status": "active",
        "created_at": _iso(now),
        "valid_until": _iso(expires),
        "created_by": actor,
    }
    store["credentials"].append(record)
    save_store(store)

    return {
        **{k: v for k, v in record.items() if k != "code_hash"},
        "code": code,
    }


def revoke_credential(
    *, community: str, company_name: str, actor: str = "system"
) -> int:
    store = load_store()
    now = _now()
    norm = _normalize_company(company_name)
    count = 0
    for cred in store["credentials"]:
        if (
            cred.get("status") == "active"
            and cred.get("community") == community
            and _normalize_company(cred.get("company_name", "")) == norm
        ):
            cred["status"] = "revoked"
            cred["revoked_at"] = _iso(now)
            cred["revoked_by"] = actor
            count += 1
    if count:
        save_store(store)
    return count


def _active_credential(community: str, company_name: str) -> dict[str, Any] | None:
    store = load_store()
    now = _now()
    norm = _normalize_company(company_name)
    candidates = [
        c
        for c in store["credentials"]
        if c.get("status") == "active"
        and c.get("community") == community
        and _normalize_company(c.get("company_name", "")) == norm
    ]
    if not candidates:
        # also try fuzzy vendor resolve
        vendor = find_vendor(company_name)
        if vendor:
            norm2 = _normalize_company(vendor["company_name"])
            candidates = [
                c
                for c in store["credentials"]
                if c.get("status") == "active"
                and c.get("community") == community
                and _normalize_company(c.get("company_name", "")) == norm2
            ]
    if not candidates:
        return None
    # newest
    candidates.sort(key=lambda c: c.get("created_at", ""), reverse=True)
    cred = candidates[0]
    until = _parse_iso(cred.get("valid_until"))
    if until and now > until:
        return None
    return cred


def verify_proof(
    *, community: str, company_name: str, proof_code: str
) -> dict[str, Any]:
    """Return ok=True if proof matches active credential."""
    code = re.sub(r"\s+", "", (proof_code or "").strip())
    if not _CODE_RE.match(code):
        return {"ok": False, "reason": "invalid_format"}
    cred = _active_credential(community, company_name)
    if not cred:
        return {"ok": False, "reason": "no_active_credential"}
    if cred["code_hash"] != _hash_code(code):
        return {"ok": False, "reason": "mismatch", "last4": cred.get("last4")}
    return {
        "ok": True,
        "credential_id": cred["id"],
        "company_name": cred["company_name"],
        "last4": cred.get("last4"),
        "valid_until": cred.get("valid_until"),
    }


def send_sms(to_phone: str, body: str) -> dict[str, Any]:
    to = _ensure_e164(to_phone)
    if (
        TWILIO_ACCOUNT_SID
        and TWILIO_AUTH_TOKEN
        and TWILIO_FROM_NUMBER
        and not SMS_LOG_ONLY
    ):
        try:
            from twilio.rest import Client

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            msg = client.messages.create(body=body, from_=TWILIO_FROM_NUMBER, to=to)
            return {
                "channel": "twilio",
                "status": "sent",
                "sid": msg.sid,
                "to": to,
                "to_masked": _mask_phone(to),
            }
        except Exception as exc:  # noqa: BLE001
            log.exception("Twilio send failed")
            return {
                "channel": "twilio",
                "status": "error",
                "error": str(exc),
                "to": to,
                "to_masked": _mask_phone(to),
            }

    log.info("SMS (log-only) → %s | %s", _mask_phone(to), body)
    return {
        "channel": "log",
        "status": "logged",
        "to": to,
        "to_masked": _mask_phone(to),
        "body": body,
    }


def send_code(
    *,
    community: str,
    company_name: str,
    phone: str,
    actor: str = "access_ui",
    reuse_active: bool = True,
) -> dict[str, Any]:
    """Mint (or reuse active) credential and SMS it to phone."""
    community = (community or "The Inlets").strip()
    company_name = (company_name or "").strip()
    to = _ensure_e164(phone)

    code: str
    cred_meta: dict[str, Any]
    active = _active_credential(community, company_name) if reuse_active else None
    if active and reuse_active:
        # Need plaintext to resend — remint/rotate for simplicity so we always know code
        minted = mint_credential(
            community=community, company_name=company_name, actor=actor
        )
        code = minted["code"]
        cred_meta = minted
    else:
        minted = mint_credential(
            community=community, company_name=company_name, actor=actor
        )
        code = minted["code"]
        cred_meta = minted

    until_local = cred_meta.get("valid_until", "")
    body = (
        f"{community} — {cred_meta['company_name']} vendor access\n"
        f"Keypad code: {code}\n"
        f"Valid until (UTC): {until_local}\n"
        f"If keypad fails: Call Attendant, say company + this PIN."
    )
    sms = send_sms(to, body)

    store = load_store()
    delivery = {
        "id": secrets.token_hex(6),
        "credential_id": cred_meta["id"],
        "community": community,
        "company_name": cred_meta["company_name"],
        "to_masked": sms.get("to_masked"),
        "channel": sms.get("channel"),
        "status": sms.get("status"),
        "actor": actor,
        "ts": _iso(_now()),
        "last4": cred_meta.get("last4"),
    }
    if sms.get("sid"):
        delivery["sid"] = sms["sid"]
    if sms.get("error"):
        delivery["error"] = sms["error"]
    store["deliveries"].append(delivery)
    # keep last 200
    store["deliveries"] = store["deliveries"][-200:]
    save_store(store)

    return {
        "ok": sms.get("status") in {"sent", "logged"},
        "community": community,
        "company_name": cred_meta["company_name"],
        "last4": cred_meta.get("last4"),
        "valid_until": cred_meta.get("valid_until"),
        "credential_id": cred_meta["id"],
        "sms": sms,
        "delivery": delivery,
        # plaintext only in API response for presenter confirmation — not stored again
        "code": code,
    }


def list_deliveries(limit: int = 20) -> list[dict[str, Any]]:
    store = load_store()
    items = list(reversed(store.get("deliveries", [])))
    return items[:limit]


def list_active_credentials() -> list[dict[str, Any]]:
    store = load_store()
    now = _now()
    out = []
    for c in store.get("credentials", []):
        if c.get("status") != "active":
            continue
        until = _parse_iso(c.get("valid_until"))
        if until and now > until:
            continue
        out.append({k: v for k, v in c.items() if k != "code_hash"})
    return out
