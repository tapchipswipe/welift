# Pricing & Insurance Deep Dive — Your Three Ideas

You floated three connected thoughts:

1. Maybe we don’t need our own insurance because the HOA already insures the gate  
2. Charge **per minute** with a **60–75% margin** so it feels fair / cheaper to try  
3. Sell as a **monthly subscription**, with a **cheaper annual** option  

Below is how those ideas work in the real HOA / myQ / overnight-AI world — and a concrete packaging model that keeps the spirit of what you want without blowing board budgets or your liability.

---

## Thought 1 — “Does the HOA’s gate insurance cover us?”

### Short answer
**No. You still need your own insurance** (and likely Florida Class B-related GL) if *you* answer calls and cause the gate to open.

### Why people get confused
| What the HOA has | What it actually covers |
|------------------|-------------------------|
| Master / property / liability policy | Association’s premises, common areas, *their* negligence, sometimes gate equipment damage |
| Directors & officers | Board decisions |
| Maybe “security” endorsement | Often narrow; rarely covers a third-party vendor’s access decisions |

| What *you* do | Who gets sued if it goes wrong |
|---------------|--------------------------------|
| AI/human verifies visitor | You + possibly HOA |
| You trigger myQ / relay open | You (wrongful admit / negligent verification) |
| Call recording / PII | You (privacy / cyber) |
| Agent or AI script error | You (E&O / professional liability) |

HOA carriers and CAMs almost always require **vendors** to bring:

- Their own **GL** ($1M/$2M typical)  
- Often **E&O / professional liability** for security-like work  
- **HOA + management company as additional insured**  
- COI on file before go-live  

Being “covered by the HOA’s policy” is backwards: **they want to be additional insured on *your* policy**, not the other way around.

### Edge case that *doesn’t* remove your need
Even if the HOA’s policy somehow responds to a gate incident, the carrier can still **subrogate against you** (chase you for what they paid). Without your own insurance + contract limits, you personally eat that.

### Practical trial approach
| Stage | Insurance stance |
|-------|------------------|
| Internal sandbox / fake calls | Maybe none yet |
| Live opens on a real gate | **Own GL + E&O bound** — non-negotiable |
| Partner under a licensed security firm’s COI | Possible short-term (they’re the named vendor; you subcontract) — still not “HOA insurance covers us” |

**Bottom line:** Gate insurance ≠ attendant insurance. Budget your own coverage as cost of goods, not optional.

---

## Thought 2 — “Charge per minute at 60–75% margin”

### What you’re optimizing for
- Feels **fair** (“quiet nights = cheap”)  
- Easy to **start** (low commitment vs $4k flat)  
- Aligns your **AI cost** with revenue  
- Sounds more “tech SaaS” than “security contract”

That instinct is good for **your** unit economics. It’s awkward for **HOA buying psychology**.

### How HOAs budget
Boards and CAMs live on **annual budgets** approved once a year. They hate:

- Unpredictable invoices  
- “We blew the security line because December had parties”  
- Usage bills that need explanation at every meeting  

Flat landscaping / management / Envera-style **monthly retainers** win because the treasurer can write **one number** into the budget.

Pure per-minute = utility bill. Utilities are tolerated; **optional security vendors** that spike are the first cut.

### Margin math (your idea, made concrete)

Assume AI all-in cost **$0.18/min**.

| Target margin | Price / min | Markup |
|---------------|-------------|--------|
| 60% | **$0.45** | 2.5× |
| 67% | **$0.54** | 3× |
| 75% | **$0.72** | 4× |

**Example month (1 HOA, 8 calls/night × 2.5 min × 30 = 600 min):**

| Price/min | Revenue | AI cost | Gross profit | Margin |
|-----------|---------|---------|--------------|--------|
| $0.45 | $270 | $108 | $162 | 60% |
| $0.54 | $324 | $108 | $216 | 67% |
| $0.72 | $432 | $108 | $324 | 75% |

**Problem:** At “enticing” pure usage, you only collect **$270–$430/mo** — but you still need:

- Insurance (~$400–$2,000+)  
- Platform / numbers (~$150–$300)  
- Your on-call / QA time  
- Setup amortized  

So **60–75% margin on minutes ≠ 60–75% margin on the business**. You can be “high margin on AI” and still **lose money every month** after fixed costs.

### When pure per-minute *does* work
- Add-on overage after a base fee  
- Resident-paid guest calls (rare politically)  
- Internal cost tracking, not the customer invoice  

### Better expression of your idea
**Don’t sell naked per-minute. Sell a subscription that *includes* minutes, with overage at your margin.**

That keeps:

- Predictable board budget (subscription)  
- Your 60–75% margin on usage (included pool sized so you win)  
- “Enticing” entry if the base is lower than flat $4,800  

---

## Thought 3 — “Monthly subscription + cheaper annual”

