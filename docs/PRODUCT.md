# We Lift — Refined Product Idea

**Last refined:** July 16, 2026  
**Status:** Locked direction for The Inlets pilot and SWFL beachhead

---

## One sentence

**We Lift is autonomous Call Attendant for gated communities: it lets authorized vendors and workers through the gate when they don’t have a resident code or sticker — without a human on the line.**

---

## What the gate already does (we don’t replace this)

| Credential | Who | Result |
|------------|-----|--------|
| Keypad code | Residents (and sometimes guests) | Gate opens |
| RFID sticker / transponder | Residents | Gate opens |
| myQ guest pass | Invited social guests | Gate opens |

Those paths stay primary. Most cars never talk to We Lift.

---

## The real problem we solve

**Vendors and workers** (gardeners, lawn crews, pool techs, pest control, contractors) usually don’t get resident stickers. Today communities hack around that with:

- Shared vendor codes (leaks, never rotate)
- “Call the office / CAM / a resident”
- Leaving someone at the gate
- Bouncing the vendor and delaying work

That pain is intermittent and **low volume** — which is exactly why paying for a full overnight guard or a full virtual-SOC package is overkill, and why a focused AI Call Attendant fits.

---

## What We Lift is

```text
Vendor at pedestal (no code / no sticker)
  → taps Call Attendant on myQ tablet
  → Retell AI asks name + company + where they’re working
  → checks CAM’s authorized vendor / exception list
  → APPROVE → myQ Partner API unlocks
  → DENY    → leave; CAM must add them (or host sends a guest pass)
  → everything logged for the board
```

| We are | We are not |
|--------|------------|
| Exception-path **vendor access** | A replacement for codes / stickers |
| Autonomous verify + open | A 2am human on SMS |
| Low-call-volume software + list ops | A full virtual guard / Envera clone |
| Overnight beachhead (when nobody answers) | Required for every entry |

---

## Who it’s for

**Buyer:** CAM / board of a LiftMaster + myQ Community HOA  

**User at the gate:** Non-resident worker without credentials  

**Not the user:** Residents (redirect to code/sticker); casual guests (prefer myQ pass)

---

## Why this version of the idea is stronger

1. **Fits existing hardware** — phone routing on Call Attendant, not new pedestals.
2. **Honest volume** — rare calls → cheap AI ops, simple autonomy, less liability theater.
3. **Clear deny policy** — unsure = deny; host/CAM updates the list. No overnight human.
4. **Right competitor set** — shared codes and “call the manager,” not Allied’s full virtual gatehouse.
5. **Right price anchor** — CAM time + bad vendor codes + missed work, **not** a $9k overnight guard.

---

## Commercial shape (refined for low volume)

Stop selling “overnight guard replacement.” Sell **vendor desk / Call Attendant coverage**.

| Component | Direction | Why |
|-----------|-----------|-----|
| Monthly platform | Modest flat (coverage + DID + logging + list hosting) | Boards like a line item; you’re always on |
| Included verified opens | Small pool (e.g. 20–40 / mo) | Matches quiet vendor traffic |
| Per extra verified open | Low single-digit to low-teens $ | Usage-fair when a renovation week spikes |
| Per denied / spam call | $0 or tiny | Don’t punish the HOA for tire-kickers |

**Do not** lead with $2.5k–$4k “vs $9k guard” unless the CAM is already shopping overnight staffing. For vendor-exception product, first paid pilots can sit **lower** — still cover insurance + Retell + your ops, but don’t pretend you’re replacing a booth.

Exact numbers stay TBD after 2–4 weeks of real Call Attendant volume at The Inlets.

---

## Technical spine (unchanged, sharper)

| Piece | Role |
|-------|------|
| Retell | Voice at the tablet |
| `check_guest_list` | Vendor/company match → approve/deny |
| `open_gate` | myQ Partner API unlock only |
| Fail closed | API down or unsure → deny + daytime log |
| CAM list | Source of truth for who may enter as vendor |

**Critical dependency:** myQ Partner API. Without remote unlock, this is only a polite phone tree.

---

## Pilot definition of done (The Inlets)

1. Residents still use code/sticker only — zero AI opens marketed as resident unlock.  
2. ≥1 real vendor company on the list completes pedestal → AI → gate open.  
3. Unknown vendor is denied cleanly; CAM can add them next day.  
4. No human woken overnight.  
5. CAM understands the product as **vendor Call Attendant**, not “AI security guard.”

---

## CAM pitch (30 seconds)

> Your residents keep their codes and stickers. Guests keep myQ passes. We Lift only answers Call Attendant for people who aren’t supposed to have those — landscapers, pool guys, contractors. We check your vendor list and open the gate automatically, or we turn them away. Low volume, fully autonomous, logged for the board.

---

## What we deliberately won’t build next

- Resident facial recognition / video-as-auth  
- Replacing daytime booth staffing  
- Shared permanent vendor codes as the product  
- Human SMS unlock as the operating model  

---

## Repo map

| Doc | Use |
|-----|-----|
| This file | Product thesis |
| [decision-log.md](docs/pilot-the-inlets/decision-log.md) | Locked Q&A |
| [prompt.md](prompt.md) | What the agent says |
| [THIS-WEEK.md](docs/pilot-the-inlets/THIS-WEEK.md) | Execution checklist |
| [myq-api-path.md](docs/pilot-the-inlets/myq-api-path.md) | Unlock dependency |
