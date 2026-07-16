# myQ Remote-Open Path — Autonomous Target

**Q1 goal:** Fully autonomous verify + open via myQ Partner API.  
**August pilot:** SMS bridge is **OK** for 30–60 nights if disclosed as human-confirmed.

---

## Recommendation

| Question | Answer |
|----------|--------|
| SMS-forever for 1-HOA trial? | **Yes** for technical learning (30–60 nights). Not a scale model. |
| Pursue API before paid pilot? | **Yes — start Week 0.** Paid contract should assume API or dedicated SOC account, not Lucas at 2am forever. |
| Claim “autonomous” in August? | **No** until checklist below passes. Say “AI verification + human-confirmed open” for SMS phase. |

**Realistic API timeline:** partner review often **4–12+ weeks** — plan SMS for entire first pilot month.

---

## Email template — integrations@myq.com

```
Subject: Partner API request — We Lift overnight virtual gate attendant (Florida HOA pilot)

Hello myQ Community Integrations team,

We Lift provides overnight (8pm–6am) virtual gate attendant services for gated
communities in Southwest Florida. Our pilot site is The Inlets, an existing
myQ Community + LiftMaster CAP installation.

We are a software/service partner (not a PMS). We need API access to:
• Remote unlock designated entrance(s) after visitor verification
• Read access event history for board reporting (with HOA authorization)
• Optionally manage/time-bound guest credentials in later phases

Current stack:
• Voice: Retell AI at the gate tablet Call Attendant number
• Verification: guest list + post orders via our webhook
• Phase 1: human unlock via myQ app; Phase 2: API unlock from open_gate

Pilot: 1 HOA, 1 main gate, Manatee/Sarasota County FL.
LiftMaster dealer of record: [DEALER NAME, if known].

Please advise:
1. Partner application steps and timeline
2. Sandbox / test facility requirements
3. Whether The Inlets' dealer must enable integration on the facility
4. Pricing or minimum commit for API access

Company: We Lift [LLC name when formed]
Contact: Lucas Despot · [YOUR EMAIL] · [YOUR PHONE]

Thank you,
Lucas Despot
```

**Parallel:** Ask The Inlets dealer on discovery call whether they've enabled API integrations at other properties.

---

## Hybrid mode (aligned with Q1)

```
Nights 1–14:   AI verify + SMS Lucas for ALL opens
Nights 15–30:  AI verify + auto-open only exact guest-list matches (API or fast SMS)
Nights 31+:    API primary; SMS fallback on API error; escalate on ambiguity
```

---

## “Confirmed autonomous” checklist

Before telling The Inlets board **“autonomous verify + open”**:

- [ ] myQ Partner API **or** dedicated SOC service account with documented unlock wrapper
- [ ] **≥ 20 consecutive** API opens with **zero** wrong-admit incidents
- [ ] End-to-end open **≤ 60 sec** in ≥ 95% of tests (API path)
- [ ] SMS fallback tested when API returns error
- [ ] Every open in `data/events.jsonl` + myQ activity log correlation
- [ ] Post orders signed; CAM knows escalation path
- [ ] Insurance + licensing path underway for paid phase
- [ ] Retell containment ≥ 70% without human ping ([02-pilot-math/one-hoa-full-ai-trial-deep-dive.md](../../02-pilot-math/one-hoa-full-ai-trial-deep-dive.md) §10)

---

## Implementation note (welift)

When API credentials arrive, extend `webhook/main.py` `open_gate`:

1. Attempt myQ Partner API remote unlock for configured entrance ID
2. On failure → fall back to existing SMS to `ONCALL_PHONE`
3. Log outcome to `data/events.jsonl`

Reference: [README.md](../../README.md) Phase 2 · [01-metro-validation/liftmaster-integration.md](../../01-metro-validation/liftmaster-integration.md) §2
