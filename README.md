# We Lift — SWFL Virtual Gate Guard

Unified repo for **We Lift**: autonomous overnight gate verification for myQ Community (Retell voice agent) plus the SWFL launch pack (941 / 34211 corridor).

**Beachhead:** 8:00pm–6:00am virtual coverage on LiftMaster + myQ Community. Voice layer is **Retell AI** with custom tools (`check_guest_list`, `open_gate`, `escalate_to_oncall`). Phase 1 unlock = SMS on-call → myQ remote open.

## Product (Retell agent)

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | FastAPI handlers: `check_guest_list`, `open_gate`, `escalate_to_oncall` |
| [configs/](configs/) | Retell LLM + agent JSON (API or dashboard import) |
| [prompt.md](prompt.md) | Begin message, system prompt, FAQs |
| [data/guest-list.example.json](data/guest-list.example.json) | Sample overnight guest list |
| [scripts/create_agent.py](scripts/create_agent.py) | Optional: push configs to Retell API |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring checklist |
| [comet-retell-install-brief.md](comet-retell-install-brief.md) | Paste-into-Comet install brief |

### Quick start

1. Copy `webhook/.env.example` → `webhook/.env` and set Twilio / Retell secrets.
2. `cd webhook && ./run.sh` — expose with ngrok (see [webhook/README.md](webhook/README.md)).
3. Create the Retell agent using [setup-checklist.md](setup-checklist.md) and point tools at your webhook URLs.
4. Route myQ Call Attendant to the Retell DID for a pilot window.

Phase 1: `open_gate` SMSes the on-call operator to unlock in myQ. Phase 2: direct myQ Community remote unlock.

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
