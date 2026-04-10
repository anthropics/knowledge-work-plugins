# Site Analysis Guide

A step-by-step playbook for analyzing any website before building a scraper. This phase is critical — spending time here prevents hours of debugging fragile selectors later.

---

## Table of Contents

- [Step 1: Initial Page Fetch](#step-1-initial-page-fetch)
- [Step 2: Content Rendering Detection](#step-2-content-rendering-detection)
- [Step 3: Hidden API Discovery](#step-3-hidden-api-discovery)
- [Step 4: Selector Strategy](#step-4-selector-strategy)
- [Step 5: Pagination Analysis](#step-5-pagination-analysis)
- [Step 6: Anti-Bot Assessment](#step-6-anti-bot-assessment)
- [Step 7: Final Decision Matrix](#step-7-final-decision-matrix)

---

## Step 1: Initial Page Fetch

Start by fetching the target page through Web Unlocker to get the raw HTML the server returns.

```python
import requests
import os

API_KEY = os.environ["BRIGHTDATA_API_KEY"]
ZONE = os.environ["BRIGHTDATA_UNLOCKER_ZONE"]

# Fetch raw HTML
response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"zone": ZONE, "url": TARGET_URL, "format": "raw"}
)
html = response.text

# Also fetch as markdown for a quick readable overview
md_response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"zone": ZONE, "url": TARGET_URL, "format": "raw", "data_format": "markdown"}
)
markdown = md_response.text
```

**What to look for in the raw HTML:**
- Is the actual content (product names, prices, text) present in the HTML?
- Or is the HTML mostly empty containers waiting for JavaScript to fill them?

---

## Step 2: Content Rendering Detection

Determine if the site renders content server-side (SSR) or client-side (CSR).

### Signs of Server-Side Rendering (Web Unlocker is sufficient)
- The data you need appears directly in the raw HTML
- Product names, prices, descriptions are visible in the source
- The HTML contains `<meta>` tags with structured data (good SEO sites do this)
- JSON-LD blocks (`<script type="application/ld+json">`) contain structured product/article data

### Signs of Client-Side Rendering (Browser API needed)
- The HTML body is mostly empty: `<div id="root"></div>` or `<div id="__next"></div>`
- Large JavaScript bundles are referenced but content isn't in the HTML
- Framework markers: `ng-app`, `data-reactroot`, `data-v-` (Vue), `__NUXT__`
- The HTML contains loading skeletons or placeholder text

### Hybrid / SSR with Hydration
Many modern sites (Next.js, Nuxt) do SSR + client hydration. The initial HTML contains the content (so Web Unlocker works), but the page also loads JS for interactivity. For these sites, Web Unlocker is the right choice — you get the data without the browser overhead.

**How to confirm:** If you see the data in the raw HTML AND you see framework scripts, it's SSR with hydration. Web Unlocker is fine.

### JSON-LD Extraction (The Hidden Goldmine)

Many e-commerce and content sites embed structured data in JSON-LD format for SEO. This is often the cleanest data source — already structured, no selector parsing needed.

```python
from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(html, "html.parser")
for script in soup.select('script[type="application/ld+json"]'):
    try:
        data = json.loads(script.string)
        print(json.dumps(data, indent=2))
    except (json.JSONDecodeError, TypeError):
        continue
```

Common JSON-LD types you'll find:
- `Product` — name, price, description, image, brand, availability, reviews
- `Article` / `NewsArticle` — headline, author, datePublished, description
- `Organization` — name, address, phone, social profiles
- `BreadcrumbList` — navigation path (useful for category/hierarchy)
- `ItemList` — collections of items on listing pages

---

## Step 3: Hidden API Discovery

Many modern websites fetch their data from internal APIs. Finding and using these endpoints directly is often the cleanest approach — structured JSON with no HTML parsing.

### Where to look in the HTML

1. **`__NEXT_DATA__` (Next.js sites):**
   ```python
   next_data_script = soup.select_one('script#__NEXT_DATA__')
   if next_data_script:
       data = json.loads(next_data_script.string)
       # The page's props are in data["props"]["pageProps"]
       page_data = data["props"]["pageProps"]
   ```

2. **`__NUXT__` or `window.__NUXT__` (Nuxt.js sites):**
   Look for `<script>window.__NUXT__=` in the HTML.

3. **Embedded state objects:**
   Search the HTML for patterns like:
   - `window.__INITIAL_STATE__`
   - `window.__PRELOADED_STATE__`
   - `window.__APP_STATE__`
   - `window.__data`

4. **API URLs in script bundles:**
   Search the HTML for patterns like `"/api/"`, `"graphql"`, or the site's API subdomain.

### Using Web Unlocker to Hit APIs Directly

Once you find an API endpoint, fetch it directly — this is faster and cheaper than parsing HTML:

```python
# Example: hitting a discovered API endpoint
api_data = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "zone": ZONE,
        "url": "https://target-site.com/api/products?category=electronics&page=1",
        "format": "raw"
    }
)
products = json.loads(api_data.text)
```

---

## Step 4: Selector Strategy

When you need to parse HTML, choosing the right selectors is the most important decision for scraper longevity.

### Selector Reliability Ranking (Best → Worst)

1. **Data attributes** — `[data-testid="product-price"]`, `[data-product-id]`
   - Created specifically for testing/automation
   - Survive visual redesigns
   - Rarely change in refactors

2. **Semantic data attributes** — `[data-price]`, `[data-sku]`, `[itemprop="price"]`
   - Carry semantic meaning tied to the business data
   - `itemprop` attributes are Schema.org microdata — very stable

3. **Aria/role attributes** — `[role="listitem"]`, `[aria-label="Price"]`
   - Accessibility attributes are stable (removing them breaks screen readers)

4. **Specific class names** — `.product-card`, `.price-amount`
   - Good when class names are semantic (describe content, not style)
   - Less reliable with CSS-in-JS (e.g., `.css-1a2b3c` changes every build)

5. **ID selectors** — `#product-details`, `#price-section`
   - Unique, but many modern frameworks don't use IDs
   - Often auto-generated and unstable

6. **Structural selectors** — `div > span:nth-child(2)`, `table tr td:last-child`
   - Most fragile — breaks if any element is added/removed
   - Use only as last resort and add defensive checks

### Identifying CSS-in-JS (Unreliable Class Names)

If you see class names like these, do NOT rely on them:
- `css-1a2b3c`, `sc-bZQynM`, `jss123` (CSS Modules / styled-components / JSS)
- `_1Fk2e`, `_3xM2T` (CSS Modules with hash)
- Single-character or random-looking names

Instead, look for:
- Parent elements with semantic classes
- Data attributes on the same or nearby elements
- Text content matching (find elements by their visible text)

### Building Robust Selectors

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# GOOD: Data attribute
price = soup.select_one('[data-testid="product-price"]')

# GOOD: Schema.org microdata
price = soup.select_one('[itemprop="price"]')

# GOOD: Semantic class with parent context
price = soup.select_one('.product-details .price')

# OK: Class name that looks semantic
price = soup.select_one('.product-price')

# BAD: Structural selector (fragile)
price = soup.select_one('.product-card > div:nth-child(3) > span')

# BAD: CSS-in-JS class (will break on next deploy)
price = soup.select_one('.css-1xk2y3z')
```

### Defensive Extraction Pattern

Always wrap individual field extraction so one missing field doesn't crash the scraper:

```python
def safe_text(element, selector: str, default: str = "") -> str:
    """Safely extract text from a child element."""
    el = element.select_one(selector)
    return el.get_text(strip=True) if el else default

def safe_attr(element, selector: str, attr: str, default: str = "") -> str:
    """Safely extract an attribute from a child element."""
    el = element.select_one(selector)
    return el.get(attr, default) if el else default

# Usage
for card in soup.select(".product-card"):
    product = {
        "name": safe_text(card, ".product-title"),
        "price": safe_text(card, ".product-price"),
        "image": safe_attr(card, "img", "src"),
        "url": safe_attr(card, "a", "href"),
    }
```

---

## Step 5: Pagination Analysis

Look at the page to understand how pagination works.

### What to Look For

1. **URL parameters:** Check if the URL changes with pages:
   - `?page=2`, `?p=2` — numbered pagination
   - `?offset=20`, `?skip=20` — offset-based
   - `?cursor=abc123` — cursor-based (common in APIs)
   - `?start=20` — start-index based

2. **HTML pagination controls:**
   ```python
   # Look for pagination elements
   pagination = soup.select_one('.pagination, .pager, nav[aria-label*="pagination"]')
   if pagination:
       links = pagination.select('a')
       for link in links:
           print(link.get_text(strip=True), link.get('href'))
   ```

3. **"Load More" buttons:** The page has a button that fetches more items — this usually means an API call you can replicate directly, or you need Browser API to click it.

4. **Infinite scroll:** No pagination controls at all; content loads on scroll. Check for:
   - `IntersectionObserver` patterns in scripts
   - Event listeners on scroll events
   - The page only showing a subset of items initially

5. **Total count indicators:** Look for text like "Showing 1-20 of 1,234 results" — this tells you total pages and current position.

### Pagination Decision

| What You See | Strategy |
|-------------|----------|
| URL changes with `?page=N` | Iterate URLs with Web Unlocker |
| "Next" link in HTML | Follow links with Web Unlocker |
| "Load More" button triggering API call | Hit the API directly with Web Unlocker |
| "Load More" button with no visible API | Browser API — click the button |
| Infinite scroll | Browser API — scroll and collect |
| API with cursor/token pagination | Hit API directly, pass cursor |

---

## Step 6: Anti-Bot Assessment

Determine how aggressively the site blocks scrapers.

### Low Protection (Web Unlocker handles easily)
- Standard websites, blogs, news sites
- Sites with basic rate limiting
- Sites that serve content to search engine crawlers

### Medium Protection (Web Unlocker usually works)
- E-commerce sites with bot detection
- Sites behind Cloudflare, Akamai, PerimeterX
- Web Unlocker's auto-bypass handles most of these

### High Protection (May need Browser API)
- Sites requiring JavaScript execution for content
- Sites with behavior-based bot detection (mouse movement, scroll patterns)
- Sites with aggressive fingerprinting
- Sites that require solving multiple CAPTCHAs

**How to tell:** If Web Unlocker returns the full content, it's sufficient. If it returns empty pages, blocked messages, or CAPTCHA pages, escalate to Browser API.

---

## Step 7: Final Decision Matrix

After completing your analysis, use this matrix:

| Content in HTML? | Interaction needed? | API endpoint found? | → Use |
|:-:|:-:|:-:|---|
| Yes | No | No | **Web Unlocker** + HTML parsing |
| Yes | No | Yes | **Web Unlocker** → API endpoint (preferred) |
| No | No | Yes | **Web Unlocker** → API endpoint |
| No | No | No | **Browser API** (JS rendering needed) |
| — | Yes (click/scroll) | No | **Browser API** |
| — | Yes (infinite scroll) | Yes | **Web Unlocker** → API (replicate scroll endpoint) |
| — | Yes (infinite scroll) | No | **Browser API** + scroll automation |
