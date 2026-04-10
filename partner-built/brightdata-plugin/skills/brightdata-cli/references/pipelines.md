# Pipeline Types Reference

All pipeline types available via `bdata pipelines <type> [params...]`.

Run `bdata pipelines list` to see all types in your terminal.

## Parameter Patterns

Most types require just a URL:
```bash
bdata pipelines <type> "<url>"
```

Some types have additional parameters — these are documented below.

---

## E-Commerce

| Type | Platform | Parameters |
|------|----------|------------|
| `amazon_product` | Amazon product page | `<url>` |
| `amazon_product_reviews` | Amazon reviews | `<url>` |
| `amazon_product_search` | Amazon search results | `<keyword> <domain_url>` |
| `walmart_product` | Walmart product page | `<url>` |
| `walmart_seller` | Walmart seller profile | `<url>` |
| `ebay_product` | eBay listing | `<url>` |
| `bestbuy_products` | Best Buy | `<url>` |
| `etsy_products` | Etsy | `<url>` |
| `homedepot_products` | Home Depot | `<url>` |
| `zara_products` | Zara | `<url>` |
| `google_shopping` | Google Shopping | `<url>` |

### Amazon Search Example
```bash
# Requires both keyword and domain URL
bdata pipelines amazon_product_search "wireless headphones" "https://amazon.com"
```

---

## Professional Networks

| Type | Platform | Parameters |
|------|----------|------------|
| `linkedin_person_profile` | LinkedIn person | `<url>` |
| `linkedin_company_profile` | LinkedIn company | `<url>` |
| `linkedin_job_listings` | LinkedIn jobs | `<url>` |
| `linkedin_posts` | LinkedIn posts | `<url>` |
| `linkedin_people_search` | LinkedIn people search | `<url> <first_name> <last_name>` |
| `crunchbase_company` | Crunchbase | `<url>` |
| `zoominfo_company_profile` | ZoomInfo | `<url>` |

### LinkedIn People Search Example
```bash
# Requires URL, first name, and last name
bdata pipelines linkedin_people_search "https://linkedin.com/search/results/people" "John" "Doe"
```

---

## Social Media

| Type | Platform | Parameters |
|------|----------|------------|
| `instagram_profiles` | Instagram profiles | `<url>` |
| `instagram_posts` | Instagram posts | `<url>` |
| `instagram_reels` | Instagram reels | `<url>` |
| `instagram_comments` | Instagram comments | `<url>` |
| `facebook_posts` | Facebook posts | `<url>` |
| `facebook_marketplace_listings` | Facebook Marketplace | `<url>` |
| `facebook_company_reviews` | Facebook reviews | `<url> [num_reviews]` |
| `facebook_events` | Facebook events | `<url>` |
| `tiktok_profiles` | TikTok profiles | `<url>` |
| `tiktok_posts` | TikTok posts | `<url>` |
| `tiktok_shop` | TikTok shop | `<url>` |
| `tiktok_comments` | TikTok comments | `<url>` |
| `x_posts` | X (Twitter) posts | `<url>` |
| `youtube_profiles` | YouTube channels | `<url>` |
| `youtube_videos` | YouTube videos | `<url>` |
| `youtube_comments` | YouTube comments | `<url> [num_comments]` |
| `reddit_posts` | Reddit posts | `<url>` |

### YouTube Comments Example
```bash
# Optional second param: number of comments (default: 10)
bdata pipelines youtube_comments "https://youtube.com/watch?v=dQw4w9WgXcQ" 50
```

### Facebook Reviews Example
```bash
# Optional second param: number of reviews (default: 10)
bdata pipelines facebook_company_reviews "https://facebook.com/company" 25
```

---

## Maps, Reviews & Other

| Type | Platform | Parameters |
|------|----------|------------|
| `google_maps_reviews` | Google Maps reviews | `<url> [days_limit]` |
| `google_play_store` | Google Play | `<url>` |
| `apple_app_store` | Apple App Store | `<url>` |
| `reuter_news` | Reuters news | `<url>` |
| `github_repository_file` | GitHub repository files | `<url>` |
| `yahoo_finance_business` | Yahoo Finance | `<url>` |
| `zillow_properties_listing` | Zillow | `<url>` |
| `booking_hotel_listings` | Booking.com | `<url>` |

### Google Maps Reviews Example
```bash
# Optional second param: days_limit (default: 3)
bdata pipelines google_maps_reviews "https://maps.google.com/maps/place/..." 7
```

---

## Output Options

All pipeline commands support:

```bash
# JSON (default)
bdata pipelines amazon_product "<url>"

# CSV
bdata pipelines amazon_product "<url>" --format csv

# NDJSON / JSONL
bdata pipelines amazon_product "<url>" --format ndjson

# Save to file
bdata pipelines amazon_product "<url>" -o product.json

# Custom timeout (default 600 seconds)
bdata pipelines amazon_product "<url>" --timeout 1200
```

## How Pipelines Work

1. CLI sends a trigger request to `/datasets/v3/trigger` with the dataset ID and input
2. Receives a `snapshot_id`
3. Polls `/datasets/v3/snapshot/{snapshot_id}` until status is no longer `starting`/`building`/`running`
4. Returns the collected data in the requested format

The default timeout is 600 seconds (10 minutes). For large datasets, increase with `--timeout` or set `BRIGHTDATA_POLLING_TIMEOUT` environment variable.
