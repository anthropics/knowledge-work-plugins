# Pre-Built Scrapers — Supported Domains

Check this list before writing any custom scraping code. If the target domain is listed here, use the Web Scraper API or Python SDK platform-specific scraper instead of building a custom solution.

**This list is a curated subset.** Bright Data supports 100+ domains with pre-built scrapers. The tables below cover the most common ones, but the full list is dynamic and grows regularly. If you don't see a domain here, **always check the live dataset list** before falling back to a custom scraper.

---

## Discovering ALL Available Scrapers (Dynamic Lookup)

The tables below are a quick reference, but they may not include every scraper Bright Data offers. Before building a custom scraper for any domain, use these two methods to check for a pre-built solution:

### Method 1: Query the Dataset List API

This returns every available pre-built scraper with its `dataset_id` and name:

```bash
curl -H "Authorization: Bearer $BRIGHTDATA_API_KEY" \
     https://api.brightdata.com/datasets/list
```

```python
import requests
import os

response = requests.get(
    "https://api.brightdata.com/datasets/list",
    headers={"Authorization": f"Bearer {os.environ['BRIGHTDATA_API_KEY']}"}
)
datasets = response.json()

# Search for a specific domain
domain = "shopify"  # whatever site you're looking for
matches = [d for d in datasets if domain.lower() in d["name"].lower()]
for d in matches:
    print(f"  {d['id']}: {d['name']} ({d['size']:,} records)")
```

**Response format:**
```json
[
  {"id": "gd_l1vijqt9jfj7olije", "name": "Crunchbase companies information", "size": 2300000},
  {"id": "gd_l1vikfch901nx3by4", "name": "Instagram - Profiles", "size": 620000000}
]
```

Each item has:
- `id` — the `dataset_id` to use with the Web Scraper API (`/datasets/v3/scrape` or `/datasets/v3/trigger`)
- `name` — human-readable name describing the scraper
- `size` — number of records in the dataset

When you find a matching dataset, use its `id` as the `dataset_id` parameter in Web Scraper API calls.

### Method 2: Browse the Full Documentation

Fetch the complete Bright Data documentation index at:

```
https://docs.brightdata.com/llms.txt
```

This file lists all available documentation pages. Use it to discover scraper-specific docs, API references, and guides for any supported domain. Particularly useful for finding input/output schemas and supported parameters for specific scrapers.

### When to Use Dynamic Lookup

- **Always** when the target domain isn't in the Quick Lookup table below
- When you're unsure if a scraper exists for a specific data type on a known domain (e.g., "does Bright Data have an Amazon seller reviews scraper?")
- When the user asks about a niche or recently-added platform
- When building scrapers for sites in categories like real estate, travel, food delivery, job boards, or classifieds — Bright Data frequently adds new scrapers for these verticals

---

## Quick Lookup

| Domain | Has Pre-Built Scraper? | Approach |
|--------|----------------------|----------|
| Amazon | Yes | SDK: `client.scrape.amazon.*` or Shell: `datasets.sh amazon_*` |
| LinkedIn | Yes | SDK: `client.scrape.linkedin.*` or Shell: `datasets.sh linkedin_*` |
| Instagram | Yes | SDK: `client.scrape.instagram.*` or Shell: `datasets.sh instagram_*` |
| Facebook | Yes | SDK: `client.scrape.facebook.*` or Shell: `datasets.sh facebook_*` |
| TikTok | Yes | SDK: `client.scrape.tiktok.*` or Shell: `datasets.sh tiktok_*` |
| YouTube | Yes | SDK: `client.scrape.youtube.*` or Shell: `datasets.sh youtube_*` |
| Twitter/X | Yes | Shell: `datasets.sh x_posts` |
| Reddit | Yes | SDK: `client.scrape.reddit.*` or Shell: `datasets.sh reddit_posts` |
| Walmart | Yes | Shell: `datasets.sh walmart_*` |
| eBay | Yes | Shell: `datasets.sh ebay_product` |
| Best Buy | Yes | Shell: `datasets.sh bestbuy_products` |
| Home Depot | Yes | Shell: `datasets.sh homedepot_products` |
| Etsy | Yes | Shell: `datasets.sh etsy_products` |
| Zara | Yes | Shell: `datasets.sh zara_products` |
| Google Maps | Yes | Shell: `datasets.sh google_maps_reviews` |
| Google Shopping | Yes | Shell: `datasets.sh google_shopping` |
| Google Play Store | Yes | Shell: `datasets.sh google_play_store` |
| Apple App Store | Yes | Shell: `datasets.sh apple_app_store` |
| Crunchbase | Yes | Shell: `datasets.sh crunchbase_company` |
| ZoomInfo | Yes | Shell: `datasets.sh zoominfo_company_profile` |
| Zillow | Yes | Shell: `datasets.sh zillow_properties_listing` |
| Booking.com | Yes | Shell: `datasets.sh booking_hotel_listings` |
| Yahoo Finance | Yes | Shell: `datasets.sh yahoo_finance_business` |
| Reuters | Yes | Shell: `datasets.sh reuter_news` |
| GitHub | Yes | Shell: `datasets.sh github_repository_file` |
| Any other site | No | Use Web Unlocker or Browser API (custom scraper) |

