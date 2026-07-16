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
cd 05-retell-agent/webhook
cp ../data/guest-list.example.json ../data/guest-list.json
cp .env.example .env   # fill RETELL_API_KEY + ONCALL_PHONE
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
# other terminal:
ngrok http 8080
```

---

## 1. Create the LLM (Response Engine)

**Option A — script**

```bash
cd 05-retell-agent
source webhook/.venv/bin/activate
python scripts/create_agent.py --webhook-base https://YOUR_NGROK.ngrok-free.app --community "Pilot HOA"
```

**Option B — dashboard**

1. **Agents → Create** (or Response Engine → Retell LLM)
2. Paste **begin_message** and **general_prompt** from [`prompt.md`](prompt.md)
3. Set temperature ~**0.2** (strict verifier)
4. Add tools (see §2)
5. Set dynamic variable `community_name` = `Pilot HOA` (change per HOA later)

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

Call the Retell number. Walk three paths:

1. **Approve** — use a name from `guest-list.json` (e.g. Jordan Lee / Sam Rivera)  
   - Expect: check → open → SMS/log `OPEN … unlock myQ NOW`  
2. **Deny** — random visitor + host not on list  
   - Expect: deny script; no open SMS  
3. **Escalate** — mumble / conflicting info  
   - Expect: escalate SMS; no open  

Confirm `data/events.jsonl` grows with each tool call.

---

## 6. Wire myQ tablet (only after §5 passes)

Same pattern as Smith ([how-to-connect-myq-to-smith.md](../01-metro-validation/how-to-connect-myq-to-smith.md)):

> Point overnight Call Attendant / quick-call at the **Retell DID**, 8pm–6am.

Do a controlled 10-minute pedestal test with the dealer/CAM present.

---

## 7. Phase 1 unlock SOP (you)

When SMS arrives:

1. Open myQ Community → that entrance → **Unlock**  
2. Optional: note time in your log  
3. Later (Phase 2): replace SMS with partner myQ remote-open API  

---

## 8. Common mistakes

| Mistake | Fix |
|---------|-----|
| Tool URL still `YOUR_WEBHOOK_HOST` | Update all three custom function URLs |
| No `guest-list.json` | Copy example; agent will escalate |
| Signature 401s | Use webhook API key; or `VERIFY_RETELL_SIGNATURES=false` for local curl only |
| Agent opens without check | Prompt must say open_gate only after approve — tighten temperature |
| Forward myQ before Retell test | Never — finish §5 first |

---

## Message to yourself on first live night

- [ ] Guest list loaded for tonight  
- [ ] Webhook + ngrok/deploy up  
- [ ] Phone on loud for SMS  
- [ ] myQ unlock works from your phone  
- [ ] One intentional test call from the physical tablet  
