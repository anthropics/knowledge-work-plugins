# Concurrency & Parallelism Guide for Scrapers

## The Problem

By default, coding agents write scrapers that fetch URLs **one at a time** — sequential loops with `time.sleep()` between requests. For small jobs (10-20 pages) this is fine, but for thousands of URLs it's painfully slow. A scraper fetching 9,000 URLs sequentially at 1 request/second takes **2.5 hours**. With 20 concurrent requests, it takes **7.5 minutes**.

**Always build scrapers with concurrency when the user has more than ~50 URLs to scrape.** This is not an optimization — it's a baseline requirement for production scrapers.

---

## Core Principle: Semaphore-Controlled Concurrency

Never fire all requests at once (`asyncio.gather(*all_tasks)`) — this overwhelms both the target site and the proxy infrastructure. Instead, use a **semaphore** to cap the number of concurrent in-flight requests.

```python
import asyncio
import aiohttp

CONCURRENCY = 20  # Max concurrent requests — tune per site (see below)

async def fetch_page(session: aiohttp.ClientSession, sem: asyncio.Semaphore, url: str) -> dict:
    """Fetch a single URL with concurrency control."""
    async with sem:
        async with session.post(
            "https://api.brightdata.com/request",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"zone": ZONE, "url": url, "format": "raw"},
            timeout=aiohttp.ClientTimeout(total=60),
        ) as response:
            html = await response.text()
            return {"url": url, "html": html, "status": response.status}

async def scrape_concurrent(urls: list[str]) -> list[dict]:
    """Scrape all URLs with controlled concurrency."""
    sem = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, sem, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = []
    for r in results:
        if isinstance(r, Exception):
            log.warning(f"Failed: {r}")
        else:
            successes.append(r)
    return successes
```

---

## How to Choose the Right Concurrency Level

The optimal concurrency depends on which Bright Data API you're using and the target site. Here are recommended starting points:

| API | Recommended Concurrency | Notes |
|-----|------------------------|-------|
| Web Unlocker | 20-50 concurrent requests | Bright Data handles rate limiting on their side |
| Web Scraper API (async) | 5-10 batch triggers | Each trigger handles batching internally |
| Browser API | 5-10 concurrent sessions | Each session is a real browser — resource-heavy |
| SERP API | 20-50 concurrent requests | Similar to Web Unlocker |

### Per-Site Tuning

Start with the recommended default, then adjust:

1. **Start conservative** — begin at 10 concurrent requests
2. **Watch for errors** — if you see 429 (rate limited) or 502/503 errors, reduce concurrency
3. **Ramp up gradually** — if no errors after 100 requests, increase to 20, then 30, etc.
4. **Different sites, different limits** — if scraping 3 sites, tune each independently

```python
# Per-site concurrency configuration
SITE_CONCURRENCY = {
    "amazon.com": 10,       # Aggressive anti-bot — keep low
    "example-blog.com": 30, # Lenient site — can push higher
    "news-site.com": 20,    # Middle ground
}
```

---

## Multi-Site Concurrent Scraping

When scraping multiple sites simultaneously (e.g., enriching a database from 3 different sources), run each site's scraper concurrently with **independent concurrency controls per site**:

```python
import asyncio
import aiohttp

async def scrape_site(site_name: str, urls: list[str], concurrency: int) -> list[dict]:
    """Scrape one site with its own concurrency limit."""
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, sem, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    log.info(f"{site_name}: scraped {len([r for r in results if not isinstance(r, Exception)])} / {len(urls)}")
    return [r for r in results if not isinstance(r, Exception)]

async def scrape_all_sites(site_configs: dict[str, dict]) -> dict[str, list[dict]]:
    """Scrape multiple sites in parallel, each with its own concurrency limit.

    site_configs = {
        "surfline": {"urls": [...], "concurrency": 20},
        "magicseaweed": {"urls": [...], "concurrency": 15},
        "wannasurf": {"urls": [...], "concurrency": 10},
    }
    """
    tasks = {
        name: scrape_site(name, cfg["urls"], cfg["concurrency"])
        for name, cfg in site_configs.items()
    }
    results = await asyncio.gather(*tasks.values())
    return dict(zip(tasks.keys(), results))
```

