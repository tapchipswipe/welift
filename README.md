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
| [webhook/](webhook/) | Verify → myQ unlock (autonomous) |
| [configs/](configs/) | Retell LLM + agent JSON |
| [configs/retell-agent-import.json](configs/retell-agent-import.json) | Retell dashboard Import (conversation-flow) |
| [configs/retell-agent-flow.base.json](configs/retell-agent-flow.base.json) | Import template (nodes + tools) |
| [prompt.md](prompt.md) | Vendor-first autonomous prompt |
| [data/guest-list.example.json](data/guest-list.example.json) | Vendor-first authorized list sample |
| [scripts/build_retell_import.py](scripts/build_retell_import.py) | Build Import JSON with webhook base |
| [scripts/create_agent.py](scripts/create_agent.py) | Push configs to Retell API (fallback) |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring |
| [webhook/DEPLOY.md](webhook/DEPLOY.md) | Stable HTTPS deploy |

### Quick start

1. `cp webhook/.env.example webhook/.env` — `AUTONOMOUS=true`. Demos: `SIMULATE_MYQ_OPEN=true`. Live: set `MYQ_*`.
2. `cd webhook && ./run.sh` (or deploy).
3. Create Retell agent via Import JSON — [setup-checklist.md](setup-checklist.md) Option C (or [prompt.md](prompt.md)).
4. Point myQ Call Attendant at the Retell DID only after approve/deny/open tests pass.

**Critical path:** [myQ Partner API](docs/pilot-the-inlets/myq-api-path.md).  

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
