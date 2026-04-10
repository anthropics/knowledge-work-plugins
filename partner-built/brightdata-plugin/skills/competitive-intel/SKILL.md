---
name: competitive-intel
description: >
  Real-time competitive intelligence and market research using Bright Data's
  web scraping infrastructure. Analyzes competitors' pricing, features, reviews,
  hiring patterns, content strategy, and market positioning with live web data.
  Use this skill when the user wants to analyze competitors, compare products,
  monitor pricing changes, track market trends, research a market landscape,
  build competitive battlecards, find positioning opportunities, or conduct
  any form of competitive or market research. Also use when the user mentions
  competitor analysis, market intelligence, competitive landscape, win/loss
  analysis, or wants to understand what competitors are doing.
---

# Competitive Intelligence

Real-time competitive intelligence powered by live web data. Combines Bright Data CLI (`bdata`) for data collection with strategic analysis frameworks to deliver actionable competitive insights — not stale training knowledge.

**Never answer competitive questions from training knowledge alone.** Always gather live data first using `bdata` commands, then analyze and synthesize.

## Prerequisites

1. Bright Data CLI installed:
   ```bash
   curl -fsSL https://cli.brightdata.com/install.sh | bash
   ```
2. One-time login completed:
   ```bash
   bdata login
   ```

That's it. No env vars, no zone config, no API keys to manage.

## Core Workflow

For every competitive intelligence request, follow this workflow:

1. **Clarify scope** — Which competitors? What specifically does the user want to know? Select the right module(s).
2. **Gather live data** — Run `bdata` commands. Parallelize independent calls. Prefer `bdata pipelines` (structured JSON) over `bdata scrape` (raw markdown) when a pipeline exists.
3. **Analyze** — Apply the appropriate strategic framework. Read [references/analysis-frameworks.md](references/analysis-frameworks.md) for SWOT, Porter's Five Forces, positioning matrices, and more.
4. **Format output** — Use the report templates from [references/output-templates.md](references/output-templates.md).
5. **Deliver actionable insights** — Every report MUST end with a "Strategic Recommendations" section. Never deliver raw data without interpretation.

## Data Collection Rules

- **Always use `--json` flag** when you need to pipe or parse `bdata` output programmatically
- **Prefer `bdata pipelines`** over `bdata scrape` whenever a pipeline type exists for the target platform — pipelines return clean structured JSON
- **Be cost-efficient** — A snapshot should use 3-8 `bdata` calls, not 50. Scrape what you need.
- **Parallelize** — Run independent `bdata` calls in parallel using multiple Bash tool calls in a single response
- **Handle failures gracefully** — If a page is gated or returns empty, say so and try the fallback. Never hallucinate data to fill gaps.
- **Cite every data point** — Include source URLs for everything. Users must be able to verify.

For the full mapping of intelligence needs to `bdata` commands, read [references/data-source-guide.md](references/data-source-guide.md).

For interpreting raw data as strategic signals, read [references/industry-signals.md](references/industry-signals.md).

---

## Analysis Modules

### 1. Competitor Snapshot

**When to use**: User asks to analyze, profile, or understand a specific competitor.

**Data gathering**:
```bash
# Step 1: Discover competitor's website and recent news
bdata search "[competitor name]" --json

# Step 2: Scrape key pages (run in parallel)
bdata scrape [competitor-url]              # Homepage — positioning, messaging
bdata scrape [competitor-url]/pricing      # Pricing tiers and model
bdata scrape [competitor-url]/about        # Team, mission, history (try /about, /about-us, /company)

# Step 3: Structured data enrichment (if URLs available)
bdata pipelines crunchbase_company "[crunchbase-url]"       # Funding, investors, employee count
bdata pipelines linkedin_company_profile "[linkedin-url]"   # Employee count, growth, locations
```

**Analysis**: Synthesize into a structured profile. Identify positioning, target audience, key claims, strengths, and vulnerabilities. Compare to user's product if context is available.

**Output**: Use the Competitor Snapshot template from [references/output-templates.md](references/output-templates.md).

---

### 2. Pricing Intelligence

**When to use**: User wants to compare pricing, understand pricing models, or find pricing positioning opportunities.

**Data gathering**:
```bash
# Scrape pricing pages for each competitor (run in parallel)
bdata scrape [competitor-a-url]/pricing
bdata scrape [competitor-b-url]/pricing
bdata scrape [competitor-c-url]/pricing

# For e-commerce products
bdata pipelines amazon_product "[amazon-url]"
bdata pipelines walmart_product "[walmart-url]"

# Supplementary: third-party pricing breakdowns
bdata search "[competitor] pricing review" --json
```

**Analysis**: Extract plan names, prices, feature lists, and limits from each page. Normalize into a comparison matrix. Identify pricing model types (per-seat, usage-based, freemium, enterprise-only). Flag positioning signals and recommend opportunities.

**Output**: Use the Pricing Intelligence template from [references/output-templates.md](references/output-templates.md).

---

### 3. Review Intelligence

**When to use**: User wants to understand customer sentiment, find competitor pain points, or identify exploitable gaps.

