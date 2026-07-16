# Smith.ai Correct Setup — Overnight Gate Attendant

Use this as a checklist while you’re in the Smith.ai dashboard. Goal: agents treat every call as a **gate verification**, not office sales intake.

Dashboard: https://app.smith.ai/vr/  
Support: support@smith.ai · (650) 727-6484

---

## 0. Before you click through

Have these ready:

| Item | Example |
|------|---------|
| Business / DBA name | Your LLC — Overnight Gate Attendant |
| Your cell (on-call unlock) | (941) XXX-XXXX |
| Summary email | you@… |
| Time zone | **Eastern Time** |
| First community name | e.g. Oak Haven (or “Pilot HOA”) |
| Unlock method | You unlock in myQ after SMS (Phase 1) |

**Do not** forward the myQ tablet to Smith until you get their **successful test call** summary.

---

## 1. Plan / product choice

| Prefer | Why |
|--------|-----|
| **AI Receptionist** (what you’re testing) | Cheap per call; good for scripted verify → escalate |
| Live Virtual Receptionist later | If AI mishandles noisy gate / edge cases |

For gate access, configure AI as **strict verifier**, not “be helpful and open.”

---

## 2. Business Info (paste these)

### Business name
```
[Your LLC] Overnight Gate Attendant
```

### Business description (≤500 chars)
```
Overnight (8pm–6am ET) virtual gate attendant for FL HOAs on LiftMaster myQ tablets. Visitors without a code tap Call Attendant; call routes here. Verify name + who they’re visiting vs guest list/post orders. If approved, text our on-call to unlock via myQ (or follow unlock SOP)—never open without verification. If denied, tell them to get a myQ guest pass from their host. Log open/deny every call. Noisy outdoor gate audio. Not office sales intake—access control only.
```

### Website
Your site if you have one, or leave blank / Linktree later.

### Address
Your FL business address (or “Serving Manatee & Sarasota Counties, FL”).

### Opening hours (how to think about this)
Smith uses “business hours” for **default vs after-hours instructions**.

**Recommended for gate use:**

- Set **timezone: Eastern**
- Set **working hours = 8:00 PM – 6:00 AM, 7 days**  
  (This is when gate attendant rules apply.)
- Put the **full gate script** in the instructions that run during those hours.

**If the UI forces normal daytime hours instead:**  
Put the gate script in **After-hours instructions** and set office hours to 9–5 *unavailable for transfers*, with a note that **all gate calls are after-hours attendant calls**.  
Or email support: *“All inbound calls are overnight gate attendant calls 8pm–6am ET; please apply gate script to every call.”*

---

## 3. Instructions (≤200 chars if required)

```
8pm-6am ET gate attendant. Verify visitor name + host vs guest list. Approve: text on-call to unlock myQ. Deny: tell them get host guest pass. Never open unverified. Log open/deny. Outdoor noisy call.
```

### Longer instructions (if a bigger box exists — paste in Call Handling / Special instructions)
```
ROLE: Overnight residential gate attendant (myQ tablet calls).
ASK: visitor name; guest/delivery/vendor; resident name or address; did they try a code/pass?
CHECK: guest list / post orders only.
APPROVE: confirm open; SMS on-call with community + visitor + resident + APPROVE; stay on line until gate moves.
DENY: no open; tell them host must add myQ guest pass; they may call back.
NEVER: give codes/passwords; open without verify; argue.
EMERGENCY: tell them to dial 911.
LOG: open / deny / escalate + notes every call.
```

---

## 4. FAQs (for the agent on the phone)

**Q: Can you just open the gate?**  
A: I can only open after I verify your visit. Please give your full name and the resident name or address you’re visiting. If you’re not on the guest list, your host needs to add a myQ guest pass, then you can call back.

**Q: I forgot the code / the resident isn’t answering.**  
A: I can’t give out gate codes. Try your guest pass or code again on the tablet, or have the resident send a myQ guest pass. If you’re on tonight’s guest list, tell me the resident’s name/address and I’ll verify.

**Q: It’s an emergency — open now.**  
A: For police, fire, or medical emergencies, hang up and dial 911. I can’t treat this line as emergency dispatch. For a normal visit, I still need to verify before opening.

