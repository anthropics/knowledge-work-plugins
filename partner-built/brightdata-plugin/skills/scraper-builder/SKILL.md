---
name: scraper-builder
description: "Build production-ready web scrapers for any website using Bright Data infrastructure. Guides you through site analysis, API selection, selector extraction, pagination handling, and complete scraper implementation. Use this skill whenever the user wants to build a scraper, create a crawler, extract data from a website, scrape product pages, handle pagination, build a data pipeline from a web source, or automate data collection from any site — even if they don't explicitly say 'scraper'. Triggers on phrases like 'build a scraper for', 'scrape data from', 'extract products from', 'crawl pages on', 'get data from [website]', or 'I need to pull data from'."
---

# Scraper Builder

You are building a production-ready web scraper for the user. Your job is to guide them from "I want data from site X" to a working, robust scraper that handles real-world challenges like pagination, dynamic content, anti-bot protection, and data parsing.

## Critical: Always Validate Your Output

After building the scraper, **always run it** on a small sample (1-3 pages) and show the extracted data to the user before scaling up. If the output is empty, malformed, or missing fields, iterate — fix selectors, switch APIs, or adjust the parsing logic. A scraper that doesn't produce clean data is not done.

Take your time with the reconnaissance phase. Spending 2 minutes analyzing the HTML upfront prevents hours of debugging later. Quality is more important than speed here.

## How This Skill Works

This skill orchestrates Bright Data's four APIs to build scrapers intelligently. Rather than writing fragile custom scraping code, you analyze the target site first, then pick the most reliable and cost-effective extraction method. The decision tree is:

1. **Does a pre-built scraper already exist?** → Use Web Scraper API (zero parsing code needed)
2. **Is the page static / no interaction needed?** → Use Web Unlocker API (cheapest, simplest)
3. **Does the page need clicks, scrolls, or JS interaction?** → Use Browser API (full automation)
4. **Need search engine results?** → Use SERP API

The skill produces complete, runnable code — not pseudocode or outlines.

---

## Phase 1: Understand the Target

Before writing any code, you need to understand what the user wants and what the site looks like. Ask these questions (skip any the user already answered):

1. **What site?** — The target URL or domain
2. **What data?** — Which fields they need (product names, prices, reviews, etc.)
3. **What scope?** — Single page, category pages, search results, entire site section?
4. **Pagination?** — Do they need to scrape across multiple pages?
5. **Volume?** — Roughly how many items/pages? (affects sync vs async choice and concurrency strategy — see [references/concurrency-guide.md](references/concurrency-guide.md))
6. **Output format?** — JSON, CSV, database? (default to JSON if unspecified)
7. **Language preference?** — Python or Node.js? (default to Python if unspecified)

Don't over-interview. If the user says "build a scraper for Amazon product pages", you already know: site=Amazon, data=product details, scope=product pages. Jump ahead.

---

## Phase 2: Check for Pre-Built Scrapers

Before doing any custom work, check if Bright Data already has a scraper for this domain. This is the fastest, cheapest, and most reliable path.

Read [references/supported-domains.md](references/supported-domains.md) for the curated list of common pre-built scrapers. But the curated list may not be complete — Bright Data supports 100+ domains and adds new scrapers regularly. If you don't see the target domain in the curated list, **query the live Dataset List API** to check:

```bash
curl -H "Authorization: Bearer $BRIGHTDATA_API_KEY" \
     https://api.brightdata.com/datasets/list
```

This returns every available scraper with its `dataset_id` and name. Search the results for the target domain. You can also browse the full documentation index at `https://docs.brightdata.com/llms.txt` to discover scraper-specific docs and supported parameters.

### If a pre-built scraper exists

Use the Web Scraper API or Python SDK platform-specific scrapers. This gives you structured JSON with no parsing code needed.

**Python SDK approach (preferred):**
```python
from brightdata import BrightDataClient

async with BrightDataClient() as client:
    result = await client.scrape.amazon.products(url="https://amazon.com/dp/B0CRMZHDG8")
    if result.success:
        print(result.data)  # Structured product data
```

