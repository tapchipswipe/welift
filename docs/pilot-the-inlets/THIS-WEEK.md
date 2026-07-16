# This Week Action Board — We Lift / The Inlets (autonomous)

**Date:** July 16, 2026  
**Product:** AI verifies + myQ opens. **No overnight human.**

---

## Track A — Tech (autonomous stack)

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| A1 | Deploy webhook HTTPS; `AUTONOMOUS=true`, `HUMAN_SMS_FALLBACK=false` | [ ] | [webhook/DEPLOY.md](../../webhook/DEPLOY.md) |
| A2 | Retell agent from `prompt.md` + tools → deploy URL | [ ] | [setup-checklist.md](../../setup-checklist.md) |
| A3 | Cell demos with `SIMULATE_MYQ_OPEN=true` (approve / deny) | [ ] | |
| A4 | **Email myQ Partner API** (critical path) | [ ] | [myq-api-path.md](myq-api-path.md) |
| A5 | When API creds arrive: set `MYQ_*`, turn simulate off, retest unlock | [ ] | [on-call-sms-sla.md](on-call-sms-sla.md) |
| A6 | Record 3 demos for CAM | [ ] | |

Twilio is **not** required.

---

## Track B — CAM

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| B1 | Call Associa Gulf Coast **(941) 552-1598** — Inlets at Riverdale CAM | [ ] | [cam-identification.md](cam-identification.md) |
| B2 | Touch 1 email (info-first) | [ ] | [cam-outreach-touch1.md](cam-outreach-touch1.md) |
| B3 | Parallel Gulf Coast AM + AMI | [ ] | |
| B4 | Pitch: **autonomous overnight verify + open** — exceptions only; myQ passes primary | [ ] | |
| B5 | Aug 1 hard pivot if cold | [ ] | |

---

## Track C — Legal

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| C1 | File FL LLC | [ ] | [entity-insurance-action-kit.md](entity-insurance-action-kit.md) |
| C2 | EIN + insurance quotes ×2 | [ ] | |
| C3 | FDACS Class B call | [ ] | |

---

## Track D — Dealer (after CAM + API path)

| # | Action | Done? | Doc |
|---|--------|-------|-----|
| D1 | Dealer of record + 8pm–6am → Retell DID | [ ] | [dealer-myq-routing.md](dealer-myq-routing.md) |
| D2 | Pedestal test with **real** myQ API unlock | [ ] | |
| D3 | Shadow nights — fail closed on API errors | [ ] | |

---

## Do not do

- Build around waking a human at 2am  
- Forward myQ before Retell + unlock path proven  
- Claim opens work live without `MYQ_*` configured  

**Week done when:** Associa contacted + myQ API email sent + Retell demo with simulate open recorded.