This maps cleanly to how HOAs already buy (and how Envera-ish contracts work).

| Plan | Board likes | You like |
|------|-------------|----------|
| **Monthly** | Easy to start / cancel after trial | Higher price, churn risk |
| **Annual (prepaid or 12-mo commit)** | Locks budget for the fiscal year; often 1–2 months “free” feel | Cash upfront, lower churn, sales cycle fits budget season |

Typical SaaS-style discount: **annual = ~2 months free** (~16.7% off), or **10–15% off**.

For HOAs, annual often isn’t “credit card SaaS” — it’s **invoice net-30, paid from operating budget**, sometimes quarterly. Offer:

- Monthly  
- Annual (best rate)  
- Optional: quarterly  

---

## Recommended packaging (combines all three thoughts)

### Product name framing
**“Overnight Gate Attendant — AI-Assisted”**  
8pm–6am · works with existing LiftMaster / myQ  

### Plan structure

#### A) Starter (trial / small quiet gate)
| | |
|--|--|
| Monthly | **$1,490**/mo |
| Annual | **$14,900**/yr (~**$1,242**/mo effective, ~2 months free) |
| Includes | **800 talk-minutes**/mo (~10–11 hrs) |
| Overage | **$0.55**/min (~67% margin vs $0.18 cost) |
| Soft cap | Alert CAM at 80% of pool |

**Why enticing:** Far below $4,800 and below night-guard ~$9k; still covers quiet AI usage + contributes to fixed costs.

#### B) Standard (your default list)
| | |
|--|--|
| Monthly | **$2,990**/mo |
| Annual | **$29,900**/yr (~**$2,492**/mo) |
| Includes | **2,000 minutes**/mo |
| Overage | **$0.55**/min |
| Positioning | Most 150–400 home gates overnight |

#### C) Plus (busier / multi-lane / less automation)
| | |
|--|--|
| Monthly | **$4,490**/mo |
| Annual | **$44,900**/yr (~**$3,742**/mo) |
| Includes | **4,000 minutes**/mo |
| Overage | **$0.50**/min (slight volume break) |

### Why this matches your instincts

| Your thought | How it’s honored |
|--------------|------------------|
| Per-minute fairness | Unused capacity isn’t infinite — overage only if they’re noisy; quiet HOAs stay on cheaper tier |
| 60–75% margin on minutes | Overage at $0.55 on $0.18 cost ≈ **67%**; included minutes priced into sub so blended margin stays healthy |
| Monthly + cheaper annual | Explicit annual discount |
| Enticing vs $4,800 flat | Starter/Standard undercut “scary” flat security quotes |
| Insurance reality | Subscription revenue must clear **insurance + platform** — don’t rely on HOA’s policy |

### Blended margin check (Standard, base volume)

Assume 600 min used of 2,000 included; price $2,990:

| | |
|--|--|
| Revenue | $2,990 |
| AI cost | 600 × $0.18 = $108 |
| Fixed (platform + thin insurance) | ~$1,000 |
| **Contribution** | ~**$1,880** |
| “Minute margin” if you only counted AI | Looks huge |
| Real contribution margin | ~**63%** after fixed — still solid on 1 HOA |

If they burn 2,500 min (500 overage):

| | |
|--|--|
| Revenue | $2,990 + 500×$0.55 = **$3,265** |
| AI cost | 2,500×$0.18 = $450 |
| After fixed $1k | Contribution ~**$1,815** |

Overage protects you when the HOA is chaotic.

---

## What I’d *not* do

1. **Pure per-minute only** — boards won’t budget it; you’ll under-collect vs insurance.  
2. **Assume HOA insurance covers attendant decisions** — CAM will still demand your COI.  
3. **75% margin on minutes as the whole business model** — fixed costs dominate at 1–5 HOAs.  
4. **Annual prepaid without cancellation/SLA terms** — if AI fails week 2, you need a pro-rata exit to stay trustworthy.

---

## Contract one-liners that make this sellable

- “**Predictable subscription** for overnight coverage; minutes included so quiet nights aren’t punished.”  
- “If traffic spikes (parties, holidays), overage is **$0.55/min** — still far below a guard hour.”  
- “Annual plan locks your rate for the budget year.”  
- “We carry our own liability insurance and name the Association additional insured — industry standard for access vendors.”

---

## Decision summary

| Question | Verdict |
|----------|---------|
| Skip our insurance because HOA has gate coverage? | **No** — you need your own; they need to be on *your* COI |
| Pure per-minute @ 60–75% margin? | **Good for overage / unit economics; bad as the only price** |
| Monthly + cheaper annual? | **Yes — do this** |
| Best synthesis | **Tiered monthly/annual subscription with included minutes + margined overage** |

That’s the realm of your thought: **usage-fair economics wrapped in budget-friendly subscription packaging**, with insurance treated as *your* cost of being a real vendor — not something the HOA’s gate policy replaces.
