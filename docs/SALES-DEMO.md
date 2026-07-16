# Sales walkthrough (uses the real product)

This is **not** a throwaway demo app. Use the real CAM desk + Retell.

Full pass/fail: [PRODUCT-ACCEPTANCE.md](PRODUCT-ACCEPTANCE.md) · Tablet: [MYQ-TABLET-RETELL.md](MYQ-TABLET-RETELL.md)

## 5-minute room walkthrough

1. Open `/access` — “CAM authorizes vendors; we text codes so they don’t burn AI minutes.”
2. Show GreenSide as **dispatch** vs a solo plumber as **owner**.
3. Send today’s code → phone buzzes (or on-screen if Twilio unset).
4. “Driver uses the keypad — primary path.”
5. Open `/gate` — “If they forget: Call Attendant.”
6. Call Retell DID → company + PIN from SMS → approve / simulate open; wrong PIN → deny.
7. Ask for dealer contact to point tablet Call Attendant at that DID.

## Setup

```bash
cd webhook && ./run.sh
# https://HOST/access  https://HOST/gate
python scripts/create_agent.py --webhook-base https://HOST
```
