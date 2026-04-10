---
name: nimble-browser-investigation-reference
description: |
  Reference for Tier 6 browser investigation. Load when Tiers 1-5 fail and selectors or XHR paths are unknown.
  Contains: browser-use vs Playwright comparison, CSS selector discovery scripts, XHR/API pattern discovery,
  when to escalate vs skip Tier 6.
---

# Browser investigation — reference (Tier 6)

Use when Tiers 1–5 fail and you don't know which CSS selectors to use or which XHR URL to intercept.
**Investigate once → build a precise nimble command → extract at scale.**

## Check available tools

```bash
which browser-use 2>/dev/null && echo "browser-use: installed" || echo "browser-use: not found"
python3 -c "from playwright.sync_api import sync_playwright; print('playwright: installed')" 2>/dev/null || echo "playwright: not found"
```

|          | browser-use                            | Playwright                                              |
| -------- | -------------------------------------- | ------------------------------------------------------- |
| Cost     | Paid (Nimble)                          | Free (open source)                                      |
| Style    | Agent-based — describe what to find    | Script-based — write what to run                        |
| Best for | Complex investigations, needs judgment | Simple selector/XHR discovery                           |
| Install  | `npm i -g @nimbleway/browser-use-cli`  | `pip install playwright && playwright install chromium` |

**Rule:** Use browser-use if installed. Fall back to Playwright if not.

---

## Finding CSS selectors

### With browser-use

```
[browser-use] Navigate to https://example.com/product
[browser-use] Take a screenshot to understand the layout
[browser-use] Inspect the price element → finds: <span data-price="49.99" class="price-now">
[browser-use] Inspect the product title → finds: <h1 class="product-title" data-testid="pdp-title">
```

### With Playwright

```python
# Save as .nimble/find-selectors.py → python3 .nimble/find-selectors.py
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com/product")
    page.wait_for_load_state("networkidle")
    for sel in ['[data-price]', '.price', '#price', '.product-price', '[data-testid*=price]']:
        els = page.query_selector_all(sel)
        if els:
            print(f"✓ '{sel}' → {len(els)} match(es), first text: '{els[0].inner_text()[:60]}'")
    for sel in ['h1', '[data-testid*=title]', '.product-title', '#product-title']:
        el = page.query_selector(sel)
        if el:
            print(f"✓ title '{sel}' → '{el.inner_text()[:80]}'")
    browser.close()
```

**Then build the nimble command:**

```bash
nimble extract --url "https://example.com/product" --render --parse \
  --parser '{
    "type": "schema",
    "fields": {
      "title": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-testid=pdp-title]"}, "extractor": {"type": "text"}},
      "price": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-price]"}, "extractor": {"type": "attr", "attr": "data-price"}}
    }
  }'
```

---

## Finding XHR/API patterns

### With browser-use

```
[browser-use] Navigate to https://example.com/search?q=shoes
[browser-use] Open DevTools Network tab, filter XHR/Fetch
[browser-use] Scroll to trigger data loading
              → GET /api/v2/search?q=shoes&page=1  →  JSON { "results": [...] }
```

### With Playwright

```python
# Save as .nimble/find-xhr.py → python3 .nimble/find-xhr.py
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    api_calls = []
    page.on("request", lambda req: api_calls.append(req) if req.resource_type in ("xhr", "fetch") else None)
    page.goto("https://example.com/search?q=shoes")
    page.wait_for_timeout(5000)
    for req in sorted(api_calls, key=lambda r: r.url):
        print(f"{req.method:6s}  {req.resource_type:5s}  {req.url[:120]}")
    browser.close()
```

**Then choose the nimble approach:**

```bash
# Option A — call the API directly (fastest, if no auth required)
nimble --transform "data.markdown" extract \
  --url "https://example.com/api/v2/search?q=shoes&page=1" \
  --is-xhr --format markdown

# Option B — trigger via browser and intercept (if session cookies required)
nimble extract \
  --url "https://example.com/search?q=shoes" --render \
  --network-capture '[{"url": {"type": "contains", "value": "/api/v2/search"}, "resource_type": ["xhr", "fetch"]}]' \
  > .nimble/search-results.json
```

---

## Finding browser actions (clicks, scrolls, waits)

### With browser-use

```
[browser-use] Navigate to https://example.com/product
[browser-use] Click "Reviews" tab → selector: button[data-tab="reviews"]
              After click: reviews appear in div.review-container
[browser-use] Scroll down to load more (lazy-loaded)
```

### With Playwright

```python
# Save as .nimble/find-actions.py → python3 .nimble/find-actions.py
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False to watch
    page = browser.new_page()
    page.goto("https://example.com/product")
    page.wait_for_load_state("networkidle")
    tabs = page.query_selector_all("button[data-tab], [role=tab], .tab-item")
    for tab in tabs:
        print(f"Tab: '{tab.inner_text()[:40]}'  data-tab={tab.get_attribute('data-tab')}")
    page.screenshot(path=".nimble/page-layout.png")
    browser.close()
```

**Then build the nimble browser actions:**

```bash
nimble --transform "data.markdown" extract \
  --url "https://example.com/product" --render \
  --browser-action '[
    {"type": "click", "selector": "button[data-tab=\"reviews\"]"},
    {"type": "wait_for_element", "selector": "div.review-container"},
    {"type": "auto_scroll", "max_duration": 10, "idle_timeout": 2}
  ]' --format markdown
```

---

## When to use Tier 6

**Go to Tier 6 when:**

- Tiers 1–5 failed and output is empty or irrelevant
- Data is dynamic but you don't know what interaction triggers it
- You need `--parser` schema or `--browser-action` for an unfamiliar site
- User asks "why isn't this working?" — investigate before retrying

**Skip Tier 6 when:**

- The site is in the proven recipes (Amazon, Yelp, etc.) — selectors are known
- `--render` or `--driver vx10-pro` already returns the content
- XHR pattern is obvious from URL structure (documented public API)
