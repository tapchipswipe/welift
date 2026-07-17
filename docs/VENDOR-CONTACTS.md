# Vendor Contacts — Who Gets the Code?

**Problem:** CAM knows *which companies* are allowed. They often do **not** know which tech’s personal phone will be at the gate today — especially for large lawn / plumbing / HVAC firms.  
**Principle:** CAM authorizes the **company**. The **company** (or a single access contact) gets the credential and routes it to the truck.

Related: [PRODUCT.md](PRODUCT.md) · [GATE-SECURITY.md](GATE-SECURITY.md)

---

## Short answer

| Company type | What CAM enters | Who receives the SMS code |
|--------------|-----------------|---------------------------|
| **SMB / owner-operator** (garage door guy, solo landscaper) | One business mobile | That owner — same number on the truck |
| **Multi-crew / big vendor** | **Dispatch / office / account-manager phone** (or email) — **not** every tech | Dispatch → they already tell Mike which HOA to hit; they forward the code the same way |
| **Optional later** | Vendor portal login for that company | Dispatcher enters “today’s tech phone” or forwards in-app |

**CAM should almost never need the driver’s personal cell for a 40-person lawn company.**

---

## Why this matches how vendors already work

Large vendors already solve “who is on which job”:

- Dispatch board / ServiceTitan / Jobber / email / group text  
- “Truck 4 — The Inlets — 9am clubhouse”

They do **not** ask the HOA CAM for each tech’s phone.  
We Lift should plug into that reality:

```text
CAM: "GreenSide is allowed Mon–Fri 7–6"
We Lift: texts today's code → GreenSide dispatch number on file
GreenSide: "Mike — Inlets code is 482193" (their channel)
Mike: types code at gate
```

Authentication for the happy path = **code held by the authorized company**, not “we SMS’d the exact human in the driver seat.”

---

## Three contact models (use all; pick per vendor)

### Model A — Owner line (SMB)

**When:** One person *is* the business.  
**CAM stores:** Mobile on the truck / Google Business listing.  
**We Lift:** SMS code to that number.  
**Friction:** None.

### Model B — Dispatch line (default for big companies)

**When:** Many techs, rotating trucks.  
**CAM stores:** One **access contact**:

- Main dispatch mobile/SMS-capable number, or  
- Account manager who already coordinates with the HOA, or  
- Shared “gates@greenside.com” + SMS gateway / email with code  

**We Lift:** Every morning (or at window start) send:

> The Inlets — GreenSide vendor access today until 6pm — keypad code 482193 — do not share outside your crew.

**Vendor responsibility:** Get code to the assigned tech (they already assign the job).  
**CAM responsibility:** Keep the **company** on the roster; update dispatch number if it changes.

### Model C — Job-day tech phone (optional precision)

**When:** You want the code only on the person on-site (higher security / one-offs).  
**Who enters the phone:** Usually **not** CAM guessing — one of:

1. **Vendor dispatcher** in a simple vendor portal: “Assign Inlets → Mike → +1…” → We Lift SMS Mike  
2. **Resident** scheduling their own plumber: creates myQ guest pass / We Lift one-off with *that* plumber’s cell  
3. **CAM** for a known one-off: “Acme Plumbing, Thursday, tech cell ___” (rare)

Use Model C for showings, emergency plumber, or when CAM insists on tighter control — not for weekly mow.

### Model D — Company phone as keypad PIN (big vendors · planned)

**When:** Multi-crew firm; tech at the pedestal doesn’t have today’s forwarded SMS code.  
**CAM stores:** Same access contact phone as Model B (dispatch / office).  
**We Lift:** During the authorized window, that **company phone number’s digits** are a valid keypad entry (typically US 10-digit national number — not country code, not a random tech cell).

```text
Mike (GreenSide) at The Inlets keypad
  → types GreenSide dispatch number on file
  → gate opens if GreenSide is authorized now
```

**Why it helps big companies:** every tech already knows “the office number”; dispatch isn’t a bottleneck for every truck.  
**Auth property:** still bound to CAM roster + schedule — not a public Facebook code.  
**Fallback:** if phone PIN fails → Call Attendant (AI) with company + proof.

---

## What CAM actually maintains (keep it tiny)

Per vendor company:

| Field | Required? | Example |
|-------|-----------|---------|
| Company name | Yes | GreenSide Lawn |
| Access contact type | Yes | owner / dispatch / email |
| Access phone (SMS) and/or email | Yes | +1941… or gates@… |
| Schedule window | Yes | Mon–Fri 07:00–18:00 |
| Notes | No | “Pool only — clubhouse” |

**Not required for v1:** Full employee directory of the lawn company.

---

## How big companies onboard (ops script)

1. CAM adds “GreenSide Lawn — allowed.”  
2. CAM asks (once): “Who should receive gate codes — dispatch text or account manager?”  
3. That number goes on the roster.  
4. CAM emails GreenSide once:  
   *“You’re on The Inlets vendor list. Codes go to [dispatch]. Forward to the tech on the ticket. If a tech has no code, Call Attendant is backup with today’s proof PIN.”*  
5. Done until they change dispatch.

If GreenSide wants techs to self-pull codes later → vendor portal (phase 2).

---

## Real estate agents (similar pattern)

| Size | Contact |
|------|---------|
| Solo agent | Their cell — showing PIN/code SMS |
| Big brokerage | Listing agent cell **or** showing coordinator; showing is a **one-off window**, not a standing company code for all agents |

Don’t give “RE/MAX” one eternal code for every agent in the county. Prefer **per-showing** credential to the agent on that appointment.

---

## Security tradeoff (be honest)

| Model | Spoof risk | Notes |
|-------|------------|-------|
| SMS to owner phone | Low–medium | Phone ≈ person |
| SMS to dispatch | Medium | Insider at company could leak; still far better than public shared code; rotate daily |
| SMS to day’s tech only | Lower | More ops friction |
| AI name-only | High | Rejected |

Mitigations for dispatch model: **daily rotate**, window expiry, log issuance, AI fallback still needs **proof PIN** (can be same digits or a second short PIN in the SMS).

---

## Product rule (lockable)

1. **CAM authorizes companies + one access contact** (owner or dispatch).  
2. **We Lift delivers codes to that contact** — not “every possible driver.”  
3. **Large vendors route codes internally** like they route job tickets.  
4. **Planned:** company access phone digits work as a **keypad PIN** during the window (Model D) — another no-AI path for big vendors.  
5. **Optional:** [vendor portal](VENDOR-PORTAL.md) so dispatch assigns today’s tech phone and sends the code.  
6. **AI** remains backup when the person at the pedestal has no SMS code and phone PIN failed / unknown.

---

## CAM one-liner

> “You don’t need every landscaper’s cell phone. You tell us the company and who gets the codes — usually the owner or dispatch. They send it to whoever’s on the truck. If someone shows up without it, AI is the backup.”
