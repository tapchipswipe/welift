# Pre-CAM Playbook — The Inlets Pilot

Actionable guidance when **no CAM relationship exists yet**. Source: Lucas status update, July 2026.

**Locked elsewhere:** [decision-log.md](decision-log.md) · **After CAM replies:** [cam-kickoff-email.md](cam-kickoff-email.md) · **Math:** [02-pilot-math/](../../02-pilot-math/)

---

## A) Reality check — August with no CAM yet

### Honest assessment

**August 15 live overnight at The Inlets is unlikely** from today's starting point (no CAM, unknown dealer, unknown myQ admin, no LLC/insurance). The original critical path assumed CAM kickoff **Jul 16** and a 3-way dealer call by **Jul 25**. Each week without CAM contact pushes live routing ~1–2 weeks.

| Milestone | Original date | Earliest if CAM starts **this week** | Blocker |
|-----------|---------------|--------------------------------------|---------|
| CAM identified + first reply | Jul 16 | Jul 18–25 | No outreach sent yet |
| Dealer of record + post orders draft | Jul 25 | Aug 1–8 | Needs CAM |
| Dealer programs 8pm–6am → Retell DID | Aug 1 | Aug 8–15 | Needs dealer + tested DID |
| On-site pedestal test + shadow nights | Aug 1–8 | Aug 15–22 | Needs CAM + dealer |
| **First live overnight** | Aug 15 | **Aug 29 – Sep 12** | All above |

**What must happen by when (minimum for *any* August activity at The Inlets):**

| By | Must happen |
|----|-------------|
| **Jul 18** | Identify who manages The Inlets (CAM firm + named manager). Send info-gathering outreach — not full pitch. |
| **Jul 25** | CAM replies OR pivot to alternate HOA from [03-channel-test/target-cam-firms.md](../../03-channel-test/target-cam-firms.md). |
| **Aug 1** | Retell + webhook + Twilio **done** (§D). Retell demo call recordable for CAM. |
| **Aug 8** | Written CAM OK for shadow/test opens + dealer contact in hand. |
| **Aug 15** | Realistic target: **shadow nights only** (Lucas on cell, not pedestal) if CAM still cold. |
| **Aug 29** | Realistic target: **first pedestal live overnight** if CAM + dealer cooperated in July. |

**August can still "work"** if you redefine success: **technical proof + CAM conversation started**, not paid production. Treat Aug 1–31 as **pre-CAM build + shadow** unless CAM engages before Jul 25.

---

## B) How to get a CAM relationship from zero

### Step 1 — Identify who manages The Inlets

Work in parallel; first confirmed source wins.

| Method | What to look for | Action |
|--------|------------------|--------|
| **County property records** | Manatee / Sarasota appraiser — HOA name, registered agent | Sunbiz / county recorder for registered agent → often management co |
| **Sunbiz** | "The Inlets" HOA entity; registered agent address | Cross-reference agent to CAM firm |
| **Visit the gate (daytime)** | Management sticker, guard booth packet, newsletter QR | Photo pedestal label; ask guard "who does the HOA use for management?" |
| **myQ tablet / directory** | Sometimes lists management company on screen | Note CAP model while there |
| **Board filings** | Annual report, budget PDF on HOA website | Management company letterhead |
| **LinkedIn** | `"The Inlets" HOA` + `community association manager` + `Bradenton` / `Lakewood Ranch` | Find named CAM; connect before cold email |
| **Neighbor apps / Nextdoor** | "Who is our management company?" | Confirm with second source |

**Deliverable:** CAM company name, manager name, email/phone, confidence level (confirmed vs guess).

### Step 2 — Outreach sequence (info gathering before sales)

**Goal of first touch:** get the six facts from [cam-kickoff-email.md](cam-kickoff-email.md) — **not** sign a contract.

| Touch | Channel | Tone | Ask |
|-------|---------|------|-----|
| **1** | Email or LinkedIn | Curious local operator | "Who manages The Inlets?" + "Who is your LiftMaster dealer?" — 5 sentences max |
| **2** (48h) | Phone or SMS | Same | Reference email; offer 15 min **info** call |
| **3** (1 week) | Email | Slightly more product | Attach 60-sec Retell demo recording (see below); still ask for dealer + post orders |
| **4** | Formal kickoff | Full [cam-kickoff-email.md](cam-kickoff-email.md) | Only after you know their name and they haven't ghosted |

**Do not** mention pricing, LLC, or Class B on touch 1. **Do** say you're local, building overnight exception coverage for myQ communities, and need dealer coordination facts.

### Step 3 — What to build before first CAM meeting

No myQ routing required yet.

