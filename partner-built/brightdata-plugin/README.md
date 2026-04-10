<p align="center">
  <img src="https://brightdata.com/wp-content/themes/brightdata/assets/images/favicon.png" alt="Bright Data" width="80" height="80">
</p>

<h1 align="center">Bright Data Plugin for Claude Code</h1>

<p align="center">
  <strong>Unlock the web with AI-powered scraping, search, and structured data</strong>
</p>

<p align="center">
  <a href="https://brightdata.com"><img src="https://img.shields.io/badge/Powered%20by-Bright%20Data-3D7FFC?style=for-the-badge" alt="Powered by Bright Data"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" alt="MIT License"></a>
  <a href="#skills"><img src="https://img.shields.io/badge/Skills-11-9D97F4?style=for-the-badge" alt="11 Skills"></a>
  <a href="#data-feeds-skill"><img src="https://img.shields.io/badge/Datasets-40+-15C1E6?style=for-the-badge" alt="40+ Datasets"></a>
  <a href="#bright-data-mcp-skill"><img src="https://img.shields.io/badge/MCP_Tools-60+-FF6B35?style=for-the-badge" alt="60+ MCP Tools"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-skills">Skills</a> •
  <a href="#-data-feeds">Data Feeds</a> •
  <a href="#bright-data-mcp-skill">MCP</a> •
  <a href="#brightdata-cli-skill">CLI</a> •
  <a href="#competitive-intel-skill">Competitive Intel</a> •
  <a href="#scraper-builder-skill">Scraper Builder</a> •
  <a href="#best-practices-skill">Best Practices</a> •
  <a href="#python-sdk-best-practices-skill">Python SDK</a> •
  <a href="#-setup">Setup</a> •
  <a href="#-examples">Examples</a>
</p>

---

## Overview

This plugin brings **Bright Data's powerful web infrastructure** directly into Claude Code, enabling AI agents to:

- **Scrape any webpage** as clean markdown — bypassing bot detection, CAPTCHAs, and JavaScript rendering
- **Search Google** with structured JSON results — titles, links, and descriptions ready for processing
- **Extract structured data** from 40+ websites — Amazon, LinkedIn, Instagram, TikTok, YouTube, and more
- **Orchestrate 60+ MCP tools** — search, scrape, extract structured data, and automate browsers via Bright Data's MCP server
- **Use the Bright Data CLI** — scrape, search, extract data, manage zones, and check budget directly from the terminal with `brightdata` / `bdata`
- **Run competitive intelligence** — real-time competitor analysis, pricing monitoring, review mining, hiring signal analysis, and market landscape mapping using live web data
- **Write correct Bright Data code** — built-in best practices for Web Unlocker, SERP API, Web Scraper API, and Browser API
- **Build with the Python SDK** — comprehensive guide for the `brightdata-sdk` package with patterns for async/sync clients, platform scrapers, SERP, datasets, and more

Built on Bright Data's [Web Unlocker](https://brightdata.com/products/web-unlocker), [SERP API](https://brightdata.com/products/serp-api), and [Web Data APIs](https://brightdata.com/products/web-scraper), this plugin handles the complexity of web access so your AI agents can focus on what matters.

---

## Skills

| Skill | Description |
|-------|-------------|
| **`search`** | Search Google and get structured JSON results with titles, links, and descriptions |
| **`scrape`** | Scrape any webpage as clean markdown with automatic bot detection bypass |
| **`data-feeds`** | Extract structured data from 40+ websites with automatic polling |
| **`bright-data-mcp`** | Orchestrate 60+ Bright Data MCP tools for search, scraping, structured extraction, and browser automation |
| **`scraper-builder`** | Build production-ready scrapers for any website — guides through site analysis, API selection, selector extraction, pagination, and complete implementation. Triggers on "build a scraper for..." |
| **`bright-data-best-practices`** | Built-in reference for Web Unlocker, SERP API, Web Scraper API, and Browser API — Claude consults this automatically when writing Bright Data code |
| **`python-sdk-best-practices`** | Comprehensive guide for the `brightdata-sdk` Python package — async/sync clients, platform scrapers, SERP, datasets, Scraper Studio, Browser API, error handling, and common patterns |
| **`brightdata-cli`** | Guide for using the Bright Data CLI (`brightdata` / `bdata`) to scrape, search, extract structured data from 40+ platforms, manage proxy zones, and check account budget — all from the terminal |
| **`competitive-intel`** | Real-time competitive intelligence using live web data — competitor snapshots, pricing comparison, review mining, hiring signal analysis, content & SEO battles, and market landscape mapping. Replaces $15K+/yr enterprise CI tools at pennies per analysis |
| **`design-mirror`** | Replicates design system patterns, tokens, and components to build consistent, high-quality UIs |
| **`brd-browser-debug`** | Debug Bright Data Scraping Browser sessions — smart triage of failures, per-session bandwidth tracking, captcha reporting, and pattern detection using the Browser Sessions API |

