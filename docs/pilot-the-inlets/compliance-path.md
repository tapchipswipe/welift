# Compliance Path — The Inlets Pilot

Plain-English path for We Lift at The Inlets. Sources: [04-risk-setup/](../../04-risk-setup/).

> Not legal advice. Confirm licensing with FDACS Division of Licensing; have Florida counsel review contracts.

---

## What We Lift is (and isn't)

**Is:** Unarmed remote visitor verification + access-control support per HOA post orders.  
**Isn't:** Police, armed guards, premises security guarantee, or warranty that unauthorized entry never occurs.

HOA keeps hardware, internet, post orders. We Lift follows their rules and logs decisions.

---

## Two tracks

| Track | Purpose | Minimum before first open |
|-------|---------|---------------------------|
| **Soft / technical pilot** | Prove routing, voice, unlock, logging | CAM written OK (email/LOE) + post orders draft |
| **Paid pilot** (~$3.5k–4k/mo) | Commercial overnight service | Signed agreement + bound insurance + Class B path |

---

## Minimum viable gates

| Requirement | Soft pilot (first real opens) | Paid pilot |
|-------------|-------------------------------|------------|
| CAM written OK | **Yes** — email or LOE | Signed service agreement |
| Post orders | Draft agreed with CAM | Final + board copy |
| myQ unlock access | Named user or CAM-operated | We Lift SOC account |
| Logging | `events.jsonl` + manual log | + monthly board report |
| Insurance | Disclose startup; quotes in flight | **Bound** GL $1M/$2M + E&O $1M |
| Class B | Confirm requirement; apply or subcontract | Licensed or subcontracted |
| Board | CAM informs board chair | Resolution or manager authority |

**No-go** ([florida-class-b-checklist.md](../../04-risk-setup/florida-class-b-checklist.md)): cannot bind insurance, cannot license/subcontract, CAM demands $5M umbrella you can't place.

---

## Florida Class B

| Scenario | Class B likely? |
|----------|-----------------|
| Marketing as security/access control; **you** perform verify+open | **Highly likely** (Ch. 493) |
| Pure tech pilot; CAM owns access decisions; you're "technology vendor" | **Gray** — confirm with FDACS before paid scale |
| **Subcontract** under licensed Class B agency | **Fastest paid path** — licensee of record on contract/COI |

**Action:** FDACS confirmation call in Week 0. Licensing drives insurance classification.

---

## Insurance order of operations

From [insurance-quote-packet.md](../../04-risk-setup/insurance-quote-packet.md):

1. Form **FL LLC** (Sunbiz) — brokers want entity
2. Email quote packet to **≥ 2 brokers**:
   - Greene & Associates: 1-800-252-6885
   - Prestige Insurance Group
   - Local Sarasota–Bradenton commercial P&C
3. Bind **GL $1M/$2M** + **E&O $1M** + review assault/battery wording
4. Add **umbrella** if CAM requires ($1M–$5M)
5. **Cyber $1M** if storing guest lists / call metadata
6. File statutory **$300k COI with FDACS** when Class B applies (floor only)
7. Issue **COI** naming Association + management company as additional insured

**Budget:** plan **$1,500–4,000/mo** all-in once licensed.

---

## Documents to get from The Inlets

| Document | Purpose |
|----------|---------|
| Board resolution or manager authority to pilot | CAM can sign soft pilot |
| CAM / management LOE or agreement addendum | Scope, hours, fee, termination |
| **Post orders** | Guest rules, vendors, deny/escalate, 911 |
| Guest pass policy | Reinforce myQ-primary; AI = exceptions |
| Emergency contacts | CAM on-call, board president, gate address for 911 |
| Hardware / ISP contacts | Dealer, ISP — outage escalation |
| COI requirements | Their additional-insured language |
| myQ user provisioning approval | We Lift SOC account |

Contract language starter: [service-agreement-liability-clauses.md](../../04-risk-setup/service-agreement-liability-clauses.md) — attorney review before signature.

---

## 30 / 60 / 90 day timeline

### Days 1–30 (technical pilot — August)

- [ ] CAM kickoff + post orders draft
- [ ] FDACS / counsel: Class B required? subcontract?
- [ ] Submit insurance quote packet (parallel)
- [ ] Entity formation if not done
- [ ] Retell + webhook + shadow nights
- [ ] Dealer routes Call Attendant to Retell (controlled test)
- [ ] First **real opens** only with CAM written OK
- [ ] Document every open; zero serious wrong-admits

### Days 31–60 (stabilize + commercialize)

- [ ] Bind insurance (or activate subcontract COI)
- [ ] Class B application or subcontract live
- [ ] Signed pilot agreement + fee
- [ ] Board informed; first monthly summary to CAM
- [ ] myQ API application follow-up
- [ ] Shift from SMS-all-opens → guest-list auto path if metrics good
- [ ] Soft → **paid** conversion or 30-day out

### Days 61–90 (autonomous + scale readiness)

- [ ] API sandbox or SOC automation live
- [ ] ≥ 20 clean API opens; measure 60s SLA
- [ ] Final post orders + data retention policy
- [ ] COI on file with CAM; FDACS COI if Class B
- [ ] Case study / referral clause if discounted trial
- [ ] Decision: expand hours, second HOA, or fix ops
