---
name: cold-outreach-welle
description: Build the next cold-outreach wave for B2B Mittelstand prospecting. A "wave" is a small named batch of 5-10 accounts shipped together, not a sequence. Trigger when the user says "build wave N", "next outreach batch", "5-10 prospects this week", "build the next wave", or describes a small batch of manufacturing-SME accounts to write to. Produces per-account drafts that pass the V2 tuning checklist (region-anchor, named pain in first paragraph, brand-word prominent, substance anchor at end) — never a bulk sequence.
---

# Cold-Outreach Welle (Wave-Based Cold Outreach)

A **Welle** ("wave") is a small named batch of cold-outreach drafts shipped together — usually 5-10 accounts in the same week, sharing the same ICP profile but with per-account personalization. Waves are the opposite of sequences: each draft is hand-built against a verified pain hook, then all of them ship within a few days.

This skill produces a wave when the user describes a batch they want to write. It enforces the gating rules a small DACH B2B sales practice refined across four months of weekly waves.

## When to fire

Trigger on phrases like:

- "build wave 7"
- "next outreach batch"
- "10 prospects this week from [region/segment]"
- "I have these [N] accounts — write cold mails for them"
- "build the next welle"
- "outreach drafts for [ICP segment]"

Do NOT fire for:

- Single ad-hoc cold mails (use the parent `sales:draft-outreach` skill instead — this skill is wave-specific)
- LinkedIn DM drafting (separate channel — see `outreach-tuning`)
- Reply drafting on existing threads

## Inputs the user owes you

Before producing drafts, confirm:

1. **Wave number / label** — for logging ("Wave 7, KW 24/2026")
2. **Target segment** — industry, employee band, geography
3. **Account list** — names of accounts the user has already pre-vetted, OR a request to source them (then use the `trigger-pipeline` skill first)
4. **Send window** — which days the user plans to send (this drives the order in which drafts are produced)

If any of these are missing, ask in one combined question — don't drip-ask.

## The wave gates (must pass before drafting starts)

For every account on the list, verify:

| Gate | Check | Action on fail |
|---|---|---|
| **HG-1 — Industry fit** | Manufacturing SME (machine building, tooling, plastics, metalworking, etc.) | Drop from wave |
| **HG-2 — Size fit** | 30-250 employees (below: too small for the typical engagement; above: parent-group risk and longer sales cycle) | Drop from wave |
| **HG-3 — Region fit** | Within the consultant's defined target region | Drop from wave |
| **HG-4 — Group check** | Not a subsidiary of a larger group with central procurement | Drop from wave; log as group-screened |
| **HG-5 — Working email** | Verified via imprint / DNS / WHOIS — generic `info@` for group domains is a bounce trap | Replace address or drop |

If 2+ accounts get dropped on any single gate during sourcing, suggest a wider sourcing pass (use `trigger-pipeline`) rather than padding the wave with weak fits.

## The V2 tuning checklist (every draft must pass before delivery)

Every draft in the wave gets a 5-point check. If any single point fails, the draft goes back into tuning — it does not ship.

- [ ] **Region anchor** in the subject OR first paragraph (not buried in the signature)
- [ ] **Named pain** in the first paragraph (specific to this company, sourced from a verifiable signal — LinkedIn post, press release, hiring page, trade-show schedule, M&A news). Generic industry-pain is a fail.
- [ ] **Brand word** ("[your-brand way of saying it]" — e.g. "Vertrieb neu denken") prominent in subject OR first paragraph, not hidden mid-body
- [ ] **Substance anchor** (years of background, certifications, named references) **at the END**, kept short. Substance anchors at the top read as generic-consultant.
- [ ] **Subject ≤ 60 characters**, no clickbait, no fake `Re:` / `Fwd:` tricks

See `examples/welle-template.md` and `outreach-tuning/SKILL.md` for the full V2 pattern.

## Output format

For each account in the wave, deliver:

```markdown
### [Account #N]: [Company Name] ([City], [Employees])
**Send day:** [Mon/Tue/Wed]
**Recipient:** [First Last, Role] — [verified email]
**Pain hook:** [1-line summary of the verifiable signal, with source + date]

---

**Subject:** [≤60 chars, region + pain stub + brand word]

**Body:**
[Paragraph 1 — Pain, in 1-2 sentences, naming the verifiable signal]

[Paragraph 2 — Region anchor + brand word + 1-line value frame]

[Paragraph 3 — Substance anchor, short]

[Paragraph 4 — CTA: low-friction 20-minute slot, named days/times if known]

---
```

After all accounts, output a **wave summary table**:

```markdown
| # | Company | City | MA | Send day | Pain source |
|---|---|---|---|---|---|
| 1 | … | … | … | … | … |
```

And a **disqualification log** (companies that were sourced but dropped, with reason — useful for the user's wiki/audit).

## What this skill does NOT do

- Does **not** auto-send. All output is draft-only. The user reviews and clicks send manually.
- Does **not** invent pain hooks. If a verifiable signal cannot be found for an account, the account is dropped from the wave, not "filled in" with generic industry pain.
- Does **not** exceed ~10 accounts per wave. Larger batches lose the per-account specificity that makes the pattern work.
- Does **not** template more than 50% of the body. Each draft must have a per-company first paragraph; only the region/substance/CTA blocks may be reused.

## Companion patterns

Two helper patterns ship alongside this skill:

- `pattern-trigger-mining.md` — how to source verifiable pain hooks (LinkedIn-page mining, press-release scraping, trade-show schedules)
- `pattern-pattern-verify.md` — how to verify a working email address before sending, to avoid the `info@group-domain.com` bounce trap

## Volume cap

Hard cap: **30 cold-outreach touches per consultant per week**, including this wave plus any cold calls and LinkedIn messages. The pattern breaks above that — drafts get generic, follow-ups slip, response quality drops. If the user pushes for more, push back: suggest a second wave next week instead.

## Reply-watch cascade

After the wave ships, set three watch points on the user's calendar (named explicitly so the user can copy them in):

- **+5 working days** — first sweep for replies, opens, bounces
- **+10 working days** — second-touch decision window (shortened follow-up, single question)
- **+15 working days** — final classification (positive reply / negative reply / no reply → 30-day cold park)

## Anti-patterns this skill blocks

1. **Bulk personalization** — merge tags into the same template body. Fails the V2 check.
2. **Buzzword spam** — "disruptive", "synergetic", "AI-powered". Fails the substance check.
3. **`info@group-domain.com`** when a working `info@subsidiary-domain.de` exists. Bounces, wastes the wave.
4. **Hiding the region anchor** in the signature. Fails the V2 check.
5. **Front-loading the substance** ("As a consultant with 20 years of…"). Reads generic. Substance goes at the end.

## Why waves and not sequences

A sequence assumes the second and third touches do most of the work and the first touch only has to be inoffensive. The DACH Mittelstand inverts this: the first touch is where the prospect decides whether to read further at all. Sequences also normalize a generic-feeling first email, because the writer expects the follow-up to land. A wave forces every first touch to carry its own weight.
