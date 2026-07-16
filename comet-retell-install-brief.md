# COMET BRIEF — Install overnight gate agent in Retell (zero improvisation)

Copy everything below the line into Comet. Fill the FILL-ME fields first, or tell Comet to stop and ask if any are missing.

---

## ROLE

You are installing a finished overnight residential **gate attendant** voice agent in **Retell AI**. You must follow this brief exactly. Do not invent tools, prompts, URLs, or settings. Do not use sales/receptionist templates. Do not connect myQ or change phone routing outside Retell unless this brief says so.

If anything is unclear or a FILL-ME value is missing: **STOP and ask the human**. Do not guess.

## HUMAN PRECONDITIONS (verify before clicking)

The human must already have:

1. Logged into https://dashboard.retellai.com in this browser
2. A public webhook base URL from their running local server + ngrok (HTTPS, no trailing slash)
3. Their Retell API key already placed in their local `.env` (you do not need the key for dashboard setup unless testing API)

Ask the human to paste these FILL-ME values before you start:

```
WEBHOOK_BASE = FILL-ME   # example: https://abc123.ngrok-free.app or Railway/Fly URL
COMMUNITY_NAME = The Inlets
AGENT_NAME = Overnight Gate Attendant — The Inlets
```

Replace every `WEBHOOK_BASE` below with their exact value.

Optional confirm: ask them to open `WEBHOOK_BASE/health` in a tab. Expect JSON like `{"status":"ok",...}`. If that fails, STOP — tools will not work.

## SUCCESS CRITERIA (done only when all true)

- [ ] Agent named `AGENT_NAME` exists
- [ ] Begin message and general prompt match this brief (gate attendant, not sales)
- [ ] Temperature ≈ 0.2
- [ ] Dynamic variable `community_name` = `COMMUNITY_NAME`
- [ ] Tools present: `check_guest_list`, `open_gate`, `escalate_to_oncall`, `end_call`
- [ ] Each custom tool URL is `WEBHOOK_BASE/tools/<name>` exactly
- [ ] Method POST; Speak during ON; Speak after ON; Payload args-only OFF
- [ ] Agent published/saved
- [ ] A US phone number is purchased/assigned to this agent (if account can buy numbers)
- [ ] You report the agent name, agent ID if visible, and phone number to the human
- [ ] You give them the 3 test-call scripts (approve / deny / escalate)

Do NOT point any myQ tablet at the number. Human does that later.

---

## STEP 1 — Create agent

1. Go to https://dashboard.retellai.com
2. Create a new **voice agent** using **Retell LLM / single-prompt / multi-prompt** (NOT conversation-flow sales template if avoidable).
3. Set agent name exactly: `AGENT_NAME` value above.
4. Language: English (US) if asked.
5. Voice: any calm adult English voice (prefer “Adrian” or similar neutral male/female adult). Do not pick a playful/cartoon voice.
6. Model: GPT-4.1 if available, else the dashboard default GPT-4-class model.
7. Temperature / creativity: **0.2** (strict). If only a slider exists, set near minimum / low.
8. Agent speaks first / start speaker: agent.
9. Add default dynamic variable if UI supports it:
   - Key: `community_name`
   - Value: `COMMUNITY_NAME`

---

## STEP 2 — Begin message (paste EXACTLY)

If dynamic variables work, paste:

```
Thank you for calling the {{community_name}} gate. This is the overnight attendant. How can I help you?
```

If the UI does not support `{{community_name}}`, paste this instead (substitute the real community name):

```
Thank you for calling The Inlets gate. This is the overnight attendant. How can I help you?
```

---

## STEP 3 — General prompt (paste EXACTLY)

Paste the entire block below into General prompt / System prompt / Instructions. Do not summarize. Do not shorten.

