# Dealer & myQ Routing — The Inlets

**Goal:** Visitor taps **Call Attendant** after hours → call rings **We Lift Retell DID** → AI verifies → on-call unlocks (Phase 1) or API opens (Phase 2).

Integration is **phone routing**, not software on the tablet. Pattern from [01-metro-validation/how-to-connect-myq-to-smith.md](../../01-metro-validation/how-to-connect-myq-to-smith.md) (ignore Smith branding).

---

## Who to call (in order)

| # | Who | Why | Contact |
|---|-----|-----|---------|
| 1 | **CAM at The Inlets** | Facility admin, post orders, dealer of record | Lead: Associa Gulf Coast (941) 552-1598 — confirm named CAM ([cam-identification.md](cam-identification.md)) |
| 2 | **LiftMaster dealer of record** | CAP programming, Phone.com SIP, time-of-day routing | Ask CAM first |
| 3 | **myQ Community support** | Confirm facility live, calling path, unlock permissions | **877-247-6764** (tech) · **800-282-6225** (solutions) |
| 4 | **We Lift (Lucas)** | Retell DID + webhook must pass [setup-checklist.md](../../setup-checklist.md) §5 **before** any myQ forward | — |

> **Rule:** Use the **dealer of record** for The Inlets. A random dealer may lack myQ Business portal access for that facility.

---

## SWFL dealer list (if CAM doesn't know dealer of record)

Verify CAP / myQ Community experience before engaging:

| Dealer | Location | Contact |
|--------|----------|---------|
| **CIA Access Control Inc** | 1843 Barber Rd, Sarasota | [LiftMaster locator](https://local.liftmaster.com/fl/sarasota/cia-access-control-inc/50860) |
| **D & D Garage Doors** | 1177 Cattlemen Rd, Sarasota | (941) 371-7242 |
| **Kelly Automatic Gate Service** | Sarasota / Bradenton / Manatee | [kellyautomaticgates.com](https://www.kellyautomaticgates.com/liftmaster-gates) |
| **Precision Gate & Security** | Manatee / Sarasota / Charlotte | [precisiongate-securityinc.com](https://www.precisiongate-securityinc.com/automatic-gate-openers-and-operators) |
| **Sarasota Gate & Access** | Sarasota | (941) 349-4455 |

Also: [LiftMaster dealer locator](https://www.liftmaster.com/dealer-locator) — filter for myQ Community / access control.

---

## Info checklist (before dealer visit)

From [01-metro-validation/liftmaster-integration.md](../../01-metro-validation/liftmaster-integration.md):

| Item | The Inlets value |
|------|------------------|
| Facility legal name in myQ | [PLACEHOLDER: exact portal name] |
| **CAP model** | CAPXL / CAPXLV — photo of pedestal label |
| **Entrance ID(s)** | Main gate name in myQ portal |
| Phone.com active? | Yes / No · account holder |
| Current guard / quick-call number | [PLACEHOLDER] |
| myQ Business admin | CAM email + dealer contact |
| Remote unlock demo | CAM or dealer unlocks main gate live on call |
| **Retell DID** | `+1…` E.164 — share **only after** Retell §5 tests pass |
| Internet / cellular at pedestal | Failover if ISP drops |
| Post orders draft | Guest-list rules, deny/escalate, vendor hours |

---

## Step-by-step: zero → overnight routing

### Week 0 — Lucas (no dealer yet)

1. Complete Retell agent per [setup-checklist.md](../../setup-checklist.md) §§1–5 and [comet-retell-install-brief.md](../../comet-retell-install-brief.md).
2. Buy/import Retell US DID; assign to agent; test approve / deny / escalate from cell.
3. Deploy webhook (`webhook/run.sh` + stable HTTPS).
4. Set `DEFAULT_COMMUNITY=The Inlets` in `webhook/.env`.

### Week 0–1 — CAM + dealer discovery (30 min, 3-way)

5. CAM provides checklist items above.
6. Dealer confirms **Call Attendant / Guard / Quick Call** can point to external 10-digit number **8pm–6am**; daytime unchanged.
7. Schedule **on-site pedestal test** (10–15 min) with CAM or dealer present.

### Week 1 — Dealer configuration

8. Implement one of:
   - **Option A:** myQ People → `Overnight Gate Attendant` → phone = Retell DID
   - **Option B:** Facility **Quick Call** → Retell DID (overnight only)
   - **Option C (ideal):** Time schedule — booth by day, Retell **8pm–6am**; fallback = Phone.com time-of-day forward
9. Create **named We Lift SOC user** in myQ (not shared CAM login) with unlock rights for main entrance only.
10. Confirm **Phone.com SIP** active on facility.

### Week 1–2 — Acceptance test

11. Controlled pedestal test (temporarily route daytime to Retell for 10 min, or test after 8pm).
12. Verify: two-way audio, script says “The Inlets,” guest-list check, SMS arrives, Lucas unlocks in myQ, barrier moves.
13. Restore schedule; run **3–7 shadow nights** before resident-facing go-live.

---

## Email template — LiftMaster dealer

```
Subject: The Inlets — after-hours Call Attendant routing change (myQ Community)

Hi [DEALER CONTACT NAME],

I'm Lucas with We Lift. [CAM NAME] at The Inlets HOA asked us to coordinate an
after-hours routing update on their myQ Community CAP panel.

Request:
• 8:00pm–6:00am Eastern: Call Attendant / Guard / Quick Call → [RETELL DID]
• 6:00am–8:00pm: keep current destination ([EXISTING NUMBER])
• No hardware changes; Phone.com SIP path unchanged

We've already tested our attendant line from a cell phone. We need a short on-site
pedestal test once programmed.

Please confirm:
1. Panel model and whether time-of-day routing is supported in portal vs Phone.com
2. Your earliest on-site test window
3. Whether you can add a "We Lift SOC" myQ user with remote unlock for [MAIN ENTRANCE] only

Happy to join a 3-way with [CAM NAME] this week.

Lucas Despot · We Lift · [YOUR PHONE] · [YOUR EMAIL]
```

---

## Email template — board (via CAM, informational)

```
Subject: The Inlets — pilot overnight virtual gate attendant (8pm–6am)

Board / CAM,

The Inlets already uses myQ Community for codes, guest passes, and resident app access.
We Lift adds overnight live verification when those paths don't work — at the gate
tablet only, 8pm–6am.

• Residents: continue using myQ app, codes, and guest passes (unchanged)
• Visitors without access: tap Call Attendant → verified attendant → gate opens if approved
• Every open is logged; post orders govern who gets in

This is a limited August pilot. Daytime booth/process unchanged. We Lift does not replace
myQ or your LiftMaster dealer.

[Optional: 30-day pilot terms — counsel review before signature]
```

---

## Timeline & cost (planning)

| Phase | Duration | Cost |
|-------|----------|------|
| Retell + webhook stand-up | 2–5 days | ~$50–150/mo voice platform |
| CAM + dealer discovery | 3–7 days | ~5–15 hrs operator time |
| Dealer reprogram + site test | 1–2 weeks | **$150–500** typical truck roll (confirm with dealer) |
| Shadow nights → go-live | 1–2 weeks | $0 incremental |
| **Earliest live overnight routing** | **~2–3 weeks** from first CAM call | Excludes compliance delays |

**Critical path:** Retell tests → CAM/dealer call → dealer routing → shadow nights. **Never** forward myQ before Retell §5 passes.
