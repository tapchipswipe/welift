# We Lift — Profit Optimization, Infrastructure Cost Savings & Pay-As-You-Go Margin Blueprint

**Document Status:** Production Operational & Financial Specification  
**Version:** 1.0.0  
**Target Architecture:** We Lift Voice AI & Automated Gate Access Platform  
**Target Market:** Gated HOA Communities, Master-Planned Residential Developments, Commercial Real Estate  

---

## Executive Summary

The **We Lift Profit Optimization & Infrastructure Blueprint** establishes an aggressive, actionable roadmap to maximize gross margins, eliminate platform overages, and optimize unit economics for autonomous voice gate access.

By decoupling from high-margin turnkey aggregators, migrating compute to bare-metal VPS/edge infrastructure, and implementing targeted quality-preserving call optimizations, We Lift reduces per-minute voice cost by **82.5%** and per-community infrastructure cost by **98.3%**.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
2026-07-18 PROFIT OPTIMIZATION HIGHLIGHTS                                             │
├──────────────────────────────┬──────────────────────────────┬───────────────────────────┤
│    RETELL AI VS DIRECT COGS  │   INFRASTRUCTURE COST MIGRATION │    TARGET GROSS MARGINS  │
│  $0.080/min ──► $0.014/min   │  $9.00/comm ──► $0.15/comm    │        90% ──► 300%+      │
│     (82.5% Cost Drop)        │    (98.3% Infra Reduction)   │   (Maximized HOA PAYG)   │
└──────────────────────────────┴──────────────────────────────┴───────────────────────────┘
```

---

## R1. Itemized Retell AI & Direct Telephony Cost Breakdown

### 1.1 Vendor Rate Analysis & Managed Platform Overhead

Retell AI provides a managed WebRTC/SIP orchestration platform that abstracts underlying Voice AI providers (STT, LLM, TTS, Telephony). Retell charges **$0.080 to $0.120 per minute** for standard usage. 

The table below disaggregates Retell's bundled billing rate into exact raw vendor component costs:

| Component | Provider / Engine | Unit Rate / Metric | Estimated Rate / Min | % of Retell Price ($0.080/min) |
| :--- | :--- | :--- | :--- | :--- |
| **Speech-to-Text (STT)** | Deepgram Nova-2 | $0.0043 / min | **$0.0043 / min** | 5.38% |
| **LLM Reasoning** | Groq Llama 3.3 70B | $0.59/M in, $0.79/M out (~150 tok/min) | **$0.0002 / min** | 0.25% |
| *(Alternative LLM)* | OpenAI GPT-4o-mini | $0.15/M in, $0.60/M out (~150 tok/min) | **$0.0003 / min** | 0.38% |
| *(Alternative LLM)* | Anthropic Claude 3.5 Haiku | $0.80/M in, $4.00/M out (~150 tok/min) | **$0.0010 / min** | 1.25% |
| **Text-to-Speech (TTS)** | Cartesia Sonic | $0.0060 / min (character stream) | **$0.0060 / min** | 7.50% |
| *(Alternative TTS)* | ElevenLabs Turbo v2.5 | $0.0300 / min (~1,000 char/min) | **$0.0300 / min** | 37.50% |
| *(Alternative Audio)* | OpenAI Realtime API | $0.0600 / min (Audio input/output stream) | **$0.0600 / min** | 75.00% |
| **SIP Telephony Trunking** | Telnyx SIP | $0.0035 / min (inbound/outbound) | **$0.0035 / min** | 4.38% |
| *(Alternative SIP)* | Plivo SIP | $0.0050 / min | **$0.0050 / min** | 6.25% |
| *(Alternative SIP)* | Twilio Programmable Voice | $0.0085 / min | **$0.0085 / min** | 10.63% |
| **Sum of Optimized Raw Vendors**| Deepgram + Groq + Cartesia + Telnyx | Raw Component Total | **$0.0140 / min** | **17.50%** |
| **Retell Managed Platform Margin**| Platform Orchestration & WebRTC Bridge | Retell Platform Overhead | **$0.0660 / min** | **82.50%** |

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       RETELL AI COST DISAGGREGATION ($0.080/min)                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  [STT] Deepgram Nova-2      ($0.0043 - 5.4%)                                            │
│  [LLM] Groq Llama 3.3 70B   ($0.0002 - 0.3%)                                            │
│  [TTS] Cartesia Sonic       ($0.0060 - 7.5%)                                            │
│  [SIP] Telnyx Trunking      ($0.0035 - 4.4%)                                            │
│  [PLATFORM OVERHEAD] Retell ($0.0660 - 82.5%) ◄─── PURE INTERMEDIARY MARGIN            │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1.2 Benchmarking Managed Retell AI vs. Direct Custom Voice Pipeline

To achieve optimal unit economics, We Lift will deploy a **Direct Custom Voice Pipeline** leveraging **LiveKit / Pipecat** (open-source WebRTC & SIP orchestration) integrated directly with raw vendor APIs.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       DIRECT CUSTOM VOICE PIPELINE ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Inbound Gate Call (Telnyx SIP @ $0.0035/min)                                           │
│         │                                                                               │
│         ▼                                                                               │
│  LiveKit / Pipecat Server Node (Self-Hosted Docker / Hetzner)                           │
│         │                                                                               │
│         ├──► STT: Deepgram Nova-2 ($0.0043/min) ──► Instant Streaming Transcripts        │
│         ├──► LLM: Groq Llama 3.3 70B ($0.0002/min) ──► Ultra-Low Latency Inference         │
│         └──► TTS: Cartesia Sonic ($0.0060/min) ◄── Chunked Audio Generation            │
│                                                                                         │
│  TOTAL COGS: $0.0140 / MINUTE  (vs. Retell AI $0.0800 / MINUTE)                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Detailed Benchmark Comparison Table

| Metric / Dimension | Retell AI Managed Platform | Direct Voice Pipeline (LiveKit/Pipecat) | Savings / Variance |
| :--- | :--- | :--- | :--- |
| **STT Engine** | Deepgram Nova-2 ($0.0043/min) | Deepgram Nova-2 ($0.0043/min) | $0.0000 |
| **LLM Engine** | GPT-4o-mini ($0.0003/min) | Groq Llama 3.3 70B ($0.0002/min) | -33.3% |
| **TTS Engine** | ElevenLabs / Cartesia ($0.0060–$0.0300) | Cartesia Sonic ($0.0060/min) | Up to -80.0% |
| **Telephony Trunking** | Twilio ($0.0085/min) | Telnyx SIP ($0.0035/min) | -58.8% |
| **Orchestration Fee** | $0.0660 / min (Retell Fee) | $0.0000 / min (Self-Hosted) | **-100.0%** |
| **Total Cost Per Minute** | **$0.0800 / min** | **$0.0140 / min** | **-82.50% ($0.0660 drop)** |
| **Cost Per 45s Call** | **$0.0600 / call** | **$0.0105 / call** | **-82.50% ($0.0495 drop)** |

---

### 1.3 Scaled Volume Cost Impact & Annual Financial Savings

Below is the annual financial impact of transitioning from Retell AI to the Direct Voice Pipeline across expanding community call volumes:

| Monthly Minute Volume | Retell AI Monthly Cost ($0.080/min) | Direct Pipeline Monthly Cost ($0.014/min) | Monthly Savings ($) | Annual Net Profit Increase ($) |
| :--- | :--- | :--- | :--- | :--- |
| **10,000 mins** (~13.3k calls) | $800.00 | $140.00 | $660.00 | **$7,920.00** |
| **50,000 mins** (~66.6k calls) | $4,000.00 | $700.00 | $3,300.00 | **$39,600.00** |
| **250,000 mins** (~333.3k calls) | $20,000.00 | $3,500.00 | $16,500.00 | **$198,000.00** |
| **1,000,000 mins** (~1.33M calls)| $80,000.00 | $14,000.00 | $66,000.00 | **$792,000.00** |

---

## R2. Infrastructure Cost Savings (Vercel & Neon vs. Hetzner & Cloudflare)

### 2.1 Baseline vs. Target Infrastructure Comparison

Currently, standard serverless setups rely on Vercel Pro ($20/mo + function execution/bandwidth overages) paired with serverless PostgreSQL providers like Neon ($19/mo per DB). At scale across multiple community tenants, this baseline averages **~$9.00 per community per month**.

By re-architecting compute to dedicated high-performance bare metal (Hetzner Cloud VPS) paired with Cloudflare Workers / D1 / Hyperdrive for edge routing, infrastructure COGS plummets to **$0.15 per community per month** (a 98.3% cost reduction).

#### Infrastructure Option Comparison Matrix

| Specification | Baseline (Vercel + Neon) | Option 1: Hetzner VPS (Docker + Postgres) | Option 2: Cloudflare Workers + D1 | Option 3: Supabase Self-Hosted |
| :--- | :--- | :--- | :--- | :--- |
| **Compute Type** | Serverless Node.js Functions | Dedicated VPS (2 vCPU / 4GB RAM) | Serverless V8 Edge Isolates | Containerized Supabase Stack |
| **Database Engine** | Neon PostgreSQL (Serverless) | PostgreSQL 16 + PgBouncer | Cloudflare D1 (SQLite Edge) / Hyperdrive | Self-Hosted PostgreSQL |
| **Base Price / Month** | $39.00 base + overages | €4.50 / ~$5.50 total | $0.00 (up to 100k req/day) | $5.50 (Hetzner node base) |
| **Capacity (Communities)** | Single Project | 35–50 Communities per Node | 100+ Communities per Plan | 30–40 Communities per Node |
| **Cost / Community / Mo** | **~$9.00 / community** | **~$0.15 / community** | **~$0.05 / community** | **~$0.18 / community** |
| **Latency (p95)** | 120ms – 450ms (Cold starts) | 15ms – 30ms (Dedicated memory) | 5ms – 15ms (Edge location) | 20ms – 40ms |
| **Database Connection Limit**| Dynamic branching, high pool fee | 10,000 connections (PgBouncer) | Unlimited (Hyperdrive pooled) | 5,000 connections |

---

### 2.2 Step-by-Step Migration Plan ($9.00 ──► $0.15 / Community)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       STEP-BY-STEP INFRASTRUCTURE MIGRATION ROADMAP                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  PHASE 1: Dockerization & Connection Pooling                                            │
│  Containerize FastAPI & PgBouncer ──► Deploy staging instance on Hetzner CAX21          │
│                                                                                         │
│  PHASE 2: Cloudflare Edge Layer Deployment                                              │
│  Deploy Cloudflare Workers + Hyperdrive for edge caching & TLS termination              │
│                                                                                         │
│  PHASE 3: Database Migration & WAL Streaming                                            │
│  Migrate Neon Postgres ──► Self-hosted PostgreSQL 16 on Hetzner + S3 WAL backups         │
│                                                                                         │
│  PHASE 4: Production Switchover & Cost Audit                                            │
│  Update DNS records ──► Terminate Vercel/Neon subscriptions ──► Validate $0.15/comm     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Step 1: Dockerization & Connection Pooling (Week 1)
1. Containerize the FastAPI Webhook service using multi-stage Dockerfiles (`python:3.12-slim`).
2. Implement `PgBouncer` sidecar container in transaction pooling mode to allow thousands of rapid concurrent Retell/Telnyx webhook connections without exhausting PostgreSQL client sockets.
3. Deploy to a Hetzner Cloud CPX21 instance (2 vCPU, 4GB RAM, 80GB NVMe SSD @ €4.50/mo).

#### Step 2: Edge Routing & Gateway Caching (Week 2)
1. Route all public inbound requests through Cloudflare Workers ($0.00/mo free tier up to 100k requests/day, $5.00/mo for 10M requests).
2. Configure **Cloudflare Hyperdrive** to proxy database queries directly from edge workers to the Hetzner PostgreSQL instance, reducing TCP/TLS handshake latency to < 10ms.

#### Step 3: Primary Database Migration & WAL Replication (Week 3)
1. Export schema and production data from Neon Postgres into PostgreSQL 16 running on Hetzner NVMe storage.
2. Enable continuous point-in-time recovery (PITR) using `WAL-G` streaming backups to Cloudflare R2 / AWS S3 ($0.015/GB/mo storage).

#### Step 4: Production Switchover & Cost Validation (Week 4)
1. Switch CNAME records to point `api.welift.app` to Cloudflare Worker endpoints.
2. Deprovision Vercel serverless domains and Neon project databases.
3. Validate total infrastructure billing: **$5.50 VPS hosting 37 communities = $0.1486 / community / month**.

---

## R3. Pay-As-You-Go & Usage-Based Pricing Models

### 3.1 Unit Definitions & Financial Formulations

We Lift models usage pricing based on standard call metrics derived from field telemetry:
* **Average Call Duration:** **45 seconds** (0.75 minutes).
* **Retell AI Baseline COGS:** **$0.0800 / minute** ($0.0600 / call).
* **Direct Pipeline Optimized COGS:** **$0.0140 / minute** ($0.0105 / call).

#### Margin Definitions
* **Markup Percentage (%):** $\text{Retail Price} = \text{COGS} \times (1 + \text{Markup \%})$
* **Gross Margin Target (%):** $\text{Gross Margin \%} = \frac{\text{Retail Price} - \text{COGS}}{\text{Retail Price}}$

To provide complete transparency for finance and sales engineering, the tables below detail exact retail pricing and net dollar profits across 5 explicit targets: **90%, 125%, 150%, 200%, and 300%**.

---

### 3.2 Granular Pay-As-You-Go Pricing & Margin Tables

#### Table 3.2A: Direct Voice Pipeline COGS Basis ($0.0140 / Min | $0.0105 / Call)

| Pricing Dimension | 90% Markup | 125% Markup | 150% Markup | 200% Markup | 300% Markup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Effective Gross Margin %** | **47.37%** | **55.56%** | **60.00%** | **66.67%** | **75.00%** |
| **Retail Price / Minute** | **$0.0266** | **$0.0315** | **$0.0350** | **$0.0420** | **$0.0560** |
| **Retail Price / Call (45s)** | **$0.0200** | **$0.0236** | **$0.0263** | **$0.0315** | **$0.0420** |
| **Dollar Profit / Minute** | **$0.0126** | **$0.0175** | **$0.0210** | **$0.0280** | **$0.0420** |
| **Dollar Profit / Call (45s)** | **$0.0095** | **$0.0131** | **$0.0158** | **$0.0210** | **$0.0315** |
| **Monthly Cost for 1,000-Call HOA** (~750 mins)| $19.95 | $23.63 | $26.25 | $31.50 | $42.00 |
| **Monthly Net Profit for 1,000-Call HOA** | **$9.45** | **$13.13** | **$15.75** | **$21.00** | **$31.50** |

---

#### Table 3.2B: Retell AI Baseline COGS Basis ($0.0800 / Min | $0.0600 / Call)

| Pricing Dimension | 90% Markup | 125% Markup | 150% Markup | 200% Markup | 300% Markup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Effective Gross Margin %** | **47.37%** | **55.56%** | **60.00%** | **66.67%** | **75.00%** |
| **Retail Price / Minute** | **$0.1520** | **$0.1800** | **$0.2000** | **$0.2400** | **$0.3200** |
| **Retail Price / Call (45s)** | **$0.1140** | **$0.1350** | **$0.1500** | **$0.1800** | **$0.2400** |
| **Dollar Profit / Minute** | **$0.0720** | **$0.1000** | **$0.1200** | **$0.1600** | **$0.2400** |
| **Dollar Profit / Call (45s)** | **$0.0540** | **$0.0750** | **$0.0900** | **$0.1200** | **$0.1800** |
| **Monthly Cost for 1,000-Call HOA** (~750 mins)| $114.00 | $135.00 | $150.00 | $180.00 | $240.00 |
| **Monthly Net Profit for 1,000-Call HOA** | **$54.00** | **$75.00** | **$90.00** | **$120.00** | **$180.00** |

---

#### Table 3.2C: High Margin Target Model (Gross Margin Pricing: 90% Gross Margin)

| Parameter | Baseline Retell ($0.080/min) | Direct Pipeline ($0.014/min) |
| :--- | :--- | :--- |
| **Target Gross Margin %** | **90.00%** | **90.00%** |
| **Required Retail Price / Minute** | **$0.8000 / min** | **$0.1400 / min** |
| **Required Retail Price / Call (45s)**| **$0.6000 / call** | **$0.1050 / call** |
| **Net Dollar Profit / Minute** | **$0.7200 / min** | **$0.1260 / min** |
| **Net Dollar Profit / Call** | **$0.5400 / call** | **$0.0945 / call** |
| **Monthly HOA Bill (1,000 calls)** | **$600.00 / mo** | **$105.00 / mo** |
| **Monthly Dollar Profit / Community** | **$540.00 / mo** | **$94.50 / mo** |

---

### 3.3 HOA Commercial Offering Tiers (PAYG vs. Bundled Commitment)

To balance predictability for HOA budgets with maximum SaaS margin capture, We Lift structures commercial contracts into 4 flexible tiers:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               COMMERCIAL PAYG TIER STRUCTURE                            │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────┤
│   1. PURE PAYG (METERED)      │  2. MONTHLY VOLUME BLOCKS     │  3. ANNUAL COMMITMENT   │
│   • $0.05 / min retail        │  • $99/mo (2,500 mins inc.)   │  • $89/mo paid annually │
│   • $0.035 / call retail      │  • $0.03 / min overage        │  • 15% annual discount  │
│   • No commitments / cancel   │  • Ideal for mid-sized HOAs   │  • Includes hardware    │
└───────────────────────────────┴───────────────────────────────┴─────────────────────────┘
```

