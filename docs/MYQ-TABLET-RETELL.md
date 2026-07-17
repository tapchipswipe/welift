# myQ tablet → Call Attendant → Retell

**Goal:** Pedestal **Call Attendant** dials the We Lift Retell DID so the AI receptionist can verify (company + proof PIN) and unlock.

**Product surfaces:** CAM desk [`/access`](../webhook/static/access.html) · Visitor UX [`/gate`](../webhook/static/gate.html)

---

## One sentence

The physical myQ / LiftMaster tablet does not run our code — it **forwards Call Attendant** to a phone number. That number must be your **Retell agent DID**.

---

## Checklist

### A. Retell agent ready

- [ ] Webhook on stable HTTPS ([webhook/DEPLOY.md](../webhook/DEPLOY.md))
- [ ] `SIMULATE_MYQ_OPEN=true` until Partner API; later set `MYQ_*` and turn simulate off
- [ ] Push agent:

```bash
cd webhook && source .venv/bin/activate
python ../scripts/create_agent.py --webhook-base https://YOUR_HOST --community "The Inlets"
```

- [ ] Buy/assign Retell DID → set `RETELL_DID=+1…` in env
- [ ] Cell-test acceptance ([PRODUCT-ACCEPTANCE.md](PRODUCT-ACCEPTANCE.md)):
  - Vendor + correct PIN → approve → open (simulate)
  - Wrong PIN → deny
  - Resident claim → redirect, no open

### B. Point the tablet

Same pattern as historical Smith wiring ([01-metro-validation/how-to-connect-myq-to-smith.md](../01-metro-validation/how-to-connect-myq-to-smith.md)):

1. myQ Community / dealer admin → Call Attendant / overnight / quick-call destination  
2. Set number = **Retell DID** (E.164)  
3. Prefer overnight window first (e.g. 8pm–6am) for controlled tests  
4. CAM + dealer present for first pedestal call  

### C. Pedestal acceptance

- [ ] Tap Call Attendant on tablet → hears We Lift greeting  
- [ ] Speak company + PIN from Access Desk SMS → gate opens (or simulate confirmed in logs)  
- [ ] Wrong PIN → clean deny; no open  

---

## What `/gate` is

Product visitor UX mirroring the pedestal: keypad reminder + Call Attendant → Retell.  
It does **not** replace the metal tablet. Use it for walkthroughs and to display `RETELL_DID` (`tel:` link).

---

## Failures

| Issue | Fix |
|-------|-----|
| Tablet rings wrong number | DID not assigned / wrong community config |
| Retell tools 404 | Webhook base URL stale — re-run `create_agent.py` |
| Approve but no motion | Still on simulate, or `MYQ_*` wrong — see [GATE-CODE-RUNBOOK.md](GATE-CODE-RUNBOOK.md) |
| Opens on company name alone | Prompt/tools out of date — vendors **must** send `proof_code` |
