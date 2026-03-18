---
name: response-drafting
description: >
  Draft professional, empathetic customer-facing responses for the Quandri CS team.
  Pulls account context from HubSpot and tailors tone and content to the situation.
  Use when: draft a response to this customer, write a reply, respond to this ticket,
  help me reply, write an email to the customer, draft a follow-up, how do I respond to this.
---

# Response Drafting

Draft a customer-facing response tailored to the situation, the customer's plan tier, and the appropriate tone for the channel.

## Workflow

### Step 1 — Understand the situation

Gather (from context or by asking):
- What is the customer's issue or question?
- What is the current status? (investigating, resolved, needs more info, etc.)
- Is there a Linear issue or HubSpot ticket already open?
- Has the customer reached out before about this?

### Step 2 — Pull customer context from HubSpot

Look up the customer in HubSpot to retrieve:
- Company name and plan tier
- Account owner / named CSM
- Tone signals: are they a new customer, longtime client, renewal risk?
- Any previous correspondence on this issue

Use this to calibrate tone — Enterprise customers and renewal risks warrant extra care.

### Step 3 — Draft the response

Write a response following the tone and structure guidelines in `references/tone-guide.md`.

**Core principles:**
- Lead with empathy — acknowledge the impact before jumping to solutions
- Be specific — reference what you know about their situation
- Be clear on next steps — what happens next and by when
- Avoid jargon — write like a human, not a support bot
- Match urgency to priority — P1/P2 responses should feel urgent; P4 can be warmer and more casual

**Response types** (see `references/response-templates.md` for examples):
- `acknowledgement` — Issue received, being investigated
- `update` — Status update while work is in progress
- `resolution` — Issue resolved, here's what happened and what was fixed
- `needs-info` — You need more details to proceed
- `feature-request-received` — Thank them and set expectations
- `billing` — Handle with extra care; loop in CS lead if in doubt

### Step 4 — Review and send

Present the draft to the agent. Offer to adjust:
- Tone (more formal / more warm)
- Length (shorter / more detailed)
- Channel (HubSpot ticket reply vs. direct email)

Once approved, the response can be sent via HubSpot or drafted as a Gmail email.
