---
name: competitor-positioning
description: |
  Tracks how competitors position themselves online — scrapes homepages,
  features, pricing, and blogs to extract messaging, value props, CTAs, and
  pricing models. Compares against previous snapshots to surface positioning
  shifts with before/after tracking. Produces messaging matrices, content gap
  analysis, white space maps, and battlecard inputs.

  Use when anyone asks about competitor messaging, positioning, website copy,
  content strategy, or how competitors present themselves. Triggers: "competitor
  positioning", "messaging comparison", "content gap", "what changed on their
  site", "competitor homepage", "landing page teardown", "marketing battlecard",
  "how do they describe their product", "share of voice", "counter-messaging".

  Do NOT use for business signals like funding/hiring (use competitor-intel),
  single-company deep dives (use company-deep-dive), or meeting prep (use
  meeting-prep).
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

# Competitor Positioning

Marketing-focused competitive positioning analysis powered by Nimble's web data APIs.
Built for marketing teams who need to understand how competitors present themselves —
messaging, value props, content themes, pricing — and how that evolves over time.

The output is a **marketing briefing**, not a signal feed. Every insight should answer:
"what does this mean for our messaging and positioning?"

User request: $ARGUMENTS

**Argument parsing** — determine what to do before running anything:
- No arguments → run full workflow (scope confirmation in Step 2)
- Competitor names (e.g., "Exa, Tavily") → research only those, skip scope confirmation
- "battlecard [competitor]" → skip to Battlecard Generation (see below) using
  existing snapshots from memory
- "delta" / "what changed" → force delta mode regardless of timing

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight

Run the preflight pattern from `references/nimble-playbook.md` (5 simultaneous Bash
calls: date calc, today, CLI check, profile load, index.md load).

From the results:
- CLI missing or API key unset → `references/profile-and-onboarding.md`, stop
- Profile exists → load prior data from two sources:
  - `~/.nimble/memory/positioning/*.md` — prior positioning snapshots (used for
    delta detection in Steps 4 + 5)
  - `~/.nimble/memory/competitors/*.md` — business signals from competitor-intel
    runs (provides context for *why* positioning may have shifted, e.g., a funding
    round or leadership change that preceded a messaging pivot)
  Determine mode:
  - **Full snapshot:** first run OR no prior positioning data OR last run > 14 days ago
  - **Delta mode:** last run < 14 days ago — only surface what changed
  - **Same-day repeat:** if `last_runs.competitor-positioning` is today, check for
    existing report at `~/.nimble/memory/reports/competitor-positioning-[today].md`.
    If found, ask: "Already ran today. Run again for fresh data?" Don't silently re-run.
  - Skip to Step 2
- No profile → Step 1

### Step 1: First-Run Onboarding (2 prompts max)

This skill shares the competitor list from `competitor-intel`. If a profile already
exists with competitors, skip onboarding entirely.

If no profile exists, follow `references/profile-and-onboarding.md` for the full
onboarding flow. The profile and competitor list created here will be shared across
all business skills.

### Step 2: Confirm Scope

If `$ARGUMENTS` already specifies competitors, use those and skip this step.

Otherwise, check how many competitors are in the profile:
- **4 or fewer** → proceed with all, no confirmation needed
- **More than 4** → ask which to focus on (use AskUserQuestion):

  > You have [N] competitors tracked. Which ones should I analyze?
  > - **All [N]** (~[3-5 × N] Nimble API credits, ~[N × 2] min)
  > - **[Category A]**: [names] (grouped by `category` from profile)
  > - **[Category B]**: [names]
  > - **Let me pick** — I'll list them

  Accept natural language: "just the AI search ones" → resolve from profile categories.

This prevents wasted API credits and wall time on competitors the user doesn't care
about right now. Each competitor costs ~3-5 Nimble API credits (1 map + 3-4 extracts
+ 2-3 searches).

### Step 3: WSA Discovery

For each competitor domain and the user's domain, discover available WSAs:

```bash
nimble agent list --search "{domain}" --limit 20
```

Run one search per domain simultaneously. Filter for SERP/PDP WSAs, prefer
`managed_by: "nimble"`, validate with `nimble agent get --template-name {name}`.
Cache discovered names + params. Pass them to competitor agents in Step 5 for
richer extraction. If no WSAs found, continue with `nimble search/extract/map`.

### Step 4: Capture the User's Own Positioning (baseline)

Before analyzing competitors, capture the user's own positioning as a baseline for
the messaging matrix.

**First, discover the site structure** to find the right pages to extract:

`nimble --transform "links.#.url" map --url "https://[company-domain]" --sitemap only --limit 200`

From the returned URLs, identify the features/product page and pricing page (look
for paths containing `/features`, `/product`, `/platform`, `/pricing`, `/plans`).

**Then extract the key pages simultaneously** (homepage + whichever pages map found):

