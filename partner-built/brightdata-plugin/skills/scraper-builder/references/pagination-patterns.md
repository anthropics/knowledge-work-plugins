# Pagination Patterns

Complete reference for handling every common pagination pattern when building scrapers with Bright Data.

---

## Table of Contents

- [Pattern 1: URL Parameter Pagination](#pattern-1-url-parameter-pagination)
- [Pattern 2: Next-Link Pagination](#pattern-2-next-link-pagination)
- [Pattern 3: Offset-Based Pagination](#pattern-3-offset-based-pagination)
- [Pattern 4: Cursor/Token Pagination](#pattern-4-cursortoken-pagination)
- [Pattern 5: Infinite Scroll](#pattern-5-infinite-scroll)
- [Pattern 6: Load More Button](#pattern-6-load-more-button)
- [Pattern 7: Category/Sitemap Crawling](#pattern-7-categorysitemap-crawling)
- [Async Bulk Pagination](#async-bulk-pagination)
- [Rate Limiting and Politeness](#rate-limiting-and-politeness)
- [Detecting End of Results](#detecting-end-of-results)

---

## Pattern 1: URL Parameter Pagination

The most common pattern. Pages are accessed via a parameter like `?page=2`.

### Basic Implementation

```python
import time
import requests
import os

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]

def fetch_page(url: str) -> str:
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"zone": ZONE, "url": url, "format": "raw"},
        timeout=60,
    )
    response.raise_for_status()
    return response.text

def scrape_paginated(base_url: str, param: str = "page", start: int = 1, max_pages: int = 100) -> list:
    """
    Scrape pages where pagination is controlled by a URL parameter.

    Args:
        base_url: The URL without pagination parameter (e.g., "https://site.com/products")
        param: The pagination parameter name (e.g., "page", "p", "pg")
        start: Starting page number (usually 1, sometimes 0)
        max_pages: Safety limit to prevent infinite loops
    """
    all_items = []
    separator = "&" if "?" in base_url else "?"

    for page_num in range(start, start + max_pages):
        url = f"{base_url}{separator}{param}={page_num}"
        html = fetch_page(url)
        items = parse_items(html)  # Your parsing function

        if not items:
            break

        all_items.extend(items)
        time.sleep(1)

    return all_items
```

### Common URL Patterns

| Site Pattern | URL Format | Parameter |
|-------------|-----------|-----------|
| `?page=2` | Most common | `page` |
| `?p=2` | Shortened | `p` |
| `?pg=2` | Alternate | `pg` |
| `/page/2` | Path-based | Build URL differently |
| `?page=2&sort=price` | With other params | Preserve existing params |

### Path-Based Pagination

Some sites use `/page/2/` instead of `?page=2`:

```python
def scrape_path_paginated(base_url: str, max_pages: int = 100) -> list:
    all_items = []

    for page_num in range(1, max_pages + 1):
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url.rstrip('/')}/page/{page_num}/"

        html = fetch_page(url)
        items = parse_items(html)

        if not items:
            break

        all_items.extend(items)
        time.sleep(1)

    return all_items
```

---

## Pattern 2: Next-Link Pagination

Follow "next page" links found in the HTML. Useful when page numbers aren't predictable or URLs are complex.

```python
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_with_next_links(start_url: str, max_pages: int = 100) -> list:
    all_items = []
    url = start_url
    pages_scraped = 0

    while url and pages_scraped < max_pages:
        html = fetch_page(url)
        items = parse_items(html)
        all_items.extend(items)
        pages_scraped += 1

        # Find the next page link — try multiple common selectors
        soup = BeautifulSoup(html, "html.parser")
        next_link = (
            soup.select_one('a[rel="next"]') or
            soup.select_one('.pagination .next a') or
            soup.select_one('a.next-page') or
            soup.select_one('li.next a') or
            soup.select_one('[aria-label="Next page"]') or
            soup.select_one('[aria-label="Next"]')
        )

        if next_link and next_link.get("href"):
            url = urljoin(url, next_link["href"])
        else:
            url = None

        time.sleep(1)

    return all_items
```

---

## Pattern 3: Offset-Based Pagination

Instead of page numbers, the API uses an offset (how many items to skip).

```python
def scrape_offset_based(base_url: str, limit: int = 20, max_items: int = 1000) -> list:
    """
    Scrape with offset-based pagination.
    Common URL pattern: ?offset=0&limit=20, ?offset=20&limit=20, etc.
    """
    all_items = []
    offset = 0

    while offset < max_items:
        separator = "&" if "?" in base_url else "?"
        url = f"{base_url}{separator}offset={offset}&limit={limit}"

        html_or_json = fetch_page(url)
        items = parse_items(html_or_json)

        if not items:
            break

        all_items.extend(items)
        offset += limit
        time.sleep(1)

    return all_items
```

---

## Pattern 4: Cursor/Token Pagination

APIs that return a `next_cursor` or `next_token` for fetching the next batch. Common in modern REST and GraphQL APIs.

```python
import json

def scrape_cursor_based(api_url: str, limit: int = 100) -> list:
    """
    Scrape API with cursor-based pagination.
    Each response includes a cursor for the next page.
    """
    all_items = []
    cursor = None

    while True:
        url = f"{api_url}?limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"

        raw = fetch_page(url)
        data = json.loads(raw)

        items = data.get("results", data.get("data", data.get("items", [])))
        if not items:
            break

        all_items.extend(items)

        # Look for next cursor in common locations
        cursor = (
            data.get("next_cursor") or
            data.get("cursor") or
            data.get("pagination", {}).get("next_cursor") or
            data.get("meta", {}).get("next_cursor")
        )

        if not cursor:
            break

        time.sleep(1)

    return all_items
```

---

## Pattern 5: Infinite Scroll

Content loads when the user scrolls to the bottom. Requires Browser API.

```python
import asyncio
from playwright.async_api import async_playwright

AUTH = os.environ.get("BROWSER_AUTH")

async def scrape_infinite_scroll(
    url: str,
    item_selector: str,
    max_items: int = 500,
    scroll_pause: float = 2.0,
    max_scroll_attempts: int = 20,
) -> list:
    """
    Scrape a page with infinite scroll.

    Args:
        url: The page URL
        item_selector: CSS selector for individual items
        max_items: Stop after this many items
        scroll_pause: Seconds to wait after each scroll for content to load
        max_scroll_attempts: Stop if no new content after this many scrolls
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            f"wss://{AUTH}@brd.superproxy.io:9222"
        )
        page = await browser.new_page()
        page.set_default_navigation_timeout(120_000)

        # Block unnecessary resources
        await page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}",
                         lambda route: route.abort())

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector(item_selector, timeout=30_000)

        previous_count = 0
        no_new_content_count = 0

        while no_new_content_count < max_scroll_attempts:
            # Count current items
            current_count = await page.evaluate(
                f"document.querySelectorAll('{item_selector}').length"
            )

            if current_count >= max_items:
                break

            if current_count == previous_count:
                no_new_content_count += 1
            else:
                no_new_content_count = 0

            previous_count = current_count

            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(int(scroll_pause * 1000))

        # Extract all items at once
        items = await page.evaluate(f"""
            () => Array.from(document.querySelectorAll('{item_selector}')).map(el => ({{
                // Customize extraction per site:
                text: el.textContent.trim(),
                // name: el.querySelector('.name')?.textContent?.trim(),
                // price: el.querySelector('.price')?.textContent?.trim(),
            }}))
        """)

        await browser.close()
        return items[:max_items]
```

### Detecting Infinite Scroll API Endpoints

Many infinite scroll pages actually fetch data from an API when you scroll. If you can find this API endpoint, you can skip the browser entirely and use Web Unlocker to hit the API directly — this is faster and cheaper.

Look for these patterns in the page's JavaScript:
- Fetch/XHR calls triggered on scroll
- URLs with `page`, `offset`, `after`, or `cursor` parameters
- GraphQL queries with pagination variables

If you find the API, use Pattern 4 (Cursor) or Pattern 3 (Offset) with Web Unlocker instead.

---

## Pattern 6: Load More Button

A "Load More" or "Show More" button that fetches additional items. Two approaches:

### If the button triggers an API call (preferred)

Find the API endpoint and hit it directly with Web Unlocker — no browser needed.

### If no API is discoverable — use Browser API

```python
async def scrape_load_more(
    url: str,
    item_selector: str,
    button_selector: str,
    max_clicks: int = 50,
) -> list:
    """Click 'Load More' button repeatedly to load all content."""
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            f"wss://{AUTH}@brd.superproxy.io:9222"
        )
        page = await browser.new_page()
        page.set_default_navigation_timeout(120_000)
        await page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}",
                         lambda route: route.abort())

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector(item_selector, timeout=30_000)

        for _ in range(max_clicks):
            try:
                button = await page.wait_for_selector(
                    button_selector, timeout=5_000
                )
                if not button:
                    break
                await button.click()
                await page.wait_for_timeout(2000)
            except Exception:
                break  # Button gone — all content loaded

        # Extract all items
        items = await page.evaluate(f"""
            () => Array.from(document.querySelectorAll('{item_selector}')).map(el => ({{
                text: el.textContent.trim(),
            }}))
        """)

        await browser.close()
        return items
```

---

## Pattern 7: Category/Sitemap Crawling

When you need to scrape across categories, sections, or the entire site.

### Approach A: Scrape sitemap.xml

Many sites publish a sitemap that lists all pages:

```python
from bs4 import BeautifulSoup

def get_urls_from_sitemap(sitemap_url: str) -> list[str]:
    """Extract all URLs from a sitemap.xml file."""
    xml = fetch_page(sitemap_url)
    soup = BeautifulSoup(xml, "xml")

    urls = []
    # Handle sitemap index (links to other sitemaps)
    for sitemap in soup.select("sitemap loc"):
        sub_xml = fetch_page(sitemap.text.strip())
        sub_soup = BeautifulSoup(sub_xml, "xml")
        urls.extend(loc.text.strip() for loc in sub_soup.select("url loc"))

    # Handle direct URL listings
    urls.extend(loc.text.strip() for loc in soup.select("url loc"))

    return urls

# Usage
all_urls = get_urls_from_sitemap("https://example.com/sitemap.xml")
product_urls = [u for u in all_urls if "/product/" in u]
```

### Approach B: Crawl category pages

```python
def discover_and_scrape(category_urls: list[str]) -> list:
    """Scrape category listing pages to find individual item URLs, then scrape each."""
    all_items = []

    for cat_url in category_urls:
        # Scrape the category listing (may be paginated)
        item_urls = scrape_paginated_listing(cat_url)

        # Scrape each individual item page
        for item_url in item_urls:
            item_data = scrape_item_page(item_url)
            all_items.append(item_data)
            time.sleep(1)

    return all_items
```

---

## Async Bulk Pagination

When you know all page URLs upfront, fetch them concurrently for maximum speed.

### Using Python SDK

```python
import asyncio
from brightdata import BrightDataClient

async def scrape_all_pages_async(urls: list[str]) -> list:
    """Fetch multiple pages concurrently."""
    async with BrightDataClient() as client:
        # Scrape all URLs concurrently
        tasks = [client.scrape_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_items = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Failed: {urls[i]} — {result}")
                continue
            if result.success:
                items = parse_items(result.data)
                all_items.extend(items)

        return all_items

# Generate all page URLs upfront
urls = [f"https://example.com/products?page={i}" for i in range(1, 51)]
items = asyncio.run(scrape_all_pages_async(urls))
```

### Using Web Scraper API Trigger (for supported domains)

For sites with pre-built scrapers, submit all URLs at once:

```python
import requests
import time

def bulk_scrape_with_trigger(urls: list[str], dataset_id: str) -> list:
    """Submit all URLs to Web Scraper API at once."""
    # Trigger
    response = requests.post(
        "https://api.brightdata.com/datasets/v3/trigger",
        params={"dataset_id": dataset_id, "format": "json"},
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"input": [{"url": u} for u in urls]}
    )
    snapshot_id = response.json()["snapshot_id"]

    # Poll
    while True:
        progress = requests.get(
            f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        status = progress.json()["status"]
        if status == "ready":
            break
        if status == "failed":
            raise RuntimeError("Bulk scrape failed")
        time.sleep(10)

    # Download
    data = requests.get(
        f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
        params={"format": "json"},
        headers={"Authorization": f"Bearer {API_KEY}"}
    ).json()

    return data
```

---

## Rate Limiting and Politeness

Even with Bright Data handling proxy rotation and anti-bot bypass, be respectful of target sites:

```python
import time
import random

def polite_delay(min_seconds: float = 0.5, max_seconds: float = 2.0):
    """Random delay between requests to avoid hammering the site."""
    time.sleep(random.uniform(min_seconds, max_seconds))
```

**Guidelines:**
- Add 1-2 second delays between requests for sequential scraping
- For concurrent/async scraping, Bright Data's infrastructure handles rate limiting
- If you get consistent failures, increase the delay
- For Browser API sessions, the delay is less important since each session is independent

---

## Detecting End of Results

Knowing when to stop is just as important as knowing how to paginate.

### Strategies

1. **Empty results:** If `parse_items()` returns an empty list, stop.

2. **Duplicate detection:** If you see items you've already scraped, you've wrapped around.
   ```python
   seen_ids = set()
   for item in items:
       if item["id"] in seen_ids:
           return all_items  # Duplicates — stop
       seen_ids.add(item["id"])
   ```

3. **Total count comparison:** If the page shows "X of Y results", check when you've reached Y.
   ```python
   total_match = re.search(r'of (\d+) results', html)
   if total_match:
       total = int(total_match.group(1))
       if len(all_items) >= total:
           break
   ```

4. **Same page detection:** For next-link pagination, check you're not looping back.
   ```python
   visited_urls = set()
   if url in visited_urls:
       break  # Already visited this page
   visited_urls.add(url)
   ```

5. **Fewer items than expected:** If a page returns fewer items than the page size, it's the last page.
   ```python
   if len(items) < expected_page_size:
       all_items.extend(items)
       break  # Partial page = last page
   ```
