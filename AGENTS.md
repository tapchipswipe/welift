# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
Mostly business/launch documentation (Markdown). The only runnable application is the
**Retell gate webhook** — a Python FastAPI service in [`webhook/`](webhook/) that verifies
visitors against a guest list and (optionally) opens a myQ gate. See [`webhook/README.md`](webhook/README.md).

### Service: `webhook/` (FastAPI + uvicorn)
- Python 3.12. The Cloud update script creates a virtualenv at `webhook/.venv` and installs
  [`webhook/requirements.txt`](webhook/requirements.txt). Activate with `source webhook/.venv/bin/activate`
  or call binaries directly (e.g. `webhook/.venv/bin/uvicorn`).
- **Run (dev):** `cd webhook && ./run.sh` — auto-creates `.env` (from `.env.example`), a venv,
  and `data/guest-list.json` (from the example), then runs `uvicorn main:app --port 8080 --reload`.
  Note: on the *first* run with no `.env`, `run.sh` copies `.env.example` and exits; re-run it (or
  start uvicorn directly) to actually start the server.
- **Run directly (skips run.sh's first-run exit):**
  `cd webhook && SIMULATE_MYQ_OPEN=true VERIFY_RETELL_SIGNATURES=false .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080 --reload`
- **Test:** `cd webhook && .venv/bin/python test_tools.py` — a self-contained smoke suite using
  FastAPI's `TestClient`; it sets its own env (`SIMULATE_MYQ_OPEN`, guest list, etc.) and needs no
  server running. Prints `ALL WEBHOOKS PASS` on success.
- **Lint:** no linter is configured in this repo (no ruff/flake8/pyproject). Use
  `python -m py_compile webhook/main.py webhook/test_tools.py scripts/create_agent.py` as a basic check.

### Non-obvious gotchas
- **`data/guest-list.json` and `webhook/.env` are gitignored** and are NOT recreated by the update
  script. Create them from the `*.example` files before running the server (or just use `run.sh`,
  which does this). `test_tools.py` reads `data/guest-list.example.json` directly, so it works without them.
- **Demo vs live opens:** set `SIMULATE_MYQ_OPEN=true` to fake gate unlocks with no myQ credentials.
  Real opens need `MYQ_API_BASE/MYQ_API_KEY/MYQ_FACILITY_ID/MYQ_ENTRANCE_ID`. With neither, `open_gate`
  intentionally **fails closed** (`status: failed`) — that is correct behavior, not a bug.
- **Signature verification:** keep `VERIFY_RETELL_SIGNATURES=false` for local curl/testing; production
  uses `true` with a real `RETELL_API_KEY`.
- The POST tool endpoints read the **raw request body** (not typed Pydantic models), so Swagger UI at
  `/docs` shows no request-body field for them. This is expected — call them with curl/fetch. `GET /health`
  and `GET /docs` work normally.
- `scripts/create_agent.py` pushes configs to the live Retell API and requires a real `RETELL_API_KEY`;
  it cannot run end-to-end in this environment without that secret.
