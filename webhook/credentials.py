"""We Lift credential + vendor roster engine backed by SQL database."""

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

from models import SessionLocal, VendorCompany, Credential, Delivery, Community

log = logging.getLogger("welift-credentials")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
SMS_LOG_ONLY = os.getenv("SMS_LOG_ONLY", "false").lower() in {"1", "true", "yes"}

_CODE_RE = re.compile(r"^\d{4,8}$")
_WINDOW_RE = re.compile(
    r"^(?P<days>[A-Za-z,\-\s]+)\s+(?P<start>\d{1,2}:\d{2})\s*-\s*(?P<end>\d{1,2}:\d{2})$"
)
_DAY_ALIASES = {
    "mon": 0, "monday": 0, "tue": 1, "tues": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2, "thu": 3, "thur": 3, "thurs": 3,
    "thursday": 3, "fri": 4, "friday": 4, "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
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
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    if raw.startswith("+"):
        return raw
    raise ValueError("Phone must be E.164 or 10-digit US number")

def load_vendors() -> dict[str, Any]:
    db = SessionLocal()
    try:
        comm = db.query(Community).first()
        tz = comm.timezone if comm else "America/New_York"
        comm_name = comm.name if comm else "The Inlets"
        return {
            "community_name": comm_name,
            "timezone": tz,
            "vendors": list_vendors(include_inactive=True),
        }
    finally:
        db.close()

def list_vendors(*, include_inactive: bool = False) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        query = db.query(VendorCompany)
        if not include_inactive:
            query = query.filter(VendorCompany.active == True)
        vendors = query.all()
        return [
            {
                "company_name": v.company_name,
                "access_contact_type": v.access_contact_type,
                "access_phone": v.access_phone,
                "invite_email": v.invite_email,
                "window": v.window,
                "notes": v.notes,
                "active": v.active,
            }
            for v in vendors
        ]
    finally:
        db.close()

def find_vendor(company_name: str, *, include_inactive: bool = False) -> dict[str, Any] | None:
    db = SessionLocal()
    try:
        norm_name = _normalize_company(company_name)
        if not norm_name:
            return None
        vendors = db.query(VendorCompany).all()
        for v in vendors:
            cn = _normalize_company(v.company_name)
            if cn == norm_name or norm_name in cn or cn in norm_name:
                if not include_inactive and not v.active:
                    return None
                return {
                    "company_name": v.company_name,
                    "access_contact_type": v.access_contact_type,
                    "access_phone": v.access_phone,
                    "invite_email": v.invite_email,
                    "window": v.window,
                    "notes": v.notes,
                    "active": v.active,
                }
        return None
    finally:
        db.close()

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
    return {
        "company_name": company,
        "access_contact_type": contact_type,
        "access_phone": phone,
        "window": window,
        "invite_email": (payload.get("invite_email") or "").strip() or None,
        "notes": (payload.get("notes") or "").strip() or None,
        "active": bool(payload.get("active", True)),
    }

def upsert_vendor(payload: dict[str, Any]) -> dict[str, Any]:
    data = _validate_vendor_payload(payload)
    db = SessionLocal()
    try:
        norm = _normalize_company(data["company_name"])
        vendors = db.query(VendorCompany).all()
        vendor = None
        for v in vendors:
            if _normalize_company(v.company_name) == norm:
                vendor = v
                break
        if vendor:
            vendor.company_name = data["company_name"]
            vendor.access_contact_type = data["access_contact_type"]
            vendor.access_phone = data["access_phone"]
            vendor.invite_email = data["invite_email"]
            vendor.window = data["window"]
            vendor.notes = data["notes"]
            vendor.active = data["active"]
        else:
            vendor = VendorCompany(
                company_name=data["company_name"],
                access_contact_type=data["access_contact_type"],
                access_phone=data["access_phone"],
                invite_email=data["invite_email"],
                window=data["window"],
                notes=data["notes"],
                active=data["active"]
            )
            db.add(vendor)
        db.commit()
        return {
            "company_name": vendor.company_name,
            "access_contact_type": vendor.access_contact_type,
            "access_phone": vendor.access_phone,
            "invite_email": vendor.invite_email,
            "window": vendor.window,
            "notes": vendor.notes,
            "active": vendor.active,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def set_vendor_active(company_name: str, active: bool) -> dict[str, Any]:
    db = SessionLocal()
    try:
        norm = _normalize_company(company_name)
        vendors = db.query(VendorCompany).all()
        vendor = None
        for v in vendors:
            if _normalize_company(v.company_name) == norm:
                vendor = v
                break
        if not vendor:
            raise ValueError(f"Vendor not found: {company_name}")
        vendor.active = active
        db.commit()
        return {
            "company_name": vendor.company_name,
            "access_contact_type": vendor.access_contact_type,
            "access_phone": vendor.access_phone,
            "invite_email": vendor.invite_email,
            "window": vendor.window,
            "notes": vendor.notes,
            "active": vendor.active,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

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
    except Exception:
        local = (when or _now()).astimezone(timezone.utc)

    m = _WINDOW_RE.match(window)
    if not m:
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
    except Exception:
        return _now() + timedelta(hours=12)

def _window_end_today(vendor: dict[str, Any] | None, tz_name: str) -> datetime:
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
    except Exception:
        return _end_of_local_day(tz_name)

def mint_credential(
    *,
    community: str,
    company_name: str,
    hours_valid: float | None = None,
    actor: str = "system",
) -> dict[str, Any]:
    db = SessionLocal()
    try:
        community = (community or "The Inlets").strip()
        company_name = (company_name or "").strip()
        if not company_name:
            raise ValueError("company_name required")

        vendor = find_vendor(company_name)
        display_company = vendor["company_name"] if vendor else company_name
        
        comm = db.query(Community).filter(Community.name == community).first()
        tz = comm.timezone if comm else "America/New_York"

        code = f"{secrets.randbelow(1_000_000):06d}"
        now = _now()
        if hours_valid is not None:
            expires = now + timedelta(hours=hours_valid)
        else:
            expires = _window_end_today(vendor, tz)

        norm = _normalize_company(display_company)
        
        active_creds = db.query(Credential).filter(
            Credential.status == "active",
            Credential.community == community
        ).all()
        for cred in active_creds:
            if cred.company_key == norm:
                cred.status = "rotated"

        now_naive = now.astimezone(timezone.utc).replace(tzinfo=None)
        expires_naive = expires.astimezone(timezone.utc).replace(tzinfo=None)

        cred_id = secrets.token_hex(8)
        new_cred = Credential(
            id=cred_id,
            community=community,
            company_name=display_company,
            company_key=norm,
            code_hash=_hash_code(code),
            last4=code[-4:],
            status="active",
            created_at=now_naive,
            valid_until=expires_naive,
            created_by=actor
        )
        db.add(new_cred)
        db.commit()

        return {
            "id": cred_id,
            "community": community,
            "company_name": display_company,
            "company_key": norm,
            "last4": code[-4:],
            "status": "active",
            "created_at": now.isoformat(),
            "valid_until": expires.isoformat(),
            "created_by": actor,
            "code": code,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def revoke_credential(
    *, community: str, company_name: str, actor: str = "system"
) -> int:
    db = SessionLocal()
    try:
        norm = _normalize_company(company_name)
        active_creds = db.query(Credential).filter(
            Credential.status == "active",
            Credential.community == community
        ).all()
        
        count = 0
        for cred in active_creds:
            if cred.company_key == norm:
                cred.status = "revoked"
                count += 1
                
        if count > 0:
            db.commit()
        return count
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def _active_credential(community: str, company_name: str) -> dict[str, Any] | None:
    db = SessionLocal()
    try:
        now = _now()
        company_key = _normalize_company(company_name)
        
        creds = db.query(Credential).filter(
            Credential.community == community,
            Credential.status == "active"
        ).all()
        
        for c in creds:
            until = c.valid_until
            if until.tzinfo is None:
                until = until.replace(tzinfo=timezone.utc)
            if now > until:
                continue
            if c.company_key == company_key:
                return {
                    "id": c.id,
                    "community": c.community,
                    "company_name": c.company_name,
                    "company_key": c.company_key,
                    "last4": c.last4,
                    "code_hash": c.code_hash,
                    "status": c.status,
                    "created_at": c.created_at.isoformat(),
                    "valid_until": c.valid_until.isoformat(),
                    "created_by": c.created_by,
                }
        return None
    finally:
        db.close()

def verify_proof(
    *, community: str, company_name: str, proof_code: str
) -> dict[str, Any]:
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
        except Exception as exc:
            log.exception("Twilio send failed")
            return {
                "channel": "twilio",
                "status": "error",
                "error": str(exc),
                "to": to,
                "to_masked": _mask_phone(to),
            }
    else:
        log.info("SMS (log-only) → %s | %s", _mask_phone(to), body.replace("\n", " | "))
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

    db = SessionLocal()
    try:
        now_naive = _now().astimezone(timezone.utc).replace(tzinfo=None)
        delivery = Delivery(
            id=secrets.token_hex(6),
            credential_id=cred_meta["id"],
            community=community,
            company_name=cred_meta["company_name"],
            to_masked=sms.get("to_masked"),
            channel=sms.get("channel"),
            status=sms.get("status"),
            actor=actor,
            ts=now_naive,
            last4=cred_meta.get("last4"),
            window_override=override_window,
        )
        db.add(delivery)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "ok": sms.get("status") in {"sent", "logged"},
        "community": community,
        "company_name": cred_meta["company_name"],
        "last4": cred_meta.get("last4"),
        "valid_until": cred_meta.get("valid_until"),
        "credential_id": cred_meta["id"],
        "sms": sms,
        "code": code,
    }

def list_deliveries(limit: int = 20) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        deliveries = db.query(Delivery).order_by(Delivery.ts.desc()).limit(limit).all()
        return [
            {
                "id": d.id,
                "credential_id": d.credential_id,
                "community": d.community,
                "company_name": d.company_name,
                "to_masked": d.to_masked,
                "channel": d.channel,
                "status": d.status,
                "actor": d.actor,
                "ts": d.ts.isoformat(),
                "last4": d.last4,
                "window_override": d.window_override,
            }
            for d in deliveries
        ]
    finally:
        db.close()

def list_active_credentials() -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        now = _now()
        creds = db.query(Credential).filter(Credential.status == "active").all()
        out = []
        for c in creds:
            until = c.valid_until
            if until.tzinfo is None:
                until = until.replace(tzinfo=timezone.utc)
            if now > until:
                continue
            out.append({
                "id": c.id,
                "community": c.community,
                "company_name": c.company_name,
                "company_key": c.company_key,
                "last4": c.last4,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
                "valid_until": c.valid_until.isoformat(),
                "created_by": c.created_by,
            })
        return out
    finally:
        db.close()

def list_recent_credentials(limit: int = 30) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        creds = db.query(Credential).order_by(Credential.created_at.desc()).limit(limit).all()
        return [
            {
                "id": c.id,
                "community": c.community,
                "company_name": c.company_name,
                "company_key": c.company_key,
                "last4": c.last4,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
                "valid_until": c.valid_until.isoformat(),
                "created_by": c.created_by,
            }
            for c in creds
        ]
    finally:
        db.close()

def twilio_configured() -> bool:
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER)
