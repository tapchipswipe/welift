# Deploy Access Desk + Retell webhook (stable HTTPS)

Local ngrok is fine for first wiring. **Before any CAM demo**, put this service on a stable host so `/access` and Retell tool URLs do not change mid-meeting.

Sales script: [docs/SALES-DEMO.md](../docs/SALES-DEMO.md)

## Env vars (all hosts)

Copy [`.env.example`](.env.example). Minimum for the real product:

| Var | Value |
|-----|-------|
| `TWILIO_*` | SMS to owner/dispatch phones |
| `RETELL_API_KEY` | Agent push + signature verify |
| `RETELL_DID` | Shown on `/gate`; tablet Call Attendant target |
| `DEFAULT_COMMUNITY` | `The Inlets` |
| `AUTONOMOUS` | `true` |
| `HUMAN_SMS_FALLBACK` | `false` |
| `VERIFY_RETELL_SIGNATURES` | `true` in prod |
| `MYQ_*` | Live autonomous opens |
| `SIMULATE_MYQ_OPEN` | `true` until Partner API |
| `SERVERLESS` | `true` if filesystem is ephemeral |

## Option A — Railway (fastest)

```bash
cd webhook
# Install Railway CLI, then:
railway init
railway up
railway variables set RETELL_API_KEY=... DEFAULT_COMMUNITY="The Inlets" \
  AUTONOMOUS=true HUMAN_SMS_FALLBACK=false VERIFY_RETELL_SIGNATURES=true SERVERLESS=true \
  MYQ_API_BASE=... MYQ_API_KEY=... MYQ_FACILITY_ID=... MYQ_ENTRANCE_ID=...
```

Uses [`Dockerfile`](Dockerfile) + [`railway.toml`](railway.toml). Health check: `GET /health`.

## Option B — Fly.io (Miami region)

```bash
cd webhook
fly launch --config fly.toml --copy-config --no-deploy
fly secrets set RETELL_API_KEY=... MYQ_API_BASE=... MYQ_API_KEY=... \
  MYQ_FACILITY_ID=... MYQ_ENTRANCE_ID=... GUEST_LIST_JSON='...'
fly deploy
```

## Option C — Docker anywhere

```bash
cd webhook
docker build -t welift-webhook .
docker run --rm -p 8080:8080 --env-file .env -e SERVERLESS=true welift-webhook
```

Put a reverse proxy / load balancer with HTTPS in front.

## After deploy

1. `https://YOUR_HOST/health` — `autonomous`, Twilio flags as expected.
2. `https://YOUR_HOST/access` — add vendor, send code.
3. `https://YOUR_HOST/gate` — Call Attendant UX; set `RETELL_DID`.
4. `python scripts/create_agent.py --webhook-base https://YOUR_HOST`
5. Run [PRODUCT-ACCEPTANCE.md](../docs/PRODUCT-ACCEPTANCE.md); wire tablet per [MYQ-TABLET-RETELL.md](../docs/MYQ-TABLET-RETELL.md).

## Local

```bash
cd webhook
./run.sh
# http://127.0.0.1:8080/access  and  /gate
```
