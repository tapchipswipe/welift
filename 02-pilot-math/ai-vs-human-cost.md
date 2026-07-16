# Cost Compare: AI Voice vs Human Agents (8pm–6am)

**Product:** Overnight virtual gate attendant on LiftMaster / myQ Community  
**Coverage:** 8:00pm–6:00am  
**Pricing basis:** Jul 2026 public voice-AI rates (~$0.10–$0.30/min all-in) + your pilot labor model

---

## 1. Assumptions (illustrative)

| Input | Value | Why |
|-------|-------|-----|
| Sites in pilot | 15 | Mid prove stage |
| Human-needed calls / site / night | **8** | Codes + guest passes take most traffic |
| Avg talk time | **2.5 min** | Verify name/address + decision |
| Minutes / mo | 15 × 8 × 2.5 × 30 = **9,000** | Scales with sites × calls |
| AI all-in rate | **$0.18/min** | Mid of Retell/Vapi/Bland real-world stacks |
| Human loaded wage | **$20/hr** | Wage + burden (your model) |
| Humans online overnight | **3** | For 15 quiet sites (your model) |
| Human shift | 10 hrs × 30 nights | 8pm–6am |

If automation is weak (20+ calls/site/night), AI minutes explode — same as human overload.

---

## 2. Monthly run-rate cost

### A) Humans only (your SOC)

| Line | $/mo |
|------|------|
| 3 agents × $20 × 10 hrs × 30 | 18,000 |
| Float / PTO (~0.5) | 3,000 |
| Light supervisor share | 2,000 |
| Telephony / recording (basic) | 1,500 |
| **Total labor-ish** | **~$24,500** |

Fixed whether 50 or 500 calls/night (until you add agents). Good when call volume is low–moderate.

### B) AI only (voice platform answers + opens)

| Line | $/mo |
|------|------|
| 9,000 min × $0.18 | 1,620 |
| Platform / numbers / logging | 200–500 |
| myQ open webhook / integration hosting | 100–300 |
| **Usage total** | **~$2,000–2,500** |

Looks ~**10× cheaper** on paper — **before** liability backup, QA, and failed opens.

### C) Hybrid (recommended): AI intake + human for grant/deny / edge cases

| Line | $/mo |
|------|------|
| AI handles ~70% of minutes (triage / FAQs / “call resident”) | ~1,200 |
| Human queue for ~30% opens + all ambiguous | 1 agent on call ≈ **6,000–8,000** (or BPO hybrid) |
| Escalation tooling | 200 |
| **Total** | **~$7,500–10,000** |

Still **~60% cheaper** than 3 full overnight humans at 15 sites, with a person accountable for opens.

### Sensitivity (AI-only minutes)

| Calls/site/night | Min/mo (15 sites) | AI @ $0.18/min |
|------------------|-------------------|----------------|
| 4 | 4,500 | ~$810 |
| 8 | 9,000 | ~$1,620 |
| 20 | 22,500 | ~$4,050 |
| 40 | 45,000 | ~$8,100 |

AI stays cheap until volume or long holds spike. Humans stay flat until you hire more.

---

## 3. Time to train / stand up

| Phase | AI voice agent | Human overnight agents |
|-------|----------------|------------------------|
| **First working demo** | **1–3 days** (script + SIP + test open) | **2–4 weeks** (hire, Class D/B, schedule) |
| **One community live** | **3–7 days** after demo (post orders in prompt, guest-list lookup, myQ unlock) | **1–2 weeks** training on that community’s SOPs |
| **Reliable enough for board pilot** | **2–4 weeks** of real-call tuning (false opens, accents, noisy roadside audio) | **1–2 weeks** with shadowing + QA |
| **Each new HOA** | **2–8 hours** (post orders, directory, deny rules) | **2–4 hours** briefing + 1–2 nights shadow |
| **Ongoing** | **2–5 hrs/week** prompt/SOP fixes from transcripts | Shift management, callouts, retraining |

**AI “training” is not model fine-tuning** for you — it’s prompt design, tool hooks (guest list, myQ open), test calls, and weekly transcript review. Budget founder/ops time, not GPU training.

**Hidden AI time cost (month 1):** often **40–80 hours** of your time (or a contractor at $50–100/hr = **$2k–$8k** one-time) to get to “don’t embarrass us on a live gate.”

**Hidden human time cost (month 1):** recruiting + licensing + scheduling often **$3k–$8k** soft cost before first clean week.

---

## 4. Side-by-side verdict

| | Humans | AI-only | Hybrid |
|--|--------|---------|--------|
| Mo cost @ 15 sites | ~$24k | ~$2–3k | ~$8–10k |
| Time to first pilot | Weeks (hiring) | Days | ~1–2 weeks |
| Time to trustworthy opens | Faster judgment | **2–4 weeks tuning** | Faster than AI-only |
| Concurrent gates | Limited by headcount | Scales with $ | Best of both |
| Board / insurance story | Strong (“live attendant”) | Weak if fully autonomous open | Strong if human owns grant |
| Failure mode | Call out / slow night | Wrong admit / loop / hang | Escalate to human |

---

## 5. What to do for *your* product

1. **Don’t buy AI as the whole overnight product** on day one — liability and “AI opened for a stranger” kills trust.  
2. **Do buy AI** to cut minutes: greet, collect name/address, check guest list, tell visitor to use code/pass, warm-transfer edge cases.  
3. Keep **one human** (you or part-time) as open authority until 10+ communities and clean metrics.  
4. Revisit AI-only opens only for **high-confidence** matches (exact guest-list + plate), with human for everything else.

**Rule of thumb:** AI wins on **$/minute and speed to demo**; humans win on **trust and weird edge cases**; hybrid wins on **margin without blowing the board story**.
