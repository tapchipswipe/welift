# Deploy Access Desk + Retell webhook (stable HTTPS)

Local ngrok is fine for first wiring. **Before any CAM demo**, put this service on a stable host so `/access` and Retell tool URLs do not change mid-meeting.

Sales script: [docs/SALES-DEMO.md](../docs/SALES-DEMO.md)

## Env vars (all hosts)

Copy [`.env.example`](.env.example). Minimum for a presentable demo:

| Var | Value |
|-----|-------|
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_FROM_NUMBER` | Real SMS in the room |
| `RETELL_API_KEY` | Retell key (signature verify) |
| `DEFAULT_COMMUNITY` | `The Inlets` |
| `AUTONOMOUS` | `true` |
| `HUMAN_SMS_FALLBACK` | `false` |
| `VERIFY_RETELL_SIGNATURES` | `true` in prod |
| `MYQ_*` | Required for live autonomous opens |
| `SIMULATE_MYQ_OPEN` | `true` for demos only |
| `SERVERLESS` | `true` if filesystem is ephemeral |
| `GUEST_LIST_JSON` | Full guest-list JSON string when you cannot mount a file |

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

1. Open `https://YOUR_HOST/health` — expect `"autonomous":true`, `"twilio_configured":true` for live SMS.
2. Open `https://YOUR_HOST/access` — send a test code to your phone.
3. Update Retell custom function URLs to `https://YOUR_HOST/tools/...`.
4. Re-run cell tests from [setup-checklist.md](../setup-checklist.md) + proof PIN path.
5. Cold-run [SALES-DEMO.md](../docs/SALES-DEMO.md) twice; save a backup screen recording.

## Local still works

```bash
cd webhook
./run.sh
# open http://127.0.0.1:8080/access
# other terminal: ngrok http 8080
```