---

## E-Commerce Scrapers

### Amazon

| Data Type | Shell Command | Python SDK | Dataset ID |
|-----------|--------------|------------|------------|
| Product details | `datasets.sh amazon_product <url>` | `client.scrape.amazon.products(url=...)` | `gd_l7q7dkf244hwjntr0` |
| Product reviews | `datasets.sh amazon_product_reviews <url>` | `client.scrape.amazon.reviews(url=...)` | — |
| Seller info | — | `client.scrape.amazon.sellers(url=...)` | — |
| Product search | `datasets.sh amazon_product_search <keyword> <domain>` | `client.scrape.amazon.products_search(keyword=...)` | — |

**Amazon-specific tips:**
- Use `x-unblock-zipcode` header with Web Unlocker to get location-specific pricing
- Product search accepts keywords + domain URL (e.g., `https://www.amazon.com`)
- Reviews scraper returns all reviews for a given product URL

### Walmart

| Data Type | Shell Command | Dataset ID |
|-----------|--------------|------------|
| Product details | `datasets.sh walmart_product <url>` | — |
| Seller info | `datasets.sh walmart_seller <url>` | — |

### eBay

| Data Type | Shell Command | Dataset ID |
|-----------|--------------|------------|
| Listing details | `datasets.sh ebay_product <url>` | — |

### Other E-Commerce

| Platform | Shell Command |
|----------|--------------|
| Best Buy | `datasets.sh bestbuy_products <url>` |
| Home Depot | `datasets.sh homedepot_products <url>` |
| Etsy | `datasets.sh etsy_products <url>` |
| Zara | `datasets.sh zara_products <url>` |
| Google Shopping | `datasets.sh google_shopping <url>` |

---

## Social Media Scrapers

### Instagram

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Profile | `datasets.sh instagram_profiles <url>` | `client.scrape.instagram.profiles(url=...)` |
| Posts | `datasets.sh instagram_posts <url>` | `client.scrape.instagram.posts(url=...)` |
| Reels | `datasets.sh instagram_reels <url>` | `client.scrape.instagram.reels(url=...)` |
| Comments | `datasets.sh instagram_comments <url>` | `client.scrape.instagram.comments(url=...)` |
| Profile search | — | `client.scrape.instagram.profiles_search(user_name=...)` |
| Posts by user | — | `client.scrape.instagram.posts_search(url=..., num_of_posts=20)` |

### Facebook

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Posts | `datasets.sh facebook_posts <url>` | `client.scrape.facebook.posts_by_profile(url=..., num_of_posts=10)` |
| Group posts | — | `client.scrape.facebook.posts_by_group(url=..., num_of_posts=10)` |
| Marketplace | `datasets.sh facebook_marketplace_listings <url>` | — |
| Reviews | `datasets.sh facebook_company_reviews <url> [num]` | — |
| Events | `datasets.sh facebook_events <url>` | — |
| Reels | — | `client.scrape.facebook.reels(url=...)` |
| Comments | — | `client.scrape.facebook.comments(url=..., num_of_comments=20)` |

