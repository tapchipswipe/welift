# We Lift - Production Deployment Guide

This guide details the step-by-step process for deploying the **We Lift** application stack to cloud hosting:
- **FastAPI Webhook Service**: Deployed on [Railway](https://railway.app/)
- **PostgreSQL Database**: Provisioned on Railway
- **Next.js Vendor Portal**: Deployed on [Vercel](https://vercel.com/)
- **Authentication**: Clerk
- **Telephony & SMS**: Twilio & Retell AI

---

## Architecture Overview

```
                          ┌───────────────────────────┐
                          │   Next.js Vendor Portal   │
                          │        (Vercel)           │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
┌─────────────────────────┐   ┌──────────────────┐   ┌────────────────────────┐
│  Retell AI / Webhooks   │──►│ FastAPI Webhook  │──►│  PostgreSQL Database   │
│   (Twilio / Gate metal) │   │    (Railway)     │   │   (Railway Postgres)   │
└─────────────────────────┘   └──────────────────┘   └────────────────────────┘
```

Both services share the same PostgreSQL relational database schema. On startup:
- **FastAPI** automatically creates and seeds tables via SQLAlchemy.
- **Next.js Portal** automatically detects `DATABASE_URL`, updates Prisma provider to `postgresql`, and pushes schema via `prisma/prepare-db.js`.

If no PostgreSQL `DATABASE_URL` is provided (local development), both services fallback to SQLite (`welift.db`) automatically.

---

## Part 1: Railway Deployment (PostgreSQL + FastAPI Webhook)

### Step 1.1: Provision PostgreSQL Database
1. Log into your [Railway Console](https://railway.app/).
2. Create a **New Project** or select an existing workspace.
3. Click **+ New** -> **Database** -> **Add PostgreSQL**.
4. Once created, click on the PostgreSQL service, navigate to the **Variables** tab, and copy the `DATABASE_URL` (e.g. `postgres://postgres:password@host.railway.app:5432/railway`).

### Step 1.2: Deploy FastAPI Webhook Service
1. In the same Railway project, click **+ New** -> **GitHub Repo** and select your `welift` repository.
2. Select the created service and navigate to **Settings**:
   - **Root Directory**: Set to `webhook`
   - **Build Command**: Uses `Dockerfile` automatically (or Nixpacks using `Procfile`)
3. Navigate to **Variables** and configure the following environment variables:

| Variable Name | Required | Description / Example Value |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL URL from Step 1.1 (`postgres://...`) |
| `RETELL_API_KEY` | Yes | Your Retell AI API Key (`key_...`) |
| `RETELL_DID` | Yes | Assigned E.164 phone number (e.g. `+18885550199`) |
| `DEFAULT_COMMUNITY` | Yes | Default community name (e.g. `The Inlets`) |
| `SIMULATE_MYQ_OPEN` | Yes | Set `true` for demo mode, or `false` for live myQ hardware |
| `VERIFY_RETELL_SIGNATURES` | Yes | Set `true` in production to verify Retell webhook signatures |
| `TWILIO_ACCOUNT_SID` | Yes | Twilio Account SID (`AC...`) |
| `TWILIO_AUTH_TOKEN` | Yes | Twilio Auth Token |
| `TWILIO_FROM_NUMBER` | Yes | Twilio E.164 phone number (`+15005550006`) |
| `MYQ_API_BASE` | Optional | myQ Partner API base URL (if live myQ used) |
| `MYQ_API_KEY` | Optional | myQ Partner API Key |
| `MYQ_FACILITY_ID` | Optional | myQ Facility ID |
| `MYQ_ENTRANCE_ID` | Optional | myQ Entrance ID |
| `PORT` | Yes | Set to `8080` (or Railway default) |

4. In **Settings** -> **Networking**, click **Generate Domain** to get your public webhook URL (e.g. `https://welift-webhook-production.up.railway.app`).

---

## Part 2: Vercel Deployment (Next.js Vendor Portal)

### Step 2.1: Import GitHub Repository
1. Log into [Vercel](https://vercel.com/) and click **Add New** -> **Project**.
2. Import your `welift` GitHub repository.

### Step 2.2: Configure Subdirectory & Project Settings
1. In the project setup screen, expand **Framework Preset** and select **Next.js**.
2. Expand **Root Directory** and click **Edit**, then select the `portal` folder.

### Step 2.3: Configure Environment Variables
Add the following Environment Variables in Vercel:

| Variable Name | Required | Description / Example Value |
|---|---|---|
| `DATABASE_URL` | Yes | **Same** PostgreSQL URL from Railway (`postgres://...`) |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Yes | Clerk publishable key (`pk_live_...` or `pk_test_...`) |
| `CLERK_SECRET_KEY` | Yes | Clerk secret key (`sk_live_...` or `sk_test_...`) |
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Yes | Set to `/sign-in` |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Yes | Set to `/sign-up` |
| `TWILIO_ACCOUNT_SID` | Yes | Twilio Account SID (`AC...`) |
| `TWILIO_AUTH_TOKEN` | Yes | Twilio Auth Token |
| `TWILIO_FROM_NUMBER` | Yes | Twilio E.164 phone number (`+15005550006`) |

### Step 2.4: Deploy
Click **Deploy**.
During the build process:
1. `npm run postinstall` executes `node prisma/prepare-db.js`.
2. `prepare-db.js` detects the PostgreSQL connection string.
3. Prisma updates `schema.prisma` provider to `postgresql`, generates the client, and executes `prisma db push` to initialize tables.
4. Next.js compiles the production portal.

---

## Part 3: Deployment Verification

Use the included verification script to test your live endpoints end-to-end:

```bash
python scripts/verify_deployment.py \
  --fastapi-url https://welift-webhook-production.up.railway.app \
  --vercel-url https://welift-portal.vercel.app
```

Or set environment variables and run:
```bash
export FASTAPI_URL=https://welift-webhook-production.up.railway.app
export VERCEL_URL=https://welift-portal.vercel.app
python scripts/verify_deployment.py
```

Expected Output:
```
============================================================
           WE LIFT DEPLOYMENT VERIFICATION TOOL          
============================================================

[1/3] Testing FastAPI webhook at: https://welift-webhook-production.up.railway.app
✅ Webhook health check responded with 200 OK.
    - Status: ok
    - Version: 0.6.0
    - Database Guest List Ready: True
    - Database Vendors Seeded: True
    - Twilio Configured: True
    - MyQ API Configured: False
    - Simulate MyQ Open: True
✅ Database connection verified (Tables seeded successfully).

[2/3] Testing FastAPI keypad entry API...
✅ Keypad entry verification responded correctly (Denied dummy code).

[3/3] Testing Vercel Portal at: https://welift-portal.vercel.app
✅ Portal home responded with status 200.
✅ Clerk authentication interface elements detected on sign-in page.

============================================================
                       SUMMARY REPORT                     
============================================================
✅ FastAPI Webhook Health Check:  PASSED
✅ FastAPI Keypad Verification:   PASSED
✅ Vercel Portal Verification:    PASSED
============================================================
🎉 ALL TESTS PASSED! Deployment is healthy and running.
```

---

## Local Development (Backward Compatibility)

When developing locally:
1. Do not set `DATABASE_URL` or keep `DATABASE_URL="file:../../data/welift.db"`.
2. FastAPI will automatically create `/data/welift.db` SQLite database and seed initial communities and vendors.
3. Portal will automatically generate Prisma Client for SQLite.
