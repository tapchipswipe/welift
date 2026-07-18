# We Lift Project Index

## Product in one sentence

We Lift manages vendor access for gated communities: a CAM authorizes a vendor,
the vendor receives a time-bound keypad code, and Retell/myQ is a fail-closed
voice fallback for a visitor who arrives without one. Residents retain their
existing keypad or RFID access.

## Start here

1. [Product thesis](PRODUCT.md) — canonical positioning, scope, and Retell prompt status.
2. [Security model](GATE-SECURITY.md) — authorization, credential, and fail-closed rules.
3. [Pilot decision log](pilot-the-inlets/decision-log.md) — locked product decisions for The Inlets.
4. [This week's action board](pilot-the-inlets/THIS-WEEK.md) — current business and technical work.
5. [Product acceptance](PRODUCT-ACCEPTANCE.md) — end-to-end pass criteria.

## Runtime architecture

```text
CAM Access Desk (/access) ──> FastAPI credential engine ──> Twilio SMS ──> vendor keypad
                                      │
Vendor Portal (Clerk + Next.js) ──────┘
                                      │
No-code visitor ──> Retell voice agent ──> FastAPI tools ──> myQ unlock
                                                    └──> log and deny on uncertainty/error
```

Both runnable services use the same database schema. Locally this is
`data/welift.db`; production is intended to use a shared PostgreSQL
`DATABASE_URL`.

## Applications

| Area | Role | Key files |
| --- | --- | --- |
| `webhook/` | FastAPI backend and CAM/visitor web surfaces | `main.py`, `credentials.py`, `models.py`, `static/access.html`, `static/gate.html` |
| `portal/` | Authenticated vendor dispatcher portal | `app/actions.ts`, `app/dashboard/`, `lib/credentials.ts`, `prisma/schema.prisma` |

### `webhook/` capabilities

- CAM roster CRUD, credential mint/send/revoke, and audit endpoints under `/access`.
- Keypad verification at `/gate/verify_code`.
- Retell tools: `/tools/check_guest_list`, `/tools/open_gate`, and `/tools/escalate_to_oncall`.
- myQ unlock is simulated only when `SIMULATE_MYQ_OPEN=true`; without simulation or `MYQ_*` credentials it fails closed.

### `portal/` capabilities

- Clerk-protected dispatcher dashboard.
- Authorizes a signed-in email against `vendor_companies.invite_email`.
- Lets an authorized vendor issue a time-bound code to a technician through the shared credential logic.
- Uses Prisma against the same tables as FastAPI.

## Non-negotiable rules

1. No human overnight bridge or founder wake-up path.
2. Deny by default; do not open on ambiguity or myQ failure.
3. Vendors must supply the current proof code for voice-assisted access.
4. The AI never grants resident access; residents use their existing access method.
5. Production voice is Retell-only; Smith.ai material is historical context.
6. Keep `prompt.md`, `configs/retell-llm.json`, and `webhook/main.py` behavior aligned.

## Configuration and verification

| Need | Where |
| --- | --- |
| Local FastAPI setup and smoke tests | [`webhook/README.md`](../webhook/README.md) |
| Stable webhook deployment | [`webhook/DEPLOY.md`](../webhook/DEPLOY.md) |
| Full Railway/Vercel deployment | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Retell and myQ wiring | [`setup-checklist.md`](../setup-checklist.md) |
| Automated tool and credential tests | `webhook/test_tools.py`, `webhook/test_credentials.py` |
| Deployment endpoint check | `scripts/verify_deployment.py` |

## Documentation map

| Area | Purpose |
| --- | --- |
| `docs/pilot-the-inlets/` | Active pilot outreach, API path, compliance, and decision records. |
| `docs/VENDOR-PORTAL*.md` | Portal product intent and phased roadmap. |
| `01-metro-validation/` | Southwest Florida market validation. |
| `02-pilot-math/` | Pilot costs, pricing, and staffing models. |
| `03-channel-test/` | CAM outreach and interview materials. |
| `04-risk-setup/` | Florida licensing, insurance, and contract work. |
| `mockups/` | Reference-only HTML and image mockups. |

## Current blockers

- A stable public webhook host is needed before a CAM demo or persistent Retell tool wiring.
- Retell API credentials and a DID are needed to complete the live voice path.
- myQ Partner API credentials are needed for physical opens; until then only simulated unlocks are valid.
- The Retell dashboard Import JSON still contains an older, code-optional conversation flow. Treat `prompt.md` as canonical and reconcile the Import flow before production use.

