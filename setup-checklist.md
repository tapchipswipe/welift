# Retell + myQ Call Attendant setup

Use after the webhook is on public HTTPS. Full product checks: [docs/PRODUCT-ACCEPTANCE.md](docs/PRODUCT-ACCEPTANCE.md).
Tablet wiring: [docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md).

Dashboard: https://dashboard.retellai.com
Configs: [`configs/retell-llm.json`](configs/retell-llm.json) + [`configs/retell-agent.json`](configs/retell-agent.json) (primary — API/one-shot script), prompt [`prompt.md`](prompt.md). Alt setup path: dashboard **Import** — [`configs/retell-agent-import.json`](configs/retell-agent-import.json) (conversation-flow shape, built from [`configs/retell-agent-flow.base.json`](configs/retell-agent-flow.base.json)). See [docs/PRODUCT.md](docs/PRODUCT.md#retell-build-paths) for the open item reconciling the two configs' prompt text.

---

## Webhook base URL (pick by stage)

Retell custom tools need a **public HTTPS** base (no trailing slash). That host is only the service in [`webhook/`](webhook/).

| Stage | Use | Why |
|-------|-----|-----|
| First Retell setup / cell tests | **ngrok** — `ngrok http 8080` while `webhook/./run.sh` runs | Fastest. URL changes when ngrok restarts. |
| CAM demo / tablet pointing | **Railway** (or Fly) — see [`webhook/DEPLOY.md`](webhook/DEPLOY.md) | Stable URL so you do not re-edit Retell tools daily. |
| Import JSON before host exists | Placeholder `https://REPLACE_WITH_WEBHOOK_HOST` | Still imports; paste the real host after `/health` works. |

Do **not** invent a fake URL. Rebuild the Import file (Option C) or the API agent (Option A) once you have a real host — see below.

Verify before live calls: `GET {WEBHOOK_BASE}/health` returns JSON with autonomous flags.

---

## 0. Prerequisites

| Item | Status |
|------|--------|
| Retell account + API key in `webhook/.env` | |
| Webhook running (`cd webhook && ./run.sh`) | |
| Public HTTPS URL (ngrok for first wiring; Railway before CAM) | |
| CAM roster at `/access` (or seed vendors from `vendors.seed.json`) | |
| `data/guest-list.json` copied from example + tonight's social-guest names | |
| `SIMULATE_MYQ_OPEN=true` until myQ API | |
| Optional Twilio for real SMS | |

```bash
cd webhook
cp .env.example .env   # fill RETELL_API_KEY; DEFAULT_COMMUNITY=The Inlets
cp ../data/guest-list.example.json ../data/guest-list.json
./run.sh
# other terminal: ngrok http 8080   # or deploy — see webhook/DEPLOY.md
```

---

## 1. Create the agent

### Option A — script (primary, API)

```bash
source webhook/.venv/bin/activate
python scripts/create_agent.py --webhook-base https://YOUR_HOST --community "The Inlets"
```

Writes `configs/retell-ids.json` with `llm_id` / `agent_id`. Tools must hit:

- `POST …/tools/check_guest_list` (vendors require `proof_code`)
- `POST …/tools/open_gate`
- `POST …/tools/escalate_to_oncall`

### Option B — dashboard (manual)

1. **Agents → Create** (or Response Engine → Retell LLM)
2. Paste **begin_message** and **general_prompt** from [`prompt.md`](prompt.md)
3. Set temperature ~**0.2** (strict verifier)
4. Add tools (see §2)
5. Set dynamic variable `community_name` = `The Inlets`

### Option C — Import JSON (alt setup path)

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
6. Continue at §2 (phone number).

Before relying on Option C live: sync its embedded conversation-flow prompt with the canonical `proof_code`-required prompt in `prompt.md` / `configs/retell-llm.json` — see the open item in [docs/PRODUCT.md](docs/PRODUCT.md#retell-build-paths).

If Import rejects the file shape, use Option A instead.

---

## 2. Phone number

1. Retell → **Phone Numbers** → buy/assign to this agent
2. Set `RETELL_DID=+1…` in `webhook/.env` (shown on `/gate`)
3. Cell-test before pointing myQ at it

---

## 3. Custom functions (critical)

Replace `REPLACE_WITH_WEBHOOK_HOST` / `YOUR_WEBHOOK_HOST` with your ngrok/deploy host.

| Name | Method | URL | Speak during | Speak after |
|------|--------|-----|--------------|-------------|
| `check_guest_list` | POST | `https://…/tools/check_guest_list` | on | on |
| `open_gate` | POST | `https://…/tools/open_gate` | on | on |
| `escalate_to_oncall` | POST | `https://…/tools/escalate_to_oncall` | on | on |
| `end_call` | built-in | — | — | — |

Parameter schemas: copy from [`configs/retell-llm.json`](configs/retell-llm.json) → each tool's `parameters` object (already in the Import file for Option C).

**Payload:** leave **args only** OFF (default wrapped `{ name, call, args }` — webhook supports both).

---

## 4. Voice agent settings

From [`configs/retell-agent.json`](configs/retell-agent.json) (already in the Import file):

- Voice: calm adult English (e.g. `11labs-Adrian` or similar; swap if pedestal audio needs slower)
- Language: `en-US`
- Interruption sensitivity: moderate (outdoor wind / road noise)
- Boosted keywords: gate, guest pass, myQ, attendant, delivery, vendor, unit
- Agent webhook (optional): `https://…/retell/webhook`
- Post-call fields: `visitor_name`, `host_name_or_address`, `result`, `open_requested`

---

## 5. Acceptance (cell)

1. CAM sends code from `/access` for GreenSide (or your test vendor)
2. Call DID → company + **correct PIN** → approve → open (simulate)
3. Wrong PIN → deny
4. Resident → redirect, no open

### Test script (simulate social guest)

Call the Retell number. Walk three social-guest paths (`SIMULATE_MYQ_OPEN=true` until myQ API is live):

1. **Approve** — name from `guest-list.json` (e.g. Jordan Lee / Sam Rivera)
   - Expect: check → open → `status: opened` (simulate or myQ)
2. **Deny** — random visitor + host not on list
   - Expect: deny script; no open
3. **Ambiguous / ops** — mumble or visit_type ops
   - Expect: deny + log; agent must **not** say a human is coming

Confirm events log grows with each tool call. Before CAM outreach: deploy a stable host ([`webhook/DEPLOY.md`](webhook/DEPLOY.md)), then rebuild Option C's Import (or update tool URLs) to the Railway/Fly base.

---

## 6. Wire myQ tablet (only after §5 passes)

Point overnight Call Attendant / quick-call at the **Retell DID**.
Details: [docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md).

Controlled pedestal test with dealer/CAM. Live barrier motion needs real `MYQ_*`.

---

## 7. Autonomous unlock SOP

When a visitor is approved:

1. Retell calls `open_gate` → myQ Partner API unlocks
2. Visitor waits for barrier motion
3. Failures fail closed — deny + daytime log review (no 2am SMS)

---

## 8. Common mistakes

| Mistake | Fix |
|---------|-----|
| Tool URL still placeholder | Re-run `create_agent.py` with current host, or rebuild Import with `--webhook-base` |
| Opens without PIN | Prompt/tools must require `proof_code` for vendors |
| No `guest-list.json` | Copy example; agent will deny social guests |
| Signature 401s | Use webhook API key; or `VERIFY_RETELL_SIGNATURES=false` for local curl only |
| Forward myQ before cell test | Never — finish §5 first |
| Expect human SMS wake | Autonomous product — configure myQ unlock instead |
| Live traffic with only simulate | Turn `SIMULATE_MYQ_OPEN=false` after myQ API works |
| ngrok URL rotated | Rebuild Import or edit tool URLs; prefer Railway before CAM |

---

## First live night

- [ ] Vendors on CAM desk; codes sent
- [ ] Webhook up; `AUTONOMOUS=true`
- [ ] Health: `unlock_ready` true
- [ ] One intentional call from the physical tablet
