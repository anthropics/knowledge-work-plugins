---
name: nimble-search-reference
description: |
  Reference for nimble search command. Load when searching the live web.
  Contains: all flags, 8 focus modes (general/coding/news/academic/shopping/social/geo/location),
  search_depth modes (lite/fast/deep), response structure, credit costs.
---

# nimble search — reference

Real-time web search with 8 focus modes. Returns results with titles, URLs, and optionally full content and AI answers.

## Table of Contents

- [Parameters](#parameters)
- [Search depth modes](#search-depth-modes)
- [Focus modes](#focus-modes)
- [CLI](#cli)
- [Python SDK](#python-sdk)
- [Response structure](#response-structure)

---

## Parameters

| Parameter                 | Type            | Default  | Description                                                                                                       |
| ------------------------- | --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `query`                   | string          | required | Search query                                                                                                      |
| `search_depth`            | string          | `deep`   | Content depth: `lite` \| `fast` \| `deep` — see depth table below                                                |
| `focus`                   | string or array | `general`| Focus mode (see table below) or array of specific agent names e.g. `["amazon_serp", "target_serp"]`               |
| `include_answer`          | bool            | `false`  | AI-synthesized answer (premium — retry without if 402/403)                                                        |
| `max_results`             | int             | `10`     | Result count (1–100)                                                                                              |
| `output_format`           | string          | —        | `plain_text` \| `markdown` \| `simplified_html`                                                                   |
| `include_domains`         | array           | —        | Restrict to these domains (max 50)                                                                                |
| `exclude_domains`         | array           | —        | Exclude these domains (max 50)                                                                                    |
| `time_range`              | string          | —        | `hour` \| `day` \| `week` \| `month` \| `year` — cannot combine with dates                                        |
| `start_date` / `end_date` | string          | —        | Date range `YYYY-MM-DD` — cannot combine with `time_range`                                                        |
| `content_type`            | string          | —        | File type filter: `pdf`, `docx`, `xlsx`, `documents`, `spreadsheets`, `presentations` — only with `general` focus |
| `max_subagents`           | int             | —        | Parallel agents for shopping/social/geo/location (1–5)                                                            |
| `country`                 | string          | —        | ISO Alpha-2 geo-targeted results (e.g. `US`)                                                                      |
| `locale`                  | string          | —        | Language code (e.g. `en`, `fr`, `de`)                                                                             |
| `deep_search`             | bool            | —        | **Deprecated** — use `search_depth` instead. `true` = `deep`, `false` = `lite`. Still works for backward compat. |

CLI uses hyphens (`--search-depth`, `--include-answer`). SDK uses underscores (`search_depth`, `include_answer`).

---

## Search depth modes

| Mode   | Content                          | Speed    | Best for                                                        |
| ------ | -------------------------------- | -------- | --------------------------------------------------------------- |
| `lite` | Metadata only (title, URL, snippet) | Fastest | High-volume pipelines, URL discovery, quick filtering           |
| `fast` | Rich cached content              | Fast     | AI agents, RAG, chatbots — quality content without scrape latency |
| `deep` | Full real-time page content      | Slowest  | Research, due diligence, tasks requiring complete source material |

**Default for AI agent use:** prefer `fast` — richest content-to-latency ratio.

---

## Focus modes

| Mode       | Best for                            | Example query                            |
| ---------- | ----------------------------------- | ---------------------------------------- |
| `general`  | Broad web (default)                 | "best practices for X"                   |
| `coding`   | Docs, code, Stack Overflow, GitHub  | "how to implement X in Python"           |
| `news`     | Current events, breaking news       | "EU AI Act enforcement 2026"             |
| `academic` | Research papers, scholarly articles | "transformer attention mechanisms paper" |
| `shopping` | Products, price comparisons         | "best wireless headphones under $200"    |
| `social`   | People, LinkedIn, X, YouTube        | "Jane Doe Head of Engineering"           |
| `geo`      | Geographic and regional data        | "tech companies in Berlin"               |
| `location` | Local businesses, restaurants       | "italian restaurants San Francisco"      |

---

## CLI

```bash
# Fast depth — rich content, low latency (best for agents)
nimble search --query "React server components" --search-depth fast

# Lite — metadata only, fastest
nimble search --query "OpenAI announcements" --focus news --search-depth lite

# Deep — full real-time page scrape
nimble search --query "EU AI Act" --focus news --search-depth deep \
  --start-date 2025-01-01 --end-date 2025-12-31

# With AI answer + domain filter
nimble search --query "Python asyncio best practices" \
  --focus coding --search-depth fast --include-answer \
  --include-domain '["docs.python.org", "realpython.com"]'

# Extract just URLs
nimble --transform "results.#.url" search --query "React tutorials" --search-depth lite
```

## Python SDK

```python
from nimble_python import Nimble
nimble = Nimble(api_key=os.environ["NIMBLE_API_KEY"])

# Fast depth — best default for AI agent use
resp = nimble.search(query="React server components", search_depth="fast")

# Lite — scan many results quickly
resp = nimble.search(
    query="OpenAI announcements",
    focus="news",
    search_depth="lite",
    time_range="week",
)

# Deep — full content for research
resp = nimble.search(
    query="EU AI Act enforcement",
    focus="news",
    search_depth="deep",
    include_answer=True,
)

# Custom focus — explicit agent array
resp = nimble.search(
    query="best wireless headphones",
    focus=["amazon_serp", "walmart_serp"],
    search_depth="fast",
    max_results=10,
)

results = resp.results       # list of result objects
answer = resp.answer         # AI summary (if include_answer=True)
```

---

## Response structure

| Field                            | Type   | Description                                                  |
| -------------------------------- | ------ | ------------------------------------------------------------ |
| `total_results`                  | int    | Total results returned                                       |
| `results`                        | array  | Search results                                               |
| `results[].title`                | string | Page title                                                   |
| `results[].description`          | string | Snippet                                                      |
| `results[].url`                  | string | Page URL                                                     |
| `results[].content`              | string | Page content — cached (`fast`) or real-time scraped (`deep`) |
| `results[].metadata.position`    | int    | Result rank                                                  |
| `results[].metadata.entity_type` | string | e.g. `OrganicResult`                                         |
| `answer`                         | string | AI summary (if `include_answer=True`)                        |
| `request_id`                     | UUID   | Request identifier                                           |
