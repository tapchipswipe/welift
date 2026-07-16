# Decision Log — Lucas / We Lift

Locked product and pilot decisions. Update only by explicit owner change.

**Last updated:** July 16, 2026 (idea refined — vendor Call Attendant)  
**Pilot:** The Inlets · **Thesis:** [PRODUCT.md](../PRODUCT.md) · **This week:** [THIS-WEEK.md](THIS-WEEK.md)

**Refined idea in one line:** Autonomous Call Attendant for authorized vendors/workers who lack resident codes/stickers — not a virtual overnight guard.

---

## Q1 — Autonomous verify + open

**Decision:** **Fully autonomous.** AI verifies the visitor and opens the gate. **No overnight human attendant. No 2am SMS wake.**

| Layer | Choice |
|-------|--------|
| Verification | Retell voice agent + guest list / post orders |
| Open | **myQ Partner API remote unlock only** |
| Ambiguous / no match | **Deny** + log for daytime review (not escalate to a waking human) |
| Human SMS bridge | **Rejected** as product path (legacy flag `HUMAN_SMS_FALLBACK` off) |

**Implication:** Sell access-control automation. **myQ Partner API is the critical path** — without it, live autonomous opens cannot ship. Use `SIMULATE_MYQ_OPEN=true` only for voice demos.

---

## Q2 — Voice vs video

**Decision:** **Voice-only** for verification (Retell).

| Topic | Choice |
|-------|--------|
| Grant/deny input | Voice only — name, host, purpose |
| Video | Optional **later** — security/audit retention only; **not** an input to `check_guest_list` or `open_gate` |

---

## Q3 — Smith.ai

**Decision:** **Fully dropped.** Retell only.

Historical Smith docs in repo are comparison/archive only ([03-channel-test/smith-ai-setup-checklist.md](../../03-channel-test/smith-ai-setup-checklist.md)).

---

## Q4 — Pilot scope

**Decision:** **One HOA**, real **myQ tablet** at the physical gate — not cell-only simulation.

Bar for success: pedestal audio, routing, unlock, logging on live hardware.

---

## Q5 — Pilot HOA

**Decision:** **The Inlets** (SWFL, LiftMaster myQ Community).

---

## Q6 — Guest list / credentials

**Decision:** Normal gate access stays as today. **AI is a low-volume exception path for non-residents.**

| Path | Who | How they enter |
|------|-----|----------------|
| **Primary — residents** | Homeowners / tenants | **Keypad code** or **RFID sticker / transponder** (unchanged) |
| **Primary — invited guests** | Social visitors | **myQ guest pass** or host-provided code (preferred) |
| **AI Call Attendant** | **Non-residents without code/sticker** — mainly **gardeners, lawn/pool/pest, contractors, workers** | Voice verify against CAM vendor / exception list → autonomous myQ unlock |

| Who maintains list | Model |
|---------------------|--------|
| Residents | Codes, stickers, myQ guest passes |
| CAM / board | Vendor / worker authorization list + post orders |
| We Lift | Hosts `guest-list.json` (vendor-first) for the AI — not a resident directory |

**Volume expectation:** Call Attendant used **rarely** (any hour of coverage). Product math should assume low concurrency, not a busy guard booth.

**Note:** “CAM” = Community Association Manager.

---

## Q7 — Primary AI audience (Lucas — Jul 16, 2026)

**Decision:** Target users of the AI are **vendors and workers** (e.g. gardeners) who do not have resident credentials — **not** residents and not the default path for social guests.

---

## Additional locked decisions

| Topic | Decision |
|-------|----------|
| **Brand** | **We Lift** (repo: [welift](https://github.com/tapchipswipe/welift)) |
| **Coverage window** | 8:00pm–6:00am Eastern (pilot hours; exception path stays low-volume anytime) |
| **Users of AI** | **Non-resident exceptions at pedestal** — vendors/workers first |
| **Residents** | Keypad + sticker only — AI must redirect, never open as resident unlock |
| **Overnight human** | **None** — autonomous; daytime log review only |
| **Repo** | Single monorepo `welift` |
| **Target month** | **August 2026** first live overnight |

---

## Site & relationships (Lucas — Jul 15–16, 2026)

| Item | Status |
|------|--------|
| **Likely community** | **The Inlets at Riverdale** (Bradenton 34208) — not Nokomis condo. Confirm on first call. |
| **CAM relationship** | **None yet** — no formal agreement |
| **CAM lead (unverified)** | **Associa Gulf Coast** — Sarasota (941) 552-1598; MLS-cited manager. See [cam-identification.md](cam-identification.md) |
| **LiftMaster dealer of record** | **Unknown** — ask CAM |
| **myQ admin** | **Unknown** |
| **Facility details** (CAP model, Phone.com, current after-hours routing) | **Unknown** — daytime gate photo recommended |

---

## Commercial (Lucas — Jul 15, 2026)

| Item | Status |
|------|--------|
| **Pricing model** | **Pay by usage** — Lucas's idea; flat monthly not chosen yet |
| **Price** | **TBD** — see usage bands in [pre-cam-playbook.md](pre-cam-playbook.md) §C |
| **Contract** | **Unknown** — no agreement path yet |

---

## Legal (Lucas — Jul 15, 2026)

| Item | Status |
|------|--------|
| **FL LLC** | **Not formed yet** |
| **Class B license** | **None** |
| **Insurance** | **None bound** — quote packet not sent |

---

## Technical (Lucas — Jul 15–16, 2026)

| Item | Status |
|------|--------|
| **Product mode** | **Autonomous** — AI decide + myQ unlock; deny when unsure |
| **Retell** | Prompt/configs updated for autonomous; needs live DID + §5 |
| **Webhook** | **v0.4 autonomous** — no SMS wake by default |
| **Twilio** | **Not required** (deprecated SMS path) |
| **myQ Partner API** | **Critical blocker** for live opens — apply Week 0 |
| **Exceptions guest list** | CAM or Lucas edits nightly; high-confidence matches only auto-open |

---

## Open items (not locked)

- Confirm Associa CAM name/email for The Inlets at Riverdale ([cam-identification.md](cam-identification.md))
- Identify dealer for The Inlets
- myQ Partner API acceptance timeline
- Class B license vs subcontract partner
- Usage pricing final numbers (bands in [pre-cam-playbook.md](pre-cam-playbook.md) §C)
- FL entity formation timing ([entity-insurance-action-kit.md](entity-insurance-action-kit.md))
- August scope: shadow vs live pedestal (default: **shadow** — pre-cam-playbook §G)
- Pivot deadline if The Inlets CAM cold (default **Aug 1**)
