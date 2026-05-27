---
name: trigger-pipeline
description: Identify B2B Mittelstand leads from fresh triggers — new VP Sales / GM in the last 90 days, VP Sales role open 8+ weeks, recently funded consulting/transformation, milestone anniversaries. Trigger when the user says "find leads from this week's news", "trigger-based prospecting", "hiring signal leads", "fresh prospects in [region]", or asks for accounts based on a specific event signal. Returns a scored, ICP-filtered candidate list with the trigger evidence inline.
---

# Trigger Pipeline

Signal-driven lead identification. Instead of working evergreen lists, this skill surfaces accounts where **something just happened** that opens a brief window of high receptivity — typically the first 90 days after a leadership change, a funded initiative, or a public commitment.

This is the source-of-leads step that feeds the `cold-outreach-welle` and `sniper-leads` skills.

## When to fire

Trigger on phrases like:

- "find leads from this week's news"
- "hiring-signal leads"
- "trigger-based prospects for [region]"
- "fresh prospects in [segment]"
- "who's hired a new VP Sales lately"
- "build the trigger pipeline for KW [N]"

## The four trigger types (priority order)

| # | Trigger | Receptivity window | Why it works |
|---|---|---|---|
| **T1** | New VP Sales / GM appointed <90 days ago | 90 days | New role-holder is building their first 90-day plan; receptive to new tooling and outside perspective |
| **T2** | VP Sales / Head of Sales role posted 8+ weeks | Open-ended while role is open | Capacity gap is acute; revenue is exposed; interim cover often welcomes outside help |
| **T3** | Funded consulting / transformation initiative (publicly announced) | 6 months from announcement | Budget is committed; gatekeeper has authority to engage; competing implementers want a slot |
| **T4** | Milestone anniversary (25 / 50 / 75 / 100 years) | 12 months around the date | Storytelling moment; companies invest in revenue modernization to mark the occasion |

For T1 the window matters most — receptivity at day 30 is roughly 3-5x receptivity at day 270 in the same role, based on our field data.

## ICP gate (every trigger hit goes through this)

A trigger is necessary but not sufficient. After surfacing a trigger hit, run the candidate through the ICP gate before adding to the pipeline:

| Gate | Pass criterion |
|---|---|
| **HG-1 — Industry** | Manufacturing SME (machine building, tooling, plastics, metalworking, electronics, automation) |
| **HG-2 — Size** | 30-250 employees |
| **HG-3 — Region** | Within the user's defined target region |
| **HG-4 — Group structure** | Not a procurement-centralized subsidiary of a >500-FTE group |
| **HG-5 — Reachable** | Has a working web presence and a verifiable email path |

Fails any one of these → drop. Don't soften the gate to pad the pipeline.

## Soft gates (scoring layer, 0-10)

After the hard gates, score 0-10 for prioritization:

- +2 if the trigger is T1 or T2 (vs T3 / T4)
- +2 if there's a documented data asset (long-running ERP, structured CRM, archive of bids)
- +2 if there's a visible pressure signal (industry transition, export uncertainty, generational change)
- +1 if the decision-maker has a sales (not engineering) background
- +1 if the decision-maker posts publicly about revenue/sales efficiency

Score 9-10 → priority of the cold-outreach queue
Score 7-8 → standard wave inclusion
Score 5-6 → borderline; manual review
Score ≤4 → drop

## Output format

```markdown
## Trigger Pipeline — [Date] — [N candidates]

### Priority (score 9-10)

#### 1. [Company] · [City] · [FTE]
- **Trigger:** T1 — [Name] appointed [Role] on [Date]; source: [URL]
- **ICP score:** 9 (HG ✓✓✓✓✓ · SG ✓✓✓)
- **Pain hypothesis:** [1-line, based on what the new role-holder is likely solving]
- **Decision-maker:** [Name, Role, contact path]
- **Suggested approach:** [sniper / wave]

### Standard (score 7-8)
… same structure …

### Dropped (with reason)
| Company | Trigger | Drop reason |
|---|---|---|
| … | … | HG-4 group screen |
```

## Sourcing channels

This skill is tool-agnostic. Useful sourcing channels in DACH:

| Channel | Trigger types it surfaces | Notes |
|---|---|---|
| **LinkedIn search** (role + region + posting date) | T1 (new appointments), T2 (open roles) | Free-tier sufficient at low volume; Sales Navigator pays off above ~50 candidates/week |
| **LinkedIn company-page mining** | T1 (announcements), T3 (funded initiatives) | Web-scraping framework helps at scale |
| **Trade press / industry news** | T3, T4, milestone announcements | Free; one or two outlets per industry is enough |
| **Public registry / Bonität** | T4 (anniversaries), structural change | Quarterly cadence — not high-frequency |
| **Google Alerts** keyed to role titles + region | T1 (appointments mentioned in press) | Set once, deliver to inbox |
| **Chamber-of-commerce reports** | T3, industry signals | Quarterly publication |

## Volume targets (small consulting practice)

- **10-15 trigger hits** identified per week (source step)
- **3-5 ICP-qualified** after the gate (typical 30-40% pass rate)
- **3-5 cold-outreach drafts** in the next wave
- **1-2 conversations** booked per 4 weeks

Below these → tighten the sourcing channels. Above → upgrade tooling (Sales Navigator at ~50 hits/wk; managed scraping at ~150 hits/wk).

## Anti-patterns

1. **Trigger without ICP gate** — leads to outreach into accounts that look exciting but won't buy
2. **ICP gate without trigger** — leads to evergreen list grinding; response rates collapse
3. **Padding the pipeline** by widening the gates when sourcing comes up short — better to source one more channel
4. **T3/T4 only** with no T1/T2 — the trigger is too soft; you'll write good mail to lukewarm prospects
5. **Same trigger-type repeated across waves** — diversify across T1/T2/T3 so the pipeline doesn't depend on one signal

## Companion skills

- `sniper-leads` — when 2-3 hits from T1 stand out, route them to sniper treatment instead of the wave
- `cold-outreach-welle` — when 5-10 hits cluster in the same week, batch them into a wave
- `outreach-tuning` — apply the V2 pattern to whichever drafts result
