# Xero — Reconciliation Reference

Sibling of [quickbooks-reconcile.md](quickbooks-reconcile.md). Same close
sequence, same packet; the reads and the "needs attention" signal differ
because Xero's data model does.

**Tool names below come from the Xero connector's published surface.
Confirm each against the connected server before the first live close.**

---

## Reports to pull

### Profit & Loss

`get_profit_and_loss` for the target month, first to last day. Accrual basis
unless the owner runs cash. Same downstream fields as the QuickBooks path:
total revenue, gross profit, net income, total operating expenses.

### The register — what "every line item" means in Xero

Xero has no single monthly transaction-register read. The register for the
close is three things, pulled separately:

| Part | Tool | What it holds |
|---|---|---|
| Bills | `get_bills` with `include_line_items=true` | Supplier invoices, paid and unpaid |
| Invoices | `get_invoices` with `include_line_items=true` | Customer invoices, paid and unpaid |
| Bank queue | `get_bank_account_transactions` | Bank-feed lines, reconciled and unreconciled |

`get_bank_account_transactions` is not the monthly register on its own; its
own description says not to treat it that way. Bills and invoices carry the
coded detail; the bank queue carries what has and has not been matched.

**State the scope in the packet.** The "Reconciled" line reads: *"Xero
(ledger: bills, invoices, and bank transactions for the month)."* An
accountant reading the packet needs to know the register was assembled from
documents plus bank lines, not exported as one report.

Key fields:

| Field | Notes |
|---|---|
| `date` | Document or bank line date |
| `status` | `AUTHORISED` (approved, unpaid), `PAID`, `DRAFT`, `VOIDED`. Drafts are excluded from the close |
| `contact.name` | Supplier or customer |
| `total` | Document total; compare to bank line amount when matching |
| `account_code` | GL account on each line item |
| `line_item_cardinality` | Number of lines on the document. Above 1 means a split |
| `has_attachments` | Present only when `include_line_items=true` |
| `is_reconciled` (bank line) | Whether the bank-feed line has been matched to a document |

---

## The "needs attention" signal: unreconciled bank lines, not uncategorized

Xero requires an account code when a bank line is reconciled, so the
QuickBooks categories ("Uncategorized Expense," "Ask My Accountant") do not
arise. The equivalent signal is **bank lines still unreconciled at month end**:
money that moved but has not been matched to a bill, invoice, or spend/receive
transaction.

Step 2 for a Xero ledger reports:

```
Unreconciled bank lines:   14 lines, AUD 6,240 across 2 accounts
```

and lists them for the owner to reconcile in Xero before the close advances.
The Step 6 summary block's "Needs attention" row carries this count.

Do not present an unreconciled line as an error. It is work not yet done,
and the owner may have a reason (a payout not yet split, a supplier bill not
yet entered). Name it, count it, and let them decide.

---

## Duplicate detection: scan documents, not bank lines

A bill entered twice in Xero sits as two `AUTHORISED` documents and produces
**no bank line until one of them is paid**. A bank-side duplicate scan cannot
see it. For a Xero ledger, Step 4 scans bills and invoices:

Flag a pair as a suspected duplicate when all four hold:

- Same `contact.name`
- Same `total` (within 0.01 in the business currency)
- Dated within 5 calendar days of each other
- Both unpaid (`AUTHORISED`), or one unpaid and one paid within the window

Present pairs to the owner exactly as the QuickBooks path does. Recurring
weekly bills from the same supplier are the usual false positive.

**Splits are one document.** A bill with several line items is one document
with `line_item_cardinality` above 1. The QuickBooks rule "group by `TxnID`
before comparing" maps to "compare documents, never lines" here. Two lines on
one bill are never a duplicate pair.

---

## Receipts: check the document first, then the folder

Xero stores attachments on the bill or invoice. Before scanning a receipts
folder (Step 5), read `has_attachments` on each expense document above the
attention threshold. It is returned only when `include_line_items=true` is
passed to `get_bills` and `get_invoices`; without that parameter the field is
absent and every document looks receipt-less.

- `has_attachments = true` → "receipt on file (Xero)"
- `false` → fall back to the folder scan, then to asking the owner

Payments made straight from the bank feed with no bill behind them (a
spend-money transaction) have no document to attach to. Treat those like a
QuickBooks expense with no attachment.

---

## Processor settlements: the payout is already a ledger line

Xero customers commonly receive Square, Stripe, and PayPal payouts through a
bank feed. The payout is therefore already in the ledger as a bank line, and
the reconciliation question is whether that line has been matched, not
whether a ledger line exists.

Step 3 for a Xero ledger:

1. Among the unreconciled bank transactions, find lines whose payee or
   reference names a processor (Square, Stripe, PayPal, Shopify Payments).
2. List them per processor as the action items: *"Stripe: 4 payouts,
   AUD 3,180, unreconciled."*
3. Match reconciled processor lines to the processor's settlement report
   net-to-net as usual, for fee verification. Keep the settlement CSV path
   for a processor with no bank feed or when the owner wants fees checked.

A processor payout with no bank line at all (feed not set up, or a manual
bank) falls back to the CSV match in
[paypal-settlements.md](paypal-settlements.md).

---

## Country, currency, and financial year

`get_organisation_info` returns the organisation's base currency and country;
`get_organisation_financial_year` returns the year end. Read them once at
the start of the close if the business context does not already carry them,
and use them for:

- Every amount in the packet (`AUD 12,400`, never `$`)
- The 0.50 / 0.01 / 25 thresholds, which are in the base currency
- Whether Step 9 offers `/tax-prep` at all (US only)

The rule is `../../../shared/currency-and-locale.md`.

---

## Graceful degradation — Xero not connected or not authorised

Take this path only when no Xero entry works. An unauthorized `small-business:xero`
beside the owner's own live Xero is connected — call the owner's entry instead
(`../../../shared/connector-neutrality.md`, "One connector, two registrations").

Ask for **two exports** from Xero: the **Profit and Loss** report for the
month, and the **Account Transactions** report with all accounts selected for
the same period. One does not contain the other. The Account Transactions
report is the register; unreconciled lines do not appear in it, so ask the
owner for the unreconciled count from the bank reconciliation screen as a
third item, or say in the packet that it was not available.

---

## Pagination and limits

Each read returns a page. Request the month in one call per bank account and
one per document type, and page until the response says there is no more.
Do not stop at the first page and call the register complete.