| Asset | Done when | Use in meeting |
|-------|-----------|----------------|
| **Retell demo call** | You call your own DID; full verify → approve → (mock) open | Screen-share or send recording |
| **Mock flow doc** | 1-page: visitor taps Call Attendant → voice verify → open/deny | Shows you understand their tablet |
| **Post orders draft (yours)** | Default deny/escalate matrix (§F) | "Here's what we'd follow — what would you change?" |
| **Shadow log sample** | 3 fake `events.jsonl` entries | Shows audit trail |

**First meeting agenda (30 min):** their gate reality → your demo → what you need from dealer → shadow timeline → **no signature**.

### Step 4 — If The Inlets CAM is cold

Do not wait more than **2 weeks** on one HOA. Parallel path:

| # | Firm | Why | Contact |
|---|------|-----|---------|
| 1 | Gulf Coast Association Management | Same ZIP 34211 | (941) 213-4801 · gulfcoastam.com |
| 2 | AMI — Advanced Management of SW Florida | 100+ associations | (941) 359-1134 · info@amiwra.com |
| 3 | FirstService Residential — Sarasota | LWR communities | fsresidential.com/florida |
| 4 | Keys-Caldwell | Gated SF along I-75 | (941) 408-8293 |
| 5 | Empire Management Group | Sarasota / LWR since 1993 | empirehoa.com |

**Pitch:** "We're piloting overnight voice attendant for myQ gates — looking for one SWFL community with LiftMaster already installed." The Inlets remains preferred if they warm up later.

---

## C) Pay-by-usage pricing model

Lucas's idea: **usage-based**, not flat monthly yet. Align with [02-pilot-math/pricing-insurance-subscription-deep-dive.md](../../02-pilot-math/pricing-insurance-subscription-deep-dive.md) and [one-hoa-full-ai-trial-deep-dive.md](../../02-pilot-math/one-hoa-full-ai-trial-deep-dive.md).

### Why not naked per-minute for CAM

Boards budget **monthly retainers**. Pure per-minute feels like a utility bill and often under-collects vs insurance + on-call time. **Hybrid usage** keeps fairness without breaking pilot math.

### Recommended structure (overnight 8pm–6am)

| Component | Pilot range (TBD — quote in band) | Rationale |
|-----------|-----------------------------------|-----------|
| **Nightly coverage minimum** | **$75–$99 / night** on duty | Covers platform, on-call standby, Retell DID — ~$1,650–$2,970/mo at 30 nights |
| **Included handled calls** | **60 / mo** in minimum | ~2/night quiet gate; matches base-case volume |
| **Per additional AI-handled call** | **$10–$15** | After included pool; 2.5 min avg @ $0.18 AI ≈ $0.45 cost → healthy margin |
| **Per approved open** (SMS bridge) | **$15–$22** | Prices Lucas tap-to-unlock labor; optional line if bundled into call fee |
| **Overage talk time** | **$0.50–$0.55 / min** after 3 min/call | Protects long arguments / language barriers |
| **Hard monthly floor** | **≥ $995 effective** | Never below fixed-cost floor (~$900/mo in pilot math) |
| **Target effective (paid pilot)** | **$2,500–$4,000 / mo** | Matches friends/trial tiers; still ~55% below ~$9k guard anchor |

**Do not quote below $995/mo effective** — you lose money on insurance + time even if AI minutes are cheap.

### Example invoice (CAM conversation — busy month)

```
We Lift — The Inlets — Overnight Attendant — September 2026 (usage)
────────────────────────────────────────────────────────────────────
Nightly coverage (30 nights × $89)                         $2,670
AI-handled calls (186 total; 60 included, 126 × $12)     $1,512
Approved opens (94 × $18)                                  $1,692
Overage talk time (41 min × $0.55)                            $23
Platform / SMS pass-through                                 $48
────────────────────────────────────────────────────────────────────
TOTAL                                                    $5,945
Effective vs on-site guard (~$9,125/mo for 10 hrs):       ~35% savings
```

### Example invoice (quiet month)

```
Nightly coverage (30 × $89)                              $2,670
AI-handled calls (72 total; 12 over included × $12)          $144
Approved opens (28 × $18)                                  $504
────────────────────────────────────────────────────────────────────
TOTAL                                                    $3,318
```

Both land in **trial band ($2.5k–$4k)** on quiet months and **approach list ($4.8k)** when the gate is busy — usage-fair without undercutting [pilot-financial-model.md](../../02-pilot-math/pilot-financial-model.md).

### CAM one-liner

> "Predictable **nightly minimum** so we're always on; you only pay extra when visitors actually need us. Quiet months stay ~$3k; busy months still beat an overnight guard."

