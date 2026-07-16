#!/usr/bin/env python3
"""Smoke-test all Retell tool webhooks (signature verify off)."""

from __future__ import annotations

import os
import sys

os.environ.setdefault("VERIFY_RETELL_SIGNATURES", "false")
os.environ.setdefault("ONCALL_PHONE", "+19415551234")

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def main_test() -> int:
    h = client.get("/health")
    assert h.status_code == 200, h.text
    assert h.json()["status"] == "ok"
    print("health OK", h.json())

    r = client.post(
        "/tools/check_guest_list",
        json={
            "name": "check_guest_list",
            "args": {
                "community_name": "Pilot HOA",
                "visitor_name": "Jordan Lee",
                "host_name_or_address": "Sam Rivera",
                "visit_type": "guest",
            },
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["decision"] == "approve", r.json()
    print("check_guest_list APPROVE OK", r.json()["decision"])

    r = client.post(
        "/tools/check_guest_list",
        json={
            "args": {
                "community_name": "Pilot HOA",
                "visitor_name": "Nobody",
                "host_name_or_address": "Unit 99",
            }
        },
    )
    assert r.json()["decision"] == "deny"
    print("check_guest_list DENY OK")

    r = client.post(
        "/tools/open_gate",
        json={
            "args": {
                "community_name": "Pilot HOA",
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
                "community_name": "Pilot HOA",
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
    print("ALL WEBHOOKS PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main_test())
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
