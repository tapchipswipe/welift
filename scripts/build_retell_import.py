#!/usr/bin/env python3
"""Build a Retell dashboard Import JSON (conversation-flow format).

Source of truth for structure: configs/retell-agent-flow.base.json
(matches Retell conversation-flow export/import shape).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLACEHOLDER = "https://REPLACE_WITH_WEBHOOK_HOST"
BASE_PATH = ROOT / "configs" / "retell-agent-flow.base.json"
OUT_PATH = ROOT / "configs" / "retell-agent-import.json"

# Old host tokens we may rewrite when substituting.
HOST_MARKERS = (
    "https://REPLACE_WITH_WEBHOOK_HOST",
    "https://YOUR_WEBHOOK_HOST",
)


def _rewrite_urls(obj: object, base: str) -> object:
    base = base.rstrip("/")
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == "url" and isinstance(v, str):
                for marker in HOST_MARKERS:
                    if v.startswith(marker):
                        suffix = v[len(marker) :]
                        out[k] = f"{base}{suffix}"
                        break
                else:
                    out[k] = v
            elif k == "webhook_url" and isinstance(v, str):
                out[k] = f"{base}/retell/webhook"
            else:
                out[k] = _rewrite_urls(v, base)
        return out
    if isinstance(obj, list):
        return [_rewrite_urls(x, base) for x in obj]
    return obj


def build_import(*, webhook_base: str, community: str) -> dict:
    with BASE_PATH.open() as f:
        payload = json.load(f)

    payload = _rewrite_urls(payload, webhook_base.rstrip("/"))
    payload["agent_name"] = f"Gate Attendant — {community}"

    flow = payload.get("conversationFlow") or {}
    dyn = flow.setdefault("default_dynamic_variables", {})
    dyn["community_name"] = community

    # Optional top-level webhook if present / wanted by some imports
    if "webhook_url" not in payload:
        payload["webhook_url"] = f"{webhook_base.rstrip('/')}/retell/webhook"
    else:
        payload["webhook_url"] = f"{webhook_base.rstrip('/')}/retell/webhook"

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Retell conversation-flow Import JSON from the base template"
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
        default=OUT_PATH,
        help="Output path for the Import JSON",
    )
    args = parser.parse_args()

    if not BASE_PATH.is_file():
        print(f"Missing base template: {BASE_PATH}", file=sys.stderr)
        return 1

    base = args.webhook_base.rstrip("/")
    if not base.startswith("https://"):
        print("webhook-base must be an https:// URL", file=sys.stderr)
        return 1

    payload = build_import(webhook_base=base, community=args.community)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {args.out}")
    print(f"  format = conversation-flow (Retell dashboard Import)")
    print(f"  webhook_base = {base}")
    print(f"  community_name = {args.community}")
    if "REPLACE_WITH_WEBHOOK_HOST" in base:
        print()
        print("Placeholder host still set. After ngrok/Railway is up:")
        print(
            "  python scripts/build_retell_import.py "
            "--webhook-base https://YOUR_HOST"
        )
    else:
        print()
        print("Next: Retell dashboard → Agents → Import → upload this file.")
        print(f"  Confirm GET {base}/health before test calls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
