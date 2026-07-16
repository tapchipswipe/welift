# This Week Action Board — We Lift / The Inlets

**Date:** July 16, 2026  
**August success (realistic):** tech proof + CAM conversation started + shadow path — not paid Aug 15 live.

Owners: Lucas (all rows). Check boxes as you finish. Details live in linked docs.

---

## Track A — Tech (unblock everything else)

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| A1 | Copy `webhook/.env.example` → `webhook/.env`; set Retell key + `ONCALL_PHONE` + `DEFAULT_COMMUNITY=The Inlets` | [ ] | [webhook/README.md](../../webhook/README.md) |
| A2 | `cd webhook && ./run.sh` — `/health` returns ok | [ ] | |
| A3 | Create Twilio account; buy 941 (or FL) number; set `TWILIO_*`; prove SMS hits phone via `open_gate` | [ ] | [on-call-sms-sla.md](on-call-sms-sla.md) |
| A4 | Deploy webhook to **stable HTTPS** (Railway / Fly / Docker) | [ ] | [webhook/DEPLOY.md](../../webhook/DEPLOY.md) |
| A5 | Retell agent: prompt + tools pointed at deploy URL (`community_name=The Inlets`) | [ ] | [setup-checklist.md](../../setup-checklist.md) · [comet-retell-install-brief.md](../../comet-retell-install-brief.md) |
| A6 | §5 cell tests: approve / deny / escalate | [ ] | setup-checklist §5 |
| A7 | Record 3 demo calls (shareable) | [ ] | [pre-cam-playbook.md](pre-cam-playbook.md) §D |
| A8 | Email myQ Partner API request | [ ] | [myq-api-path.md](myq-api-path.md) |

**Code already ready in repo:** Phase 1 SMS tools, Phase 2 myQ unlock stub, fuzzy guest-list match, deploy configs, tests.

---

## Track B — CAM

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| B1 | Call Associa Gulf Coast Sarasota **(941) 552-1598** — ask who manages The Inlets at Riverdale | [ ] | [cam-identification.md](cam-identification.md) |
| B2 | Send Touch 1 email to named CAM (or Associa route-please) | [ ] | [cam-outreach-touch1.md](cam-outreach-touch1.md) |
| B3 | Same day: parallel email/call Gulf Coast AM + AMI | [ ] | cam-outreach-touch1 §E |
| B4 | Optional: daytime gate visit — photo CAP label | [ ] | cam-identification |
| B5 | On reply: formal kickoff + six-item checklist | [ ] | [cam-kickoff-email.md](cam-kickoff-email.md) |
| B6 | **Aug 1 hard pivot** if still cold | [ ] | pre-cam-playbook §H |

---

## Track C — Legal / insurance

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| C1 | File FL LLC on Sunbiz | [ ] | [entity-insurance-action-kit.md](entity-insurance-action-kit.md) |
| C2 | Get EIN | [ ] | same |
| C3 | Send insurance quote packet to ≥2 brokers | [ ] | entity kit + [insurance-quote-packet.md](../../04-risk-setup/insurance-quote-packet.md) |
| C4 | FDACS Class B confirmation call | [ ] | entity kit §3 |
| C5 | Soft LOE only after CAM + tech ready | [ ] | entity kit §4 |

---

## Track D — Dealer / myQ (after CAM)

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| D1 | Get dealer of record from CAM | [ ] | [dealer-myq-routing.md](dealer-myq-routing.md) |
| D2 | 3-way call; program 8pm–6am → Retell DID **after** A6 | [ ] | dealer-myq-routing |
| D3 | Pedestal test + shadow nights | [ ] | pilot README |

---

## Do not do yet

- Forward myQ Call Attendant before A6 passes  
- Claim "autonomous open" (Phase 1 = human-confirmed)  
- Sign paid contract without LLC + insurance path  
- Quote below ~$995/mo effective ([pre-cam-playbook.md](pre-cam-playbook.md) §C)

---

## Definition of done for this week (Jul 16–18)

- [ ] Associa called + Touch 1 sent  
- [ ] Twilio SMS proven OR blocked only on account signup  
- [ ] Webhook on stable HTTPS **or** scheduled deploy date  
- [ ] LLC filing started **or** consciously deferred with date  
- [ ] myQ API email sent  
