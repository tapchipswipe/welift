# Decision Log — Lucas / We Lift

Locked product and pilot decisions. Update only by explicit owner change.

**Last updated:** July 16, 2026 (autonomous lock)  
**Pilot:** The Inlets · **Target:** August 2026 (shadow / pre-CAM — see [pre-cam-playbook.md](pre-cam-playbook.md) · [THIS-WEEK.md](THIS-WEEK.md))

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

## Q6 — Guest list / credentials (original question)

**Decision:** **Residents use myQ guest passes and codes** as primary entry. **AI handles exceptions only** — visitors who cannot self-serve after hours.

| Who maintains list | Model |
|---------------------|--------|
| Residents | myQ guest passes (preferred path) |
| CAM / board | Post orders, vendor rules, deny/escalate policy |
| We Lift | Nightly exception list in `data/guest-list.json` only as needed for pilot; not replacing myQ passes |

**Note:** “CAM” = Community Association Manager — management company or on-staff manager running the HOA day to day.

---

## Additional locked decisions

| Topic | Decision |
|-------|----------|
| **Brand** | **We Lift** (repo: [welift](https://github.com/tapchipswipe/welift)) |
| **Coverage window** | 8:00pm–6:00am Eastern |
| **Users of AI** | **Visitors at pedestal only** — not residents |
| **Residents** | Continue myQ app, codes, guest passes — unchanged |
| **On-call Phase 1** | **None** — autonomous overnight; daytime log review only |
| **Repo** | Single monorepo `welift` (launch pack + product code merged) |
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
