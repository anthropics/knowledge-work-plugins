# Trigger Types — Field Reference

The four trigger types the `trigger-pipeline` skill works with, with worked sourcing notes and example signals.

## T1 — New leadership <90 days

The strongest trigger in DACH Mittelstand B2B sales advisory. A new VP Sales, Head of Sales, or General Manager in their first 90 days is statistically the most receptive buyer profile for outside sales-process help.

**Receptivity window:** Sharp curve. Day 0-30: very high. Day 30-90: high. Day 90-120: noticeable drop. Day 120+: indistinguishable from cold outreach with no trigger.

**Sourcing channels:**

- LinkedIn search filtered to role + region + "started in [current quarter]"
- Press releases announcing appointments (Mittelstand companies often issue these for VP-level hires)
- Trade-press personnel sections (most industry outlets run a "Personalien" column)
- Google Alerts on `"hat ... als Vertriebsleiter" OR "neuer Geschäftsführer"` + your region

**Verification:** Cross-check LinkedIn start-date against the press release / company announcement. Don't trust the "I'm honored to share I've started…" post date — it can lag the actual start by 30-60 days.

**Example signal:** "M. P. became Managing Director of Sondermaschinenbau-Group B in January 2025. Source: company press release dated 14 Jan 2025."

## T2 — VP Sales / Head of Sales role open 8+ weeks

A role posted and unfilled at 8 weeks signals genuine capacity strain. Either the search is hard (small specialist market) or the role is being rewritten (organizational uncertainty). In both cases, an outside advisor can carry meaningful weight in the interim.

**Receptivity window:** Open-ended while the role is open. Closes immediately on hire.

**Sourcing channels:**

- LinkedIn Jobs filtered to role + region + posting date >8 weeks ago
- Company career pages (some Mittelstand SMEs don't list on LinkedIn — check directly)
- Indeed, Stepstone, regional job boards
- Personalverbund — chamber-of-commerce job-listing aggregations in some regions

**Verification:** Confirm the role is still active. Roles sometimes stay listed after being filled. Check the company's careers page directly, not the third-party aggregator.

**Example signal:** "Toolmaker A's VP Sales role has been listed on their careers page since March 4. As of May 25, that's 12 weeks open."

## T3 — Funded initiative (public)

A publicly announced transformation budget — digital transformation, sales modernization, ERP migration with a sales component — signals committed money and a gatekeeper with authority. Often more workable than T1 for larger-side Mittelstand (150-250 FTE) where the new VP may not yet have budget signing authority.

**Receptivity window:** 6 months from public announcement. After that, vendors are usually locked in.

**Sourcing channels:**

- Trade press (`Produktion`, `markt&mittelstand`, regional industry publications)
- Government / EU funded-project databases (especially for Mittelstand transformation grants)
- LinkedIn announcements from CFOs and CIOs (less common but high-signal when they fire)
- Chamber-of-commerce quarterly reports

**Verification:** Confirm the initiative is genuinely funded (not just a press release of intent). Press releases often precede actual budget signoff by a quarter.

**Example signal:** "Drives Manufacturer C announced their NL showroom + service hub opening on 14 April 2026, with public reference to expanding industrial sales channels alongside the traditional segment."

## T4 — Milestone anniversary

The softest trigger. Anniversaries — 25, 50, 75, 100 years — open a year-long storytelling window. Companies often invest in modernization to mark the occasion. Less universally applicable than T1/T2/T3 but useful for filling out a wave when T1 is dry.

**Receptivity window:** 12 months around the anniversary date.

**Sourcing channels:**

- Public registries (founding date + age math)
- Chamber-of-commerce member directories (some publish anniversary calendars)
- Company "About us" pages
- Local press, especially for round-number anniversaries (regional papers cover these)

**Verification:** Match the founding year against multiple sources. Some companies have "founded in 1934" on their website but the legal entity dates to a 1981 restructuring.

**Example signal:** "Toolmaker A founded in 1964 → 60-year anniversary in 2024 → likely investment cycle 2025-2027."

## Trigger-mix discipline

A healthy pipeline carries a mix of trigger types across waves. Single-trigger pipelines fail when the source dries up. Rough target distribution across a quarter:

- T1: 40-50% of pipeline (highest receptivity, source-dependent)
- T2: 20-30% (steady, depends on regional job market)
- T3: 15-20% (slow-moving, high-value)
- T4: 10% (filler, never the primary)

If T1 drops below 30% for two consecutive months, expand sourcing — typically by adding a LinkedIn channel or a new trade-press feed.

## Trigger half-lives (field observations)

Rough field observations from one practice across ~4 months and ~60 accounts. Small sample — treat as starting hypotheses, not fixed numbers.

| Trigger | Receptivity at day 30 | At day 90 | At day 180 |
|---|---|---|---|
| T1 new leadership | High | High | Low |
| T2 open role | High (while open) | High (while open) | Drops to zero on hire |
| T3 funded initiative | High | High | Medium |
| T4 anniversary | Medium | Medium | Medium (year-long flat) |

Calibrate against your own data after 20-30 sent touches per trigger type.
