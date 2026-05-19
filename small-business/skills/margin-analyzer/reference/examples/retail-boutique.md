# Example: Retail Boutique — Apparel

**Business:** Small women's clothing boutique, brick-and-mortar + Shopify
**Connectors:** QuickBooks (costs), PayPal (online sales)
**Data:** 14 months of transactions

---

## What the owner asked

"My wholesale costs have gone up a lot this year. I feel like I need to raise prices but I don't want to lose customers. Can you look at my margins?"

---

## Step 1: Pre-flight

`company-info` returns Industry: "Retail — Apparel". Pre-flight passes.

---

## Step 2: Scope clarification

Owner wants to analyze her top 5 SKU categories:
- Dresses
- Tops
- Denim
- Accessories
- Knitwear

Metric priority: gross margin % (she wants to understand profitability, not just revenue).

---

## Step 3–4: Data pulled

- **QuickBooks:** 14 months of COGS by product category
- **PayPal:** 14 months of transaction history (online sales only; in-store via Square separately)

---

## Step 5: Unit economics output

| Category | Revenue | COGS | Gross Profit | Margin % |
|---|---|---|---|---|
| Dresses | $42,800 | $18,200 | $24,600 | 57.5% |
| Tops | $31,500 | $15,100 | $16,400 | 52.1% |
| Denim | $18,900 | $11,300 | $7,600 | 40.2% |
| Accessories | $9,400 | $2,800 | $6,600 | 70.2% |
| Knitwear | $14,200 | $9,600 | $4,600 | 32.4% ⚠️ |

⚠️ Knitwear is flagged: 32.4% is below the 40–55% typical range for apparel retail.

---

## Step 6: Benchmarking

"For apparel retail, typical gross margins run 45–65%. Your portfolio average is 51%, which is within range. However, Knitwear at 32.4% is below the floor — this could indicate that wholesale costs for knitwear rose faster than your prices over the past year. Your overall cost base rose approximately 12% year over year, while revenue grew 7% — that 5-point gap is where the margin pressure is coming from."

---

## Step 7: Pricing scenarios — Knitwear (low-margin item)

Current average Knitwear price: $89. Current cost: ~$61.

| Scenario | New Price | Est. Revenue* | Gross Margin % |
|---|---|---|---|
| +5% ($93) | $93 | ~$14,560 (−3% vol) | 34.4% |
| +10% ($98) | $98 | ~$14,130 (−6% vol) | 37.8% |
| +15% ($102) | $102 | ~$13,700 (−8% vol) | 40.2% |

*Volume estimates based on 14-month elasticity: historical data shows ~0.6 volume drop per 1% price increase for this category.

Note: "These projections use your 14-month history as a guide. Actual response depends on your customers and what competitors are charging for similar items."

---

## Step 8: What was presented

The owner received the full unit economics table, the benchmarking paragraph, and the knitwear scenario table. She noted that Accessories was the standout performer (70% margin). The analysis did not recommend a course of action — it surfaced that knitwear was the category most worth evaluating for a price adjustment.

---

## Notes for skill author

- This example shows graceful handling of mixed data sources (PayPal online + Square in-store noted as limitation)
- Elasticity was computable because the owner had raised Knitwear prices once 8 months ago (from $79 → $89) and volume dipped 5% the following month — that's the one-data-point limitation referenced in gotchas.md
