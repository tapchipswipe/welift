# WeLift

Autonomous overnight gate verification for myQ Community — a Retell voice agent that checks the guest list and requests a gate open **during** the call via custom webhooks.

## Layout

| Path | Purpose |
|------|---------|
| [webhook/](webhook/) | FastAPI handlers: `check_guest_list`, `open_gate`, `escalate_to_oncall` |
| [configs/](configs/) | Retell LLM + agent JSON (API or dashboard import) |
| [prompt.md](prompt.md) | Begin message, system prompt, FAQs |
| [data/guest-list.example.json](data/guest-list.example.json) | Sample overnight guest list |
| [scripts/create_agent.py](scripts/create_agent.py) | Optional: push configs to Retell API |
| [setup-checklist.md](setup-checklist.md) | Retell + myQ wiring checklist |

## Quick start

1. Copy `webhook/.env.example` → `webhook/.env` and set Twilio / Retell secrets.
2. `cd webhook && ./run.sh` — expose with ngrok (see [webhook/README.md](webhook/README.md)).
3. Create the Retell agent using [setup-checklist.md](setup-checklist.md) and point tools at your webhook URLs.
4. Route myQ Call Attendant to the Retell DID for a pilot window.

Phase 1: `open_gate` SMSes the on-call operator to unlock in myQ. Phase 2: direct myQ Community remote unlock.

Analyst launch materials (market validation, Smith.ai comparisons, mockups) live in the separate **virtual-gate-guard** repo.
