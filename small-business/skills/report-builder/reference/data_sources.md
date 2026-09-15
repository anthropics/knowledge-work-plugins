# Data Sources

Metric-to-connector mapping. Pull everything in one parallel batch; never serially.

---

## The ledger — the spine of most reports

Most SMB reports resolve to the accounting ledger. Whichever is connected — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books — is the source; they are peers (`../../../shared/connector-neutrality.md`). The metric families below are written against QuickBooks report names; the NetSuite, Xero, MYOB, and Zoho Books sections say where each family comes from there. Amounts carry the business's currency code (`../../../shared/currency-and-locale.md`).

### QuickBooks

| Metric family | Where it comes from |
|---|---|
| Revenue, expenses, net income | Profit and Loss report — from the rows or `monthlyBreakdown`, never the summary's `totalExpenses` / `grossProfit` / `grossProfitMargin`, which report 0 / 100% against real rows (Trap 2) |
| Revenue by location or class | P&L with class or location split |
| AR aging | AR aging summary, always constrained — see below |
| AP aging | AP aging **detail** (`qbo_accounting_get_ap_aging_detail`), constrained by `vendor_name` or `due_before`; bucket the rows yourself. Never the AP aging summary: it nets vendor credits into the buckets and reports negative overdue totals (a defect in that tool, `../../../shared/quickbooks-report-traps.md` Trap 6) |
| Cash position | Balance sheet |
| Sales by customer | Sales by customer summary, rollup rows filtered — see below |
| Sales by product | Sales by product summary |
| Payroll expense | P&L payroll lines |

**Fallback:** if QuickBooks returns empty, a sync-in-progress state, or an auth error, mark the affected metrics "n/a — QuickBooks unavailable" and continue with other sources. Do not retry in a loop and do not ask the owner to reconnect mid-report.

### Aging reports must be constrained, every time

An unconstrained aging call fails on any real book. On a mid-size ledger the AR aging summary returns well over a hundred thousand characters, overflows the tool output limit, and comes back as nothing usable. This is not an edge case; it is the normal result for a business with a few hundred customers.

Always pass narrowing arguments. The three that matter:

- a top-N cap, so only the biggest balances come back
- a minimum days-overdue threshold, which drops the current bucket entirely
- a minimum dollar threshold, which drops the long tail of small balances

For a report, "the twenty largest balances at least one day overdue" is the useful shape and it always fits. If the owner genuinely needs every line, pull the detail report per customer rather than asking for the whole book at once.

The same rule applies to AP aging, which comes from the detail report: narrow it by vendor or due date. It is the smaller report of the two, but it grows the same way.

### Sales by customer double-counts parent customers

The sales-by-customer summary returns two rows for any customer with sub-customers or jobs underneath it: a summary row for the parent, and a separate total row for the same parent. They carry the same figure. The report's own top-customer list contains both.

Read naively, this puts a customer in your rankings twice — once under its own name and once as "Total for" that name — and overstates every concentration figure you compute from it.

Drop rows whose metadata type marks them as a total before you rank, sum, or compute concentration. Keep the parent summary row; it is the real one. Concentration built on unfiltered rows is wrong every time, not occasionally.

---

## HubSpot — pipeline and customers

| Metric family | Where it comes from |
|---|---|
| Deal counts by stage | CRM deals search |
| Win rate, cycle time | Deals with close dates and outcomes |
| Weighted pipeline | Deal value times stage probability |
| New contacts, lead sources | Contacts with create date and source property |
| Deal owner performance | Deals grouped by owner |

**Watch out:** CRM deal values are forecasts. When a report mixes CRM and accounting data, revenue always comes from the books. Say which source each number came from.

---

## Payment processors

| Source | What it's good for |
|---|---|
| PayPal | Settlements, fees, disputes, transaction detail |
| Stripe | Settlements, fees, refunds, subscription revenue |
| Square | In-person sales, per-location splits, tips |

**Double-count risk.** A Shopify order settled through Stripe appears in both. Pick one system as the revenue source per report, state the choice in the summary, and use the other only for fees and timing.

---

## Shopify

Orders, SKU-level revenue, variant performance, fulfillment status, refunds. Best source for anything grouped by product.

COGS usually is not in Shopify. Margin metrics need QuickBooks or an uploaded cost file.

---

## NetSuite

Common at the larger end of the segment. Same metric families as the QuickBooks section via `ns_runReport` and `ns_runCustomSuiteQL`, plus item-level COGS and inventory valuation.

