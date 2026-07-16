# Gate Security — Authorization, Codes, AI Fallback

**Product:** We Lift Vendor Access Desk + AI Call Attendant backup  
**Thesis:** [PRODUCT.md](PRODUCT.md)  
**Goal:** Easy for CAM/vendors; hard to spoof; minimize AI minutes  

---

## Preferred model (Lucas — Jul 16)

```text
CAM approves companies + one access contact each (owner or dispatch)
  → We Lift auto-SMS time-bound gate codes to that contact
  → SMB: owner uses code / Big firm: dispatch forwards to today's tech
  → Keypad entry (no AI cost)
  → AI Call Attendant only if no/lost code + proof required
```

**Who gets the SMS?** Not “whoever might drive up.” See [VENDOR-CONTACTS.md](VENDOR-CONTACTS.md).

Twilio = **credential delivery** to the company access contact.  
Retell = **rare fallback**.  
myQ API = mint guest pass / temp code + remote unlock for AI path.

---

## 1. Authorization vs authentication

| Layer | Question | How We Lift answers |
|-------|----------|---------------------|
| **Authorization** | Is this vendor allowed? | CAM roster |
| **Authentication (happy path)** | Is this the real vendor crew? | Code sent to **registered phone** |
| **Authentication (AI fallback)** | Same, without keypad | Visit PIN / WO# + list match — never name alone |
| **Context** | Allowed now / here? | Schedule window + address |

---

## 2. CAM Access Desk (ease)

CAM enters:

- Company (GreenSide Lawn, …)  
- Phone(s)  
- Window (standing schedule or one-off)  
- Optional crew names / job address  

On save → system **issues credential + SMS**. CAM does not babysit the gate.

Real estate showings: same flow — agent phone gets a windowed code / PIN.

---

## 3. Why SMS codes beat AI-for-every-vendor

| | Auto code SMS | AI every time |
|--|---------------|---------------|
| Cost | Pennies | Retell $/min |
| Spoof resistance | Phone must receive SMS | Voice claim weak without PIN |
| Vendor UX | Familiar keypad | Extra call in the sun |
| CAM UX | Approve once | Still need a list anyway |

AI remains valuable for: lost code, subcontractor not texted, after-hours one-off, wrong day education (“your window is Tue–Thu”).

---

## 4. Code hygiene

| Do | Don’t |
|----|--------|
| Rotate daily or per window | Eternal shared vendor code |
| SMS only roster numbers | Paper list in the clubhouse |
| Expire with window | 24/7 code for daytime-only vendor |
| Log issue / revoke | One code for all trades forever |
| AI asks for proof if they skip keypad | AI opens on “I’m with X” |

---

## 5. AI fallback rules

Open only if:

1. On roster (or valid one-off)  
2. Inside window  
3. **Proof** (spoken PIN issued with the SMS, or WO#)  
4. myQ unlock OK  

Deny: wrong/missing proof, outside window, claims resident (→ sticker/code), emergency claim (→ 911).

---

## 6. Build order

1. Roster + SMS of time-bound codes (even manual myQ pass + Twilio text as MVP)  
2. AI fallback with required `proof_code`  
3. myQ API: create guest pass / temp code automatically  
4. Optional: burn code after first use; failed-PIN lockout  

---

## 7. Open questions

1. Daily rotate for standing vendors vs weekly?  
2. SMS to dispatch only, or each tech’s phone?  
3. Same digits for keypad and AI proof PIN, or separate?  
4. myQ native guest pass vs CAP vendor code slot (dealer-dependent)?
