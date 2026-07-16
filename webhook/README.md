# We Lift — Access Desk + Retell gate webhooks

Real thin MVP: mint/SMS vendor gate codes, Retell proof PIN, myQ unlock (or simulate).

## Endpoints

| Method | Path | What it does |
|--------|------|----------------|
| GET | `/access` | **Access Desk UI** — send vendor codes |
| GET | `/access/meta` | Community, vendors, recent deliveries |
| POST | `/access/send_code` | Mint + Twilio SMS `{company_name, phone}` |
| POST | `/access/revoke` | Revoke active credential |
| GET | `/health` | Liveness + Twilio / myQ / simulate flags |
| POST | `/tools/check_guest_list` | Vendors: **proof_code** required; guests: name match |
| POST | `/tools/open_gate` | myQ unlock or `SIMULATE_MYQ_OPEN` |
| POST | `/tools/escalate_to_oncall` | Log + deny (no human wake) |
| POST | `/retell/webhook` | Optional call-ended events |

## Start locally

```bash
cd webhook
cp .env.example .env
# Sales demo: TWILIO_* + SIMULATE_MYQ_OPEN=true
./run.sh
# open http://127.0.0.1:8080/access
```

Production: [DEPLOY.md](DEPLOY.md) · Sales script: [docs/SALES-DEMO.md](../docs/SALES-DEMO.md)

## Configure `.env`

| Var | Purpose |
|-----|---------|
| `TWILIO_*` | Real SMS for Access Desk |
| `AUTONOMOUS` | `true` — no human SMS wake |
| `HUMAN_SMS_FALLBACK` | Keep `false` |
| `SIMULATE_MYQ_OPEN` | Demo unlock without API |
| `MYQ_*` | Required for real autonomous opens |
| `DEFAULT_COMMUNITY` | `The Inlets` |
| `RETELL_API_KEY` | Signature verify in prod |
| `GUEST_LIST_JSON` | Inline list if no file (serverless) |

## Seed vendors

[`../data/vendors.seed.json`](../data/vendors.seed.json) — GreenSide Lawn, AquaClear Pools, Bayshore Plumbing.

## Smoke tests

```bash
source .venv/bin/activate
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_credentials.py
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_tools.py
```

## Curl

```bash
curl -s http://127.0.0.1:8080/health | jq

curl -s -X POST http://127.0.0.1:8080/access/send_code \
  -H 'Content-Type: application/json' \
  -d '{"company_name":"GreenSide Lawn","phone":"+19415551234"}' | jq

curl -s -X POST http://127.0.0.1:8080/tools/check_guest_list \
  -H 'Content-Type: application/json' \
  -d '{"args":{"community_name":"The Inlets","visitor_name":"Jordan Lee","host_name_or_address":"Sam Rivera","visit_type":"guest"}}' | jq
```
