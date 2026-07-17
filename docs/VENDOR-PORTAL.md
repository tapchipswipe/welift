# Vendor Portal — How It Works

**Idea:** Large vendors (lawn, plumbing, HVAC) log into a simple portal so **dispatch** can put today’s gate code on the **right tech’s phone** — without the CAM knowing every driver.  
**Related:** [VENDOR-PORTAL.md](VENDOR-PORTAL.md) · [VENDOR-CONTACTS.md](VENDOR-CONTACTS.md) · [PRODUCT.md](PRODUCT.md) · [GATE-SECURITY.md](GATE-SECURITY.md)

**Full build steps:** [VENDOR-PORTAL-ROADMAP.md](VENDOR-PORTAL-ROADMAP.md)

**Wave 1 (now):** Same send API + UI at [`/access`](../webhook/static/access.html) — CAM or vendor dispatch can send a code to any tech/dispatch phone. Auth-separated Vendor Portal is Wave 2 (this doc).

---

## One sentence

**CAM says which companies are allowed; the vendor portal lets that company’s dispatcher assign who is coming and where the code should go.**

---

## Who uses what

| App | User | Job |
|-----|------|-----|
| **CAM Access Desk** | Community manager | Approve/revoke companies, windows, community rules |
| **Vendor Portal** | Vendor dispatch / owner | See communities they’re allowed into; assign today’s tech; get/send codes |
| **Keypad / myQ** | Tech in the truck | Type the code |
| **AI Call Attendant** | Tech with no code | Rare fallback + proof |

Vendors **cannot** authorize themselves at an HOA. Only CAM can add the company to the roster. Portal access is invited after CAM approval.

---

## Happy path (big lawn company)

```text
1. CAM adds "GreenSide Lawn" at The Inlets (window Mon–Fri 7–6)
2. CAM invites gates@greenside.com (or dispatch mobile) → vendor portal account
3. Monday 6:30am — dispatch opens We Lift Vendor Portal
4. Sees: The Inlets · authorized today · needs tech assignment
5. Selects: Tech = Mike Torres · phone = +1… · job = clubhouse commons
6. Taps "Send today's gate code"
7. We Lift mints time-bound code + SMS to Mike (optional: also email dispatch)
8. Mike arrives, types code on keypad — no AI call
```

SMB owner-operator can skip the portal: codes still SMS to their one business phone from the CAM desk. Portal is optional power for multi-crew firms.

---

## What the vendor sees (screens)

### 1) Login
- Email + password, or magic link SMS/email  
- Scoped to **their company only** (never other vendors, never CAM tools)

### 2) Home — “Today”
List of communities where this company is currently authorized:

| Community | Window | Status | Action |
|-----------|--------|--------|--------|
| The Inlets | 7:00am–6:00pm | Needs assignment | Assign tech |
| Oak Grove HOA | 8:00am–4:00pm | Code sent to Dana · **···2193** | Resend / reassign |

### 3) Assign & send (core action)
Fields:

- Community (pre-filled)  
- Tech name (optional but nice for logs)  
- **Tech mobile** (required to SMS)  
- Job note / area (clubhouse, lot 12, etc.)  
- Date (default today)  

Button: **Send gate code**

System:

1. Checks company still authorized + inside window  
2. Creates/rotates today’s credential for that community  
3. SMS to tech: `The Inlets — GreenSide — today until 6pm — keypad 482193`  
4. Logs: who assigned, which phone, when, which community  

### 4) Crew list (optional convenience)
Dispatch saves frequent techs (name + phone) as favorites so assignment is 2 taps, not retyping.

### 5) History
- Codes sent (masked), opens if we get myQ events later, AI fallback uses  
- CAM can see the same audit from their desk  

### 6) Multi-community (scale)
Same company servicing 15 HOAs on We Lift → one login, filter by community, assign per site.

---

## Roles inside the vendor company

| Role | Can do |
|------|--------|
| **Dispatch admin** | Assign any tech, manage crew list, see all communities for that company |
| **Dispatcher** | Assign + send codes |
| **Tech** (later) | Optional: “Request my code for The Inlets today” if dispatch allows self-serve |

V1 can be a **single company login** (shared dispatch user). Fine for pilot.

---

## Security model