**REST API approach (shell/curl):**
```bash
bash scripts/datasets.sh amazon_product "https://www.amazon.com/dp/B09V3KXJPB"
```

For bulk scraping with pre-built scrapers, use the async trigger/poll/fetch pattern:
```python
async with BrightDataClient() as client:
    # Trigger without waiting
    job = await client.scrape.amazon.products_trigger(url=url)
    # Poll until ready
    await job.wait(timeout=180, poll_interval=10, verbose=True)
    # Fetch results
    data = await job.fetch()
```

Skip to Phase 5 (pagination/orchestration) if the user needs multi-page scraping with a pre-built scraper.

### If no pre-built scraper exists

Continue to Phase 3 — you need to analyze the site and build a custom scraper.

---

## Phase 3: Site Reconnaissance

This is the critical step that separates reliable scrapers from brittle ones. You need to understand the site's structure before writing extraction code.

### Step 3a: Fetch the page HTML

Use Web Unlocker to get the raw HTML. This tells you whether the content is server-rendered or client-rendered, and gives you the actual DOM to analyze.

```python
import requests
import os

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]

response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "zone": ZONE,
        "url": "https://target-site.com/page",
        "format": "raw"
    }
)
html = response.text
```

Or use the scrape skill's shell script:
```bash
bash skills/scrape/scripts/scrape.sh "https://target-site.com/page"
```

### Step 3b: Analyze the HTML structure

Read [references/site-analysis-guide.md](references/site-analysis-guide.md) for the detailed analysis playbook.

Look at the fetched HTML and determine:

1. **Is the content in the HTML?** If the data you need is present in the raw HTML, Web Unlocker is sufficient. If the HTML is mostly empty shells with JS framework markers (`<div id="root"></div>`, `<div id="__next"></div>`, `ng-app`), the content is client-rendered and you need Browser API.

2. **Identify reliable selectors.** Find the CSS selectors or data attributes that target the data fields. Prefer selectors in this order (most reliable → least):
   - `data-*` attributes (e.g., `[data-testid="product-price"]`) — survive redesigns
   - Semantic HTML with specific classes (e.g., `.product-card .price`)
   - `id` attributes — unique but may change
   - Structural selectors (e.g., `div > span:nth-child(2)`) — fragile, avoid

3. **Identify the data pattern.** Is it:
   - **List page** — multiple items in a repeating structure (product grid, search results)
   - **Detail page** — single item with many fields (product page, profile)
   - **Paginated** — multiple pages of results with next/prev controls
   - **Infinite scroll** — content loads on scroll (needs Browser API)
   - **API-backed** — check the Network tab pattern; some sites fetch data from JSON APIs

4. **Check for hidden APIs.** Many modern sites load data via XHR/fetch calls to internal APIs. If you see structured JSON endpoints in the page source or network activity, hitting those directly through Web Unlocker is often cleaner than parsing HTML.

### Step 3c: Decide the extraction approach

Based on your analysis:

| Finding | Approach |
|---------|----------|
| Content in HTML, no interaction needed | **Web Unlocker** — fetch HTML, parse with BeautifulSoup/Cheerio |
| Content loaded via JSON API | **Web Unlocker** — hit the API endpoint directly |
| Content requires JS rendering | **Browser API** — render then extract |
| Content needs click/scroll/interaction | **Browser API** — automate the interaction |
| Infinite scroll pagination | **Browser API** — scroll and collect |
| Standard URL-based pagination | **Web Unlocker** — iterate page URLs |
| CAPTCHA-heavy site | **Browser API** — auto-solves CAPTCHAs |

---

## Phase 4: Build the Extractor

Now write the actual extraction code. The approach depends on Phase 3's decision.

### Approach A: Web Unlocker + HTML Parsing

Best for static sites or sites with server-rendered HTML. This is the cheapest and fastest approach.

