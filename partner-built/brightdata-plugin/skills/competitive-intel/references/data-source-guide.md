# Data Source Selection Guide

This reference maps every competitive intelligence need to the specific `bdata` CLI command. Use this to decide which command to run for each piece of intelligence.

## Command Selection Rule

**Always prefer `bdata pipelines`** (structured JSON) **over `bdata scrape`** (raw markdown) when a pipeline type exists for the target platform. Pipelines return clean, structured data that's easier to analyze. Fall back to `bdata scrape` only when no pipeline exists.

## Intelligence Need → Command Mapping

### Company & Business Intelligence

| Need | Primary Command | Fallback |
|------|----------------|----------|
| Company overview (funding, size, investors) | `bdata pipelines crunchbase_company "[crunchbase-url]"` | `bdata scrape [url]/about` |
| Employee count & company details | `bdata pipelines linkedin_company_profile "[linkedin-url]"` | `bdata pipelines crunchbase_company "[url]"` |
| Financial data (public companies) | `bdata pipelines yahoo_finance_business "[yahoo-finance-url]"` | `bdata pipelines crunchbase_company "[url]"` |
| Company news & PR | `bdata search "[company] news" --json` | `bdata pipelines reuter_news "[reuters-url]"` |
| Company website / homepage | `bdata scrape [url]` | — |

### Pricing & Products

| Need | Primary Command | Fallback |
|------|----------------|----------|
| SaaS pricing pages | `bdata scrape [url]/pricing` | `bdata search "[company] pricing" --json` |
| Amazon product details | `bdata pipelines amazon_product "[amazon-url]"` | `bdata scrape [url]` |
| Amazon product reviews | `bdata pipelines amazon_product_reviews "[amazon-url]"` | — |
| Amazon search results | `bdata pipelines amazon_product_search "[keyword]" "[amazon-domain]"` | `bdata search "[keyword] site:amazon.com" --json` |
| Walmart products | `bdata pipelines walmart_product "[walmart-url]"` | `bdata scrape [url]` |
| eBay listings | `bdata pipelines ebay_product "[ebay-url]"` | `bdata scrape [url]` |
| Etsy products | `bdata pipelines etsy_products "[etsy-url]"` | `bdata scrape [url]` |
| Best Buy products | `bdata pipelines bestbuy_products "[bestbuy-url]"` | `bdata scrape [url]` |
| Third-party pricing reviews | `bdata search "[company] pricing review" --json` | — |

### Reviews & Customer Sentiment

| Need | Primary Command | Fallback |
|------|----------------|----------|
| G2 reviews (SaaS) | `bdata scrape [g2-product-url]` | `bdata search "[product] site:g2.com" --json` → scrape result |
| Capterra reviews (SaaS) | `bdata scrape [capterra-product-url]` | `bdata search "[product] site:capterra.com" --json` → scrape result |
| Google Maps reviews (local) | `bdata pipelines google_maps_reviews "[maps-url]" [days]` | — |
| Google Play Store (apps) | `bdata pipelines google_play_store "[play-url]"` | — |
| Apple App Store (apps) | `bdata pipelines apple_app_store "[appstore-url]"` | — |
| Trustpilot reviews | `bdata scrape [trustpilot-url]` | `bdata search "[company] site:trustpilot.com" --json` → scrape result |

### Hiring & Talent

| Need | Primary Command | Fallback |
|------|----------------|----------|
| Job listings | `bdata pipelines linkedin_job_listings "[linkedin-url]"` | `bdata scrape [careers-url]` |
| Company LinkedIn page | `bdata pipelines linkedin_company_profile "[linkedin-url]"` | `bdata search "[company] linkedin" --json` |
| Key people / leadership | `bdata pipelines linkedin_person_profile "[linkedin-url]"` | `bdata scrape [url]/team` |
| Careers page | `bdata scrape [url]/careers` | `bdata search "[company] careers" --json` → scrape result |

### Content & SEO

| Need | Primary Command | Fallback |
|------|----------------|----------|
| SERP rankings for keyword | `bdata search "[keyword]" --json` | — |
| Indexed page count | `bdata search "site:[domain]" --json` | — |
| Blog / content pages | `bdata scrape [url]/blog` | `bdata search "site:[domain] blog" --json` |
| Individual articles | `bdata scrape [article-url]` | — |
| News search | `bdata search "[topic]" --json --type news` | `bdata search "[topic] news" --json` |

