# On-Call & SMS SLA — Phase 1

**Pilot:** The Inlets · **Operator:** Lucas (sole on-call Phase 1)  
**Open path (August):** Retell `open_gate` → SMS → Lucas taps **Unlock** in myQ Community

---

## Recommended model: sole operator

For one gate, one HOA:

| Model | Verdict |
|-------|---------|
| **Lucas solo** | **Recommended** — ~6–10 AI calls/night base case; ~4–8 opens on busy nights. One phone, one myQ login, full audit trail. |
| Shared backup | Only if Lucas cannot cover 8pm–6am **and** one trusted backup completes a supervised shadow night first. |

Run **hybrid** first 14 nights: AI handles conversation; **every** open = SMS → manual myQ tap. See [02-pilot-math/one-hoa-full-ai-trial-deep-dive.md](../../02-pilot-math/one-hoa-full-ai-trial-deep-dive.md).

---

## SLAs (SMS → barrier motion)

| Step | Target | Notes |
|------|--------|-------|
| Visitor taps Call → AI answers | **≤ 60 sec** | Aligns with [04-risk-setup/service-agreement-liability-clauses.md](../../04-risk-setup/service-agreement-liability-clauses.md) §3.1 |
| AI approve → SMS delivered | **≤ 5 sec** | Requires Twilio live — log-only mode unacceptable for pilot |
| SMS → human taps Unlock in myQ | **≤ 30 sec** | Lucas keeps phone on loud; myQ app logged in |
| Unlock tap → barrier starts moving | **≤ 15 sec** | Gate hardware + myQ latency |
| **End-to-end (approve → motion)** | **≤ 60 sec** | Tell visitor to wait for gate ([prompt.md](../../prompt.md)) |

**Escalation:** ambiguous calls → `escalate_to_oncall` SMS; callback or deny within **3 min** if visitor still waiting.

**Marketing:** Do **not** promise autonomous open during Phase 1. Say “AI-assisted overnight attendant with human-confirmed remote open.”

---

## Nightly SOP (Lucas)

When SMS arrives: `OPEN [The Inlets] … unlock myQ NOW`

1. Open myQ Community → main entrance → **Unlock**
2. Confirm barrier motion before telling visitor (if still on line)
3. Note time in log; verify `data/events.jsonl` entry

Pre-shift checklist ([setup-checklist.md](../../setup-checklist.md) §7):

- [ ] Guest list loaded for tonight (`data/guest-list.json`)
- [ ] Webhook + HTTPS deploy up
- [ ] Phone on loud; myQ app ready
- [ ] One intentional test call if any config changed

---

## Shared rotation (Phase 2 ops — if needed)

```
Primary:   Lucas (Mon–Thu + Sun)
Backup:    [Trusted person] (Fri–Sat)
Handoff:   Shared doc — myQ login, post orders, guest-list process
Alert:     Single ONCALL_PHONE in Phase 1 (webhook sends to one number)
Rule:      Backup completes one supervised shadow night before solo shift
```

No PagerDuty for one gate.

---

## Phase 1 → Phase 2 path

| Phase | Open path | Claim |
|-------|-----------|-------|
| **1a** (nights 1–14) | Every open = SMS → Lucas taps myQ | “AI-assisted overnight attendant” |
| **1b** (nights 15–30) | Auto-SMS only for exact guest-list matches; escalate rest | “Automated verification; human-confirmed opens” |
| **2** | `open_gate` → **myQ Partner API**; SMS fallback on API error | **“Autonomous verify + open”** (after [myq-api-path.md](myq-api-path.md) checklist) |

Code: extend `webhook/main.py` `open_gate` to call myQ API when credentials exist; keep SMS fallback.

---

## Environment variables (`webhook/.env`)

From [webhook/.env.example](../../webhook/.env.example) and [webhook/README.md](../../webhook/README.md):

| Variable | Pilot value | Required |
|----------|-------------|----------|
| `RETELL_API_KEY` | Your Retell key | Yes (prod signature verify) |
| `ONCALL_PHONE` | Lucas cell E.164 e.g. `+1941…` | **Yes** |
| `DEFAULT_COMMUNITY` | `The Inlets` | Yes |
| `VERIFY_RETELL_SIGNATURES` | `false` local → `true` prod | Yes |
| `TWILIO_ACCOUNT_SID` | Twilio creds | **Strongly recommended** |
| `TWILIO_AUTH_TOKEN` | | |
| `TWILIO_FROM_NUMBER` | | |
| `IGNORE_VALIDITY_WINDOW` | `false` (or `true` early pilot) | Optional |
| `SERVERLESS` | `false` unless deploy requires | Optional |

**Also:**

- Copy `data/guest-list.example.json` → `data/guest-list.json`
- Point Retell tools at HTTPS webhook: `/tools/check_guest_list`, `/tools/open_gate`, `/tools/escalate_to_oncall`
- Set Retell dynamic variable `community_name` = `The Inlets`

**Never commit** `.env` or real guest lists with PII to git.
