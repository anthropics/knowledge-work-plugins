# Memory & Distribution

How skills persist knowledge across sessions and distribute reports to external tools.

---

## Memory Architecture

All persistence lives under `~/.nimble/` — never touch user project files.

```
~/.nimble/
├── business-profile.json          # Tier 1: Hot cache (see profile-and-onboarding.md)
└── memory/                        # Tier 2: Deep storage (loaded on demand)
    ├── index.md                   # Global index (one line per directory)
    ├── log.md                     # Chronological activity log (append-only)
    ├── backlog.md                 # Research questions and knowledge gaps
    ├── synthesis/                 # Cross-entity analysis pages
    ├── competitors/               # Accumulated intel per competitor
    │   └── index.md              # Per-directory entity catalog
    ├── people/                    # Contact profiles for meeting prep
    │   └── index.md
    ├── companies/                 # Deep-dive research results
    │   └── index.md
    ├── reports/                   # Timestamped full skill outputs
    ├── positioning/               # Per-competitor positioning snapshots
    │   └── index.md
    └── glossary.md                # Industry terms and jargon
```

**Tier 1** (`business-profile.json`) — loaded every session. See
`references/profile-and-onboarding.md` for the full schema and update patterns.

**Tier 2** (`memory/`) — loaded on demand when a skill needs deeper context.

### Wiki Primitives

The memory directory includes wiki-level files that make the knowledge base
navigable, queryable, and self-maintaining:

```
~/.nimble/memory/
├── index.md                       # Global summary (one line per directory)
├── log.md                         # Chronological activity log (append-only)
├── backlog.md                     # Research questions and knowledge gaps
├── synthesis/                     # Cross-entity analysis pages
│   ├── index.md                   # Per-directory catalog (same format as others)
│   └── competitive-landscape.md   # (created dynamically when patterns emerge)
├── competitors/
│   ├── index.md                   # Per-directory entity catalog
│   ├── widgetco.md
│   └── gizmotech.md
├── people/
│   ├── index.md
│   └── alex-kim.md
├── companies/
│   ├── index.md
│   └── ...
├── reports/
├── positioning/
│   ├── index.md
│   └── ...
└── glossary.md
```

Skills create index files, `log.md`, and `synthesis/` on first write if missing.

---

## Wiki Content Index (Two-Tier)

Indexes live at two levels: a lightweight **global index** for cross-directory
navigation, and **per-directory indexes** for detailed entity catalogs.

### Global Index (`~/.nimble/memory/index.md`)

One line per directory — entity count and last-updated date. Never lists individual
entities. Stays under 30 lines forever.

```markdown
# Knowledge Index

| Directory | Entities | Last Updated |
|-----------|----------|-------------|
| [[competitors/index]] | 5 | 2026-03-20 |
| [[people/index]] | 3 | 2026-03-15 |
| [[companies/index]] | 8 | 2026-03-18 |
| [[positioning/index]] | 5 | 2026-03-20 |
| [[synthesis/index]] | 2 | 2026-03-20 |
```

### Per-Directory Index (`{dir}/index.md`)

One row per entity file with summary and last-updated date. Owned by the skills that
write to that directory. Scales independently — each directory can grow without
affecting other indexes.

```markdown
# Competitors Index

| File | Summary | Updated |
|------|---------|---------|
| [[competitors/widgetco]] | Enterprise SaaS competitor, Series C | 2026-03-20 |
| [[competitors/gizmotech]] | API-first competitor, growing fast | 2026-03-20 |
```

### Rules

- **Skills read only their directory's index in preflight.** competitor-intel reads
  `competitors/index.md`; meeting-prep reads `people/index.md`. Cross-directory
  lookups go through the global index first, then the relevant directory index.
- **Skills update only their directory's index on write.** When a skill creates or
  updates an entity file, update the row in that directory's index. Use the entity
  file's first `# Heading` as the summary if none exists.
- **Global index is updated after directory index changes.** Bump the entity count
  and last-updated date for the affected directory.
- **Created on first skill run** if missing. Skills should not fail if an index
  doesn't exist — create it with whatever entities are written in that run.
