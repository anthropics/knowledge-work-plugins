# Close Packet Format Reference

The close packet is two files: an xlsx workbook and a one-page PDF summary.

## File naming

```
close-packet-2024-03.xlsx
close-packet-2024-03-summary.pdf
```

Use ISO 8601 year-month (`YYYY-MM`) in the filename. Default save location is the
Desktop; use the user's preferred path if specified.

---

## xlsx workbook — three sheets

### Sheet 1: P&L

A formatted copy of the ledger's P&L for the target month. Two-column layout:
**Category** and **Amount**.

Required rows (in order):
1. Revenue subtotal
2. COGS subtotal
3. **Gross Profit** (bold)
4. **Gross Margin %** (bold, formatted as %)
5. Operating expenses by category (each on its own row)
6. Total Operating Expenses
7. **Net Income** (bold)

Include a MoM comparison column if prior-month data is available. Format amounts as
currency using the business's ISO code, never a bare symbol: `"AUD "#,##0.00`,
`"GBP "#,##0.00`, `"USD "#,##0.00` (`../../../shared/currency-and-locale.md`).
Negative values in red.

### Sheet 2: Reconciliation

Side-by-side comparison of ledger deposits vs. processor settlements.

Columns:
| Column | Source |
|---|---|
| Date (Ledger) | Ledger deposit date |
| Amount (Ledger) | Ledger deposit amount |
| Processor | PayPal / Shopify / Square / Stripe |
| Date (Processor) | Processor arrival date |
| Amount (Processor) | Processor net payout |
| Delta | Ledger amount minus processor amount |
| Status | RECONCILED / MISSING_IN_LEDGER / UNMATCHED_DEPOSIT / DATE_MISMATCH / UNRECONCILED_IN_LEDGER |

`UNRECONCILED_IN_LEDGER` is the bank-feed case: the payout is a ledger line that has
not yet been matched to a document (the usual Xero shape).

Color-code the Status column:
- RECONCILED → green fill
- DATE_MISMATCH or UNRECONCILED_IN_LEDGER → yellow fill
- MISSING_IN_LEDGER or UNMATCHED_DEPOSIT → red fill

### Sheet 3: Action Items

Any open flags from the checklist. Columns:
| Column | Notes |
|---|---|
| Category | Needs Attention (uncategorized or unreconciled) / Missing Receipt / Duplicate / Reconciliation Flag |
| Date | Transaction date |
| Amount | Amount, in the business's currency |
| Vendor / Customer | Name |
| Description | What's wrong and what to do |

If there are no open items, show a single row: "No open action items — books are clean."

### Sheet 4: Payroll (only when a payroll connector is connected)

The Step 5a totals beside what the ledger recorded. One row per payroll run
plus a contractor row and a total row. Columns:

| Column | Source |
|---|---|
| Run | Check date, or "Contractors" for the contractor-payments row |
| Gross pay | Payroll connector `totals.gross_pay` |
| Employer taxes | `totals.employer_taxes` |
| Employee taxes | `totals.employee_taxes` |
| Net pay | `totals.net_pay`; contractor row uses `total.wages` |
| Ledger payroll expense | The month's payroll expense lines from the ledger, matched by date |
| Delta | Ledger minus (net pay + employer taxes), flagged above 0.50 |

Totals only. No employee names or per-person amounts on this sheet — the run
count and the month totals are what an accountant needs. Footnote when Gusto
supplied the contractor row: "Contractor payments cover US contractors only."

---

## PDF summary — one page

Layout (top to bottom):

```
[Business Name]                    Close Packet — [Month Year]
────────────────────────────────────────────────────────────

KEY FIGURES
Revenue        AUD XX,XXX
Gross Margin   XX%
Net Income     AUD XX,XXX
Payroll        AUD XX,XXX (X runs)     [only when a payroll connector is connected]

P&L SUMMARY
[150–250 word plain-English narrative from Step 7]

ACTION ITEMS
X items needing attention · X missing receipts · X open flags
[or "Books are clean — no open items." if all clear]

────────────────────────────────────────────────────────────
Prepared [Date] · Powered by Claude
```

Use a clean sans-serif font (Helvetica or equivalent). No logo required. Keep
margins ≥ 0.75 in on all sides so it prints cleanly. The currency code in the key
figures is the business's own (`AUD` above is an example).

**Generating the PDF:** Use the `xlsxwriter` or `reportlab` Python library if running
a script, or instruct Claude to render the content and export via the Desktop
connector's print-to-PDF capability. The user can also print the PDF from the xlsx
P&L sheet if a script isn't available.
