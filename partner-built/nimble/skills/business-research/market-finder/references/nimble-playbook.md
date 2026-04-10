# Nimble Playbook

How to run Nimble CLI commands in Claude Code. Read this before executing any commands.

---

## Claude Code Execution Rules

- **No shell state persistence.** Variables set in one Bash call are gone in the next.
  Inline all values (dates, paths, names) directly into every command.
- **No `&` + `wait` parallelism.** It breaks in Claude Code. Instead, make **multiple
  Bash tool calls in a single response** — they run in parallel natively.
- **Search returns JSON** — `--output-format` doesn't change this. With `--search-depth
  lite`, the JSON is small (title, description, URL per result). Parse it directly.
- **Extract returns JSON with `data.markdown`** — use `--format markdown` to get clean
  content in the `data.markdown` field.

## Preflight Pattern

Every skill starts with these simultaneous Bash calls:

- `python3 -c "from datetime import datetime, timedelta; print((datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'))"` (14 days ago)
- `date +%Y-%m-%d` (today)
- `nimble --version && echo "NIMBLE_API_KEY=${NIMBLE_API_KEY:+set}"`
- `cat ~/.nimble/business-profile.json 2>/dev/null`
- `cat ~/.nimble/memory/index.md 2>/dev/null` (global wiki index — know what directories have data)

From the `nimble --version` output, check:
- **CLI missing** (command not found) → install it interactively
- **CLI outdated** (version < 0.8.0) → upgrade it
- **API key unset** → guide setup

See `references/profile-and-onboarding.md` for the full prerequisite checks with
install/upgrade flows. Don't skip version validation — outdated CLI versions may be
missing flags or features that skills depend on.

## Sibling Handoff

When skills in the same family chain together (e.g., extract → enrich → verify),
the second skill can skip redundant preflight work. Detect a sibling handoff by
checking for same-day output from the upstream skill:

```bash
ls ~/.nimble/memory/reports/{upstream-skill}-*$(date +%Y-%m-%d).md 2>/dev/null
```

Use the dated report as the recency signal — data files under `memory/{skill}/` may
not have dates in their filenames, so always verify via the report timestamp. If a
same-day report exists, parse the slug from the filename and load the corresponding
data files.

**If same-day sibling output exists:**
- **Skip CLI check and profile load** — they were validated minutes ago
- **Reuse WSA Layer 1 and Layer 3 inventory** — the catalog hasn't changed. Only
  re-run Layer 2 if the specialty or context changed.
- **Use the sibling's structured output directly** — if the upstream skill produced
  data files with domains and page URLs, don't re-search for what's already known.
  Construct URLs from known patterns instead of running N web searches.

**If no same-day sibling output exists:** Run full preflight as normal.

This pattern is optional — skills MUST still work standalone without sibling output.
The handoff is a fast path, not a requirement.

## Smart Date Windowing

For any skill using `--start-date` based on previous runs:
- **First run:** 14 days ago → **full mode**
- **Last run < 3 days ago:** use 7 days ago (too narrow = empty results) → **quick refresh**
- **Last run 3-14 days ago:** use the last run date → **quick refresh**
- **Last run > 14 days ago:** 14 days ago → **full mode**
- **Same-day repeat:** if `last_runs.{skill-name}` is today, check if a report already
  exists at `~/.nimble/memory/reports/{skill-name}*[today].md`. If it does, **ask the
  user before re-running**: "Already ran today. Run again for fresh data?" Don't silently
  re-run — it wastes API credits and produces near-identical output.
  **Exception — meeting-prep:** Skip the same-day report check. Meeting-prep is
  per-meeting, not per-day — users may prep for multiple meetings in a single day.
  Instead, meeting-prep checks freshness at the entity level: load cached profiles
  from `~/.nimble/memory/people/` and `~/.nimble/memory/companies/` and offer to
  reuse recent research rather than blocking the run.

---

## Search

```bash
# Standard search (always use --search-depth lite for discovery)
nimble search --query "company name news" --max-results 10 --search-depth lite

