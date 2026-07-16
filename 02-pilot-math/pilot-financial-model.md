# Pilot Financial & Staffing Model (10–20 Communities)

**Market:** Sarasota–Bradenton–Lakewood Ranch (941 / 34211)  
**Beachhead product:** Overnight virtual gate **8:00pm–6:00am** (10 hrs)  
**Outside coverage:** On-site guard and/or keypad codes stay with the community  
**Run the calculator:** `python3 staffing_model.py`

---

## Why 8pm–6am

| Window | Traffic | Ops reality |
|--------|---------|-------------|
| Before 8pm | Evening guests / dinners | Community booth or codes — **not your shift** |
| 8pm–6am | Sparse overnight | Easy multiplex; core product |
| After 6am | School / work rush | Community booth or codes — **not your shift** |

**Board pitch:** Cut the low-utilization overnight booth; keep evening/morning presence if residents want it. Easier SLA than 5pm–9am because you skip both rush windows.

---

## 1. Pricing assumptions (SWFL)

| Line | Value | Notes |
|------|-------|-------|
| HOA bill rate for on-site unarmed gate | $30/hr | Mid of FL ~$25–$40 range |
| Your coverage hours / day | **10** | 8pm–6am |
| Days / year | 365 | Full year |
| Status-quo cost for those 10 hrs | **$109,500/yr** (**~$9,125/mo**) | 10 × 365 × $30 |
| Your 8pm–6am virtual price | **$4,800/mo** | ~47% savings vs status quo |
| Upsell to 5pm–9am or 24/7 later | $7,500+ / $9,000+ | After density + automation |
| Hardware (HOA CapEx, not your P&L) | $8,000–$20,000 / entrance | Partner-installed |

---

## 2. Revenue scenarios

| Communities | Monthly revenue @ $4,800 | ARR |
|-------------|--------------------------|-----|
| 10 | $48,000 | $576,000 |
| 15 | $72,000 | $864,000 |
| 20 | $96,000 | $1,152,000 |
| 50 (scale) | $240,000 | $2,880,000 |
| 100 (stretch) | $480,000 | $5,760,000 |

---

## 3. Cost structure — 15-community 8pm–6am pilot

Overnight is mostly quiet — staffing is simpler than evening/morning coverage.

### Labor (illustrative)

| Role | Count | Loaded cost / mo | Notes |
|------|-------|------------------|-------|
| Overnight agents | 3 | $18,000 | ~$20/hr loaded × 10 hrs × 30 × 3 |
| Float / PTO | 0.5 FTE equiv | $3,000 | Part-time 4th / OT |
| Supervisor (shared) | 0.25 | $2,000 | Founder / lead |
| **Labor subtotal** | | **~$23,000** | |

3 agents can cover many quiet gates if answer SLA is 30–60s and codes/guest lists handle routine entry.

### Other monthly OpEx (15 sites)

| Item | $/mo |
|------|------|
| Software / telephony / recording | 1,500 |
| Internet / SOC workspace | 800 |
| Insurance (GL + E&O + WC allocated) | 2,500 |
| Sales / CAM relationship | 2,000 |
| Misc / QA | 700 |
| **OpEx subtotal** | **~$7,500** |

### P&L summary @ 15 communities

| | Monthly |
|--|---------|
| Revenue | $72,000 |
| Labor | ~(23,000) |
| Other OpEx | ~(7,500) |
| **Contribution** | **~$41,500** (~58% margin) |

---

## 4. Peak concurrency

See `staffing_model.py`. For **8pm–6am**, design for quiet multiplex — not AM/PM rush.

If you later expand into 5–8pm or 6–9am, re-run peak scenarios; those windows need more agents or stronger automation.

---

## 5. Recommended pilot plan

| Phase | Sites | Product | Price target | Overnight agents |
|-------|-------|---------|--------------|------------------|
| Pilot | 3–5 | 8pm–6am | $4,800/mo | 2 |
| Prove | 10–15 | 8pm–6am + board reports | $4,800/mo | 3 |
| Expand | 20–30 | Same | $4,500–$5,200 | 3–4 |
| Upsell | Select sites | Extend to 5pm–9am | $7,500 | Peak overlay |

**Hybrid site rule:** Keypad/codes stay live 24/7; booth covers before 8pm / after 6am as the board chooses; your attendants own the intercom **8pm–6am**.

---

## 6. Files

- `pilot-model.csv` — tabular assumptions  
- `staffing_model.py` — concurrency & P&L calculator (defaults to 8pm–6am)
