# Square integration (future enhancement)

Square is listed as an optional connector for content-strategy, but the full integration path is not yet implemented. This document outlines what's needed.

## Current state

- Square is named in `reference/connectors` but not fully wired into the workflow
- QuickBooks and PayPal are the primary, tested paths

## What needs to happen

### 1. Location ID discovery

Square organizations can have multiple locations. Before pulling orders, we need to:

1. Call `make_api_request` with `service="locations"` and `method="list"` to discover available locations
2. Ask user: "Which location(s) should I analyze?" (or default to primary)
3. Fetch location ID(s) for subsequent calls

### 2. Order fetching

For each location ID:

```
Call list_orders with:
- location_id: <from step 1>
- begin_time: <90 days ago, ISO 8601>
- end_time: <now, ISO 8601>
- sort_order: "DESC"
```

Extract:
- Order date
- Line items (product name, quantity, price)
- Total revenue per order

### 3. Categorization

Square orders may not have explicit "product" or "service" taxonomy — items live in catalog. Correlate line items to catalog entries to extract product names and categories.

## Why it's stubbed

1. **No test account** — would need a Square merchant account to validate end-to-end
2. **Catalog complexity** — Square's catalog model is more flexible than QuickBooks and adds surface area for errors
3. **Location multiplicity** — QuickBooks and PayPal have simpler single-account models; Square requires user to pick a location

## How to implement

1. Obtain a Square sandbox/test account
2. Write scenarios for single-location and multi-location merchants
3. Add `reference/square-orders-example.md` with worked example
4. Update SKILL.md workflow to include Square as co-equal path (not just "also supported")
5. Run through scenarios with a Square user before shipping

## Time estimate

~4 hours for discovery + implementation + testing, assuming a test account is available.
