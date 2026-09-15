# Worked example — cash-flow-snapshot

**Scenario:** Small services business. QuickBooks + PayPal connected. Three
active customers, monthly payroll, office rent.

---

## Input data (pulled from connectors)

**AR aging (QuickBooks):**

| Customer       | Invoice | Amount   | Due Date   | Days Outstanding |
|----------------|---------|----------|------------|------------------|
| Acme Corp      | INV-112 | USD 8,400   | Apr 10     | 12               |
| BlueSky LLC    | INV-108 | USD 14,200  | Apr 22     | 0                |
| Crestwood Inc  | INV-115 | USD 6,000   | May 5      | —                |

**Historical payment lag (from PayPal settlements):**

| Customer       | Mean Lag | Std Dev | Payments on Record |
|----------------|----------|---------|--------------------|
| Acme Corp      | 18 days  | 4 days  | 11                 |
| BlueSky LLC    | 7 days   | 2 days  | 8                  |
| Crestwood Inc  | 12 days  | 5 days  | 6                  |

**Fixed costs (QuickBooks recurring AP):**
- Payroll: USD 22,000 — hits April 15
- Rent: USD 3,200 — hits May 1
- Software subscriptions: USD 480 — hits May 1

---

## Step 3 output — adjusted inflow dates

| Customer       | Invoice Amount | Adj. Receipt Date | Notes                             |
|----------------|---------------|-------------------|-----------------------------------|
| Acme Corp      | USD 8,400        | Apr 28            | Due Apr 10 + 18-day mean lag      |
| BlueSky LLC    | USD 14,200       | Apr 29            | Due Apr 22 + 7-day mean lag       |
| Crestwood Inc  | USD 6,000        | May 17            | Due May 5 + 12-day mean lag       |

---

## Step 4 output — 30/60/90 forecast

Confidence band calculation:
- Weighted avg stddev: 3.6 days
- Weighted avg mean lag: 12.7 days
- band_pct = 3.6 / 12.7 = **28.3%**

| Window  | Expected Inflows | Expected Outflows | Net      | Low (−28%) | High (+28%) |
|---------|-----------------|-------------------|----------|------------|-------------|
| 0–30d   | USD 22,600         | USD 22,000           | +USD 600    | −USD 5,928    | +USD 7,128     |
| 31–60d  | USD 6,000          | USD 3,680            | +USD 2,320  | +USD 1,670    | +USD 2,970     |
| 61–90d  | USD 0              | USD 0                | USD 0       | —          | —           |

---

## Step 5 output — risks flagged

1. **Payroll crunch:** Payroll (USD 22,000) hits April 15. Low-band inflows through
   April 14: USD 0 (both AR receipts fall April 28–29). Shortfall risk: up to USD 22,000.
   *Recommend: confirm receivables timing with Acme and BlueSky before April 14.*

2. **Late-payer risk:** Acme Corp historically pays 18 days late. Their USD 8,400
   invoice (due Apr 10) shifts to April 28 — after payroll.

---

## Step 6 output — chat summary

```
Cash Flow Snapshot — Apr 23 → Jul 21, 2026
Sources: QuickBooks, PayPal

              Expected    Low        High
30-day net:   +USD 600      −USD 5,928    +USD 7,128
60-day net:   +USD 2,320    +USD 1,670    +USD 2,970
90-day net:   USD 0         —          —

⚠ 2 risks flagged:
  • Payroll crunch: USD 22K payroll hits Apr 15; AR receipts don't clear until
    Apr 28–29. Low-band shortfall risk: up to USD 22,000.
  • Late-payer: Acme Corp (mean 18-day lag) shifts USD 8,400 past payroll date.

Confidence band: ±28% (based on historical payment variance across 3 customers).

This forecast is based on QuickBooks AR/AP and PayPal settlement history.
It is not a substitute for accounting advice — verify with your bookkeeper
before making financing decisions.
```

**XLSX:** `cash-flow-snapshot-2026-04-23.xlsx` — Summary / Detail / Risks sheets.
