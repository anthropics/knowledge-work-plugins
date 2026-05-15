# QuickBooks — Reconciliation Reference

## Reports to pull

### Profit & Loss (P&L)

Use the **Profit and Loss** report via the QuickBooks connector:
- Date range: first day to last day of target month
- Accounting method: **Accrual** unless the user has told you they run cash-basis
- Include all accounts

Key fields used downstream:
| Field | Notes |
|---|---|
| `TotalRevenue` | Top-line revenue |
| `GrossProfit` | Revenue minus COGS |
| `GrossProfitMargin` | Compute as GrossProfit / TotalRevenue |
| `NetIncome` | Bottom line |
| `TotalExpenses` | Operating expenses subtotal |

### Transaction Register

Pull the **Transaction List by Date** report or equivalent for the target month.
This is the line-item detail used for uncategorized flagging and duplicate detection.

Key fields:
| Field | Notes |
|---|---|
| `TxnDate` | Transaction date (not posting date) |
| `TxnType` | Invoice, Payment, Expense, Deposit, etc. |
| `Amount` | Positive = income, negative = expense in most QB exports |
| `AccountRef.name` | The GL account category |
| `EntityRef.name` | Vendor or customer name |
| `Memo` | Free-text description |
| `AttachmentCount` | > 0 means a receipt is attached in QB |

## Identifying uncategorized transactions

Flag a transaction as uncategorized if `AccountRef.name` is any of:
- "Uncategorized Income"
- "Uncategorized Expense"
- "Uncategorized Asset"
- blank / null
- "Ask My Accountant" (QB's built-in "I don't know" category)

## Pagination

The QB API returns a maximum of 1,000 rows per request. For businesses with high
transaction volumes, paginate using `startPosition` and `maxResults` parameters.
Request in 500-row batches to stay safely under the limit.

## Common data issues

**Split transactions** — a single purchase split across multiple categories appears as
multiple rows with the same date and vendor but different amounts. These are NOT
duplicates. Before flagging duplicates, group rows by `TxnID` — rows sharing an ID
are splits of one transaction.

**Bank feeds vs. manual entries** — bank-feed transactions have `PrivateNote` set to
"bank feed" or similar. Manual entries often lack a memo. Neither is a signal of a
problem on its own, but it helps explain why a transaction might lack a receipt.

**PayPal transactions already in QB** — if the user has the PayPal-QB auto-sync
enabled, PayPal transactions will already appear in the register. Don't double-count
them during reconciliation (Step 3). Check whether the QB deposit lines have
"PayPal" in the account or memo before matching.

**Retainer / deposit transactions** — a customer deposit is not revenue until the
work is delivered. If the user is on cash-basis accounting this distinction matters
less, but flag any large Deposit-type transactions without a matching Invoice for
their awareness.
