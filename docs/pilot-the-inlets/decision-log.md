# Decision Log — Lucas / We Lift

Locked product and pilot decisions. Update only by explicit owner change.

**Last updated:** July 2026  
**Pilot:** The Inlets · **Target:** August 2026

---

## Q1 — Autonomous verify + open

**Decision:** Fully autonomous — AI verifies visitor and opens the gate (e.g. gardener at gate without a code).

| Layer | Choice |
|-------|--------|
| Verification | Retell voice agent + guest list / post orders |
| Open (target) | myQ Partner API remote unlock (Phase 2) |
| Open (August pilot) | **SMS bridge OK** — Lucas taps Unlock in myQ app; disclose as human-confirmed |

**Implication:** Sell access-control automation, not call-handling only. API pursuit starts Week 0; SMS acceptable for first 30–60 nights.

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
| **On-call Phase 1** | **Sole operator: Lucas** |
| **Repo** | Single monorepo `welift` (launch pack + product code merged) |
| **Target month** | **August 2026** first live overnight |

---

## Open items (not locked)

- LiftMaster **dealer of record** for The Inlets (discovery in progress)
- myQ Partner API acceptance timeline
- Class B license vs subcontract partner
- Paid pilot fee and signed agreement timing
- FL entity legal name for contracts/insurance