**Price:** mark **TBD** in proposals until post-shadow volume data; show **ranges above** in first CAM meeting only if they ask.

---

## D) Pre-CAM technical stack order

**Do not wait for CAM to finish tech.** Dealer routing is last.

```
Retell agent + prompt
    → webhook deploy (HTTPS, not ngrok-only)
        → Twilio SMS live
            → cell / mock §5 tests
                → THEN dealer + CAM (DID handoff)
```

### Priority checklist

| # | Task | Done looks like | Owner |
|---|------|-----------------|-------|
| 1 | Retell LLM + tools wired | Demo call: verify → check_guest_list → approve/deny/escalate | Lucas |
| 2 | Webhook on **stable HTTPS** | Public URL in Retell; `events.jsonl` logging | Lucas |
| 3 | Twilio | `ONCALL_PHONE` receives real SMS on open/escalate ([on-call-sms-sla.md](on-call-sms-sla.md)) | Lucas |
| 4 | §5 cell tests | All paths pass per [setup-checklist.md](../../setup-checklist.md) | Lucas |
| 5 | myQ API email | Sent to integrations@myq.com — non-blocking for Aug | Lucas |
| 6 | **Dealer/CAM** | 3-way call; 8pm–6am → Retell DID | CAM + dealer |

### Twilio setup (minimal)

1. Create Twilio account; buy one US local number (941 if available).
2. In `webhook/.env`: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `ONCALL_PHONE` (E.164).
3. Send test SMS from webhook `open_gate` / `escalate_to_oncall` — **must hit Lucas's phone**, not logs only.
4. Budget ~$15–30/mo for pilot SMS volume.

### "Done" before CAM pitch

- [ ] 3 recorded demo calls (approve, deny, escalate) you can email
- [ ] Webhook uptime on stable host (Railway/Fly/Vercel — not daily ngrok URL)
- [ ] Twilio SMS proven end-to-end
- [ ] `data/guest-list.json` loaded; CAM **or Lucas** can edit nightly (§F maintenance)
- [ ] Retell DID ready to give dealer — **but don't share until CAM meeting scheduled**

---

## E) Legal / compliance — IDEA stage (no LLC yet)

See [compliance-path.md](compliance-path.md) and [04-risk-setup/](../../04-risk-setup/).

### Safe now (no LLC)

| Activity | OK? |
|----------|-----|
| Retell demo calls to your own phone | Yes |
| Internal docs, mockups, pilot math | Yes |
| Insurance **quote** requests (use personal name + "forming FL LLC") | Yes |
| FDACS / Class B **research** calls | Yes |
| CAM **info-gathering** emails (no contract) | Yes |
| Shadow calls on **your cell** with fake community name | Yes |

### Requires LLC (or subcontract partner) first

| Activity | Why |
|----------|-----|
| Signed service agreement / LOE with fee | Contract party must be entity |
| Bound GL + E&O | Carriers need Sunbiz entity |
| COI naming Association | Issued to LLC |
| myQ SOC user in **production vendor name** | Account tied to business entity |
| Paid pilot invoice | Tax / liability |

### Cheapest / fastest order

1. **Sunbiz LLC** (~$125) — 1–3 business days online
2. **EIN** (IRS, free, same day)
3. **Insurance quotes** to ≥2 brokers ([insurance-quote-packet.md](../../04-risk-setup/insurance-quote-packet.md))
4. **FDACS call** — Class B required? subcontract path?
5. **Class B** — apply OR sign subcontract under licensed agency ([florida-class-b-checklist.md](../../04-risk-setup/florida-class-b-checklist.md))

### Soft pilot without LLC — risks and mitigations

| Risk | Mitigation |
|------|------------|
| Personal liability on wrong admit | **Shadow only** until LLC + CAM written OK; no production opens in We Lift name |
| CAM won't engage without COI | Offer **technical demo only**; defer live gate until entity + quotes in flight |
| Class B gray area | CAM owns access decision; you're "technology demo"; document in writing |
| Can't sign dealer work orders | CAM or dealer programs routing; no vendor contract from Lucas personally |

**Paid August at The Inlets without LLC + insurance: not recommended.** Free/shadow with CAM email OK is the ceiling.

---

## F) Product edge cases — recommended post-order DEFAULTS

Give CAM a draft; they edit. Encode in `prompt.md` + guest-list process.

