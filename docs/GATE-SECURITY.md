# Gate Security Brainstorm — Who Gets In, and How We Know

**Product:** We Lift vendor Call Attendant (autonomous)  
**Constraint:** Voice at the myQ tablet; no overnight human; residents keep codes/stickers  
**Goal:** Easy authorization for the right people + hard spoofing for fakes  

---

## 1. The trust problem in one line

Anyone can *say* “I’m with GreenSide Lawn.”  
The AI must require **something a random walker can’t invent in 10 seconds.**

| Layer | Question |
|-------|----------|
| **Authorization** | Is this company/person allowed *at all*? |
| **Authentication** | Is *this* caller actually that company/person? |
| **Context** | Are they allowed *here / now*? |

Voice name-match alone = authorization without authentication. That’s the hole.

---

## 2. Make authorization easy (ops UX)

Different roles need different “easy.”

### A) CAM / board (source of truth)

| Pattern | How it works | Ease | Security |
|---------|--------------|------|----------|
| **Vendor roster** | Company name, optional crew names, phone, days/hours | High | Medium alone |
| **Standing vendors** | Lawn/pool/pest on a recurring schedule window | High | Higher with windows |
| **One-off work order** | Address + date + company + optional PIN | Medium | High |
| **Real estate showing desk** | Brokerage + agent name + listing address + window | Medium | High with proof |

**Ease win:** One shared **Vendor & Access Desk** (web form or even Airtable/Notion → syncs to `guest-list.json`):

- Add vendor company  
- Toggle active / schedule  
- Issue **today’s visit PIN** (auto-generated)  
- Add “showing: 123 Oak, 2–4pm, Agent Jane, PIN 4821”

CAM should never edit raw JSON.

### B) Residents (social guests & their own contractors)

Don’t invent a second system. Push them to **myQ guest passes** (already familiar).  
We Lift only catches people who *can’t* or *won’t* use that.

### C) Vendor companies (dispatch)

| Pattern | Ease for vendor |
|---------|-----------------|
| Standing company on roster + **daily crew PIN** texted to dispatch | High |
| Dispatcher enters “Mike on site 9–11 at clubhouse” in a 30-sec form | Medium |
| Each tech gets a myQ guest pass from CAM | High for HOA, medium for vendor |

### D) Real estate agents

Treat as a **special vendor class**, not “trust the name”:

1. Brokerage on approved list **or** listing tied to a unit  
2. Showing window (start/end)  
3. Proof: **showing PIN** or **last 4 of lockbox / MLS** that CAM/listing agent set  

Cold-call “I’m the realtor” with no PIN → **deny**.

---

## 3. Proof factors the AI can check (voice-friendly)

Pick factors that work **over a noisy outdoor tablet** — no app install required for v1.

| Proof | What caller must provide | Spoof difficulty | Friction |
|-------|--------------------------|------------------|----------|
| **Visit PIN** (4–6 digits, time-bound) | “My code is 4821” | High if rotated | Low |
| **Company + PIN** | Name + company + PIN | High | Low |
| **Scheduled window only** | Must call during booked slot | Medium | Low |
| **Work order / ticket #** | Matches CAM entry | Medium–high | Low |
| **Callback to known dispatch #** | AI/system dials company; they confirm truck | Very high | Medium |
| **myQ guest pass** (preferred when possible) | Already on tablet | Very high | Low for guest |
| **License plate last 3** on list | Spoken plate fragment | Medium | Low |
| **Photo of badge / WO** (later) | Tablet camera / MMS | High | Higher |
| **Video face match** (later) | Out of scope for now | — | — |

**Best v1 combo for We Lift:**  
**Authorized company (or agent) on list + time window + visit PIN.**  
Name alone never opens.

---

## 4. Recommended policy (concrete)

### Open only if **all** true

