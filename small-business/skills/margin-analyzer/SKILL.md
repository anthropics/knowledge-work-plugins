---
name: margin-analyzer
description: >
  Analyzes unit economics by product or service using PayPal merchant
  insights and QuickBooks cost data, benchmarks against inflation and cost
  changes, and shows pricing-scenario data (e.g. "a 5% increase historically
  correlates with ~3% volume drop"). Surfaces analysis only — does not
  recommend a price. Use when the user asks about raising prices, pricing,
  margin analysis, what to charge, whether costs are eating into profit, or
  how a price change might affect their business. Trigger even if the user
  doesn't say "margin" explicitly — phrases like "am I making enough?",
  "should I charge more?", or "my costs are going up" all call for this skill.
---

# Margin Analyzer

> **Status:** MVP draft · **Owner:** JJ · **Version:** 1.1.0
> **Category:** Finance & Ops · **Phase:** V2

## Quick start

When an SMB owner asks "should I raise my prices?" or "are my margins okay?", this skill:

1. **Identifies what to analyze** — which products/services are in scope
2. **Pulls cost data** from QuickBooks (COGS, direct expenses)
3. **Pulls revenue data** from PayPal or Square (transaction history)
4. **Computes unit economics** — revenue, COGS, gross margin, margin % per item
5. **Benchmarks against context** — inflation, cost changes, industry norms if available
6. **Builds pricing scenarios** — shows what happens to revenue and margin at +5%, +10%, +15% price changes, using historical correlation where data allows
7. **Presents the analysis** — no price recommendation; the owner decides

The output equips the owner to make their own pricing call with real data behind it.

---

## Workflow

### Step 1: Pre-flight check

**QuickBooks:** Call `company-info` to verify the industry field is populated. If it's missing or "Unknown", ask: "I need your business category to pull relevant benchmarks. What industry are you in?" Then call `quickbooks-profile-info-update`.

**PayPal:** No pre-flight needed, but PayPal rate-limits on rapid calls — see `reference/gotchas.md`.

**No connectors:** Offer CSV upload as a fallback. The skill can work from exported transaction and expense data. The expected CSV schema is in `reference/csv-schema.md`.

### Step 2: Clarify scope

Ask the owner two questions:

1. **"Which products or services do you want to analyze?"**
   - All of them, or a specific subset?
   - If they say "all," confirm the connector has enough data to be meaningful before pulling everything.

2. **"What metric matters most to you?"**
   - Gross margin (revenue minus direct costs)?
   - Net margin (after all expenses)?
   - Revenue per unit?
   - Their answer shapes how you present the output.

### Step 3: Pull cost data (QuickBooks)

Fetch from QuickBooks using `profit-loss-quickbooks-account`:
- **Date range:** Last 12 months (or full history if less is available)
- **Extract:** Cost of goods sold by product/service line, direct expenses

If QuickBooks isn't connected, ask the owner for:
- A cost breakdown by product/service line (materials, labor, direct delivery costs per item)
- Any known cost changes in the last 6–12 months

If QuickBooks is connected but COGS = $0 across all periods, do not use $0 as the cost input. Surface this to the owner:

> "QuickBooks shows no cost of goods sold recorded for this period. To compute meaningful margins, I need a cost breakdown by product or service line — not a single average for the whole business. For each item you want analyzed, what does it cost you to deliver it? Materials, direct labor, any direct expenses per item. Even rough figures work."

Flag this limitation in the Data Quality Notes section of the final output.

### Step 4: Pull revenue data (PayPal / Square)

Fetch from `list_transactions` (PayPal) or `make_api_request` (Square):
- **Date range:** Match the cost data window (last 12 months)
- **Extract:** Transaction amount, item/service name, date, quantity if available

If you hit PayPal rate limits, pause 30 seconds and retry once. If still blocked, offer: "PayPal is temporarily rate-limited. Want to switch to Square or upload a CSV instead?"

If only one data source is available, note the limitation in the output.

### Step 5: Compute unit economics

For each product/service in scope, calculate:

| Metric | Formula |
|---|---|
| **Revenue** | Sum of transaction amounts for the item |
| **COGS** | Cost data from QB or owner-provided |
| **Gross Profit** | Revenue − COGS |
| **Gross Margin %** | (Gross Profit ÷ Revenue) × 100 |
| **Units Sold** | Count of transactions (if available) |
| **Revenue per Unit** | Revenue ÷ Units Sold |
| **Cost per Unit** | COGS ÷ Units Sold |

Flag any item where margin is below 20% — not as a recommendation, but as a data point worth the owner's attention.

### Step 6: Benchmark

Layer in context to make the numbers meaningful:

- **Inflation:** Note relevant cost trends if discussing input cost increases. Example: "Your input costs rose ~X% over this period while your prices held flat — that compressed margin by Y points."
- **Industry benchmarks:** Use the QuickBooks industry profile to surface rough gross margin norms for their category. See `reference/industry-benchmarks.md`.
- **Historical comparison:** If 24+ months of data is available, compare this year's margins to last year's to surface the trend direction.

Handle low-data gracefully: if fewer than 6 months of transactions exist, omit the elasticity section and note: "You need at least 6 months of pricing history to estimate how volume responds to price changes. I'll show scenario math instead."

### Step 7: Pricing scenarios

Build a table for each product/service showing three price-change scenarios:

| Scenario | New Price | Projected Revenue* | Gross Margin % |
|---|---|---|---|
| +5% | $X | $Y | Z% |
| +10% | $X | $Y | Z% |
| +15% | $X | $Y | Z% |

**How to compute projected revenue:**
- **If 6+ months of history:** Estimate volume response using historical data. If a past price change exists, compute observed elasticity: `Elasticity = % change in volume ÷ % change in price`. Apply that to project volume at the new price.
- **If insufficient history:** Show three volume assumptions (−0%, −5%, −10%) and let the owner pick what seems realistic.

Add a note: *"These are projections based on available data, not guarantees. Actual volume response depends on competition, customer sensitivity, and timing."*

### Step 8: Present the analysis

Structure the output as:

Structure the output with an H2 header showing the business name and date range,
followed by four sections: a Unit Economics Summary table (product/service,
revenue, COGS, gross margin, margin %), a Context and Benchmarking section
(2-4 sentences on inflation, cost shifts, industry norms), Pricing Scenarios
(scenario table per product, or top 3-5 if many), and Data Quality Notes
(flag any limitations such as partial data, missing COGS, or short history).

Keep it factual. Do not say "you should raise prices" or "consider lowering your price." The owner is looking at data to make their own call.

---

## Scope boundary

**This skill surfaces data. It does not recommend a price.**

If the owner asks "so what should I do?" — respond with: "I can show you what the data suggests, but the pricing decision is yours. Would you like me to model any additional scenarios?"

This is intentional. Pricing decisions have real business consequences and depend on context only the owner knows (competitive positioning, customer relationships, cash needs). The skill's job is to make sure they're looking at real numbers when they decide.

---

## Connectors

**Primary:** QuickBooks, PayPal
**Also supported:** Square, Brex · Desktop (CSV/export)

---

## Reference files

- `reference/gotchas.md` — common pitfalls (data gaps, elasticity traps, margin math errors)
- `reference/industry-benchmarks.md` — gross margin ranges by SMB category
- `reference/csv-schema.md` — expected columns when the owner uploads a CSV
- `reference/examples/` — worked scenarios (retail, services, product-based)
