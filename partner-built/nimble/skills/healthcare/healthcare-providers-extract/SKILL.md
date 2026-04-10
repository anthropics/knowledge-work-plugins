---
name: healthcare-providers-extract
description: |
  Extracts structured practitioner data from healthcare practice websites.
  Returns names, credentials, specialties, contact info, and education for
  every provider on a practice's site.

  Use when user asks to extract, pull, or list doctors, providers, or staff
  from practice websites. Triggers: "extract doctors from", "pull providers
  from", "who are the providers at", "build a provider database", "list all
  doctors at", "scrape the team page", "get practitioner data from".

  Accepts practice URLs (pasted, CSV, Google Sheet) or discovers practices
  via Google Maps when given specialty + location. Single sites or 100+ URLs.

  Do NOT use for filling data gaps — use healthcare-providers-enrich instead.
  Do NOT use for credential validation — use healthcare-providers-verify instead.
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

# Healthcare Providers Extract

Structured practitioner extraction from healthcare practice websites, powered by
Nimble's web data APIs.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight + WSA Discovery

Run the preflight pattern from `references/nimble-playbook.md` (5 simultaneous Bash
calls: date calc, today, CLI check, profile load, index.md load).

**Also simultaneously** — run WSA discovery and setup:
- `mkdir -p ~/.nimble/memory/{reports,healthcare-providers-extract/checkpoints}`
- `ls ~/.nimble/memory/healthcare-providers-extract/checkpoints/ 2>/dev/null`
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
  - **Quick refresh:** last run < 14 days ago (re-extract only new/changed pages)
  - **Same-day repeat:** if `last_runs.healthcare-providers-extract` is today, check
    for existing report at `~/.nimble/memory/reports/healthcare-providers-extract-*[today].md`.
    If found, ask: "Already ran today. Run again for fresh data?"
- No profile -> that's fine. This skill doesn't require onboarding. Proceed to Step 1.

### Step 1: Parse Input & Starting Questions

Parse `$ARGUMENTS` for input type using the Input Parsing Pattern from
`references/nimble-playbook.md`. Key routing:
- **URLs detected** -> proceed to Step 3
- **Specialty + location** (no URLs) -> proceed to Step 2 (practice discovery)
- **Unclear** -> ask (counts as 1 of max 2 prompts)

**If input is clear**, confirm and ask one shaping question (plain text, not
AskUserQuestion):

> "Extracting providers from **N practice sites**. Quick questions:
> 1. Healthcare vertical? (ophthalmology, dental, dermatology, general, or other)
> 2. Quick scan (names + credentials only) or full extraction (all 5 fields)?"

**If input is ambiguous**, use AskUserQuestion (counts as 1 of max 2 prompts):

> **What practice sites should I extract providers from?**
> - Paste URLs directly (one per line)
> - Provide a CSV file path or Google Sheet URL with practice URLs
> - Or describe what you're looking for (e.g., "ophthalmologists in Austin, TX")
>   and I'll find practices first

Skip questions the user already answered in their initial message.

### Step 2: Practice Discovery (Optional)

Only if the user provided a specialty + location instead of URLs.

**Two input paths into discovery:**

**Path A — Fresh discovery.** User gave specialty + location. Run Layer 2 WSA
discovery for session-specific agents:

```bash
nimble agent list --limit 50 --search "[specialty]"
nimble agent list --limit 50 --search "[directory-user-mentioned]"
```

See `references/wsa-reference.md` for the full discovery strategy, agent evaluation
criteria, and healthcare discovery prioritization.

Run all discovery-phase agents simultaneously. Validate params with
`nimble agent get` first.

**Path B — Market-finder handoff.** User ran `market-finder` first and wants to
extract providers from those results. Read the market-finder output:

```bash
cat ~/.nimble/memory/market-finder/{slug}/entities.json 2>/dev/null
```

