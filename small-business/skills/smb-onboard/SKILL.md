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

Four moves: identify the two functional categories the owner needs → learn what they already use for each and set up the data path (connector, CSV, or paste) → run one recipe to prove value → capture business context → set a weekly rhythm. The whole arc takes 15–20 minutes and ends with Claude knowing enough about the business to be immediately useful.

```
User: "get me started"
→ Map their headaches to the two functional categories that matter most
→ Ask what they currently use for each — do not recommend brands
→ Branch on the answer:
   (a) Supported connector → walk through auth
   (b) Alternative tool they use → describe the CSV/manual path
   (c) Nothing yet → CSV/paste path + list of skills that won't run
→ Run one recipe against whatever data path is live
→ Ask remaining business questions; store to persistent memory
→ "Each Monday, say 'weekly check-in' — I'll pull your numbers and flag anything urgent."
```

## Voice and register

Onboarding is a setup conversation, not a sales pitch. The owner needs to understand what Claude needs and why — not why one tool is better than another. Rules apply to every message in this skill:

- **Recommend functional categories, not connectors.** "A CRM" / "bookkeeping software" / "your calendar" — not "HubSpot" / "QuickBooks" / "Google Calendar." Connector names only appear after the owner discloses what they use, or as a single informational line in branch (c) of Step 3.
- **No marketing language.** Forbidden phrases include: "source of truth," "unlocks," "single highest-leverage," "stage your week," "the better pair," "direct hit," "supercharge," "seamless," "easy to set up," "free tier," "powerful," "trusted by," "one place for everything." If a sentence would pass as a line on a vendor landing page, rewrite it.
- **No bolded brand names.** Bold the functional category instead.
- **Cost mentioned only when asked.** If the owner asks what a tool costs, answer plainly. Do not mention pricing tiers, free versions, or paid upgrades on Claude's initiative.
- **One sentence on what you'll use the data for.** Describe what Claude will *do* with it (function), not what the tool *does* (features).

## Workflow

1. **Welcome and assess.** Greet the owner briefly. Check which connectors are already active. If a `## Business context` block already exists in the owner's CLAUDE.md or memory, read it first — then skip to the return-session path: show the existing profile, ask what's changed, update only the fields that changed. Do not re-interview from scratch.

2. **Identify the two categories.** Ask: *"What are your biggest day-to-day headaches — money, customers, scheduling, or getting organized?"* Use the [reference/onboard-checklist.md](reference/onboard-checklist.md) headache-to-category matrix to translate their headaches into two functional categories.

   Present those two categories to the owner — **do not name brands at this step**. One sentence per category on what Claude would use the data for, then ask what they use today.

   Example:

   > For those two, here's what I'd want access to:
   >
   > A CRM — somewhere structured to keep contacts, deals, and conversations so I can prioritize who needs attention.
   >
   > Your inbox — so I can read what customers are asking and surface unanswered threads.
   >
   > What are you using for each, if anything?

3. **Branch on what the owner uses.** For each category, the owner's answer falls into one of three branches. Walk one category at a time — never set up two data paths simultaneously.

   **(a) Supported connector** (e.g. "HubSpot," "QuickBooks Online," "Gmail"). → *"Got it — that's a supported connector. I'll walk you through connecting it."* Guide auth.

   **(b) Alternative tool they already use** (e.g. "Xero," "Pipedrive," "spreadsheet"). → Describe the CSV/manual path for the skills they'll touch. Be honest about the friction: *"No direct connector for Xero, but you can export CSVs and I'll work from those. A few skills will need the manual export each time — I'll flag those as they come up."*

   **(c) Nothing yet.** → *"OK — you can still use most of this, you'll just hand me the data each time instead of me pulling it. For [category], that means uploading a CSV (or pasting numbers in chat) when you want to use a skill that needs it."* Then name explicitly:

   - Skills with built-in CSV/paste support that will work for them (see per-category list in [reference/onboard-checklist.md](reference/onboard-checklist.md)).
   - Skills that require live structured data and won't run until they have a tool in this category.

   End with one informational line: *"If you want to add a [category] later, the supported connector here is [brand]."* No further commentary on the brand.

4. **Run one recipe to prove value.** Once the first data path is live (connector OR CSV upload OR pasted data), immediately run the matched recipe for the owner's primary headache (see recipe table in [reference/onboard-checklist.md](reference/onboard-checklist.md)). Narrate what Claude is doing and why — this is the "aha" moment. Do not skip it to get to the interview faster. For a worked example of the full arc, see [reference/examples/happy-path.md](reference/examples/happy-path.md).

5. **Interview the owner.** Ask the remaining questions from [reference/onboard-checklist.md](reference/onboard-checklist.md), one at a time, conversationally. **Skip question 4 (Tools already in use) — Step 2 covered it.** Ask questions 1, 2, 3, and 5. Wait for the full answer before moving to the next. If the owner is short on time, compress to questions 1 and 3 — those feed the most downstream skills.

6. **Store context.** Show the owner the full profile before writing. Wait for explicit approval. Write the block to the Cowork session memory directory under the heading `## Business context` using the exact format in [reference/onboard-checklist.md](reference/onboard-checklist.md). If a memory file already exists, update only the `## Business context` section — do not touch other content. Confirm: *"Saved. Every skill from here will know your business."*

7. **Set the weekly cadence.** Propose: *"Each Monday, just say 'weekly check-in' and I'll pull a snapshot of your numbers, flag anything urgent, and remind you what's due."* If they prefer a different phrase or day, store it in the profile.

   Then name **only the skills the owner can actually run right now** given their current data paths (connectors + CSV/paste). Do not list skills that require a tool the owner doesn't have — those were surfaced in Step 3 as not-yet-available. Include the exact trigger phrase for each skill named.

## Approval gates

- **Show context before writing.** Display the full owner profile draft before storing it. Wait for explicit approval.
- **Never overwrite existing context silently.** If a `## Business context` block already exists, show current vs. proposed before writing any changes.
- **Never connect a tool on the owner's behalf.** Guide; do not act. Connector auth is always owner-initiated.
- **Never recommend a brand.** Brand names appear only in response to what the owner discloses (branch a/b) or as one informational line in branch (c). No comparative claims, no nudges to switch tools.

## Reference

- [reference/onboard-checklist.md](reference/onboard-checklist.md) — interview questions, headache-to-category mapping, category-to-brand reference, recipe selection, per-category CSV-capable skill lists, context storage format
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for tone, pacing, brand-mention discipline, context storage
- [reference/examples/happy-path.md](reference/examples/happy-path.md) — worked example: retail shop owner, first session end-to-end
