#!/usr/bin/env python3
"""CLI: mint + SMS a vendor gate code (for dry runs without the UI)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "webhook"))

from dotenv import load_dotenv

load_dotenv(ROOT / "webhook" / ".env")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send We Lift vendor gate code")
    parser.add_argument("--company", required=True)
    parser.add_argument("--phone", default="", help="Override E.164; blank = roster phone")
    parser.add_argument("--community", default=os.getenv("DEFAULT_COMMUNITY", "The Inlets"))
    parser.add_argument("--override-window", action="store_true")
    args = parser.parse_args()

    import credentials as creds

    try:
        result = creds.send_code(
            community=args.community,
            company_name=args.company,
            phone=args.phone or None,
            actor="cli",
            override_window=args.override_window,
        )
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(json.dumps({**result, "code": result.get("code")}, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
