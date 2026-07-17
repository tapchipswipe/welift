# SEND NOW — myQ Partner API (copy/paste)

**To:** integrations@myq.com  
**From:** Lucas Despot  
**Status:** Ready to send — fill email/phone placeholders once.

---

**Subject:** Partner API request — We Lift autonomous gate Call Attendant (Florida HOA pilot)

```
Hello myQ Community Integrations team,

We Lift provides autonomous Call Attendant coverage for LiftMaster / myQ
Community gates in Southwest Florida. Pilot site: The Inlets at Riverdale
(Bradenton / Manatee County — myQ Community + LiftMaster CAP).

We need Partner API access to:
• Remote unlock designated entrance(s) after AI visitor verification
• Read access event history for board reporting (with HOA authorization)
• Later: time-bound guest / vendor credentials (codes + optional company-phone PIN)

Stack:
• Voice: Retell AI on the gate tablet Call Attendant number
• Verification: authorized vendor/guest list via our webhook (approve/deny only)
• Unlock: Partner API from our open_gate tool — fail closed if API errors
• No human attendant on this line; AI is exception-path backup to keypad codes

Product context: CAM authorizes vendors; we prefer keypad (SMS code or company
dispatch phone digits). AI + remote unlock is the fallback when the visitor
has no working code.

Pilot: 1 HOA, 1 main gate.
LiftMaster dealer of record: [UNKNOWN — will confirm with CAM]

Please advise:
1. Partner application steps and timeline
2. Sandbox / test facility requirements
3. Whether The Inlets' dealer must enable integration on the facility
4. Pricing or minimum commit for API access
5. Exact unlock endpoint path + auth scheme

Company: We Lift [LLC pending]
Contact: Lucas Despot · [YOUR EMAIL] · [YOUR PHONE]

Thank you,
Lucas Despot
```

After send: reply in Cursor with “myQ email sent” so we can track Partner wait + keep `SIMULATE_MYQ_OPEN=true` until creds arrive.