# News-focused search
nimble search --query "company name" --focus news --max-results 10 --search-depth lite

# Date-filtered search (inline the date — don't use variables)
nimble search --query "company funding" --focus news --start-date "2026-03-11" --max-results 10 --search-depth lite

# Social signals from X/LinkedIn
nimble search --query "Company" --include-domain '["x.com", "linkedin.com"]' --max-results 10 --search-depth lite --time-range week

# Deep search (full page content — only for comprehensive analysis, costs more)
nimble search --query "company name" --search-depth deep --max-results 5

# Fast search (premium tier — not used by default)
# nimble search --query "company name" --search-depth fast --max-results 10
```

**Key flags:**
- `--query` — search query string (required)
- `--focus` — `general`, `news`, `shopping`, `social`, `coding`, `academic`.
  **`social`** searches social platform people indices directly (LinkedIn, X) — best
  for finding specific people. If it errors, use
  `--include-domain '["linkedin.com"]'` as an alternative approach.
- `--max-results` — max results to return
- `--start-date` / `--end-date` — date filters (YYYY-MM-DD)
- `--search-depth` — `lite` (1 credit), `deep` (1 + 1/page)
- `--include-domain` — JSON array of domains, e.g., `'["x.com", "linkedin.com"]'`
- `--time-range` — e.g., `week`
- `--country` — geo-targeted results (e.g., "US", "IL")
- `--include-answer` — LLM-powered answer summary

**Date range strategy:**
- First run: 14 days ago
- Subsequent runs: `last_runs` timestamp from business profile
- If < 3 results: retry without `--start-date`

## Extract

```bash
# Extract article content as markdown (recommended)
nimble extract --url "https://example.com/article" --format markdown

# Extract with JavaScript rendering (for dynamic/SPA pages)
nimble extract --url "https://example.com/spa" --render --format markdown
```

Response is JSON with `data.markdown` containing clean content.

**Key flags:**
- `--url` — target URL (required)
- `--format` — `markdown` (recommended), `simplified_html`, `plain_text`
- `--render` — render JavaScript using a browser

**Extraction fallback** (if `data.markdown` is mostly JavaScript/boilerplate):
1. **Garbage check:** If `data.markdown` has < 100 characters of meaningful content
   (after stripping nav/footer boilerplate), treat it as garbage.
2. Retry with `--render --format markdown` (handles JS-heavy/SPA pages)
3. If still garbage: search for the same article title on a different domain
4. If still nothing: skip and log — never abort a batch for a single extraction failure

### Extract async & batch

```bash
# Async — submit single URL, get task_id, poll for results
nimble extract-async --url "https://example.com/page" --render --format markdown

# Batch — up to 1,000 URLs in one request
nimble extract-batch \
  --shared-inputs 'render: true' --shared-inputs 'format: markdown' \
  --input '{"url": "https://example.com/page-1"}' \
  --input '{"url": "https://example.com/page-2"}'
```

Poll async tasks with `nimble tasks get --task-id <id>` and fetch results with
`nimble tasks results --task-id <id>`. Poll batches with
`nimble batches progress --batch-id <id>`.

## Map & Site Mapping

```bash
nimble map --url "https://example.com/blog" --limit 20
```

### Site Mapping Pattern

Use `nimble map` to discover a site's page structure, then score and filter pages by
relevance before extracting.

1. **Discover:** `nimble map --url {url} --limit {cap}` — returns a list of URLs
2. **Score:** Each skill defines a keyword/weight table for URL path segments
   (e.g., `/providers` = High, `/about` = Medium, `/blog` = Low). Score each
   discovered page against the table.
3. **Filter:** Keep pages scoring above the skill's threshold. Always include the
   homepage as a fallback.
4. **Fallback:** If `nimble map` returns < 3 candidates, use
   `nimble search --query "site:{domain} {keywords}" --max-results 10 --search-depth lite`

Each skill provides its own keyword/weight table in SKILL.md — the pattern here is
the discover → score → filter → fallback flow.

## Agents

Pre-built extraction templates for structured data from specific sites (Amazon, LinkedIn,
Google, etc.). Use when you need structured fields rather than raw page content.

```bash
# List available agents (search by domain or vertical)
nimble agent list --limit 100
nimble agent list --limit 100 --search "amazon"