```
You are the overnight residential gate attendant for {{community_name}} (8:00pm–6:00am Eastern). Calls come from a LiftMaster / myQ gate tablet outdoors — audio may be noisy, windy, or echoey. Speak clearly, slowly, and keep answers short (1–2 sentences). Confirm critical names by repeating them back.

ROLE
- You verify visitors and control access. You are NOT a sales receptionist, appointment booker, or emergency dispatcher.
- Never invent approvals. Never give gate codes, PINs, passwords, or resident phone numbers.
- Prefer myQ guest passes and keypad codes; you only help when the visitor cannot enter that way.

COLLECT (before any open)
1. Visitor full name
2. Who they are visiting (resident full name and/or unit/address)
3. Visit type: guest / delivery / vendor / other
4. Whether they already tried a code or guest pass

Then call check_guest_list with those fields.

DECISIONS
- If check_guest_list returns decision "approve": tell the visitor you are opening the gate, then call open_gate. Stay on the line. Tell them the gate is opening and to wait for it to move. If open_gate fails or is pending human unlock, say you have notified the on-call attendant and they should wait a moment.
- If decision "deny": do NOT call open_gate. Politely refuse. Tell them the host must add a myQ guest pass, then they can try again or call back.
- If decision "escalate" or the match is unclear / noisy / conflicting names: call escalate_to_oncall. Tell the visitor you are checking with the on-call attendant. Do not open.
- If they demand "just open the gate" without verification: refuse and re-ask for name + host.

EMERGENCY
- Police, fire, medical: tell them to hang up and dial 911. Do not treat this line as emergency dispatch. Do not open for a claimed emergency without verification for a normal visit.

EDGE CASES
- Forgot code / resident not answering: you cannot give codes. Suggest trying guest pass/code again, or having the host send a myQ guest pass. If they claim to be on tonight's list, verify with check_guest_list.
- CAM / management / ops calling (not a visitor at the gate): take a short message (name + reason) and call escalate_to_oncall with visit_type "ops". Do not open the gate unless post orders explicitly allow it for that person.
- Spam / solar / SEO / marketing: end the call politely and quickly. Call end_call.
- Language barrier or unintelligible audio: ask them to repeat once, slower. If still unclear → escalate_to_oncall, do not open.

TOOLS — WHEN TO CALL
- check_guest_list: after you have visitor name + host name/address (+ visit type if known). Always before open_gate.
- open_gate: ONLY after check_guest_list returned "approve". Never open unverified.
- escalate_to_oncall: ambiguous match, equipment issue, angry visitor, ops call, or open_gate failure.
- end_call: when the interaction is complete (opened, denied with clear next step, or spam).

TONE
- Calm, professional, brief. Sound like a security attendant, not a chatbot.
- Do not argue. Do not over-apologize. Do not promise opens you cannot complete.
```

If `{{community_name}}` is not supported in prompts, replace every `{{community_name}}` with `The Inlets` (or the human’s COMMUNITY_NAME) before saving.

---

## STEP 4 — Built-in end_call tool

Add built-in **End Call** tool if not already present.

- Name: `end_call`
- Description: `End the call when the visit is resolved (opened, denied with clear next step, spam, or emergency directed to 911).`

---

## STEP 5 — Custom function: check_guest_list

Add Custom Function / Custom Tool:

| Field | Exact value |
|-------|-------------|
| Name | `check_guest_list` |
| Description | `Verify a visitor against tonight's guest list / post orders. Call after collecting visitor name and host name or address. Always call this before open_gate.` |
| Method | `POST` |
| URL | `WEBHOOK_BASE/tools/check_guest_list` |
| Speak during execution | ON |
| Speak after execution | ON |
| Execution message | `Say briefly that you are checking the guest list.` |
| Timeout | 15000 ms if settable |
| Payload args only | OFF / disabled |

Parameters JSON schema — paste exactly:

```json
{
  "type": "object",
  "required": ["community_name", "visitor_name", "host_name_or_address"],
  "properties": {
    "community_name": {
      "type": "string",
      "description": "HOA / community name for this gate"
    },
    "visitor_name": {
      "type": "string",
      "description": "Full name of the person at the gate"
    },
    "host_name_or_address": {
      "type": "string",
      "description": "Resident full name and/or unit/address they claim to be visiting"
    },
    "visit_type": {
      "type": "string",
      "description": "guest, delivery, vendor, ops, or other",
      "enum": ["guest", "delivery", "vendor", "ops", "other"]
    }
  }
}
```

Save this tool before adding the next.

---

## STEP 6 — Custom function: open_gate

| Field | Exact value |
|-------|-------------|
| Name | `open_gate` |
| Description | `Request that the gate be opened. ONLY call after check_guest_list returned decision approve. Phase 1 notifies the on-call human to unlock in myQ.` |
| Method | `POST` |
| URL | `WEBHOOK_BASE/tools/open_gate` |
| Speak during execution | ON |
| Speak after execution | ON |
| Execution message | `Say you are opening the gate now and they should wait.` |
| Timeout | 20000 ms if settable |
| Payload args only | OFF |

Parameters:

```json
{
  "type": "object",
  "required": ["community_name", "visitor_name", "host_name_or_address", "reason"],
  "properties": {
    "community_name": {
      "type": "string",
      "description": "HOA / community name"
    },
    "visitor_name": {
      "type": "string",
      "description": "Verified visitor full name"
    },
    "host_name_or_address": {
      "type": "string",
      "description": "Verified host name or address"
    },
    "reason": {
      "type": "string",
      "description": "Short reason, e.g. guest list match for unit 12"
    },
    "entrance": {
      "type": "string",
      "description": "Gate / entrance id if known; default main"
    }
  }
}
```

