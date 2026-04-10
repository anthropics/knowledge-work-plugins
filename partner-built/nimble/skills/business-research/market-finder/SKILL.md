---
name: market-finder
description: |
  Discovers all businesses of a given type in any geography using Nimble
  WSAs. Two modes: Discovery finds businesses from scratch; Audit compares
  a user's existing list (Google Sheet, CSV, inline) against fresh
  discovery, categorizing entries as matched, discovered-only, or
  reference-only. Vertical presets (Healthcare, SaaS, Restaurants, Legal,
  Auto/Home) auto-select WSA routing.

  Triggers: "find all X in Y", "build a list of", "market sizing",
  "account universe", "how many X in Y", "TAM for", "discover all",
  "audit my list", "compare against", "what am I missing", "gap analysis",
  "verify my business list", "prospect list".

  Do NOT use for competitor monitoring — use competitor-intel instead.
  Do NOT use for company deep dives — use company-deep-dive instead.
  Do NOT use for neighborhood-level exploration with social enrichment
  — use local-places instead.
allowed-tools:
  - Bash(nimble:*)
  - Bash(date:*)
  - Bash(cat:*)
  - Bash(mkdir:*)
  - Bash(python3:*)
  - Bash(echo:*)
  - Bash(jq:*)
  - Bash(ls:*)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
metadata:
  author: Nimbleway
  version: 0.17.0
---

# Market Finder

Market intelligence powered by Nimble Web Search Agents.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight

Run the preflight pattern from `references/nimble-playbook.md` (5 simultaneous Bash
calls: date calc, today, CLI check, profile load, index.md load).

Also simultaneously:
- `mkdir -p ~/.nimble/memory/{reports,market-finder/checkpoints}`
- Check for existing checkpoints: `ls ~/.nimble/memory/market-finder/checkpoints/ 2>/dev/null`

From the results:
- CLI missing or API key unset -> `references/profile-and-onboarding.md`, stop
- Profile exists -> note industry keywords if any. Apply smart date windowing from
  `references/nimble-playbook.md`. Market-finder tweak: in quick refresh mode,
  skip enrichment and only discover new metros.
- No profile -> fine. Market-finder doesn't require onboarding. Proceed to Step 1.

### Step 1: Parse Request & Detect Mode

Parse `$ARGUMENTS` for business type, geography, qualifiers, and **mode detection**.

#### Mode detection

Check `$ARGUMENTS` for a reference list. Read `references/audit-mode.md` for the
full detection signals and parsing rules.

| Signal | Mode |
|--------|------|
| Google Sheet URL, CSV path, or inline list of 3+ businesses | **Audit** |
| Explicit audit language ("audit my list", "compare against", "gap analysis") | **Audit** |
| No reference list provided | **Discovery** (default) |

If a reference list is present but intent is ambiguous, ask: "Want me to **audit**
your list against fresh discovery, or use it as a starting point?"

If audit language is detected but no reference list is provided, ask: "You mentioned
auditing — please provide your list (Google Sheet URL, CSV file path, or paste inline)."
Do not proceed with Audit mode until a reference list is received.

#### Extract fields

| Field | Required | Source |
|-------|----------|--------|
| Business type / vertical | Yes | User input ("dentists", "SaaS CRM tools") |
| Geography | Yes (except SaaS) | User input ("Florida", "Austin TX", "nationwide") |
| Reference list | Audit mode only | Google Sheet URL, CSV path, or inline |
| Qualification criteria | Optional | User input ("must have website", "10+ reviews") |
| Output preference | Optional | User input ("quick summary", "full dataset") |

