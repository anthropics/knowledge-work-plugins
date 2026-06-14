---
name: rates
description: Current-year US federal indexed rates — brackets, 401(k), SS wage base, HSA, FEIE, gift/estate, mileage, 1099-K thresholds.
---

The user wants a specific dollar amount that changes yearly (e.g. 2025 401(k) limit, Social Security wage base, mileage rate, FEIE cap).

Call the `openaccountants` MCP server's `get_rates` tool:

```json
{ "jurisdiction": "US", "tax_year": <year> }
```

Currently supports US federal for 2025 and 2026. Return the figures with a citation to the IRS Revenue Procedure source.

For non-US jurisdictions or specialized rates not in the table, fall back to `get_skill` — the markdown content holds rate tables for every covered jurisdiction.

**Do not** quote rates from your training data. Indexed rates change yearly and your training data is stale.