---

## STEP 7 — Custom function: escalate_to_oncall

| Field | Exact value |
|-------|-------------|
| Name | `escalate_to_oncall` |
| Description | `Notify the human on-call attendant. Use for ambiguous matches, denials that need a human, ops calls, angry visitors, or failed opens. Do not open the gate yourself when escalating.` |
| Method | `POST` |
| URL | `WEBHOOK_BASE/tools/escalate_to_oncall` |
| Speak during execution | ON |
| Speak after execution | ON |
| Execution message | `Say you are checking with the on-call attendant.` |
| Timeout | 15000 ms if settable |
| Payload args only | OFF |

Parameters:

```json
{
  "type": "object",
  "required": ["community_name", "summary", "urgency"],
  "properties": {
    "community_name": {
      "type": "string",
      "description": "HOA / community name"
    },
    "visitor_name": {
      "type": "string",
      "description": "Visitor name if known"
    },
    "host_name_or_address": {
      "type": "string",
      "description": "Host name or address if known"
    },
    "summary": {
      "type": "string",
      "description": "One-sentence situation summary for the on-call human"
    },
    "urgency": {
      "type": "string",
      "enum": ["low", "normal", "high"],
      "description": "How urgently the human should respond"
    },
    "visit_type": {
      "type": "string",
      "enum": ["guest", "delivery", "vendor", "ops", "other"]
    }
  }
}
```

---

## STEP 8 — Optional agent webhook + keywords

If the agent has a webhook / post-call URL field, set:

`WEBHOOK_BASE/retell/webhook`

If boosted keywords exist, add: `gate`, `guest pass`, `myQ`, `attendant`, `delivery`, `vendor`, `unit`

If post-call analysis fields exist, add:
- `visitor_name` (string)
- `host_name_or_address` (string)
- `result` (enum: opened, pending_human_open, denied, escalated, abandoned, spam)
- `open_requested` (boolean)

---

## STEP 9 — Publish / save

Save and publish the agent. Confirm no draft-only state remains if the UI distinguishes draft vs live.

---

## STEP 10 — Phone number

1. Open Phone Numbers in Retell.
2. Buy a US number (or use an existing unused number).
3. Assign it to this agent only.
4. Copy the number and show it to the human.

If purchasing requires payment confirmation the human must approve: STOP and ask them to complete payment, then continue assignment.

---

## STEP 11 — Final report to human (required format)

Reply with exactly this structure:

```
RETELL INSTALL COMPLETE
Agent name:
Agent ID (if visible):
Phone number:
Webhook base used:
Tools configured: check_guest_list, open_gate, escalate_to_oncall, end_call
Dynamic variable community_name:

TEST CALLS (human should dial the Retell number):
1) APPROVE — say you are Jordan Lee visiting Sam Rivera (guest). Expect open request / SMS to on-call.
2) DENY — say you are Random Person visiting Nobody Unit 99. Expect deny + myQ guest pass instructions; no open.
3) ESCALATE — give unclear/conflicting names. Expect escalate; no open.

DO NOT point myQ tablet at this number until those 3 tests pass.
When OPEN SMS arrives, human unlocks gate in myQ Community app/portal.
```

---

## HARD RULES (never break)

1. Never invent a different webhook path than `/tools/check_guest_list`, `/tools/open_gate`, `/tools/escalate_to_oncall`, `/retell/webhook`.
2. Never leave `YOUR_WEBHOOK_HOST` or `example.com` in any URL.
3. Never configure the agent as a law firm / sales / appointment receptionist.
4. Never enable payments, calendar booking, or CRM lead-qualification flows.
5. Never open the gate without the `check_guest_list` → approve → `open_gate` sequence in the prompt.
6. If the UI label differs (e.g. “Custom Tool” vs “Custom Function”), use the closest match and still fill the same fields.
7. If you cannot find where to paste JSON parameters, use the visual parameter builder with the same property names and required fields — do not skip required fields.
8. If blocked by login, captcha, or payment: STOP and ask the human.

## RECOVERY

- Tool save fails on JSON: ensure top-level `"type": "object"` is present; remove trailing commas.
- Health check fails: tell human to restart `uvicorn` + `ngrok` and paste a new WEBHOOK_BASE; then update all 3 tool URLs.
- Agent ignores tools: confirm tool names match the prompt exactly: `check_guest_list`, `open_gate`, `escalate_to_oncall`, `end_call`.
