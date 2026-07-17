# Vendor Portal — Complete Build Breakdown

**Goal:** Ship a working vendor portal so dispatch can assign today’s tech and send a time-bound gate code — without CAM knowing every driver.  
**Depends on:** CAM can authorize companies first (portal alone is useless).  
**Related:** [VENDOR-PORTAL.md](VENDOR-PORTAL.md) · [VENDOR-CONTACTS.md](VENDOR-CONTACTS.md) · [PRODUCT.md](PRODUCT.md) · [GATE-SECURITY.md](GATE-SECURITY.md)

This is the full path from “idea” → pilot → production. Do **not** start coding the portal UI before Phase 0–1 foundations exist.

---

## Big picture (dependency order)

```text
Phase 0  Decide + entity/accounts
    ↓
Phase 1  Credential engine (mint code + SMS + log)     ← shared brain
    ↓
Phase 2  CAM Access Desk (authorize companies)         ← portal food
    ↓
Phase 3  Vendor Portal MVP (assign tech + send)        ← this product
    ↓
Phase 4  Wire real gate codes (myQ / CAP)
    ↓
Phase 5  Tie AI fallback to same proof codes
    ↓
Phase 6  Pilot with 1 HOA + 1–2 vendors
    ↓
Phase 7  Harden + Phase-2 portal features
    ↓
Phase 8  Scale (multi-HOA vendors, billing, integrations)
```

The portal is **Phase 3**. Everything before it is load-bearing.

---

## Phase 0 — Decisions & setup (before code)

### Product decisions (lock these)

| # | Decision | Recommendation |
|---|----------|----------------|
| 0.1 | Magic link vs password | **Magic link** (email) for MVP |
| 0.2 | One shared dispatch login vs named users | **Shared OK** for pilot; named later |
| 0.3 | One daily code per company×community vs per-tech code | **One daily code per company×community**; SMS can go to multiple techs |
| 0.4 | Same digits for keypad + AI proof PIN? | **Yes** for MVP simplicity |
| 0.5 | SMS only or SMS + email? | **SMS required**; email copy to dispatch optional |
| 0.6 | Who creates the actual gate credential? | MVP: We Lift–issued code CAM/dealer programs **or** myQ guest pass; Target: **myQ API** |

### Business / ops setup

| # | Step | Done looks like |
|---|------|-----------------|
| 0.7 | FL LLC + EIN (before paid) | Sunbiz doc # |
| 0.8 | Twilio account (SMS delivery) | Can send test SMS |
| 0.9 | Domain for app (`app.welift…` or similar) | DNS ready |
| 0.10 | Pick pilot HOA + 1 multi-crew vendor willing to try portal | Names committed |
| 0.11 | Confirm with dealer how temp vendor codes / myQ guest passes work at that CAP | Written notes |

### Stack recommendation (engineering)

| Layer | Choice |
|-------|--------|
| App | Next.js (App Router) on Vercel — CAM Desk + Vendor Portal same app, role-gated |
| Auth | Magic link (Clerk, Auth.js, or Supabase Auth) |
| DB | Postgres (Neon / Supabase) |
| SMS | Twilio |
| Jobs | Cron / Inngest for “morning code rotate” later |
| Existing | Keep FastAPI Retell webhook; call shared credential APIs |

---

## Phase 1 — Credential engine (shared backend)

**Why first:** Both CAM “send to owner phone” and Vendor Portal “send to tech phone” call the same service.

### Data model (minimum tables)

```text
organizations          # We Lift customers (management cos) — optional early
communities            # The Inlets, …
vendor_companies       # GreenSide Lawn, …
community_vendors      # join: community ↔ company, windows, status
vendor_users           # portal logins (email) ↔ vendor_company
crew_members           # optional favorites: name, phone, company_id
credentials            # minted codes: community_id, company_id, code_hash,
                       # valid_from, valid_until, status
credential_deliveries  # SMS/email log: to_phone, masked, sent_at, actor_user_id
audit_events           # everything else
```

**Never store plaintext codes long-term in logs** — store hash + last-4 for display; show full code only at send time / to authorized roles if needed.

### API / service functions

| Function | Behavior |
|----------|----------|
| `authorize_vendor(community, company, window)` | CAM-only |
| `invite_vendor_user(company, email)` | Creates portal access |
| `mint_credential(community, company, window)` | Creates/rotates today’s code |
| `send_credential_sms(credential, phone, actor)` | Twilio send + delivery log |
| `revoke_vendor(community, company)` | Kill switch — invalidates codes + portal send |
| `verify_proof(community, company, proof_code)` | Used later by AI webhook |

### Steps to complete Phase 1