```python
import requests
import os
from bs4 import BeautifulSoup

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]

def fetch_page(url: str) -> str:
    """Fetch a page through Bright Data Web Unlocker."""
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"zone": ZONE, "url": url, "format": "raw"}
    )
    response.raise_for_status()
    return response.text

def parse_products(html: str) -> list[dict]:
    """Extract product data from HTML. Customize selectors per site."""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for card in soup.select(".product-card"):  # Adjust selector
        product = {
            "name": card.select_one(".product-title").get_text(strip=True),
            "price": card.select_one(".product-price").get_text(strip=True),
            "url": card.select_one("a")["href"],
            # Add more fields as needed
        }
        products.append(product)

    return products

# Usage
html = fetch_page("https://example.com/products")
products = parse_products(html)
```

**Key patterns for robust parsing:**
- Always use `.get_text(strip=True)` to clean whitespace
- Use `.get("href", "")` instead of `["href"]` to avoid KeyError on missing attributes
- Wrap individual field extraction in try/except so one bad item doesn't kill the whole scrape
- Normalize prices (strip currency symbols, convert to float) in a separate step

### Approach B: Web Unlocker + Direct API Extraction

When you discover the site loads data from a JSON API endpoint, hit it directly. This is the cleanest approach — no HTML parsing needed.

```python
import requests
import json
import os

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]

def fetch_api(api_url: str) -> dict:
    """Fetch a JSON API endpoint through Web Unlocker."""
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"zone": ZONE, "url": api_url, "format": "raw"}
    )
    return json.loads(response.text)

# Example: site with internal API
data = fetch_api("https://example.com/api/products?page=1&limit=50")
products = data["results"]  # Already structured!
```

### Approach C: Browser API + Playwright

Use when the site requires JavaScript rendering, interaction (clicks, scrolls, form fills), or has aggressive anti-bot measures.

```python
import asyncio
from playwright.async_api import async_playwright

AUTH = os.environ.get("BROWSER_AUTH", "brd-customer-CUSTOMER_ID-zone-ZONE_NAME:PASSWORD")

async def scrape_with_browser(url: str) -> str:
    """Scrape a page using Bright Data Browser API."""
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            f"wss://{AUTH}@brd.superproxy.io:9222"
        )
        page = await browser.new_page()
        page.set_default_navigation_timeout(120_000)  # 2 minutes — required

        # Block unnecessary resources to reduce bandwidth costs
        await page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}",
                         lambda route: route.abort())

        await page.goto(url, wait_until="domcontentloaded")

        # Wait for the content you need to appear
        await page.wait_for_selector(".product-card", timeout=30_000)

        # Extract data using page.evaluate for performance
        products = await page.evaluate("""
            () => Array.from(document.querySelectorAll('.product-card')).map(card => ({
                name: card.querySelector('.product-title')?.textContent?.trim(),
                price: card.querySelector('.product-price')?.textContent?.trim(),
                url: card.querySelector('a')?.href,
            }))
        """)

        await browser.close()
        return products
```

**Browser API rules you must follow:**
- Always set navigation timeout to 120 seconds (`set_default_navigation_timeout(120_000)`)
- One `page.goto()` per session — for a new URL, create a new browser connection
- Use `wait_until="domcontentloaded"` not `networkidle` (SPAs never reach networkidle)
- Wait for specific selectors rather than arbitrary delays
- Block images, CSS, fonts to reduce bandwidth costs
- Use `page.evaluate()` for bulk extraction — it's faster than individual selector calls

### Approach D: Browser API for Infinite Scroll

For sites that load more content when you scroll down.

```python
async def scrape_infinite_scroll(url: str, max_items: int = 100) -> list:
    """Scrape a page with infinite scroll."""
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            f"wss://{AUTH}@brd.superproxy.io:9222"
        )
        page = await browser.new_page()
        page.set_default_navigation_timeout(120_000)
        await page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}",
                         lambda route: route.abort())
        await page.goto(url, wait_until="domcontentloaded")

        all_items = []
        previous_count = 0

        while len(all_items) < max_items:
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # Wait for content to load

            # Extract all currently visible items
            items = await page.evaluate("""
                () => Array.from(document.querySelectorAll('.item-selector')).map(el => ({
                    // ... extract fields
                }))
            """)

            all_items = items
            if len(all_items) == previous_count:
                break  # No new content loaded — we've reached the end
            previous_count = len(all_items)

        await browser.close()
        return all_items[:max_items]
```