- `nimble extract --url "https://[company-domain]" --format markdown`
  → Homepage messaging, tagline, hero copy, CTAs
- `nimble extract --url "[features-page-url]" --format markdown`
  → Features page structure and emphasis (skip if map found no match)
- `nimble extract --url "[pricing-page-url]" --format markdown`
  → Pricing structure and tier naming (skip if map found no match)

If a page extraction returns garbage, note "page not accessible" and continue —
partial baseline is better than none.

### Step 5: Parallel Research Per Competitor (sub-agents)

Read `references/positioning-agent-prompt.md` for the full agent prompt template.
Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

**Call estimation & Scaled Execution:** Before launching agents, estimate total API
calls: ~1 map + 3 extractions + 3 searches per competitor = ~7 × N calls (plus baseline
from Step 3). For 2+ competitors (14+ calls), tell agents to use `extract-batch` for
page extractions instead of individual calls. See the Scaled Execution pattern in
`references/nimble-playbook.md` for tier selection.

For each competitor in scope, spawn a **general-purpose** sub-agent with
`mode: "bypassPermissions"` and inline the prompt from
`references/positioning-agent-prompt.md`. Customize the prompt with each competitor's
name, domain, start-date, previous positioning snapshot from memory (loaded in
Step 0), and any discovered WSA names from Step 3 for richer data access.

Do NOT use `agents/nimble-researcher.md` — that agent is scoped for raw data gathering
and explicitly forbids analysis, but this skill requires interpretive work (identifying
audience signals, comparing positioning snapshots, assessing structure implications).

Each agent handles the complete research cycle for one competitor:
1. `nimble map` to discover the site's actual page structure
2. Extract homepage, features, and pricing pages (using discovered URLs)
3. Search for and extract recent blog posts (2-3 deep dives)
4. Analyze social proof (case studies, testimonials)
5. Compare against previous snapshot for changes

The agent returns a structured positioning snapshot — see the prompt template for the
full output format. No separate blog extraction step is needed; agents handle it.

**If an agent's blog extraction was thin** (< 2 posts extracted), optionally extract
additional posts from the main context using URLs from the agent's search results.

**Fallback:** If an agent fails entirely, run extractions directly from the main context
using the same prompt template steps.

### Step 6: Analysis & Output

Frame everything for a marketing team. Use terms they work with: messaging
hierarchy, share of voice, battlecard inputs, content calendar implications.

When analyzing blog content from agent results, look for:
- **Recurring narratives** — what story is this company telling repeatedly?
- **Audience targeting** — are posts aimed at developers, executives, practitioners?
- **Competitive mentions** — do they name competitors or position against categories?
- **SEO patterns** — what keywords do titles and headings target?
- **Content maturity** — original research, thought leadership, or generic how-tos?

**Full snapshot mode** (first run or > 14 days since last):

