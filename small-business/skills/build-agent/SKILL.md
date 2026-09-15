---
name: build-agent
description: >
  Turns a task the owner keeps doing by hand into a named, reusable skill they
  can trigger by name or put on a schedule. Watches them do it once or listens
  to them describe it, works out what varies and what stays fixed, writes the
  skill with approval checkpoints in the right places, registers it with the
  router, and shares it with the team. This is how a business gets a workflow
  nobody shipped for them. Use this whenever the owner describes something
  repetitive they wish were automatic — including phrasings like "I do this
  every week," "can you remember how to do this," "make this a thing I can just
  ask for," "build me an agent," "automate this for me," "turn this into a
  workflow," or "I want this to happen every Monday." Reach for it when they
  describe a routine, even without asking for automation.
allowed-tools: Read, WebFetch
---

# Build Agent

Turn something the owner does every week into something they ask for by name.

This is what keeps the plugin from having to ship every industry's workflow. No catalog can cover a septic contractor's permit routine or an insurance agency's carrier commission reconciliation. Those owners can build them.

## Step 1 — Watch it happen, or hear it described

Two starting points, and the first is much better.

**Best: they just did it in this conversation.** If the owner has walked through the task with you — pulled the files, made the decisions, corrected you twice — that transcript is the specification. Extract it rather than re-interviewing them. The corrections they made are the most valuable part, because they encode judgment the owner would never have thought to state.

**Otherwise: they describe it.** Ask them to walk through the last time they did it, concretely. Real specifics beat an abstract description every time — "last Tuesday I pulled the carrier file, matched it against what we'd booked, and chased six discrepancies" tells you more than "I reconcile commissions."

Read `reference/capture.md` for how to get a complete picture without an interrogation.

## Step 2 — Separate what varies from what stays fixed

This is the whole craft of the step. A skill that hardcodes last Tuesday's specifics only works on last Tuesday.

For each part of the task, decide:

- **Fixed** — the sequence, the sources, the output format, the rules
- **Varies** — dates, names, amounts, which file, which customer
- **Judgment** — the parts where the owner decides, which become approval gates

The corrections the owner made while walking through it usually mark the judgment points. When someone says "no, not that one — we skip anything under USD 50," that is a rule. When they say "hmm, depends," that is an approval gate.

## Step 3 — Find the approval gates

Every step that sends, spends, publishes, or deletes needs a gate. So does every step where the owner hesitated.

Do not gate everything — a skill that asks permission nine times is worse than doing it by hand. Gate the consequential and the ambiguous, and let the rest run.

Read `reference/skill_authoring.md` for where gates belong and how to phrase them.

## Step 4 — Write it

Produce a real skill in the same shape as everything else in this plugin: a `SKILL.md` with frontmatter and numbered steps, plus a `reference/` folder if the detail warrants it.

Requirements it must meet, same as every shipped skill:

- Name and folder match, lowercase with hyphens
- Description says what it does **and** when to trigger, in third person
- A real fallback for when a connector is missing
- Approval gates on anything consequential
- Never invents a number; missing data is reported as missing

**Write it in the owner's terms, not in generic business language.** If they call it "the carrier file," the skill says carrier file. A skill full of unfamiliar vocabulary is one they will not trust to run unattended.

## Step 5 — Test it on a real case, before they rely on it

Run the new skill against a case the owner already knows the answer to — ideally the exact one they walked through. Show the output next to what they got by hand.

This is the step that determines whether the skill gets used. An owner who has seen it reproduce a known-good result will schedule it. One who hasn't will run it manually and check it every time, which saves nothing.

If it doesn't match, fix the skill and run it again. Do not ask the owner to accept a near-miss.

## Step 6 — Register and set the cadence

Add it to `smb-router` so plain-English requests reach it, and record the trigger phrases the owner actually uses.

If it is a recurring task, offer to schedule it. Scheduling is what converts "a skill I could run" into "something that happens without me," which is the outcome they wanted.

## Step 7 — Share it, with approval

Offer to share with the team. Say what sharing means: who gets it, what data it can reach, and what it can do unattended.

**Be specific about the risk when a skill sends, spends, or writes.** A skill that emails customers, running for someone who did not build it and does not know its assumptions, is a real hazard. Recommend draft-only for shared skills that send anything.

## What not to do

- **Do not re-interview about a task they just walked through.** The transcript is the spec.
- **Do not hardcode the example.** Names, dates, and amounts vary; the sequence does not.
- **Do not gate every step.** Nine approvals is worse than doing it by hand.
- **Do not skip the test run.** An untested skill gets checked manually forever, which saves nothing.
- **Do not write it in generic business language.** Their words, or they won't trust it.
- **Do not build something that sends or spends without approval gates.** Ever, regardless of what the owner asks for.

## After the build

The owner now has a named skill they can trigger or schedule. If the new skill hit a tool that isn't connected, "connect to my ERP" (`build-connector`) is the natural next step — it turns the missing system into a working source. Also nearby: "brief me" to fold the new output into the daily picture, and "Monday brief" if the skill should feed the weekly one. Offer at most three, and skip any offer the owner already declined this session.

## Reference files

- `reference/capture.md` — getting a complete picture of the task without an interrogation
- `reference/skill_authoring.md` — the structure, frontmatter, and where approval gates belong
- `reference/gotchas.md` — the failure modes that produce a skill nobody uses
