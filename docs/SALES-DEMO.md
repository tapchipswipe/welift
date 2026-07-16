# Sales Demo Script — We Lift Access Desk (5 minutes)

**Goal:** Live meeting where a phone buzzes with a real gate code, then optional Retell PIN proof.  
**App:** `https://YOUR_HOST/access` · Health: `https://YOUR_HOST/health`

---

## Setup (morning of)

1. Twilio funded; `TWILIO_*` set on deploy  
2. `SIMULATE_MYQ_OPEN=true` until myQ API live  
3. Open `/health` — `twilio_configured: true`, `status: ok`  
4. Two phones charged (yours + “vendor”)  
5. Retell DID pointed at this webhook; prompt from [prompt.md](../prompt.md)  
6. Backup: record one successful Send + call the night before  

Local:

```bash
cd webhook
cp .env.example .env   # fill Twilio + SIMULATE_MYQ_OPEN=true
./run.sh
# open http://127.0.0.1:8080/access
```

CLI alternate:

```bash
python scripts/send_vendor_code.py --company "GreenSide Lawn" --phone +1YOURNUMBER
```

---

## Script (memorize)

1. **“Residents keep stickers and codes. We handle vendors.”**  
2. Open **Access Desk** → The Inlets → **GreenSide Lawn**  
3. Enter their cell (or yours) → **Send today’s gate code**  
4. Phone gets SMS with keypad code + Call Attendant PIN note  
5. **“Driver types that on the keypad — no AI charge.”** (show tablet mockup)  
6. Optional: call Retell → “GreenSide” + read PIN from SMS → AI approves / opens (simulate)  
7. Wrong PIN → clean deny  
8. Ask: dealer of record + soft pilot interest  

---

## If things break

| Issue | Fix |
|-------|-----|
| SMS status `logged` not `sent` | Twilio env missing — still show code on screen |
| Retell 401 | `VERIFY_RETELL_SIGNATURES` / API key |
| ngrok URL changed | Use Railway/Fly stable host — see [webhook/DEPLOY.md](../webhook/DEPLOY.md) |
| Wi‑Fi dies | Play backup recording |

---

## Exit: sales-ready

- [ ] Send → SMS (or on-screen code) in &lt;60s  
- [ ] Retell accepts correct PIN / rejects wrong  
- [ ] Cold run twice without code changes  
- [ ] Backup recording saved  