**If both type and geography are clear** from `$ARGUMENTS`, confirm briefly and
proceed: "Finding **dentists** in **Florida**..." (or "Auditing your list against
**dentists** in **Florida**..." in Audit mode)

**If partial or ambiguous**, ask one combined question (counts as 1 of max 2
AskUserQuestion prompts):

Use AskUserQuestion with up to 3 questions:
1. **Vertical** -- "What type of business?" with options: Healthcare, SaaS/Software,
   Restaurants/Food, Legal/Financial, Auto/Home Services, Other
2. **Geography** -- "What geography?" (free text or: City, State, Region, Nationwide)
3. **Depth** -- "Quick scan or comprehensive discovery?"

Skip questions already answered by `$ARGUMENTS`.

**Depth modes** (determines how much work each step does):

| Depth | Discovery | Enrichment | Verification | Distribution |
|-------|-----------|------------|-------------|--------------|
| **Quick scan** | All sources, 1 pass | Skip (or top 5 only) | Top 5 entities | Offer |
| **Comprehensive** | All sources + fallback retries | Full | All entities | Offer |

### Step 2: Vertical Detection & Preset Loading

Read `references/vertical-presets.md` and match the user's business type against
preset trigger keywords.

| Match | Action |
|-------|--------|
| Clear match | Load that preset's WSA routing and query pattern |
| Partial match | Confirm: "This looks like **Healthcare**. Use healthcare presets?" |
| No match | Use Custom preset with user's keywords |
| SaaS match | Switch to non-geographic pipeline (no geo-tiling) |

Note which discovery WSAs and enrichment WSAs the preset specifies.

### Step 3: Geographic Scoping

**Skip this step for SaaS vertical** (no geography needed).

| Geography level | Tiling strategy |
|----------------|-----------------|
| City | Single query, no tiling |
| Metro area | Single query per WSA |
| State | Tile by top 5-10 metros in the state |
| Region | Tile by states, then top metros per state |
| Nationwide | Tile by all states, then top metros per state |

**Estimate API calls:** `metros * discovery_wsas * (1 + enrichment_ratio)` where
`enrichment_ratio` is ~0.3. Follow the Scaled Execution pattern from
`references/nimble-playbook.md` to choose execution tier (individual / batch /
multi-batch / confirmation gate):

```
Estimated API calls: ~1,560 (50 states x 8 metros x 3 WSAs + enrichment)
This is a nationwide search. Proceed? [Y/n]
```

Derive a `slug` for checkpointing: lowercase, hyphenated, includes vertical + geo
(e.g., `dentists-florida`, `saas-crm-tools`, `hvac-nationwide`).

### Step 4: Check for Existing Checkpoint

Follow the Checkpointing & Resume pattern from `references/memory-and-distribution.md`.

Check: `cat ~/.nimble/memory/market-finder/checkpoints/{slug}/discovery.json 2>/dev/null`

- **Checkpoint found** -> offer: "Found previous run ({N} entities from {date}).
  Resume and fill gaps, or start fresh?"
- **No checkpoint** -> proceed to Step 5

### Step 5: WSA Discovery & Execution

#### 5a: Discover available WSAs

For each target domain in the selected vertical preset, discover current WSAs:

```bash
nimble agent list --search "{domain}" --limit 20
```

Run these searches simultaneously (one per target domain). From the results:
1. Filter by entity_type (SERP for discovery, PDP/Profile for enrichment)
2. Prefer `managed_by: "nimble"` over `managed_by: "community"`
3. If no WSA found for a domain, mark it for `nimble search` fallback
4. If no WSAs found for ANY domain, fall back entirely to `nimble search` for all metros

Then validate each discovered WSA's input params:
```bash
nimble agent get --template-name {discovered_name}
```

Cache the discovered WSA names + params for the rest of the run.

#### 5b: Geographic discovery (all except SaaS)

For each metro in the tiling plan, run the discovered WSAs simultaneously:

```bash
nimble agent run --agent {maps_wsa} --params '{...validated params...}'
```
```bash
nimble agent run --agent {yelp_wsa} --params '{...validated params...}'
```

Run tertiary domain WSAs only if the preset includes them AND primary + secondary
return < 10 combined unique results for that metro.

Choose execution tier per the Scaled Execution pattern in
`references/nimble-playbook.md` (based on total estimated calls from Step 3).

#### 5c: SaaS discovery (non-geographic)

SaaS skips WSA discovery. Run the two-pass search queries defined in the SaaS
preset from `references/vertical-presets.md`:
- **Pass 1 -- Product discovery:** G2, Capterra, general, ProductHunt, GitHub
- **Pass 2 -- Financial discovery:** Crunchbase, funding news, market landscape

Both passes run simultaneously. Pass 2 is critical -- without it, funding and
traction data will be missing or wrong.

#### 5d: Fallback

If no WSA was found for a target domain, or if a WSA fails for any metro:
```bash
nimble search --query "[type] in [metro]" --max-results 20 --search-depth lite
```

**After discovery:**
1. Parse all results into a unified entity list
2. Deduplicate following the Entity Deduplication pattern from
   `references/nimble-playbook.md`: place_id -> domain -> fuzzy name + city
3. Track `source_count` per entity (how many WSAs/sources found it)
4. Save checkpoint: `~/.nimble/memory/market-finder/checkpoints/{slug}/discovery.json`

### Step 6: Enrichment

Run enrichment using the WSAs discovered in Step 5a for the preset's enrichment
target domains. Prioritize entities with the highest source count first. Choose
execution tier per Scaled Execution in `references/nimble-playbook.md`.

```bash
nimble agent run --agent {enrichment_wsa} --params '{...validated params...}'
```

Only run enrichment WSAs that apply to the current vertical's enrichment targets
(see `references/vertical-presets.md`). Skip entities without the required ID/URL
for the enrichment WSA.

Save checkpoint: `~/.nimble/memory/market-finder/checkpoints/{slug}/enrichment.json`

### Step 6b: Financial Verification (SaaS vertical)

For SaaS entities, verify funding claims before reporting. Never label a company's
funding stage without a source.

For each entity in the top results (top 5 in quick scan, all in comprehensive):
```bash
nimble search --query "{company name} funding raised series" --max-results 5 --search-depth lite
```

- **Source found:** Use the sourced amount and date
- **No source found:** Display "Undisclosed" -- never guess "Early stage" or "Bootstrapped"

This step prevents publishing unverified financial claims. It's fast (one search
per entity, lite depth) and catches recent funding rounds that directory sites miss.

