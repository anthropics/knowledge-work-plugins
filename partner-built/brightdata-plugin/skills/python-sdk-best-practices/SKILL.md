---
name: python-sdk-best-practices
description: Guide for writing correct Bright Data Python SDK code. Always use this skill when writing, modifying, debugging, or reviewing Python code that uses the brightdata-sdk package, imports from brightdata, or interacts with Bright Data APIs. Use when the user asks to scrape websites, search Google/Bing, access datasets, or automate browsers via Bright Data in Python.
---

# Bright Data Python SDK - Best Practices for Coding Agents

You are writing code that uses the `brightdata-sdk` Python package. Follow these rules precisely.

## Installation

```bash
pip install brightdata-sdk
```

## Critical Rules

1. **Always use context managers.** The client MUST be used with `async with` (or `with` for sync). Forgetting this causes `RuntimeError: BrightDataClient not initialized`.
2. **Async is the default.** The primary client is `BrightDataClient` (async). Use `SyncBrightDataClient` only when you cannot use async.
3. **Never use SyncBrightDataClient inside async functions.** It raises `RuntimeError`. Use `BrightDataClient` instead.
4. **Token auto-loads from environment.** Set `BRIGHTDATA_API_TOKEN` env var or pass `token=` param. Do not hardcode tokens.
5. **All scraper methods are awaitable.** Every call on the async client must be `await`ed.

## Authentication

```python
# Option 1: Environment variable (preferred)
# export BRIGHTDATA_API_TOKEN="your_token"
async with BrightDataClient() as client:
    ...

# Option 2: Explicit token
async with BrightDataClient(token="your_token") as client:
    ...

# Option 3: .env file (requires python-dotenv)
# BRIGHTDATA_API_TOKEN=your_token
async with BrightDataClient() as client:
    ...
```

## Imports

```python
# Main clients
from brightdata import BrightDataClient          # Async (primary)
from brightdata import SyncBrightDataClient       # Sync wrapper

# Result models
from brightdata import ScrapeResult, SearchResult, CrawlResult

# Job model (for manual trigger/poll/fetch)
from brightdata import ScrapeJob

# Exceptions
from brightdata import (
    BrightDataError,       # Base exception
    ValidationError,       # Invalid input
    AuthenticationError,   # Bad/missing token
    APIError,              # API request failed (has .status_code, .response_text)
    ZoneError,             # Zone operation failed
    NetworkError,          # Network issue
    SSLError,              # SSL cert error
)

# Scraper Studio
from brightdata import ScraperStudioJob, JobStatus

# Dataset export utility
from brightdata.datasets import export
```

## Core Patterns

### Pattern 1: Web Scraping (Web Unlocker)

Scrapes any URL through Bright Data's proxy network, bypassing bot detection.

```python
import asyncio
from brightdata import BrightDataClient

async def main():
    async with BrightDataClient() as client:
        # Single URL - returns ScrapeResult
        result = await client.scrape_url("https://example.com")
        print(result.success)  # bool
        print(result.data)     # HTML string or parsed data
        print(result.cost)     # float, USD

        # With options
        result = await client.scrape_url(
            url="https://example.com",
            country="us",              # Proxy country
            response_format="raw",     # "raw" (HTML) or "json"
            method="GET",              # HTTP method
            timeout=60,                # Request timeout seconds
        )

asyncio.run(main())
```

**Async mode** (non-blocking, for batch/background):
```python
result = await client.scrape_url(
    url="https://example.com",
    mode="async",           # Triggers, polls, returns when ready
    poll_interval=5,        # Seconds between polls
    poll_timeout=180,       # Max wait (Web Unlocker async ~2 min)
)

# Batch: pass a list of URLs
results = await client.scrape_url(
    url=["https://example.com/1", "https://example.com/2"],
    mode="async",
    poll_timeout=180,
)
# Returns List[ScrapeResult]
```

### Pattern 2: Platform-Specific Scrapers

Structured data extraction from major platforms. Pattern: `client.scrape.<platform>.<method>(url=...)`.

