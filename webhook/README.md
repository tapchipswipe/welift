# Retell overnight gate webhooks

Public HTTPS endpoints Retell calls **mid-call**.

## Endpoints

| Method | Path | What it does |
|--------|------|----------------|
| GET | `/health` | Liveness + config flags |
| POST | `/tools/check_guest_list` | Match visitor+host → approve / deny / escalate |
| POST | `/tools/open_gate` | SMS on-call to unlock myQ (Phase 1) |
| POST | `/tools/escalate_to_oncall` | SMS on-call with summary |
| POST | `/retell/webhook` | Optional call-ended events |

## Start locally

```bash
cd 05-retell-agent/webhook
cp .env.example .env   # set ONCALL_PHONE=+1… and RETELL_API_KEY
./run.sh
```

Second terminal:

```bash
ngrok http 8080
```

Copy the `https://….ngrok-free.app` base. In Retell, set custom function URLs to:

```
https://YOUR_NGROK/tools/check_guest_list
https://YOUR_NGROK/tools/open_gate
https://YOUR_NGROK/tools/escalate_to_oncall
```

Optional agent webhook:

```
https://YOUR_NGROK/retell/webhook
```

## Configure `.env`

| Var | Required | Purpose |
|-----|----------|---------|
| `ONCALL_PHONE` | yes (for real SMS) | E.164 cell, e.g. `+19415551234` |
| `RETELL_API_KEY` | for live Retell | Signature verify |
| `VERIFY_RETELL_SIGNATURES` | | `false` for local curl; `true` in prod |
| `DEFAULT_COMMUNITY` | | Default HOA name |
| `TWILIO_*` | optional | Real SMS; else messages go to server logs |
| `GUEST_LIST_JSON` | optional | Inline JSON if no file (serverless) |
| `IGNORE_VALIDITY_WINDOW` | optional | Ignore entry date windows |
| `SERVERLESS` | optional | Log events instead of writing `events.jsonl` |

## Guest list

Edit [`../data/guest-list.json`](../data/guest-list.json) (copied from example on first run).

Approve test names:
- Visitor **Jordan Lee** → host **Sam Rivera**
- Visitor **Alex Kim** → host **Pat Morgan**

## Smoke test

```bash
source .venv/bin/activate
VERIFY_RETELL_SIGNATURES=false python test_tools.py
```

## Curl examples

```bash
curl -s http://127.0.0.1:8080/health | jq

curl -s -X POST http://127.0.0.1:8080/tools/check_guest_list \
  -H 'Content-Type: application/json' \
  -d '{"args":{"community_name":"Pilot HOA","visitor_name":"Jordan Lee","host_name_or_address":"Sam Rivera","visit_type":"guest"}}' | jq
```

(Use `VERIFY_RETELL_SIGNATURES=false` in `.env` for unsigned local curls.)
