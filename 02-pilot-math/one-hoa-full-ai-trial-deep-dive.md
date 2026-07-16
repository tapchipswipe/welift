# Deep Dive: 1-HOA Full-AI Trial P&L (8pm–6am)

**Scenario:** First paying (or soft-paying) association. LiftMaster + **myQ Community** already installed. Your product is overnight **live AI voice attendant** that can verify and remote-open. No dedicated human SOC yet.

**Coverage:** 8:00pm–6:00am (10 hrs)  
**Not included in “full AI”:** daytime booth, your own hired overnight agents

---

## 1. What “full AI” means in cash terms

```text
Visitor at gate (8pm–6am)
  → LiftMaster rings your SIP / DID
  → AI voice agent answers
  → Collects name / address / purpose
  → Checks guest list / pass / directory (tool call)
  → HIGH confidence → remote open via myQ / relay
  → LOW confidence → deny, instruct to get pass, or SMS you
  → Log everything for board PDF
```

**Money only leaves for:** voice minutes, phone numbers, hosting, thin insurance, and *your* time.  
**Money does not leave for:** W-2 overnight agents (that’s the point of this trial).

---

## 2. Revenue — what you can charge one HOA

| Price tier | $/mo | When to use |
|------------|------|-------------|
| Free pilot | $0 | Only if you need a logo; treat as R&D |
| Friends / CAM intro | $2,500 | High-touch learning; still covers AI + fixed |
| Trial list | **$3,500–$4,000** | Recommended first paid |
| Full list | **$4,800** | After 30–60 clean nights |
| Aggressive vs Envera | $2,900–$3,500 | If CAM says Envera quote is ~$1.5–3k |

**Board value anchor (their cost):**  
Overnight manned ~10 hrs × $30 × 30 ≈ **$9,000/mo**.  
Even at $4,000 you are selling ~**55% savings**.

**Recommended trial charge:** **$4,000/mo** (or $3,500 if they sign a case-study + referral clause).

---

## 3. Variable cost — AI usage (the small number)

### Formula
```
minutes/mo = sites × calls_needing_AI_per_night × avg_minutes × 30
AI_$ = minutes × all_in_rate
```

### What drives “calls needing AI”
Most cars never hit you:

| Path | Hits AI? |
|------|----------|
| Keypad / myQ code | No |
| Guest pass | No |
| Resident unlocks in app | No |
| “Call guard” / directory / no code | **Yes** |

### Call-volume bands (1 gate, overnight)

| Band | AI calls / night | Why |
|------|------------------|-----|
| Quiet / well-run myQ | 3–5 | Passes + codes doing their job |
| **Base** | **6–10** | Typical first HOA |
| Messy | 12–20 | Shared codes, no guest-pass culture |
| Broken ops | 25+ | You’re the default entry — fix product/process |

### Talk time
- Clean verify + open: **1.5–2.5 min**  
- Argument / no resident answer / language: **4–6 min**  
- Use **2.5 min** average for planning

### All-in AI rate
Voice platforms (Retell / Vapi / Bland-class) real-world: **~$0.12–$0.25/min**.  
Use **$0.18/min** midpoint.

### Usage table (1 HOA)

| Calls/night | Min/mo | @ $0.12 | @ $0.18 | @ $0.25 |
|-------------|--------|---------|---------|---------|
| 4 | 300 | $36 | $54 | $75 |
| 8 | 600 | $72 | **$108** | $150 |
| 12 | 900 | $108 | $162 | $225 |
| 20 | 1,500 | $180 | $270 | $375 |

**Insight:** On one gate, AI usage is **noise** next to insurance and your time. You don’t lose the trial on minutes — you lose it on a bad open or a month of free work.

---

## 4. Fixed monthly cost (1 site, trial-scale)

| Line | Low | Base | High | Notes |
|------|-----|------|------|-------|
| Voice platform min / numbers | $50 | $150 | $300 | DID + SIP trunk |
| Agent hosting / logging / dashboard | $50 | $150 | $250 | Simple stack |
| myQ / open path (API, cellular relay backup) | $0 | $100 | $200 | Dealer may already cover panel |
| **Insurance allocation** | $200 | **$400** | $1,000+ | Full GL/E&O for “security” can dwarf this once licensed |
| Incident tools / SMS escalate | $20 | $50 | $100 | Twilio SMS to you |
| Misc | $30 | $50 | $100 | |
| **Fixed total** | **~$350** | **~$900** | **~$1,950** | |

**Base fixed used below: ~$1,000/mo.**

> Once you hold a real Class B + $1M/$2M GL + E&O, insurance may jump to **$1.5k–$4k/mo** even with one client. For a *true* trial under a dealer/partner’s COI, keep the thin $400 — but know that’s temporary.

---

## 5. Soft cost — your time (usually the real P&L)

| Activity | Hours | When |
|----------|-------|------|
| Build voice flow + tools | 20–40 | Week 0 |
| myQ / LiftMaster dealer coordination | 5–15 | Week 0–1 |
| Post orders + guest-list process with CAM | 4–8 | Week 1 |
| Live shadow nights / prompt fixes | 15–30 | Weeks 1–3 |
| Weekly transcript QA | 3–5 / week | Ongoing |
| Board packet / CAM check-in | 2–4 / mo | Ongoing |

| Valuation | |
|-----------|--|
| 50 hrs setup @ $50/hr opportunity | **$2,500** |
| 50 hrs @ $75/hr contractor | **$3,750** |
| 80 hrs “do it right” @ $75 | **$6,000** |

**Ongoing soft:** ~**4–8 hrs/week** first month ≈ **$800–$1,600/mo** if you cost your time; drops to **2–4 hrs/week** after prompts stabilize.

