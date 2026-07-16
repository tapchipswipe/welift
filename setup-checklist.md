# Retell Dashboard Setup — Gate Attendant

Use this after the webhook is reachable on HTTPS (ngrok or deploy).

Dashboard: https://dashboard.retellai.com  
Configs: [`configs/retell-agent-import.json`](configs/retell-agent-import.json) (preferred Import), [`configs/retell-llm.json`](configs/retell-llm.json), [`configs/retell-agent.json`](configs/retell-agent.json), full prompt in [`prompt.md`](prompt.md).

---

## Webhook base URL (pick by stage)

Retell custom tools need a **public HTTPS** base (no trailing slash). That host is only the service in [`webhook/`](webhook/).

| Stage | Use | Why |
|-------|-----|-----|
| First Retell import / cell tests | **ngrok** — `ngrok http 8080` while `webhook/./run.sh` runs | Fastest. URL changes when ngrok restarts. |
| CAM demo / tablet pointing | **Railway** (or Fly) — see [`webhook/DEPLOY.md`](webhook/DEPLOY.md) | Stable URL so you do not re-edit Retell tools daily. |
| Agent file before host exists | Placeholder `https://REPLACE_WITH_WEBHOOK_HOST` in the Import JSON | Agent still imports; paste the real host after `/health` works. |

Do **not** invent a fake URL. After Import, either edit the three tool URLs (+ optional agent webhook) in the Retell UI, or rebuild:

```bash
python scripts/build_retell_import.py --webhook-base https://YOUR_HOST
```

Verify before live calls: `GET {WEBHOOK_BASE}/health` returns JSON with autonomous flags.

---

## 0. Prerequisites

| Item | Status |
|------|--------|
| Retell account + API key | |
| Webhook running (`uvicorn` in `webhook/`) | |
| Public HTTPS URL (ngrok for first wiring; Railway before CAM) | |
| `data/guest-list.json` copied from example + tonight’s names | |
| Optional Twilio for real SMS | |

```bash
cd webhook
cp ../data/guest-list.example.json ../data/guest-list.json
cp .env.example .env   # fill RETELL_API_KEY; DEFAULT_COMMUNITY=The Inlets
# demos without myQ API:
#   SIMULATE_MYQ_OPEN=true
./run.sh
# other terminal:
ngrok http 8080
# Prefer stable HTTPS before CAM demos — see webhook/DEPLOY.md
```

---

## 1. Create the agent

### Option C — Import JSON (preferred)

1. Confirm `GET https://YOUR_HOST/health` works (skip if you will paste URLs later).
2. Build (or rebuild) the Import file:

```bash
# from repo root — placeholder (edit URLs in Retell after Import):
python3 scripts/build_retell_import.py

# or with a real host:
python3 scripts/build_retell_import.py --webhook-base https://xxxx.ngrok-free.app
```

3. Dashboard → **Agents → Import** → upload [`configs/retell-agent-import.json`](configs/retell-agent-import.json) (conversation-flow export shape).
4. If you used the placeholder host, update all three custom tool URLs (+ optional agent webhook) to your real `WEBHOOK_BASE`.
5. Confirm dynamic variable `community_name` = `The Inlets`.
6. Continue at §4 (phone number).

If Import rejects the file shape, use **Option A** (API script) below.

### Option A — script (API fallback)

```bash
# from repo root
source webhook/.venv/bin/activate
python scripts/create_agent.py --webhook-base https://YOUR_HOST --community "The Inlets"
```

### Option B — dashboard (manual)

1. **Agents → Create** (or Response Engine → Retell LLM)
2. Paste **begin_message** and **general_prompt** from [`prompt.md`](prompt.md)
3. Set temperature ~**0.2** (strict verifier)
4. Add tools (see §2)
5. Set dynamic variable `community_name` = `The Inlets`

---

## 2. Custom functions (critical)

Replace `REPLACE_WITH_WEBHOOK_HOST` / `YOUR_WEBHOOK_HOST` with your ngrok/deploy host.