```python
async with BrightDataClient() as client:
    # Amazon
    product = await client.scrape.amazon.products(url="https://amazon.com/dp/B0CRMZHDG8")
    reviews = await client.scrape.amazon.reviews(url="https://amazon.com/dp/B0CRMZHDG8")
    sellers = await client.scrape.amazon.sellers(url="https://amazon.com/dp/B0CRMZHDG8")

    # LinkedIn
    profile = await client.scrape.linkedin.profiles(url="https://linkedin.com/in/username")
    company = await client.scrape.linkedin.companies(url="https://linkedin.com/company/name")
    posts   = await client.scrape.linkedin.posts(url="https://linkedin.com/posts/...")

    # Instagram
    ig_profile  = await client.scrape.instagram.profiles(url="https://instagram.com/username")
    ig_posts    = await client.scrape.instagram.posts(url="https://instagram.com/p/...")
    ig_comments = await client.scrape.instagram.comments(url="https://instagram.com/p/...")
    ig_reels    = await client.scrape.instagram.reels(url="https://instagram.com/reel/...")

    # Facebook
    fb_posts    = await client.scrape.facebook.posts_by_profile(url="https://facebook.com/user", num_of_posts=10)
    fb_group    = await client.scrape.facebook.posts_by_group(url="https://facebook.com/groups/...", num_of_posts=10)
    fb_comments = await client.scrape.facebook.comments(url="https://facebook.com/post/...", num_of_comments=20)
    fb_reels    = await client.scrape.facebook.reels(url="https://facebook.com/reel/...")

    # YouTube
    yt_profile  = await client.scrape.youtube.profiles(url="https://youtube.com/@channel")
    yt_video    = await client.scrape.youtube.videos(url="https://youtube.com/watch?v=...")
    yt_comments = await client.scrape.youtube.comments(url="https://youtube.com/watch?v=...")

    # ChatGPT
    response = await client.scrape.chatgpt.prompt(prompt="What is Python?")
    # Batch prompts
    responses = await client.scrape.chatgpt.prompts(prompts=["Q1", "Q2", "Q3"])

    # TikTok
    tt_profile = await client.scrape.tiktok.profiles(url="https://tiktok.com/@user")

    # Reddit
    reddit_post = await client.scrape.reddit.posts(url="https://reddit.com/r/...")
```

**All scraper methods return `ScrapeResult`** with `.success`, `.data`, `.cost`, `.status`.

### Pattern 3: Search Discovery (keyword-based)

Find content by keyword instead of URL:

```python
async with BrightDataClient() as client:
    # Amazon product search
    results = await client.scrape.amazon.products_search(keyword="wireless headphones")

    # LinkedIn searches
    profiles = await client.scrape.linkedin.profiles_search(keyword="data engineer", location="San Francisco")
    jobs     = await client.scrape.linkedin.jobs_search(keyword="python developer", location="New York")
    companies = await client.scrape.linkedin.companies_search(keyword="AI startup")

    # Instagram search
    ig_profiles = await client.scrape.instagram.profiles_search(user_name="photography")
    ig_posts    = await client.scrape.instagram.posts_search(url="https://instagram.com/user", num_of_posts=20)
    ig_reels    = await client.scrape.instagram.reels_search(url="https://instagram.com/user", num_of_posts=10)

    # YouTube search
    videos = await client.scrape.youtube.videos_search(keyword="python tutorial", num_of_videos=10)
```

### Pattern 4: SERP (Search Engine Results)

```python
async with BrightDataClient() as client:
    # Google
    result = await client.search.google(
        query="python web scraping",
        location="United States",    # Optional
        language="en",               # Default: "en"
        device="desktop",            # "desktop" or "mobile"
        num_results=10,              # Number of results
    )
    for item in result.data:
        print(item["title"], item["link"])

    # Bing
    result = await client.search.bing(query="python tutorial", num_results=10)

    # Yandex
    result = await client.search.yandex(query="python", num_results=10)
```

**SERP async mode:**
```python
result = await client.search.google(
    query="python",
    mode="async",
    poll_interval=2,
    poll_timeout=30,
)
```

**SERP returns `SearchResult`** with `.data` (list of dicts), `.query`, `.search_engine`.

### Pattern 5: Datasets API

Access 175+ pre-collected, structured datasets.

```python
async with BrightDataClient() as client:
    # Filter a dataset - returns snapshot_id (string)
    snapshot_id = await client.datasets.imdb_movies(
        filter={"name": "title", "operator": "includes", "value": "black"},
        records_limit=5,
    )

    # Download results (polls until ready)
    data = await client.datasets.imdb_movies.download(snapshot_id)
    print(f"Got {len(data)} records")

    # Quick sample (no filter needed)
    snapshot_id = await client.datasets.amazon_products.sample(records_limit=10)
    data = await client.datasets.amazon_products.download(snapshot_id)

    # Get field metadata
    metadata = await client.datasets.imdb_movies.get_metadata()
    for name, field in metadata.fields.items():
        print(f"{name}: {field.type}")
```

**Export to file:**
```python
from brightdata.datasets import export

export(data, "results.json")    # JSON
export(data, "results.csv")     # CSV
export(data, "results.jsonl")   # JSONL
```

