#!/usr/bin/env python3
"""Create Retell LLM + voice agent from configs/ (requires RETELL_API_KEY).

One-shot product setup: points custom tools at your public webhook base.
"""

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
    parser = argparse.ArgumentParser(
        description="Push We Lift Call Attendant agent to Retell"
    )
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
    parser.add_argument(
        "--out",
        default=str(ROOT / "configs" / "retell-ids.json"),
        help="Write llm_id / agent_id here (gitignored if local)",
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

    required_tools = {"check_guest_list", "open_gate", "escalate_to_oncall"}
    found = set()
    for tool in llm_cfg.get("general_tools", []):
        if tool.get("type") == "custom" and "url" in tool:
            name = tool["name"]
            tool["url"] = f"{base}/tools/{name}"
            found.add(name)
            # Ensure proof_code on check_guest_list schema
            if name == "check_guest_list":
                props = tool.setdefault("parameters", {}).setdefault("properties", {})
                props.setdefault(
                    "proof_code",
                    {
                        "type": "string",
                        "description": (
                            "Today's SMS gate PIN. Required for vendors/workers."
                        ),
                    },
                )

    missing = required_tools - found
    if missing:
        print(f"configs/retell-llm.json missing tools: {missing}", file=sys.stderr)
        return 1

    if agent_cfg.get("webhook_url") is not None:
        agent_cfg["webhook_url"] = f"{base}/retell/webhook"

    client = Retell(api_key=api_key)

    llm_cfg.setdefault("default_dynamic_variables", {})
    llm_cfg["default_dynamic_variables"]["community_name"] = args.community

    print("Creating Retell LLM (proof-PIN vendor path)…")
    llm = client.llm.create(**llm_cfg)
    print(f"  llm_id = {llm.llm_id}")

    agent_cfg["response_engine"] = {"type": "retell-llm", "llm_id": llm.llm_id}

    print("Creating voice agent…")
    agent = client.agent.create(**agent_cfg)
    print(f"  agent_id = {agent.agent_id}")

    out = {
        "llm_id": llm.llm_id,
        "agent_id": agent.agent_id,
        "webhook_base": base,
        "community_name": args.community,
        "tools": {
            name: f"{base}/tools/{name}"
            for name in sorted(required_tools)
        },
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    print()
    print("Next (product):")
    print("  1. Retell → Phone Numbers → assign DID to this agent")
    print("  2. Set RETELL_DID=+1… in webhook/.env (shows on /gate)")
    print("  3. Run docs/PRODUCT-ACCEPTANCE.md Retell checks")
    print("  4. Point myQ Call Attendant at that DID — docs/MYQ-TABLET-RETELL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
