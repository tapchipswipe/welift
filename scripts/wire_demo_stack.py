#!/usr/bin/env python3
"""Deploy webhook to Railway + wire Retell tools/DID for cell demos.

Requires env:
  RETELL_API_KEY
  RAILWAY_TOKEN   (or a prior `railway login`)

Usage (from repo root):
  python3 scripts/wire_demo_stack.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBHOOK = ROOT / "webhook"
GUEST_EXAMPLE = ROOT / "data" / "guest-list.example.json"
SERVICE = "welift-webhook"
RAILWAY_BIN = os.path.expanduser("~/.railway/bin/railway")


def _run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = os.path.expanduser("~/.railway/bin") + ":" + env.get("PATH", "")
    print("+", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=check,
    )


def _railway(args: list[str], *, cwd: Path | None = None, check: bool = True) -> str:
    bin_path = RAILWAY_BIN if Path(RAILWAY_BIN).exists() else "railway"
    cp = _run([bin_path, *args], cwd=cwd, check=check)
    out = (cp.stdout or "") + (cp.stderr or "")
    if cp.returncode != 0 and check:
        print(out)
        raise RuntimeError(f"railway {' '.join(args)} failed ({cp.returncode})")
    return out


def _http_json(method: str, url: str, *, headers: dict | None = None, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            **(headers or {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"{method} {url} -> {e.code}: {err}") from e


def ensure_creds() -> str:
    key = os.environ.get("RETELL_API_KEY", "").strip()
    if not key or key.startswith("key_xxx") or "xxxx" in key:
        raise SystemExit(
            "Set RETELL_API_KEY in the environment (Retell dashboard → API Keys)."
        )
    # Railway: token or logged-in CLI
    who = _railway(["whoami"], check=False)
    if "Unauthorized" in who or "login" in who.lower():
        token = (os.environ.get("RAILWAY_TOKEN") or os.environ.get("RAILWAY_API_TOKEN") or "").strip()
        if not token:
            raise SystemExit(
                "Railway not logged in. Set RAILWAY_TOKEN or run: railway login --browserless"
            )
        os.environ["RAILWAY_TOKEN"] = token
        who = _railway(["whoami"], check=False)
        if "Unauthorized" in who:
            raise SystemExit("RAILWAY_TOKEN present but railway whoami still unauthorized.")
    print("Railway:", who.strip().splitlines()[0] if who.strip() else "ok")
    return key


def deploy_railway(retell_key: str) -> str:
    guest = GUEST_EXAMPLE.read_text()
    # Ensure service exists
    status = _railway(["status"], cwd=WEBHOOK, check=False)
    print(status)
    services = _railway(["service", "status"], cwd=WEBHOOK, check=False)
    if SERVICE not in status and SERVICE not in services:
        _railway(["add", "--service", SERVICE], cwd=WEBHOOK, check=False)

    _railway(
        [
            "variables",
            "set",
            f"RETELL_API_KEY={retell_key}",
            "DEFAULT_COMMUNITY=The Inlets",
            "AUTONOMOUS=true",
            "HUMAN_SMS_FALLBACK=false",
            "VERIFY_RETELL_SIGNATURES=true",
            "SERVERLESS=true",
            "SIMULATE_MYQ_OPEN=true",
            f"GUEST_LIST_JSON={guest}",
        ],
        cwd=WEBHOOK,
        check=False,
    )
    # Prefer service-scoped vars
    _railway(
        [
            "variables",
            "--service",
            SERVICE,
            "set",
            f"RETELL_API_KEY={retell_key}",
            "DEFAULT_COMMUNITY=The Inlets",
            "AUTONOMOUS=true",
            "HUMAN_SMS_FALLBACK=false",
            "VERIFY_RETELL_SIGNATURES=true",
            "SERVERLESS=true",
            "SIMULATE_MYQ_OPEN=true",
            f"GUEST_LIST_JSON={guest}",
        ],
        cwd=WEBHOOK,
        check=False,
    )

    up = _railway(["up", "--service", SERVICE, "-d"], cwd=WEBHOOK, check=False)
    print(up)
    if "Unauthorized" in up or "error" in up.lower() and "success" not in up.lower():
        up = _railway(["up", "-d"], cwd=WEBHOOK, check=False)
        print(up)

    # Domain
    dom = _railway(["domain"], cwd=WEBHOOK, check=False)
    print("domains:", dom)
    if "http" not in dom.lower() and ".up.railway.app" not in dom:
        gen = _railway(["domain", "generate"], cwd=WEBHOOK, check=False)
        print(gen)
        dom = _railway(["domain"], cwd=WEBHOOK, check=False)
        print("domains after generate:", dom)

    host = None
    for line in dom.splitlines():
        line = line.strip().strip("/")
        if "railway.app" in line or line.startswith("http"):
            host = line if line.startswith("http") else f"https://{line}"
            break
    if not host:
        # try JSON
        j = _railway(["domain", "--json"], cwd=WEBHOOK, check=False)
        try:
            data = json.loads(j)
            if isinstance(data, list) and data:
                d0 = data[0]
                host = d0.get("domain") or d0.get("edgeId") or ""
                if host and not host.startswith("http"):
                    host = f"https://{host}"
        except json.JSONDecodeError:
            pass
    if not host:
        raise RuntimeError("Could not resolve Railway public domain. Run: railway domain")

    host = host.rstrip("/")
    # Wait for health
    health_url = f"{host}/health"
    for i in range(36):
        try:
            status, body = _http_json("GET", health_url)
            print(f"health try {i+1}:", status, body)
            if status == 200:
                return host
        except Exception as e:
            print(f"health try {i+1}: {e}")
        time.sleep(5)
    raise RuntimeError(f"Health check failed for {health_url}")


def wire_retell(api_key: str, webhook_base: str) -> dict:
    from retell import Retell

    client = Retell(api_key=api_key)
    agents = client.agent.list()
    # SDK may return list or object
    items = agents if isinstance(agents, list) else getattr(agents, "items", None) or list(agents)
    target = None
    for a in items:
        name = getattr(a, "agent_name", None) or (a.get("agent_name") if isinstance(a, dict) else None)
        if name and "Gate Attendant" in name and "Inlets" in name:
            target = a
            break
    if target is None and items:
        target = items[0]
    if target is None:
        raise RuntimeError("No Retell agents found — import Gate Attendant first.")

    agent_id = getattr(target, "agent_id", None) or target["agent_id"]
    engine = getattr(target, "response_engine", None) or target.get("response_engine")
    print("Using agent", agent_id, getattr(target, "agent_name", None))

    # Update agent webhook
    try:
        client.agent.update(
            agent_id,
            webhook_url=f"{webhook_base}/retell/webhook",
        )
    except Exception as e:
        print("agent webhook update warn:", e)

    # Conversation flow tool URL rewrite
    flow_id = None
    if engine is not None:
        flow_id = getattr(engine, "conversation_flow_id", None)
        if flow_id is None and isinstance(engine, dict):
            flow_id = engine.get("conversation_flow_id")
    if flow_id:
        flow = client.conversation_flow.retrieve(flow_id)
        tools = getattr(flow, "tools", None) or []
        new_tools = []
        for t in tools:
            td = t.model_dump() if hasattr(t, "model_dump") else dict(t)
            name = td.get("name")
            if td.get("type") == "custom" and name:
                td["url"] = f"{webhook_base}/tools/{name}"
            new_tools.append(td)
        client.conversation_flow.update(flow_id, tools=new_tools)
        print("Updated conversation flow tools →", webhook_base)
    else:
        print("No conversation_flow_id on agent — update tool URLs in dashboard or re-import.")

    # Rebuild local import file with real host
    _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_retell_import.py"),
            "--webhook-base",
            webhook_base,
        ]
    )

    # Phone number
    phones = client.phone_number.list()
    phone_list = phones if isinstance(phones, list) else list(phones)
    did = None
    for p in phone_list:
        num = getattr(p, "phone_number", None) or (p.get("phone_number") if isinstance(p, dict) else None)
        inbound = getattr(p, "inbound_agent_id", None) or getattr(p, "inbound_agents", None)
        print("phone", num, inbound)
        if num and (not inbound or inbound == agent_id):
            did = num
            break
    if did is None and phone_list:
        did = getattr(phone_list[0], "phone_number", None)

    buy = os.environ.get("BUY_RETELL_DID", "yes").lower() in ("1", "true", "yes")
    if did is None and buy:
        print("Buying US DID (area 941)…")
        created = client.phone_number.create(
            area_code=941,
            nickname="We Lift — The Inlets Gate",
            inbound_agents=[{"agent_id": agent_id, "weight": 1.0}],
        )
        did = getattr(created, "phone_number", None)
    elif did:
        try:
            client.phone_number.update(
                did,
                inbound_agents=[{"agent_id": agent_id, "weight": 1.0}],
            )
        except TypeError:
            # older signature: inbound_agent_id
            try:
                client.phone_number.update(did, inbound_agent_id=agent_id)
            except Exception as e:
                print("phone bind warn:", e)
        except Exception as e:
            print("phone bind warn:", e)

    return {"agent_id": agent_id, "phone_number": did, "webhook_base": webhook_base}


def smoke_tools(webhook_base: str) -> None:
    payload = {
        "args": {
            "community_name": "The Inlets",
            "visitor_name": "Jordan Lee",
            "host_name_or_address": "Sam Rivera",
            "visit_type": "guest",
        }
    }
    status, body = _http_json(
        "POST",
        f"{webhook_base}/tools/check_guest_list",
        body=payload,
    )
    print("check_guest_list", status, body)
    if not body or body.get("decision") not in ("approve", "approved") and body.get("decision") != "approve":
        # webhook may return decision: approve
        if isinstance(body, dict) and body.get("decision") != "approve":
            print("WARN: expected approve for Jordan Lee / Sam Rivera; got", body)


def main() -> int:
    key = ensure_creds()
    host = deploy_railway(key)
    print("WEBHOOK_BASE=", host)
    info = wire_retell(key, host)
    smoke_tools(host)
    print("\n=== DEMO STACK READY ===")
    print(json.dumps(info, indent=2))
    print(
        "\nCell tests — call the DID and walk:\n"
        "1) APPROVE: Jordan Lee visiting Sam Rivera\n"
        "2) DENY: Random Person visiting Nobody Unit 99\n"
        "3) AMBIGUOUS: mumble / unclear names\n"
    )
    out = ROOT / "configs" / "demo-stack.json"
    out.write_text(json.dumps(info, indent=2) + "\n")
    print("Wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
