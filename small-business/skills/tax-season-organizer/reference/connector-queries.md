# Connector Query Guide

How to pull the right data from each connector for each mode.

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

**1099-K note:** PayPal issues its own 1099-K to any recipient who receives ≥ $600
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

## Desktop / CSV fallback

If any connector is unavailable, ask the user to:
1. Export a P&L from QuickBooks as CSV (Reports → Profit & Loss → Export)
2. Export a transaction history from PayPal (Activity → Download → CSV)
3. Export a payout report from Stripe (Dashboard → Payouts → Export)

When reading uploaded CSVs, look for these columns (names vary by export):
- P&L: `Description`, `Amount`, `Type` (Income / Expense)
- PayPal: `Name`, `Type`, `Amount`, `Date`, `Transaction ID`
- Stripe: `Description`, `Amount`, `Created date`, `Status`

If columns don't match, ask the user to identify the payee name and amount columns.
