# Gotchas — cash-flow-snapshot

Known edge cases and connector failure modes. 2–5 entries, Good/Bad format.

---

## 1. QuickBooks AR aging includes invoices already collected

**Bad:** Including fully-paid invoices from the AR aging report inflates inflow
projections. QuickBooks sometimes shows $0-balance invoices in aging exports.

**Good:** Filter AR rows to `balance_due > 0` before computing inflows. If the
connector doesn't expose balance_due, subtract known PayPal/Stripe settlements
from the invoice total before including it.

---

## 2. PayPal settlement lag varies by transaction type

**Bad:** Assuming all PayPal receipts settle in 1–2 business days. PayPal holds
funds differently for disputes, new sellers, and high-value transactions — using
a flat settlement assumption produces overconfident inflow timing.

**Good:** Compute settlement lag from actual `transaction_date` → `completed_date`
pairs in the PayPal transaction history. Use the computed mean and stddev per
customer or transaction type.

---

## 3. CSV column names are inconsistent across accounting exports

**Bad:** Requiring exact column names like "Date", "Amount", "Type". QuickBooks
CSV exports use "Transaction Date", "Amount", "Transaction Type". Wave uses
"Date", "Amount", "Account Type". Rigid parsing fails silently.

**Good:** Fuzzy-match column headers (date → transaction date → txn date;
amount → debit/credit; type → category → account type). Show the header row
to the user and confirm mapping before computing — one question beats a silent
wrong forecast.

---

## 4. Fixed costs hidden in one-off AP entries

**Bad:** Only pulling recurring line items labeled as "recurring" in QuickBooks.
Many SMBs don't tag fixed costs consistently — rent may appear as a one-off
vendor bill each month.

**Good:** Look for AP entries that appear in 3+ consecutive months with the same
vendor and similar amount (±10%). Treat these as recurring fixed costs in the
forecast. Surface the list to the user: "I'm treating these as fixed monthly
costs — does that look right?"

---

## 5. Confidence band formula breaks when mean payment lag is zero

**Bad:** Dividing stddev by a mean lag of 0 (e.g. immediate payment customers
like Square POS) produces a divide-by-zero error or an infinite band.

**Good:** If mean lag ≤ 1 day, set band_pct to 5% (low variance, near-immediate
settlement). Don't attempt the division.
