---
name: healthcare-providers-enrich
description: |
  Fills gaps in existing healthcare practitioner lists — adds missing phone numbers,
  credentials, specialties, contact info, education, reviews, and regulatory data.

  Triggers: "enrich my provider list", "fill in missing data", "add phone numbers
  to these doctors", "complete this practitioner database", "enrich CRM export",
  "fill gaps in my provider data", "supplement this healthcare list".

  Accepts CSV, Google Sheet URL, or pasted data. Searches for each provider's
  practice website, extracts missing fields, and enriches with reviews, clinical
  trials, and accreditation via WSAs.

  Do NOT use for extracting providers from practice URLs — use healthcare-providers-extract instead.
  Do NOT use for validating credentials — use healthcare-providers-verify instead.
  Do NOT use for discovering practices — use market-finder or local-places instead.
  Do NOT use for general extraction — use nimble-web-expert instead.
allowed-tools:
  - Bash(nimble:*)
  - Bash(date:*)
  - Bash(cat:*)
  - Bash(mkdir:*)
  - Bash(python3:*)
  - Bash(echo:*)
  - Bash(jq:*)
  - Bash(ls:*)
  - Bash(wc:*)
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

# Healthcare Providers Enrich

Fill gaps in existing practitioner lists with verified web data, powered by Nimble's
web data APIs.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight + WSA Discovery

**Sibling handoff check:** Before running full preflight, check if
`healthcare-providers-extract` ran earlier in this session by following the Sibling
Handoff pattern from `references/nimble-playbook.md`. If same-day extract output
exists, skip CLI check and profile load, and reuse WSA Layer 1/3 inventory. Only
re-run Layer 2 if the specialty changed.

**Otherwise, run full preflight** from `references/nimble-playbook.md` (5 simultaneous
Bash calls: date calc, today, CLI check, profile load, index.md load).

**Also simultaneously** — run WSA discovery and setup:
- `mkdir -p ~/.nimble/memory/{reports,healthcare-providers-enrich/checkpoints}`
- `ls ~/.nimble/memory/healthcare-providers-enrich/checkpoints/ 2>/dev/null`
- Run Layer 1 (vertical) and Layer 3 (general tools) WSA discovery from
  `references/wsa-reference.md`. Layer 2 (session-specific) runs after Step 1 when
  you know the user's specialty.

Classify discovered agents into phases and validate with `nimble agent get` per
`references/wsa-reference.md`.

From the preflight results:
- CLI missing or API key unset -> `references/profile-and-onboarding.md`, stop
- Profile exists -> note it for context. Determine mode using smart date windowing
  from `references/nimble-playbook.md`:
  - **Full mode:** first run OR last run > 14 days ago
  - **Quick refresh:** last run < 14 days ago (re-enrich only records with gaps)
  - **Same-day repeat:** if `last_runs.healthcare-providers-enrich` is today, check
    for existing report at `~/.nimble/memory/reports/healthcare-providers-enrich-*[today].md`.
    If found, ask: "Already ran today. Run again for fresh data?"
- No profile -> that's fine. This skill doesn't require onboarding. Proceed to Step 1.

### Step 1: Parse Input + Starting Questions

**Chained-from-extract shortcut:** Check for a same-day extract report:
```bash
ls ~/.nimble/memory/reports/healthcare-providers-extract-*$(date +%Y-%m-%d).md 2>/dev/null
```
If a same-day report exists, parse the `{slug}` from the filename and load
`~/.nimble/memory/healthcare-providers-extract/{slug}/providers.json`. The practice
domains and page URL patterns are already known — construct individual bio page URLs
from the site's URL convention and skip Step 3 entirely. This avoids N unnecessary
web searches. If no same-day report exists, do not reuse old `providers.json` files.

Parse `$ARGUMENTS` for input type using the Input Parsing Pattern from
`references/nimble-playbook.md`. Key routing:
- **Extract output detected** (providers.json) -> proceed to Step 2, mark Step 3 skip
- **CSV/Sheet/pasted data detected** -> proceed to Step 2
- **Unclear** -> ask (counts as 1 of max 2 prompts)

**If input is clear**, confirm and ask one shaping question (plain text, not
AskUserQuestion):

> "Found **N providers** in your list. Quick questions:
> 1. Which fields need filling? (contact info, credentials, specialty, reviews, regulatory — or all gaps)
> 2. Healthcare vertical? (ophthalmology, dental, dermatology, general, or other)"

**If input is ambiguous**, use AskUserQuestion (counts as 1 of max 2 prompts):

