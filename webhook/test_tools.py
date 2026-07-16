#!/usr/bin/env python3
"""Smoke-test all Retell tool webhooks (signature verify off)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("VERIFY_RETELL_SIGNATURES", "false")
os.environ.setdefault("ONCALL_PHONE", "+19415551234")
os.environ.setdefault("DEFAULT_COMMUNITY", "The Inlets")
os.environ.setdefault("SERVERLESS", "true")

# Prefer example guest list so tests don't need a local copy
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
    assert body["community_default"] == "The Inlets"
    print("health OK", body)

    r = client.post(
        "/tools/check_guest_list",
        json={
            "name": "check_guest_list",
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Jordan Lee",
                "host_name_or_address": "Sam Rivera",
                "visit_type": "guest",
            },
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["decision"] == "approve", r.json()
    print("check_guest_list APPROVE OK", r.json()["decision"])

    # Token-order / partial host address match
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
                "community_name": "The Inlets",
                "visitor_name": "Nobody",
                "host_name_or_address": "Unit 99",
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
    assert r.json()["decision"] == "escalate"
    print("check_guest_list OPS ESCALATE OK")

    r = client.post(
        "/tools/open_gate",
        json={
            "args": {
                "community_name": "The Inlets",
                "visitor_name": "Jordan Lee",
                "host_name_or_address": "Sam Rivera",
                "reason": "test open",
            }
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "pending_human_open"
    print("open_gate OK", r.json()["status"])

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
    assert r.json()["status"] == "escalated"
    print("escalate_to_oncall OK")

    r = client.post("/retell/webhook", json={"event": "call_ended"})
    assert r.json()["ok"] is True
    print("retell/webhook OK")

    # Inline guest list via env (serverless path)
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
    # Reload module env-backed constants used at request time via GUEST_LIST_JSON
    main.GUEST_LIST_JSON = os.environ["GUEST_LIST_JSON"]
    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "visitor_name": "Test Visitor",
                "host_name_or_address": "Host Person",
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