1. **Identity claim** matches a list entry (company and/or person)  
2. **Visit type** allowed (vendor / showing / delivery — not “resident”)  
3. **Time window** active (or standing “Mon–Fri 7am–6pm” for that vendor)  
4. **Proof:** correct **visit PIN** (or work-order # if PIN not used)  
5. myQ unlock succeeds  

### Always deny if

- Company not on list  
- PIN wrong / expired / already used (one-time PINs)  
- Outside window  
- Claims “resident” → redirect to code/sticker  
- Claims emergency → 911, no open  
- Multiple failed PIN attempts → lock that call + log  

### Real estate specifically

```text
Agent: name + brokerage + listing address + showing PIN
List entry: type=showing, address, window, pin_hash, brokerage
Match all → open once → optional burn PIN
```

### Vendors specifically

```text
Standing: GreenSide Lawn | Mon–Fri 07:00–18:00 | daily_pin=rotated
OR one-off: Acme Plumbing | 12 Oak | today 09:00–12:00 | pin=3910 | WO#8842
Caller must say company + PIN (+ address if one-off)
```

---

## 5. How the AI agent uses this (tool shape)

Evolve `check_guest_list` → effectively `verify_access`:

```text
inputs:
  visitor_name
  company_name          # vendor / brokerage
  host_name_or_address  # unit / common areas / listing
  visit_type            # vendor | showing | delivery | guest
  proof_code            # PIN or WO#  ← NEW, required for vendor/showing
  claimed_window        # optional

logic:
  find candidate entries
  if none → deny
  if outside valid_from/valid_until → deny
  if proof_code missing → ask once, then deny
  if proof_code != entry.pin → deny (log attempt)
  else → approve → open_gate
```

Prompt rule: **Never call open_gate without a successful proof check.**

---

## 6. Making PINs easy (so people actually use them)

Friction kills security if CAM won’t issue codes.

| Approach | Who gets the PIN | Rotation |
|----------|------------------|----------|
| **Daily vendor PIN** | Texted to company dispatch each morning | Daily |
| **Per-visit PIN** | Created when CAM adds a one-off job | Single use or end-of-window |
| **Showing PIN** | Listing agent / CAM when booking showing | Per showing |
| **Standing + long PIN** | Weak — avoid for months-long static PINs | Prefer rotate |

Implementation options (light → heavy):

1. CAM web form generates PIN, SMS/email to vendor contact  
2. Twilio (or email) only for **PIN delivery to vendors** — not for waking Lucas to open  
3. Later: vendor dispatch login to mint a same-day crew PIN  

Note: Twilio here is **credential delivery**, not “human unlock.” Different job.

---

## 7. Defense in depth (practical tiers)

| Tier | When | What |
|------|------|------|
| **Tier 0 — now** | Before API even | Deny without list match; no resident opens; log everything |
| **Tier 1 — pilot** | First live HOA | List + **time window** + **visit PIN** required for vendor/showing |
| **Tier 2 — harden** | After spoof attempt or scale | One-time PINs; attempt lockout; plate fragment; burn-after-open |
| **Tier 3 — later** | If needed | Dispatch callback; badge photo; LPR; video audit (still not sole auth unless strong) |

Don’t jump to Tier 3 for The Inlets. Tier 1 solves “anybody can say they’re the gardener.”

---

## 8. What we explicitly won’t rely on

| Weak control | Why it fails |
|--------------|--------------|
| Name only | Trivial spoof |
| Company name only | Trivial spoof |
| “Resident said it’s OK” via voice | Unverifiable overnight |
| Forever-shared vendor gate code | Your whole product exists to replace this |
| AI “vibes” / confidence from chatty speech | Not authentication |

---

## 9. Ease checklist by persona

| Persona | Happy path |
|---------|------------|
| **CAM** | Add vendor or showing in 60 seconds; auto PIN; optional SMS to vendor |
| **Lawn company** | Morning text: “Inlets PIN today 4821”; tech says company + PIN at gate |
| **Realtor** | Showing booked → PIN on calendar invite; says address + PIN at gate |
| **Resident** | Never talks to AI; uses sticker/code or myQ pass for guests |
| **Board** | Monthly PDF: opens, denies, failed PIN attempts |

---

## 10. Recommendation for We Lift (lockable decision)

**Adopt Tier 1 as product security baseline:**

1. Authorization = CAM-maintained roster (vendors, showings, one-offs)  
2. Authentication = **time-bound visit PIN** (or WO#) spoken to the agent  
3. Context = address/common area + active window  
4. Autonomous open only after (1)+(2)+(3)  
5. Wrong PIN → deny; no human override overnight  
6. Prefer myQ guest pass whenever the visit is “social guest,” not vendor  

**Next build steps (when you say go):**

- Extend guest-list schema: `pin`, `pin_expires`, `schedule`, `visit_type: showing`  
- Require `proof_code` in `check_guest_list` for vendor/showing  
- Tiny CAM “Access Desk” (even a secured form) that writes the list + emails/SMS PINs  
- Update Retell prompt: always collect company + PIN for vendors/agents  

---

## Open questions (decide with Lucas / CAM)

1. Daily rotating PIN per company vs per-visit PIN only?  
2. Are real estate showings in v1 or phase 1.5?  
3. Max failed PIN attempts per call before hard stop?  
4. Should successful open burn a one-time PIN immediately?  
5. Is dispatch callback worth the complexity for high-risk communities?
