# myQ Community + LiftMaster — 8pm–6am Virtual Attendant

**Stack confirmed:** LiftMaster panel on **myQ Community** (cloud).  
**Coverage:** Your agents own visitor exceptions **8:00pm–6:00am**.  
**Day/evening outside that window:** Booth and/or residents via myQ app + codes.

This is a strong retrofit — you are **not** replacing myQ. You are the overnight human layer when the booth is closed and the visitor doesn’t have a code/pass.

---

## What already works (leave alone)

| myQ / LiftMaster feature | Role in your model |
|--------------------------|--------------------|
| Keypad / PIN codes | Primary self-serve entry — never rip these out in phase 1 |
| **Virtual Guest Passes** | Best automation: resident/manager issues pass → visitor enters without calling you |
| Resident myQ app unlock / video answer | Residents can still admit their own guests anytime |
| Activity log / video clips | Feed into monthly board reports (with HOA permission) |
| Dealer + myQ Business portal | Facility admin, credentials, remote diagnostics |

---

## Your overnight role (the product)

```text
Visitor at gate (8pm–6am)
        │
        ├─ Valid code or guest pass ──► Gate opens (myQ/LiftMaster) — no agent
        │
        ├─ Resident answers via myQ app ──► Resident grants — no agent
        │
        └─ No pass / no answer / “Call guard”
                 │
                 └─ Routes to YOUR attendant (SIP / forwarded guard number)
                          │
                          ├─ Verify vs guest list / call resident / post orders
                          └─ Remote OPEN via myQ portal or dealer-authorized open path
```

**Sell this line:**  
> “myQ handles codes, guest passes, and resident app unlocks. We handle the overnight live attendant when none of those work — at a fraction of a night booth.”

---

## How to wire 8pm–6am onto myQ Community

### 1. Call routing (visitor → agent)

With CAPXL / CAPXLV-class panels on myQ:

- Keep SIP / phone service active (dealer / Phone.com-style setup as required by LiftMaster).
- Set **Guard / Attendant** destination on a schedule:
  - **Outside 8pm–6am** → booth handset / daytime number  
  - **8pm–6am** → your SOC DID or SIP endpoint  

Confirm with the **LiftMaster dealer of record** for that facility (myQ permissions are usually dealer + property admin).

### 2. Gate open (agent → barrier)

Prefer, in order:

1. **myQ Community / Business portal remote unlock** for that entrance (manager-level permission for your SOC accounts)  
2. Same Door Board / gate channel the panel already opens (dealer-configured)  
3. Last resort: operator EXIT/OPEN relay (UL325 via authorized dealer only)

Create **named SOC user accounts** (not a shared CAM login). Audit every remote open.

### 3. Reduce call volume (makes 8pm–6am profitable)

Push the community to use what myQ already sold them:

- Time-boxed **guest passes** for parties / Airbnb / overnight guests  
- Recurring vendor passes (Amazon, landscapers)  
- Directory → resident phone/app first; attendant only on no-answer  

Your agents should be **exception handling**, not the default path for every car.

---

## Permissions & ops checklist (ask CAM / dealer)

- [ ] Facility is live in **myQ Community** — admin who can add users?
- [ ] Dealer of record name / phone (SWFL LiftMaster dealer)
- [ ] Panel model: CAPXL / CAPXLV / other?
- [ ] Can property manager **remotely unlock** main gate today from the web portal?
- [ ] Is **Guard** call destination configurable by time of day?
- [ ] Guest pass feature enabled for residents?
- [ ] Can we export or view **access activity** for board monthly PDF?
- [ ] Video: live stream / clip retention available for attendant use?
- [ ] Internet / cellular failover at the pedestal?

---

## Product rules on myQ sites

1. **Do not compete with myQ** — partner with it. You sell overnight live labor + SOPs + board reporting.  
2. **Codes + guest passes stay primary**; you take overflow.  
3. **8pm–6am only** until volume and SLAs are proven.  
4. Every agent open is logged (who, when, why, clip if available).  
5. If myQ/cloud is down: codes/local still work; post orders escalate to on-call CAM — you don’t promise unlocks you can’t complete.

---

## Sales one-liner for boards already on myQ

> “You’re already paying for myQ Community hardware and apps. We don’t replace that — we replace the overnight guard shift. Codes and guest passes still work; from 8pm to 6am, anyone without access gets a live attendant who can verify and open through your existing LiftMaster/myQ system.”

---

## Dealer partnership

Stay in good standing with the local LiftMaster/myQ dealer:

- They own CapEx, warranty, CAP programming, SIP signup  
- You own 8pm–6am attendant labor, post orders, QA, board packs  

Ask for preferred-vendor intros to other myQ Community HOAs they support in Manatee/Sarasota.
