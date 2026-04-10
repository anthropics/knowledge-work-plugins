---
name: company-deep-dive
description: |
  Use this skill ANY TIME the user asks about a specific company. Triggers:
  "tell me about [company]", "research [company]", "what does [company] do",
  "who is [company]", "look up [company]", "company deep dive", "due diligence
  on [company]", "background on [company]", "dig into [company]", "analyze
  [company]", or evaluating a company for investment, partnership, or sales.
  MUST be used instead of answering from memory — fetches real-time web data
  (funding, leadership changes, product launches, news) your training data
  lacks. Use even for well-known companies.

  Produces a sourced 360° report covering funding, leadership, product/tech,
  market position, news, and strategic outlook with dates and URLs.

  Do NOT use for multi-company competitor monitoring (use competitor-intel)
  or meeting prep with attendees (use meeting-prep).
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

# Company Deep Dive

360° company research powered by Nimble's web data APIs.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight

Run the preflight pattern from `references/nimble-playbook.md` (5 simultaneous Bash
calls: date calc, today, CLI check, profile load, index.md load).

From the results:
- CLI missing or API key unset → `references/profile-and-onboarding.md`, stop
- Profile exists → note it for context (company name helps frame the research). Read
  `~/.nimble/memory/companies/index.md` to check if the target company already has
  prior research. Follow `[[path/entity]]` cross-references to load related context.
  - **Prior research exists:** Load it. Run in **refresh mode** — focus on what's new
    since the last report date. Tell the user: "I have prior research on [Company]
    from [date]. Refreshing with latest data."
  - **No prior research:** Run in **full mode** — comprehensive across all dimensions.
- No profile → that's fine. Company deep dive doesn't require onboarding (unlike
  competitor-intel). Proceed directly to Step 1.

### Step 1: Identify Target Company

Parse the target company from `$ARGUMENTS` or the user's message.

**If clear** (e.g., "research Stripe", "tell me about Datadog"):
- Extract the company name
- Run two Bash calls simultaneously to confirm identity:
  - `nimble search --query "[Company] official site" --max-results 3 --search-depth lite`
  - `nimble search --query "[Company] company overview" --max-results 5 --search-depth lite`
- Confirm briefly: "Researching **[Company]** ([domain])..."

**If ambiguous** (e.g., "research Mercury" — could be bank, auto, or other):
- Ask one clarifying question with the top candidates

**If missing** — ask: "Which company would you like me to research?"

**Scope selection** — if the user hasn't specified depth, default to **full deep dive**.
If they say "quick overview", "brief", or "summary", run a **quick mode** that skips
the Deep Extraction step and produces a shorter report.

### Step 2: WSA Discovery

Discover available WSAs for the target company's domain. Run both searches
simultaneously:

```bash
nimble agent list --search "{company-domain}" --limit 20
```

```bash
nimble agent list --search "{company-name}" --limit 20
```

From the results, filter for WSAs with `entity_type` matching SERP or PDP, and
prefer `managed_by: "nimble"`. Validate each with
`nimble agent get --template-name {name}`, then cache discovered WSA names + params
for the run. Pass them to dimension agents in Step 3 for enrichment alongside
`nimble search`. If no WSAs found, continue with `nimble search` alone.

### Step 3: Parallel Research Across Dimensions (sub-agents)

Read `references/dimension-agent-prompt.md` for the full agent prompt template.
Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

Spawn `nimble-researcher` agents (`agents/nimble-researcher.md`) with
`mode: "bypassPermissions"`. Each agent researches one dimension of the company.
Pass discovered WSA names from Step 2 to each agent so they can use them for
enrichment alongside `nimble search`.

**Important:** The Nimble API has a 10 req/sec rate limit per API key. With each agent
running 4-5 searches in parallel, limit concurrent agents to 2 per batch to stay under
the limit. Run overview searches in their own phase, not alongside agent batches.

**Call estimation & Scaled Execution:** Before launching agents, estimate total API
calls: 2 overview searches + ~5 searches per agent × 5 agents = ~27 calls. Each agent
should use `extract-batch` or `agent run-batch` for 11+ calls instead of individual
calls. See the Scaled Execution pattern in `references/nimble-playbook.md` for tier
selection.

**Phase A — Overview searches** (run directly, before agents):

- `nimble search --query "about" --include-domain '["[domain]"]' --max-results 3 --search-depth lite`
- `nimble search --query "[Company] Wikipedia OR Crunchbase OR Pitchbook" --max-results 5 --search-depth lite`

These give foundational context (founding date, HQ, employee count, mission) that
frames all dimensional findings.

**Phase B — Batch 1** (2 agents simultaneously):

| Agent | Dimension | Focus |
|-------|-----------|-------|
| 1 | **Funding & Financials** | Funding rounds, valuation, revenue signals, investors, financial health |
| 2 | **Product & Technology** | Products, tech stack, recent launches, engineering blog, open-source |

**Phase C — Batch 2** (2 agents simultaneously):

| Agent | Dimension | Focus |
|-------|-----------|-------|
| 3 | **Leadership & Team** | Founders, C-suite, key hires, departures, team size, culture signals |
| 4 | **Recent News & Events** | Press coverage, announcements, partnerships, awards, conferences |

**Phase D — Batch 3** (1 agent):

| Agent | Dimension | Focus |
|-------|-----------|-------|
| 5 | **Market Position** | Competitors, market share, positioning, analyst coverage, customer reviews |

**Refresh mode adjustment:** If prior research exists, pass the known facts to each
agent as context so they focus on what's new. Agents should use `--start-date` to
filter for recent data only.

**Fallback:** If any agent fails or returns empty, run those dimension searches
directly from the main context. Don't leave gaps in the report.

