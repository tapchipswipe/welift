# Annual Operational Expenses (OPEX) Analysis

This document details all fixed, indirect annual operating expenses (OPEX) required to run **We Lift**, excluding variable per-call costs (telephony minutes, SMS, and Retell AI voice).

---

## 📋 Itemized Annual OPEX Comparison (Modeled for 10 Gates)

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           ANNUAL OPEX COMPARISON (10 GATES)                              │
├──────────────────────────────────────┬────────────────────────┬──────────────────────────┤
│ Expense Category                     │ CURRENT SETUP          │ UPGRADED SETUP           │
├──────────────────────────────────────┼────────────────────────┼──────────────────────────┤
│ Core Compute Server / Hosting        │ $ 240.00 / yr (Vercel) │ $  66.00 / yr (Hetzner)  │
│ Database Hosting                     │ $ 228.00 / yr (Neon)   │ $   0.00 / yr (On VPS)   │
│ Vercel Pro Account (Frontend Only)   │ $   0.00 (In Core)     │ $ 240.00 / yr            │
│ Inbound Gate Phone Numbers (DIDs)    │ $ 138.00 / yr (Twilio) │ $ 120.00 / yr (Telnyx)   │
│ Clerk Authentication (Free Tier)     │ $   0.00 / yr          │ $   0.00 / yr            │
│ E&O / General Liability Insurance    │ $1,200.00 / yr          │ $1,200.00 / yr          │
│ LLC Taxes, Filings & Domains         │ $ 200.00 / yr          │ $ 200.00 / yr            │
├──────────────────────────────────────┼────────────────────────┼──────────────────────────┤
│ TOTAL ANNUAL OPEX (10 Gates)         │ $2,006.00 / year       │ $1,826.00 / year         │
└──────────────────────────────────────┴────────────────────────┴──────────────────────────┘
```

---

## 📈 OPEX Scaling to 50 Gates

As the business scales from 10 to 50 contracted gates:

### Current Setup (50 Gates)
* **Vercel Pro Account:** $240 / year
* **Neon Serverless Database (Scale Tier):** $960 / year ($80/mo)
* **Twilio Inbound Phone Numbers (50 DIDs):** $690 / year ($1.15/mo per DID)
* **E&O Insurance & Legal:** $1,339 / year
* **Total Current Annual OPEX (50 Gates):** **$3,229 / year**

### Upgraded Setup (50 Gates)
* **Hetzner Dedicated VPS (2 vCPU / 4GB RAM):** **$66 / year** ($5.50/mo total — a single $5.50 VPS handles 50+ PostgreSQL databases with ease)
* **Vercel Pro (Frontend Portal Only):** $240 / year
* **Telnyx Inbound Phone Numbers (50 DIDs):** **$600 / year** ($1.00/mo per DID)
* **E&O Insurance & Legal:** $1,339 / year
* **Total Upgraded Annual OPEX (50 Gates):** **$2,245 / year**

---

## 💡 Key Takeaways

1. **Ultra-Low Fixed Cost Floor:** Fixed company expenses under the upgraded setup are only **~$152 / month** for 10 gates.
2. **Database Overhead Eliminated:** Self-hosting PostgreSQL on a $5.50/mo Hetzner VPS reduces database hosting costs to **$0.00** as you add dozens of new HOAs.
3. **High Net Profit Conversion:** Over 90% of all gross revenues convert straight into net EBITDA.
