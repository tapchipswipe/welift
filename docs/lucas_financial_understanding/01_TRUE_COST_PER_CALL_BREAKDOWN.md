# True Cost Per Call Breakdown (Now vs. Upgraded)

This document details the exact side-by-side cost per visitor call based on a standard **45-second gate interaction** (0.75 minutes).

---

## 📊 True Cost Per Call Matrix

| Component | Current Stack (Retell + Vercel/Neon + Twilio) | Upgraded Stack (Direct LiveKit + Hetzner + Telnyx) | Cost Variance ($) | Cost Variance (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Voice AI Engine** | **$0.06000** (Retell AI @ $0.080/min) | **$0.00785** (Deepgram + Groq + Cartesia) | -$0.05215 | **-86.9%** |
| **SIP Telephony Inbound** | **$0.00638** (Twilio SIP @ $0.0085/min) | **$0.00263** (Telnyx SIP @ $0.0035/min) | -$0.00375 | **-58.8%** |
| **SMS Credential Dispatch** | **$0.00790** (Twilio SMS @ $0.0079/msg) | **$0.00400** (Telnyx SMS @ $0.0040/msg) | -$0.00390 | **-49.4%** |
| **Server & Database Compute** | **$0.00600** (Vercel Edge + Neon DB) | **$0.00020** (Hetzner VPS + Cloudflare) | -$0.00580 | **-96.7%** |
| **TOTAL COST PER CALL** | **$0.08028 / call** (~8.0 cents) | **$0.01468 / call** (~1.5 cents) | **-$0.06560** | **-81.7%** |

---

## 🔬 Component Math Details

### 1. Current Stack Breakdown ($0.0803 / Call)
* **Retell Voice AI:** 0.75 mins × $0.0800 / min = **$0.0600**
* **Twilio Inbound SIP:** 0.75 mins × $0.0085 / min = **$0.0064**
* **Twilio SMS Dispatch:** 1 SMS × $0.0079 / msg = **$0.0079**
* **Vercel & Neon Infra Allocation:** **$0.0060**
* **Total:** **$0.0803 per call**

### 2. Upgraded Stack Breakdown ($0.0147 / Call)
* **Deepgram Nova-2 (STT):** 0.75 mins × $0.0043 / min = **$0.00323**
* **Groq Llama 3.3 70B (LLM):** ~112 tokens × ($0.59/M in, $0.79/M out) = **$0.00015**
* **Cartesia Sonic (TTS):** 0.75 mins × $0.0060 / min = **$0.00450**
* **Telnyx Inbound SIP:** 0.75 mins × $0.0035 / min = **$0.00263**
* **Telnyx SMS Dispatch:** 1 SMS × $0.0040 / msg = **$0.00400**
* **Hetzner VPS & Cloudflare Allocation:** **$0.00017**
* **Total:** **$0.0147 per call (1.47 cents)**

---

## 📈 Impact on 1,000 Monthly Calls (1 HOA)

* **Current Cost:** 1,000 calls × $0.0803 = **$80.30 / month** ($963.60 / year)
* **Upgraded Cost:** 1,000 calls × $0.0147 = **$14.68 / month** ($176.16 / year)
* **Net Monthly Savings:** **$65.62 / month per community** (an **81.7% cost reduction**)
