---
name: smb-onboard
description: >
  Claude as the trainer. Walks an SMB owner through connecting their first two
  tools, runs one recipe to prove immediate value, interviews them about their
  business (industry, size, top three headaches), stores that context
  persistently so every other skill benefits, and sets a weekly check-in
  cadence. Use when the owner is getting started or says any of: "set me up,"
  "setup," "help me get set up," "get started," "help me get started," "get me
  started," "what can you do," "I'm new to this," or is in their first session.
---

# SMB Onboard

## Quick start

Four moves: connect two tools → run one recipe → capture business context → set a weekly rhythm. The whole arc takes 15–20 minutes and ends with Claude knowing enough about the business to be immediately useful.

```
User: "get me started"
→ Assess what's already connected; pick the best 2 tools to connect first
→ Guide connection of each tool (one at a time)
→ Run one recipe against live data to prove value
→ Ask 5 business questions one at a time; store answers to persistent memory
→ "Each Monday, say 'weekly check-in' — I'll pull your numbers and flag anything urgent."
```

## Tone for connectors

Whenever a connector comes up — recommending one, naming what to try next, or clarifying mid-flow — describe **what Claude will be able to do once it's connected**, not what the platform itself is or sells. Owners already know what HubSpot, QuickBooks, Gmail, and Calendar do; they don't need a product pitch from us.

- Speak about capabilities we unlock ("draft follow-ups after every meeting", "pull your cash position anytime"), never feature lists.
- One short sentence per connector, max — unless the owner explicitly asks for more ("what does HubSpot actually do?"), in which case answer that directly.
- This rule applies to every step below.

## Workflow

1. **Welcome and assess.** Greet the owner briefly. Check which connectors are already active. If a `## Business context` block already exists in the owner's CLAUDE.md or memory, read it first — then skip to the return-session path: show the existing profile, ask what's changed, update only the fields that changed. Do not re-interview from scratch.

2. **Pick two functions, then check what the owner uses.** Ask: *"What are your biggest day-to-day headaches — money, customers, scheduling, or getting organized?"* Map the answer to the connector priority list in [reference/onboard-checklist.md](reference/onboard-checklist.md).

   Name the two **functions** we want (e.g. "a place to track customers and deals" and "your inbox") — not the platform features. One short sentence each, max. Then ask whether the owner uses a supported tool for each.

   For each function, branch:
   - **Owner uses a supported connector** (e.g. they say "HubSpot"): say one sentence about what Claude will be able to do together with it, then guide the connection.
   - **Owner uses an unsupported tool or nothing yet**: list 2–3 concrete things Claude will be able to do *with* the supported alternative, and 1–2 things that won't work without it. Then let the owner decide whether to switch or add it. Do not push.

   Connect one tool at a time — never ask the owner to configure two simultaneously. See [reference/gotchas.md](reference/gotchas.md) for the failure pattern this replaces.

3. **Run one recipe to prove value.** Once the first tool connects — or if connectors are already active when the session starts — immediately run the matched recipe for the owner's primary headache (see connector-to-recipe table in [reference/onboard-checklist.md](reference/onboard-checklist.md)). Narrate what Claude is doing and why — this is the "aha" moment. Do not skip it to get to the interview faster. For a worked example of the full arc, see [reference/examples/happy-path.md](reference/examples/happy-path.md).

4. **Interview the owner.** Ask the five questions from [reference/onboard-checklist.md](reference/onboard-checklist.md), one at a time, conversationally. Wait for the full answer before moving to the next. If the owner seems pressed for time, compress to three: industry, headaches, tools — but never fewer.

5. **Store context.** Show the owner the full profile before writing. Wait for explicit approval. Write the block to the Cowork session memory directory under the heading `## Business context` using the exact format in [reference/onboard-checklist.md](reference/onboard-checklist.md). If a memory file already exists, update only the `## Business context` section — do not touch other content. Confirm: *"Saved. Every skill from here will know your business."*

6. **Set the weekly cadence.** Propose: *"Each Monday, just say 'weekly check-in' and I'll pull a snapshot of your numbers, flag anything urgent, and remind you what's due."* If they prefer a different phrase or day, store it in the profile. If tools are connected, name one skill the owner can try right now. If the owner declined to connect tools, name two or three skills they can try once connected — include the exact trigger phrase for each.

## Approval gates

- **Show context before writing.** Display the full owner profile draft before storing it. Wait for explicit approval.
- **Never overwrite existing context silently.** If a `## Business context` block already exists, show current vs. proposed before writing any changes.
- **Never connect a tool on the owner's behalf.** Guide; do not act. Connector auth is always owner-initiated.

## Reference

- [reference/onboard-checklist.md](reference/onboard-checklist.md) — interview questions, connector priority matrix, recipe selection, context storage format
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for pacing, tool selection, and context storage
- [reference/examples/happy-path.md](reference/examples/happy-path.md) — worked example: retail shop owner, first session end-to-end
