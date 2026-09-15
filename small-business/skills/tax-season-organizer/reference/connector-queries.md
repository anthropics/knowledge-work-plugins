# Connector Query Guide

How to pull the right data from each connector for each mode. Ledgers are peers
(`../../../shared/connector-neutrality.md`): use whichever is connected. Both modes are
US federal tax; the country check in the skill's Step 0 runs before any of this.

---

## Xero — Quarterly mode (P&L)

`get_profit_and_loss` for January 1 through the last day of the most recently completed
quarter. Capture the same three figures as the QuickBooks path: total income, total
expenses, net profit.

Read `get_organisation_info` first if the business context has no Country or Currency:
it returns both, plus the base currency the P&L is in. `get_organisation_financial_year`
returns the year end; a US organisation on a calendar year is the case this path was
built for, and a non-calendar year end changes which months "YTD" covers — resolve the
dates once and say which basis the estimate is on.

**Confirm each tool name in this section before the first live run.**

---

## Xero — Year-end mode (contractor payments)

Two reads, in this order:

1. **`get_1099_report_summary`** — for a US organisation, Xero already computes the
   1099 view: payees, totals for the year, and the contact's tax-ID status. This is the
   expected output of Path 2 in one call. Use it as the candidate list and skip to the
   W-9 check.
2. **`get_bills`** with `include_line_items=true`, status `PAID`, grouped by
   `contact.name` — when the summary is unavailable, or to cross-check it. **Attribute
   each bill to the year it was paid, not the year it was dated:** 1099 totals are by
   payment date, so a bill dated in December and paid in January belongs to the later
   year. Read the payment date from the bill's payments (or `fully_paid_on_date` where
   the connector exposes it), pull bills from both calendar years around the boundary,
   and sum per contact by payment year. Exclude bills coded to goods, refunds, and
   transfers.

For each contact, capture: name, tax ID present or not (the W-9 signal), total paid,
payment dates. Xero's contact record holds a tax number field; empty means no W-9 on
file.

Worked example, shape only:

```
Xero 1099 summary, tax year 2025:
  Rivera Design Co        USD 14,200   tax ID on file
  M. Okafor               USD  2,850   no tax ID — collect W-9
  Northgate Electrical    USD    580   under threshold — near-threshold list
```

Same aggregation, threshold, and W-9 logic as every other source from here.

---

## QuickBooks — Quarterly mode (P&L)

Pull a **Profit & Loss** report for the period January 1 through the last day of the most recently completed quarter.

Key fields to capture:
- `Total Income` (gross revenue)
- `Total Expenses` (all operating expenses)
- `Net Ordinary Income` (= income − expenses; this is the basis for tax calculation)

If QuickBooks returns multiple income/expense categories, sum them. You want the single
bottom-line net profit figure.

**If the user's QuickBooks is on cash basis**, use that. If accrual, note it in output —
the accountant should confirm which basis to use for estimated taxes.

---

## QuickBooks — Year-end mode (contractor payments)

Pull all **bill payments and checks** to vendors for the full tax year (Jan 1 – Dec 31).

Filter for:
- Vendor type = "1099 eligible" (if the user has tagged vendors in QuickBooks)
- OR any vendor whose category is: consulting, contract labor, subcontractor, freelance, design, legal, accounting, marketing, staffing

For each vendor record, capture:
- Vendor name (legal name if available)
- EIN / SSN (from vendor profile — indicates W-9 on file)
- Total payments for the year
- Payment dates and amounts (for cross-reference)
- Vendor type / 1099 eligibility flag

**Common issue:** Many QuickBooks users do not tag vendors as 1099-eligible. If
`1099 eligible` returns few or no results, pull ALL vendors with significant payment
totals and let the user / accountant classify them. Note this in output.

### When the connector returns totals with no payee breakdown

Try the live connector first, then fall back. Three steps:

1. **Try the live connector.** Attempt to pull vendor-level payment records via the
   QuickBooks MCP. If it returns individual payee records with name, amount, and account
   category, use them directly and skip the rest of this section.

2. **Detect an aggregate-only response.** If the response carries only category-level
   totals — "Contract labor: USD 7,500" with no payee breakdown — the connector does not
   support vendor-level queries on this account. Ask for an export:

   > "QuickBooks returned summary data only — I need payee-level detail to build your 1099
   > list. Please export a **Transaction List by Vendor** report (QuickBooks → Reports →
   > Expenses → Transaction List by Vendor, filtered to this tax year) and upload the CSV
   > here. I'll process it automatically."

3. **Process the CSV.** Map columns: payee name, amount, date, payment method, and
   EIN/SSN status. From there the aggregation and threshold logic is identical regardless
   of which source the data came from.

If the QuickBooks MCP later exposes vendor payment records directly, step 1 simply
succeeds and the fallback is skipped. No skill change is needed — the try-first order
handles it.

---

## PayPal — Year-end mode

Pull all **"Goods & Services" payments sent** (not received) for the tax year.

Key fields:
- Recipient name / email
- Total amount per recipient (aggregate for the year)
- Transaction type = "Payment" or "Business Payment"
- Date

**Exclude:** personal payments ("Friends & Family"), refunds, disputes, transfers
to own accounts.

**1099-K note:** PayPal issues its own 1099-K to any recipient who receives ≥ USD 600
in goods & services payments. Flag this in output — the accountant determines whether
the business must also issue a 1099-NEC or can rely on PayPal's 1099-K.

---

## Stripe — Year-end mode