**Data gathering**:
```bash
# Find review pages via search
bdata search "[competitor] site:g2.com" --json
bdata search "[competitor] site:capterra.com" --json

# Scrape review pages
bdata scrape [g2-url]
bdata scrape [capterra-url]

# Structured review data (use when direct URLs are available)
bdata pipelines google_maps_reviews "[google-maps-url]" 30
bdata pipelines amazon_product_reviews "[amazon-url]"
bdata pipelines google_play_store "[play-store-url]"
bdata pipelines apple_app_store "[app-store-url]"
```

**Analysis**: Categorize sentiment (positive/neutral/negative). Extract top praised features, top complaints, and feature requests. Identify comparison mentions ("switched from X", "better than Y"). Complaints are the user's positioning opportunity.

**Output**: Use the Review Intelligence template from [references/output-templates.md](references/output-templates.md).

---

### 4. Hiring Signal Analysis

**When to use**: User wants to infer a competitor's strategic direction from their hiring patterns.

**Data gathering**:
```bash
# Find LinkedIn company page
bdata search "[competitor] linkedin company" --json

# Get structured job listings
bdata pipelines linkedin_job_listings "[linkedin-company-url]"

# Fallback: scrape careers page directly
bdata search "[competitor] careers" --json
bdata scrape [careers-url]
```

**Analysis**: Categorize roles by department. Analyze hiring velocity (scaling vs. stable vs. contracting). Identify technology signals from job descriptions. Look for geographic expansion signals. Interpret seniority mix (hiring leaders = new initiative; hiring ICs = scaling existing).

**Output**: Use the Hiring Signal Analysis template from [references/output-templates.md](references/output-templates.md).

---

### 5. Content & SEO Battle

**When to use**: User wants to understand competitors' content strategy or search positioning for specific keywords.

**Data gathering**:
```bash
# Check SERP rankings for target keywords (run in parallel)
bdata search "[keyword 1]" --json
bdata search "[keyword 2]" --json
bdata search "[keyword 3]" --json

# Estimate competitor's indexed content
bdata search "site:[competitor.com]" --json

# Scrape blog/content pages
bdata scrape [competitor-url]/blog
bdata scrape [top-ranking-article-url]
```

**Analysis**: Map which competitors rank for which keywords. Estimate content volume and publishing frequency. Identify topic clusters each competitor invests in. Find content gaps — topics nobody covers well that the user could own.

**Output**: Use the Content & SEO Battle template from [references/output-templates.md](references/output-templates.md).

---

### 6. Market Landscape Map

**When to use**: User wants to understand all players in a market, find white space, or map the competitive landscape.

**Data gathering**:
```bash
# Discover players via multiple search queries (run in parallel)
bdata search "[industry] companies" --json
bdata search "best [product category] tools" --json
bdata search "[product category] alternatives" --json

# Scrape category/comparison pages
bdata scrape [g2-category-url]

# Quick snapshot of each discovered competitor
bdata scrape [competitor-1-url]
bdata scrape [competitor-2-url]
# ... for each key player (limit to top 8-10)

# Enrich key players with funding/size data
bdata pipelines crunchbase_company "[crunchbase-url]"
```

**Analysis**: Categorize players by tier (enterprise, mid-market, SMB, open-source). Build a positioning map (e.g., price vs. feature breadth). Identify white space — underserved segments or positioning no one owns. Note market trends, recent entrants, and consolidation signals.

**Output**: Use the Market Landscape Map template from [references/output-templates.md](references/output-templates.md).

---

## Multi-Module Analysis

When the user asks for a comprehensive competitive analysis (e.g., "full battlecard", "deep dive", "board meeting prep"), combine multiple modules:

1. Start with **Competitor Snapshot** for each competitor
2. Add **Pricing Intelligence** for comparison
3. Add **Review Intelligence** for customer sentiment
4. Optionally add **Hiring Signals** and **Content & SEO** for strategic depth
5. Wrap everything in the **Executive Summary** template from [references/output-templates.md](references/output-templates.md)

For full battlecards, use the **Competitive Battlecard** template.

## Choosing the Right Module

| User says... | Module to use |
|-------------|--------------|
| "Analyze [competitor]", "Tell me about [company]" | Competitor Snapshot |
| "Compare pricing", "How much does [X] cost" | Pricing Intelligence |
| "What do customers think", "Reviews of [X]", "Pain points" | Review Intelligence |
| "What are they hiring for", "Job postings", "Where are they expanding" | Hiring Signal Analysis |
| "How do they rank", "Their content strategy", "SEO" | Content & SEO Battle |
| "Who are the players", "Market landscape", "Competitive landscape" | Market Landscape Map |
| "Full battlecard", "Deep competitive analysis", "Board prep" | Multi-Module (combine all) |

## Output Quality Standards

1. **Every data point must have a source URL** — no unattributed claims
2. **Separate facts from analysis** — clearly distinguish scraped data from Claude's interpretation
3. **End with "So What?"** — every report must have actionable strategic recommendations
4. **Be honest about gaps** — if data is unavailable, say so. Never fill gaps with training knowledge presented as live data.
5. **Date-stamp the analysis** — include "Data collected on [date]" so users know freshness
