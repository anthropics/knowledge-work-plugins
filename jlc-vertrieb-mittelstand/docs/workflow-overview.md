# End-to-End Workflow

How the four skills fit together for a typical week of outreach.

## The weekly rhythm

```
Monday morning      → trigger-pipeline (60-90 min)
                       Source 10-15 trigger hits, score against ICP,
                       short-list to 5-8 for the week's wave.

Monday late morning → sniper-leads (60 min)
                       If 2-3 of the trigger hits score 9-10,
                       lift them out and treat them as snipers
                       instead of folding them into the wave.

Mon-Tue afternoon   → cold-outreach-welle (90-120 min)
                       Build 5-8 drafts for the wave. Each goes
                       through trigger-mining + email-verify
                       + V2 tuning before it lands in Drafts.

Tuesday late        → outreach-tuning (45-60 min)
                       Run every draft (wave + snipers) through
                       the 10-point checklist. Revise or drop.

Wed-Thu             → SEND (manual — the plugin never auto-sends)
                       3-4 drafts per send-day, spaced across
                       Wednesday and Thursday.

Friday              → reply watch + log
                       Check bounces, reply triage. Log results
                       in your CRM/pipeline. Identify wave-level
                       patterns for next week.
```

Total operating cost: 5-7 hours per week of senior consultant time.

Output: 5-10 cold touches per week + 2-3 sniper touches per week = ~10 cold-outreach touches sent per week, well under the 30-per-week volume cap.

## The skill-graph

```
                  ┌──────────────────────┐
                  │  trigger-pipeline    │
                  │  (source leads)      │
                  └────┬─────────────────┘
                       │ scored, ICP-filtered candidates
                       │
              ┌────────┴───────────┐
              │                    │
              v                    v
   ┌──────────────────┐  ┌──────────────────┐
   │  cold-outreach-  │  │  sniper-leads    │
   │  welle (5-10)    │  │  (2-3, hand-made)│
   └────┬─────────────┘  └────┬─────────────┘
        │ wave drafts          │ sniper drafts
        │                      │
        v                      v
   ┌──────────────────────────────┐
   │  outreach-tuning             │
   │  (V2 audit, 10-point check)  │
   └────┬─────────────────────────┘
        │ tuned drafts
        v
   USER (manual send)
        │
        v
   reply watch / next week's cycle
```

## What gets shared between skills

- **ICP definition** — the hard gates (industry / size / region / group / reachable) are the same across all four skills. Define them once in `settings.local.json`.
- **Region anchor** — used by `cold-outreach-welle`, `sniper-leads`, and enforced by `outreach-tuning`. One value, three readers.
- **Brand word** — same: defined once, used everywhere.
- **Substance anchor** — same.

## What stays per-skill

- **Wave gates** are wave-specific (volume cap, 50%-template rule, send-day spread)
- **Sniper scoring** is sniper-specific (the 8+/10 threshold)
- **Trigger taxonomy** lives only in `trigger-pipeline`
- **The 10-point checklist** lives only in `outreach-tuning`

## Typical pipeline math

For a single-consultant practice running this rhythm steady-state:

| Stage | Per week | Per month |
|---|---|---|
| Trigger hits sourced | 10-15 | ~50 |
| ICP-qualified (after gates) | 4-6 | ~20 |
| Drafts shipped (wave + sniper) | 5-8 | ~25 |
| Replies | 1-2 | 4-8 |
| Conversations booked | 0-1 | 2-4 |
| Audit-tier engagements | — | 1-2 |

These are realistic working numbers for a B2B sales advisory practice in DACH Mittelstand. Above-average response weeks happen; below-average weeks also happen. Treat the monthly number as the trend.

## When to break the rhythm

- **Hot follow-up:** if a reply comes in mid-week, drop the rhythm and respond same-day. The plugin's cadence is for cold; warm conversations supersede.
- **Anniversary cluster:** if your region has 5+ T4 anniversaries in the same quarter, you can run a dedicated wave around that single trigger.
- **Live event:** if a trade show is happening in your region, build a pre-event wave to all attending Mittelstand SMEs in your ICP — the event itself becomes the anchor.

## When to add tooling

The standalone tier (browser + manual sourcing) works up to roughly 30 touches per week. Above that, expect tooling spend:

- ~99 EUR/mo LinkedIn Sales Navigator at >50 candidates/week
- ~50-150 EUR/mo for a managed scraping channel (LinkedIn pages, press monitoring) at >100 candidates/week

Do not buy tooling earlier — the patterns matter more than the volume in the first 3-6 months.