1. Create Postgres schema + migrations  
2. Implement mint (crypto-random 6-digit or myQ-compatible format)  
3. Implement Twilio SMS template  
4. CLI or admin script: mint + SMS to your phone  
5. Unit tests: window enforcement, revoke, rate limit  
6. **Do not build UI yet** until this is boringly reliable  

**Exit criteria:** You can mint a code and receive it on a real phone in &lt;5 seconds, with an audit row.

---

## Phase 2 — CAM Access Desk (authorization UI)

Portal food. Without this, vendors have nothing to see.

### CAM screens (MVP)

1. **Community home** — The Inlets  
2. **Vendors list** — company, window, status, last code sent  
3. **Add vendor** — name, access contact (owner/dispatch phone + invite email), schedule  
4. **Invite to portal** — sends magic link to dispatch email  
5. **Revoke** — one click  
6. **Audit** — codes issued, AI opens/denies (later)

### Steps to complete Phase 2

1. Auth for CAM users (separate role from vendor)  
2. CRUD `community_vendors`  
3. Invite flow → `vendor_users`  
4. Manual “Send code to access contact” button (SMB path without portal)  
5. Seed The Inlets + 2–3 fake vendors in staging  

**Exit criteria:** CAM adds GreenSide, invites `gates@greenside.com`, can revoke them.

---

## Phase 3 — Vendor Portal MVP (the product you like)

### Screens to build (only these)

| Screen | Must have |
|--------|-----------|
| Magic-link login | Email → link → session |
| Today | List authorized communities + status |
| Assign & send | Tech phone, optional name, Send |
| Confirmation | “Sent to ···0199” + last-4 of code optional |
| History (simple) | Last 20 sends for this company |

Explicitly **out of MVP:** native app, crew roster, Jobber sync, tech self-serve, billing UI.

### Step-by-step build list

#### 3A — Auth & tenancy
1. Magic link login  
2. Session includes `vendor_company_id`  
3. Middleware: vendor user **cannot** see other companies or CAM routes  
4. Invite acceptance: first login binds email → company  

#### 3B — Today feed
5. Query communities where `community_vendors.status = active` and window includes today  
6. Show window, “needs assignment” vs “code sent at HH:MM → ···1234”  
7. Empty state: “Your company isn’t on any community yet — ask the CAM”  

#### 3C — Send code action
8. Form validation (E.164 phone)  
9. Server action: check authorization + window → mint (or reuse today’s credential) → SMS → log  
10. Rate limit: e.g. max 10 sends / company / community / hour  
11. Idempotency: resend same day’s code to new phone without minting forever  
12. Error states: revoked, outside window, Twilio failure  

#### 3D — Mobile UX
13. Mobile-first layout (dispatch is on a phone)  
14. Big tap targets; one primary button  
15. Works on Safari iOS / Chrome Android  

#### 3E — Observability
16. Structured logs + basic dashboard (sends success/fail)  
17. Admin ability to look up delivery by community (support)  

**Exit criteria:** Dispatch on mobile sends code to a tech phone in under 30 seconds end-to-end.

---

## Phase 4 — Make the code open the real gate

Without this, SMS is theater.

### Path A — myQ guest pass (preferred)

| Step | Detail |
|------|--------|
| 4.1 | myQ Partner API access |
| 4.2 | On mint/send: create time-bound guest pass / PIN for facility |
| 4.3 | SMS contains that PIN  
| 4.4 | Pass auto-expires with window |
| 4.5 | On revoke: delete/disable pass via API |

### Path B — CAP vendor code slot (dealer-assisted MVP)

| Step | Detail |
|------|--------|
| 4.1b | Dealer programs temporary vendor code capacity |
| 4.2b | We Lift issues codes that match agreed format |
| 4.3b | CAM/dealer sync process documented (manual at first) |
| 4.4b | Replace with Path A when API lands |

### Steps to complete Phase 4

1. Pedestal test: SMS code → keypad → barrier moves  
2. Expiry test: after window, code fails  
3. Revoke test: CAM revoke → code dead  
4. Document dealer runbook  

**Exit criteria:** Real truck or test user enters The Inlets on a We Lift–issued code **with no AI call**.

---

## Phase 5 — AI Call Attendant uses the same proof

| Step | Detail |
|------|--------|
| 5.1 | Webhook `check_guest_list` / `verify_access` accepts `proof_code` |
| 5.2 | Looks up active credential for company + community |
| 5.3 | Approve only if proof matches + window OK |
| 5.4 | Prompt: vendors must give company + PIN  
| 5.5 | SMS template includes “If keypad fails, Call Attendant + this PIN” |
| 5.6 | Portal shows today’s PIN to dispatch (so they can read it to a stuck tech) |