---

## Phase 5: Handle Pagination

Most scraping tasks involve multiple pages. The approach depends on the pagination type.

Read [references/pagination-patterns.md](references/pagination-patterns.md) for detailed pagination strategies.

### Pattern 1: URL-Based Pagination (most common)

Pages are accessed via URL parameters like `?page=2` or `?offset=20`.

```python
import time

def scrape_all_pages(base_url: str, max_pages: int = 50) -> list[dict]:
    """Scrape all pages of a paginated listing."""
    all_items = []

    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?page={page_num}"
        html = fetch_page(url)
        items = parse_products(html)

        if not items:
            break  # No more results

        all_items.extend(items)
        print(f"Page {page_num}: {len(items)} items (total: {len(all_items)})")

        time.sleep(1)  # Be respectful — don't hammer the site

    return all_items
```

### Pattern 2: Next-Page Link Pagination

Follow "next" links found in the HTML.

```python
def scrape_with_next_links(start_url: str) -> list[dict]:
    """Follow next-page links to scrape all pages."""
    all_items = []
    url = start_url

    while url:
        html = fetch_page(url)
        items = parse_products(html)
        all_items.extend(items)

        # Find next page link
        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one("a.next-page, a[rel='next'], .pagination .next a")
        url = next_link["href"] if next_link else None

        # Handle relative URLs
        if url and not url.startswith("http"):
            from urllib.parse import urljoin
            url = urljoin(start_url, url)

        time.sleep(1)

    return all_items
```

### Pattern 3: Concurrent Bulk Scraping

When you have many URLs (50+), **always use concurrent requests with a semaphore** — never fetch them one-by-one in a sequential loop. Read [references/concurrency-guide.md](references/concurrency-guide.md) for the full concurrency playbook including per-site tuning, multi-site parallelism, and retry strategies.

```python
import asyncio
import aiohttp

CONCURRENCY = 20  # Start here, tune per site — see concurrency guide

async def scrape_pages_concurrent(urls: list[str]) -> list[dict]:
    """Scrape multiple pages with controlled concurrency."""
    sem = asyncio.Semaphore(CONCURRENCY)

    async def fetch_one(session, url):
        async with sem:
            async with session.post(
                "https://api.brightdata.com/request",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"zone": ZONE, "url": url, "format": "raw"},
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                return {"url": url, "html": await resp.text()}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items = []
    for r in results:
        if not isinstance(r, Exception):
            all_items.extend(parse_products(r["html"]))
    return all_items

# Generate all page URLs
urls = [f"https://example.com/products?page={i}" for i in range(1, 51)]
items = asyncio.run(scrape_pages_concurrent(urls))
```

### Pattern 4: Cursor/Token-Based Pagination (APIs)

Some APIs use cursor tokens instead of page numbers.

```python
def scrape_with_cursor(api_base: str) -> list[dict]:
    """Handle cursor-based API pagination."""
    all_items = []
    cursor = None

    while True:
        url = f"{api_base}?limit=100"
        if cursor:
            url += f"&cursor={cursor}"

        data = fetch_api(url)
        all_items.extend(data["results"])

        cursor = data.get("next_cursor")
        if not cursor:
            break

    return all_items
```

---

## Phase 6: Assemble the Complete Scraper

Now put it all together into a clean, runnable script. Every scraper you build should have:

1. **Configuration** — environment variables, target URLs, output settings
2. **Fetcher** — the function that retrieves pages (Web Unlocker or Browser API)
3. **Parser** — the function that extracts structured data from HTML/JSON
4. **Paginator** — the logic that handles multiple pages
5. **Concurrency** — parallel fetching with semaphore control (see [references/concurrency-guide.md](references/concurrency-guide.md))
6. **Output** — saving results to the requested format
7. **Error handling** — retries, logging, graceful failures

**Important:** If the user has more than ~50 URLs to scrape, the scraper **must** use concurrent requests — not a sequential loop. See [references/concurrency-guide.md](references/concurrency-guide.md) for the complete concurrent scraper template and tuning guidelines.

