# CSV Upload Schema

When the owner doesn't have QuickBooks or PayPal connected, they can upload exported CSV files. This document specifies what columns to expect and how to handle variations.

## Revenue CSV (transactions export)

Expected columns (order doesn't matter; headers are case-insensitive):

| Column | Required | Description |
|---|---|---|
| `date` | Yes | Transaction date (any standard format: YYYY-MM-DD, MM/DD/YYYY, etc.) |
| `item` or `product` or `service` or `description` | Yes | What was sold |
| `amount` or `revenue` or `total` | Yes | Transaction amount (USD) |
| `quantity` or `qty` | No | Units sold — if missing, assume 1 per transaction |

**Exports that typically match this format:**
- PayPal: Activity → Download (CSV) — use "Transaction ID, Date, Name, Type, Status, Currency, Amount"
- Square: Reports → Transactions → Export
- Shopify: Orders → Export

If the export has more columns, ignore the extras. If a required column is missing, ask the owner which column maps to it.

## Cost CSV (expense or COGS export)

Expected columns:

| Column | Required | Description |
|---|---|---|
| `date` | No | Expense date (useful for trend analysis) |
| `item` or `product` or `service` or `category` | Yes | What the cost relates to |
| `amount` or `cost` or `expense` | Yes | Cost amount (USD) |
| `type` | No | COGS vs. operating expense — if absent, ask the owner |

**Exports that typically match this format:**
- QuickBooks: Reports → Profit & Loss Detail → Export
- Brex: Transactions → Export → Filter by expense category

## Handling messy CSVs

Real-world exports are messy. Common issues:

- **Extra header rows:** Skip rows until you find one that looks like column names
- **Currency symbols:** Strip `$`, `,` from numeric fields before parsing
- **Negative refunds:** Include them — they reduce net revenue
- **Mixed currencies:** Flag it and ask which currency to use; default to USD if unclear
- **"Gross" vs "Net" amounts:** Prefer net (after fees) for revenue; ask if unclear

## After loading

Confirm the data shape with the owner before proceeding:
- "I loaded X transactions from [date] to [date] across Y products. Does that look right?"
- If the date range or product count looks off, ask them to double-check the export filters.
