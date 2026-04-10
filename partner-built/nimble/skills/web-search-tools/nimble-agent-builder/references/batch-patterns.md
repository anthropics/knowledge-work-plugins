# Batch Patterns

Patterns for processing multiple inputs, comparing across stores, and normalizing output.

## Table of Contents

- [When to use batch patterns](#when-to-use-batch-patterns)
- [Multi-store comparison walkthrough](#multi-store-comparison-walkthrough)
- [Normalization and unified schema](#normalization-and-unified-schema)
- [Interactive batch extraction](#interactive-batch-extraction)

---

## When to use batch patterns

| Scenario | Path | Pattern |
|----------|------|---------|
| 2–5 URLs, display output | Interactive | Run `nimble agent run` per URL via CLI, aggregate results |
| 6+ URLs or file output | Codegen | Generate SDK script with `asyncio.gather` or async pipeline |
| Multi-store comparison | Codegen | Generate script with per-store normalization + merged output |
| Batch input file (URLs/IDs) | Codegen | Read file, generate async pipeline script |
| 50+ items per store | Codegen | Async batch pipeline (`/v1/agent/async` + poll) |

**Routing rule:** The interactive batch approach (CLI runs) works for small batches (~2–5 items). Beyond that, route to codegen — generate a script using templates from `sdk-patterns.md` (Python) or `rest-api-patterns.md` (other languages).

---

## Multi-store comparison walkthrough

End-to-end example of the codegen path for a multi-store comparison request.

### Scenario

User request: *"Compare prices for wireless headphones on Amazon and Walmart, save results to comparison.csv"*

### Step 1 — Route to codegen

| Signal | Value | Evidence |
|--------|-------|----------|
| Execution mode | `codegen` | Multi-store comparison + CSV output |
| Output format | `csv` | "save results to comparison.csv" |
| Stores | Amazon, Walmart | "on Amazon and Walmart" |
| Target type | `search` | "wireless headphones" is a keyword |
| Language | Python | Default — no project files detected |

### Step 2 — Agent discovery (parallel)

Search for agents for both stores simultaneously:

```bash
export PATH="$HOME/go/bin:$PATH"
nimble agent list --limit 100   # filter results for "amazon" and "walmart" locally
```

Results: found `amazon_serp` and `walmart_serp`. On the codegen path with clear matches, narrate the agent choice without presenting options — the user reviews the generated code.

### Step 3 — Get schemas (parallel)

Run `nimble agent get --template-name` for both agents (CLI). Extract key schema details:

| Agent | Required input | Key output fields |
|-------|---------------|-------------------|
| `amazon_serp` | `keyword` (string) | `product_name`, `price`, `rating`, `review_count` |
| `walmart_serp` | `keyword` (string) | `product_name`, `product_price`, `product_rating`, `product_reviews_count` |

Note the field name differences — the generated script must normalize these.

### Step 4 — Infer language

Check the project for language signals. No project files detected → default to **Python**. Only ask if conflicting signals exist.

### Step 5 — Generate script

This request involves 2 agents. Per the routing table in `sdk-patterns.md` > "When to use async vs sync": 2–3 agents → batch sync template (`asyncio.gather` + `/v1/agent`).

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["nimble_python"]
# ///
"""Compare wireless headphone prices: Amazon vs Walmart."""
import asyncio, csv, os
from nimble_python import AsyncNimble

nimble = AsyncNimble(api_key=os.environ["NIMBLE_API_KEY"], max_retries=4, timeout=120.0)
SEM = asyncio.Semaphore(10)


async def run_agent(agent: str, params: dict):
    async with SEM:
        return await nimble.agent.run(agent=agent, params=params)


def normalize(store: str, record: dict) -> dict:
    """Map store-specific fields to a common schema."""
    if store == "Amazon":
        return {
            "store": "Amazon",
            "product_name": record.get("product_name", ""),
            "price": record.get("price"),
            "rating": record.get("rating"),
            "review_count": record.get("review_count"),
        }
    return {
        "store": "Walmart",
        "product_name": record.get("product_name", ""),
        "price": record.get("product_price"),
        "rating": record.get("product_rating"),
        "review_count": record.get("product_reviews_count"),
    }


async def main():
    results = await asyncio.gather(
        run_agent("amazon_serp", {"keyword": "wireless headphones"}),
        run_agent("walmart_serp", {"keyword": "wireless headphones"}),
        return_exceptions=True,
    )

    rows = []
    for (store, resp) in zip(["Amazon", "Walmart"], results):
        if isinstance(resp, Exception):
            print(f"  {store} failed: {resp}")
            continue
        parsing = resp.data.parsing
        if isinstance(parsing, list):
            # SERP items are typed Pydantic objects — must call .model_dump() before passing to normalize()
            rows.extend(normalize(store, r.model_dump()) for r in parsing)

    # Deduplicate by (store, product_name)
    seen, unique = set(), []
    for row in rows:
        key = (row["store"], row["product_name"])
        if key not in seen:
            seen.add(key)
            unique.append(row)

    if unique:
        with open("comparison.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=unique[0].keys())
            w.writeheader()
            w.writerows(unique)
        print(f"Wrote {len(unique)} products to comparison.csv")

    await nimble.close()

asyncio.run(main())
```

### Step 6 — Present and execute

Use `AskUserQuestion` to confirm execution, then run via `uv run comparison.py`.

### Variations

**TypeScript project:** Infer TypeScript/Node from `package.json`/`tsconfig.json`. Use REST API `POST /v1/agent` with `Promise.all`. See `rest-api-patterns.md`.

**Large scale (50+ items per store):** Use the async batch pipeline template (`POST /v1/agent/async` + poll). See `sdk-patterns.md` > "Async Agent Endpoint".

---

## Normalization and unified schema

When comparing data across multiple agents, normalize output fields to a single unified schema.

### When to apply

- Multi-source comparison (2+ agents whose `skills` output fields differ)
- Aggregation from different agents into a single CSV/table
- Any request combining results that need a consistent structure

If all agents share identical field names, skip normalization.

### Strategy

1. Run `nimble agent get --template-name <agent>` (CLI) for each agent to read `skills` (output fields).
2. Compare field names across schemas — identify semantically equivalent fields.
3. Choose unified field names for the merged output.
4. Build a mapping function per agent: `{unified_name: agent_specific_name}`.
5. Apply the mapping after each agent run, before merging results. Each record gets a `store`/`source` label.

### Normalization function template

#### Python

```python
def make_normalizer(store: str, field_map: dict[str, str]):
    """Create a normalizer from a field mapping."""
    def normalize(record: dict) -> dict:
        return {"store": store, **{
            unified: record.get(agent_field, "")
            for unified, agent_field in field_map.items()
        }}
    return normalize

# Example:
amazon_norm = make_normalizer("Amazon", {
    "product_name": "product_name",
    "price": "price",
    "rating": "rating",
    "review_count": "review_count",
})

walmart_norm = make_normalizer("Walmart", {
    "product_name": "product_name",
    "price": "product_price",
    "rating": "product_rating",
    "review_count": "product_reviews_count",
})
```

### Deduplication

After normalization, deduplicate by a composite key — typically `(store, product_name)`:

```python
seen, unique = set(), []
for row in rows:
    key = (row["store"], row["product_name"])
    if key not in seen:
        seen.add(key)
        unique.append(row)
```

Choose the composite key based on what uniquely identifies a record. For search results, `(store, product_name)`. For detail pages, `(store, url)` may be better.

### Dynamic normalization

When agents are discovered at runtime (not hardcoded), build the field mapping dynamically:

1. Read the `skills` dict from each agent via `nimble agent get --template-name` (CLI).
2. For each unified field, search the agent's properties for a matching or similar name.
3. Use exact matches first, then fall back to substring/suffix matching:
   - `price` matches `price`, `product_price`, `web_price`
   - `rating` matches `rating`, `product_rating`, `average_of_reviews`
4. If no match is found, omit the field for that agent (use empty string).

---

## Interactive batch extraction

Pattern for running an agent against several URLs via CLI commands and aggregating results.

### When to use

Small batches (2–5 URLs) where running `nimble agent run` per URL via CLI is practical. For larger batches, route to codegen instead.

### Walkthrough

**Scenario:** Extract product details from five Amazon product pages using `amazon-product-details`.

**1. Confirm the agent** — run `nimble agent get --template-name amazon-product-details` (CLI) to verify the agent and inspect input schema.

**2. Prepare the URL list** — define the set of URLs to process.

**3. Run per URL** — run `nimble agent run` once per URL (CLI):

```bash
export PATH="$HOME/go/bin:$PATH"
nimble --transform "data.parsing" agent run --agent amazon-product-details \
  --params '{"url": "https://www.amazon.com/dp/B0DGHRT7PS"}'
```

**4. Handle errors gracefully** — if a run returns an error for one URL, log it and continue. Do not abort the entire batch.

**5. Aggregate into a summary table:**

| Field | Value |
|-------|-------|
| Agent | `amazon-product-details` |
| URLs processed | 5 |
| Successful | 4 |
| Failed | 1 |

| # | Title | Price | Rating | Availability | Source URL |
|---|-------|-------|--------|--------------|-----------|
| 1 | Wireless Headphones Pro | $79.99 | 4.6 | In Stock | .../B0DGHRT7PS |
| 2 | USB-C Charging Hub | $34.99 | 4.3 | In Stock | .../B0CX23V2ZK |

**Failed URLs:**

| # | URL | Error |
|---|-----|-------|
| 1 | .../B0BT9CXXXX | Page not found or access denied |

### Multi-parameter agents

Some agents accept more than just a URL (e.g., `url` + `query`). Iterate over different parameter combinations and add a column for the varying parameter in the summary table.

### Routing to codegen

For 6+ URLs, file-based output, or multi-store comparisons, route to codegen. Generate a script using the async batch pipeline from `sdk-patterns.md`.

## Key takeaways

- Codegen triggers when: scale >50, file output, multi-store, batch input, or explicit request.
- Language is inferred from project files, not asked.
- Field normalization is needed when comparing across stores with different schemas.
- Interactive batch works for 2–5 items; beyond that, generate a script.
- Always deduplicate merged results by a composite key.
- Handle individual failures without aborting the batch.