Pull all **transfers to external accounts** (payouts to contractors, not payouts to the
business owner's own bank).

Key fields:
- Recipient name / ID
- Total transferred per recipient for the year
- Payment description / metadata (to confirm these are for services)

**Exclude:** Stripe payouts to the business's own bank account.

**1099-K note:** Same as PayPal — Stripe issues 1099-K to contractors above the
threshold. Flag and defer to accountant.

---

## Square — both modes

Square is a peer of PayPal and Stripe in the payments category, and it holds less of what
this skill needs. Say what it cannot do, in one line, and move on.

**Quarterly mode:** the P&L comes from the ledger, not from Square. Square's payments
list (all locations — `ListPayments` without `location_id` returns only the main one)
gives gross card receipts for the period, useful only as a cross-check that the ledger's
income line is not missing a location. Never substitute it for the P&L.

**Year-end mode:** Square exposes no payments *to* external parties through the
connector — its payouts go to the business's own bank, and contractor pay lives in Square
Payroll, which the connector does not reach. Square contributes nothing to the 1099-NEC
list. Say so by name in the Sources section rather than leaving it out silently.

**1099-K note:** like PayPal and Stripe, Square issues a 1099-K to the *business* for
card receipts above the threshold. That is the business's own income reporting, not a
contractor's; note it for the accountant so gross receipts on the return reconcile to the
processors.

---

## Ramp — both modes

Card transactions with GL and category coding, vendor bills with their approval history,
vendor records, and reimbursements.

- **Quarterly mode:** card spend by category, for the expense side of the estimate. Anything not yet synced to the ledger is spend the P&L does not know about — name it as an adjustment rather than folding it in silently.
- **Year-end mode:** vendor and bill records help confirm a payee list built from the ledger. Ramp is a cross-check, not the source of truth.

Ramp can approve bills and mark them ready to sync. **Nothing in this skill writes.** Read only.

---

## Expensify — both modes

**Read-only search.** Expense reports, individual expenses, receipts, invoices, trips,
category-grouped totals, and approval-state statuses.

- **Quarterly mode:** category-grouped expense totals, for the deduction side.
- **Receipt substantiation is a first-class filter.** Search for expenses with no receipt attached and report the total and the count. That is the line the accountant acts on: an expense without a receipt is a deduction that may not hold.
- Expensify does not carry contractor payee detail suitable for a 1099 list. Do not build one from it.

---

## NetSuite — both modes

P&L via `ns_runReport` for the quarterly path; vendor bill payments by payee via
`ns_runCustomSuiteQL` for the year-end path. Same fields as the QuickBooks path. NetSuite
vendor records carry the tax-ID field that stands in for the W-9 signal.

---

## MYOB — quarterly mode only

**Read-only, and P&L-side only.** MYOB gives net profit with monthly or quarterly breakdown
and a prior-year comparison — which is exactly the input the quarterly estimate needs.

What it cannot do:

- **No contractor or payee detail.** MYOB has no role in 1099 prep. Say so and fall back to PayPal, Stripe, or a CSV for the payee list.
- **No bank balances.**
- **Three financial years only** — the current and prior two. Anything older is unavailable.

Resolve the business financial-year dates once before pulling the P&L and reuse them. Any
"last quarter" or "FYTD" reference means the financial year, not the calendar year, unless
the owner says otherwise — and if the financial year is not the calendar year, say which
basis the estimate is on, because the accountant needs that stated.

---

## Zoho Books — both modes

No report endpoints, so both modes are assembled from document lists and labelled
as such.

**Quarterly mode.** `list_invoices` for January 1 through the quarter end with
`response_option=3` (summed `total`), and `list_expenses` for the same range
summed on `total`. Income minus expenses is the net figure for the estimate —
**an invoiced-and-recorded estimate, not a P&L.** Say that in the output; the
accountant confirms basis. `get_organization` supplies `country_code`,
`currency_code`, and `fiscal_year_start_month` for the Step 0 country check
and the YTD dates.

**Year-end mode.** `list_contacts` with `contact_type=vendor`, reading
`track_1099` (Zoho's own 1099-eligible flag) and `tax_id_type` / tax ID
presence as the W-9 signal. Then `list_expenses` per `vendor_id` for the tax
year, summed on `total` by payment year.

**What it cannot do:** there is no bill object and no vendor-payment list, so
only expenses count toward each payee's total. A vendor paid through bills in
Zoho Books is invisible here — say so, and ask for the **Payments Made** or
**Vendor Balances** export from Reports for the payee list when the business
uses bills.

---

## Desktop / CSV fallback

If any connector is unavailable, ask the user to:
1. Export a P&L from their ledger as CSV (QuickBooks: Reports → Profit & Loss → Export; Xero: Reports → Profit and Loss → Export; Zoho Books: Reports → Profit and Loss → Export; and for the year-end path, Xero's 1099 report or a Payable Invoice Summary by contact, or Zoho Books' Payments Made report by vendor)
2. Export a transaction history from PayPal (Activity → Download → CSV)
3. Export a payout report from Stripe (Dashboard → Payouts → Export)

When reading uploaded CSVs, look for these columns (names vary by export):
- P&L: `Description`, `Amount`, `Type` (Income / Expense)
- PayPal: `Name`, `Type`, `Amount`, `Date`, `Transaction ID`
- Stripe: `Description`, `Amount`, `Created date`, `Status`

If columns don't match, ask the user to identify the payee name and amount columns.