### Social Media

| Need | Primary Command | Fallback |
|------|----------------|----------|
| Instagram profile | `bdata pipelines instagram_profiles "[instagram-url]"` | — |
| Instagram posts | `bdata pipelines instagram_posts "[instagram-url]"` | — |
| TikTok profile | `bdata pipelines tiktok_profiles "[tiktok-url]"` | — |
| TikTok posts | `bdata pipelines tiktok_posts "[tiktok-url]"` | — |
| YouTube channel | `bdata pipelines youtube_profiles "[youtube-url]"` | — |
| YouTube video details | `bdata pipelines youtube_videos "[youtube-url]"` | — |
| YouTube comments | `bdata pipelines youtube_comments "[youtube-url]" [count]` | — |
| X (Twitter) posts | `bdata pipelines x_posts "[x-url]"` | — |
| Reddit posts | `bdata pipelines reddit_posts "[reddit-url]"` | — |
| Facebook posts | `bdata pipelines facebook_posts "[facebook-url]"` | — |
| Facebook reviews | `bdata pipelines facebook_company_reviews "[facebook-url]"` | — |
| LinkedIn posts | `bdata pipelines linkedin_posts "[linkedin-url]"` | — |

### Competitor Discovery

| Need | Primary Command | Fallback |
|------|----------------|----------|
| Find competitors by category | `bdata search "[category] companies" --json` | `bdata search "best [category] tools" --json` |
| Find alternatives | `bdata search "[product] alternatives" --json` | `bdata scrape [g2-category-url]` |
| G2 category page | `bdata scrape [g2-category-url]` | `bdata search "[category] site:g2.com" --json` → scrape result |
| Market overview | `bdata search "[industry] market landscape" --json` | — |

## Finding URLs When You Don't Have Them

Often you'll know a competitor's name but not their specific URLs on platforms. Use this pattern:

```bash
# Find a company's Crunchbase page
bdata search "[company name] crunchbase" --json | jq -r '.organic[0].link'

# Find a company's LinkedIn page
bdata search "[company name] linkedin company" --json | jq -r '.organic[0].link'

# Find a company's G2 page
bdata search "[company name] site:g2.com" --json | jq -r '.organic[0].link'

# Find a company's careers page
bdata search "[company name] careers" --json | jq -r '.organic[0].link'
```

## Cost Efficiency Guidelines

| Analysis Type | Recommended `bdata` Calls | Estimated Cost |
|--------------|--------------------------|----------------|
| Quick Snapshot (1 competitor) | 3-5 calls | ~$0.01-$0.05 |
| Pricing Comparison (3 competitors) | 3-6 calls | ~$0.01-$0.05 |
| Review Intelligence (1 competitor) | 2-4 calls | ~$0.01-$0.05 |
| Hiring Signal Analysis | 2-3 calls | ~$0.01-$0.03 |
| Content & SEO Battle | 4-8 calls | ~$0.02-$0.08 |
| Market Landscape Map | 6-15 calls | ~$0.05-$0.15 |
| Full Battlecard (1 competitor) | 8-15 calls | ~$0.05-$0.15 |
| Multi-competitor deep dive (3+) | 15-30 calls | ~$0.10-$0.50 |

## Error Handling

| Error / Situation | What to Do |
|------------------|------------|
| Page returns empty or minimal content | Try the fallback command. If that fails too, note "Data unavailable — page may be gated or require authentication." |
| 403 / Access Denied | The page likely requires login. Note this and try alternative sources (e.g., search for third-party coverage). |
| Pipeline timeout | Use `--async` flag, then `bdata status <job-id> --wait --timeout 300`. |
| Pipeline type doesn't exist | Fall back to `bdata scrape [url]` for raw content. |
| No results from search | Broaden the search query. Try different query variations. |
| Rate limit exceeded | Wait briefly and retry, or use `--async` mode. |

## Chaining Commands

The CLI is pipe-friendly. Useful patterns:

```bash
# Search → extract first URL → scrape it
bdata search "[company] pricing" --json | jq -r '.organic[0].link' | xargs bdata scrape

# Get all organic result URLs from a search
bdata search "[query]" --json | jq -r '.organic[].link'

# Pipeline output to file for later analysis
bdata pipelines crunchbase_company "[url]" -o competitor_data.json
```
