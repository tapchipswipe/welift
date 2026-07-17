# We Lift — CAM Access Desk + Retell Call Attendant

Real product spine: CAM authorizes vendors → SMS gate codes (save AI minutes) →
Retell AI Call Attendant verifies proof PIN when someone has no code.

## Surfaces

| URL | Audience |
|-----|----------|
| `GET /access` | **CAM / admin only** — roster CRUD, send/revoke, audit |
| `GET /gate` | Visitor Call Attendant UX (mirrors pedestal; dials Retell DID) |
| `GET /health` | Ops flags |

## Endpoints

| Method | Path | What |
|--------|------|------|
| GET/POST | `/access/vendors` | List / upsert vendors (owner vs dispatch) |
| PATCH | `/access/vendors/{company}` | Update / deactivate |
| GET | `/access/audit` | Deliveries + credentials + events |
| POST | `/access/send_code` | Mint + SMS (`phone` optional = roster; `override_window`) |
| POST | `/access/revoke` | Revoke active PIN |
| GET | `/gate/meta` | Community + `RETELL_DID` |
| POST | `/tools/check_guest_list` | Vendors need `proof_code` |
| POST | `/tools/open_gate` | myQ or `SIMULATE_MYQ_OPEN` |
| POST | `/tools/escalate_to_oncall` | Log + deny |

## Start locally

```bash
cd webhook
cp .env.example .env
# TWILIO_*, RETELL_DID, SIMULATE_MYQ_OPEN=true
./run.sh
# CAM:   http://127.0.0.1:8080/access
# Gate:  http://127.0.0.1:8080/gate
```

Retell agent: `python ../scripts/create_agent.py --webhook-base https://YOUR_HOST`  
Acceptance: [docs/PRODUCT-ACCEPTANCE.md](../docs/PRODUCT-ACCEPTANCE.md)  
Tablet → Retell: [docs/MYQ-TABLET-RETELL.md](../docs/MYQ-TABLET-RETELL.md)  
Deploy: [DEPLOY.md](DEPLOY.md)

## Smoke tests

```bash
source .venv/bin/activate
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_credentials.py
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_tools.py
```
