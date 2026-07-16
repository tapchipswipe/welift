#!/usr/bin/env bash
# Start Phase-1 Retell webhooks on :8080
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env — set RETELL_API_KEY and ONCALL_PHONE, then re-run."
  exit 1
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

GUEST="../data/guest-list.json"
if [[ ! -f "$GUEST" ]]; then
  cp ../data/guest-list.example.json "$GUEST"
  echo "Created $GUEST from example"
fi

export VERIFY_RETELL_SIGNATURES="${VERIFY_RETELL_SIGNATURES:-false}"
echo "Starting webhooks on http://127.0.0.1:8080"
echo "Health: http://127.0.0.1:8080/health"
echo "In another terminal: ngrok http 8080"
echo "Then set Retell tool URLs to https://YOUR_NGROK/tools/<name>"
exec uvicorn main:app --host 0.0.0.0 --port 8080 --reload