- **Obsidian-compatible.** `[[path/entity]]` links (without `.md` extension) work as
  wiki links in Obsidian. Path is relative to `~/.nimble/memory/`.

---

## Chronological Wiki Log (`log.md`)

`~/.nimble/memory/log.md` is an append-only timestamped record of skill runs and
findings. Grep-friendly format for answering "what did I learn this week?"

```markdown
# Activity Log

## [2026-03-15] meeting-prep
- Updated: [[people/alex-kim]], [[companies/widgetco]]
- Key findings:
  - Alex Kim moved to VP Engineering role
  - Interested in API performance benchmarks

## [2026-03-18] company-deep-dive
- Created: [[companies/target-corp]]
- Key findings:
  - Series B closed at $30M, Sep 2025
  - Expanding into EU market Q2 2026

## [2026-03-20] competitor-intel
- Created: [[competitors/widgetco]], [[competitors/gizmotech]]
- Updated: [[competitors/acme-rival]]
- Key findings:
  - WidgetCo launched enterprise tier pricing
  - GizmoTech hired new CTO from CloudCorp
```

### Rules

- **Append at the end of the file** (oldest first, newest last). Normal writes are
  pure appends — no read-insert-rewrite needed. LLMs read the whole file; humans use
  `grep "^## \[" log.md | tail -10` for recent entries.
- **Format:** `## [YYYY-MM-DD] skill-name` — enables `grep "^## \[" log.md | tail -10`.
- **Content:** List entities created/updated (as `[[path/entity]]` links), then 2-3
  bullet points of key findings. Keep entries concise — this is a log, not a report.
- **Rotate entries older than 90 days** as a separate maintenance step. After
  appending the new entry, check the oldest entries (at the top). If older than 90
  days, remove them. This rotation is not part of the normal append — it's a periodic
  cleanup that triggers during writes. The full reports in `reports/` are the
  permanent record; `log.md` is for recent activity scanning.
- **Created on first skill run** if missing.

---

## Cross-Entity References

Entity files use Obsidian-compatible `[[path/entity]]` wiki links to connect related
entities across directories.

### Format

```markdown
# Alex Kim

## Current Role
VP of Engineering at [[competitors/widgetco]] (since 2024)

## Related
- Employer: [[competitors/widgetco]]
- Previous: [[companies/cloudcorp]]
```

```markdown
# WidgetCo

## Key People
- [[people/alex-kim]] — VP Engineering
- [[people/jane-smith]] — CEO

## Related Competitors
- [[competitors/gizmotech]] — overlapping market segment
```

### Rules

- **Link format:** `[[directory/entity-slug]]` — no `.md` extension, path relative
  to `~/.nimble/memory/`. Obsidian resolves these as wiki links.
- **Add cross-references when relationships are discovered.** When a skill finds
  that a person works at a tracked company, or two competitors share a market segment,
  add links in both directions.
- **Handle missing targets gracefully.** A cross-reference to a file that doesn't
  exist yet is fine — it becomes a valid link once that entity is created. Skills
  should not fail on dangling links.
- **Skills follow links to enrich output.** When meeting-prep finds
  `[[competitors/widgetco]]` in a person's file, it loads that competitor file for
  additional context. When competitor-intel finds `[[people/alex-kim]]` in a
  competitor file, it can surface that relationship in the briefing.

### When to Add Cross-References

| Relationship discovered | Link from | Link to |
|------------------------|-----------|---------|
| Person works at company | `people/{name}` → `competitors/{company}` or `companies/{company}` | Reverse link too |
| Companies compete | `competitors/{a}` → `competitors/{b}` | Reverse link too |
| Person previously at company | `people/{name}` → `companies/{company}` | — (one-way is fine) |
| Synthesis cites entity | `synthesis/{topic}` → entity files | — (one-way) |

---

## Ad-Hoc Insights

When a user signals "save this", "remember that", "note this down", or similar intent
during a conversation, file the insight into the relevant entity file(s) instead of
letting it vanish into chat history.

### Filing Pattern