### Template: Complete Scraper Script

```python
#!/usr/bin/env python3
"""
Scraper for [SITE NAME] - [DESCRIPTION]
Built with Bright Data [API NAME]

Usage:
    export BRIGHTDATA_API_KEY="your-api-key"
    export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
    python scraper.py
"""

import json
import os
import sys
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- Configuration ---
API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]
TARGET_URL = "https://example.com/products"
OUTPUT_FILE = "results.json"
MAX_PAGES = 50

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

# --- Fetcher ---
def fetch_page(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = requests.post(
                "https://api.brightdata.com/request",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"zone": ZONE, "url": url, "format": "raw"},
                timeout=60,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            log.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts")

# --- Parser ---
def parse_items(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for card in soup.select("ITEM_SELECTOR"):
        try:
            item = {
                "name": card.select_one("NAME_SELECTOR").get_text(strip=True),
                "price": card.select_one("PRICE_SELECTOR").get_text(strip=True),
                "url": card.select_one("a").get("href", ""),
            }
            items.append(item)
        except (AttributeError, TypeError) as e:
            log.warning(f"Failed to parse item: {e}")
            continue

    return items

# --- Paginator ---
def scrape_all(base_url: str) -> list[dict]:
    all_items = []

    for page in range(1, MAX_PAGES + 1):
        url = f"{base_url}?page={page}"
        log.info(f"Scraping page {page}...")

        html = fetch_page(url)
        items = parse_items(html)

        if not items:
            log.info(f"No items on page {page} — stopping")
            break

        all_items.extend(items)
        log.info(f"Got {len(items)} items (total: {len(all_items)})")
        time.sleep(1)

    return all_items

# --- Output ---
def save_results(items: list[dict], path: str):
    with open(path, "w") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    log.info(f"Saved {len(items)} items to {path}")

# --- Main ---
if __name__ == "__main__":
    items = scrape_all(TARGET_URL)
    save_results(items, OUTPUT_FILE)
```

When building the scraper for the user, customize this template:
- Replace `ITEM_SELECTOR`, `NAME_SELECTOR`, `PRICE_SELECTOR` with real selectors from Phase 3
- Choose the right fetcher (Web Unlocker vs Browser API)
- Choose the right pagination pattern from Phase 5
- Add the specific fields the user needs
- Adjust the output format if they want CSV or database insertion

---

## Decision Reference: API Selection Quick Guide

| Scenario | API | Cost | Speed |
|----------|-----|------|-------|
| Site has pre-built scraper (Amazon, LinkedIn, etc.) | Web Scraper API | Per record | Fast |
| Static HTML pages, no JS needed | Web Unlocker | Per request (success only) | Fast |
| Site exposes JSON API | Web Unlocker → API endpoint | Per request (success only) | Fastest |
| JS-rendered content (React, Vue, Angular) | Browser API | Per bandwidth | Medium |
| Infinite scroll | Browser API | Per bandwidth | Slow |
| Form submission / login required | Browser API | Per bandwidth | Medium |
| CAPTCHA-heavy sites | Browser API | Per bandwidth | Medium |
| Search engine results | SERP API | Per request | Fast |

---

## Common Pitfalls to Avoid

1. **Don't default to Browser API when Web Unlocker suffices.** Browser API costs more (bandwidth-based) and is slower. Always try Web Unlocker first.

2. **Don't use structural CSS selectors** like `div:nth-child(3) > span`. They break when the site adds a banner or rearranges elements. Use data attributes or semantic selectors.

3. **Don't hardcode pagination limits.** Always check if the page returned actual items. An empty page means you've reached the end.

4. **Don't skip the reconnaissance phase.** Spending 2 minutes analyzing the HTML saves hours of debugging brittle selectors.

5. **Don't forget error handling per item.** One malformed product card shouldn't crash the entire scrape. Wrap individual item parsing in try/except.

6. **Don't use `networkidle` with Browser API.** SPAs never truly reach network idle. Use `domcontentloaded` + `wait_for_selector` instead.

