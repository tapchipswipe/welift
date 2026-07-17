"""We Lift credential + vendor roster engine.

Persistent JSON stores (migrate to Postgres later):
- vendors.json — CAM-authorized companies (owner vs dispatch phones)
- credentials.json — hashed PINs + delivery audit

Plaintext code returned only at mint/send time.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import secrets
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("welift-credentials")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"

CREDENTIALS_PATH = Path(
    os.getenv("CREDENTIALS_PATH", str(DATA_DIR / "credentials.json"))
)
VENDORS_PATH = Path(os.getenv("VENDORS_PATH", str(DATA_DIR / "vendors.json")))
VENDORS_SEED_PATH = Path(
    os.getenv("VENDORS_SEED_PATH", str(DATA_DIR / "vendors.seed.json"))
)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
SMS_LOG_ONLY = os.getenv("SMS_LOG_ONLY", "false").lower() in {"1", "true", "yes"}

_CODE_RE = re.compile(r"^\d{4,8}$")
_WINDOW_RE = re.compile(
    r"^(?P<days>[A-Za-z,\-\s]+)\s+(?P<start>\d{1,2}:\d{2})\s*-\s*(?P<end>\d{1,2}:\d{2})$"
)
_DAY_ALIASES = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tues": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


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


def _empty_cred_store() -> dict[str, Any]:
    return {"credentials": [], "deliveries": []}


def load_store() -> dict[str, Any]:
    if not CREDENTIALS_PATH.exists():
        return _empty_cred_store()
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


def _default_vendor_book() -> dict[str, Any]:
    return {
        "community_name": "The Inlets",
        "timezone": "America/New_York",
        "notes": "CAM-authorized vendor roster",
        "vendors": [],
    }


def ensure_vendors_file() -> None:
    """Seed vendors.json from vendors.seed.json on first run."""
    if VENDORS_PATH.exists():
        return
    VENDORS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if VENDORS_SEED_PATH.exists():
        shutil.copy(VENDORS_SEED_PATH, VENDORS_PATH)
        log.info("Seeded vendor roster from %s", VENDORS_SEED_PATH)
    else:
        save_vendors(_default_vendor_book())


def load_vendors() -> dict[str, Any]:
    ensure_vendors_file()
    with VENDORS_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("community_name", "The Inlets")
    data.setdefault("timezone", "America/New_York")
    data.setdefault("vendors", [])
    return data


def save_vendors(book: dict[str, Any]) -> None:
    VENDORS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = VENDORS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(book, f, indent=2)
        f.write("\n")
    tmp.replace(VENDORS_PATH)


def list_vendors(*, include_inactive: bool = False) -> list[dict[str, Any]]:
    book = load_vendors()
    out = []
    for v in book.get("vendors", []):
        if not include_inactive and v.get("active") is False:
            continue
        out.append(v)
    return out


def find_vendor(company_name: str, *, include_inactive: bool = False) -> dict[str, Any] | None:
    target = _normalize_company(company_name)
    if not target:
        return None
    for v in list_vendors(include_inactive=include_inactive):
        cn = _normalize_company(v.get("company_name", ""))
        if cn == target or target in cn or cn in target:
            return v
    return None


def _validate_vendor_payload(payload: dict[str, Any], *, partial: bool = False) -> dict[str, Any]:
    company = (payload.get("company_name") or "").strip()
    if not company and not partial:
        raise ValueError("company_name required")
    contact_type = (payload.get("access_contact_type") or "owner").strip().lower()
    if contact_type not in {"owner", "dispatch"}:
        raise ValueError("access_contact_type must be owner or dispatch")
    phone_raw = (payload.get("access_phone") or "").strip()
    phone = _ensure_e164(phone_raw) if phone_raw else ""
    if not phone and not partial:
        raise ValueError("access_phone required")
    window = (payload.get("window") or "Mon-Fri 07:00-18:00").strip()
    out: dict[str, Any] = {
        "company_name": company,
        "access_contact_type": contact_type,
        "access_phone": phone,
        "window": window,
        "invite_email": (payload.get("invite_email") or "").strip() or None,
        "notes": (payload.get("notes") or "").strip() or None,
        "active": bool(payload.get("active", True)),
    }
    return out


def upsert_vendor(payload: dict[str, Any]) -> dict[str, Any]:
    """Create or update a vendor by company_name (case-insensitive)."""
    data = _validate_vendor_payload(payload)
    book = load_vendors()
    norm = _normalize_company(data["company_name"])
    now = _iso(_now())
    for i, v in enumerate(book["vendors"]):
        if _normalize_company(v.get("company_name", "")) == norm:
            updated = {**v, **data, "updated_at": now}
            if not updated.get("created_at"):
                updated["created_at"] = now
            book["vendors"][i] = updated
            save_vendors(book)
            return updated
    record = {**data, "created_at": now, "updated_at": now}
    book["vendors"].append(record)
    save_vendors(book)
    return record


def set_vendor_active(company_name: str, active: bool) -> dict[str, Any]:
    book = load_vendors()
    norm = _normalize_company(company_name)
    for i, v in enumerate(book["vendors"]):
        if _normalize_company(v.get("company_name", "")) == norm:
            v["active"] = active
            v["updated_at"] = _iso(_now())
            book["vendors"][i] = v
            save_vendors(book)
            return v
    raise ValueError(f"Vendor not found: {company_name}")


def _parse_days(days_part: str) -> set[int]:
    days_part = days_part.strip().lower().replace(" ", "")
    if not days_part or days_part in {"daily", "everyday", "as-needed", "asneeded", "any"}:
        return {0, 1, 2, 3, 4, 5, 6}
    out: set[int] = set()
    for chunk in days_part.split(","):
        if "-" in chunk and not chunk.startswith("-"):
            a, b = chunk.split("-", 1)
            if a in _DAY_ALIASES and b in _DAY_ALIASES:
                start, end = _DAY_ALIASES[a], _DAY_ALIASES[b]
                if start <= end:
                    out.update(range(start, end + 1))
                else:
                    out.update(list(range(start, 7)) + list(range(0, end + 1)))
                continue
        if chunk in _DAY_ALIASES:
            out.add(_DAY_ALIASES[chunk])
    return out or {0, 1, 2, 3, 4, 5, 6}


def _parse_hhmm(value: str) -> tuple[int, int]:
    h, m = value.split(":")
    return int(h), int(m)


def vendor_window_allows(
    vendor: dict[str, Any] | None,
    *,
    when: datetime | None = None,
    tz_name: str | None = None,
) -> dict[str, Any]:
    """Check if now falls in vendor's authorized window."""
    if not vendor:
        return {"ok": True, "reason": "unknown_vendor_no_window"}
    window = (vendor.get("window") or "").strip()
    if not window or window.lower() in {"as-needed", "as needed", "any", "always"}:
        return {"ok": True, "reason": "as_needed"}

    book = load_vendors()
    tz = tz_name or book.get("timezone") or "America/New_York"
    try:
        from zoneinfo import ZoneInfo

        local = (when or _now()).astimezone(ZoneInfo(tz))
    except Exception:  # noqa: BLE001
        local = (when or _now()).astimezone(timezone.utc)

    m = _WINDOW_RE.match(window)
    if not m:
        # Unparseable → allow (CAM free-text) but note it
        return {"ok": True, "reason": "unparsed_window", "window": window}

    days = _parse_days(m.group("days"))
    if local.weekday() not in days:
        return {
            "ok": False,
            "reason": "outside_days",
            "window": window,
            "local": local.isoformat(),
        }

    sh, sm = _parse_hhmm(m.group("start"))
    eh, em = _parse_hhmm(m.group("end"))
    minutes = local.hour * 60 + local.minute
    start_m = sh * 60 + sm
    end_m = eh * 60 + em
    if start_m <= end_m:
        in_hours = start_m <= minutes <= end_m
    else:
        # overnight window
        in_hours = minutes >= start_m or minutes <= end_m
    if not in_hours:
        return {
            "ok": False,
            "reason": "outside_hours",
            "window": window,
            "local": local.isoformat(),
        }
    return {"ok": True, "reason": "in_window", "window": window}