- **TL;DR for Marketing** — 3-5 key positioning insights the marketing team should
  act on, each with a specific implication (e.g., "Competitor X shifted tagline from
  developer-focused to enterprise — consider whether our messaging still differentiates")

- **Messaging Matrix** — build a comparison table with rows for Tagline, Primary CTA,
  Value Props, Target Audience, and Pricing Model across all competitors including
  your company. Use verbatim quotes for taglines and CTAs.

- **Per Competitor — Positioning Profile**:
  - Site structure signals (what pages exist/don't exist, subdomains)
  - Homepage messaging breakdown (tagline, hero, CTAs, value props)
  - Features page analysis (what they emphasize, differentiation claims)
  - Pricing positioning (model, tier strategy, enterprise signals)
  - Content strategy (blog themes, cadence, audience, content types)
  - Social proof strategy (who they showcase, what outcomes they highlight)

- **Content Gap Analysis** — what competitors are publishing that you're not:
  - Topics they cover that you don't
  - Content formats they use (case studies, benchmarks, ROI calculators)
  - Audience segments they address in content

- **Positioning White Space** — messaging angles no competitor has claimed strongly:
  - Unclaimed value props
  - Underserved audience segments
  - Narrative gaps

- **Recommended Actions** — specific, actionable next steps for the marketing team
  (e.g., "Draft counter-messaging for Competitor X's new enterprise positioning",
  "Prioritize case studies targeting [segment] — 3 competitors already own this space")

**Delta mode** (last run < 14 days) — changes only:

- **What Changed** — per competitor, before/after for each shift:
  - "Tagline: '[old]' → '[new]'"
  - "New feature category added: [name]"
  - "Pricing model shifted from [old] to [new]"
  - "New blog theme emerging: [topic] (3 posts in last 2 weeks)"

- **Nothing Changed** — list competitors with no positioning shifts

- **Marketing Implications** — what the changes mean for your team's priorities

**Core rules:**
- Every claim must link to the source page.
- Deduplicate against `~/.nimble/memory/positioning/*.md` — in delta mode, only
  surface genuinely new changes.
- Say "no positioning changes detected" rather than padding with fluff.
- Use verbatim quotes for taglines, CTAs, and value props — don't paraphrase.

**WSA enrichment:** If WSAs were discovered in Step 3, agents should use them
alongside `nimble map`/`nimble extract` for richer page data.

### Step 7: Save & Update Memory

Make all Write calls simultaneously:

- Report → `~/.nimble/memory/reports/competitor-positioning-[date].md`
  (save the **full briefing**, not a summary — this is the local source of truth)

- Per competitor → save positioning snapshot to
  `~/.nimble/memory/positioning/[name].md` using the format in
  `references/positioning-snapshot-format.md`. Append a dated entry to the History
  section so future runs can detect what changed and when. Add `[[competitors/name]]`
  cross-references to link positioning snapshots to competitor intel files.

- Profile → update `last_runs.competitor-positioning` in
  `~/.nimble/business-profile.json`

- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.

### Step 8: Share & Distribute

**Always offer distribution — do not skip this step.** Follow
`references/memory-and-distribution.md` for connector detection, sharing flow, and
source links enforcement. Marketing teams especially benefit from shared Notion pages
they can reference in positioning workshops and content planning sessions.

### Battlecard Generation

Triggered by `"battlecard [competitor]"` argument or as a follow-up request.

**Inputs:** Read the competitor's positioning snapshot from
`~/.nimble/memory/positioning/[name].md` and the user's own baseline from the most
recent report. If no snapshot exists (or it's stale > 14 days), run Steps 4-5 for
that competitor first, then return here.

**Output format:**

```
# Battlecard: [Your Company] vs [Competitor]
## As of [date]

### Competitor Overview
- Tagline: [verbatim]
- Primary CTA: [verbatim]
- Target audience: [who their messaging speaks to]
- Pricing model: [type and entry price if known]

### Their Key Claims
[List each value prop / differentiator they emphasize, verbatim with source URL]

### Our Counter-Positioning
[For each claim above: our response, proof points, and messaging angle]

### Feature Comparison
| Capability | Us | Them | Advantage |
|---|---|---|---|

### Where They Win (acknowledge honestly)
[Areas where their positioning is stronger or they have genuine advantages]

### Where We Win
[Our unique advantages, with evidence]

### Objection Handling
| Prospect Says | Respond With |
|---|---|

### Recommended Talking Points
[3-5 concise talking points for sales/marketing conversations]
```

---

### Step 9: Follow-ups

- **Generate battlecard** for a competitor → runs Battlecard Generation above
- **Draft counter-messaging** for a specific competitor claim → suggest alternative
  angles and proof points
- **Content calendar comparison** → map your publishing against competitors' cadence
- **Go deeper** on a competitor → extract additional pages (about, careers, partners,
  case studies)
- **Track a new competitor** → update `competitors`, create positioning snapshot
- **Skip a competitor** → update `preferences.skip_competitors`
- **"Looks good"** → done

**Sibling skill suggestions:**

> **Next steps:**
> - Run `competitor-intel` for business signals (funding, hiring, product launches)
> - Run `company-deep-dive` for a full 360 profile on any competitor
> - Run `meeting-prep` if you're meeting with someone at a competitor

---

## Agent Teams Mode (Dual-Mode)

Check at startup: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`

**Team mode** (flag set):
- Use the `Agent` tool with `name:` parameter so teammates are addressable
- Teammates can use `SendMessage` to share cross-competitor patterns they discover
  (e.g., "two competitors both shifted to usage-based pricing this month")
- After all competitor teammates return, spawn a **Marketing Analyst** teammate
  with all findings as input, focused solely on content gap analysis and positioning
  white space — this separates data collection from strategic analysis
- Lead synthesizes the final cross-validated marketing briefing

**Solo mode** (flag not set):
- Standard fire-and-forget sub-agents (no `SendMessage`, no `name:`)
- All analysis happens in the main context after agents return

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key, 429,
401, empty results, extraction garbage). Skill-specific errors:

- **Search 500:** Retry once without `--focus` flag. If still failing, retry with a
  simplified query (shorter terms, no date filter). Log the failure but don't skip
  the competitor.
- **Search timeout:** Retry once, then skip that call and continue — consistent with
  the playbook's timeout policy.
- **Page extraction fails (404/garbage):** The map step should prevent most 404s by
  discovering actual URLs first. If extraction still fails, note "page not accessible"
  and continue — partial data is better than no data.
- **Map returns empty:** Some sites block sitemap access. Fall back to extracting
  the homepage directly and guessing common paths (/features, /pricing, /blog).
- **Empty blog results:** Some companies don't blog. Note "no active blog detected"
  and focus on page-based positioning instead.