**Available datasets include:** amazon_products, amazon_reviews, linkedin_profiles, linkedin_companies, linkedin_jobs, airbnb_properties, imdb_movies, google_maps_reviews, yelp_businesses, glassdoor_companies, zillow_properties, instagram_profiles, tiktok_profiles, facebook_pages_posts, reddit_posts, goodreads_books, nba_players_stats, and 150+ more.

### Pattern 6: Scraper Studio (Custom Scrapers)

Run custom scrapers built in Bright Data's Scraper Studio.

```python
async with BrightDataClient() as client:
    # High-level: trigger + poll + return
    data = await client.scraper_studio.run(
        collector="c_abc123",                          # Collector ID from dashboard
        input={"url": "https://example.com/page"},     # Input for the scraper
        timeout=180,                                    # Max wait seconds
        poll_interval=10,                               # Poll frequency
    )

    # Manual control
    job = await client.scraper_studio.trigger(
        collector="c_abc123",
        input={"url": "https://example.com/page"},
    )
    print(job.response_id)
    status = await job.status()        # Returns JobStatus enum
    data = await job.wait_and_fetch(timeout=120, poll_interval=10)
```

### Pattern 7: Browser API (CDP)

Connect to Bright Data cloud browsers via Chrome DevTools Protocol.

```python
from brightdata import BrightDataClient

client = BrightDataClient(
    browser_username="brd-customer-hl_xxx-zone-scraping_browser1",
    browser_password="your_password",
)
# Or use env vars: BRIGHTDATA_BROWSERAPI_USERNAME, BRIGHTDATA_BROWSERAPI_PASSWORD

url = client.browser.get_connect_url(country="us")  # Optional country

# With Playwright
from playwright.async_api import async_playwright

async with async_playwright() as pw:
    browser = await pw.chromium.connect_over_cdp(url)
    page = await browser.new_page()
    await page.goto("https://example.com")
    content = await page.content()
    await browser.close()
```

### Pattern 8: Manual Trigger/Poll/Fetch

For fine-grained control over long-running scrapes:

```python
async with BrightDataClient() as client:
    # Step 1: Trigger (non-blocking)
    job = await client.scrape.amazon.products_trigger(url="https://amazon.com/dp/B123")
    print(f"Snapshot ID: {job.snapshot_id}")

    # Step 2: Check status
    status = await job.status()  # "ready", "running", etc.

    # Step 3: Wait for completion
    await job.wait(timeout=180, poll_interval=10, verbose=True)

    # Step 4: Fetch results
    data = await job.fetch()

    # Or combine wait + fetch into ScrapeResult:
    result = await job.to_result(timeout=180)
    print(result.data)
```

### Pattern 9: Concurrent Batch Operations

```python
import asyncio
from brightdata import BrightDataClient

async def main():
    async with BrightDataClient() as client:
        # Concurrent scraping
        urls = [
            "https://amazon.com/dp/B001",
            "https://amazon.com/dp/B002",
            "https://amazon.com/dp/B003",
        ]
        tasks = [client.scrape.amazon.products(url=u) for u in urls]
        results = await asyncio.gather(*tasks)

        for r in results:
            print(f"{r.url}: success={r.success}, cost=${r.cost:.4f}")

        # Concurrent SERP queries
        queries = ["python", "javascript", "rust"]
        search_tasks = [client.search.google(query=q) for q in queries]
        search_results = await asyncio.gather(*search_tasks)

asyncio.run(main())
```

### Pattern 10: Sync Client

For scripts, notebooks, or non-async codebases:

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient() as client:
    # All methods are synchronous - no await needed
    result = client.scrape_url("https://example.com")
    print(result.data)

    result = client.scrape.amazon.products(url="https://amazon.com/dp/B123")
    result = client.search.google(query="python")

    # Datasets
    snapshot_id = client.datasets.imdb_movies(
        filter={"name": "title", "operator": "includes", "value": "black"},
        records_limit=5,
    )
    data = client.datasets.imdb_movies.download(snapshot_id)
```

**WARNING:** Never use `SyncBrightDataClient` inside an `async def` function. It will raise a RuntimeError.

## Result Objects Reference

All results inherit from `BaseResult`:

```python
result.success          # bool - operation succeeded
result.cost             # Optional[float] - cost in USD
result.error            # Optional[str] - error message if failed
result.elapsed_ms()     # Optional[float] - total time in ms
result.to_dict()        # Dict - serializable dictionary
result.to_json(indent=2)  # str - JSON string
result.save_to_file("out.json")  # Save to file
```

**ScrapeResult** additional fields:
```python
result.url              # str - original URL
result.status           # "ready" | "error" | "timeout" | "in_progress"
result.data             # Any - scraped data (dict, list, or HTML string)
result.snapshot_id      # Optional[str] - Bright Data snapshot ID
result.platform         # Optional[str] - "amazon", "linkedin", etc.
result.row_count        # Optional[int] - number of data rows
```

**SearchResult** additional fields:
```python
result.query            # Dict - original query params
result.data             # List[Dict] - search results
result.search_engine    # "google" | "bing" | "yandex"
result.total_found      # Optional[int] - total results found
```

## Error Handling

```python
from brightdata import (
    BrightDataClient,
    BrightDataError,
    ValidationError,
    AuthenticationError,
    APIError,
    NetworkError,
)