1. **Identify the relevant entity file(s).** If the insight is about a competitor,
   file it in `competitors/{name}.md`. If it spans multiple entities (e.g., "WidgetCo
   is partnering with GizmoTech"), update all relevant files.
2. **Append under a dated `## Insights` section:**

```markdown
## Insights
### 2026-03-22
- User noted: WidgetCo's enterprise pricing is 2x ours — [[competitors/gizmotech]]
  is closer to our price point [ad-hoc]
```

3. **Add cross-references** if the insight connects entities (as shown above).
4. **Update the directory's `index.md`** — bump the last-updated date for the
   affected file(s), and update the global `index.md` counts.
5. **Append to `log.md`** (at the end of the file):

```markdown
## [2026-03-22] ad-hoc-insight
- Updated: [[competitors/widgetco]], [[competitors/gizmotech]]
- Key findings:
  - WidgetCo enterprise pricing is 2x user's, GizmoTech closer to parity
```

### Rules

- **Tag with `[ad-hoc]`** so skills can distinguish user-contributed insights from
  skill-generated findings during dedup.
- **Multi-entity insights update all relevant files** with cross-references between
  them.
- **Don't create entity files for throwaway comments.** If the user says "remember
  that meetings on Fridays are bad", that's a preference (update
  `business-profile.json`), not an entity insight.

---

## Cross-Entity Synthesis Pages

`~/.nimble/memory/synthesis/` contains pages that analyze patterns across multiple
entity files. Unlike entity files (which accumulate facts about one entity), synthesis
pages draw conclusions across the knowledge base.

### Page Creation

Synthesis pages are created **dynamically** when patterns emerge across entities —
not from a pre-defined list. Common examples:

| Page | Purpose | Typical trigger |
|------|---------|----------------|
| `competitive-landscape.md` | Market positioning, feature gaps, pricing comparison | competitor-intel after 3+ competitors |
| `pricing-trends.md` | Pricing pattern analysis across competitors | Pricing signals recur across 3+ competitor runs |

Page names should be slug-formatted topic labels (not skill names). Skills create
synthesis pages when a pattern recurs across 3+ entities — this keeps synthesis
data-driven rather than speculative.

### Format

Synthesis pages use YAML frontmatter to track which entity files they were built
from and when. This makes staleness deterministic — compare current file timestamps
against the recorded ones.

```markdown
---
confidence: high
sources:
  - path: competitors/widgetco.md
    updated: 2026-03-20
  - path: competitors/gizmotech.md
    updated: 2026-03-20
  - path: competitors/acme-rival.md
    updated: 2026-03-18
generated_by: competitor-intel
generated_at: 2026-03-20
---
# Competitive Landscape

## Market Map
[Positioning of each competitor by segment, size, strategy]

## Feature Comparison
| Capability | Us | [[competitors/widgetco]] | [[competitors/gizmotech]] |
|---|---|---|---|
| Real-time data | ✅ | ❌ | Partial |

## Pricing Comparison
[Tier-by-tier comparison where known]

## Key Patterns
- Trend 1 with evidence from multiple competitors
- Trend 2 with cross-entity citations

## What This Means
[Strategic implications — what the patterns suggest for the user's company]
```

### Rules

- **Cite source entity files** with `[[path/entity]]` links. Every claim must trace
  back to an entity file.
- **Track sources and confidence in frontmatter.** `confidence: high|medium|low`
  reflects data completeness (high = all key sources available, low = sparse data).
  The `sources:` block lists every entity file used and its last-modified date at
  generation time. To check staleness, compare current file timestamps against the
  recorded ones — if any source was updated since generation, the page is stale.
- **Refresh when sources are stale.** If a skill adds major new signals to 2+ source
  entities since the synthesis was generated, regenerate. Don't regenerate on every
  run — only when the source timestamps diverge.
- **Use `nimble-analyst` agent** for synthesis generation. The analyst has the right
  model (Sonnet) for cross-entity pattern recognition and strategic analysis.

### Generation Trigger

competitor-intel generates `competitive-landscape.md` when:
- 3+ competitors have been researched in the current run, OR
- The existing synthesis page's source timestamps are stale (source entities were
  updated since generation)

Other synthesis pages are created by the relevant skills when patterns emerge, or
on user request.

---

## Research Backlog (`backlog.md`)

