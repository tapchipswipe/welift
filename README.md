# We Lift — SWFL Vendor Call Attendant

Autonomous **Call Attendant** for LiftMaster / myQ Community gates in Southwest Florida — plus the SWFL launch pack (941 corridor).

## The idea (refined)

Residents already get in with a **keypad code** or **RFID sticker**. Guests should use **myQ guest passes**.  

**We Lift handles the exception:** vendors and workers (gardeners, pool techs, contractors) who don’t have those credentials tap Call Attendant → AI verifies against the association’s authorized list → **myQ opens the gate** (or denies). Low volume by design. No overnight human.

Full thesis: **[docs/PRODUCT.md](docs/PRODUCT.md)**

| We are | We are not |
|--------|------------|
| Vendor / worker exception path | Replacement for codes & stickers |
| Autonomous verify + myQ unlock | 2am SMS to a founder |
| Low-call-volume software | Full virtual guardhouse (Envera-class) |

## Product code

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | Verify → myQ unlock (autonomous) |
| [configs/](configs/) | Retell LLM + agent JSON |
| [prompt.md](prompt.md) | Vendor-first autonomous prompt |
| [data/guest-list.example.json](data/guest-list.example.json) | Vendor-first authorized list sample |
| [scripts/create_agent.py](scripts/create_agent.py) | Push configs to Retell API |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring |
| [webhook/DEPLOY.md](webhook/DEPLOY.md) | Stable HTTPS deploy |

### Quick start

1. `cp webhook/.env.example webhook/.env` — `AUTONOMOUS=true`. Demos: `SIMULATE_MYQ_OPEN=true`. Live: set `MYQ_*`.
2. `cd webhook && ./run.sh` (or deploy).
3. Create Retell agent from [setup-checklist.md](setup-checklist.md) / [prompt.md](prompt.md).
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
