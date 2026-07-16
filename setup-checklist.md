# Retell Dashboard Setup — Overnight Gate Attendant

Use this after the webhook is reachable on HTTPS (ngrok or deploy).

Dashboard: https://dashboard.retellai.com  
Configs in this folder: [`configs/retell-llm.json`](configs/retell-llm.json), [`configs/retell-agent.json`](configs/retell-agent.json), full prompt in [`prompt.md`](prompt.md).

---

## 0. Prerequisites

| Item | Status |
|------|--------|
| Retell account + API key | |
| Webhook running (`uvicorn` in `webhook/`) | |
| Public HTTPS URL (ngrok) | |
| `data/guest-list.json` copied from example + tonight’s names | |
| `ONCALL_PHONE` in `webhook/.env` (your cell, E.164) | |
| Optional Twilio for real SMS | |

```bash
cd webhook
cp ../data/guest-list.example.json ../data/guest-list.json
cp .env.example .env   # fill RETELL_API_KEY + ONCALL_PHONE; DEFAULT_COMMUNITY=The Inlets
./run.sh
# other terminal:
ngrok http 8080
# Prefer stable HTTPS before CAM demos — see webhook/DEPLOY.md
```

---

## 1. Create the LLM (Response Engine)

**Option A — script**

```bash
# from repo root
source webhook/.venv/bin/activate
python scripts/create_agent.py --webhook-base https://YOUR_HOST --community "The Inlets"
```

**Option B — dashboard**

1. **Agents → Create** (or Response Engine → Retell LLM)
2. Paste **begin_message** and **general_prompt** from [`prompt.md`](prompt.md)
3. Set temperature ~**0.2** (strict verifier)
4. Add tools (see §2)
5. Set dynamic variable `community_name` = `The Inlets`

---

## 2. Custom functions (critical)

Replace `YOUR_WEBHOOK_HOST` with your ngrok/deploy host.

| Name | Method | URL | Speak during | Speak after |
|------|--------|-----|--------------|-------------|
| `check_guest_list` | POST | `https://…/tools/check_guest_list` | on | on |
| `open_gate` | POST | `https://…/tools/open_gate` | on | on |
| `escalate_to_oncall` | POST | `https://…/tools/escalate_to_oncall` | on | on |
| `end_call` | built-in | — | — | — |

Parameter schemas: copy from [`configs/retell-llm.json`](configs/retell-llm.json) → each tool’s `parameters` object.

**Payload:** leave **args only** OFF (default wrapped `{ name, call, args }` — webhook supports both).

---

## 3. Voice agent settings

From [`configs/retell-agent.json`](configs/retell-agent.json):

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
| Tool URL still `YOUR_WEBHOOK_HOST` | Update all three custom function URLs |
| No `guest-list.json` | Copy example; agent will deny |
| Signature 401s | Use webhook API key; or `VERIFY_RETELL_SIGNATURES=false` for local curl only |
| Agent opens without check | Prompt: open_gate only after approve — temperature ~0.2 |
| Forward myQ before Retell test | Never — finish §5 first |
| Expect human SMS | Product is autonomous — configure `MYQ_*` instead |
| Live traffic with only simulate | Turn `SIMULATE_MYQ_OPEN=false` after API works |

---

## Message to yourself on first live night

- [ ] Guest list loaded for tonight  
- [ ] Webhook deploy up; `AUTONOMOUS=true`; real `MYQ_*`  
- [ ] Health shows `unlock_ready: true` and `simulate_myq_open: false`  
- [ ] One intentional test call from the physical tablet  