7. **Don't create a new browser session per page when scraping a list.** If you're on a list page and clicking "next", you can stay in the same session. Only create new sessions for different base URLs.

8. **Don't scrape URLs sequentially when you have many of them.** Fetching 1,000+ URLs one-by-one with `time.sleep(1)` between each is unacceptably slow. Use concurrent requests with a semaphore. See [references/concurrency-guide.md](references/concurrency-guide.md).

---

## Examples

### Example 1: E-commerce product scraper (pre-built exists)

User says: "Build a scraper for Amazon product pages, I have a list of 200 ASINs"

Actions:
1. Check supported-domains.md → Amazon has pre-built scrapers
2. 200 URLs → use async trigger/poll/fetch (over 20 URL sync limit)
3. Use `client.scrape.amazon.products_trigger()` with batch of URLs
4. Poll until ready, download structured JSON
5. No HTML parsing needed — data comes pre-structured

Result: Complete Python script with async batch scraping, progress logging, JSON output.

### Example 2: Custom site scraper (no pre-built)

User says: "I need to scrape all job listings from jobs.customsite.com including pagination"

Actions:
1. Check supported-domains.md → not listed → query Dataset List API → not found
2. Fetch page HTML via Web Unlocker to analyze structure
3. Content is in the HTML (SSR) → Web Unlocker approach
4. Identify selectors: `.job-card`, `.job-title`, `.company-name`, `.salary`
5. Pagination via `?page=N` URL parameter
6. Build complete scraper with fetcher + parser + paginator

Result: Complete Python script using Web Unlocker + BeautifulSoup with URL-based pagination.

### Example 3: JS-heavy site (Browser API needed)

User says: "Scrape product prices from a React SPA that loads data on scroll"

Actions:
1. Fetch HTML via Web Unlocker → body is empty `div#root` → client-rendered
2. Check for hidden API in page source → no API found
3. Escalate to Browser API with Playwright
4. Implement infinite scroll pattern with resource blocking
5. Extract data via `page.evaluate()` after content loads

Result: Async Playwright script with Browser API, infinite scroll handling, bandwidth optimization.

---

## Troubleshooting

### Web Unlocker returns empty or blocked page
**Cause:** Site requires JavaScript rendering or has aggressive bot detection.
**Solution:** Escalate to Browser API. Also try adding `data_format: "markdown"` to see if the content is there but in a different format.

### Selectors work locally but fail in production
**Cause:** Site serves different HTML to different regions or user agents.
**Solution:** Add `country` parameter to Web Unlocker request to target the same region. Verify selectors on the actual HTML returned by the API, not browser DevTools.

### Scraper returns duplicate items across pages
**Cause:** Pagination logic is wrapping around or site uses inconsistent pagination.
**Solution:** Track seen item IDs in a set. Break when duplicates appear. Verify the pagination URL pattern is correct.

### Browser API session times out
**Cause:** Navigation timeout too short or site is slow to unblock.
**Solution:** Always set `set_default_navigation_timeout(120_000)`. Use `wait_until="domcontentloaded"` not `networkidle`. Check if the site requires premium domains enabled on your zone.

### API returns 401 Unauthorized
**Cause:** Missing or invalid `BRIGHTDATA_API_KEY` environment variable.
**Solution:** Verify the key is set: `echo $BRIGHTDATA_API_KEY`. Get a fresh key from `https://brightdata.com/cp/setting/users`.

---

## Reference Files

- **[references/supported-domains.md](references/supported-domains.md)** — Complete list of pre-built scrapers with dataset IDs and Python SDK methods. Check this FIRST before writing custom scraping code.
- **[references/site-analysis-guide.md](references/site-analysis-guide.md)** — Step-by-step playbook for analyzing a site's HTML structure and choosing reliable selectors.
- **[references/pagination-patterns.md](references/pagination-patterns.md)** — Detailed pagination strategies with code examples for every common pattern.
- **[references/concurrency-guide.md](references/concurrency-guide.md)** — How to scrape URLs concurrently with semaphore control, per-site tuning, multi-site parallelism, retries, and progress tracking. **Read this whenever the user has 50+ URLs to scrape.**
