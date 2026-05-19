# Payment Processor Settlements Reference

## Contents

- [PayPal](#paypal)
- [Square](#square)
- [Stripe](#stripe)
- [Reconciliation logic (all processors)](#reconciliation-logic-all-processors)

---

## PayPal

### Settlement report structure

The PayPal connector returns a **Transaction History** or **Settlement** report.
Key fields:

| Field | Notes |
|---|---|
| `transaction_info.transaction_id` | PayPal transaction ID |
| `transaction_info.transaction_initiation_date` | When the transaction occurred |
| `transaction_info.transaction_amount.value` | Gross amount (positive = money in) |
| `transaction_info.fee_amount.value` | PayPal fee (negative) |
| `transaction_info.transaction_status` | Use only `S` (Success) and `P` (Pending) |
| `payer_info.email_address` | Customer email — useful for matching |

**Deposit date vs. transaction date:** PayPal batches payouts. A sale on April 28
may not deposit until May 2. Match by **deposit date** when reconciling against QB
bank entries, not transaction date.

**Refunds:** Appear as negative amounts with `transaction_type` = `T1107` or
`T1114`. They should offset the original sale — don't flag a refund as a
discrepancy against the QB register unless there's no corresponding QB credit.

**Holds:** Transactions in status `F` (Funds on Hold) have not been deposited yet.
Note them separately — they'll appear in next month's settlement.

---

## Square

### Settlement report structure

Square calls these **Payouts**. Each payout covers 1–2 business days of sales.

Key fields from the Square Payouts API:

| Field | Notes |
|---|---|
| `id` | Payout ID |
| `arrived_at` | Date the funds landed in the bank account |
| `amount_money.amount` | Net payout in cents (already minus Square fees) |
| `status` | Use only `PAID` status for reconciliation |

**Fees:** Square deducts fees before the payout — so `amount_money.amount` is net.
When matching against QB, compare to the net bank deposit, not the gross sale total.

**Same-day payouts:** If the user has Square Instant Transfer, funds may arrive on
the transaction date. The default is next business day.

---

## Stripe

### Settlement report structure

Stripe calls these **Payouts**. The Stripe connector returns payout objects plus
the balance transactions within each payout.

Key fields:

| Field | Notes |
|---|---|
| `id` | Payout ID |
| `arrival_date` | Unix timestamp of bank arrival date |
| `amount` | Net payout in cents (fees already deducted) |
| `status` | Use only `paid` for reconciliation |

**Stripe fees:** Like Square, fees are deducted before payout. Compare net amounts.

**Stripe Connect / platform accounts:** If the user runs a platform on Stripe
Connect, individual transfer payouts may look unusual. Ask the user to confirm
their Stripe account type if payout patterns don't match expectations.

---

## Reconciliation logic (all processors)

Use this logic to match processor deposits against QuickBooks bank deposits:

```
for each processor deposit in target month:
    find QB deposit where:
        abs(QB.amount - processor.net_amount) < $0.50
        AND abs(QB.date - processor.arrival_date) <= 2 days

    if match found:
        mark as RECONCILED
    elif abs(QB.amount - processor.net_amount) < $0.50 (date mismatch only):
        flag as DATE_MISMATCH (usually a timing difference — low priority)
    elif processor deposit not matched at all:
        flag as MISSING_IN_QB
    elif QB deposit not matched to any processor record:
        flag as UNMATCHED_DEPOSIT (may be ACH, check, or other income)
```

**Multi-processor businesses:** Run this logic independently per processor, then
aggregate flags. A QB deposit that doesn't match PayPal may legitimately be a
Square payout — don't flag it until you've checked all connected processors.