### Step 7: Deduplication & Scoring

**Final deduplication:** Run a final dedup pass across all phases following the
Entity Deduplication pattern from `references/nimble-playbook.md`. Merge fields
from multiple sources into a single record per entity.

**Discovery strength scoring** (skill-specific, varies by vertical):

Geographic verticals (Healthcare, Restaurants, Legal, Auto/Home, Custom):

| Level | Criteria |
|-------|----------|
| **High** | 3+ sources OR 2+ sources with reviews > 50 |
| **Medium** | 2 sources OR 1 source with reviews > 10 |
| **Low** | 1 source only, few/no reviews |

SaaS vertical (funding + directory presence matter more than review count):

| Level | Criteria |
|-------|----------|
| **High** | Verified funding > $10M OR 3+ directory sources OR 1000+ G2 reviews |
| **Medium** | Verified funding < $10M OR 2 sources OR 100+ G2 reviews |
| **Low** | 1 source only, no verified funding, few reviews |

Display as: `*** High`, `** Medium`, `* Low`

### Step 7b: Audit Comparison (Audit mode only)

**Skip this step in Discovery mode.**

Read `references/audit-mode.md` for the full matching algorithm, normalization rules,
and output template.

1. **Parse reference list** — detect format (Google Sheet / CSV / inline), extract
   records, normalize to `{name, domain, city, state, phone}` per the parsing rules
   in `references/audit-mode.md`
2. **Run three matching layers** in order (domain → name+city → phone). Once an entity
   matches at any layer, stop. Track which layer produced the match.
3. **Categorize** every entity:
   - `matched` — in both reference list and discovery results
   - `discovered_only` — found by discovery, not in reference list
   - `reference_only` — in reference list, not found by discovery
4. **Calculate coverage score** — `matched / reference_count × 100`

Proceed to Step 8 with the categorized results.

### Step 8: Output

```
# Market Finder: [Business Type] in [Geography]
*Found [N] businesses | [Date] | Strength: [H] High, [M] Medium, [L] Low*

## Summary
- **Total discovered:** [N] unique businesses across [M] metros
- **Geographic breakdown:** [top 5 metros by count]
- **Source coverage:** [list each source used with entity counts]

## Top Results (High Strength)

| # | Name | Location | Rating | Reviews | Strength | Sources |
|---|------|----------|--------|---------|----------|---------|
| 1 | Acme Dental | Miami, FL | 4.8 | 312 | *** High | Maps, Yelp, BBB |
| 2 | WidgetCo Health | Orlando, FL | 4.6 | 89 | *** High | Maps, Yelp |
...

## All Results by Geography

### Miami, FL ([n] businesses)
[Table of businesses in this metro]

### Orlando, FL ([n] businesses)
[Table of businesses in this metro]
...

## What's Missing
[Data gaps: metros with low coverage, entities without websites, etc.]
```

**SaaS output variant** (when vertical is SaaS, replace "All Results by Geography"
with tier-based grouping):

```
## Players by Tier

### Pure-Play (dedicated to this vertical)
| # | Name | Domain | Funding | Key Metric | Strength | Sources |
...

### Adjacent (feature overlap from larger platforms)
| # | Name | Domain | Funding | Key Metric | Strength | Sources |
...

### Open Source
| # | Name | Repo | Stars | Key Metric | Strength | Sources |
...
```