def _end_of_local_day(tz_name: str = "America/New_York") -> datetime:
    try:
        from zoneinfo import ZoneInfo

        local = datetime.now(ZoneInfo(tz_name))
        end = local.replace(hour=23, minute=59, second=59, microsecond=0)
        return end.astimezone(timezone.utc)
    except Exception:  # noqa: BLE001
        return _now() + timedelta(hours=12)


def _window_end_today(vendor: dict[str, Any] | None, tz_name: str) -> datetime:
    """Expire at end of today's window hours when parseable, else end of local day."""
    if not vendor:
        return _end_of_local_day(tz_name)
    window = (vendor.get("window") or "").strip()
    m = _WINDOW_RE.match(window)
    if not m:
        return _end_of_local_day(tz_name)
    try:
        from zoneinfo import ZoneInfo

        local = datetime.now(ZoneInfo(tz_name))
        eh, em = _parse_hhmm(m.group("end"))
        end = local.replace(hour=eh, minute=em, second=0, microsecond=0)
        if end < local:
            end = end + timedelta(days=1)
        return end.astimezone(timezone.utc)
    except Exception:  # noqa: BLE001
        return _end_of_local_day(tz_name)


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
    tz = load_vendors().get("timezone") or "America/New_York"

    code = f"{secrets.randbelow(1_000_000):06d}"
    now = _now()
    if hours_valid is not None:
        expires = now + timedelta(hours=hours_valid)
    else:
        expires = _window_end_today(vendor, tz)

    store = load_store()
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
    phone: str | None = None,
    actor: str = "access_ui",
    reuse_active: bool = False,
    override_window: bool = False,
) -> dict[str, Any]:
    """Mint (rotate) credential and SMS to roster phone or override phone.

    Default: always rotate on send so CAM gets a fresh code and we know plaintext.
    """
    community = (community or "The Inlets").strip()
    company_name = (company_name or "").strip()
    vendor = find_vendor(company_name)
    if vendor and vendor.get("active") is False:
        raise ValueError("Vendor is deactivated — reactivate before sending a code")

    window_check = vendor_window_allows(vendor)
    if not window_check.get("ok") and not override_window:
        raise ValueError(
            f"Outside authorized window ({window_check.get('window')}). "
            "Pass override_window=true for CAM emergency send."
        )

    to_raw = (phone or "").strip() or (vendor or {}).get("access_phone") or ""
    to = _ensure_e164(to_raw)

    if reuse_active:
        active = _active_credential(community, company_name)
        if active:
            # Cannot resend unknown plaintext — rotate
            pass

    minted = mint_credential(
        community=community, company_name=company_name, actor=actor
    )
    code = minted["code"]
    cred_meta = minted

    until_local = cred_meta.get("valid_until", "")
    contact = (vendor or {}).get("access_contact_type") or "access"
    body = (
        f"{community} — {cred_meta['company_name']} vendor access\n"
        f"Keypad code: {code}\n"
        f"Valid until (UTC): {until_local}\n"
        f"If keypad fails: Call Attendant, say company + this PIN.\n"
        f"(Sent to {contact} contact)"
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
        "window_override": override_window,
    }
    if sms.get("sid"):
        delivery["sid"] = sms["sid"]
    if sms.get("error"):
        delivery["error"] = sms["error"]
    store["deliveries"].append(delivery)
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
        "window": window_check,
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


def list_recent_credentials(limit: int = 30) -> list[dict[str, Any]]:
    store = load_store()
    items = sorted(
        store.get("credentials", []),
        key=lambda c: c.get("created_at", ""),
        reverse=True,
    )
    return [{k: v for k, v in c.items() if k != "code_hash"} for c in items[:limit]]


def twilio_configured() -> bool:
    return bool(
        TWILIO_ACCOUNT_SID
        and TWILIO_AUTH_TOKEN
        and TWILIO_FROM_NUMBER
        and not SMS_LOG_ONLY
    )