| Name | Method | URL | Speak during | Speak after |
|------|--------|-----|--------------|-------------|
| `check_guest_list` | POST | `https://…/tools/check_guest_list` | on | on |
| `open_gate` | POST | `https://…/tools/open_gate` | on | on |
| `escalate_to_oncall` | POST | `https://…/tools/escalate_to_oncall` | on | on |
| `end_call` | built-in | — | — | — |

Parameter schemas: copy from [`configs/retell-llm.json`](configs/retell-llm.json) → each tool’s `parameters` object (already in the Import file for Option C).

**Payload:** leave **args only** OFF (default wrapped `{ name, call, args }` — webhook supports both).

---

## 3. Voice agent settings

From [`configs/retell-agent.json`](configs/retell-agent.json) (already in the Import file):

- Voice: calm adult English (e.g. `11labs-Adrian` or similar; swap if pedestal audio needs slower)
- Language: `en-US`
- Interruption sensitivity: moderate (outdoor wind / road noise)
- Boosted keywords: gate, guest pass, myQ, attendant, delivery, vendor, unit
- Agent webhook (optional): `https://…/retell/webhook`
- Post-call fields: `visitor_name`, `host_name_or_address`, `result`, `open_requested`

---

## 4. Phone number

1. Retell → **Phone Numbers** → buy or import a US DID  
2. Assign to this agent  
3. Test from your cell **before** pointing myQ at it  

---

## 5. Test script (simulate visitor)

Call the Retell number. Walk three paths (`SIMULATE_MYQ_OPEN=true` until myQ API is live):

1. **Approve** — name from `guest-list.json` (e.g. Jordan Lee / Sam Rivera)  
   - Expect: check → open → `status: opened` (simulate or myQ)  
2. **Deny** — random visitor + host not on list  
   - Expect: deny script; no open  
3. **Ambiguous / ops** — mumble or visit_type ops  
   - Expect: deny + log; agent must **not** say a human is coming  

Confirm events log grows with each tool call.

Before CAM outreach: deploy a stable host ([`webhook/DEPLOY.md`](webhook/DEPLOY.md)), then rebuild Import or update tool URLs to the Railway/Fly base.

---

## 6. Wire myQ tablet (only after §5 passes)

Same pattern as Smith ([how-to-connect-myq-to-smith.md](../01-metro-validation/how-to-connect-myq-to-smith.md)):

> Point overnight Call Attendant / quick-call at the **Retell DID**, 8pm–6am.

Do a controlled 10-minute pedestal test with the dealer/CAM present. Live opens require real `MYQ_*` (not simulate).

---

## 7. Autonomous unlock SOP

When a visitor is approved overnight:

1. Retell calls `open_gate` → myQ Partner API unlocks  
2. Visitor waits for barrier motion  
3. Failures fail closed — deny + daytime log review (no 2am SMS)

---

## 8. Common mistakes

| Mistake | Fix |
|---------|-----|
| Tool URL still `REPLACE_WITH_WEBHOOK_HOST` / `YOUR_WEBHOOK_HOST` | Update all three custom function URLs (or rebuild Import with `--webhook-base`) |
| No `guest-list.json` | Copy example; agent will deny |
| Signature 401s | Use webhook API key; or `VERIFY_RETELL_SIGNATURES=false` for local curl only |
| Agent opens without check | Prompt: open_gate only after approve — temperature ~0.2 |
| Forward myQ before Retell test | Never — finish §5 first |
| Expect human SMS | Product is autonomous — configure `MYQ_*` instead |
| Live traffic with only simulate | Turn `SIMULATE_MYQ_OPEN=false` after API works |
| ngrok URL rotated | Rebuild Import or edit tool URLs; prefer Railway before CAM |

---

## Message to yourself on first live night

- [ ] Guest list loaded for tonight  
- [ ] Webhook deploy up; `AUTONOMOUS=true`; real `MYQ_*`  
- [ ] Health shows `unlock_ready: true` and `simulate_myq_open: false`  
- [ ] One intentional test call from the physical tablet  