---

## 6. Cash P&L by month (base case)

**Assumptions:** Charge **$4,000**; **8 AI calls/night**; **$0.18/min**; fixed **$1,000**; setup **$3,000** cash-equivalent in Month 0/1.

### Month 0 (build — no revenue)
| | |
|--|--|
| Revenue | $0 |
| AI usage | ~$0–50 (testing) |
| Fixed (partial) | ~$500 |
| Setup | **$3,000** |
| **Cash result** | **−$3,500 to −$3,600** |

### Month 1 (go-live + tuning)
| | |
|--|--|
| Revenue | $4,000 |
| AI usage | ~$110 |
| Fixed | $1,000 |
| Residual setup / dealer | $500 |
| **Cash contribution** | **~$2,400** |
| Cumulative (after M0) | **~−$1,100** |

### Month 2 (stable)
| | |
|--|--|
| Revenue | $4,000 |
| AI + fixed | ~$1,110 |
| **Cash contribution** | **~$2,890** |
| Cumulative | **~+$1,800** |

### Month 3
| | |
|--|--|
| Same run-rate | **~+$2,890** |
| Cumulative | **~+$4,700** |

**Payback of setup:** roughly **end of month 2** on this base case.

---

## 7. Full scenarios (monthly run-rate after setup)

Cash only (no founder time):

| Price | Calls/n | AI $ | Fixed | Cost | **Profit** | Margin |
|-------|---------|------|-------|------|------------|--------|
| $3,500 | 8 | $108 | $1,000 | $1,108 | **$2,392** | 68% |
| **$4,000** | **8** | **$108** | **$1,000** | **$1,108** | **$2,892** | **72%** |
| $4,800 | 8 | $108 | $1,000 | $1,108 | **$3,692** | 77% |
| $4,000 | 20 | $270 | $1,000 | $1,270 | **$2,730** | 68% |
| $0 (free) | 8 | $108 | $1,000 | $1,108 | **−$1,108** | n/a |

**Including soft QA ($1,000/mo of your time):**

| Price | Cash profit | After soft | |
|-------|-------------|------------|--|
| $4,000 | $2,892 | **~$1,892** | Still fine |
| $3,500 | $2,392 | **~$1,392** | OK |
| $2,500 | ~$1,392 | **~$392** | Tight |
| $0 | −$1,108 | **−$2,108** | Pure R&D |

---

## 8. Stress cases (when the trial loses money)

| Stress | Effect | Monthly impact @ $4k price |
|--------|--------|----------------------------|
| Free pilot | No revenue | **−$1.1k** run-rate + setup |
| Insurance jumps to real security quote | Fixed → $2,500 | Profit falls to **~$1.4k** |
| 40 AI calls/night (broken process) | AI ~$540 | Still **~$2.5k** profit — but SLA/reputation dies |
| Cellular failover + dealer truck rolls | One incident | **−$500–$2,000** one-time |
| Wrong admit → claim / board meltdown | Not a P&L line | Can end the company |

**Operational stress > cost stress** on one HOA full AI.

---

## 9. Unit economics in one line

```
Contribution ≈ Price − (calls × 2.5 × 30 × $0.18) − ~$1,000 fixed
            ≈ Price − ~$1,100   (at base volume)
```

So:
- Break-even **cash** price ≈ **$1,100/mo** (ignoring setup & your time)  
- Break-even **with soft QA** ≈ **$2,100/mo**  
- Break-even **with real insurance** ≈ **$2,500–$3,500/mo**  
- Your **$4,000** trial price clears those hurdles with room — if you don’t give it away

---

## 10. Trial success metrics (not just profit)

Track weekly:

| Metric | Target |
|--------|--------|
| Answer &lt; 60s | ≥ 95% |
| AI containment (no human ping) | ≥ 70% |
| False / disputed opens | **0** serious; investigate every open |
| Avg handle time | ≤ 3 min |
| Resident/CAM complaints | Declining by week 3 |
| % entries via code/pass (not AI) | Rising — healthy |

If containment &lt; 50%, you’re paying AI *and* living on-call — switch to hybrid math.

---

## 11. Decision rule for *your* trial

| Choice | Expected 90-day cash | Learn speed | Risk |
|--------|----------------------|-------------|------|
| Free full AI | **−$5k to −$8k** | High | Medium |
| **$4k full AI** | **+$4k to +$7k** after setup | High | Medium–high (opens) |
| $4k hybrid (AI + you approve opens) | **+$2k to +$5k** | Highest trust | Lower |
| Hire humans for 1 HOA | **−$5k to −$10k**/mo | Low | Low product risk |

**Analyst call:** Run the trial at **$3,500–$4,000**, full AI for *talk*, but **you approve opens by SMS for the first 14 nights** (hybrid control, AI cost). Then flip to auto-open only for exact guest-list matches. That keeps the ~$2.5k+/mo cash shape without betting the HOA on untested autonomy.

---

## 12. Bottom line (deep)

On **one HOA, full AI, 8pm–6am**:

1. **AI minutes are ~$50–$300/mo** — not the story.  
2. **~$1,000/mo fixed + setup ~$3k** — the real cash outlay.  
3. At **$4,000** revenue, expect **~$2,500–$3,000/mo cash profit** after month 1.  
4. **Month 0 is a loss**; cumulative turns positive around **month 2**.  
5. Your **time** is the hidden cost (~$1k/mo soft early).  
6. **Insurance and wrong opens** are the existential variables — not Retell’s per-minute fee.

Price the trial so it funds learning. Don’t make the first HOA free unless you explicitly budget **~$5k+ R&D**.
