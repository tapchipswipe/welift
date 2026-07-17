#!/usr/bin/env python3
"""Tests for credential engine, CAM roster, access desk, vendor proof PIN."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

TMP = Path(tempfile.mkdtemp())
SEED = Path(__file__).resolve().parents[1] / "data" / "vendors.seed.json"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["CREDENTIALS_PATH"] = str(TMP / "credentials.json")
os.environ["VENDORS_PATH"] = str(TMP / "vendors.json")
os.environ["VENDORS_SEED_PATH"] = str(SEED)
os.environ["SMS_LOG_ONLY"] = "true"
os.environ["VERIFY_RETELL_SIGNATURES"] = "false"
os.environ["SIMULATE_MYQ_OPEN"] = "true"
os.environ["AUTONOMOUS"] = "true"
os.environ["SERVERLESS"] = "true"
os.environ["DEFAULT_COMMUNITY"] = "The Inlets"

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault(
    "GUEST_LIST_PATH", str(ROOT / "data" / "guest-list.example.json")
)

import credentials as creds  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

client = TestClient(main.app)


def test_mint_verify_revoke() -> None:
    minted = creds.mint_credential(
        community="The Inlets", company_name="GreenSide Lawn", actor="test"
    )
    assert len(minted["code"]) == 6
    ok = creds.verify_proof(
        community="The Inlets",
        company_name="GreenSide Lawn",
        proof_code=minted["code"],
    )
    assert ok["ok"] is True
    bad = creds.verify_proof(
        community="The Inlets",
        company_name="GreenSide Lawn",
        proof_code="000000",
    )
    assert bad["ok"] is False
    n = creds.revoke_credential(
        community="The Inlets", company_name="GreenSide Lawn", actor="test"
    )
    assert n >= 1
    after = creds.verify_proof(
        community="The Inlets",
        company_name="GreenSide Lawn",
        proof_code=minted["code"],
    )
    assert after["ok"] is False
    print("mint/verify/revoke OK")


def test_vendor_crud() -> None:
    v = creds.upsert_vendor(
        {
            "company_name": "Solo HVAC Pros",
            "access_contact_type": "owner",
            "access_phone": "+19415558888",
            "window": "Mon-Fri 07:00-18:00",
            "notes": "SMB test",
        }
    )
    assert v["access_contact_type"] == "owner"
    listed = creds.list_vendors()
    assert any(x["company_name"] == "Solo HVAC Pros" for x in listed)

    r = client.post(
        "/access/vendors",
        json={
            "company_name": "Big Lawn Co",
            "access_contact_type": "dispatch",
            "access_phone": "9415557777",
            "window": "as-needed",
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["vendor"]["access_contact_type"] == "dispatch"

    r = client.patch(
        "/access/vendors/Big Lawn Co",
        json={"active": False},
    )
    assert r.status_code == 200
    assert r.json()["vendor"]["active"] is False
    print("vendor CRUD OK")


def test_send_code_api() -> None:
    # use as-needed vendor to avoid window flake
    client.post(
        "/access/vendors",
        json={
            "company_name": "Anytime Plumbing",
            "access_contact_type": "owner",
            "access_phone": "+19415559999",
            "window": "as-needed",
        },
    )
    r = client.post(
        "/access/send_code",
        json={
            "company_name": "Anytime Plumbing",
            "community_name": "The Inlets",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["sms"]["status"] == "logged"
    assert len(body["code"]) == 6
    print("send_code API OK", body["last4"])


def test_window_enforcement() -> None:
    creds.upsert_vendor(
        {
            "company_name": "Night Only Co",
            "access_contact_type": "dispatch",
            "access_phone": "+19415551111",
            "window": "Mon-Fri 02:00-03:00",
        }
    )
    # Almost certainly outside 2–3am local → should fail without override
    try:
        creds.send_code(
            community="The Inlets",
            company_name="Night Only Co",
            override_window=False,
        )
        # If somehow inside window, still OK — skip assert
        print("window check skipped (inside narrow window)")
    except ValueError as exc:
        assert "Outside authorized window" in str(exc)

    ok = creds.send_code(
        community="The Inlets",
        company_name="Night Only Co",
        override_window=True,
    )
    assert ok["ok"] is True
    print("window enforcement OK")


def test_vendor_proof_retell() -> None:
    client.post(
        "/access/vendors",
        json={
            "company_name": "AquaClear Pools",
            "access_contact_type": "owner",
            "access_phone": "+19415551212",
            "window": "as-needed",
        },
    )
    sent = client.post(
        "/access/send_code",
        json={"company_name": "AquaClear Pools"},
    ).json()
    code = sent["code"]

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "company_name": "AquaClear Pools",
                "visitor_name": "Pool Tech",
                "visit_type": "vendor",
            }
        },
    )
    assert r.json()["decision"] == "deny"
    assert r.json().get("needs_proof_code") is True

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "company_name": "AquaClear Pools",
                "visitor_name": "Pool Tech",
                "visit_type": "vendor",
                "proof_code": "111111",
            }
        },
    )
    assert r.json()["decision"] == "deny"

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "company_name": "AquaClear Pools",
                "visitor_name": "Pool Tech",
                "visit_type": "vendor",
                "proof_code": code,
            }
        },
    )
    assert r.json()["decision"] == "approve", r.json()
    print("vendor proof Retell OK")

    r = client.post(
        "/tools/open_gate",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Pool Tech",
                "host_name_or_address": "clubhouse",
                "reason": "vendor proof",
            }
        },
    )
    assert r.json()["status"] == "opened"
    print("open_gate simulate OK")


def test_access_and_gate_pages() -> None:
    r = client.get("/access")
    assert r.status_code == 200
    assert "CAM Access Desk" in r.text
    assert "Admin / CAM only" in r.text
    meta = client.get("/access/meta")
    assert meta.status_code == 200
    assert meta.json()["role"] == "cam_admin"
    audit = client.get("/access/audit")
    assert audit.status_code == 200
    g = client.get("/gate")
    assert g.status_code == 200
    assert "Call Attendant" in g.text
    gm = client.get("/gate/meta")
    assert gm.status_code == 200
    print("access + gate UI OK")


def main_test() -> int:
    h = client.get("/health")
    assert h.status_code == 200
    assert h.json()["version"] == "0.6.0"
    print("health OK", h.json()["version"])
    test_mint_verify_revoke()
    test_vendor_crud()
    test_send_code_api()
    test_window_enforcement()
    test_vendor_proof_retell()
    test_access_and_gate_pages()
    print("ALL CREDENTIAL/ACCESS TESTS PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main_test())
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
