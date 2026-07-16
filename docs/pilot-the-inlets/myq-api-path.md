# myQ Remote-Open Path — Autonomous Product

**Product rule:** AI verifies + **myQ Partner API** opens. No overnight human. No SMS wake.

---

## Recommendation

| Question | Answer |
|----------|--------|
| SMS / human unlock overnight? | **No** — rejected as product path |
| Cell demos without API? | `SIMULATE_MYQ_OPEN=true` only |
| Claim autonomous before API? | **No** — voice demo ≠ live open |
| When to email myQ? | **Week 0 — critical path** |

Partner review often **4–12+ weeks**. Start now; do not design the product around waiting while awake at 2am.

---

## Email template — integrations@myq.com

```
Subject: Partner API request — We Lift autonomous overnight gate attendant (Florida HOA)

Hello myQ Community Integrations team,

We Lift provides autonomous overnight (8pm–6am) virtual gate attendant services
for gated communities in Southwest Florida. Pilot site: The Inlets
(myQ Community + LiftMaster CAP).

We need Partner API access to:
• Remote unlock designated entrance(s) after AI visitor verification
• Read access event history for board reporting (with HOA authorization)
• Optionally read/time-bound guest credentials in later phases

Stack:
• Voice: Retell AI at the gate tablet Call Attendant number
• Verification: guest list + post orders via our webhook (approve/deny only)
• Unlock: Partner API from our open_gate tool — fail closed if API errors
• No overnight human attendant

Pilot: 1 HOA, 1 main gate, Manatee/Sarasota County FL.
LiftMaster dealer of record: [DEALER NAME, if known].

Please advise:
1. Partner application steps and timeline
2. Sandbox / test facility requirements
3. Whether The Inlets' dealer must enable integration on the facility
4. Pricing or minimum commit for API access
5. Exact unlock endpoint path + auth scheme (we will align MYQ_UNLOCK_PATH)

Company: We Lift [LLC name when formed]
Contact: Lucas Despot · [YOUR EMAIL] · [YOUR PHONE]

Thank you,
Lucas Despot
```

---

## Confirmed autonomous checklist

Before telling the board **“autonomous verify + open”**:

- [ ] myQ Partner API credentials live in webhook env
- [ ] `SIMULATE_MYQ_OPEN=false`, `HUMAN_SMS_FALLBACK=false`
- [ ] ≥ 20 consecutive API opens with **zero** wrong-admit incidents
- [ ] End-to-end open ≤ 60 sec in ≥ 95% of tests
- [ ] API error → fail closed (deny script); logged for daytime review
- [ ] Every open in events log + myQ activity correlation
- [ ] Post orders: deny-when-unsure overnight policy agreed with CAM

---

## Implementation (welift v0.4+)

`webhook/main.py` `open_gate`:

1. Attempt myQ Partner API unlock (`MYQ_*` env)
2. On success → `status: opened`
3. On failure / missing config → `status: failed` (agent denies; no human SMS)

`escalate_to_oncall` → `logged_deny` only (daytime audit).

Reference: [on-call-sms-sla.md](on-call-sms-sla.md) · [webhook/.env.example](../../webhook/.env.example)
