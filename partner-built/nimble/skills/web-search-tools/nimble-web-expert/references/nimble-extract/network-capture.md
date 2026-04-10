---
name: nimble-network-capture-reference
description: |
  Reference for --network-capture flag. Load when page data comes from XHR or AJAX calls,
  or when you want to call a known API endpoint directly (--is-xhr).
  Contains: filter syntax (url contains/regex), resource_type, --is-xhr mode for direct API calls,
  capture+parse combined patterns. Note: --is-xhr and --render are mutually exclusive.
---

# Network Capture

Docs: https://docs.nimbleway.com/nimble-sdk/web-tools/extract/features/network-capture

Two modes for accessing API data:

1. **With rendering** (`--render`) — intercepts XHR/fetch calls the browser fires during page load. Use when data is lazy-loaded or triggered by interactions.
2. **Without rendering** (`--is-xhr`) — calls a known API endpoint directly, no browser. Use when you already know the API URL.

## Table of Contents

- [Mode 1 — Network capture with rendering](#mode-1--network-capture-with-rendering)
- [Mode 2 — XHR without rendering (--is-xhr)](#mode-2--xhr-without-rendering---is-xhr)
- [Why use API/network capture over HTML parsing](#why-use-apinetwork-capture-over-html-parsing)
- [Notes](#notes)

---

## Mode 1 — Network capture with rendering

Intercepts API calls fired by the browser during page load. Returns structured JSON directly — bypasses HTML parsing.

**Best for:** SPAs, lazy-loaded data, dynamic content loaded by the page's own JS.

### CLI flag

```bash
--network-capture '[{"url": {"type": "contains", "value": "/api/"}, ...}]'
```

Requires `--render`. Pass a JSON array of filter objects.

### Python SDK

```python
from nimble_python import Nimble

nimble = Nimble()
resp = nimble.extract(
    url="https://example.com/products",
    render=True,
    network_capture=[{"url": {"type": "contains", "value": "/api/products"}, "resource_type": ["xhr", "fetch"]}],
)
captures = resp["data"]["network_capture"]
# captures[0]["result"] → list of {request, response} objects
```

SDK: pass `network_capture` as a Python list of dicts — no JSON serialization needed.

### Filter parameters

| Param                             | Type     | Description                                                                 |
| --------------------------------- | -------- | --------------------------------------------------------------------------- |
| `url.type`                        | string   | `exact` (full URL match) or `contains` (pattern match)                      |
| `url.value`                       | string   | URL or pattern to match                                                     |
| `method`                          | string   | HTTP verb filter: `GET`, `POST`, `PUT`, `DELETE`                            |
| `resource_type`                   | string[] | Filter by type: `xhr`, `fetch`, `document`, `script`, `stylesheet`, `image` |
| `validation`                      | bool     | Verify response content is valid                                            |
| `wait_for_requests_count`         | int      | Wait for this many matching requests before returning (default: 0)          |
| `wait_for_requests_count_timeout` | int (s)  | Max wait time for request count (default: 10s)                              |

### Examples

```bash
# Capture a specific API endpoint by pattern
nimble extract --url "https://example.com/products" --render \
  --network-capture '[{"url": {"type": "contains", "value": "/api/products"}}]' \
   --format markdown

# Narrow to XHR/fetch only
nimble extract --url "https://example.com/products" --render \
  --network-capture '[{
    "url": {"type": "contains", "value": "/api/products"},
    "resource_type": ["xhr", "fetch"]
  }]'  --format markdown

# Capture exact endpoint
nimble extract --url "https://example.com/page" --render \
  --network-capture '[{"url": {"type": "exact", "value": "https://example.com/api/v2/listings"}}]' \
   --format markdown

# Wait for 3 matching requests (pagination / multiple chunks)
nimble extract --url "https://example.com/feed" --render \
  --network-capture '[{
    "url": {"type": "contains", "value": "/api/feed"},
    "wait_for_requests_count": 3,
    "wait_for_requests_count_timeout": 15
  }]'  --format markdown

# Capture multiple endpoints simultaneously
nimble extract --url "https://example.com/page" --render \
  --network-capture '[
    {"url": {"type": "contains", "value": "/api/listings"}},
    {"url": {"type": "contains", "value": "/api/prices"}}
  ]'  --format markdown

# Capture POST requests triggered by a form fill
nimble extract --url "https://example.com/search" --render \
  --browser-action '[
    {"type": "fill", "selector": "#q", "value": "laptop", "mode": "type"},
    {"type": "press", "key": "Enter"}
  ]' \
  --network-capture '[{"url": {"type": "contains", "value": "/api/search"}, "method": "POST"}]' \
   --format markdown
```

### Accessing network capture data in `--parser`

Use `root` selector + JSON path to extract fields from captured API responses:

```bash
nimble extract --url "https://example.com/products" --render \
  --network-capture '[{"url": {"type": "contains", "value": "/api/products"}}]' \
  --parse --parser '{
    "type": "terminal",
    "selector": {
      "type": "sequence",
      "sequence": [
        {"type": "root"},
        {"type": "json", "path": "network_capture[0].response_body.data.products"}
      ]
    },
    "extractor": {"type": "raw"}
  }'
```

---

## Mode 2 — XHR without rendering (`--is-xhr`)

Docs: https://docs.nimbleway.com/nimble-sdk/web-tools/extract/features/network-capture#xhr-without-rendering

Call a known public API endpoint directly — no browser, no page load, no rendering overhead. Sends XHR-specific headers and targets the API URL directly.

**Best for:** Public REST APIs where you already know the endpoint URL.

**Critical constraint: `--is-xhr` only works when `--render` is NOT set.** Never combine `--is-xhr` with `--render`.

### CLI syntax

```bash
# GET request to a public API
nimble extract --url "https://api.example.com/v1/markets?q=elections&limit=50" \
  --is-xhr  --format markdown

# POST request
nimble extract --url "https://api.example.com/v1/search" \
  --method POST --is-xhr \
  --headers "Content-Type=application/json" \
   --format markdown
```

### Python SDK

```python
# GET — direct API endpoint
resp = nimble.extract(
    url="https://api.example.com/v1/markets?q=elections&limit=50",
    is_xhr=True,
)
print(resp["data"]["html"])  # raw API response body

# POST
resp = nimble.extract(
    url="https://api.example.com/v1/search",
    method="POST",
    is_xhr=True,
)
```

### Examples

```bash
# Polymarket — search markets by keyword
nimble extract --url "https://gamma-api.polymarket.com/markets?_q=elections&limit=50&active=true" \
  --is-xhr  --format markdown

# Any public JSON API
nimble extract --url "https://api.example.com/products?category=laptops&limit=20" \
  --is-xhr  --format markdown

# API requiring a specific HTTP method
nimble extract --url "https://api.example.com/v2/search" \
  --method POST --is-xhr \
  --headers "Content-Type=application/json" \
   --format markdown
```

### When to prefer `--is-xhr` over `--network-capture`

| Scenario                                | Use                                                   |
| --------------------------------------- | ----------------------------------------------------- |
| You know the API endpoint URL           | `--is-xhr` (faster, no browser)                       |
| You need to discover the API URL first  | `--render` + `--network-capture`                      |
| Data only loads after page interactions | `--render` + `--browser-action` + `--network-capture` |
| Not sure — try API first                | `--is-xhr` → fallback to `--network-capture`          |

---

## Why use API/network capture over HTML parsing

- Returns clean JSON from the API — no brittle CSS selectors
- More reliable — API responses change less often than page layout
- Often contains more data than what's rendered in the DOM
- `--is-xhr` is faster and cheaper than rendering (no browser spun up)

---

## Notes

- `--is-xhr` requires `render` to be false — never combine with `--render`
- Always test with a small limit first to confirm the response structure before scaling
- Use `wait_for_requests_count` when the page fires the same endpoint multiple times (pagination, chunks)
- Combine `--network-capture` with `--browser-action` to trigger interactions before capturing calls