`~/.nimble/memory/backlog.md` tracks knowledge gaps and research questions — things
to investigate in future skill runs. This is not synthesis (derived, read-only
output) — it's imperative (drives future action).

```markdown
# Research Backlog

## Open
- [ ] WidgetCo pricing for enterprise tier — couldn't find public pricing [2026-03-20, competitor-intel]
- [ ] GizmoTech Series B details — rumored but unconfirmed [2026-03-20, competitor-intel]
- [ ] Alex Kim's LinkedIn activity — profile was private [2026-03-15, meeting-prep]

## Resolved
- [x] WidgetCo new CTO name — confirmed: Sarah Chen [2026-03-22, competitor-intel]
```

### Rules

- **Any skill can append questions** to the `## Open` section when it encounters
  gaps during research. Tag each with date and skill name.
- **Users can add questions** via ad-hoc insights ("find out about X next time").
- **Skills check backlog before running** to avoid re-researching resolved questions
  and to prioritize open ones relevant to the current run.
- **Resolved questions** get moved to `## Resolved` with a resolution date — not
  deleted. This preserves the audit trail.

---

## Deep Storage Formats

### competitors/

One file per competitor. Append new findings under dated headers — never overwrite.

```markdown
# WidgetCo

## Key Facts
- Domain: widgetco.com
- HQ: San Francisco
- Funding: Series C ($45M, Jan 2026)
- CEO: Jane Smith

## Signals
### 2026-03-20
- Launched new enterprise tier pricing — [source URL]
- Hired VP of Sales from CRMHub — [source URL]

### 2026-03-13
- Announced partnership with AWS — [source URL]
```

### people/

One file per contact. Used by meeting-prep skill.

```markdown
# Alex Kim

## Current Role
VP of Engineering at WidgetCo (since 2024)

## Background
- Previously: Senior Director at CloudCorp (2019-2024)
- Education: MS Computer Science, top-10 program

## Notes from Previous Meetings
### 2026-03-15
- Interested in our API performance benchmarks
- Prefers technical depth over high-level summaries
```

### companies/

Detailed company profiles from deep-dive research.

```markdown
# Target Corp

## Overview
- Industry: Enterprise SaaS | Founded: 2015 | HQ: Austin, TX | ~500 employees

## Financials
- Last funding: Series B ($30M, Sep 2025) | Revenue: Est. $40M ARR

## Recent News
(dated entries, same format as competitors/)
```

### reports/

Timestamped **full** skill outputs. Save the complete briefing, not a summary.

**Naming:** `{skill-name}-{YYYY-MM-DD}.md` — if a skill may produce multiple reports
per day (e.g., meeting-prep for different companies), add a qualifier:
`{skill-name}-{qualifier}-{YYYY-MM-DD}.md`. The qualifier is defined in each skill's
SKILL.md (e.g., company slug for meeting-prep).

### glossary.md

Industry terms and jargon. Updated when the user uses unfamiliar terms.

## Bootstrapping (First Run)

```bash
mkdir -p ~/.nimble/memory/{competitors,people,companies,reports,positioning,synthesis}
```

Create stub files for each competitor from the onboarding flow.

`index.md` and `log.md` are created automatically on the first skill run that writes
to memory — no need to create empty stubs during bootstrapping.

## Differential Analysis

The key feature across all skills — only surface what's genuinely new.

### Dedup Lifecycle

Memory loading happens at two points in every skill:

1. **Step 0 (Preflight):** Load relevant memory files for context. This tells the skill
   what's already known so it can pass known signals to sub-agents for dedup during
   research. For example, competitor-intel loads `~/.nimble/memory/competitors/*.md`;
   meeting-prep loads `~/.nimble/memory/people/*.md`.

2. **Analysis step (before report generation):** Final dedup check. Compare all findings
   from research against loaded memory. Only signals classified as NEW or UPDATED (per
   the freshness classification in `nimble-playbook.md`) make it into the report.

### What "new" means

- "WidgetCo raised a Series C" is noise if already in memory
- "WidgetCo just hired a new CTO" is a new signal worth highlighting
- "WidgetCo raised a Series C" with a new detail (amount, lead investor) is an UPDATE

## Learning from Corrections