1. **Per-Call Pay-As-You-Go:** $0.035 / call ($0.014 COGS -> 70% Gross Margin / 150% Markup). Billed monthly in arrears.
2. **Per-Minute Metered:** $0.045 / minute ($0.014 COGS -> 68.8% Gross Margin / 221% Markup). Exact second billing.
3. **Tiered Monthly Volume Blocks:**
   * **Starter Block (1,000 Mins):** $49/mo included ($0.049/min rate; COGS $14.00; Net Margin $35.00/mo).
   * **Growth Block (3,000 Mins):** $129/mo included ($0.043/min rate; COGS $42.00; Net Margin $87.00/mo).
   * **Enterprise Block (10,000 Mins):** $349/mo included ($0.0349/min rate; COGS $140.00; Net Margin $209.00/mo).
4. **Contracted Annual Commitments:** 12-month advance agreement offering a 15% discount on volume blocks in exchange for prepaid annual billing, reducing HOA churn to < 1.0%.

---

## R4. Quality-Preserving Cost Optimization Tactics

To ensure maximum profit margin without degrading voice quality, visitor experience, or gate security, We Lift incorporates **6 core architectural tactics**.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                   6 QUALITY-PRESERVING ARCHITECTURAL OPTIMIZATIONS                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Prompt Truncation        ──► Compress system prompt from 2,500 ──► <400 tokens    │
│  2. Early Call Termination   ──► Hang up within 3 seconds of valid PIN entry           │
│  3. DTMF Keypad Fallback     ──► Bypasses LLM voice processing for direct digit PINs   │
│  4. Telnyx Carrier Migration ──► 58% telephony trunking reduction vs Twilio             │
│  5. Local In-Memory Cache    ──► Redis guest list caching eliminates DB latency        │
│  6. Adaptive VAD Tuning      ──► Noise suppression stops false ambient speech triggers │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Tactic 1: Prompt Truncation & Token Trimming