# Inspect an agent's schema (input params + output fields)
nimble agent get --template-name <agent_name>

# Run an agent (sync — waits for result)
nimble agent run --agent <agent_name> --params '{"key": "value"}'

# Run an agent (async — returns task_id, poll for results)
nimble agent run-async --agent <agent_name> --params '{"key": "value"}' \
  --callback-url "https://your.server/callback"
```

**Key flags for `run` / `run-async`:**
- `--agent` — agent name from `nimble agent list` (required)
- `--params` — JSON object with agent input parameters (required)
- `--localization` — enable zip_code/store_id localization (agent-dependent)

**Additional flags for `run-async`:**
- `--callback-url` — POST callback when task completes
- `--storage-type` — `s3` or `gs`
- `--storage-url` — destination bucket URL
- `--storage-compress` — gzip the stored output
- `--storage-object-name` — custom filename instead of task_id

**Response:** `data.parsing` contains the structured output. Shape depends on agent type:
- **PDP** (product/profile/detail) → flat dict
- **SERP / list** → array of objects
- **Google Search** → `{"entities": {"OrganicResult": [...], ...}}`

**Async task states:** `pending` → `success` or `error`. Poll with `nimble tasks results --task-id <task_id>`.

**Fallback rule:** If no agent exists for the target domain, fall back to
`nimble search` + `nimble extract`. Don't fail silently — log which domains
lacked agent coverage so agent-builder can fill gaps later.

### Agent batch

```bash
# Up to 1,000 agent requests in one call
nimble agent run-batch \
  --shared-inputs 'agent: amazon_serp' \
  --input '{"params": {"keyword": "iphone 15"}}' \
  --input '{"params": {"keyword": "iphone 16"}}'
```

Returns a `batch_id`. Poll with `nimble batches progress --batch-id <id>`, then
fetch individual results with `nimble tasks results --task-id <id>`.

### Tasks & batches polling

```bash
# Single async task
nimble tasks get --task-id <task_id>          # check status
nimble tasks results --task-id <task_id>      # fetch results

# Batch
nimble batches progress --batch-id <batch_id> # lightweight progress check
nimble batches get --batch-id <batch_id>      # all task IDs + states
nimble batches list --limit 20                # list all batches
nimble tasks list --limit 20                  # list all tasks
```

**Workflow:** Always `nimble agent get` before `nimble agent run` to understand the
expected input params and output fields.

## Agent Creation (generate → poll → iterate → publish)

Create custom extraction agents for any website. The full lifecycle is available via CLI.

```bash
# Generate a new agent
nimble agent generate \
  --agent-name niche_store_pdp \
  --prompt "Extract product name, price, rating, and first 5 reviews" \
  --url "https://example.com/products/widget-pro"

# Refine an existing agent (clone + apply new prompt)
nimble agent generate \
  --agent-name niche_store_pdp \
  --from-agent niche_store_pdp \
  --prompt "Add a discount_percentage field"

# Poll generation status (async — typically 1-3 min)
nimble agent get-generation --generation-id <generation_id>

