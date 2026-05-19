# Gotchas

Common mistakes and edge cases in month-end close. Each entry has the pattern,
the reason it matters, and a Bad / Good example.

---

## Gotcha: Flagging split transactions as duplicates

**Why it matters:** A single purchase split across multiple GL categories appears
as multiple rows in the QB export — same vendor, same date, different amounts.
Flagging these as duplicates sends the owner on a wild goose chase.

### ✗ Bad

> Flagged as duplicate: Office Depot $47.50 on March 12 and Office Depot $62.50
> on March 12 — same vendor, same date.

Both rows share the same `TxnID` — they're splits of a $110 purchase across
"Office Supplies" and "Equipment."

### ✓ Good

Before flagging duplicates, group rows by `TxnID`. Only compare transactions
with distinct IDs. Splits of the same transaction are never duplicates.

---

## Gotcha: Treating a refund as a missing settlement

**Why it matters:** A PayPal refund appears as a negative transaction in the
settlement report. If you treat it as an unmatched outflow, you'll flag a
legitimate refund as a problem.

### ✗ Bad

> Flagged: PayPal outflow of –$89.00 on March 18 has no matching QB deposit.
> Possible missing transaction.

The –$89.00 is a refund to a customer. It should match a QB credit memo, not
a deposit.

### ✓ Good

Separate inflows (positive) from outflows (negative) before reconciling. Match
negative processor amounts against QB credit memos or refund transactions, not
deposits. Only flag an unmatched negative if no credit memo exists in QB.

---

## Gotcha: Comparing gross PayPal amount to net QB deposit

**Why it matters:** QuickBooks often records the net bank deposit (after PayPal
fees), but PayPal's transaction report shows the gross sale amount. Comparing
gross to net will always show a discrepancy equal to the fee.

### ✗ Bad

> Discrepancy: PayPal settlement $500.00, QB deposit $484.80 — delta $15.20.
> Flagged as reconciliation error.

The $15.20 is PayPal's 3.04% processing fee. This is expected and correct.

### ✓ Good

Use the **net payout** field from the PayPal settlement report
(`transaction_info.transaction_amount.value` minus
`transaction_info.fee_amount.value`) when comparing to the QB bank deposit.
If the delta is < $0.50 after fee adjustment, mark as RECONCILED.

---

## Gotcha: Advancing past Step 6 when there are unresolved flags

**Why it matters:** The close packet is the final artifact the owner files or
shares with their accountant. Exporting it with open flags bakes errors into
the record.

### ✗ Bad

> Owner hasn't responded about the 3 uncategorized transactions. Generating
> the close packet now so they have something to look at.

### ✓ Good

Hold at the Step 6 gate until the owner acknowledges every flag — either
resolving it ("categorize this as office supplies") or explicitly deferring it
("mark that as 'to review later'"). Only then export. Open items that the owner
deferred should appear in the Action Items sheet, not be silently dropped.