**Source links are mandatory.** Every entity must have at least one clickable source
URL (Google Maps link, Yelp listing, website, BBB profile, G2 page, or GitHub repo).

**Audit output variant** (when in Audit mode, replace the Discovery output above):
Use the audit output template from `references/audit-mode.md`. Key sections: Summary
with coverage score, Matched table, Discovered Only table (expansion candidates),
Reference Only table (coverage gaps), and "What This Means" interpretation.

### Step 9: Save to Memory

Make all Write calls simultaneously:

**Discovery mode:**
- Report -> `~/.nimble/memory/reports/market-finder-{slug}-{date}.md`
- Entity data -> `~/.nimble/memory/market-finder/{slug}/entities.json`

**Audit mode:**
- Report -> `~/.nimble/memory/reports/market-finder-audit-{slug}-{date}.md`
- Structured data -> `~/.nimble/memory/market-finder/{slug}/audit-{date}.json`
  (all three categories with match metadata)

**Both modes:**
- Profile -> update `last_runs.market-finder` in `~/.nimble/business-profile.json`
  (only if profile exists)
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.
- Clean up checkpoint (complete run) or keep (partial run)

### Step 10: Share & Distribute

**Always offer distribution -- do not skip this step.** Follow
`references/memory-and-distribution.md` for connector detection, sharing flow, and
source links enforcement.

Notion: full results table as a dated subpage.
Slack: TL;DR with total count + top 10 entities only.

### Step 11: Follow-ups

**Discovery mode follow-ups:**
- **"Tell me more about #N"** -> show full detail for that entity
- **"Filter by [criteria]"** -> re-filter existing results
- **"Expand to [new geography]"** -> add metros and re-run discovery
- **"Export as CSV"** -> generate CSV from entities.json
- **"Run enrichment on all"** -> extend enrichment beyond top entities
- **"Audit against my existing list"** -> switch to Audit mode with this run's results
- **"Looks good"** -> done

**Audit mode follow-ups:**
- **"Export discovered-only as CSV for outreach?"** -> CSV of expansion candidates
- **"Investigate reference-only gaps?"** -> targeted searches for reference_only entries
- **"Run company-deep-dive on new discoveries?"** -> deep research on discovered_only
- **"Re-run with a different geography?"** -> audit the same list against a new area
- **"Looks good"** -> done

**Sibling skill suggestions:**

> **Next steps:**
> - Run `company-deep-dive` for a full 360 profile on any business from this list
> - Run `competitor-positioning` to compare top players in this market
> - Run `local-places` for neighborhood-level discovery with social enrichment and maps

---

## Sub-Agent Strategy

For large jobs, `nimble agent run-batch` handles WSA parallelism server-side (see
Scaled Execution in `references/nimble-playbook.md`). Sub-agents are useful for
**preparing** batch inputs and **processing** results, not for running individual
WSA calls.

Use `nimble-researcher` agents (`agents/nimble-researcher.md`) when:
- Building metro query lists for large geographies (one agent per state)
- Processing and deduplicating batch results in parallel

Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, fallback on failure).

---

## Agent Teams Mode (Dual-Mode)

Check at startup: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`

**Team mode** (flag set): Spawn **teammates** for parallel phases:

- **Discovery teammate(s):** Run all discovery WSAs across metro batches
- **Enrichment teammate:** Run enrichment WSAs for top entities
- **Lead** (you): Coordinate, scope, deduplicate, score, generate output

**Solo mode** (flag not set): Standard sequential flow from Steps 5-8.

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key,
429, 401, empty results, extraction garbage). Skill-specific errors:

- **WSA not found:** Skip silently and rely on other discovery sources. Log which
  WSAs were unavailable.
- **Search 500/timeout:** Retry once without `--focus` flag. If still failing,
  retry with a simplified query. Log the failure but don't skip the entire search
  category -- partial data is better than none.
- **No results for metro:** "No [type] found in [metro]. Skipping to next metro."
  Don't abort the entire job for one empty metro.
- **Ambiguous business type:** "Did you mean [option A] or [option B]?"
  (e.g., "practice" could be medical, dental, legal)
- **SaaS with geography:** If the selected preset has no geo-tiling but the user
  specified a geography, offer it as a search qualifier instead.
- **Reference list parse failure:** If Google Sheet extraction returns garbage or
  CSV is malformed, ask the user to paste the data inline instead.
- **Empty reference list:** If parsed list has 0 valid records, warn and offer to
  switch to Discovery mode.
- **No matches found:** If all three matching layers produce zero matches, report
  it — a 0% coverage score is valid and informative.