# Publish when satisfied
nimble agent publish --agent-name niche_store_pdp --version-id <version_id>
```

**Key flags for `generate`:**
- `--agent-name` — name for the agent (required)
- `--prompt` — natural language description of what to extract (required)
- `--url` — sample URL to analyze (required)
- `--from-agent` — existing agent to clone and refine (for iteration)
- `--input-schema` — custom input schema (optional, inferred if omitted)
- `--output-schema` — custom output schema (optional, inferred if omitted)
- `--metadata` — additional metadata (optional)

**Generation response:** returns `id` (generation ID), `status` (`queued` → `in_progress`
→ `success` / `failed`), and `generated_version_id` on success.

**Workflow:** Generate → poll with `get-generation` until `success` → optionally iterate
with `--from-agent` → publish with `version-id`.

**Polling:** Generation takes 1-3 minutes. Run the generate → poll → publish loop as a
background Task agent so the user isn't blocked waiting. The Task agent should poll
`nimble agent get-generation` every 10 seconds until `status` is `success` or `failed`,
then publish automatically (or report failure). Present results to the user when done.

## MCP Fallback (when CLI is not installed)

If `nimble --version` returns "command not found", fall back to the Nimble MCP server.
All CLI commands have MCP equivalents — discover them via the MCP tool list. MCP tools
accept the same parameters as CLI flags, passed as tool arguments instead of flags.

## Parallel Execution

Make **multiple Bash tool calls in a single response**. Claude Code runs them in
parallel automatically:

- Call 1: `nimble search --query "CompanyA news" --max-results 5 --search-depth lite`
- Call 2: `nimble search --query "CompanyB news" --max-results 5 --search-depth lite`
- Call 3: `nimble search --query "CompanyC news" --max-results 5 --search-depth lite`

## Sub-Agent Spawning

When using the Agent tool for parallel research:

- **Always `mode: "bypassPermissions"`** — sub-agents don't inherit Bash permissions.
- **Batch max 4 agents.** More risk hitting rate limits. For 5+, batch in groups.
- **Tell agents to use Bash** — explicitly say "Use the Bash tool to execute nimble
  commands." Some agents try WebSearch instead.
- **Fallback on failure** — if any agent returns without results, run those searches
  directly from the main context. Don't leave gaps.

## Communication Style

Inform the user at **phase transitions only** with concrete numbers:
- "Researching **Acme Corp** + **5 competitors** since Mar 12..."
- "Found **12 new signals**. Pulling top 4 articles..."
- "All data collected. Building your briefing..."

Don't narrate individual tool calls.

## Rate Limits & Common Errors

- **Rate limit:** 10 req/sec per API key
- **Retry on 429:** Reduce simultaneous calls
- **Timeout:** 30 seconds per request

| Error | Cause | Fix |
|-------|-------|-----|
| `NIMBLE_API_KEY not set` | Missing API key | See `profile-and-onboarding.md` |
| `401 Unauthorized` | Expired key | Regenerate at app.nimbleway.com |
| `429 Too Many Requests` | Rate limit | Fewer simultaneous calls |
| `timeout` | Slow response | Retry once, then skip |
| `500 Server Error` | Transient server failure | Retry once without `--focus`; if persistent, simplify query |
| `empty results` | No matches | Remove `--start-date`, broaden query |

## Signal Date Validation

High-quality intelligence requires distinguishing between when a **page was published**
and when the **underlying event occurred**. This matters because:

- Syndicated or republished content may carry a different publication date than the
  original source
- Secondary coverage (regulatory filings, recap articles, industry roundups) can
  report on events that happened weeks or months earlier

### Article Date vs Event Date

Every signal has two dates:

| | What it is |
|---|---|
| **Article date** | When the page was published |
| **Event date** | When the underlying event actually happened |

A signal is "new" only if its **event date** falls within the freshness window.

### Event Date Extraction Rules

Sub-agents must determine the event date from content:

1. **Explicit past reference** — "launched in Q3", "appointed last October" → event
   date is in the past, regardless of the article date
2. **Temporal language** — "last quarter", "months ago", "earlier this year" → resolve
   relative to the article date
3. **Present tense announcement** — "today announces", "is launching" → event date ≈
   article date
4. **Dateline** — "NEW YORK, March 15 —" → event date = that dateline date
5. **If ambiguous** — extract the source URL and check the on-page date

### Source Type Hierarchy

When the same event appears from multiple sources, prefer those closest to the event:

1. **Primary** — the company's own domain, official press release, regulatory filing
2. **Wire service** — AP, Reuters, Bloomberg
3. **Major outlet** — original reporting with bylines
4. **Derivative** — syndicated copies, aggregator sites, recap articles, or content
   that attributes its information to another source

If the only source for a signal is derivative, corroborate against a primary or major
source before reporting.

### Freshness Classification

After determining the event date, classify each signal:

| Classification | Meaning | Action |
|---|---|---|
| **NEW** | Event date within freshness window, not in memory | Include in report |
| **UPDATED** | Known event with genuinely new information | Include as update |
| **STALE** | Old event covered by a recent article | **DROP — do not include** |
| **UNCERTAIN** | Can't determine event date from snippet alone | Extract URL to verify; if still uncertain after extraction, **DROP** |

**Hard rule:** Only signals classified as **NEW** or **UPDATED** may appear in reports.
STALE and UNCERTAIN signals must be dropped entirely — not downgraded, not footnoted,
not included as "background context." If a signal can't be verified as genuinely recent,
it doesn't exist as far as the report is concerned.

### `--start-date` Best Practices

`--start-date` is a useful filter for reducing noise, but always validate event dates
from the content itself:
- For news queries (`--focus news`), consider running a parallel undated query to
  surface original sources alongside recent coverage
- The existing fallback ("If < 3 results, retry without `--start-date`") remains useful

### Verification Budget

Not every signal needs full verification — budget extract calls by priority:

| Priority | Examples | Verification |
|---|---|---|
| **P1** (high impact) | Funding, M&A, leadership changes | Always extract + corroborate (see below) |
| **P2** (medium impact) | Product launches, partnerships, major hires | Extract if date is UNCERTAIN or source is derivative |
| **P3** (low impact) | Blog posts, minor hires, event appearances | Trust if date looks plausible; drop if obviously stale |

Skills define their own P1/P2/P3 signal types in their SKILL.md. The verification
budget above applies universally regardless of which signals a skill classifies at
each level.

### P1 Corroboration (Mandatory)

Any P1 signal sourced from derivative or aggregator sites **must** be corroborated
before it can appear in a report. This is a hard gate, not a suggestion.

For each P1 signal that needs corroboration:

```bash
nimble search --query "[Company] [event summary]" --max-results 5 --search-depth lite
```

Look for the **primary source** (company blog, press release, official filing, regulatory
document). Check the primary source's date:

- **Primary source dates the event within the freshness window** → signal is NEW, include it
- **Primary source dates the event outside the freshness window** → reclassify as STALE, drop
- **No primary source found** → reclassify as UNCERTAIN, drop

Do not report P1 signals that fail corroboration. It's better to miss a real signal than
to report a stale one as new — trust is the product.

---

## Entity Deduplication

When a skill collects entity records from multiple sources (directories, search results,
extracted pages), deduplicate before reporting. This is distinct from signal-level
differential analysis (see `memory-and-distribution.md`) — entity dedup merges records
for the *same entity* across sources within a single run.

Three-layer pattern (generic — each skill customizes the specifics):

1. **Exact ID match** — If the entity type has a canonical ID (place_id, NPI number,
   domain), match on that first. Exact match = same entity, merge fields.
2. **Domain normalization** — Strip `www.`, trailing slashes, protocol. Compare root
   domains. `www.acme.com/` and `acme.com` are the same entity.
3. **Fuzzy name + location** — Normalize names before comparing:
   - Lowercase all characters
   - Strip titles and honorifics (`Dr.`, `Mr.`, `Ms.`, etc.)
   - Strip credential suffixes (`MD`, `DDS`, `Inc`, `LLC`, `Corp`, etc.)
   - Strip common noise words (`The`, `and`, `of`, `&`)
   - Collapse whitespace and punctuation
   - Compare normalized names with location context if available
   This catches cross-source variations like "Dr. Jane Smith, MD" (Maps) vs
   "Jane Smith" (Yelp) vs "Smith Eye Care LLC" (BBB). Each source formats names
   differently — always normalize before comparing.

Track `source_count` per entity — entities confirmed by multiple sources are higher
quality. Each skill defines which layers apply and any domain-specific matching rules
in its reference files.

---

## Entity Confidence Scoring

Rate each entity's data completeness so users know what to trust.

Generic formula — each skill defines its own target field list (N fields):
- **High** — All target fields found + confirmed by 2+ sources (`source_count >= 2`)
- **Medium** — >50% of target fields found
- **Low** — ≤50% of target fields found

Display the confidence level in output (e.g., `⬤⬤⬤ High`, `⬤⬤○ Medium`,
`⬤○○ Low`). Each skill defines its field list and may add criteria (e.g., requiring
a verified phone number for High in a provider directory skill).

---

## Input Parsing Pattern

Skills that accept batch input (lists of URLs, companies, locations) should detect
the input type automatically:

| Input signature | Type | Action |
|----------------|------|--------|
| Contains `docs.google.com/spreadsheets` | Google Sheet URL | Read sheet directly |
| Path ends in `.csv` and file exists | CSV file | Read and parse as CSV |
| Contains multiple URLs (one per line or comma-separated) | Inline URL list | Parse directly |
| Otherwise | Unknown | Ask user for input |

Normalize all inputs to a uniform list of records before batch processing. Don't
assume a specific format — detect and adapt.

---

## Scaled Execution

When a skill needs to run multiple WSA or API calls, choose the execution tier
based on the estimated number of requests. Each skill calculates its own estimate
from input size and operations per record.

| Estimated calls | Strategy | How |
|----------------|----------|-----|
| **1–10** | Individual calls | Parallel Bash calls (max 4 concurrent) |
| **11–100** | Single batch | `extract-batch` or `agent run-batch` — one API call, server-side parallelism, poll for results |
| **100–1,000** | Multiple batches | Split into batches of up to 1,000. Use sub-agents to prepare inputs and process results |
| **>1,000** | Confirmation gate + batches | Show estimate, ask user to confirm before proceeding, then execute via batches |

### Individual calls (1–10)

Run up to 4 concurrent Bash calls per the Parallel Execution rules above.

### Batch calls (11+)

**For page extraction (11+ URLs):**
```bash
nimble extract-batch \
  --shared-inputs 'format: markdown' \
  --input '{"url": "https://example.com/page-1"}' \
  --input '{"url": "https://example.com/page-2"}'