| Scenario | Default | Escalate? |
|----------|---------|-----------|
| **Unknown visitor claiming resident** | Deny open. Require full visitor name + host full name + unit. Must match guest list **or** active myQ pass (visitor confirms they have one — you don't issue). No match → deny + "host must send myQ guest pass." | Escalate if visitor insists host is "expecting them" and names match partially (fuzzy) |
| **Delivery after hours** | Deny unless on tonight's vendor/delivery list **or** post orders name approved carriers (UPS/FedEx/Amazon). No list entry → deny; instruct to return during delivery window or leave at guard if community allows | Escalate for medical delivery (pharmacy) — Lucas callback |
| **Vendor without pass** | Deny. Vendor must be on CAM-maintained vendor list with company name match. Pool/lawn/pest: require scheduled window in list if post orders say so | Escalate if vendor claims emergency repair (water leak) — Lucas verifies with CAM on-call |
| **Emergency claims** ("heart attack", "fire") | **Do not open.** Tell caller to dial **911**. Do not dispatch via this line. Log call. | Auto-escalate SMS to Lucas for awareness only — no open without normal verify |
| **Resident locked out** | **Not your user.** Direct to myQ app, resident code, or call CAM daytime line. Deny gate open for "I'm a resident" without guest-list entry | N/A |
| **Forgot code / host not answering** | Deny codes. Suggest retry pass/code. If on guest list → approve. Else deny | Escalate after 2 failed verify attempts if visitor calm |
| **CAM / ops calling** | Message + escalate. No open unless post orders name them | Lucas callback |
| **Spam / marketing** | End call | No |

### Deny vs escalate matrix

| Signal | Action |
|--------|--------|
| Clear deny rule (not on list, no pass, resident self-serve) | **Deny** — no SMS |
| Partial name match, angry visitor, equipment fault, open_gate failure | **Escalate** → SMS Lucas |
| 911 / medical / fire language | **Deny open** + 911 instruction + escalate SMS (awareness) |
| High-confidence guest-list match | **Approve** → open_gate → SMS |

**Guest list maintenance:** CAM **or Lucas** — either can edit `data/guest-list.json` nightly; document who edited in log notes.

---

## G) August scope recommendation

### Shadow vs paid (current state)

| Mode | Recommend? | Why |
|------|------------|-----|
| **Shadow / technical pilot** | **Yes — default for August** | No CAM, no LLC, no insurance, Twilio not started |
| **Paid pilot** | **No for August** | Needs entity + bound COI + signed agreement ([compliance-path.md](compliance-path.md)) |
| **Cell-only simulation** | OK **parallel** to CAM hunt | Proves Retell; does **not** satisfy Q4 (real myQ tablet) — disclose to CAM |

**August success definition (measurable):**

| Metric | Target |
|--------|--------|
| CAM identified + 1 substantive conversation | 1 CAM firm engaged |
| Retell + webhook + Twilio production-ready | §5 tests pass; stable HTTPS |
| Demo asset | 3 recorded call scenarios shareable |
| Shadow nights (cell or pedestal) | ≥ 5 nights logged in `events.jsonl` |
| Wrong-admit incidents | **0** on any real gate |
| Dealer contact obtained | Name + phone from CAM |
| Post orders draft | CAM redlined or Lucas defaults accepted for shadow |
| Paid contract signed | **Not required for August success** |

If CAM + dealer cooperate by **Aug 22**: add **≥ 3 pedestal shadow nights** before first live overnight (target **Sep 1**, not Aug 15).

---

## H) Remaining unknowns — decide next (prioritized)

| # | Decision | Options | Recommend by |
|---|----------|---------|--------------|
| **1** | **Send first CAM outreach this week?** | The Inlets only vs parallel 2 firms from metro list | **Jul 17** — delay kills August pedestal |
| **2** | **August success = shadow or live?** | Redefine to shadow + CAM demo **or** hold Aug 15 and risk missing | **Jul 18** — pick shadow default |
| **3** | **Form FL LLC now?** | Sunbiz this week vs wait until CAM bites | **Jul 21** — needed before any paid path; ~$125 |
| **4** | **Usage pricing bands for first CAM quote** | Use §C ranges vs "TBD after shadow" | **First CAM meeting** — show ranges, don't commit |
| **5** | **The Inlets vs alternate HOA if cold 2 weeks** | Stay vs pivot pilot to AMI/Gulf Coast client | **Aug 1** — hard pivot deadline |

---

## Quick weekly rhythm (pre-CAM)

| Day | Focus |
|-----|-------|
| Mon–Tue | Tech: Retell → webhook deploy → Twilio |
| Wed | CAM identification + first outreach |
| Thu | Record demo calls; update guest-list defaults |
| Fri | Insurance quote packet prep; Sunbiz if GO on LLC |
| Weekend | 1–2 shadow test calls on cell; log review |

**When CAM replies:** switch to [README.md](README.md) critical path and [cam-kickoff-email.md](cam-kickoff-email.md) § After CAM replies.
