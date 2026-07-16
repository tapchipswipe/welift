# Retell overnight gate webhooks (autonomous)

Public HTTPS endpoints Retell calls **mid-call**. AI verifies; myQ API opens. No overnight human.

## Endpoints

| Method | Path | What it does |
|--------|------|----------------|
| GET | `/health` | Liveness + autonomous/unlock flags |
| POST | `/tools/check_guest_list` | Match visitor+host → **approve / deny** |
| POST | `/tools/open_gate` | myQ Partner API unlock (or simulate for demos) |
| POST | `/tools/escalate_to_oncall` | Log for daytime review; still deny |
| POST | `/retell/webhook` | Optional call-ended events |

## Start locally

```bash
cd webhook
cp .env.example .env
# For demos without API:
#   SIMULATE_MYQ_OPEN=true
# For live opens:
#   set MYQ_API_BASE, MYQ_API_KEY, MYQ_FACILITY_ID, MYQ_ENTRANCE_ID
./run.sh
```

Production: [DEPLOY.md](DEPLOY.md).

## Configure `.env`

| Var | Purpose |
|-----|---------|
| `AUTONOMOUS` | `true` (default) — no human SMS wake |
| `HUMAN_SMS_FALLBACK` | Keep `false` |
| `SIMULATE_MYQ_OPEN` | Demo unlock without API |
| `MYQ_*` | Required for real autonomous opens |
| `DEFAULT_COMMUNITY` | `The Inlets` |
| `RETELL_API_KEY` | Signature verify in prod |
| `GUEST_LIST_JSON` | Inline list if no file (serverless) |

## Guest list

Edit [`../data/guest-list.json`](../data/guest-list.json) (from example).

Approve test names: **Jordan Lee** / **Sam Rivera**; **Alex Kim** / **Pat Morgan**.

## Smoke test

```bash
source .venv/bin/activate
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_tools.py
```

## Curl

```bash
curl -s http://127.0.0.1:8080/health | jq

curl -s -X POST http://127.0.0.1:8080/tools/check_guest_list \
  -H 'Content-Type: application/json' \
  -d '{"args":{"community_name":"The Inlets","visitor_name":"Jordan Lee","host_name_or_address":"Sam Rivera","visit_type":"guest"}}' | jq
```