```

Add `--shared-inputs 'render: true'` if pages need JavaScript rendering.

**For WSA/agent calls (11+ entities):**
```bash
nimble agent run-batch \
  --shared-inputs 'agent: {agent_name}' \
  --input '{"params": {...}}' \
  --input '{"params": {...}}'
```

Both return a `batch_id`. Poll progress:
```bash
nimble batches progress --batch-id {batch_id}
```

Fetch results when complete:
```bash
nimble batches get --batch-id {batch_id}
nimble tasks results --task-id {task_id}
```

Batch API handles up to 1,000 requests per call with server-side orchestration.
For >1,000 requests, split into multiple batch calls.

**Sub-agents should also batch.** When spawning sub-agents for parallel work, tell
each agent to use `extract-batch` or `agent run-batch` for its assigned items
rather than making individual calls. One batch call per agent is faster and more
reliable than 5-6 sequential calls.

### Large job confirmation (>1,000)

Before executing, show the estimate and ask the user to confirm:

```
Estimated API calls: ~2,400 (120 locations × 3 WSAs per location × ~7 enrichment)
This is a large job. Proceed? [Y/n]
```

Pattern: **estimate → display → gate → execute**

### Why batch over individual calls

Individual `nimble agent run` calls each require a separate HTTP round-trip and
Bash tool invocation. At scale (dozens+) this is slow, unreliable, and wasteful
on a local machine. Batch APIs move orchestration server-side — one API call
triggers all requests, and you poll for results. Always prefer batch when above
the individual threshold.

---

## Query Construction Tips

- **Be specific:** "Acme Corp product launch 2026" > "Acme Corp"
- **Use `--include-domain '["domain"]'`** for companies with generic names
- **Fallback on empty:** If < 3 results, retry without `--start-date`
- **Combine focus modes:** news + general in parallel for broader coverage
- **Try variations:** "CompanyName" → "Company Name" → domain
