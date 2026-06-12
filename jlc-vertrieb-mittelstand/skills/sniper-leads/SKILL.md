---
name: sniper-leads
description: Build a "sniper" list — 2-3 named B2B Mittelstand accounts that score 8+/10 on the ICP gate AND carry a fresh trigger, each with a hand-built per-account first touch. Trigger when the user says "3 sniper accounts", "top ICP fits this week", "build a sniper list", "best 3 accounts to chase", or wants high-precision named-account targeting instead of a wave. Output includes per-account pain analysis, decision-maker map, approach path, and first-touch draft.
---

# Sniper Leads — Named-Account, High-Precision Outreach

The sniper pattern is the opposite of the wave. A wave ships 5-10 drafts that share structure; a sniper list ships 2-3 drafts that share **no** structure — each one is hand-built end-to-end against everything the user knows about that single account.

Use this skill when the user wants their highest-confidence accounts handled individually, not batched.

## When to fire

Trigger on phrases like:

- "3 sniper accounts"
- "build a sniper list"
- "top ICP fits this week"
- "best 3 accounts to chase"
- "named-account targeting"
- "warm-cold hybrid"
- "GTM sniper — [date]"

Do NOT fire for:

- Wave-sized batches (5-10) → use `cold-outreach-welle`
- Pure cold-list sourcing (no pre-vetted candidates) → use `trigger-pipeline`

## Inputs the user owes you

1. **Candidate set** — typically 5-10 accounts the user has already noticed (Notion pipeline tagged `Active=YES, Status=Neu`, or a hand-curated list). Sniper-skill picks the top 2-3 from this set.
2. **Constraint set** — region, industry, anything off-limits
3. **Approach budget** — how much time the user has to invest in the touches (60 minutes for the batch is enough; 4 hours produces noticeably better drafts)

## What "sniper" means

Three commitments per account:

1. **Decision-maker named by full name + role + tenure** — not "Geschäftsführer", not "Vertriebsleitung". If the name isn't reachable in 5 minutes of imprint + LinkedIn search, the account drops out.
2. **Pain hypothesis sourced from at least two independent signals** — a LinkedIn post AND a trade-press item, or a press release AND a chamber report. One-signal pain hooks belong in waves, not snipers.
3. **Approach path chosen explicitly** — cold-mail vs LinkedIn-DM vs phone vs hybrid. The choice is per-account, based on the decision-maker's surface (active on LinkedIn → DM; quiet online → mail; long-tenured founder type → phone with a personal-named opener).

## Scoring (8+/10 to qualify as sniper)

Each candidate scores out of 10:

- **+3 if all hard gates pass** (industry / size / region / not-a-subsidiary / reachable)
- **+2 if the trigger is T1 or T2** from the `trigger-pipeline` taxonomy
- **+2 if there are at least 2 soft gates** firing (pressure signal, data asset, sales-background decision-maker, investment signal)
- **+1 if there's a regional or network bridge** (chamber, industry cluster, mutual contact)
- **+1 if the decision-maker is publicly visible** (LinkedIn-active, press-quoted, conference-speaker)
- **+1 if the engagement timing is right** (funded budget, fiscal-year start, mid-cycle for their typical buying season)

Below 8 → don't sniper. Either route to a wave (if a working email exists) or back to the trigger pipeline.

## Output format

For each of the 2-3 selected accounts:

```markdown
## #N — [Company Name]

| Field | Content |
|---|---|
| **Company** | [Full name] · [Industry sub-segment] · [City], [Region] · [FTE] · founded [Year] |
| **Decision-maker** | [Name], [Role] (since [Year]) · [Contact path: phone / LinkedIn / verified email] |
| **Pain signal** | [Source #1 with date] + [Source #2 with date] |
| **ICP match** | **[Score]/10** — [terse list of which gates fire] |
| **Approach path** | [Cold-mail / LinkedIn-DM / Phone / Hybrid] — [why this choice for this DM] |
| **Funding story** | [How the engagement could be structured, including any applicable public funding mechanisms] |
| **First touch (draft)** | [Full draft of the first touch, in the chosen channel] |

```

After the per-account blocks, produce a **batch overview table**:

```markdown
| # | Company | Region | Industry | FTE | Score | Trigger | Approach | Send day |
|---|---|---|---|---|---|---|---|---|
```

And a **next-steps plan** for the user:

- Per account: send-day + channel + follow-up date if no reply
- A fallback for each (if cold mail bounces / LinkedIn DM gets ignored)

## Approach-path heuristics

| Decision-maker profile | First touch |
|---|---|
| LinkedIn-active, posts about sales/revenue | LinkedIn DM (warm-cold hybrid) |
| LinkedIn-quiet, named in imprint | Cold mail to verified address, named in subject |
| Long-tenured founder/family GM, phone-listed | Phone call with a specific-anchor opener (a recent press item, an anniversary) |
| Recently appointed (T1 trigger) | Cold mail with the appointment as anchor, low-friction CTA |
| Multi-brand / multi-country company | Cold mail referencing the structural challenge (synchronization across brands, integration after acquisition) |

## Risk register per account

Sniper drafts include a 2-3-line risk register: what could make this account not respond, and what the fallback touch looks like. Examples:

- "Decision-maker may filter outside-consultant requests by default → fallback via chamber-of-commerce referral or mutual-contact intro"
- "Multi-generational family business may be conservative about engaging consultants → fallback emphasizes regional / industry peer references and downplays methodology jargon"

## Anti-patterns

1. **Snipering 5+ accounts at once** — produces wave-quality, not sniper-quality. Cap at 3.
2. **Mass-personalization** — same body, different first paragraph. Fails the V2 check and reads as wave-grade mail.
3. **Hidden region anchor** — at sniper-level, the regional connection should be in the **first sentence** if any geographic proximity exists.
4. **Phone-first for online-active DMs** — the channel mismatch reads as "outside the loop"
5. **No risk register** — if you don't know what could go wrong, you don't know the account well enough yet

## Typical pipeline value

For a small consulting practice working DACH Mittelstand:

- 3 snipers → 3 well-crafted touches → 1-2 conversations
- 1 conversation → typically 1 audit-tier engagement (small fixed scope) + 30-40% chance of follow-on operator engagement
- Across a quarter: 3 sniper batches → 18-25k revenue baseline + 30-50k follow-on potential

These numbers are for a single-consultant practice. Scale up only by adding consultants, not by widening the sniper batch.

## Companion files

- `example-icp.md` — three anonymized example sniper accounts showing the full output shape (different industries, different approach paths, different decision-maker profiles)
