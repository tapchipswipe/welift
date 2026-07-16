# We Lift — SWFL Virtual Gate Guard

Unified repo for **We Lift**: autonomous overnight gate verification for myQ Community (Retell voice agent) plus the SWFL launch pack (941 / 34211 corridor).

**Beachhead:** 8:00pm–6:00am **autonomous** coverage on LiftMaster + myQ Community. Voice layer is **Retell AI** with tools (`check_guest_list`, `open_gate`, `escalate_to_oncall` = log-only). Unlock = **myQ Partner API**. Ambiguous visits are **denied** — no overnight human.

## Product (Retell agent)

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | FastAPI: verify → myQ unlock (autonomous) |
| [configs/](configs/) | Retell LLM + agent JSON |
| [prompt.md](prompt.md) | Autonomous begin message + system prompt |
| [data/guest-list.example.json](data/guest-list.example.json) | Sample overnight guest list |
| [scripts/create_agent.py](scripts/create_agent.py) | Optional: push configs to Retell API |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring checklist |
| [comet-retell-install-brief.md](comet-retell-install-brief.md) | Paste-into-Comet install brief |

### Quick start

1. Copy `webhook/.env.example` → `webhook/.env` (`AUTONOMOUS=true`). For demos set `SIMULATE_MYQ_OPEN=true`; for live opens set `MYQ_*`.
2. `cd webhook && ./run.sh` — or deploy ([webhook/DEPLOY.md](webhook/DEPLOY.md)).
3. Create the Retell agent ([setup-checklist.md](setup-checklist.md)); point tools at your webhook.
4. Route myQ Call Attendant → Retell DID only after approve/deny/open tests pass with real or simulated unlock.

**Critical path:** myQ Partner API credentials. Without them, the product cannot open gates autonomously.

**Pilot this week:** [docs/pilot-the-inlets/THIS-WEEK.md](docs/pilot-the-inlets/THIS-WEEK.md)

## Launch pack (analyst materials)

| Folder | Deliverable |
|--------|-------------|
| [01-metro-validation/](01-metro-validation/) | Market map: HOA density, CAMs, competitors, overnight wedge |
| [02-pilot-math/](02-pilot-math/) | 10–20 community P&L + peak staffing model |
| [03-channel-test/](03-channel-test/) | CAM interview kit, firm targets, outreach, findings |
| [04-risk-setup/](04-risk-setup/) | Insurance quote packet + contract liability language |
| [mockups/](mockups/) | myQ tablet / kiosk HTML mockups |

### Suggested order

1. Read [01-metro-validation/SWFL-941-metro-map.md](01-metro-validation/SWFL-941-metro-map.md).
2. Run `python3 02-pilot-math/staffing_model.py` to stress-test concurrency.
3. Use [03-channel-test/outreach-emails.md](03-channel-test/outreach-emails.md) for CAM outreach.
4. Complete [04-risk-setup/](04-risk-setup/) before any paid pilot.
5. Ship the voice stack using the product paths above.

Historical Smith.ai references in older docs are for comparison only; production voice is Retell-only.
