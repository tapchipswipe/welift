#!/usr/bin/env python3
"""Create Retell LLM + voice agent from configs/ (requires RETELL_API_KEY)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / "webhook" / ".env")


def main() -> int:
    parser = argparse.ArgumentParser(description="Push overnight gate agent to Retell")
    parser.add_argument(
        "--webhook-base",
        required=True,
        help="Public HTTPS base, e.g. https://xxxx.ngrok-free.app",
    )
    parser.add_argument(
        "--community",
        default=os.getenv("DEFAULT_COMMUNITY", "The Inlets"),
        help="Default community_name dynamic variable",
    )
    args = parser.parse_args()

    api_key = os.getenv("RETELL_API_KEY")
    if not api_key:
        print("Set RETELL_API_KEY in webhook/.env", file=sys.stderr)
        return 1

    try:
        from retell import Retell
    except ImportError:
        print("pip install retell-sdk", file=sys.stderr)
        return 1

    base = args.webhook_base.rstrip("/")
    llm_path = ROOT / "configs" / "retell-llm.json"
    agent_path = ROOT / "configs" / "retell-agent.json"

    with llm_path.open() as f:
        llm_cfg = json.load(f)
    with agent_path.open() as f:
        agent_cfg = json.load(f)

    # Point custom tools at this webhook host
    for tool in llm_cfg.get("general_tools", []):
        if tool.get("type") == "custom" and "url" in tool:
            name = tool["name"]
            tool["url"] = f"{base}/tools/{name}"

    if agent_cfg.get("webhook_url"):
        agent_cfg["webhook_url"] = f"{base}/retell/webhook"

    client = Retell(api_key=api_key)

    print("Creating Retell LLM…")
    llm = client.llm.create(**llm_cfg)
    print(f"  llm_id = {llm.llm_id}")

    agent_cfg["response_engine"] = {"type": "retell-llm", "llm_id": llm.llm_id}
    # Seed dynamic variable used in begin_message / prompt
    agent_cfg.setdefault("default_dynamic_variables", {})
    agent_cfg["default_dynamic_variables"]["community_name"] = args.community

    print("Creating voice agent…")
    # Filter to known create-agent fields if SDK is strict — pass through and let API validate
    agent = client.agent.create(**agent_cfg)
    print(f"  agent_id = {agent.agent_id}")
    print()
    print("Next:")
    print("  1. In Retell dashboard → Phone Numbers → buy/assign a number to this agent")
    print("  2. Make a test call; confirm SMS/logs on open_gate")
    print("  3. Point myQ Call Attendant at that number for a controlled window")
    print()
    print(f"Saved ids → write these down: llm={llm.llm_id} agent={agent.agent_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
