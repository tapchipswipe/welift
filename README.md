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

## Product code

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | CAM Access Desk + credentials + Retell tools + myQ unlock |
| [webhook/static/access.html](webhook/static/access.html) | **CAM admin** desk (`/access`) |
| [webhook/static/gate.html](webhook/static/gate.html) | Call Attendant visitor surface (`/gate`) |
| [data/vendors.seed.json](data/vendors.seed.json) | Seed roster (persists to `vendors.json`) |
| [data/guest-list.example.json](data/guest-list.example.json) | Vendor-first authorized list sample |
| [configs/](configs/) | Retell LLM + agent JSON |
| [configs/retell-agent-import.json](configs/retell-agent-import.json) | Retell dashboard Import (conversation-flow) — alt setup path, see note below |
| [configs/retell-agent-flow.base.json](configs/retell-agent-flow.base.json) | Import template (nodes + tools) |
| [prompt.md](prompt.md) | Vendor proof-PIN autonomous prompt (canonical) |
| [docs/PRODUCT-ACCEPTANCE.md](docs/PRODUCT-ACCEPTANCE.md) | Product pass/fail checks |
| [docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md) | Tablet Call Attendant → Retell DID |
| [docs/GATE-CODE-RUNBOOK.md](docs/GATE-CODE-RUNBOOK.md) | PIN → physical barrier |
| [scripts/create_agent.py](scripts/create_agent.py) | One-shot Retell agent push (API) |
| [scripts/build_retell_import.py](scripts/build_retell_import.py) | Build Import JSON with webhook base |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring (both setup paths) |
| [webhook/DEPLOY.md](webhook/DEPLOY.md) | Stable HTTPS deploy |

> **Two Retell build paths, one prompt should win:** [`prompt.md`](prompt.md) / [`configs/retell-llm.json`](configs/retell-llm.json) require a vendor `proof_code` and match the shipped `webhook/credentials.py` desk. [`configs/retell-agent-import.json`](configs/retell-agent-import.json) / [`configs/retell-agent-flow.base.json`](configs/retell-agent-flow.base.json) (Retell's newer conversation-flow Import format) still embed an older, code-optional prompt. Treat `prompt.md` as canonical and regenerate the Import JSON's conversation-flow prompts to match before using it live — see [docs/PRODUCT.md](docs/PRODUCT.md#retell-build-paths).

### Quick start

1. `cp webhook/.env.example webhook/.env` — `TWILIO_*`, `SIMULATE_MYQ_OPEN=true`, later `RETELL_DID`.
2. `cd webhook && ./run.sh` → **http://127.0.0.1:8080/access** (CAM) and **/gate** (Call Attendant UX).
3. Add vendors (owner or dispatch phone) → Send code → revoke/audit.
4. Create the Retell agent either way — API script: `python scripts/create_agent.py --webhook-base https://HOST`, or dashboard Import JSON: [setup-checklist.md](setup-checklist.md) Option C — then point myQ Call Attendant at the Retell DID only after approve/deny/open tests pass ([docs/MYQ-TABLET-RETELL.md](docs/MYQ-TABLET-RETELL.md)).

**Thesis:** [docs/PRODUCT.md](docs/PRODUCT.md) · **Who gets the SMS:** [docs/VENDOR-CONTACTS.md](docs/VENDOR-CONTACTS.md)

**Critical path for metal:** [myQ Partner API](docs/pilot-the-inlets/myq-api-path.md)

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

## Onboarding an AI agent / indexer

New to this repo? [docs/PROJECT-INDEX-PROMPT.md](docs/PROJECT-INDEX-PROMPT.md) is a copy-paste-ready prompt for Antigravity or any other agentic platform to fully understand and index the project.
