#!/usr/bin/env python3
"""Smoke-test autonomous Retell tool webhooks (signature verify off)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("VERIFY_RETELL_SIGNATURES", "false")
os.environ.setdefault("DEFAULT_COMMUNITY", "The Inlets")
os.environ.setdefault("SERVERLESS", "true")
os.environ.setdefault("AUTONOMOUS", "true")
os.environ.setdefault("HUMAN_SMS_FALLBACK", "false")
os.environ.setdefault("SIMULATE_MYQ_OPEN", "true")

ROOT = Path(__file__).resolve().parents[1]
example = ROOT / "data" / "guest-list.example.json"
os.environ.setdefault("GUEST_LIST_PATH", str(example))

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def main_test() -> int:
    h = client.get("/health")
    assert h.status_code == 200, h.text
    body = h.json()
    assert body["status"] == "ok"
    assert body["autonomous"] is True
    assert body["unlock_ready"] is True
    assert body["version"] == "0.6.0"
    print("health OK", body)

    # Vendors require proof PIN — without it, ask for PIN (do not approve).
    r = client.post(
        "/tools/check_guest_list",
        json={
            "name": "check_guest_list",
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Mike Torres",
                "company_name": "GreenSide Lawn",
                "host_name_or_address": "common areas",
                "visit_type": "vendor",
            },
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["decision"] == "deny", r.json()
    assert r.json().get("needs_proof_code") is True
    print("check_guest_list VENDOR NEEDS_PROOF OK")

    send = client.post(
        "/access/send_code",
        json={"company_name": "GreenSide Lawn", "phone": "+19415559876", "override_window": True},
    )
    assert send.status_code == 200, send.text
    code = send.json()["code"]
    assert len(code) >= 4

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Mike Torres",
                "company_name": "GreenSide Lawn",
                "host_name_or_address": "common areas",
                "visit_type": "vendor",
                "proof_code": code,
            },
        },
    )
    assert r.json()["decision"] == "approve", r.json()
    print("check_guest_list VENDOR PROOF APPROVE OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Crew Member",
                "company_name": "GreenSide Lawn",
                "host_name_or_address": "association",
                "visit_type": "vendor",
                "proof_code": "000000",
            }
        },
    )
    assert r.json()["decision"] == "deny", r.json()
    print("check_guest_list WRONG PIN DENY OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Jordan Lee",
                "host_name_or_address": "Sam Rivera",
                "visit_type": "guest",
            },
        },
    )
    assert r.json()["decision"] == "approve", r.json()
    print("check_guest_list GUEST APPROVE OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Lee Jordan",
                "host_name_or_address": "12 Oak",
                "visit_type": "guest",
            }
        },
    )
    assert r.json()["decision"] == "approve", r.json()
    print("check_guest_list FUZZY APPROVE OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "visitor_name": "Resident Bob",
                "host_name_or_address": "12 Oak",
                "visit_type": "resident",
            }
        },
    )
    assert r.json()["decision"] == "deny", r.json()
    print("check_guest_list RESIDENT DENY OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Nobody",
                "host_name_or_address": "Unit 99",
                "visit_type": "guest",
            }
        },
    )
    assert r.json()["decision"] == "deny"
    print("check_guest_list DENY OK")

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Ops",
                "host_name_or_address": "CAM",
                "visit_type": "ops",
            }
        },
    )
    assert r.json()["decision"] == "deny", r.json()
    print("check_guest_list OPS DENY OK")

    r = client.post(
        "/tools/open_gate",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Mike Torres",
                "host_name_or_address": "common areas",
                "reason": "vendor approve",
            }
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "opened", r.json()
    assert r.json()["autonomous"] is True
    print("open_gate AUTONOMOUS OPEN OK", r.json()["myq"]["channel"])

    r = client.post(
        "/tools/escalate_to_oncall",
        json={
            "args": {
                "community_name": "The Inlets",
                "summary": "unclear names",
                "urgency": "normal",
                "visitor_name": "???",
            }
        },
    )
    assert r.json()["status"] == "logged_deny", r.json()
    assert r.json()["decision"] == "deny"
    print("escalate_to_oncall LOG+DENY OK")

    # Fail closed when simulate off and no myQ
    main.SIMULATE_MYQ_OPEN = False
    main.MYQ_API_BASE = ""
    r = client.post(
        "/tools/open_gate",
        json={
            "args": {
                "visitor_name": "Jordan Lee",
                "host_name_or_address": "Sam Rivera",
                "reason": "no api",
            }
        },
    )
    assert r.json()["status"] == "failed", r.json()
    print("open_gate FAIL-CLOSED OK")
    main.SIMULATE_MYQ_OPEN = True

    r = client.post("/retell/webhook", json={"event": "call_ended"})
    assert r.json()["ok"] is True
    print("retell/webhook OK")

    os.environ["GUEST_LIST_JSON"] = json.dumps(
        {
            "community_name": "The Inlets",
            "timezone": "America/New_York",
            "entries": [
                {
                    "visitor_name": "Test Visitor",
                    "host_name": "Host Person",
                    "host_address": "1 Main",
                    "visit_type": "guest",
                    "always_active": True,
                }
            ],
        }
    )
    main.GUEST_LIST_JSON = os.environ["GUEST_LIST_JSON"]
    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "visitor_name": "Test Visitor",
                "host_name_or_address": "Host Person",
                "visit_type": "guest",
            }
        },
    )
    assert r.json()["decision"] == "approve", r.json()
    print("GUEST_LIST_JSON APPROVE OK")

    print("ALL WEBHOOKS PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main_test())
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
