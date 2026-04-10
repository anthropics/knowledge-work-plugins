---
name: nimble-recipes-reference
description: |
  Production-tested nimble commands for common sites. Load for proven extraction patterns.
  Contains: any page (markdown default), Amazon product/search, Yelp, Target (network capture),
  public APIs/XHR, docs/static pages, LinkedIn jobs, Google search and maps,
  research workflow (search→extract), docs site (map→extract), bulk parallel extraction.
---

# Proven recipes — reference

Production-tested extract commands for common sites. Copy, swap the URL/params, present results.

## Any page — markdown (default)

```bash
mkdir -p .nimble
nimble --transform "data.markdown" extract \
  --url "https://example.com/any-page" --format markdown > .nimble/page.md
head -100 .nimble/page.md
```
Works for articles, docs, blogs. If empty → add `--render`. Still empty → add `--render --driver vx10-pro`.

---

## Amazon

### Product page (PDP)
```bash
nimble agent run --agent amazon_pdp --params '{"asin": "B0CHWRXH8B"}' > .nimble/amazon-pdp.json
python3 -c "import json; d=json.load(open('.nimble/amazon-pdp.json')); p=d['data']['parsing']; print(p.get('product_title'), p.get('web_price'), p.get('average_of_reviews'))"
```

### Search results
```bash
nimble agent run --agent amazon_serp --params '{"keyword": "wireless headphones"}' > .nimble/amazon-serp.json
python3 -c "
import json
items = json.load(open('.nimble/amazon-serp.json'))['data']['parsing']
for i in items[:10]:
    print(f\"{(i.get('product_name') or '?')[:55]:55s}  \${i.get('price','?'):>7}  {i.get('asin','')}\")
"
```

### Manual extract (if agent unavailable)
> ⚠ CSS selectors may break on Amazon redesigns. Prefer the `amazon_pdp` agent when available.
```bash
nimble extract --url "https://www.amazon.com/dp/B0CHWRXH8B" --country US --parse \
  --parser '{
    "type": "schema",
    "fields": {
      "product_title": {"type": "terminal", "selector": {"type": "css", "css_selector": "#productTitle"}, "extractor": {"type": "text"}},
      "web_price": {"type": "terminal", "selector": {"type": "css", "css_selector": "[name=\"items[0.base][customerVisiblePrice][amount]\"]"}, "extractor": {"type": "attr", "attr": "value"}},
      "average_of_reviews": {"type": "terminal", "selector": {"type": "css", "css_selector": ".reviewCountTextLinkedHistogram a > span"}, "extractor": {"type": "text"}},
      "asin": {"type": "terminal", "selector": {"type": "css", "css_selector": "#ASIN"}, "extractor": {"type": "attr", "attr": "value"}}
    }
  }' | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('data',{}).get('parsing',{}), indent=2))"
```

---

## Yelp

### Via agent
```bash
nimble agent run --agent yelp_serp \
  --params '{"search_query": "italian restaurant", "location": "San Francisco, CA"}' > .nimble/yelp.json
python3 -c "
import json
items = json.load(open('.nimble/yelp.json'))['data']['parsing']
for i in items[:10]:
    print(f\"{i.get('business_name','?')[:40]:40s} {i.get('business_rating','?'):>4s}\")
"
```

### Manual extract (v0.5.0+)
> ⚠ CSS selectors may break on Yelp redesigns. Prefer the `yelp_serp` agent when available.
```bash
nimble extract \
  --url "https://www.yelp.com/search?find_desc=italian+restaurant&find_loc=San+Francisco%2C+CA" \
  --render --country US --locale en-US \
  --browser-action '[
    {"type": "wait_for_element", "selector": "[data-traffic-crawl-id=OrganicBusinessResult]", "timeout": 30000},
    {"type": "scroll", "to": "[role=navigation]"},
    {"type": "wait", "duration": "5s"}
  ]' \
  --render-options '{"userbrowser": true}' --parse \
  --parser '{
    "type": "schema_list",
    "selector": {"type": "css", "css_selector": "[data-testid=serp-ia-card]"},
    "fields": {
      "business_name": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-traffic-crawl-id=SearchResultBizName] a"}, "extractor": {"type": "text"}},
      "business_rating": {"type": "terminal", "selector": {"type": "css", "css_selector": "[data-traffic-crawl-id=SearchResultBizRating] span[data-font-weight]"}, "extractor": {"type": "text"}}
    }
  }' > .nimble/yelp-results.json
```

---

## Target

> ⚠ CSS selectors may break on Target redesigns. If a Target agent becomes available, prefer it.
```bash
nimble extract \
  --url "https://www.target.com/p/-/A-88790928" \
  --render --driver vx8-pro --country US \
  --browser-action '[
    {"type": "wait_for_element", "selector": "#above-the-fold-information", "timeout": 10000},
    {"type": "wait", "duration": "15s"}
  ]' \
  --render-options '{"timeout": 60000}' \
  --network-capture '[
    {"url": {"type": "contains", "value": "/web/pdp_client_v1"}, "validation": false, "wait_for_requests_count": 1}
  ]' --format markdown > .nimble/target-product.json
head -80 .nimble/target-product.json
```

---

## Public APIs / XHR

```bash
# Polymarket
nimble --transform "data.markdown" extract \
  --url "https://gamma-api.polymarket.com/markets?_q=elections&limit=20&active=true" \
  --is-xhr --format markdown

# Any known JSON API
nimble --transform "data.markdown" extract \
  --url "https://api.example.com/v1/endpoint?param=value" \
  --is-xhr --format markdown
```

---

## Docs / static pages

```bash
nimble --transform "data.markdown" extract \
  --url "https://react.dev/reference/rsc/server-components" --format markdown > .nimble/react-docs.md
head -80 .nimble/react-docs.md
```

---

## LinkedIn jobs

```bash
nimble --transform "data.markdown" extract \
  --url "https://www.linkedin.com/jobs/search/?keywords=data+scientist&location=Austin%2C+TX&f_TPR=r604800" \
  --render --driver vx10-pro --format markdown > .nimble/linkedin-jobs.md
head -100 .nimble/linkedin-jobs.md
```

---

## Google search & maps

```bash
# Google search via agent
nimble agent run --agent google_search --params '{"query": "OpenAI news 2026"}' | python3 -c "
import json, sys
entities = json.load(sys.stdin)['data']['parsing']['entities']
for r in entities.get('OrganicResult', [])[:5]:
    print(r.get('title'), '|', r.get('link'))
"

# Google Maps
nimble agent run --agent google_maps_search --params '{"query": "italian restaurants NYC"}' > .nimble/maps.json
```

---

## Research workflow

```bash
# Search → extract top results
nimble search --query "React server components best practices" --focus coding --search-depth lite --include-answer
nimble --transform "data.markdown" extract --url "https://react.dev/reference/rsc/server-components" --format markdown
```

---

## Docs site (map → selective extract)

```bash
nimble --transform "links.#.url" map --url "https://docs.stripe.com" --limit 200 > .nimble/stripe-urls.txt
grep "charges\|refund" .nimble/stripe-urls.txt
nimble --transform "data.markdown" extract --url "https://docs.stripe.com/api/charges/object" --format markdown
```
