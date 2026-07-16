# Autonomous overnight ops — no human awake

**Pilot:** The Inlets · **Mode:** AI verifies + myQ API unlocks · **No overnight SMS wake**

---

## Product rule

| Situation | AI action | Human overnight? |
|-----------|-----------|------------------|
| Clear guest-list match | `open_gate` → myQ Partner API unlock | **No** |
| No match / ambiguous / ops / noise | **Deny** + log | **No** |
| myQ API down | Fail closed — deny; daytime review of logs | **No** |
| 911 / fire / medical claim | Instruct dial 911; do not open | **No** |

Twilio / on-call SMS is **not** part of the product. Optional `HUMAN_SMS_FALLBACK=true` exists only as a deprecated debug switch.

---

## SLAs (approve → barrier motion)

| Step | Target |
|------|--------|
| Visitor taps Call → AI answers | ≤ 60 sec |
| AI approve → myQ unlock command | ≤ 5 sec |
| Unlock → barrier motion | ≤ 15 sec (hardware) |
| **End-to-end** | ≤ 60 sec |

Marketing: **“Autonomous overnight verify + open.”** Do not say human-confirmed.

---

## Env vars (`webhook/.env`)

| Variable | Value | Required |
|----------|-------|----------|
| `AUTONOMOUS` | `true` | Yes |
| `HUMAN_SMS_FALLBACK` | `false` | Yes |
| `MYQ_API_BASE` / `MYQ_API_KEY` / `MYQ_FACILITY_ID` / `MYQ_ENTRANCE_ID` | Partner credentials | **Yes for live opens** |
| `SIMULATE_MYQ_OPEN` | `true` only for cell demos without API | Demo only |
| `DEFAULT_COMMUNITY` | `The Inlets` | Yes |
| `RETELL_API_KEY` | | Yes (prod signatures) |
| `GUEST_LIST_JSON` or file | Tonight’s exception list | Yes |

---

## Daytime review (not overnight wake)

Each morning, skim `events.jsonl` (or serverless logs) for:

- `decision: deny` with angry / ops flags  
- `open_gate` `status: failed`  
- Unusual volume  

CAM gets a weekly summary — not a 2am phone call.

---

## Critical path to go live

1. myQ Partner API accepted + unlock tested in sandbox  
2. Retell §5 with `SIMULATE_MYQ_OPEN` then real `MYQ_*`  
3. Dealer routes 8pm–6am Call Attendant → Retell DID  
4. Shadow nights with **real API unlock**, fail-closed on errors  

See [myq-api-path.md](myq-api-path.md) · [webhook/DEPLOY.md](../../webhook/DEPLOY.md)
