# Gate code → real barrier (Phase 4 runbook)

Wave 1 MVP texts a We Lift PIN and can prove it on Retell. **This runbook** connects that PIN to a physical open.

## Path A — myQ Partner API (target)

1. Complete partner application ([pilot-the-inlets/myq-api-path.md](pilot-the-inlets/myq-api-path.md))  
2. On `send_code` / mint: create time-bound guest pass / PIN via API  
3. SMS that native PIN  
4. Set `SIMULATE_MYQ_OPEN=false`; configure `MYQ_*` for AI `open_gate`  
5. Test: SMS → keypad → barrier; AI open_gate → barrier; revoke disables pass  

Hook point in code: extend `credentials.send_code` / mint to call myQ create-pass when `MYQ_*` set (same pattern as `open_gate` unlock in [webhook/main.py](../webhook/main.py)).

## Path B — Dealer temp CAP codes (until API)

1. Ask LiftMaster dealer: temp vendor code slots / myQ guest passes at The Inlets  
2. Agree format (6-digit) matching We Lift mint  
3. Either: dealer programs daily codes We Lift also mints, **or** CAM creates myQ guest pass and We Lift SMS is the delivery layer only  
4. Document who rotates codes each morning  
5. Pedestal acceptance test with CAM present  

## Acceptance tests

| Test | Pass |
|------|------|
| SMS code on keypad | Barrier moves |
| After `valid_until` | Code rejected |
| Access Desk revoke | Code dead |
| AI `open_gate` with myQ API | Barrier moves (or simulate until API) |

## Status in MVP

Unlock stub already in webhook (`MYQ_*` + `SIMULATE_MYQ_OPEN`). Credential SMS works without metal. **Do not claim live pedestal opens** until Path A or B tested on-site.
