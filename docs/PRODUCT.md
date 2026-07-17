# We Lift — Refined Product Idea

**Last refined:** July 16, 2026 (code-first + AI fallback)  
**Status:** Locked direction for The Inlets pilot and SWFL beachhead

---

## One sentence

**We Lift is vendor access for gated communities: the CAM approves vendors, we text them a working time-bound gate code, and an AI Call Attendant is only the backup when the code isn’t used.**

---

## The insight

Most authorized vendors should **never talk to the AI**.

| Path | Cost to We Lift | Experience |
|------|-----------------|------------|
| **Primary — SMS / myQ code** | Cheap SMS (or myQ guest pass API) | Vendor types code on keypad → in |
| **Fallback — AI Call Attendant** | Retell minutes | No code / lost code / one-off → verify + unlock |
| **Residents** | $0 | Sticker / resident code (unchanged) |

If CAM lists GreenSide, AquaClear, and Acme Plumbing with phone numbers, We Lift **automatically texts each a working code** for the allowed window. That saves AI cost, reduces spoofing (code went to a known phone), and matches how gates already work.

---

## What the gate already does (we don’t replace this)

| Credential | Who | Result |
|------------|-----|--------|
| Keypad code | Residents | Gate opens |
| RFID sticker / transponder | Residents | Gate opens |
| myQ guest pass | Invited social guests | Gate opens |

---

## What We Lift adds

### 1) Access Desk (CAM) — authorization

CAM enters vendors (and optional realtors / one-offs):

- Company name  
- **Access contact** — owner mobile (SMB) or **dispatch / office** (multi-crew). CAM does **not** need every driver’s personal cell. See [VENDOR-CONTACTS.md](VENDOR-CONTACTS.md).  
- Schedule window (e.g. Mon–Fri 7am–6pm, or “Thursday only”)  
- Optional: unit / common areas  

### 2) Auto credential — authentication

On save / each morning / at window start:

```text
CAM adds vendor + access contact phone
  → We Lift creates time-bound keypad code or myQ guest pass
  → SMS to access contact: "The Inlets vendor access 7am–6pm: code 482193"
  → SMB: owner is on the truck → done
  → Big company: dispatch forwards code to today's tech (same as job assignment)
  → Tech uses keypad — no Call Attendant, no AI charge
```

Prefer **myQ guest pass / temporary code via Partner API** when available (native to the tablet). Until then: coordinated temp codes with dealer/CAM process, or SMS of a We Lift–issued code the CAP already accepts.

### 3) AI Call Attendant — exception only

```text
Someone at pedestal without a working code
  → taps Call Attendant
  → AI asks company + proof (PIN / WO / why no code)
  → on list + proof → myQ remote unlock
  → else deny + log
```

AI volume should trend toward **near-zero** for standing vendors who get morning texts.

---

| We are | We are not |
|--------|------------|
| **Vendor credential issuer** + low-volume AI backup | An AI receptionist for every entry |
| Time-bound codes to **known phones** | Forever shared “vendor code 1234” on a sticky note |
| Autonomous unlock when AI is needed | Overnight human on SMS |
| Software sitting on existing myQ hardware | New pedestals / full virtual guardhouse |

---

## Why this is better than “AI answers everyone”

1. **Unit economics** — SMS pennies vs Retell minutes per visit.  
2. **Security** — code delivered to CAM-registered phone beats “I’m with GreenSide” on the mic.  
3. **Familiar UX** — vendors already understand keypad codes.  
4. **Honest product** — Call Attendant stays rare (lost code, new subcontractor, after-hours one-off).  
5. **CAM ease** — approve once; system texts; no babysitting the gate.

---

## Security notes (codes done right)

| Do | Don’t |
|----|--------|
| Rotate daily or per-window | One static vendor code for years |
| Send only to roster phone numbers | Post codes in Facebook groups |
| Expire at end of window | Let codes work at 2am if only daytime authorized |
| Log issue + use + revoke | Share one code across unrelated trades |
| AI requires extra proof if they didn’t use the SMS code | Let AI open on company name alone |

Standing vendors: **daily rotating code** texted to dispatch.  
One-offs / showings: **single-window code** texted at booking.

---

## Who it’s for

**Buyer:** CAM / board on LiftMaster + myQ Community  

**Happy path user:** Vendor who got a morning text and uses the keypad  

**AI user:** Exception — no code, wrong day, subcontractor not on roster  

**Not the user:** Residents (sticker/code only)

---

## Commercial shape

Sell **Vendor Access Desk** (roster + auto codes + logging), not “AI guard hours.”

| Component | Direction |
|-----------|-----------|
| Monthly platform | Roster, auto-SMS codes, logging, Call Attendant standby |
| Included SMS credentials | e.g. 50–100 code sends / mo |
| Included AI fallback calls | Small pool (e.g. 10–20 / mo) |
| Overage | Per extra SMS; per extra AI call / verified open |

AI is a **feature of the desk**, not the meter you want spinning.

---

## Technical spine

| Piece | Role |
|-------|------|
| Access Desk UI / form | CAM CRUD for vendors + phones + windows |
| Credential worker | Mint time-bound code / myQ pass; SMS via Twilio |
| Retell + webhook | Fallback verify + myQ unlock |
| Audit log | Issued codes, keypad use (if available), AI opens/denies |

**Critical path still:** myQ Partner API (guest passes + remote unlock). Twilio here is for **code delivery to vendors**, not waking a human to open the gate.

---

## Pilot definition of done (The Inlets)

1. CAM adds ≥3 standing vendors with phones.  
2. Each receives an automated time-bound code SMS.  
3. ≥1 vendor enters via keypad using that code (no AI).  
4. AI path tested for “forgot code” with proof — not name-only.  
5. Board log shows credentials issued vs AI fallbacks.

---

## CAM pitch (30 seconds)

> You tell us which vendors are allowed and their phone numbers. We text them a working gate code for their window — they use the keypad like everyone else. If someone shows up without a code, our AI Call Attendant is the backup: verify against your list, open or deny, all logged. Residents keep stickers and codes. You’re not buying an AI guard; you’re buying vendor access that doesn’t need a person.

---

## Repo map

| Doc | Use |
|-----|-----|
| This file | Product thesis |
| [GATE-SECURITY.md](GATE-SECURITY.md) | Proof, PIN/code, anti-spoof |
| [VENDOR-CONTACTS.md](VENDOR-CONTACTS.md) | SMB owner vs big-company dispatch — who gets the SMS |
| [VENDOR-PORTAL.md](VENDOR-PORTAL.md) | How dispatch assigns today’s tech and sends the code |
| [VENDOR-PORTAL-ROADMAP.md](VENDOR-PORTAL-ROADMAP.md) | Complete step-by-step build breakdown (Phase 0→8) |
| [decision-log.md](pilot-the-inlets/decision-log.md) | Locked Q&A |
| [prompt.md](../prompt.md) | AI fallback script |
| [THIS-WEEK.md](pilot-the-inlets/THIS-WEEK.md) | Execution |
