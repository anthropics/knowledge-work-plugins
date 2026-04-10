---
name: nimble-crawl-reference
description: |
  Reference for nimble crawl command. Load when bulk-crawling many pages asynchronously.
  Contains: async workflow (create → status → tasks results), all flags, polling guidelines,
  CRITICAL: use task_id (not crawl_id) for results, crawl vs map comparison.
---

# nimble crawl — reference

Async bulk crawling — starts a crawl job, returns a `crawl_id`, then you poll for status and retrieve per-page content via individual `task_id`s.

> **Tip:** For LLM use, prefer `nimble map` + `nimble extract --format markdown` (faster, cleaner). Use crawl when you need raw HTML archives of many pages at once.

## Table of Contents

- [1. Create crawl (async)](#1-create-crawl-async)
- [2. Get crawl status](#2-get-crawl-status)
- [3. List crawls](#3-list-crawls)
- [4. Cancel crawl](#4-cancel-crawl)
- [Polling guidelines](#polling-guidelines)
- [Retrieving page content](#retrieving-page-content)
- [Crawl vs Map](#crawl-vs-map)

---

## 1. Create crawl (async)

**Parameters:**

| Parameter                 | CLI flag                    | Type     | Default   | Description                                  |
| ------------------------- | --------------------------- | -------- | --------- | -------------------------------------------- |
| `url`                     | `--url`                     | string   | required  | Starting URL                                 |
| `limit`                   | `--limit`                   | int      | `5000`    | Max pages (1–10,000) — always set this       |
| `name`                    | `--name`                    | string   | —         | Label for tracking                           |
| `sitemap`                 | `--sitemap`                 | string   | `include` | `include` \| `only` \| `skip`                |
| `include_path`            | `--include-path`            | string[] | —         | URL path regex to include (repeatable)       |
| `exclude_path`            | `--exclude-path`            | string[] | —         | URL path regex to exclude (repeatable)       |
| `max_discovery_depth`     | `--max-discovery-depth`     | int      | `5`       | Max link depth from start (1–20)             |
| `crawl_entire_domain`     | `--crawl-entire-domain`     | bool     | `false`   | Follow sibling/parent paths                  |
| `allow_subdomains`        | `--allow-subdomains`        | bool     | `false`   | Follow links to subdomains                   |
| `allow_external_links`    | `--allow-external-links`    | bool     | `false`   | Follow links to external domains             |
| `ignore_query_parameters` | `--ignore-query-parameters` | bool     | `false`   | Deduplicate query-param variants             |
| `callback`                | `--callback`                | string   | —         | Webhook URL for real-time page notifications |
| `extract_options`         | `--extract-options`         | object   | —         | Extraction config applied to each page       |

**CLI:**

```bash
nimble crawl run --url "https://docs.example.com" --limit 50 --name "docs-crawl"
```

**Python SDK:**

```python
from nimble_python import Nimble
nimble = Nimble(api_key=os.environ["NIMBLE_API_KEY"])

resp = nimble.crawl.run(url="https://docs.example.com", limit=50, name="docs-crawl")
crawl_id = resp.crawl_id
```

**Response fields:** `crawl_id`, `status` (initial: `queued`), `url`, `name`, `crawl_options`, `created_at`

**Crawl status values:** `queued` → `running` → `succeeded` / `failed` / `canceled`

---

## 2. Get crawl status

**Parameters:**

| Parameter | CLI flag | Type   | Description           |
| --------- | -------- | ------ | --------------------- |
| `id`      | `--id`   | string | `crawl_id` (required) |

**CLI:**

```bash
nimble crawl status --id "abc-123"
```

**Python SDK:**

```python
crawl = nimble.crawl.status(id=crawl_id)
print(crawl.status, crawl.completed, crawl.total)
```

**Response adds:** `total`, `pending`, `completed`, `failed`, `tasks[]`

| Field             | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `tasks[].task_id` | Use with `nimble tasks results` to fetch page content |
| `tasks[].status`  | `pending` / `processing` / `completed` / `failed`     |

> **CRITICAL:** Use `tasks[].task_id` — NOT `crawl_id` — to fetch page content. Using `crawl_id` with tasks returns 404.

---

## 3. List crawls

**Parameters:**

| Parameter | CLI flag   | Type   | Description                                                            |
| --------- | ---------- | ------ | ---------------------------------------------------------------------- |
| `status`  | `--status` | string | Filter: `queued` \| `running` \| `completed` \| `failed` \| `canceled` |
| `limit`   | `--limit`  | int    | Results per page                                                       |
| `cursor`  | `--cursor` | string | Pagination cursor                                                      |

**CLI:**

```bash
nimble crawl list --status running
```

**Python SDK:**

```python
result = nimble.crawl.list()
# result.data = list of crawl objects
# result.pagination = { has_next, next_cursor, total }
```

---

## 4. Cancel crawl

**Parameters:**

| Parameter | CLI flag | Type   | Description           |
| --------- | -------- | ------ | --------------------- |
| `id`      | `--id`   | string | `crawl_id` (required) |

**CLI:**

```bash
nimble crawl terminate --id "abc-123"
```

**Python SDK:**

```python
nimble.crawl.terminate(id=crawl_id)
# Returns: {"status": "canceled"}
```

---

## Polling guidelines

```bash
CRAWL_ID=$(nimble crawl run --url "https://example.com" --limit 100 --name "my-crawl" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['crawl_id'])")

while true; do
  STATUS=$(nimble crawl status --id "$CRAWL_ID" \
    | python3 -c "import json,sys; print(json.load(sys.stdin).get('status',''))")
  echo "Status: $STATUS"
  [ "$STATUS" = "succeeded" ] || [ "$STATUS" = "failed" ] || [ "$STATUS" = "canceled" ] && break
  sleep 30
done
```

| Crawl size   | Poll interval |
| ------------ | ------------- |
| < 50 pages   | every 15–30s  |
| 50–500 pages | every 30–60s  |
| 500+ pages   | every 60–120s |

---

## Retrieving page content

After crawl `succeeded`, fetch each completed task — see `nimble-tasks` reference:

```bash
nimble tasks results --task-id "task-456"
```

---

## Crawl vs Map

|          | `map`                                       | `crawl`                   |
| -------- | ------------------------------------------- | ------------------------- |
| Speed    | Seconds (sync)                              | Minutes (async)           |
| Output   | URL list with metadata                      | Full page content per URL |
| Best for | Discover URLs, then selectively extract     | Archive all pages at once |
| LLM use  | ✅ Combine with `extract --format markdown` | ⚠️ Returns raw HTML       |
