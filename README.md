# We Lift — SWFL Vendor Call Attendant

Autonomous **Call Attendant** for LiftMaster / myQ Community gates in Southwest Florida — plus the SWFL launch pack (941 corridor).

## The idea (refined)

Residents already get in with a **keypad code** or **RFID sticker**. Guests should use **myQ guest passes**.

**We Lift:** CAM approves vendors (and their phones) → we **auto-text a time-bound gate code** → they use the keypad. **AI Call Attendant is only the backup** when someone has no code — verify + myQ unlock (or deny). That cuts AI cost and beats “I’m with the lawn company” on the speaker.

Full thesis: **[docs/PRODUCT.md](docs/PRODUCT.md)** · Security: **[docs/GATE-SECURITY.md](docs/GATE-SECURITY.md)**

| We are | We are not |
|--------|------------|
| Vendor **credential desk** + rare AI fallback | AI receptionist for every truck |
| Time-bound codes to known phones | Eternal shared vendor codes |
| Autonomous unlock when AI is needed | 2am SMS to a founder |

## Product code (real thin MVP)

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | Access Desk + credential SMS + Retell proof PIN + myQ unlock |
| [webhook/static/access.html](webhook/static/access.html) | **Access Desk UI** (`GET /access`) |
| [data/vendors.seed.json](data/vendors.seed.json) | The Inlets sample vendors |
| [configs/](configs/) | Retell LLM + agent JSON |
| [prompt.md](prompt.md) | Vendor proof-PIN autonomous prompt |
| [docs/SALES-DEMO.md](docs/SALES-DEMO.md) | 5-minute live demo script |
| [docs/PHASE0-OPS.md](docs/PHASE0-OPS.md) | Twilio / myQ / Associa checklist |
| [docs/GATE-CODE-RUNBOOK.md](docs/GATE-CODE-RUNBOOK.md) | Wire PIN → physical barrier |
| [docs/PILOT-WEEK.md](docs/PILOT-WEEK.md) | The Inlets pilot week |
| [scripts/send_vendor_code.py](scripts/send_vendor_code.py) | CLI mint + SMS |
| [webhook/DEPLOY.md](webhook/DEPLOY.md) | Stable HTTPS deploy |

### Quick start

1. `cp webhook/.env.example webhook/.env` — set `TWILIO_*`, `AUTONOMOUS=true`, `SIMULATE_MYQ_OPEN=true` for demos.
2. `cd webhook && ./run.sh` → open **http://127.0.0.1:8080/access**
3. Send a code → phone buzzes (or log-only without Twilio).
4. Retell agent from [setup-checklist.md](setup-checklist.md) / [prompt.md](prompt.md) — vendors need `proof_code`.
5. Deploy stable HTTPS before a CAM meeting — [webhook/DEPLOY.md](webhook/DEPLOY.md).

**Critical path for metal:** [myQ Partner API](docs/pilot-the-inlets/myq-api-path.md) · [GATE-CODE-RUNBOOK.md](docs/GATE-CODE-RUNBOOK.md)

**This week:** [docs/pilot-the-inlets/THIS-WEEK.md](docs/pilot-the-inlets/THIS-WEEK.md)

## Pilot — The Inlets

Playbooks: [docs/pilot-the-inlets/](docs/pilot-the-inlets/) · Locked decisions: [decision-log.md](docs/pilot-the-inlets/decision-log.md)

## Launch pack (analyst)

| Folder | Deliverable |
|--------|-------------|
| [01-metro-validation/](01-metro-validation/) | Market map: HOA density, CAMs, competitors |
| [02-pilot-math/](02-pilot-math/) | P&L + staffing model (re-anchor to vendor desk, not full guard) |
| [03-channel-test/](03-channel-test/) | CAM interview kit + outreach |
| [04-risk-setup/](04-risk-setup/) | Insurance + contract liability |
| [mockups/](mockups/) | myQ tablet HTML mockups |

Historical Smith.ai docs are archive/comparison only. Production voice is Retell-only.