### Step 4: Deep Extraction

From all agents' results, identify the **top 5-8 most informative URLs** across
dimensions. Prioritize:
- Funding announcements with specific amounts
- Official product/feature pages
- Executive interviews, podcast appearances, or conference talks
- In-depth analyst or journalist profiles
- The company's own about/team page

Make one Bash call per URL, all simultaneously:

`nimble extract --url "https://..." --format markdown`

For extraction failures, follow the fallback in `references/nimble-playbook.md`.

**Quick mode:** Skip this step entirely. Report from search snippets only.

**WSA enrichment:** If WSAs were discovered in Step 2, use them here for richer
extraction on key URLs before falling back to `nimble extract`.

### Step 5: Synthesize Report

Structure the output as a **360° Company Report**:

```
# [Company Name] — Deep Dive
*As of [today's date]*

## Quick Assessment
[2-3 sentence verdict: what this company is, where they stand, and the one thing
that matters most right now. This is the "if you read nothing else" paragraph.]

## Company Overview
- Founded: [year] | HQ: [location] | Employees: [estimate]
- Domain: [domain] | Industry: [industry]
- Mission/focus: [one line]

## Funding & Financials
[Latest round, total raised, key investors, valuation signals, revenue indicators.
Every claim dated and sourced.]

## Leadership & Team
[Founders, C-suite, notable recent hires or departures. Executive perspectives
on company direction — direct quotes when available from interviews or talks.]

## Product & Technology
[Core products, recent launches, tech stack signals, engineering culture,
open-source contributions. What they're building and how.]

## Market Position
[Key competitors, differentiation, market share signals, analyst perspectives,
customer sentiment from reviews (G2/Capterra/Reddit).]

## Recent News & Events
[Chronological, most recent first. Each entry dated with source.]

## Strategic Outlook
[Synthesis across all dimensions: where the company is heading, key risks,
growth signals, and strategic bets. This is insight, not summary.]

## Sources
[Numbered list of all URLs cited in the report]
```

**Core rules:**
- Every factual claim must have a date and source URL.
- Lead with the Quick Assessment — most readers stop there.
- Say "no public data found" for a dimension rather than speculating.
- Distinguish between confirmed facts and inferred signals.
- Executive quotes add credibility — include direct quotes from interviews,
  earnings calls, or conference talks when found.
- In refresh mode: lead with "What's New Since [last date]" before the full sections.

### Step 6: Save to Memory

Make all Write calls simultaneously:

- Report → `~/.nimble/memory/reports/company-deep-dive-[date].md`
- Company profile → `~/.nimble/memory/companies/[company-name-slug].md`
  (use the format in `references/memory-and-distribution.md`). Add `[[path/entity]]`
  cross-references for key people discovered (e.g., `[[people/jane-smith]]`),
  competitors in the same space (e.g., `[[competitors/widgetco]]`), and any other
  related entities.
- If profile exists → update `last_runs.company-deep-dive` in
  `~/.nimble/business-profile.json`
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.

The company profile in `companies/` should contain structured key facts (overview,
financials, leadership, products) that can be loaded by future runs of any skill
that needs context on this company.

### Step 7: Share & Distribute

**Always offer distribution — do not skip this step.** Follow
`references/memory-and-distribution.md` for connector detection, sharing flow, and
source links enforcement.

### Step 8: Follow-ups

- **Go deeper** on a dimension → focused searches on that topic
- **Compare with another company** → side-by-side analysis
- **"What about [specific topic]?"** → targeted search + extraction
- **"Looks good"** → done

**Sibling skill suggestions:**

> **Next steps:**
> - Run `competitor-intel` to track this company as a competitor over time
> - Run `meeting-prep` if you're meeting with someone at this company
> - Run `competitor-positioning` to analyze their messaging vs yours

---

## Agent Teams Mode (Dual-Mode)

Check at startup: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`

**Team mode** (flag set): Spawn 3 **teammates** instead of sub-agents. Each teammate
covers related dimensions and can message the others to cross-check findings.

| Teammate | Dimensions | Cross-checks with |
|----------|-----------|-------------------|
| **Financials & News** | Funding, revenue, recent news, events | Market (valuation vs positioning) |
| **Product & Leadership** | Products, tech stack, founders, key hires | Financials (pivots vs funding) |
| **Market** | Competitors, positioning, reviews, analysts | Product (differentiation claims) |

Lead (you): Create shared tasks, wait for all teammates to complete, then synthesize
the final report. When a teammate finds a claim that another should verify (e.g., a
funding amount that implies a valuation), it posts a task for the relevant teammate.

**Solo mode** (flag not set): Standard sub-agent flow from Step 3.

---

## What This Skill Is NOT

- **Not competitor monitoring.** For tracking multiple competitors over time, use
  `competitor-intel`. This skill goes deep on ONE company.
- **Not meeting prep.** For researching people you're meeting with, use `meeting-prep`.
  This skill researches companies, not individuals.
- **Not financial advice.** This is intelligence gathering from public sources, not
  investment analysis or due diligence certification.
- **Not real-time monitoring.** This produces a point-in-time report. For ongoing
  tracking, run it again later or use `competitor-intel` with the company added.

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key, 429,
401, empty results, extraction garbage). Skill-specific errors:

- **Search 500:** Retry once without `--focus` flag. If still failing, retry with a
  simplified query (shorter terms, no date filter). Log the failure but don't skip
  the dimension.
- **Search timeout:** Retry once, then skip that call and continue — consistent with
  the playbook's timeout policy.
- **Company not found:** Retry with domain, alternative names, or parent company
- **Empty results for a dimension:** Note "No public data found" — don't speculate
