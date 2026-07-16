# The Inlets Pilot — We Lift Playbooks

**Pilot HOA:** The Inlets (SWFL)  
**Target go-live:** August 2026 — overnight **8:00pm–6:00am Eastern**  
**Product:** **Autonomous** Call Attendant for **vendors/workers** (and other non-residents without code/sticker). Residents keep keypad + RFID. Guest passes preferred for social guests. Unclear → deny. No overnight human.  
**Unlock:** myQ Partner API only (`SIMULATE_MYQ_OPEN` for demos)

---

## Playbook index

| Doc | Purpose |
|-----|---------|
| **[../PRODUCT.md](../PRODUCT.md)** | **Refined product thesis — read first** |
| **[THIS-WEEK.md](THIS-WEEK.md)** | **Single checklist — tech + CAM + legal this week** |
| [decision-log.md](decision-log.md) | Locked product Q&A from Lucas |
| **[pre-cam-playbook.md](pre-cam-playbook.md)** | **No CAM yet — timeline, outreach, pricing, tech order, legal, edge cases** |
| [cam-identification.md](cam-identification.md) | Which Inlets + Associa Gulf Coast lead |
| [cam-outreach-touch1.md](cam-outreach-touch1.md) | Info-first call/email/SMS scripts |
| [cam-kickoff-email.md](cam-kickoff-email.md) | Formal CAM kickoff (after you have a name) |
| [entity-insurance-action-kit.md](entity-insurance-action-kit.md) | Sunbiz LLC, broker emails, FDACS script, soft LOE |
| [dealer-myq-routing.md](dealer-myq-routing.md) | Zero → overnight Call Attendant → Retell DID |
| [on-call-sms-sla.md](on-call-sms-sla.md) | Autonomous ops SLAs (no overnight human) |
| [myq-api-path.md](myq-api-path.md) | Partner API request, hybrid mode, autonomous checklist |
| [compliance-path.md](compliance-path.md) | Class B, insurance, soft vs paid pilot |

**Related repo docs:** [setup-checklist.md](../../setup-checklist.md) · [01-metro-validation/](../../01-metro-validation/) · [04-risk-setup/](../../04-risk-setup/)

---

## August 2026 critical path

> **Update (Jul 15):** No CAM at The Inlets yet. Use [pre-cam-playbook.md](pre-cam-playbook.md) first; treat **Aug 15 live** as stretch — **shadow + CAM demo** is the realistic August win. First pedestal live likely **Aug 29 – Sep 12** if outreach starts this week.

Today → **Aug 1:** technical foundation. **Aug 1–15:** dealer routing + shadow nights. **Aug 15+:** live overnight (SMS bridge OK).

| Week | Dates (approx) | Milestone | Owner | Blocker if missed |
|------|----------------|-----------|-------|-------------------|
| **0** | Jul 15–18 | Retell agent + webhook live; §5 cell tests pass ([setup-checklist.md](../../setup-checklist.md)) | Lucas | Cannot share Retell DID with dealer |
| **0** | Jul 16 | Send [CAM kickoff email](cam-kickoff-email.md) | Lucas | No dealer of record |
| **0** | Jul 17 | Email integrations@myq.com ([myq-api-path.md](myq-api-path.md)) | Lucas | API delayed (non-blocking for Aug) |
| **0** | Jul 17 | Insurance quote packet to 2 brokers ([04-risk-setup/insurance-quote-packet.md](../../04-risk-setup/insurance-quote-packet.md)) | Lucas | Paid pilot blocked |
| **1** | Jul 21–25 | 3-way CAM + dealer call; info checklist complete | CAM + dealer | No pedestal test scheduled |
| **1** | Jul 28–Aug 1 | Dealer programs 8pm–6am → Retell DID; We Lift myQ user created | Dealer | No live routing |
| **2** | Aug 1–8 | On-site pedestal test + 3–7 shadow nights | All | Go-live without validation |
| **2** | Aug 8 | CAM check-in: post orders, metrics, paid-pilot path | Lucas + CAM | Scope creep / no board awareness |
| **3** | **Aug 15** | **First live overnight** (myQ API unlock; fail closed if API down) | Lucas | — |
| **4+** | Aug 15–Sep | Tune prompt/guest list; bind insurance for paid phase | Lucas | Scale before compliance |

---

## Pre-flight (do not skip)

- [ ] Retell approve / deny / open tests pass **before** myQ forward ([setup-checklist.md](../../setup-checklist.md) §5)
- [ ] `MYQ_*` configured (or simulate for demos only) — [on-call-sms-sla.md](on-call-sms-sla.md)
- [ ] CAM written OK for first real opens ([compliance-path.md](compliance-path.md))
- [ ] `DEFAULT_COMMUNITY=The Inlets` + `AUTONOMOUS=true` in `webhook/.env`
- [ ] Do **not** go live without Partner API unlock proven ([myq-api-path.md](myq-api-path.md))

---

## One-line visitor story

> Residents use codes and stickers as today. Social guests use myQ passes. After hours, if a **vendor or worker** without credentials taps **Call Attendant**, AI verifies them against the association’s authorized list and opens the gate — or denies if they’re not on it.