| Rule | Why |
|------|-----|
| Portal invite only after CAM adds company | Vendors can’t freeload onto a gate |
| Codes only for communities on their roster | No cross-HOA fishing |
| Window enforced at send time | Can’t mint overnight code if only daytime authorized |
| SMS to tech phone dispatch entered | Credential lands on the truck |
| Daily / window expiry | Limits blast radius if forwarded |
| Audit: dispatcher identity + phone + timestamp | Board / incident review |
| Rate limits | Stop spam minting |
| CAM can revoke company → portal loses send rights instantly | Kill switch |

**Still not perfect:** a bad dispatcher can SMS a friend. That’s an **insider** risk at the vendor — same as them sharing a paper code today. Mitigate with rotate + logs + CAM revoke. Better than a public Facebook code.

---

## How this ties to AI fallback

SMS body can include both:

```text
Keypad code: 482193
If the keypad fails, Call Attendant and say you're with GreenSide; proof PIN: 482193
```

Same digits = simple. Or separate proof PIN if you want keypad codes managed only in myQ.

If Mike never got SMS → Call Attendant → must give company + proof PIN (dispatch can read it from portal “today’s code”).

---

## Relationship to CAM Access Desk

```text
CAM Desk                          Vendor Portal
────────                          ─────────────
Add/remove company        →       Company appears after invite
Set schedule windows      →       Enforced when sending codes
Revoke company            →       Send disabled
View audit of all vendors ←       View audit for own company
Never enters tech phones  ←       Dispatch enters tech phones
```

---

## MVP vs later

### MVP (pilot — enough to love)

1. Magic-link login for one dispatch email per company  
2. List of authorized communities  
3. Form: tech phone + Send code  
4. SMS via Twilio + log  
5. CAM can see “code sent to ···1234 at 6:41am by gates@greenside.com”

No native app. Mobile web is enough (dispatch is often on a phone).

### Phase 2

- Saved crew roster  
- “Resend to same tech”  
- Push/email digest of morning codes for all assigned HOAs  
- Tech self-serve request (dispatch approval)  
- Jobber / ServiceTitan: job scheduled at The Inlets → auto-prompt assign code  

### Phase 3

- myQ API creates the guest pass automatically on Send  
- Burn-after-first-use codes  
- Geofence / time-of-send alerts  

---

## UX sketch (mobile web)

```text
┌─────────────────────────────┐
│ GreenSide · We Lift         │
│ Today — Tue Jul 16          │
├─────────────────────────────┤
│ The Inlets                  │
│ Mon–Fri 7am–6pm · OK to send│
│                             │
│ Tech phone                  │
│ ┌─────────────────────────┐ │
│ │ +1 (941) 555-0199       │ │
│ └─────────────────────────┘ │
│ Name (optional) Mike Torres │
│                             │
│ [ Send today's gate code ]  │
│                             │
│ Last sent 6:41am → ···0199  │
├─────────────────────────────┤
│ Oak Grove — code active ✓   │
└─────────────────────────────┘
```

Three fields. One button. That’s the product.

---

## Why vendors will use it

| Pain today | Portal |
|------------|--------|
| CAM texts a random code in email threads | One place, every HOA they service |
| Tech at gate with no code → angry call to dispatch | Dispatch sends in 10 seconds from phone |
| Shared company code leaked | Daily code per community, logged |
| New temp doesn’t know the gate | Assign their cell before the route |

Pitch to GreenSide: *“You’re already approved at The Inlets. Open this link, put the tech’s number, hit send. Done.”*

---

## Why We Lift wants it

1. CAM doesn’t manage 200 personal cells  
2. Codes land on the actual truck more often → **fewer AI calls**  
3. Sticky workflow for multi-site vendors → expansion across HOAs  
4. Clear audit for boards  

---

## Build note (repo today)

Not built yet. Current stack is Retell + webhook + guest-list JSON.  
Vendor portal is the **next product surface** after:

1. CAM can maintain roster (even a simple form / Airtable)  
2. Credential mint + SMS works  
3. One pilot vendor (GreenSide-class) uses assign → SMS → keypad  

Suggested stack later: simple Next.js app + auth + Twilio + same credential service the webhook uses.

---

## Open decisions

1. Magic link vs password for dispatch? (**Recommend magic link** for MVP)  
2. One shared dispatch login vs named dispatchers? (Shared OK for pilot)  
3. Can one code be active per company per community per day, or per tech? (**Recommend one community-daily code**; SMS can go to multiple techs if two trucks — same code that day, or mint per assignment if CAM wants tighter)  
4. Email codes as well as SMS?
