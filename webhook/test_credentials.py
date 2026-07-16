#!/usr/bin/env python3
"""Tests for credential engine + access + vendor proof PIN."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

# Isolate store before importing modules
TMP = Path(tempfile.mkdtemp())
os.environ["CREDENTIALS_PATH"] = str(TMP / "credentials.json")
os.environ["VENDORS_PATH"] = str(
    Path(__file__).resolve().parents[1] / "data" / "vendors.seed.json"
)
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


def test_send_code_api() -> None:
    r = client.post(
        "/access/send_code",
        json={
            "company_name": "GreenSide Lawn",
            "phone": "9415559999",
            "community_name": "The Inlets",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["sms"]["status"] == "logged"
    assert len(body["code"]) == 6
    print("send_code API OK", body["last4"])


def test_vendor_proof_retell() -> None:
    sent = client.post(
        "/access/send_code",
        json={"company_name": "AquaClear Pools", "phone": "+19415551212"},
    ).json()
    code = sent["code"]

    # missing proof
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

    # wrong proof
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

    # good proof
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


def test_access_page() -> None:
    r = client.get("/access")
    assert r.status_code == 200
    assert "We Lift" in r.text
    meta = client.get("/access/meta")
    assert meta.status_code == 200
    assert len(meta.json()["vendors"]) >= 1
    print("access UI OK")


def main_test() -> int:
    h = client.get("/health")
    assert h.status_code == 200
    assert h.json()["version"] == "0.5.0"
    print("health OK", h.json()["version"])
    test_mint_verify_revoke()
    test_send_code_api()
    test_vendor_proof_retell()
    test_access_page()
    print("ALL CREDENTIAL/ACCESS TESTS PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main_test())
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
