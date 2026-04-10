---
name: nimble-extract-reference
description: |
  Reference for nimble extract command. Load when fetching URLs or scraping pages.
  Contains: render tiers 1-3, all flags, browser actions, network capture,
  parser schemas, geo targeting, async, parallelization.
---

# nimble extract — reference

Fetches a URL and returns its content. The workhorse command — use for any URL where no agent exists.

## Table of Contents

- [Parameters](#parameters)
- [Drivers](#drivers)
- [CLI](#cli)
- [Python SDK](#python-sdk)
- [Render tiers — escalate on failure](#render-tiers--escalate-on-failure)
- [Browser actions](#browser-actions)
- [Network capture](#network-capture)
- [Parser schemas — structured extraction](#parser-schemas--structured-extraction)
- [Geo targeting](#geo-targeting)
- [Async extract](#async-extract)
- [Batch extract](#batch-extract)
- [Parallelization](#parallelization)
- [Response](#response)

---

## Parameters

| Parameter         | CLI flag            | Type   | Default | Description                                                                 |
| ----------------- | ------------------- | ------ | ------- | --------------------------------------------------------------------------- |
| `url`             | `--url`             | string | —       | Target URL (**required**)                                                   |
| `render`          | `--render`          | bool   | false   | Enable headless browser (JS rendering)                                      |
| `driver`          | `--driver`          | string | `vx6`   | Engine: `vx6` · `vx8` · `vx8-pro` · `vx10` · `vx10-pro` — see Drivers table |
| `formats`         | `--format`          | array  | `["html"]` | Output format(s): `"html"`, `"markdown"`. CLI: string (`--format markdown`). SDK: array (`formats=["markdown"]`). |
| `parse`           | `--parse`           | bool   | false   | Enable parser (use with `parser`)                                           |
| `parser`          | `--parser`          | JSON   | —       | Extraction schema — see [parsing-schema.md](parsing-schema.md)              |
| `browser_actions` | `--browser-action`  | JSON   | —       | Browser actions sequence — see [browser-actions.md](browser-actions.md)     |
| `network_capture` | `--network-capture` | JSON   | —       | XHR intercept rules — see [network-capture.md](network-capture.md)          |
| `is_xhr`          | `--is-xhr`          | bool   | false   | Direct API call — no browser, no render                                     |
| `country`         | `--country`         | string | —       | ISO Alpha-2 geo proxy (e.g. `US`, `GB`)                                     |
| `state`           | `--state`           | string | —       | State-level geo targeting                                                   |
| `city`            | `--city`            | string | —       | City-level geo targeting                                                    |
| `locale`          | `--locale`          | string | —       | LCID locale (e.g. `en-US`, `fr-FR`) — pair with `country`                   |
| `method`          | `--method`          | string | `GET`   | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`                        |
| `tag`             | `--tag`             | string | —       | Request tag for analytics                                                   |

---

## Drivers

| Driver     | Description       | Render | Best for                       |
| ---------- | ----------------- | ------ | ------------------------------ |
| `vx6`      | Fast HTTP (no JS) | No     | Static HTML, APIs, high volume |
| `vx8`      | Headless browser  | Yes    | Dynamic sites, SPAs            |
| `vx8-pro`  | Headful browser   | Yes    | Complex interactions           |
| `vx10`     | Stealth headless  | Yes    | Bot-protected sites            |
| `vx10-pro` | Stealth headful   | Yes    | Most protected sites           |

---

## CLI

```bash
# Markdown output (default for most tasks)
nimble --transform "data.markdown" extract \
  --url "https://example.com/page" --format markdown

# Save to file
nimble --transform "data.markdown" extract \
  --url "https://example.com/page" --format markdown > .nimble/page.md
```

## Python SDK

```python
from nimble_python import Nimble

nimble = Nimble()
resp = nimble.extract(url="https://example.com/page", formats=["markdown"])
print(resp["data"]["markdown"])
```

---

## Render tiers — escalate on failure

**Failure signals:** status 500 · empty `data.html` / `data.markdown` · "captcha" / "verify you are human" in content · login wall instead of target page

| Tier | CLI                                                                   | When                                            |
| ---- | --------------------------------------------------------------------- | ----------------------------------------------- |
| 1    | `extract --url "..."`                                                 | Static pages, docs, news, GitHub, Wikipedia, HN |
| 2    | `extract --url "..." --render`                                        | SPAs, dynamic content, JS-rendered pages        |
| 2b   | `--render --render-options '{"render_type":"idle2","timeout":60000}'` | Slow SPAs, wait for network idle                |
| 3    | `--render --driver vx10-pro`                                          | E-commerce, social, job boards — max stealth    |

```bash
# Tier 1 — no render
nimble --transform "data.markdown" extract --url "https://example.com" --format markdown

# Tier 2 — render
nimble --transform "data.markdown" extract --url "https://example.com" --render --format markdown

# Tier 3 — stealth
nimble --transform "data.markdown" extract --url "https://example.com" --render --driver vx10-pro --format markdown
```

```python
# Tier 2 — render
resp = nimble.extract(url="https://example.com", render=True, formats=["markdown"])

# Tier 3 — stealth
resp = nimble.extract(url="https://example.com", render=True, driver="vx10-pro", formats=["markdown"])
```

---

## Browser actions

For interacting with a page before extracting — clicks, scrolls, form fills, infinite scroll. Requires `render=True`.

See [browser-actions.md](browser-actions.md) for all action types and params.

```bash
nimble --transform "data.markdown" extract \
  --url "https://example.com/product" --render \
  --browser-action '[
    {"type": "click", "selector": ".tab-reviews", "required": false},
    {"type": "wait_for_element", "selector": ".review-list"}
  ]' --format markdown
```

```python
resp = nimble.extract(
    url="https://example.com/product",
    render=True,
    browser_actions=[
        {"type": "click", "selector": ".tab-reviews", "required": False},
        {"type": "wait_for_element", "selector": ".review-list"},
    ],
    formats=["markdown"],
)
```

---

## Network capture

When page data comes from XHR/AJAX calls, or to call a known API endpoint directly with `--is-xhr`.

See [network-capture.md](network-capture.md) for filter syntax and `--is-xhr` mode.

```bash
# Intercept an API call triggered by the page
nimble extract \
  --url "https://example.com/products" --render \
  --network-capture '[{"url": {"type": "contains", "value": "/api/products"}, "resource_type": ["xhr", "fetch"]}]' \
  > .nimble/products-api.json

# Known public API endpoint — use --is-xhr (no browser, fastest)
nimble --transform "data.markdown" extract \
  --url "https://api.example.com/v1/markets?q=elections&limit=50" \
  --is-xhr --format markdown
```

```python
# Intercept via render
resp = nimble.extract(
    url="https://example.com/products",
    render=True,
    network_capture=[{"url": {"type": "contains", "value": "/api/products"}, "resource_type": ["xhr", "fetch"]}],
)
captures = resp["data"]["network_capture"]

# Direct API call — no browser
resp = nimble.extract(
    url="https://api.example.com/v1/markets?q=elections&limit=50",
    is_xhr=True,
)
```

> **Note:** `is_xhr` and `render` are mutually exclusive.

---

## Parser schemas — structured extraction

When markdown doesn't contain fields cleanly. Results land in `data.parsing`.

See [parsing-schema.md](parsing-schema.md) for selector types, extractors, and post-processors.

```bash
nimble extract --url "https://example.com/product" --render --parse \
  --parser '{
    "type": "schema",
    "fields": {
      "title": {"type": "terminal", "selector": {"type": "css", "css_selector": "h1"}, "extractor": {"type": "text"}},
      "price": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-price]"}, "extractor": {"type": "text"}}
    }
  }'
```

```python
resp = nimble.extract(
    url="https://example.com/product",
    render=True,
    parse=True,
    parser={
        "type": "schema",
        "fields": {
            "title": {"type": "terminal", "selector": {"type": "css", "css_selector": "h1"}, "extractor": {"type": "text"}},
            "price": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-price]"}, "extractor": {"type": "text"}},
        },
    },
)
print(resp["data"]["parsing"])
```

---

## Geo targeting

```bash
# Country
nimble --transform "data.markdown" extract --url "https://example.com" --country US --format markdown

# City-level
nimble --transform "data.markdown" extract --url "https://example.com" --country US --state CA --city los_angeles --format markdown

# Localized (pair --locale with --country)
nimble --transform "data.markdown" extract --url "https://example.com/fr" --country FR --locale fr-FR --format markdown
```

```python
resp = nimble.extract(url="https://example.com", country="US", formats=["markdown"])

resp = nimble.extract(url="https://example.com", country="US", state="CA", city="los_angeles", formats=["markdown"])
```

---

## Async extract

For batch processing or long-running extractions. Returns immediately with a task ID; poll for results.

**Additional async-only params:**

| Parameter      | CLI flag         | Type   | Description                               |
| -------------- | ---------------- | ------ | ----------------------------------------- |
| `storage_type` | `--storage-type` | string | Cloud provider: `s3` or `gs`              |
| `storage_url`  | `--storage-url`  | string | Destination (e.g. `s3://my-bucket/path/`) |
| `compress`     | `--compress`     | bool   | GZIP compress results before storing      |
| `custom_name`  | `--custom-name`  | string | Custom filename (default: task ID)        |
| `callback_url` | `--callback-url` | string | Webhook URL — called on completion        |

**Task states:** `pending` → `running` → `success` / `failed`

```bash
# Submit async
nimble extract-async --url "https://example.com/page" --render --format markdown

# Poll status
nimble tasks get --task-id <task_id>

# Fetch results
nimble tasks results --task-id <task_id>
```

```python
import asyncio
from nimble_python import AsyncNimble

async def extract():
    nimble = AsyncNimble()
    task = await nimble.extract_async(url="https://example.com/page", render=True, formats=["markdown"])
    task_id = task["task"]["id"]
    while True:
        status = await nimble.tasks.get(task_id=task_id)
        state = status["task"]["state"]
        if state in ("success", "failed"):
            break
        await asyncio.sleep(5)
    result = await nimble.tasks.results(task_id=task_id)
    print(result["data"]["markdown"])

asyncio.run(extract())
```

---

## Batch extract

Submit up to 1,000 URLs in a single request. Uses an `inputs` + `shared_inputs` pattern
— shared config applies to all items, per-item values override.

**Parameters:**

| Parameter       | CLI flag          | Type  | Default  | Description                                                     |
| --------------- | ----------------- | ----- | -------- | --------------------------------------------------------------- |
| `inputs`        | `--input`         | array | required | Array of per-URL requests, each with at least `url`             |
| `shared_inputs` | `--shared-inputs` | JSON  | —        | Defaults applied to all items (render, format, driver, delivery)|

**`shared_inputs` fields:**

- **Extraction defaults** (overridable per item): `render`, `driver`, `formats`, `country`, `locale`, `parse`, `parser`
- **Delivery params** (batch-wide, not overridable): `storage_type`, `storage_url`, `storage_compress`, `storage_object_name`, `callback_url`

**CLI:**

```bash
nimble extract-batch \
  --shared-inputs 'render: true' --shared-inputs 'format: markdown' \
  --input '{"url": "https://example.com/page-1"}' \
  --input '{"url": "https://example.com/page-2"}' \
  --input '{"url": "https://example.com/page-3"}'
```

**Python SDK:**

```python
resp = nimble.extract_batch(
    inputs=[
        {"url": "https://example.com/page-1"},
        {"url": "https://example.com/page-2"},
        {"url": "https://example.com/page-3"},
    ],
    shared_inputs={"render": True, "formats": ["markdown"]},
)
batch_id = resp["batch_id"]
```

**Node SDK:**

```javascript
const resp = await nimble.extractBatch({
  inputs: [
    { url: "https://example.com/page-1" },
    { url: "https://example.com/page-2" },
    { url: "https://example.com/page-3" },
  ],
  sharedInputs: { render: true, formats: ["markdown"] },
});
const batchId = resp.batch_id;
```

**Response:**

```json
{
  "batch_id": "b7e1a2f3-...",
  "batch_size": 3,
  "tasks": [
    { "id": "task-001-uuid", "state": "pending", "batch_id": "b7e1a2f3-..." }
  ]
}
```

**Polling:** Use `nimble batches progress --batch-id <batch_id>` to check completion,
then `nimble batches get --batch-id <batch_id>` to get all task IDs, then
`nimble tasks results --task-id <id>` for each successful task.
See `nimble-tasks` reference for the full polling flow.

**Delivery options:**
- **Polling** — check status with batch/task IDs (default)
- **Webhooks** — pass `callback_url` in `shared_inputs`; Nimble POSTs on completion
- **Cloud storage** — set `storage_type` + `storage_url` in `shared_inputs`

---

## Parallelization

```bash
mkdir -p .nimble
nimble --transform "data.markdown" extract --url "https://example.com/1" --format markdown > .nimble/1.md &
nimble --transform "data.markdown" extract --url "https://example.com/2" --format markdown > .nimble/2.md &
nimble --transform "data.markdown" extract --url "https://example.com/3" --format markdown > .nimble/3.md &
wait
```

---

## Response

| Field                     | Type   | Description                                          |
| ------------------------- | ------ | ---------------------------------------------------- |
| `data.html`               | string | Extracted HTML content                               |
| `data.markdown`           | string | Content as markdown (if `format=markdown`)           |
| `data.parsing`            | object | Structured data (if `parse=True`)                    |
| `data.network_capture`    | array  | Captured network requests (if `network_capture` set) |
| `status_code`             | number | HTTP status code from target                         |
| `task_id`                 | string | Unique request identifier                            |
| `metadata.driver`         | string | Driver used (e.g. `vx6`, `vx10-pro`)                 |
| `metadata.query_duration` | number | Extraction time in ms                                |