**Exit criteria:** “Forgot code” path works with PIN; name-only is denied.

---

## Phase 6 — Pilot (prove the loop)

### Pilot cast
- 1 HOA (The Inlets)  
- 1 CAM user  
- 1 SMB vendor (owner phone, no portal needed)  
- 1 multi-crew vendor (portal dispatch)  

### Pilot script (week)

| Day | Activity |
|-----|----------|
| Mon | CAM adds both vendors; invite portal user |
| Tue | Dispatch sends code to tech; tech uses keypad |
| Wed | Intentionally test AI fallback with PIN |
| Thu | Revoke test / wrong-day deny |
| Fri | Review audit with CAM; capture quotes for case study |

### Success metrics

| Metric | Target |
|--------|--------|
| Keypad entries via We Lift code | ≥ 3 |
| AI calls | ≤ keypad entries (ideally near 0 for standing vendors) |
| Dispatch time to send | &lt; 1 minute |
| Wrong-admit via AI | 0 |
| CAM would renew | Verbal yes / written interest |

---

## Phase 7 — Harden & Phase-2 portal features

Only after pilot love:

1. Saved **crew roster** (favorites)  
2. Resend / reassign UI polish  
3. Named dispatcher accounts + permissions  
4. Morning digest email: “Your HOAs today”  
5. Failed SMS alerts to dispatch  
6. CAM weekly PDF for board  
7. Burn-after-N-uses optional  
8. Stronger rate limits + anomaly alerts (send to weird area codes)  

---

## Phase 8 — Scale

1. Multi-community vendors (one login, many HOAs) — already designed, load-test it  
2. Billing: platform fee + SMS pack + AI overage  
3. Jobber / ServiceTitan: job at The Inlets → deep link “Send gate code”  
4. White-label for large CAM firms  
5. SOC2-ish basics if enterprise CAMs ask  

---

## Workstream checklist (everything, by function)

### Engineering
- [ ] DB schema + migrations  
- [ ] Credential mint/revoke/verify service  
- [ ] Twilio SMS  
- [ ] CAM Desk MVP  
- [ ] Vendor Portal MVP  
- [ ] Role-based auth  
- [ ] Retell webhook proof_code  
- [ ] myQ API integration  
- [ ] Deploy (Vercel + webhook host)  
- [ ] Staging + prod environments  
- [ ] Tests + smoke scripts  

### Design / UX
- [ ] CAM Desk wireframes  
- [ ] Vendor Portal mobile wireframes (Today + Send)  
- [ ] SMS copy (clear, short, brand)  
- [ ] Empty/error states  

### Partnerships
- [ ] myQ Partner application  
- [ ] LiftMaster dealer for pilot site  
- [ ] Pilot CAM agreement (soft LOE)  
- [ ] Pilot vendor (dispatch champion)  

### Compliance / trust
- [ ] LLC + insurance path for paid  
- [ ] Data retention policy (phones, logs)  
- [ ] Terms: vendor responsible for forwarding codes  
- [ ] Incident runbook (leaked code)  

### Go-to-market
- [ ] CAM pitch (Access Desk)  
- [ ] Vendor pitch (Portal — 30 sec)  
- [ ] Demo video: assign → SMS → keypad  
- [ ] Pricing aligned to SMS-primary economics  

---

## Suggested calendar (effort, not calendar promises)

Order of attack for a small team / solo + agents:

| Block | Focus |
|-------|--------|
| **1** | Phase 1 credential engine + Twilio |
| **2** | Phase 2 CAM Desk MVP |
| **3** | Phase 3 Vendor Portal MVP |
| **4** | Phase 4 real gate open (dealer or myQ) |
| **5** | Phase 5 AI proof wiring |
| **6** | Phase 6 live pilot week |

Do not parallelize portal UI with zero credential backend — you’ll demo a button that texts fake numbers.

---

## Definition of “vendor portal complete”

**Complete for pilot** means all true:

1. CAM authorized company + invited dispatch  
2. Dispatch logs in on phone  
3. Sees The Inlets as allowed today  
4. Sends code to tech cell  
5. Tech opens gate on keypad with that code  
6. Audit shows who sent what when  
7. AI fallback accepts same proof if needed  
8. CAM can revoke and kill access  

**Complete for product** adds: myQ-native credentials, crew roster, multi-HOA polish, billing, and a second CAM logo.

---

## What to build next (single next action)

**Start Phase 1:** credential engine + Twilio SMS in this repo (shared service), with a tiny admin script — then CAM Desk, then Vendor Portal UI.

When you say go, we implement Phase 1 in code.
