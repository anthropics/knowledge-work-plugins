---
name: nimble-browser-actions-reference
description: |
  Reference for --browser-action flag. Load when you need to interact with a page before extracting —
  clicks, scrolls, form fills, infinite scroll, dropdown selection. Not just for escalation;
  use directly whenever the target data requires browser interaction.
  Contains: all action types (click, fill, scroll, auto_scroll, wait, wait_for_element, press, fetch), parameters, chaining examples.
  Note: fetch uses special syntax {"fetch": "url"} or {"fetch": {...}} — NOT {"type": "fetch"}.
---

# Browser Actions

Docs: https://docs.nimbleway.com/nimble-sdk/web-tools/extract/features/browser-actions

Programmatic browser control — click, scroll, fill forms, wait for elements. Use whenever the target data requires browser interaction before extraction.

Use cases include (but are not limited to):
- Scraping data that loads after a click (tabs, accordions, modals)
- Submitting a search or filter form
- Infinite scroll / "Load More" pagination
- Dismissing cookie banners or popups
- Selecting dropdowns to trigger price/variant updates

**Requires `--render`.**

All actions execute sequentially. Global timeout: 240 seconds.

## Table of Contents

- [CLI flag](#cli-flag)
- [Python SDK](#python-sdk)
- [All action types](#all-action-types)
- [fetch — HTTP request from browser context](#fetch--http-request-from-browser-context)
- [Examples](#examples)
- [Tips](#tips)

---

## CLI flag

```bash
--browser-action '[{"type": "...", ...}, {"type": "...", ...}]'
```

Pass a JSON array of action objects. Always combine with `--render`.

## Python SDK

```python
from nimble_python import Nimble

nimble = Nimble()
resp = nimble.extract(
    url="https://example.com/product",
    render=True,
    browser_actions=[
        {"type": "click", "selector": ".tab-reviews", "required": False},
        {"type": "wait_for_element", "selector": ".review-list"},
    ],
    formats=["markdown"],
)
print(resp["data"]["markdown"])
```

SDK: pass `browser_actions` as a Python list of dicts. Python booleans (`False`) are used instead of JSON `false`.

---

## All action types

| Type               | Key params                                               | Use for                           |
| ------------------ | -------------------------------------------------------- | --------------------------------- |
| `goto`             | `url`, `timeout`, `wait_until`, `referer`                | Navigate to a different URL       |
| `wait`             | `duration` ("1s", "500ms", "2000ms")                     | Pause between actions             |
| `wait_for_element` | `selector`, `timeout`, `visible`                         | Wait for DOM element to appear    |
| `click`            | `selector` OR `x`/`y`, `delay`, `count`, `scroll`        | Click buttons, tabs, links        |
| `press`            | `key` (Enter, Tab, Escape, Space, ArrowDown…)            | Keyboard interaction              |
| `fill`             | `selector`, `value`, `mode` (type/paste)                 | Type or paste into input field    |
| `scroll`           | `y` (px), `x` (px), `to` (CSS selector)                  | Scroll page or to element         |
| `auto_scroll`      | `max_duration` (s), `idle_timeout` (s), `click_selector` | Infinite scroll / lazy load       |
| `screenshot`       | `full_page`, `format`, `quality`                         | Capture page state for debugging  |
| `get_cookies`      | `domain` (optional filter)                               | Extract browser cookies           |
| `fetch`            | see below — **uses different syntax**                    | HTTP request from browser context (with page cookies/tokens) |

### `required` parameter

Add `"required": false` to any action to make it optional — the action chain continues even if the element is absent. Use for cookie banners, popups, optional UI elements.

---

## `fetch` — HTTP request from browser context

`fetch` makes an HTTP request from within the live browser session — cookies, CSRF tokens, and session headers from the page load are automatically included. Use it to replay API calls (form submissions, search requests, etc.) without needing to re-authenticate.

**`fetch` uses a different syntax from all other actions** — `"fetch"` is the key, not `"type"`:

```json
// Direct form — GET request
{"fetch": "https://api.example.com/data"}

// Extended form — custom method, headers, body
{
  "fetch": {
    "url": "https://api.example.com/submit",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": "{\"key\": \"value\"}",
    "timeout": 15000
  }
}
```

**Parameters (extended form):**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | required | URL to request |
| `method` | string | `GET` | HTTP method: `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| `headers` | object | — | Key-value HTTP headers |
| `body` | string | — | Request body (for POST/PUT/PATCH) |
| `timeout` | number | `15000` | Max wait time in milliseconds |

**Billing:** the first `fetch` action per request is free. Each additional `fetch` is billed as a VX6 request.

### CLI

```bash
# Direct form — GET from browser context
nimble extract --url "https://example.com" --render \
  --browser-action '[
    {"fetch": "https://api.example.com/data"}
  ]' --format markdown

# Extended form — POST with JSON body (replicate a form submission)
nimble extract --url "https://example.com/careers/apply" --render \
  --browser-action '[
    {"fetch": {
      "url": "https://api.example.com/v1/apply",
      "method": "POST",
      "headers": {"Content-Type": "application/json"},
      "body": "{\"job_id\": \"123\", \"name\": \"Jane Doe\", \"email\": \"jane@example.com\"}"
    }}
  ]' --format markdown
```

### Python SDK

```python
# Direct form — GET
resp = nimble.extract(
    url="https://example.com",
    render=True,
    browser_actions=[
        {"fetch": "https://api.example.com/data"},
    ],
)

# Extended form — POST with JSON body
import json
resp = nimble.extract(
    url="https://example.com/careers/apply",
    render=True,
    browser_actions=[
        {
            "fetch": {
                "url": "https://api.example.com/v1/apply",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"job_id": "123", "name": "Jane Doe", "email": "jane@example.com"}),
            }
        }
    ],
)
print(resp)
```

---

## Examples

### CLI

```bash
# Click a tab and wait for content
nimble extract --url "https://example.com/product" --render \
  --browser-action '[
    {"type": "click", "selector": ".tab-reviews"},
    {"type": "wait_for_element", "selector": ".review-list"}
  ]' --format markdown

# Dismiss optional cookie banner, then extract
nimble extract --url "https://example.com" --render \
  --browser-action '[
    {"type": "click", "selector": "#accept-cookies", "required": false},
    {"type": "wait", "duration": "500ms"}
  ]' --format markdown

