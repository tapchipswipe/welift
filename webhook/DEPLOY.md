# Deploy the Retell webhook (stable HTTPS)

Local ngrok is fine for first wiring. **Before any CAM demo or myQ forward**, put this service on a stable host so Retell tool URLs do not change daily.

## Env vars (all hosts)

Copy [`.env.example`](.env.example). Minimum for Phase 1:

| Var | Value |
|-----|-------|
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

1. Open `https://YOUR_HOST/health` — expect `"autonomous":true`, `"unlock_ready":true`.
2. Update Retell custom function URLs to `https://YOUR_HOST/tools/...`.
3. Re-run §5 cell tests from [setup-checklist.md](../setup-checklist.md).
4. Record three demos (approve / deny / fail-closed) before CAM outreach.

## Local still works

```bash
cd webhook
./run.sh
# other terminal: ngrok http 8080
```