> **What provider list should I enrich?**
> - Paste provider data directly (name + any known info, one per line)
> - Provide a CSV file path or Google Sheet URL
> - Or describe what you have (e.g., "a list of 50 ophthalmologists with just names and states")

Skip questions the user already answered in their initial message.

### Step 2: Analyze Existing Data

Parse the input into structured records. For each provider, identify:
- **Known fields** — what the user already has (name, state, specialty, etc.)
- **Missing fields** — gaps against the 5 core fields from
  `references/provider-extraction-patterns.md` (name, credentials, specialty,
  contact, education)
- **Enrichment targets** — additional fields the user requested (reviews, regulatory,
  accreditation)

**Early exit — no gaps:** If all providers are already High confidence (5/5 fields),
skip to Step 5 (WSA enrichment) or report: "All providers already have complete
profiles. Want me to add supplementary data (reviews, clinical trials, accreditation)
instead?"

Build a gap analysis summary:

> "Analyzing **N providers**:
> - Names: N/N present
> - Credentials: N/N present (N missing)
> - Specialty: N/N present (N missing)
> - Contact info: N/N present (N missing)
> - Education: N/N present (N missing)
>
> Starting enrichment for **N providers with gaps**..."

Run Layer 2 WSA discovery now that you know the specialty:
```bash
nimble agent list --limit 50 --search "[specialty]"
nimble agent list --limit 50 --search "[directory-user-mentioned]"
```

See `references/wsa-reference.md` for session-specific discovery.

### Step 3: Web Search for Provider Identity

For each provider with gaps, find their practice website and bio page:

```bash
nimble search --query "[provider name] [credentials] [location] [specialty]" --max-results 5 --search-depth lite
```

**Search strategy:**
- Include all known fields in the query to disambiguate common names
- Prioritize results from practice websites over directory listings
- If the provider has a known practice name, add it to the query
- For providers with only name + state, broaden: `"[name] [state] doctor"`

**Result selection:** Pick the most relevant result — practice bio page > healthcare
directory profile > LinkedIn. Save the selected URL for extraction.

For 10+ providers, use sub-agents (see Sub-Agent Strategy below).

**Checkpoint (mandatory):** You MUST write the checkpoint file before proceeding.
Interrupted runs with 20+ providers waste significant API credits without resume.
```bash
echo '{...}' > ~/.nimble/memory/healthcare-providers-enrich/checkpoints/{slug}/search.json
```

### Step 4: Extract Missing Fields

Choose extraction strategy based on provider count. Follow the Scaled Execution
pattern from `references/nimble-playbook.md` — it covers individual calls (1-10),
`extract-batch` (11-100), and the confirmation gate for larger jobs. Use the Page
Extraction with Retry pattern from the same reference for garbage detection and
retry logic.

Parse extracted content for missing fields using the detection patterns from
`references/provider-extraction-patterns.md` (credential regex, specialty keywords,
contact patterns, education mentions).

**Merge rules:**
- Only fill fields that are actually missing — never overwrite existing data
- Track which fields were added and their source URL
- If extracted data conflicts with existing data, keep the existing value and flag
  the conflict for user review

**Checkpoint (mandatory):** You MUST write the checkpoint file before proceeding.
```bash
echo '{...}' > ~/.nimble/memory/healthcare-providers-enrich/checkpoints/{slug}/extraction.json
```

### Step 5: WSA Enrichment (Optional)

If the user requested reviews, regulatory data, or accreditation — or if the gap
analysis shows most core fields are already filled and enrichment adds more value:

**Run enrichment-phase WSAs** discovered in Step 0. See `references/wsa-reference.md`
for the enrichment phase mapping, agent evaluation, and fallback chains.

For each practice or provider, run relevant enrichment agents simultaneously.
Follow the Scaled Execution pattern from `references/nimble-playbook.md` for
batching.

**Merge enrichment data** into provider records:
- Reviews/ratings -> add as supplementary fields (not part of core 5)
- Clinical trial activity -> add as supplementary field
- Accreditation status -> add as supplementary field

### Step 6: Deduplication & Confidence Scoring

Follow the Entity Deduplication and Entity Confidence Scoring patterns from
`references/nimble-playbook.md`. Skill-specific dedup rules and the 5-field
confidence criteria are in `references/provider-extraction-patterns.md`.

**Enrichment-specific confidence:** Score only the **newly added** fields:
- **High** — field found and confirmed by 2+ sources
- **Medium** — field found from 1 source
- **Low** — field inferred or partially matched

### Step 7: Output

Present results as an enrichment diff — showing what was added to each provider.
Group by practice, sort by confidence within each group, and include a "What This
Means" section at the end with actionable next steps.

