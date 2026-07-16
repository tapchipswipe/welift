#!/usr/bin/env python3
"""Build a Retell dashboard Import JSON from configs/retell-*.json."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLACEHOLDER = "https://REPLACE_WITH_WEBHOOK_HOST"

# Stable synthetic ids — Retell dashboard import has failed when tool_id was missing.
TOOL_IDS = {
    "end_call": "tool_end_call_welift_inlets",
    "check_guest_list": "tool_check_guest_list_welift_inlets",
    "open_gate": "tool_open_gate_welift_inlets",
    "escalate_to_oncall": "tool_escalate_to_oncall_welift_inlets",
}


def _apply_webhook_base(llm_cfg: dict, agent_cfg: dict, base: str) -> None:
    base = base.rstrip("/")
    for tool in llm_cfg.get("general_tools", []):
        name = tool.get("name")
        if tool.get("type") == "custom" and name:
            tool["url"] = f"{base}/tools/{name}"
        if name and "tool_id" not in tool:
            tool["tool_id"] = TOOL_IDS.get(name, f"tool_{name}_welift_inlets")
    if agent_cfg.get("webhook_url") is not None or "webhook_url" in agent_cfg:
        agent_cfg["webhook_url"] = f"{base}/retell/webhook"


def build_import(
    *,
    webhook_base: str,
    community: str,
) -> dict:
    llm_path = ROOT / "configs" / "retell-llm.json"
    agent_path = ROOT / "configs" / "retell-agent.json"

    with llm_path.open() as f:
        llm_cfg = json.load(f)
    with agent_path.open() as f:
        agent_cfg = json.load(f)

    _apply_webhook_base(llm_cfg, agent_cfg, webhook_base)

    llm_cfg.setdefault("default_dynamic_variables", {})
    llm_cfg["default_dynamic_variables"]["community_name"] = community

    # Drop live ids so Import creates a new agent + LLM.
    agent_cfg.pop("agent_id", None)
    agent_cfg.pop("version", None)
    agent_cfg.pop("is_published", None)
    agent_cfg.pop("last_modification_timestamp", None)

    # Embed LLM definition for dashboard Import (no foreign llm_id).
    agent_cfg["response_engine"] = {
        "type": "retell-llm",
        "llm": llm_cfg,
    }
    agent_cfg.setdefault("default_dynamic_variables", {})
    agent_cfg["default_dynamic_variables"]["community_name"] = community

    return agent_cfg


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge retell-llm.json + retell-agent.json into a Retell Import file"
    )
    parser.add_argument(
        "--webhook-base",
        default=DEFAULT_PLACEHOLDER,
        help=f"Public HTTPS base (default: {DEFAULT_PLACEHOLDER})",
    )
    parser.add_argument(
        "--community",
        default=os.getenv("DEFAULT_COMMUNITY", "The Inlets"),
        help="Default community_name dynamic variable",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "configs" / "retell-agent-import.json",
        help="Output path for the Import JSON",
    )
    args = parser.parse_args()

    base = args.webhook_base.rstrip("/")
    if not base.startswith("https://"):
        print(
            "webhook-base must be an https:// URL (or the REPLACE_WITH_WEBHOOK_HOST placeholder)",
            file=sys.stderr,
        )
        return 1

    payload = build_import(webhook_base=base, community=args.community)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {args.out}")
    print(f"  webhook_base = {base}")
    print(f"  community_name = {args.community}")
    if "REPLACE_WITH_WEBHOOK_HOST" in base:
        print()
        print("Placeholder host still set. After ngrok/Railway is up:")
        print(
            "  python scripts/build_retell_import.py "
            "--webhook-base https://YOUR_HOST"
        )
        print("Then: Retell dashboard → Agents → Import → upload the JSON.")
    else:
        print()
        print("Next: Retell dashboard → Agents → Import → upload this file.")
        print(f"  Confirm GET {base}/health before test calls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