---

## Adding Retries with Backoff

Concurrent scrapers need smarter retry logic than sequential ones. Use exponential backoff:

```python
async def fetch_with_retry(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    url: str,
    max_retries: int = 3,
) -> dict | None:
    """Fetch a URL with concurrency control and exponential backoff."""
    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.post(
                    "https://api.brightdata.com/request",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={"zone": ZONE, "url": url, "format": "raw"},
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status == 429:
                        wait = 2 ** attempt
                        log.warning(f"Rate limited on {url}, waiting {wait}s")
                        await asyncio.sleep(wait)
                        continue
                    response.raise_for_status()
                    return {"url": url, "html": await response.text()}
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    log.error(f"Failed after {max_retries} attempts: {url} — {e}")
                    return None
```

---

## Progress Tracking

For large jobs, show progress so the user knows it's working:

```python
import asyncio

async def scrape_with_progress(urls: list[str], concurrency: int = 20) -> list[dict]:
    """Scrape with a live progress counter."""
    sem = asyncio.Semaphore(concurrency)
    completed = 0
    total = len(urls)
    results = []

    async def fetch_and_track(session, url):
        nonlocal completed
        result = await fetch_with_retry(session, sem, url)
        completed += 1
        if completed % 50 == 0 or completed == total:
            log.info(f"Progress: {completed}/{total} ({100*completed//total}%)")
        return result

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_track(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]
```

---

## Complete Template: Concurrent Scraper

```python
#!/usr/bin/env python3
"""
Concurrent scraper template.
Usage:
    export BRIGHTDATA_API_KEY="your-key"
    export BRIGHTDATA_UNLOCKER_ZONE="your-zone"
    python scraper.py
"""

import asyncio
import json
import logging
import os

import aiohttp
from bs4 import BeautifulSoup

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]
CONCURRENCY = 20
OUTPUT_FILE = "results.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


async def fetch_page(session, sem, url, max_retries=3):
    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.post(
                    "https://api.brightdata.com/request",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={"zone": ZONE, "url": url, "format": "raw"},
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    if resp.status == 429:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    resp.raise_for_status()
                    return {"url": url, "html": await resp.text()}
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    log.error(f"Failed: {url} — {e}")
                    return None


def parse_items(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for card in soup.select("ITEM_SELECTOR"):
        try:
            items.append({
                "name": card.select_one("NAME_SELECTOR").get_text(strip=True),
                "url": card.select_one("a").get("href", ""),
            })
        except (AttributeError, TypeError):
            continue
    return items


async def main():
    # Generate your URLs
    urls = [f"https://example.com/page/{i}" for i in range(1, 501)]

    sem = asyncio.Semaphore(CONCURRENCY)
    completed = 0
    total = len(urls)
    all_items = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, sem, url) for url in urls]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            completed += 1
            if result:
                items = parse_items(result["html"])
                all_items.extend(items)
            if completed % 50 == 0 or completed == total:
                log.info(f"Progress: {completed}/{total} — {len(all_items)} items extracted")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    log.info(f"Done. Saved {len(all_items)} items to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Quick Decision Guide

| Situation | Approach |
|-----------|----------|
| < 50 URLs | Sequential is fine — keep it simple |
| 50-500 URLs | Concurrent with semaphore (concurrency=10-20) |
| 500-10,000 URLs | Concurrent with semaphore (concurrency=20-50), add progress tracking |
| 10,000+ URLs | Concurrent + batch into chunks of 1,000, save intermediate results |
| Multiple sites | Independent concurrent scrapers per site, run in parallel |
| Pre-built scraper (Web Scraper API) | Use async trigger/poll/fetch — batching is built in |