---

## Xero

Same metric families as the QuickBooks section, from `get_profit_and_loss` (revenue, expenses, net income, by period), `get_aged_receivables` (AR aging, same aging-constraint rules), and `get_bills` (AP). The organisation record supplies the base currency and financial year, so period references resolve against the business's year end.

---

## Ramp and Expensify

Card spend, expense categories, receipts, reimbursements. Useful for expense-side reports and for catching spend that has not yet hit the books.

**Ramp** also carries real business and treasury account balances with history, plus vendor bill detail and natural-language spend analytics. Its write actions — approve or reject a bill, mark a bill ready to sync — belong to `ap-processor`, never to a report. Read only, here.

**Expensify is read-only search.** Expense reports, individual expenses, invoices, trips, category-grouped totals, and approval-state statuses. Receipt substantiation is a first-class filter: "expenses over USD 75 with no receipt attached" is a real query and a genuinely useful report.

**Reimbursements appear in both.** Ramp and Expensify overlap here. Pick one as the reimbursement source per report, say which, and use the other for detail it uniquely holds — the same rule the processors follow.

---

## MYOB

The ledger for MYOB shops. **Read-only.** Same P&L and receivables shape as QuickBooks, with three hard limits worth stating in the report rather than discovering mid-run.

| Metric family | Where it comes from |
|---|---|
| Revenue, expenses, net profit | P&L, with monthly or quarterly breakdown and prior-year comparison |
| AR aging by customer | Outstanding customer balances, with at-risk flags |
| AP | Outstanding payables |
| Sales totals | Sales invoice totals |
| Payment terms | Standard payment terms |

- **No bank or cash balances.** MYOB gives the AR and AP legs, never cash on hand. A cash-position metric sourced from MYOB is not available — say so rather than substituting AR.
- **No customer contact detail.** Names and balances only.
- **Three financial years.** Reporting covers the current and prior two financial years. A four-year comparison is not available; say so instead of returning a short series that looks complete.
- Any period reference — "last quarter", "FYTD" — means the *business financial year* unless the owner says calendar. Resolve the financial-year dates once and reuse them across the run.

---

## Zoho Books

The ledger for Zoho shops. Document-level reads, no report endpoints — the
metric families are assembled from lists, and the report says so.

| Metric family | Where it comes from |
|---|---|
| Revenue (invoiced) | `list_invoices` by date range with `response_option=3` for the summed total; by customer via `customer_id`, by item via `item_id` |
| Expenses | `list_expenses` by date range, grouped on `account_name` or `vendor_name` |
| AR aging | `list_invoices` with `status=overdue`, bucketed on `due_date`; `list_contacts` with `filter_by=Invoice.OverDue` for per-customer `outstanding_receivable_amount` |
| AP (open commitments) | `list_purchase_orders` open, plus `list_expenses` with `status=unbilled` |
| Cash position | `list_bank_accounts` — `current_balance` per active account |
| Sales by customer / product | `list_invoices` grouped by `customer_name` or by line `item_name`; `list_sales_orders` for orders not yet invoiced |
| Payroll expense | Not available — no P&L. Take it from the payroll connector (`month-end-prep` Step 5a) or an export |

- **No P&L, cash-flow, or aging report endpoints.** "Net income" is invoiced revenue minus recorded expenses, labelled as such; a true P&L comes from the Reports export.
- **No bill object and no vendor payments.** AP is purchase orders and expenses only.
- **No bank-transaction feed.** Balances only, with an `uncategorized_transactions` count per account.
- The organisation record (`get_organization`) supplies `country_code`, `currency_code`, and `fiscal_year_start_month`, so period references resolve against the business's year end.

---

## The uploaded-file path

**This is a first-class mode, not a degraded one.** A large share of owners have tool sprawl and no clean connector.

When no connector covers a metric:

1. Say plainly what you need: "Export your sales report for the period and drop it here."
2. Accept CSV or XLSX. Read the header row and map columns to the spec's metrics.
3. If a needed column is absent, name it specifically — "there's no cost column, so I can't compute margin" — rather than silently dropping the metric.
4. Record the file's column mapping in the saved spec so the next run can reuse it.

A report built from a file is a real report. Deliver the same chat summary and the same workbook.

---

## Parallel-pull rule

Every source call goes out in one batch. Reports commonly touch four or five systems, and serial pulls turn a thirty-second skill into a two-minute wait that owners will not sit through twice.

Record failures internally. Surface them in the report appendix, never mid-stream.