async with BrightDataClient() as client:
    try:
        result = await client.scrape_url("https://example.com")
    except AuthenticationError:
        print("Invalid API token")
    except APIError as e:
        print(f"API error {e.status_code}: {e.message}")
        print(f"Response: {e.response_text}")
    except NetworkError:
        print("Network connectivity issue")
    except ValidationError:
        print("Invalid input parameters")
    except BrightDataError as e:
        print(f"Bright Data error: {e.message}")
```

## Client Configuration

```python
client = BrightDataClient(
    token="...",                    # API token (or use env var)
    timeout=30,                     # Default request timeout (seconds)
    web_unlocker_zone="sdk_unlocker",  # Web Unlocker zone name
    serp_zone="sdk_serp",          # SERP zone name
    auto_create_zones=True,        # Auto-create zones if missing
    validate_token=False,          # Validate token on init
    rate_limit=10.0,               # Max requests per rate_period (None to disable)
    rate_period=1.0,               # Rate limit window (seconds)
)
```

**Zone auto-creation:** By default, the SDK creates `sdk_unlocker` and `sdk_serp` zones on first use. Set `auto_create_zones=False` to disable.

## Zone Management

```python
async with BrightDataClient() as client:
    # List all active zones
    zones = await client.list_zones()
    for zone in zones:
        print(f"{zone['name']}: {zone.get('type', 'unknown')}")

    # Delete a zone
    await client.delete_zone("test_zone")

    # Test connection
    is_valid = await client.test_connection()
```

## Common Mistakes to Avoid

1. **Forgetting the context manager:**
   ```python
   # WRONG - will raise RuntimeError
   client = BrightDataClient()
   result = await client.scrape_url("https://example.com")

   # CORRECT
   async with BrightDataClient() as client:
       result = await client.scrape_url("https://example.com")
   ```

2. **Using sync client in async code:**
   ```python
   # WRONG - will raise RuntimeError
   async def main():
       with SyncBrightDataClient() as client:
           result = client.scrape_url("...")

   # CORRECT
   async def main():
       async with BrightDataClient() as client:
           result = await client.scrape_url("...")
   ```

3. **Forgetting await:**
   ```python
   # WRONG - returns coroutine, not result
   result = client.scrape_url("https://example.com")

   # CORRECT
   result = await client.scrape_url("https://example.com")
   ```

4. **Not checking result.success:**
   ```python
   result = await client.scrape_url("https://example.com")
   # Always check success before using data
   if result.success:
       process(result.data)
   else:
       print(f"Failed: {result.error}")
   ```

5. **Hardcoding API tokens:**
   ```python
   # WRONG
   client = BrightDataClient(token="abc123secret")

   # CORRECT - use environment variable
   # export BRIGHTDATA_API_TOKEN=abc123secret
   client = BrightDataClient()
   ```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `BRIGHTDATA_API_TOKEN` | API authentication token | Required |
| `WEB_UNLOCKER_ZONE` | Web Unlocker zone name | `sdk_unlocker` |
| `SERP_ZONE` | SERP zone name | `sdk_serp` |
| `BRIGHTDATA_BROWSERAPI_USERNAME` | Browser API username | None |
| `BRIGHTDATA_BROWSERAPI_PASSWORD` | Browser API password | None |

## Quick Decision Guide

| Task | Method |
|------|--------|
| Scrape any URL (HTML) | `client.scrape_url(url)` |
| Scrape Amazon/LinkedIn/etc. (structured) | `client.scrape.<platform>.<method>(url=...)` |
| Search Google/Bing/Yandex | `client.search.google(query=...)` |
| Find products/profiles by keyword | `client.scrape.<platform>.<type>_search(keyword=...)` |
| Access pre-collected datasets | `client.datasets.<name>(filter=..., records_limit=...)` |
| Run custom Scraper Studio scraper | `client.scraper_studio.run(collector=..., input=...)` |
| Automate browser (Playwright/Puppeteer) | `client.browser.get_connect_url()` |
| Long-running scrape with manual control | `client.scrape.<platform>.<method>_trigger(url=...)` then `job.wait()` + `job.fetch()` |

For the full API surface and advanced patterns, read [references/api-reference.md](references/api-reference.md).