---

## Quick Start

### 1. Get Your Credentials

1. Sign up at [brightdata.com](https://brightdata.com) if you haven't already
2. Go to the [Bright Data Dashboard](https://brightdata.com/cp)
3. Create a **Web Unlocker zone**: Click "Add" → Select "Unlocker zone"
4. Copy your **API Key** from the dashboard

### 2. Set Environment Variables

```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

### 3. Start Using

```bash
# Search Google
bash skills/search/scripts/search.sh "artificial intelligence trends"

# Scrape a webpage
bash skills/scrape/scripts/scrape.sh "https://example.com/article"

# Get LinkedIn profile data
bash skills/data-feeds/scripts/datasets.sh linkedin_person_profile "https://linkedin.com/in/satyanadella"
```

---

## Bright Data MCP Skill

The `bright-data-mcp` skill teaches Claude how to optimally use Bright Data's MCP server — selecting the right tool, handling errors, and following best practices across 60+ tools.

### MCP Server Connection

Connect the Bright Data MCP server using the remote URL:

```
https://mcp.brightdata.com/mcp?token=YOUR_BRIGHTDATA_API_TOKEN
```

**Optional parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `pro=1` | Enable all 60+ Pro tools | `...&pro=1` |
| `groups=<name>` | Enable specific tool groups | `...&groups=social,ecommerce` |
| `tools=<names>` | Enable specific tools only | `...&tools=search_engine,scrape_as_markdown` |

### Available Tool Groups

| Group | Tools | Platforms |
|-------|-------|-----------|
| **Rapid (Free)** | `search_engine`, `scrape_as_markdown` | Google/Bing/Yandex search, any webpage |
| **ecommerce** | 11 tools | Amazon, Walmart, eBay, Best Buy, Etsy, Home Depot, Zara, Google Shopping |
| **social** | 22 tools | LinkedIn, Instagram, Facebook, TikTok, YouTube, X, Reddit |
| **business** | 4 tools | Crunchbase, ZoomInfo, Google Maps, Zillow |
| **finance** | 1 tool | Yahoo Finance |
| **research** | 2 tools | Reuters, GitHub |
| **app_stores** | 2 tools | Google Play, Apple App Store |
| **travel** | 1 tool | Booking.com |
| **browser** | 13 tools | Full browser automation (navigate, click, type, screenshot) |
| **advanced_scraping** | 5 tools | HTML scraping, AI extraction, batch operations |

### Claude Code Setup

Add to your MCP settings:

```json
{
  "mcpServers": {
    "brightdata": {
      "url": "https://mcp.brightdata.com/mcp?token=YOUR_TOKEN&pro=1"
    }
  }
}
```

### Why This Skill Matters

The `bright-data-mcp` skill ensures Bright Data MCP is **always the default for all web data tasks** — replacing built-in tools like WebFetch and WebSearch with superior alternatives that handle bot detection, CAPTCHAs, and JavaScript rendering automatically.

With this skill:
- **Default web tool** — Claude always uses Bright Data MCP for any web data request, no exceptions
- **Replaces built-in tools** — `search_engine` replaces WebSearch, `scrape_as_markdown` replaces WebFetch
- **Automatic tool selection** — the most specific tool is chosen based on the task
- **Structured data preferred** — `web_data_*` tools used over raw scraping when available
- **Error handling** — built-in fallback strategies and URL validation guidance
- **Workflow orchestration** — multi-step workflows for research, competitive analysis, social monitoring, and lead generation

---

## Competitive Intel Skill

The `competitive-intel` skill turns Bright Data's scraping infrastructure into **real-time competitive intelligence** — replacing $15K–$50K/year enterprise CI tools (Crayon, Klue, AlphaSense) with an AI-native alternative that costs pennies per analysis.

### How it works

The skill combines **live web data** (via `bdata` CLI) with **strategic analysis frameworks** to deliver actionable competitive insights — not stale training knowledge.

Say "analyze my competitor" or "compare pricing" and Claude will:
1. Gather live data using `bdata search`, `bdata scrape`, and `bdata pipelines`
2. Apply the appropriate analytical framework (SWOT, Porter's Five Forces, positioning matrix, etc.)
3. Deliver a structured report with source citations and strategic recommendations

### Analysis modules

| Module | What it does | Data sources |
|--------|-------------|-------------|
| **Competitor Snapshot** | Quick profile: positioning, pricing, team, funding, strengths/weaknesses | `bdata scrape` (website), `bdata pipelines` (Crunchbase, LinkedIn) |
| **Pricing Intelligence** | Compare pricing across competitors with positioning analysis | `bdata scrape` (pricing pages), `bdata search` (third-party reviews) |
| **Review Intelligence** | Mine customer reviews for pain points, loved features, and gaps | `bdata scrape` (G2, Capterra), `bdata pipelines` (app stores, Google Maps) |
| **Hiring Signal Analysis** | Infer strategic direction from job postings | `bdata pipelines` (LinkedIn jobs), `bdata scrape` (careers pages) |
| **Content & SEO Battle** | Compare content strategy and search positioning | `bdata search` (SERP rankings), `bdata scrape` (blogs) |
| **Market Landscape Map** | Discover and categorize all players in a market | `bdata search` (discovery), `bdata scrape` (homepages), `bdata pipelines` (Crunchbase) |

### Example usage

```
> Analyze Notion as a competitor. I'm building a PM tool for small teams.

# Claude will:
# 1. Search Google for Notion
# 2. Scrape notion.com, /pricing, /about
# 3. Pull Crunchbase and LinkedIn data
# 4. Deliver a structured Competitor Snapshot with
#    pricing table, messaging analysis, strengths,
#    vulnerabilities, and strategic recommendations
```

```
> Compare pricing between Slack, Teams, and Discord

# Claude will:
# 1. Scrape all three pricing pages
# 2. Normalize into comparison matrix
# 3. Identify pricing models and positioning opportunities
# 4. Deliver a Pricing Intelligence Report
```

### Reference files

- [skills/competitive-intel/SKILL.md](skills/competitive-intel/SKILL.md) — Main skill with 6 analysis modules and CLI command patterns
- [skills/competitive-intel/references/data-source-guide.md](skills/competitive-intel/references/data-source-guide.md) — Maps 30+ CI needs to specific `bdata` commands
- [skills/competitive-intel/references/output-templates.md](skills/competitive-intel/references/output-templates.md) — 8 report templates (Snapshot, Pricing, Reviews, Hiring, Content, Landscape, Battlecard, Executive Summary)
- [skills/competitive-intel/references/analysis-frameworks.md](skills/competitive-intel/references/analysis-frameworks.md) — SWOT, Porter's Five Forces, positioning matrix, Jobs-to-be-Done, Blue Ocean, Win/Loss
- [skills/competitive-intel/references/industry-signals.md](skills/competitive-intel/references/industry-signals.md) — How to interpret pricing, hiring, content, review, funding, and social signals

---

## Scraper Builder Skill

The `scraper-builder` skill guides you through building **production-ready web scrapers** for any website. Say "build a scraper for [site]" and Claude will walk you through the entire process.

### How it works

The skill follows a 6-phase workflow:

1. **Understand the target** — What site, what data, what scope?
2. **Check for pre-built scrapers** — Searches 100+ supported domains via the Dataset List API before writing any custom code
3. **Site reconnaissance** — Fetches HTML via Web Unlocker, analyzes rendering (SSR vs CSR), discovers hidden APIs and JSON-LD data
4. **Build the extractor** — Picks the right approach: Web Unlocker + parsing, direct API endpoint, or Browser API with Playwright
5. **Handle pagination** — URL params, next-links, cursor tokens, infinite scroll, load-more buttons, sitemap crawling
6. **Assemble complete scraper** — Runnable script with config, fetcher, parser, paginator, output, and error handling

### API selection logic

| Scenario | API Used |
|----------|----------|
| Site has pre-built scraper (Amazon, LinkedIn, etc.) | Web Scraper API |
| Static HTML, no interaction needed | Web Unlocker |
| Site exposes JSON API internally | Web Unlocker → API endpoint |
| JS-rendered (React, Vue, Angular) | Browser API |
| Infinite scroll / click required | Browser API |
| Search engine results | SERP API |

### Example usage

```
> build a scraper for Amazon product pages, I have 50 ASINs

# Claude will:
# 1. Find Amazon's pre-built scraper
# 2. Use async trigger/poll/fetch for the batch
# 3. Output a complete Python script with structured JSON
```

```
> scrape all job listings from jobs.customsite.com with pagination

# Claude will:
# 1. Check for pre-built scraper (not found)
# 2. Fetch HTML to analyze structure
# 3. Pick Web Unlocker + BeautifulSoup
# 4. Handle pagination automatically
# 5. Output a complete working scraper
```

### Reference files

- [skills/scraper-builder/SKILL.md](skills/scraper-builder/SKILL.md) — Main skill with decision tree and code patterns
- [skills/scraper-builder/references/supported-domains.md](skills/scraper-builder/references/supported-domains.md) — Pre-built scraper lookup + dynamic Dataset List API
- [skills/scraper-builder/references/site-analysis-guide.md](skills/scraper-builder/references/site-analysis-guide.md) — HTML analysis playbook, selector strategy, hidden API discovery
- [skills/scraper-builder/references/pagination-patterns.md](skills/scraper-builder/references/pagination-patterns.md) — 7 pagination strategies with complete code examples

---

## Brightdata CLI Skill

The `brightdata-cli` skill teaches Claude how to use the [Bright Data CLI](https://github.com/nichochar/brightdata-cli) (`brightdata` or `bdata`) — a terminal tool for scraping, searching, structured data extraction, zone management, and budget monitoring.

### Quick start

```bash
# One-time login (auto-creates zones, saves API key)
brightdata login

# Scrape any URL as markdown
brightdata scrape https://example.com

# Search Google with structured results
brightdata search "web scraping best practices"

# Extract LinkedIn profile data
brightdata pipelines linkedin_person_profile "https://linkedin.com/in/username"

# Check account balance
brightdata budget
```

### Key commands

| Command | Purpose |
|---------|---------|
| `brightdata scrape <url>` | Scrape any URL as markdown, HTML, JSON, or screenshot |
| `brightdata search "<query>"` | Search Google/Bing/Yandex with structured results |
| `brightdata pipelines <type> [params]` | Extract structured data from 40+ platforms |
| `brightdata status <job-id>` | Check async job status |
| `brightdata zones` | List proxy zones |
| `brightdata budget` | View account balance and costs |
| `brightdata skill add` | Install AI agent skills |
| `brightdata config` | View/set configuration |

### Pipe-friendly

```bash
# Search → extract first URL → scrape it
brightdata search "top open source projects" --json \
  | jq -r '.organic[0].link' \
  | xargs brightdata scrape

# Amazon product data to CSV
brightdata pipelines amazon_product "https://amazon.com/dp/xxx" --format csv > product.csv
```

### Reference files

- [skills/brightdata-cli/SKILL.md](skills/brightdata-cli/SKILL.md) — Main skill with command overview and usage patterns
- [skills/brightdata-cli/references/commands.md](skills/brightdata-cli/references/commands.md) — Full command reference with all flags and options
- [skills/brightdata-cli/references/pipelines.md](skills/brightdata-cli/references/pipelines.md) — 40+ pipeline types with platform-specific parameters

---

## Best Practices Skill

The `bright-data-best-practices` skill is a **reference knowledge base** that Claude consults automatically when writing or reviewing Bright Data code. It is not a slash command — it works silently in the background.

### What it covers

| API | Key topics |
|-----|-----------|
| **Web Unlocker** | All request parameters, special headers (`x-unblock-expect`, `x-unblock-data-format`), async flow, billing model, anti-patterns |
| **SERP API** | All Google params (Search, Maps, Trends, Reviews, Lens, Hotels, Flights), Bing params, `brd_json=1` parsed output, async with `x-response-id` |
| **Web Scraper API** | Sync `/scrape` vs async `/trigger`, progress polling, status values, snapshot lifecycle, output formats |
| **Browser API** | Connection strings by framework, session rules, all custom CDP functions (`Captcha.solve`, `Proxy.setLocation`, `Emulation.setDevice`, etc.), bandwidth optimization |

### How it works

The skill has `user-invocable: false` — it never appears in the `/` command menu. Instead, Claude loads its reference material when you ask it to write Bright Data integrations, ensuring generated code uses correct endpoints, real parameter names, and proper patterns.

### Reference files

- [skills/bright-data-best-practices/references/web-unlocker.md](skills/bright-data-best-practices/references/web-unlocker.md)
- [skills/bright-data-best-practices/references/serp-api.md](skills/bright-data-best-practices/references/serp-api.md)
- [skills/bright-data-best-practices/references/web-scraper-api.md](skills/bright-data-best-practices/references/web-scraper-api.md)
- [skills/bright-data-best-practices/references/browser-api.md](skills/bright-data-best-practices/references/browser-api.md)

---

## Python SDK Best Practices Skill

The `python-sdk-best-practices` skill is a comprehensive guide for writing correct code with the `brightdata-sdk` Python package. Claude consults this automatically when writing, modifying, or reviewing Python code that uses the Bright Data SDK.

### What it covers

| Topic | Details |
|-------|---------|
| **Client setup** | Async (`BrightDataClient`) and sync (`SyncBrightDataClient`) clients, context managers, authentication |
| **Platform scrapers** | Amazon, LinkedIn, Instagram, Facebook, YouTube, ChatGPT, TikTok, Reddit — URL-based and keyword search |
| **SERP API** | Google, Bing, Yandex search with location, language, device, and async mode |
| **Datasets API** | 175+ pre-collected datasets with filter, download, sample, and export |
| **Scraper Studio** | Custom scraper execution with trigger/poll/fetch lifecycle |
| **Browser API** | CDP WebSocket URLs for Playwright/Puppeteer automation |
| **Error handling** | Full exception hierarchy with `APIError.status_code`, `APIError.response_text` |
| **Batch operations** | Concurrent scraping with `asyncio.gather()` |
| **Common mistakes** | Forgetting context managers, sync in async, missing `await`, hardcoded tokens |

### Reference files

- [skills/python-sdk-best-practices/SKILL.md](skills/python-sdk-best-practices/SKILL.md) — Core patterns and best practices
- [skills/python-sdk-best-practices/references/api-reference.md](skills/python-sdk-best-practices/references/api-reference.md) — Full API surface, service hierarchy, payload models, constants

---

## Setup

### Prerequisites

| Dependency | Version | Description |
|------------|---------|-------------|
| `curl` | ≥ 7.0 | HTTP client for API requests |
| `jq` | ≥ 1.5 | JSON processor for parsing responses |

**Install on Ubuntu/Debian:**
```bash
sudo apt-get install curl jq
```

**Install on macOS:**
```bash
brew install curl jq
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BRIGHTDATA_API_KEY` | Yes | Your Bright Data API key from the [dashboard](https://brightdata.com/cp) |
| `BRIGHTDATA_UNLOCKER_ZONE` | Yes* | Name of your Web Unlocker zone (*required for search/scrape) |
| `BRIGHTDATA_POLLING_TIMEOUT` | No | Max seconds to wait for data-feeds (default: 600) |

---

## Usage

### Search Skill

Search Google and receive structured JSON results.

```bash
bash skills/search/scripts/search.sh "query" [page]
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | - | Search query string |
| `page` | No | `0` | Page number (0-indexed) for pagination |

**Output Format:**
```json
{
  "organic": [
    {
      "link": "https://example.com/result",
      "title": "Result Title",
      "description": "Brief description of the page..."
    }
  ]
}
```

### Scrape Skill

Scrape any webpage and get clean markdown content.

```bash
bash skills/scrape/scripts/scrape.sh "url"
```

**Features:**
- Automatic bot detection bypass
- CAPTCHA solving
- JavaScript rendering
- Clean markdown output

### Data Feeds Skill

Extract structured data from 40+ supported websites.

```bash
bash skills/data-feeds/scripts/datasets.sh <dataset_type> <url> [params...]
```

Run without arguments to see all available datasets:
```bash
bash skills/data-feeds/scripts/datasets.sh
```

---

## Data Feeds

### E-Commerce

| Dataset | Command | Description |
|---------|---------|-------------|
| Amazon Product | `datasets.sh amazon_product <url>` | Product details, pricing, ratings |
| Amazon Reviews | `datasets.sh amazon_product_reviews <url>` | Customer reviews |
| Amazon Search | `datasets.sh amazon_product_search <keyword> <domain>` | Search results |
| Walmart Product | `datasets.sh walmart_product <url>` | Product details |
| eBay Product | `datasets.sh ebay_product <url>` | Listing details |
| Best Buy | `datasets.sh bestbuy_products <url>` | Product info |
| Etsy | `datasets.sh etsy_products <url>` | Listing data |
| Home Depot | `datasets.sh homedepot_products <url>` | Product data |
| Zara | `datasets.sh zara_products <url>` | Product details |

### Professional Networks

| Dataset | Command | Description |
|---------|---------|-------------|
| LinkedIn Person | `datasets.sh linkedin_person_profile <url>` | Profile, experience, skills |
| LinkedIn Company | `datasets.sh linkedin_company_profile <url>` | Company page data |
| LinkedIn Jobs | `datasets.sh linkedin_job_listings <url>` | Job posting details |
| LinkedIn Posts | `datasets.sh linkedin_posts <url>` | Post content |
| Crunchbase | `datasets.sh crunchbase_company <url>` | Funding, employees |
| ZoomInfo | `datasets.sh zoominfo_company_profile <url>` | Company profile |

### Social Media

| Dataset | Command | Description |
|---------|---------|-------------|
| Instagram Profiles | `datasets.sh instagram_profiles <url>` | Bio, followers |
| Instagram Posts | `datasets.sh instagram_posts <url>` | Post details |
| Instagram Reels | `datasets.sh instagram_reels <url>` | Reel metrics |
| TikTok Profiles | `datasets.sh tiktok_profiles <url>` | Creator data |
| TikTok Posts | `datasets.sh tiktok_posts <url>` | Video details |
| TikTok Shop | `datasets.sh tiktok_shop <url>` | Product data |
| Facebook Posts | `datasets.sh facebook_posts <url>` | Post content |
| Facebook Marketplace | `datasets.sh facebook_marketplace_listings <url>` | Listings |
| X (Twitter) | `datasets.sh x_posts <url>` | Tweet data |
| YouTube Profiles | `datasets.sh youtube_profiles <url>` | Channel data |
| YouTube Videos | `datasets.sh youtube_videos <url>` | Video details |
| YouTube Comments | `datasets.sh youtube_comments <url> [num]` | Comments |
| Reddit Posts | `datasets.sh reddit_posts <url>` | Post data |

### Other

| Dataset | Command | Description |
|---------|---------|-------------|
| Google Maps Reviews | `datasets.sh google_maps_reviews <url> [days]` | Business reviews |
| Google Shopping | `datasets.sh google_shopping <url>` | Product comparison |
| Google Play Store | `datasets.sh google_play_store <url>` | App details |
| Apple App Store | `datasets.sh apple_app_store <url>` | iOS app data |
| Yahoo Finance | `datasets.sh yahoo_finance_business <url>` | Stock data |
| Zillow | `datasets.sh zillow_properties_listing <url>` | Property listings |
| Booking.com | `datasets.sh booking_hotel_listings <url>` | Hotel data |
| Reuters News | `datasets.sh reuter_news <url>` | Article content |
| GitHub | `datasets.sh github_repository_file <url>` | Repository file |

---

## Examples

### Research Task
```bash
# Search for recent news
bash skills/search/scripts/search.sh "climate change 2024"

# Get full article content
bash skills/scrape/scripts/scrape.sh "https://example.com/climate-article"
```

### Competitive Analysis
```bash
# With the competitive-intel skill, just ask Claude:
# "Analyze Notion as a competitor" or "Compare pricing between Slack and Teams"
# Claude will automatically run the right bdata commands:

# Search for competitor info
bdata search "Notion project management" --json

# Scrape competitor pricing page
bdata scrape https://www.notion.com/pricing

# Get company data from Crunchbase
bdata pipelines crunchbase_company "https://www.crunchbase.com/organization/notion-so"

# Get LinkedIn company profile
bdata pipelines linkedin_company_profile "https://www.linkedin.com/company/notionhq"
```

### Social Media Monitoring
```bash
# Get Instagram profile
bash skills/data-feeds/scripts/datasets.sh instagram_profiles "https://instagram.com/natgeo"

# Get YouTube video stats
bash skills/data-feeds/scripts/datasets.sh youtube_videos "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

### Lead Generation
```bash
# Get LinkedIn profile
bash skills/data-feeds/scripts/datasets.sh linkedin_person_profile "https://linkedin.com/in/satyanadella"

# Get company funding data
bash skills/data-feeds/scripts/datasets.sh crunchbase_company "https://crunchbase.com/organization/openai"
```

---

## Project Structure

```
brightdata-plugin/
├── .claude-plugin/
│   ├── plugin.json              # Plugin configuration
│   └── marketplace.json         # Marketplace metadata
├── skills/
│   ├── search/
│   │   ├── SKILL.md             # Search skill
│   │   └── scripts/
│   │       └── search.sh        # Google search implementation
│   ├── scrape/
│   │   ├── SKILL.md             # Scrape skill
│   │   └── scripts/
│   │       └── scrape.sh        # Web scraper implementation
│   ├── data-feeds/
│   │   ├── SKILL.md             # Data feeds skill
│   │   └── scripts/
│   │       ├── datasets.sh      # Dataset wrapper (40+ sources)
│   │       └── fetch.sh         # Core polling logic
│   ├── bright-data-mcp/
│   │   ├── SKILL.md             # MCP workflow guide
│   │   └── references/
│   │       ├── mcp-tools.md     # Complete MCP tool reference (60+ tools)
│   │       └── mcp-setup.md     # MCP server setup guide
│   ├── bright-data-best-practices/
│   │   ├── SKILL.md             # API best practices (user-invocable: false)
│   │   └── references/
│   │       ├── web-unlocker.md  # Web Unlocker API deep reference
│   │       ├── serp-api.md      # SERP API deep reference
│   │       ├── web-scraper-api.md  # Web Scraper API deep reference
│   │       └── browser-api.md   # Browser API deep reference
│   ├── python-sdk-best-practices/
│   │   ├── SKILL.md             # Python SDK patterns and best practices
│   │   └── references/
│   │       └── api-reference.md # Full API surface, payloads, constants
│   ├── scraper-builder/
│   │   ├── SKILL.md             # Scraper builder workflow and decision tree
│   │   └── references/
│   │       ├── supported-domains.md   # Pre-built scraper lookup + API
│   │       ├── site-analysis-guide.md # HTML analysis playbook
│   │       └── pagination-patterns.md # 7 pagination strategies
│   ├── brightdata-cli/
│   │   ├── SKILL.md             # CLI usage guide and command patterns
│   │   └── references/
│   │       ├── commands.md      # Full command reference with all flags
│   │       └── pipelines.md     # 40+ pipeline types and parameters
│   ├── competitive-intel/
│   │   ├── SKILL.md             # Competitive intelligence (6 analysis modules)
│   │   └── references/
│   │       ├── data-source-guide.md    # CI needs → bdata command mapping
│   │       ├── output-templates.md     # 8 report templates
│   │       ├── analysis-frameworks.md  # SWOT, Porter's, positioning, JTBD, Blue Ocean
│   │       └── industry-signals.md     # Signal interpretation guide
│   └── design-mirror/
│       └── SKILL.md             # Design system mirroring skill
├── sdk-python/                  # Bright Data Python SDK source
├── README.md
└── LICENSE
```

---

## API Reference

### Search & Scrape (Web Unlocker API)

```
POST https://api.brightdata.com/request
Authorization: Bearer <BRIGHTDATA_API_KEY>
Content-Type: application/json

{
  "url": "<target_url>",
  "zone": "<BRIGHTDATA_UNLOCKER_ZONE>",
  "format": "raw",
  "data_format": "markdown" | "parsed_light"
}
```

### Data Feeds (Web Data API)

```
POST https://api.brightdata.com/datasets/v3/trigger?dataset_id=<id>
Authorization: Bearer <BRIGHTDATA_API_KEY>
Content-Type: application/json

[{"url": "<target_url>"}]
```

Then poll for results:
```
GET https://api.brightdata.com/datasets/v3/snapshot/<snapshot_id>?format=json
```

---

## Troubleshooting

### "BRIGHTDATA_API_KEY is not set"
```bash
export BRIGHTDATA_API_KEY="your-api-key"
```

### "BRIGHTDATA_UNLOCKER_ZONE is not set"
Create a Web Unlocker zone in your [dashboard](https://brightdata.com/cp):
```bash
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

### Data feeds timing out
Increase the polling timeout:
```bash
export BRIGHTDATA_POLLING_TIMEOUT=900
```

### Empty or malformed results
- Verify your API key is valid
- Check that your zone is active
- Ensure `jq` is installed

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Links

- [Bright Data](https://brightdata.com) - Official website
- [Documentation](https://docs.brightdata.com) - API documentation
- [Dashboard](https://brightdata.com/cp) - Manage your account
- [Web Unlocker](https://brightdata.com/products/web-unlocker) - Learn about Web Unlocker
- [SERP API](https://brightdata.com/products/serp-api) - Learn about SERP API
- [Web Data APIs](https://brightdata.com/products/web-scraper) - Learn about Web Data APIs
- [MCP Server](https://docs.brightdata.com) - MCP server documentation
- [MCP Tools Reference](skills/bright-data-mcp/references/mcp-tools.md) - Complete tool reference
- [Web Unlocker Best Practices](skills/bright-data-best-practices/references/web-unlocker.md) - Parameters, headers, async, billing
- [SERP API Best Practices](skills/bright-data-best-practices/references/serp-api.md) - All query params, parsed JSON, async
- [Web Scraper API Best Practices](skills/bright-data-best-practices/references/web-scraper-api.md) - Sync/async, polling, formats
- [Browser API Best Practices](skills/bright-data-best-practices/references/browser-api.md) - CDP functions, geo, bandwidth
- [Python SDK Best Practices](skills/python-sdk-best-practices/SKILL.md) - Async/sync clients, scrapers, SERP, datasets
- [Python SDK API Reference](skills/python-sdk-best-practices/references/api-reference.md) - Full API surface, payloads, constants
- [Scraper Builder](skills/scraper-builder/SKILL.md) - Build scrapers for any site with guided API selection
- [Supported Domains](skills/scraper-builder/references/supported-domains.md) - 100+ pre-built scrapers lookup
- [Bright Data CLI](skills/brightdata-cli/SKILL.md) - Terminal tool for scraping, search, and data extraction
- [CLI Commands Reference](skills/brightdata-cli/references/commands.md) - Full command reference with all flags
- [CLI Pipelines Reference](skills/brightdata-cli/references/pipelines.md) - 40+ platform pipeline types
- [Competitive Intelligence](skills/competitive-intel/SKILL.md) - Real-time competitor analysis with live web data
- [CI Data Source Guide](skills/competitive-intel/references/data-source-guide.md) - CI needs mapped to bdata commands
- [CI Analysis Frameworks](skills/competitive-intel/references/analysis-frameworks.md) - SWOT, Porter's, positioning, JTBD, Blue Ocean
- [CI Output Templates](skills/competitive-intel/references/output-templates.md) - 8 report templates
- [CI Industry Signals](skills/competitive-intel/references/industry-signals.md) - Signal interpretation guide

---

<p align="center">
  <sub>Built with the power of <a href="https://brightdata.com">Bright Data</a></sub>
</p>