---

## 5. Caller types / intake fields (AI Receptionist)

Smith’s default types (new client / existing / sales) don’t match gates. Map like this:

| Smith label | Treat as | Collect | Action |
|-------------|----------|---------|--------|
| Potential new / All other | **Gate visitor** | Name, host name/address, visit type | Verify → SMS you or deny |
| Existing client | **CAM / resident calling ops** | Name + reason | Take message / transfer to you |
| Sales | **Spam** | — | Reject / end call |

**Custom fields to enable (if available):**
1. Community / gate name  
2. Visitor full name  
3. Resident name or address  
4. Visit type (guest / delivery / vendor / other)  
5. Result (Opened / Denied / Escalated)

**Call action after intake:**  
Prefer **Take a message / complete workflow** + **SMS you** — not “book appointment.”  
Disable appointment booking and payments for this use case.

---

## 6. Notifications (critical)

Turn **ON**:
- SMS to your phone on **every call**
- Email call summary / transcript
- Include: visitor name, host, result

**SMS template you want from them (ask support if not configurable):**  
`[Community] [Visitor] visiting [Host] → APPROVE/DENY/ESCALATE`

Your reply workflow (Phase 1):  
See SMS → unlock in myQ if APPROVE → optional reply `OPENED` to Smith.

---

## 7. Transfers

- **Warm transfer to you:** only for escalate / equipment failure / CAM  
- **Do not** transfer visitors to random resident cell numbers unless post orders say so  
- Add your cell as the only transfer destination initially  

---

## 8. Spam / blocks

Block or reject:
- Marketing, SEO, solar, “Google Business,” warrantors  
Keep: anything that sounds like a gate / visitor / delivery / “I’m at the entrance”

---

## 9. Greeting

Ask them to use (or record) something like:

> “Thank you for calling the community gate. This is the overnight attendant. How can I help you?”

Not: “Thanks for calling [sales company], how can I direct your call?”

---

## 10. Test sequence (before myQ)

1. Wait for Smith’s **setup complete + test summary** email/SMS  
2. Call the **Smith number from your cell** (simulate visitor)  
3. Walk the script: give fake visitor + host  
4. Confirm you get SMS/email with notes  
5. Practice deny path once  
6. Practice approve → you unlock (dry run without live gate is fine)

Only then: dealer points tablet Call Attendant → Smith number for 8pm–6am.

---

## 11. First live night checklist

- [ ] Guest list for tonight loaded (sheet or email to yourself)  
- [ ] myQ unlock works from your phone  
- [ ] You are on-call 8pm–6am  
- [ ] Smith hours/instructions match gate script  
- [ ] One intentional test call from the **physical tablet** after hours  
- [ ] CAM has your emergency cell  

---

## 12. Message to send Smith.ai support (copy/paste)

```
Hi Smith.ai team — we use your AI/receptionist line as an overnight residential GATE ATTENDANT (not office sales).

Calls come from LiftMaster myQ Community gate tablets (outdoor noisy audio), 8pm–6am Eastern only.

Please configure:
1) Greeting as overnight gate attendant
2) Always collect: visitor name, resident name/address, visit type
3) Never open/authorize without verification; on approve, SMS my on-call number to unlock via myQ
4) On deny: tell caller to get a myQ guest pass from their host
5) Disable appointment booking/payments
6) Treat sales/spam as reject
7) SMS + email me every call summary with open/deny result

On-call unlock number: [YOUR CELL]
Email for summaries: [YOUR EMAIL]
```

---

## 13. Common mistakes to avoid

| Mistake | Fix |
|---------|-----|
| Leaving default “law firm / sales” intake | Overwrite with gate script |
| 9–5 business hours only | Align hours to **8pm–6am** attendant window |
| Letting AI “be helpful” and invent approval | Hard rule: never open unverified |
| Forwarding myQ before Smith test passes | Wait for their test summary |
| No SMS to you | You won’t unlock in time |

---

When your dashboard shows the fields you’re stuck on, tell me the **exact labels on screen** (Business Info, Instructions, Caller Types, etc.) and I’ll give click-by-click answers for that page only.
