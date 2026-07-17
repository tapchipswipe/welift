# Retell + myQ Call Attendant setup

Use after the webhook is on public HTTPS. Full product checks: [docs/PRODUCT-ACCEPTANCE.md](docs/PRODUCT-ACCEPTANCE.md).  
Tablet wiring: [docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md).

Dashboard: https://dashboard.retellai.com  
Configs: [`configs/retell-llm.json`](configs/retell-llm.json), [`configs/retell-agent.json`](configs/retell-agent.json), prompt [`prompt.md`](prompt.md).

---

## 0. Prerequisites

| Item | Status |
|------|--------|
| Retell account + API key in `webhook/.env` | |
| Webhook running (`cd webhook && ./run.sh`) | |
| Public HTTPS URL | |
| CAM roster at `/access` (or seed vendors) | |
| `SIMULATE_MYQ_OPEN=true` until myQ API | |
| Optional Twilio for real SMS | |

```bash
cd webhook
cp .env.example .env
./run.sh
# other terminal: ngrok http 8080   # or deploy — see webhook/DEPLOY.md
```

---

## 1. Create the LLM + agent (one-shot)

```bash
source webhook/.venv/bin/activate
python scripts/create_agent.py --webhook-base https://YOUR_HOST --community "The Inlets"
```

Writes `configs/retell-ids.json` with `llm_id` / `agent_id`. Tools must hit:

- `POST …/tools/check_guest_list` (vendors require `proof_code`)
- `POST …/tools/open_gate`
- `POST …/tools/escalate_to_oncall`

---

## 2. Phone number

1. Retell → **Phone Numbers** → buy/assign to this agent  
2. Set `RETELL_DID=+1…` in `webhook/.env` (shown on `/gate`)  
3. Cell-test before pointing myQ at it  

---

## 3. Acceptance (cell)

1. CAM sends code from `/access` for GreenSide (or your test vendor)  
2. Call DID → company + **correct PIN** → approve → open (simulate)  
3. Wrong PIN → deny  
4. Resident → redirect, no open  

---

## 4. Wire myQ tablet (only after §3 passes)

Point overnight Call Attendant / quick-call at the **Retell DID**.  
Details: [docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md).

Controlled pedestal test with dealer/CAM. Live barrier motion needs real `MYQ_*`.

---

## 5. Common mistakes

| Mistake | Fix |
|---------|-----|
| Tool URL still placeholder | Re-run `create_agent.py` with current host |
| Opens without PIN | Prompt/tools must require `proof_code` for vendors |
| Forward myQ before cell test | Never |
| Expect human SMS wake | Autonomous product — configure myQ unlock |

---

## First live night

- [ ] Vendors on CAM desk; codes sent  
- [ ] Webhook up; `AUTONOMOUS=true`  
- [ ] Health: `unlock_ready` true  
- [ ] One intentional call from the physical tablet  