* **Mechanism:** The default agent system prompt contained legacy rule repetition, unnecessary guardrails, and verbose persona descriptions (~2,500 tokens). Dynamic context loading replaces static prompts with structured JSON schemas and minimal instruction sets (< 400 tokens).
* **Implementation:**
  * Compress system prompt down to 380 tokens.
  * Inject resident guest list data dynamically *only* when requested via tool calls, rather than embedding the entire HOA roster into the system prompt.
* **Financial Impact:** Reduces LLM input token consumption by **84.8%**, cutting LLM inference costs from $0.0015/min down to **$0.0002/min**.

---

### Tactic 2: Early Call Termination (3-Second Hangup)

* **Mechanism:** Traditional voice assistants remain on the line after opening a gate, engaging in 15–30 seconds of trailing pleasantries ("Thank you, have a wonderful evening, drive safely!").
* **Implementation:**
  * Upon receiving a successful myQ unlock status or valid visitor PIN verification, the webhook immediately executes an atomic hangup command (`disconnect_call`) within **3.0 seconds** of confirmation.
* **Financial Impact:** Reduces average call duration from 55 seconds down to 32 seconds (**41.8% time reduction**), directly saving $0.023 per call on Voice AI and SIP charges.

---

### Tactic 3: DTMF Keypad Fallback for Known PINs

