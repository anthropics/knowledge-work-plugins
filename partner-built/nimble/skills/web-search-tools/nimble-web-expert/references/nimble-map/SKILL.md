---
name: nimble-map-reference
description: |
  Reference for nimble map command. Load when discovering URLs on a site before bulk extraction.
  Contains: all flags (limit 1-100000, sitemap include/only/skip, domain_filter),
  response structure {links[].url/title/description}, map→filter→extract pattern, map vs crawl comparison.
---

# nimble map — reference

Discovers all URLs on a site in seconds. Returns URL metadata (url, title, description) — run `extract` on results to get page content. Single synchronous call — no polling required.

## Table of Contents

- [Parameters](#parameters)
- [CLI](#cli)
- [Python SDK](#python-sdk)
- [Response](#response)
- [Common patterns](#common-patterns)
- [Map vs Crawl](#map-vs-crawl)

---

## Parameters

| Parameter       | CLI flag          | Type   | Default   | Description                                                                          |
| --------------- | ----------------- | ------ | --------- | ------------------------------------------------------------------------------------ |
| `url`           | `--url`           | string | required  | Starting URL                                                                         |
| `limit`         | `--limit`         | int    | `100`     | Max URLs returned (1–100,000)                                                        |
| `sitemap`       | `--sitemap`       | string | `include` | `include` (sitemap + crawl) \| `only` (sitemap only, fastest) \| `skip` (crawl only) |
| `domain_filter` | `--domain-filter` | string | —         | `domain` (exact) \| `subdomain` (include subdomains) \| `all` (follow all links)     |
| `country`       | `--country`       | string | `ALL`     | ISO Alpha-2 proxy location (e.g. `US`)                                               |
| `locale`        | `--locale`        | string | —         | LCID locale (e.g. `en-US`) or `auto`                                                 |

## CLI

```bash
nimble map --url "https://docs.example.com" --limit 100

# Sitemap only (fastest)
nimble map --url "https://example.com" --sitemap only --limit 500

# Extract just the URL list
nimble --transform "links.#.url" map --url "https://docs.example.com" --limit 100
```

## Python SDK

```python
from nimble_python import Nimble
nimble = Nimble(api_key=os.environ["NIMBLE_API_KEY"])

resp = nimble.map(url="https://docs.example.com", limit=100, sitemap="include")
links = resp.links  # list of link objects
urls = [l.url for l in links]
```

## Response

| Field                 | Type    | Description                          |
| --------------------- | ------- | ------------------------------------ |
| `task_id`             | string  | Request identifier                   |
| `success`             | boolean | Whether the request succeeded        |
| `links`               | array   | Discovered URLs                      |
| `links[].url`         | string  | The discovered URL                   |
| `links[].title`       | string  | Page title (if available)            |
| `links[].description` | string  | Page meta description (if available) |

---

## Common patterns

```bash
# Map → filter → extract
nimble --transform "links.#.url" map --url "https://docs.stripe.com" --limit 200 > .nimble/urls.txt
grep "charges\|refund" .nimble/urls.txt

# Specific path section
nimble map --url "https://shop.example.com/products/" --limit 200
```

---

## Map vs Crawl

|          | `map`                                       | `crawl`                   |
| -------- | ------------------------------------------- | ------------------------- |
| Speed    | Seconds (sync)                              | Minutes (async)           |
| Output   | URL list with metadata                      | Full page content per URL |
| Best for | Discover URLs, then selectively extract     | Archive all pages at once |
| LLM use  | ✅ Combine with `extract --format markdown` | ⚠️ Returns raw HTML       |