Extract practice records. Note: Google Maps results contain `place_url` (a Maps
link) but not the practice's actual website URL. Proceed to Step 2b to resolve
real website URLs before site mapping.

**After either path:** Deduplicate by domain. Present discovered practices:

> "Found **N practices** for [specialty] in [location] across [M] data sources.
> Proceeding to extract providers from these sites..."

**Fallback** — if no discovery WSAs were found, or results are sparse (< 3):
```bash
nimble search --query "[specialty] in [location]" --max-results 20 --search-depth lite
```

### Step 2b: Resolve Practice Website URLs

Discovery sources (Google Maps, Yelp, BBB) return listing URLs, not practice
website URLs. Before site mapping, resolve the actual website for each practice:

1. **Check structured data first** — Google Maps results often include a `website`
   field in the structured output. Use it if present.
2. **Extract from listing page** — if no `website` field, extract the Maps listing
   to find the practice website link:
   ```bash
   nimble extract --url "[maps-listing-url]" --format markdown
   ```
3. **Search fallback** — if extraction fails:
   ```bash
   nimble search --query "[practice-name] [city] official website" --max-results 3 --search-depth lite
   ```

Skip practices where no website URL can be resolved — note them in the "Data
Quality Summary" output section.

### Step 3: Site Mapping

Follow the Site Mapping Pattern from `references/nimble-playbook.md` for each
practice URL. Skill-specific settings:
- **Keyword weight table:** `references/provider-extraction-patterns.md`
- **Page cap:** 15 per site
- **Fallback query:** `site:[domain] doctors OR providers OR team`

For 6+ practices, use sub-agents (see Sub-Agent Strategy below).

Save checkpoint: `~/.nimble/memory/healthcare-providers-extract/checkpoints/{slug}/mapping.json`

### Step 4: Page Extraction

**WSA shortcuts first:** If WSA discovery found agents that extract provider data
from healthcare directories, use those for matching practices — structured WSA
output is higher quality than parsed markdown.

For all other practices, follow the Page Extraction with Retry pattern from
`references/nimble-playbook.md`. Scale using the Scaled Execution pattern from
the same reference.

Save checkpoint: `~/.nimble/memory/healthcare-providers-extract/checkpoints/{slug}/extraction.json`

### Step 5: Structured Parsing

Parse extracted markdown to identify providers and their fields. Read
`references/provider-extraction-patterns.md` for the 5 core fields, credential
regex patterns, and specialty keywords.

**For each extracted page:**
1. Scan for provider name patterns (Dr. prefix, heading patterns, bold text near
   credential suffixes)
2. Match credentials using the regex patterns from
   `references/provider-extraction-patterns.md`
3. Match specialty using keywords for the detected healthcare vertical
4. Extract contact info (phone regex, appointment URLs, email)
5. Extract education/training mentions

**Build structured records:**
```json
{
  "name": "Dr. Jane Smith",
  "credentials": "MD, FACS",
  "specialty": "Retinal Surgery",
  "contact": {"phone": "(555) 123-4567", "scheduling_url": "..."},
  "education": "Fellowship: Bascom Palmer Eye Institute",
  "source_url": "https://practice.com/our-doctors",
  "practice_name": "Shore Center for Eye Care",
  "practice_url": "https://practice.com",
  "confidence": "High"
}
```

### Step 6: Deduplication & Confidence Scoring

Follow the Entity Deduplication and Entity Confidence Scoring patterns from
`references/nimble-playbook.md`. Skill-specific dedup rules and the 5-field
confidence criteria are in `references/provider-extraction-patterns.md`.

### Step 7: Output

Present results grouped by practice, sorted by confidence within each practice.