### TikTok

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Profile | `datasets.sh tiktok_profiles <url>` | `client.scrape.tiktok.profiles(url=...)` |
| Posts/Videos | `datasets.sh tiktok_posts <url>` | — |
| Shop products | `datasets.sh tiktok_shop <url>` | — |
| Comments | `datasets.sh tiktok_comments <url>` | — |

### YouTube

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Channel | `datasets.sh youtube_profiles <url>` | `client.scrape.youtube.profiles(url=...)` |
| Videos | `datasets.sh youtube_videos <url>` | `client.scrape.youtube.videos(url=...)` |
| Comments | `datasets.sh youtube_comments <url> [num]` | `client.scrape.youtube.comments(url=...)` |
| Video search | — | `client.scrape.youtube.videos_search(keyword=..., num_of_videos=10)` |

### Twitter/X

| Data Type | Shell Command |
|-----------|--------------|
| Posts/Tweets | `datasets.sh x_posts <url>` |

### Reddit

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Posts | `datasets.sh reddit_posts <url>` | `client.scrape.reddit.posts(url=...)` |

---

## Professional / Business Scrapers

### LinkedIn

| Data Type | Shell Command | Python SDK |
|-----------|--------------|------------|
| Person profile | `datasets.sh linkedin_person_profile <url>` | `client.scrape.linkedin.profiles(url=...)` |
| Company profile | `datasets.sh linkedin_company_profile <url>` | `client.scrape.linkedin.companies(url=...)` |
| Job listings | `datasets.sh linkedin_job_listings <url>` | — |
| Posts | `datasets.sh linkedin_posts <url>` | `client.scrape.linkedin.posts(url=...)` |
| People search | `datasets.sh linkedin_people_search <url> <first> <last>` | `client.scrape.linkedin.profiles_search(keyword=..., location=...)` |
| Job search | — | `client.scrape.linkedin.jobs_search(keyword=..., location=...)` |
| Company search | — | `client.scrape.linkedin.companies_search(keyword=...)` |

### Other Business

| Platform | Shell Command |
|----------|--------------|
| Crunchbase | `datasets.sh crunchbase_company <url>` |
| ZoomInfo | `datasets.sh zoominfo_company_profile <url>` |

---

## Other Scrapers

| Platform | Data Type | Shell Command |
|----------|-----------|--------------|
| Zillow | Property listings | `datasets.sh zillow_properties_listing <url>` |
| Booking.com | Hotel listings | `datasets.sh booking_hotel_listings <url>` |
| Yahoo Finance | Company/stock data | `datasets.sh yahoo_finance_business <url>` |
| Reuters | News articles | `datasets.sh reuter_news <url>` |
| GitHub | Repository files | `datasets.sh github_repository_file <url>` |
| Google Maps | Business reviews | `datasets.sh google_maps_reviews <url> [days]` |
| Google Play | App details | `datasets.sh google_play_store <url>` |
| Apple App Store | App details | `datasets.sh apple_app_store <url>` |

---

## Using Pre-Built Scrapers for Bulk Operations

### Python SDK — Concurrent Batch

```python
import asyncio
from brightdata import BrightDataClient

async def bulk_scrape(urls: list[str]):
    async with BrightDataClient() as client:
        tasks = [client.scrape.amazon.products(url=u) for u in urls]
        results = await asyncio.gather(*tasks)
        return [r.data for r in results if r.success]
```

### Shell — Multiple URLs with Web Scraper API

```bash
# Direct API call with multiple inputs
bash scripts/fetch.sh gd_l7q7dkf244hwjntr0 '[{"url":"https://amazon.com/dp/B001"},{"url":"https://amazon.com/dp/B002"}]'
```

### REST API — Async Trigger for Large Batches

For 20+ URLs, use the async trigger endpoint:

```python
import requests

# Trigger
response = requests.post(
    "https://api.brightdata.com/datasets/v3/trigger",
    params={"dataset_id": "gd_l7q7dkf244hwjntr0", "format": "json"},
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"input": [{"url": u} for u in urls]}
)
snapshot_id = response.json()["snapshot_id"]

# Poll + Download (see Web Scraper API reference for full pattern)
```