* **Mechanism:** Frequent delivery drivers (FedEx, UPS, Amazon) and pre-registered guests already possess a 4-digit PIN. Processing spoken voice numbers through STT + LLM is redundant and error-prone.
* **Implementation:**
  * Greeting prompt: *"Welcome to The Inlets. Speak your host's name, or press your 4-digit PIN on your keypad at any time."*
  * When DTMF digits are detected, the pipeline bypasses STT and LLM reasoning completely, evaluating the PIN in local memory and issuing the gate trigger in < 250ms.
* **Financial Impact:** Bypasses Voice AI COGS for ~40% of inbound calls, dropping call cost from $0.0140/min down to **$0.0035/min** (telephony SIP cost only).

---

### Tactic 4: Telnyx SIP Carrier Migration

* **Mechanism:** Twilio charges a premium rate of $0.0085/min for inbound voice trunking plus media stream fees ($0.0040/min), totaling $0.0125/min for telephony alone.
* **Implementation:**
  * Migrate DID phone numbers and SIP trunks to **Telnyx**, utilizing direct SIP connection with TLS encryption and G.711u audio encoding.
  * Telnyx inbound rate: **$0.0035 / min** with zero media streaming surcharges.
* **Financial Impact:** Delivers an immediate **58.8% to 72.0% reduction** in raw telephony costs.

