# How to connect the myQ tablet to your live attendant (Smith.ai)

## Important: what “integration” actually is

The myQ / LiftMaster tablet does **not** load a Smith.ai app or video widget on screen.

It already knows how to **place a phone/VoIP call**. You change **who that call rings**.

```text
Visitor taps “Call” / directory / quick-call on tablet
        ↓
Tablet uses Phone.com SIP (myQ’s calling path)
        ↓
Rings a 10-digit number you control
        ↓
That number is answered by Smith.ai
        ↓
Agent follows your script → you/they unlock in myQ
```

To the visitor it feels like “talking to the gate attendant.”  
Behind the scenes it’s: **tablet call → Smith.ai number**.

---

## What you need in place

| Piece | Who provides it |
|-------|-----------------|
| Working myQ Community tablet (CAPXL / CAPXLV) | Already at gate |
| Active **Phone.com** calling on that facility (LiftMaster’s SIP path) | Dealer / myQ admin |
| **myQ Business / Community** admin access | CAM or LiftMaster dealer |
| **Smith.ai** account + phone number they assign you | You |
| Written **post orders** / script for that HOA | You |
| Way to **unlock** (myQ remote open login, or you on SMS) | You + CAM |

---

## Step-by-step setup

### Step 1 — Stand up Smith.ai first
1. Create Smith.ai account for this HOA (or one account with HOA-specific intake).
2. Get your **Smith.ai phone number**.
3. Load the script, e.g.:
   - “Thank you for calling Oak Haven gate, this is the overnight attendant.”
   - Ask: name, vehicle, who they’re visiting / address
   - Check guest list rules you provide
   - If approved: confirm you’ll open the gate
   - If denied: ask them to contact their host for a guest pass
4. Complete Smith’s test call before forwarding anything.

### Step 2 — Decide the “open gate” method (separate from the call)
The call only talks. Opening is a second action:

| Mode | What happens |
|------|----------------|
| **Shadow (week 1)** | Smith texts/emails you → **you** tap Unlock in myQ Community web/app |
| **Smith unlocks** | Give Smith a dedicated myQ manager login (or your ops person) with unlock rights only for that gate |
| **Later** | Webhook/automation if you build it — not required for trial |

### Step 3 — Get the LiftMaster dealer / myQ admin on a call
You usually **cannot** fully reprogram CAP calling alone without facility admin rights. Ask the dealer of record:

> “We need after-hours calls from the main gate tablet to ring this number: **(XXX) XXX-XXXX** (Smith.ai), from **8:00pm–6:00am**. Daytime stays as today (booth / resident directory).”

They will work in **myQ Business / Community** (and Phone.com linked to the facility).

### Step 4 — Point the tablet’s attendant call at Smith
Exact labels vary by firmware, but the pattern is one of these:

**Option A — Staff / Management / Guard person**
1. In myQ People, add a person: `Overnight Gate Attendant`
2. Set their phone number = **your Smith.ai number**
3. Put them in a group that can be called from the gate directory / quick-call
4. On the tablet UI, that entry is what visitors tap (or rename button label if the community customizes welcome actions)

**Option B — Quick Call / Auto Call number**
1. In myQ facility settings, set **Quick call** (or similar) to the Smith.ai number  
2. Used when the panel has a one-tap “call office/guard” or loop auto-call

**Option C — Schedule (ideal)**
1. Daytime: quick-call / guard = booth phone  
2. **8pm–6am:** same field = Smith.ai number  
3. If the portal can’t time-route, use Phone.com / carrier **time-of-day forward**:  
   booth number forwards to Smith only at night

**Most SWFL trials use:** Smith number as the overnight guard destination + dealer confirms a test call from the live tablet.

### Step 5 — Test at the actual pedestal
1. After 8pm (or temporarily point daytime to Smith for a 10-minute test)
2. On the tablet, tap the attendant / quick-call control
3. Confirm:
   - Audio both ways on the pedestal speaker/mic
   - Smith answers with the right community script
   - Unlock works (you or Smith)
   - Event shows in myQ activity if applicable
4. Flip routing back / enable the 8pm–6am schedule

### Step 6 — Train the HOA on the visitor story
Residents should still:
- Use codes / remotes / guest passes (preferred)
- Use directory → resident app when possible  

Visitors without a code: **Call attendant** → your overnight service.

---

## What you will *not* get out of the box

| Expectation | Reality |
|-------------|---------|
| Smith.ai video face pops up full-screen on the myQ tablet | **No** — CAP video is built for **resident myQ app** / Phone.com video path, not Smith’s receptionist UI |
| Custom “our company” branded app on the tablet | **No** without replacing hardware |
| Silent API from tablet → Smith without a phone call | **Not** how CAP works today |

**Visitor experience:** talk through the tablet like a phone intercom.  
**Your branding:** in the *voice script* and board materials, not a custom tablet OS.

If you need **on-screen video of the agent**, that’s a different product (replace/supplement panel) — not a stock myQ + Smith hookup.

---

## Checklist for the dealer meeting

- [ ] Facility name / CAP model (CAPXL vs CAPXLV)
- [ ] Phone.com already active? (required for calling)
- [ ] Who has myQ Business admin login?
- [ ] Current “guard / office / quick call” number today?
- [ ] Can we schedule by hours (8pm–6am)?
- [ ] Who can remote-unlock the main gate in myQ today? (demo it)
- [ ] Test call window booked on-site

---

## One-sentence summary

**Integrate by making the tablet dial your Smith.ai number for after-hours attendant calls; use myQ remote unlock to open the gate — you don’t install software on the tablet.**
