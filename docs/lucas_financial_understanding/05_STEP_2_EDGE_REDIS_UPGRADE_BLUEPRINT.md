# Step 2 Technical & Operational Blueprint: Edge + Redis Upgrade

This document is the technical execution blueprint for **Step 2** (scaling from 10 to 100+ communities with **sub-30ms gate unlocks**, **$0.0147/call COGS**, and **98.5% gross profit margins**).

---

## 🏗️ Target Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              STEP 2 TARGET ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. TELEPHONY (Telnyx SIP)                                                              │
│     Inbound Gate Calls ($0.0035/min) & SMS ($0.004/msg)                                │
│         │                                                                               │
│         ▼                                                                               │
│  2. EDGE ROUTING (Cloudflare Workers | $5/mo)                                           │
│     Global V8 Isolates (Sub-10ms Latency | Zero Cold Starts)                            │
│         │                                                                               │
│         ├──► FAST PATH: Upstash Redis Edge Cache (3ms Response) ──► Gate Release        │
│         │                                                                               │
│         └──► SLOW PATH: Postgres DB (Via Cloudflare Hyperdrive)                         │
│         │                                                                               │
│  3. DIRECT VOICE AI PIPELINE (Self-Hosted LiveKit on $5.50 Hetzner VPS)                 │
│     • STT: Deepgram Nova-2 ($0.0043/min)                                                │
│     • LLM: Groq Llama 3.3 70B ($0.0002/min)                                             │
│     • TTS: Cartesia Sonic ($0.0060/min)                                                 │
│                                                                                         │
│  TOTAL COST PER CALL: $0.01468 / CALL  │  TOTAL INFRA: $5.00 / MONTH TOTAL              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 4-Phase Implementation Steps

### Phase 2.1: Telephony Migration (Twilio ➔ Telnyx SIP)
* **Goal:** Cut telephony and SMS costs by **58%**.
* **Action Steps:**
  1. Order DIDs on Telnyx ($1.00/mo per phone number vs. Twilio $1.15/mo).
  2. Configure Telnyx SIP trunks to direct inbound calls to the gate webhook URL (`https://welift-gate.vercel.app/retell/webhook`).
  3. Update `webhook/main.py` and `portal/app/actions.ts` to execute SMS dispatches via Telnyx REST API (`$0.004` per message vs. Twilio `$0.0079`).

---

### Phase 2.2: Edge Caching (Upstash Redis Integration)
* **Goal:** Slash database query response time from **300ms down to 3ms** and eliminate 95% of database queries.
* **Action Steps:**
  1. Provision an Upstash Redis database (native REST API support for Cloudflare Workers).
  2. Update Vendor Portal & CAM Admin write actions (`portal/app/actions.ts`):
     * When a 6-digit gate code or guest entry is created, write it to PostgreSQL **and** push it to Upstash Redis with expiration.
  3. Update `/gate/verify_code` in `webhook/main.py`:
     * Query Redis first. On cache hit, return **Access Granted in 3ms** without touching PostgreSQL.

---

### Phase 2.3: Edge Gateway (Cloudflare Workers + Hyperdrive)
* **Goal:** Eliminate serverless cold starts completely and provide enterprise DDoS protection.
* **Action Steps:**
  1. Deploy a `Cloudflare Worker` (`worker.js`) as the global API Gateway.
  2. Connect Cloudflare **Hyperdrive** to your PostgreSQL database to pool and accelerate SQL queries globally at 300+ edge cities.
  3. Set up custom SSL routing (`gate.welift.com` and `portal.welift.com`).

---

### Phase 2.4: Direct Voice Pipeline (LiveKit / Pipecat Orchestration)
* **Goal:** Cut Voice AI costs from **$0.080/min down to $0.014/min** (an 82.5% reduction).
* **Action Steps:**
  1. Provision a **$5.50/mo Hetzner VPS** (2 vCPU / 4GB RAM running Docker).
  2. Deploy **LiveKit Server** + **LiveKit Agents** framework.
  3. Wire the voice engines:
     * **STT:** Deepgram Nova-2 API key ($0.0043/min).
     * **LLM:** Groq Llama 3.3 70B API key ($0.0002/min, 300ms response time).
     * **TTS:** Cartesia Sonic API key ($0.0060/min).
  4. Point inbound Telnyx SIP calls directly to your LiveKit server.

---

## 📊 Expected Performance & Financial Summary

| Metric | Current Stack (Step 1) | Upgraded Stack (Step 2) | Gain |
| :--- | :--- | :--- | :--- |
| **Gate Unlock Latency** | 300ms – 1,200ms | **3ms – 30ms** | **100x Faster!** |
| **Serverless Cold Starts** | 500ms – 2,000ms | **0ms (Zero Cold Starts)** | **Instant Response** |
| **Cost Per 45s Visitor Call**| $0.0803 / call | **$0.0147 / call** | **81.7% Cost Reduction!** |
| **Monthly Hosting Overhead** | ~$39.00 / month | **$5.00 / month TOTAL** | **87.2% Fixed Cost Savings** |
| **Gross Margin @ $1.00/call** | 92.0% Margin | **98.5% Gross Margin!** | **Maximized Net Cash Flow** |