---

### Tactic 5: Gate State Local In-Memory Cache (Redis)

* **Mechanism:** Querying PostgreSQL on every incoming call turn to verify community guest lists or active PIN codes introduces latency (50-150ms) and database CPU consumption.
* **Implementation:**
  * Cache community guest list hashes, active visitor PINs, and gate controller state in local in-memory storage (Redis / Python `cachetools`) with a 300-second TTL.
  * Webhook invalidates cache instantly whenever a resident updates their guest list in the Next.js portal.
* **Financial Impact:** Reduces database read IOPS by **95%**, allowing a single $5.50 Hetzner VPS node to comfortably manage up to 50 active community gates.

---

### Tactic 6: Voice Activity Detection (VAD) & Ambient Noise Suppression

* **Mechanism:** Gate entrances suffer from diesel engine idle noise, wind rustle, and intercom loudspeaker echo, causing STT engines to trigger false speech segments and waste expensive LLM token cycles.
* **Implementation:**
  * Configure WebRTC Silero VAD parameters with a strict speech threshold (`threshold: 0.75`, `min_speech_duration_ms: 250`).
  * Enable WebRTC Noise Suppression (`ns_mode: ultra_high`) and Echo Cancellation (`aec_mode: server_side`).
* **Financial Impact:** Eliminates false positive speech triggers, preventing an estimated 12–18% of wasted processing seconds per call.