# Fill search form and submit
nimble extract --url "https://example.com/search" --render \
  --browser-action '[
    {"type": "fill", "selector": "#search-input", "value": "running shoes", "mode": "type"},
    {"type": "press", "key": "Enter"},
    {"type": "wait_for_element", "selector": ".results"}
  ]' --format markdown

# Infinite scroll — load all lazy content
nimble extract --url "https://example.com/feed" --render \
  --browser-action '[
    {"type": "auto_scroll", "max_duration": 15, "idle_timeout": 3}
  ]' --format markdown

# Auto-scroll with "Load More" button
nimble extract --url "https://example.com/products" --render \
  --browser-action '[
    {"type": "auto_scroll", "click_selector": ".load-more-btn", "max_duration": 20, "idle_timeout": 5}
  ]' --format markdown

# Navigate to a tab URL, then extract
nimble extract --url "https://example.com" --render \
  --browser-action '[
    {"type": "goto", "url": "https://example.com/reviews"},
    {"type": "wait_for_element", "selector": ".review-item"}
  ]' --format markdown

# Scroll to specific element
nimble extract --url "https://example.com/page" --render \
  --browser-action '[
    {"type": "scroll", "to": ".pricing-section"},
    {"type": "wait", "duration": "1s"}
  ]' --format markdown

# Select dropdown then wait
nimble extract --url "https://example.com/product" --render \
  --browser-action '[
    {"type": "click", "selector": ".size-dropdown"},
    {"type": "click", "selector": "[data-value=\"XL\"]"},
    {"type": "wait_for_element", "selector": ".price-updated"}
  ]' --format markdown

# Take screenshot for debugging
nimble extract --url "https://example.com" --render \
  --browser-action '[
    {"type": "screenshot", "full_page": true}
  ]' --format screenshot
```

### Python SDK

```python
# Click a tab and wait for content
resp = nimble.extract(
    url="https://example.com/product",
    render=True,
    browser_actions=[
        {"type": "click", "selector": ".tab-reviews"},
        {"type": "wait_for_element", "selector": ".review-list"},
    ],
    formats=["markdown"],
)

# Fill search form and submit
resp = nimble.extract(
    url="https://example.com/search",
    render=True,
    browser_actions=[
        {"type": "fill", "selector": "#search-input", "value": "running shoes", "mode": "type"},
        {"type": "press", "key": "Enter"},
        {"type": "wait_for_element", "selector": ".results"},
    ],
    formats=["markdown"],
)

# Infinite scroll
resp = nimble.extract(
    url="https://example.com/feed",
    render=True,
    browser_actions=[
        {"type": "auto_scroll", "max_duration": 15, "idle_timeout": 3},
    ],
    formats=["markdown"],
)

# Dismiss optional cookie banner then extract
resp = nimble.extract(
    url="https://example.com",
    render=True,
    browser_actions=[
        {"type": "click", "selector": "#accept-cookies", "required": False},
        {"type": "wait", "duration": "500ms"},
    ],
    formats=["markdown"],
)
```

---

## Tips

- **`required: false`** — always use for cookie banners, popups, optional elements
- **`wait_for_element` over `wait`** — prefer waiting for a specific element to appear rather than a fixed duration
- **`auto_scroll` `idle_timeout: 3-5`** — right setting for most infinite scroll pages
- **`fill` `mode: "paste"`** — faster for large text blocks; `mode: "type"` simulates human typing
- **`click` `scroll: true`** — auto-scrolls element into viewport before clicking
- **`fetch` billing** — first fetch per request is free; each additional fetch billed as a VX6 request
- **`fetch` vs `--is-xhr`** — use `fetch` when you need page cookies/tokens; use `--is-xhr` for public APIs with no auth
- All actions run within 240s total — budget your timeouts accordingly