When the user corrects the skill, update both tiers:

| Correction | Profile update | Deep storage update |
|------------|---------------|-------------------|
| "Skip CompanyX" | `preferences.skip_competitors` | Archive file |
| "Track CompanyY" | `competitors` list | Create stub file |
| "That info is wrong" | — | Update the file |
| "ARR means Annual Recurring Revenue" | — | Add to `glossary.md` |
| "I prefer bullet points" | `preferences.output_format` | — |

Always confirm the update to the user.

## Checkpointing & Resume

For multi-phase pipelines (map → extract → enrich → score), save intermediate results
so failed or interrupted runs can resume without re-doing completed work.

### Storage

```
~/.nimble/memory/{skill-name}/checkpoints/{slug}/
├── map.json           # Phase 1 output
├── extract.json       # Phase 2 output
└── enrich.json        # Phase 3 output
```

`{slug}` is a stable identifier derived from the run's input parameters (e.g., URL
domain, search query hash). Same input = same slug = resumable.

### Checkpoint format

Each phase file is JSON:
```json
{
  "phase": "extract",
  "status": "complete",
  "timestamp": "2026-04-03T15:30:00Z",
  "record_count": 47,
  "data": [ ... ]
}
```

`status` is `"complete"` or `"partial"` (interrupted mid-phase).

### Resume logic

On re-run with the same parameters:
1. Detect existing checkpoint directory for the slug
2. Offer: **"Found previous run (47 records from Apr 3). Resume and fill gaps, or start fresh?"**
3. If resume: skip phases where `status = "complete"`, re-run where `status = "partial"`
   or file is missing
4. If start fresh: delete the checkpoint directory and begin from phase 1

### Rules

- One checkpoint directory per unique run (keyed by slug)
- Clean up checkpoints older than 30 days on skill startup
- Don't checkpoint trivial runs (< 5 records) — the overhead isn't worth it

## Rules

- **Never touch user project files.** All persistence under `~/.nimble/`.
- **Append, don't overwrite.** Deep storage grows over time with dated sections.
- **Read on demand.** Only load files when the skill actually needs them.
- **Update profile after every run.** At minimum, `last_runs` timestamp.
- **Update wiki files after every memory write.** Update the directory's `index.md`
  for affected entities, bump the global `index.md` counts, append a `log.md` entry
  for the run, and add cross-references where relationships are discovered.
- **Handle missing gracefully.** If a file doesn't exist, create it. This includes
  index files, `log.md`, `backlog.md`, and cross-reference targets.

---

## Source Links Enforcement

**Every signal in every report must include a clickable source URL.** This is a hard
requirement — reports without source links are incomplete and must not be distributed.

What counts as a source link:
- A direct URL to the article, press release, or page where the signal was found
- The URL returned by `nimble search` in the result's `url` field
- For extracted content, the URL passed to `nimble extract --url`

What does NOT count:
- A company's homepage (unless the signal is specifically about homepage content)
- A generic domain without a path (e.g., `https://widgetco.com`)
- "Source: web search" or any non-clickable attribution

If a signal has no source URL after research and extraction, drop it from the report.
An unsourced signal is worse than a missing one — it can't be verified and erodes trust.

---

## Report Distribution

After presenting output, offer sharing based on available MCP connectors.

### Connector Detection

Check before presenting options:
- **Notion:** `mcp__plugin_Notion_notion__notion-create-pages`
- **Slack:** Any Slack MCP tool

### Sharing Flow

Use `AskUserQuestion` with only the available options:

> **Share this report?**
> - **Save to Notion** — full report as a page
> - **Send to Slack** — TL;DR to a channel
> - **Both**
> - **Skip**

**Notion:** Create a dated subpage. If `integrations.notion.reports_page_id` exists
in the profile, use it as parent. Otherwise ask and save the ID for next time.

**Slack:** Post **TL;DR only** — Slack is for alerts, not full reports. If
`integrations.slack.channel` exists, use it. Otherwise ask and save.

**Neither available** (first run only):
> **Tip:** If you connect a Notion or Slack MCP server, I can save reports or post
> TL;DRs to your team automatically.

Don't repeat this tip on subsequent runs.
