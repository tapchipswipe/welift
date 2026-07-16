# Product acceptance — CAM desk + Retell backbone

Not a pitch script. These checks mean the **product** works.

## Preconditions

```bash
cd webhook
cp .env.example .env   # TWILIO_*, RETELL_*, SIMULATE_MYQ_OPEN=true
./run.sh
# public HTTPS for Retell tools — see DEPLOY.md
```

Health: `GET /health` → `status: ok`, `unlock_ready: true`.

---

## 1. CAM Access Desk (`/access`)

| Step | Pass |
|------|------|
| Add SMB vendor (contact **owner**) with phone + window | Appears on roster |
| Add big vendor (contact **dispatch**) | Appears; type pill = dispatch |
| **Send code** with blank override phone | SMS (or log) to roster number; code shown once |
| Resend | Prior code rotated; new code works for proof |
| **Revoke** | Active credential gone; old PIN fails Retell proof |
| Outside window without override | Send rejected |
| Outside window + override | Send succeeds |
| Audit panel | Shows deliveries + active codes |

## 2. Retell AI Call Attendant

| Step | Pass |
|------|------|
| Call Retell DID | Overnight attendant greeting |
| Vendor, no PIN | Asks for proof PIN; does not open |
| Vendor + wrong PIN | Deny |
| Vendor + correct PIN from SMS | Approve → `open_gate` → opened (simulate or myQ) |
| “I’m a resident” | Redirect to keypad/sticker; no open |
| Guest on list (Jordan Lee / Sam Rivera) | Approve without proof PIN |

Push agent: `python scripts/create_agent.py --webhook-base https://HOST`

## 3. Tablet path

See [MYQ-TABLET-RETELL.md](MYQ-TABLET-RETELL.md). `/gate` mirrors visitor UX; metal tablet must dial Retell DID.

## 4. Automated

```bash
cd webhook && source .venv/bin/activate
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_credentials.py
SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false python test_tools.py
```
