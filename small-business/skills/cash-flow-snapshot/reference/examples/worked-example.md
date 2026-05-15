# Worked example — cash-flow-snapshot

**Scenario:** Small services business. QuickBooks + PayPal connected. Three
active customers, monthly payroll, office rent.

---

## Input data (pulled from connectors)

**AR aging (QuickBooks):**

| Customer       | Invoice | Amount   | Due Date   | Days Outstanding |
|----------------|---------|----------|------------|------------------|
| Acme Corp      | INV-112 | $8,400   | Apr 10     | 12               |
| BlueSky LLC    | INV-108 | $14,200  | Apr 22     | 0                |
| Crestwood Inc  | INV-115 | $6,000   | May 5      | —                |

**Historical payment lag (from PayPal settlements):**

| Customer       | Mean Lag | Std Dev | Payments on Record |
|----------------|----------|---------|--------------------|
| Acme Corp      | 18 days  | 4 days  | 11                 |
| BlueSky LLC    | 7 days   | 2 days  | 8                  |
| Crestwood Inc  | 12 days  | 5 days  | 6                  |

**Fixed costs (QuickBooks recurring AP):**
- Payroll: $22,000 — hits April 15
- Rent: $3,200 — hits May 1
- Software subscriptions: $480 — hits May 1

---

## Step 3 output — adjusted inflow dates

| Customer       | Invoice Amount | Adj. Receipt Date | Notes                             |
|----------------|---------------|-------------------|-----------------------------------|
| Acme Corp      | $8,400        | Apr 28            | Due Apr 10 + 18-day mean lag      |
| BlueSky LLC    | $14,200       | Apr 29            | Due Apr 22 + 7-day mean lag       |
| Crestwood Inc  | $6,000        | May 17            | Due May 5 + 12-day mean lag       |

---

## Step 4 output — 30/60/90 forecast

Confidence band calculation:
- Weighted avg stddev: 3.6 days
- Weighted avg mean lag: 12.7 days
- band_pct = 3.6 / 12.7 = **28.3%**

| Window  | Expected Inflows | Expected Outflows | Net      | Low (−28%) | High (+28%) |
|---------|-----------------|-------------------|----------|------------|-------------|
| 0–30d   | $22,600         | $22,000           | +$600    | −$5,928    | +$7,128     |
| 31–60d  | $6,000          | $3,680            | +$2,320  | +$1,670    | +$2,970     |
| 61–90d  | $0              | $0                | $0       | —          | —           |

---

## Step 5 output — risks flagged

1. **Payroll crunch:** Payroll ($22,000) hits April 15. Low-band inflows through
   April 14: $0 (both AR receipts fall April 28–29). Shortfall risk: up to $22,000.
   *Recommend: confirm receivables timing with Acme and BlueSky before April 14.*

2. **Late-payer risk:** Acme Corp historically pays 18 days late. Their $8,400
   invoice (due Apr 10) shifts to April 28 — after payroll.

---

## Step 6 output — chat summary

```
Cash Flow Snapshot — Apr 23 → Jul 21, 2026
Sources: QuickBooks, PayPal

              Expected    Low        High
30-day net:   +$600      −$5,928    +$7,128
60-day net:   +$2,320    +$1,670    +$2,970
90-day net:   $0         —          —

⚠ 2 risks flagged:
  • Payroll crunch: $22K payroll hits Apr 15; AR receipts don't clear until
    Apr 28–29. Low-band shortfall risk: up to $22,000.
  • Late-payer: Acme Corp (mean 18-day lag) shifts $8,400 past payroll date.

Confidence band: ±28% (based on historical payment variance across 3 customers).

This forecast is based on QuickBooks AR/AP and PayPal settlement history.
It is not a substitute for accounting advice — verify with your bookkeeper
before making financing decisions.
```

**XLSX:** `cash-flow-snapshot-2026-04-23.xlsx` — Summary / Detail / Risks sheets.