```markdown
# Provider Extraction: [N] Providers from [M] Practices
*[Date] | [H] High, [M] Medium, [L] Low confidence*

## TL;DR
Extracted [N] providers from [M] practice websites. [H] with complete profiles,
[L] with partial data. [Key finding: e.g., "12 of 15 providers are board-certified"].

## [Practice Name] ([domain])

| # | Name | Credentials | Specialty | Contact | Education | Confidence |
|---|------|------------|-----------|---------|-----------|------------|
| 1 | Dr. Jane Smith | MD, FACS | Retinal Surgery | (555) 123-4567 | Fellowship: Bascom Palmer | High |
| 2 | Dr. John Doe | OD | General Ophthalmology | [Book](url) | Residency: Wills Eye | Medium |

[Repeat per practice]

## Data Quality Summary
- **Complete profiles (High):** [N] providers
- **Partial profiles (Medium):** [N] providers — missing: [list common gaps]
- **Minimal profiles (Low):** [N] providers — missing: [list common gaps]

## Sources
[Clickable URL for every page extracted, grouped by practice]
```

**Source links are mandatory.** Every provider record must trace back to a source URL.

### Step 8: Save to Memory

Make all Write calls simultaneously:

- Report -> `~/.nimble/memory/reports/healthcare-providers-extract-{slug}-{date}.md`
- Provider data -> `~/.nimble/memory/healthcare-providers-extract/{slug}/providers.json`
- Profile -> update `last_runs.healthcare-providers-extract` in
  `~/.nimble/business-profile.json` (only if profile exists)
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.
- Clean up checkpoint (complete run) or keep (partial run)

### Step 9: Share & Distribute

**Always offer distribution -- do not skip.** Follow
`references/memory-and-distribution.md` for connector detection and sharing flow.

Notion: full provider table as a dated subpage.
Slack: TL;DR with provider count and confidence breakdown only.

### Step 10: Follow-ups

- **"Tell me more about Dr. X"** -> show full extracted profile
- **"Export as CSV"** -> generate CSV from providers.json
- **"Run on more sites"** -> append new practice URLs, extract and merge
- **"What's missing?"** -> detail the data gaps per provider

**Enrichment from discovered WSAs:** If Step 0 found enrichment-phase agents
(reviews, regulatory, practice details), offer them as immediate follow-ups:

> "I also found [N] WSAs that could enrich this data: [brief list]. Want me to
> run reputation checks or regulatory lookups on these providers/practices?"

See `references/wsa-reference.md` for enrichment phase mapping and fallback chains.

**Sibling skill suggestions:**

> **Next steps:**
> - Run `healthcare-providers-enrich` to fill data gaps (NPI lookup, board
>   certification verification, additional contact info)
> - Run `healthcare-providers-verify` to validate credentials and license status
> - Run `market-finder` to discover more practice URLs in this area

---

## Sub-Agent Strategy

For batch extraction (6+ practices), use `nimble-researcher` agents
(`agents/nimble-researcher.md`) to parallelize site mapping and extraction.

Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

**Spawn pattern:** One agent per practice (or per batch of 3 practices for large
jobs). Each agent runs Steps 3-5 for its assigned practices and returns structured
provider records.

**Single-practice optimization:** If only 1-2 practices, run directly from the
main context instead of spawning agents.

**Fallback:** If any agent fails, run those extractions directly from the main
context. Never leave gaps in the output.

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key,
429, 401, empty results, extraction garbage). Skill-specific errors:

- **No provider pages found:** "Couldn't find provider/team pages on [domain].
  The site may list staff differently. Want me to try extracting from the homepage
  or search for this practice on healthcare directories?"
- **All extractions returned garbage:** "The practice sites appear to be heavily
  JavaScript-rendered. Retrying with browser rendering..." (auto-retry with
  `--render` per the shared pattern)
- **Ambiguous practice name:** If a URL fails and the user provided a name instead,
  search for the practice: `nimble search --query "[practice name] [location] doctors" --max-results 5 --search-depth lite`
- **CSV/Sheet parse error:** "Couldn't parse the input file. Expected a column with
  practice URLs. Can you paste the URLs directly instead?"