```markdown
# Provider Enrichment: [N] Providers Updated
*[Date] | [A] fields added across [P] providers | [H] High, [M] Medium, [L] Low confidence*

## TL;DR
Enriched [P] of [T] providers. Added [A] total fields: [breakdown by field type].
[Key finding: e.g., "Found contact info for 18 of 20 providers, 3 have clinical trials"].

## Enrichment Results

| # | Name | Added Fields | Confidence | Source |
|---|------|-------------|------------|--------|
| 1 | Dr. Jane Smith | +credentials (MD, FACS), +contact ((555) 123-4567) | High | [source](url) |
| 2 | Dr. John Doe | +specialty (General Ophthalmology), +education (Wills Eye) | Medium | [source](url) |
| 3 | Dr. Alex Chen | +contact ((555) 987-6543) | Low | [source](url) |

## Detailed Records

### Dr. Jane Smith
**Existing:** Name, State (TX)
**Added:**
- Credentials: MD, FACS — [source](url)
- Contact: (555) 123-4567 — [source](url)
- Education: Fellowship, Bascom Palmer Eye Institute — [source](url)
**Confidence:** High (3 fields added, 2 sources)

[Repeat per provider with additions]

## Providers Not Enriched
[List providers where no additional data was found, with attempted searches]

## Data Quality Summary
- **Fully enriched (5/5 fields):** [N] providers
- **Partially enriched:** [N] providers — common gaps: [list]
- **No new data found:** [N] providers

## Sources
[Clickable URL for every page used, grouped by provider]

## What This Means
[Actionable interpretation: which providers are ready to contact, which need more
data, what the enrichment coverage tells you about this list's quality]
```

**Source links are mandatory.** Every added field must trace back to a source URL.

### Step 8: Save to Memory

Make all Write calls simultaneously:

- Report -> `~/.nimble/memory/reports/healthcare-providers-enrich-{slug}-{date}.md`
- Enriched data -> `~/.nimble/memory/healthcare-providers-enrich/{slug}/enriched.json`
- Profile -> update `last_runs.healthcare-providers-enrich` in
  `~/.nimble/business-profile.json` (only if profile exists)
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.
- Clean up checkpoint (complete run) or keep (partial run)

### Step 9: Share & Distribute

**Always offer distribution — do not skip.** Follow
`references/memory-and-distribution.md` for connector detection and sharing flow.

Notion: full enrichment report as a dated subpage.
Slack: TL;DR with enrichment summary and field counts only.

### Step 10: Follow-ups

- **"Tell me more about Dr. X"** -> show full enriched profile
- **"Export as CSV"** -> generate CSV with original + enriched fields
- **"Enrich more fields"** -> re-run with expanded field targets
- **"Which providers still have gaps?"** -> filter to incomplete records

**Sibling skill suggestions:**

> **Next steps:**
> - Run `healthcare-providers-verify` to validate the enriched credentials and
>   license status
> - Run `healthcare-providers-extract` to discover more providers from practice
>   websites
> - Run `market-finder` to find additional practices in this area

---

## Sub-Agent Strategy

For batch enrichment (10+ providers), use `nimble-researcher` agents
(`agents/nimble-researcher.md`) to parallelize search and extraction.

Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

**Spawn pattern:** One agent per batch of 5 providers. Each agent runs Steps 3-4
for its assigned providers and returns enriched records. Tell each agent to use
`nimble extract-batch` for its assigned URLs rather than individual `nimble extract`
calls — one batch call per agent is faster and more reliable than sequential calls.

**Small batch optimization:** If fewer than 10 providers, run directly from the
main context instead of spawning agents.

**Fallback:** If any agent fails, run those enrichments directly from the main
context. Never leave gaps in the output.

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key,
429, 401, empty results, extraction garbage). Skill-specific errors:

- **No search results for provider:** "Couldn't find a web presence for [name] in
  [state]. The name may be too common or the provider may not have an online
  presence. Want me to try with additional context (practice name, specialty)?"
- **Ambiguous provider match:** "Found multiple providers named [name] in [state].
  Can you confirm which one? [list top 3 with practice names]"
- **All extractions returned garbage:** "The provider websites appear to be heavily
  JavaScript-rendered. Retrying with browser rendering..." (auto-retry with
  `--render` per the shared pattern)
- **CSV/Sheet parse error:** "Couldn't parse the input file. Expected columns with
  provider names and at least one identifier (state, specialty, or practice).
  Can you paste the data directly instead?"
- **No gaps detected:** Handled in Step 2 (early exit to WSA enrichment or report).
