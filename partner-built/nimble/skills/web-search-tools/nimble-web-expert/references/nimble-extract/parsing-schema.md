---
name: nimble-parsing-schema-reference
description: |
  Reference for --parser flag structured extraction. Load when markdown output lacks the specific fields needed.
  Contains: schema and schema_list types, CSS/jsonpath/xpath selectors, text/attr/html extractors,
  post-processors (regex, number, boolean, sequence), results in data.parsing.
---

# Parsing Schema

Docs: https://docs.nimbleway.com/nimble-sdk/web-tools/extract/features/parsing-schema

Structured data extraction using declarative selectors, extractors, and post-processors. Use when you need specific fields as clean structured output rather than free-form markdown.

## Table of Contents

- [CLI flags](#cli-flags)
- [Python SDK](#python-sdk)
- [Parser types](#parser-types)
- [Selector types](#selector-types)
- [Extractors](#extractors)
- [Post-processors](#post-processors)
- [Examples](#examples)
- [When to use structured parsing vs markdown](#when-to-use-structured-parsing-vs-markdown)
- [Notes](#notes)

---

## CLI flags

```bash
--parse              # enable parsing
--parser '{"type": "schema", "fields": {...}}'  # structured extraction schema
```

Without `--parser`, `--parse` returns cleaned markdown/HTML. With `--parser`, it returns structured JSON matching your schema.

## Python SDK

```python
from nimble_python import Nimble

nimble = Nimble()
resp = nimble.extract(
    url="https://example.com/product",
    render=True,
    parse=True,
    parser={
        "type": "schema",
        "fields": {
            "title": {"type": "terminal", "selector": {"type": "css", "css_selector": "h1"}, "extractor": {"type": "text"}},
            "price": {"type": "terminal", "selector": {"type": "css", "css_selector": ".price"}, "extractor": {"type": "text", "post_processor": {"type": "number"}}},
        },
    },
)
print(resp["data"]["parsing"])
# → {"title": "Product Name", "price": 49.99}
```

SDK uses underscores for keys (e.g. `post_processor`, `css_selector`). Pass the `parser` dict directly — no JSON serialization needed.

---

## Parser types

| Type | Output | Use for |
|------|--------|---------|
| `terminal` | Single value | One field |
| `terminal_list` | Array of values | List of same field (e.g. all image URLs) |
| `schema` | Object with named fields | Structured record (e.g. product) |
| `schema_list` | Array of objects | List of records (e.g. search results) |
| `or` | First non-null result | Fallback across multiple selectors |
| `and` | Merged object | Combine results from multiple schemas |
| `const` | Fixed value | Hardcode a field value |

---

## Selector types

| Type | Syntax | Use for |
|------|--------|---------|
| `css` | `{"type": "css", "css_selector": ".class"}` | Standard HTML elements |
| `xpath` | `{"type": "xpath", "path": "//element"}` | XML/HTML navigation, RSS feeds, namespaced XML |
| `json` | `{"type": "json", "path": "nested.key", "coercion_filter": "$[?...]"}` | Embedded JSON, LD+JSON |
| `sequence` | `{"type": "sequence", "sequence": [...]}` | Chain multiple selectors |
| `parent` | `{"type": "parent", "times": 2}` | Traverse DOM upward |
| `root` | `{"type": "root"}` | Access full response (needed for network_capture data) |

---

## Extractors

| Type | Description |
|------|-------------|
| `text` | Text content. Params: `strip` (bool, default true), `separator` (string) |
| `attr` | Attribute value (href, src, data-*, class, id) |
| `json` | JSONPath expression on JSON data |
| `raw` | Return element unchanged (default) |

---

## Post-processors

| Type | Description |
|------|-------------|
| `url` | Resolve relative URLs to absolute |
| `regex` | Pattern match. Params: `pattern`, `group` (capture group index) |
| `format` | String template using `{data}` placeholder |
| `date` | Normalize date format. Params: `format` (e.g. `"%d/%m/%y"`) |
| `boolean` | Convert to true/false via `contains`, `exists`, or `regex` condition. Use `not: true` to negate. |
| `number` | Coerce formatted numbers: "1.5M" → 1500000, "$1,299" → 1299. Params: `locale`, `force_type` ("int"/"float") |
| `country` | Map country name to ISO code |
| `sequence` | Chain multiple post-processors |

---

## Examples

### CLI

```bash
# Single product — extract specific fields
nimble extract --url "https://example.com/product/123" --parse \
  --parser '{
    "type": "schema",
    "fields": {
      "title":  {"type": "terminal", "selector": {"type": "css", "css_selector": "h1.product-title"}, "extractor": {"type": "text"}},
      "price":  {"type": "terminal", "selector": {"type": "css", "css_selector": ".price"}, "extractor": {"type": "text", "post_processor": {"type": "number"}}},
      "rating": {"type": "terminal", "selector": {"type": "css", "css_selector": ".rating-value"}, "extractor": {"type": "text"}}
    }
  }'

# List of products from search results
nimble extract --url "https://example.com/search?q=shoes" --parse \
  --parser '{
    "type": "schema_list",
    "selector": {"type": "css", "css_selector": ".product-card"},
    "fields": {
      "title": {"type": "terminal", "selector": {"type": "css", "css_selector": ".title"}, "extractor": {"type": "text"}},
      "price": {"type": "terminal", "selector": {"type": "css", "css_selector": ".price"}, "extractor": {"type": "text", "post_processor": {"type": "number"}}},
      "url":   {"type": "terminal", "selector": {"type": "css", "css_selector": "a"}, "extractor": {"type": "attr", "attr": "href", "post_processor": {"type": "url"}}}
    }
  }'

# Fallback — try two selectors, use first that works
nimble extract --url "https://example.com/product" --parse \
  --parser '{
    "type": "terminal",
    "selector": {"type": "or", "selectors": [
      {"type": "css", "css_selector": ".price-sale"},
      {"type": "css", "css_selector": ".price-regular"}
    ]},
    "extractor": {"type": "text", "post_processor": {"type": "number"}}
  }'

# Extract all image URLs as a list
nimble extract --url "https://example.com/product" --parse \
  --parser '{
    "type": "terminal_list",
    "selector": {"type": "css", "css_selector": "img.product-image"},
    "extractor": {"type": "attr", "attr": "src", "post_processor": {"type": "url"}}
  }'

# Extract embedded JSON-LD (schema.org)
nimble extract --url "https://example.com/product" --parse \
  --parser '{
    "type": "schema",
    "selector": {"type": "css", "css_selector": "script[type=\"application/ld+json\"]"},
    "fields": {
      "name":  {"type": "terminal", "extractor": {"type": "json", "path": "name"}},
      "price": {"type": "terminal", "extractor": {"type": "json", "path": "offers.price", "post_processor": {"type": "number"}}}
    }
  }'

# Parse RSS feed with XPath
nimble extract --url "https://example.com/feed.xml" --parse \
  --parser '{
    "type": "schema_list",
    "selector": {"type": "xpath", "path": "//item"},
    "fields": {
      "title": {"type": "terminal", "selector": {"type": "xpath", "path": ".//title"}, "extractor": {"type": "text"}},
      "link":  {"type": "terminal", "selector": {"type": "xpath", "path": ".//link"}, "extractor": {"type": "text"}},
      "date":  {"type": "terminal", "selector": {"type": "xpath", "path": ".//pubDate"}, "extractor": {"type": "text", "post_processor": {"type": "date"}}}
    }
  }'

# Extract data from network capture response
nimble extract --url "https://example.com/products" --render \
  --network-capture '[{"url": {"type": "contains", "value": "/api/products"}}]' \
  --parse --parser '{
    "type": "terminal",
    "selector": {"type": "sequence", "sequence": [
      {"type": "root"},
      {"type": "json", "path": "network_capture[0].response_body.data.products"}
    ]},
    "extractor": {"type": "raw"}
  }'
```

### Python SDK

```python
# Single product
resp = nimble.extract(
    url="https://example.com/product/123",
    parse=True,
    parser={
        "type": "schema",
        "fields": {
            "title": {"type": "terminal", "selector": {"type": "css", "css_selector": "h1.product-title"}, "extractor": {"type": "text"}},
            "price": {"type": "terminal", "selector": {"type": "css", "css_selector": ".price"}, "extractor": {"type": "text", "post_processor": {"type": "number"}}},
            "rating": {"type": "terminal", "selector": {"type": "css", "css_selector": ".rating-value"}, "extractor": {"type": "text"}},
        },
    },
)
print(resp["data"]["parsing"])

# List of products from search results
resp = nimble.extract(
    url="https://example.com/search?q=shoes",
    parse=True,
    parser={
        "type": "schema_list",
        "selector": {"type": "css", "css_selector": ".product-card"},
        "fields": {
            "title": {"type": "terminal", "selector": {"type": "css", "css_selector": ".title"}, "extractor": {"type": "text"}},
            "price": {"type": "terminal", "selector": {"type": "css", "css_selector": ".price"}, "extractor": {"type": "text", "post_processor": {"type": "number"}}},
            "url": {"type": "terminal", "selector": {"type": "css", "css_selector": "a"}, "extractor": {"type": "attr", "attr": "href", "post_processor": {"type": "url"}}},
        },
    },
)
for item in resp["data"]["parsing"][:5]:
    print(item)

# All image URLs as a list
resp = nimble.extract(
    url="https://example.com/product",
    parse=True,
    parser={
        "type": "terminal_list",
        "selector": {"type": "css", "css_selector": "img.product-image"},
        "extractor": {"type": "attr", "attr": "src", "post_processor": {"type": "url"}},
    },
)
print(resp["data"]["parsing"])
```

---

## When to use structured parsing vs markdown

| Use `--parser`  | Use `--format markdown` |
|-----------------|------------------------|
| Need specific fields | Need full page content |
| Extracting a list of items | Reading an article or docs |
| Data will be used programmatically | LLM needs to read and summarize |
| Building a dataset | One-off research |

---

## Notes

- Use `or` parser as fallback for pages with varying layouts or A/B tests
- Chain post-processors with `sequence` for multi-step transforms
- Use `root` selector to access `network_capture` data in the parser
- `number` post-processor handles "$1,299", "1.5M", "2,100" automatically
- Selectors break when page structure changes — monitor and update as needed