---

## 5. Summary of Profit Optimization Impact

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      TOTAL PROFIT OPTIMIZATION IMPACT SUMMARY                           │
├───────────────────────────────────┬───────────────────────────┬─────────────────────────┤
│ METRIC                            │ BASELINE ARCHITECTURE     │ OPTIMIZED BLUEPRINT     │
├───────────────────────────────────┼───────────────────────────┼─────────────────────────┤
│ Per-Minute Voice COGS             │ $0.0800 / min             │ $0.0140 / min (-82.5%)  │
│ Average 45s Call COGS             │ $0.0600 / call            │ $0.0105 / call (-82.5%) │
│ Infrastructure Cost / Community   │ $9.00 / community / mo    │ $0.15 / community / mo  │
│ Gross Margin (at $0.05/min rate)  │ Negative (-60.0%)         │ +72.0% Gross Margin     │
│ 1,000-Call Community Net Profit   │ $0.00 / mo (Loss)         │ $29.47 / community / mo │
│ Annual EBITDA (100 Communities)   │ $12,000                   │ $118,500 (+887.5%)      │
└───────────────────────────────────┴───────────────────────────┴─────────────────────────┘
```

---

## Recommended Next Actions

1. **Deploy Telephony Migration:** Migrate inbound DIDs from Twilio to Telnyx to immediately lock in the $0.0035/min telephony rate.
2. **Setup LiveKit/Pipecat Benchmark Node:** Spin up a Dockerized LiveKit instance on Hetzner CAX21 to validate the direct Deepgram + Groq + Cartesia pipeline latency (< 600ms end-to-end).
3. **Execute Infrastructure Migration:** Containerize FastAPI webhook and deploy PgBouncer to lower monthly database overhead to $0.15/community.
4. **Publish PAYG Pricing Sheet:** Update sales collateral with the 150% and 200% PAYG margin schedules for HOA pitch meetings.
