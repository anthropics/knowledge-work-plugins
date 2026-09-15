# Zoho Books — Reconciliation Reference

Sibling of [quickbooks-reconcile.md](quickbooks-reconcile.md) and
[xero-reconcile.md](xero-reconcile.md). Same close sequence, same packet;
the reads and the "needs attention" signal differ because the connector's
surface does.

Every call takes `organization_id`; get it once from
`list_organizations` (or `get_organization`, which also returns the locale
fields) and reuse it.

---

## What the connector holds, and what it does not

| Holds | Does not hold |
|---|---|
| Invoices, estimates, sales orders, customer payments | Bills, vendor payments |
| Expenses, purchase orders | Bank transactions or a bank feed |
| Bank and cash accounts with balances and an uncategorised count | Journals |
| Contacts (customers and vendors, with a 1099 flag) | Any report: P&L, cash flow, aging |
| Chart of accounts with balances (`list_chart_of_accounts` with `showbalance`) | |
| Organisation record: country, currency, fiscal year start | |

State this in the packet: an accountant needs to know which parts came from
the connector and which from an export.

---

## Reports to pull

### Profit & Loss — from an export

There is no P&L endpoint. Ask for the **Profit and Loss** export (Reports →
Profit and Loss → Export, target month) before Step 2 runs, even when the
connector is connected. Say why in one line: *"Zoho Books doesn't expose
reports through the connector, so I need the P&L export; everything else I
can read directly."*

A stand-in when the owner cannot export: invoiced revenue from
`list_invoices` (`date_start`/`date_end`, `response_option=3` for the summed
`total`) minus recorded expenses from `list_expenses` for the same range.
Label it *"invoiced minus recorded, not a P&L"* everywhere it appears.

### The register — three document lists

| Part | Tool | What it holds |
|---|---|---|
| Invoices | `list_invoices` with `date_start` / `date_end`, `per_page` up to 200 | Customer invoices, all statuses; `status` filter for `paid`, `unpaid`, `overdue`, `draft`, `void` |
| Expenses | `list_expenses` with `date_start` / `date_end` | Money spent, coded to an `account_name`, with `vendor_name` and `status` |
| Purchase orders | `list_purchase_orders` for the month | Open commitments to vendors |

Exclude `draft` and `void` documents from the close. Page until
`page_context.has_more_page` is false; a single page is not the month.

Key fields:

| Field | Notes |
|---|---|
| `date`, `due_date` | Document dates |
| `status`, `current_sub_status` | `overdue` carries `due_days` as text ("Overdue by 323 days") |
| `customer_name` / `vendor_name` | Counterparty |
| `total`, `balance` | Document total and what is still unpaid |
| `has_attachment` | Receipt or document attached |
| `reminders_sent`, `last_reminder_sent_date` | Invoice chase history |
| `currency_code`, `exchange_rate` | Per document; `bcy_*` fields are base currency |

---

## The "needs attention" signal: uncategorised transactions per account

`list_bank_accounts` (`filter_by=Status.Active`) returns each bank and cash
account with `current_balance`, `bank_balance`, and
`uncategorized_transactions`. That count is the attention signal — bank-feed
lines the owner has not yet coded.

Step 2 for a Zoho Books ledger reports:

```
Uncategorised bank transactions:   9 across 2 accounts (Operating 7, Savings 2)
```

The lines themselves cannot be listed through the connector. Tell the owner
the count and the account, and that they are categorised in Zoho Books
(Banking → account → Uncategorized) before the close advances. The Step 6
summary block's "Needs attention" row carries this count.

`Undeposited Funds` is a cash account in this list, not a bank. A large
balance there at month end means customer payments received and not yet
deposited — name it as an open item, not as cash on hand.

---

## Duplicate detection: scan documents

Same rule as Xero — a document keyed twice is two documents. Step 4 scans
invoices and expenses separately:

- Same `customer_name` (invoices) or `vendor_name` (expenses)
- Same `total` (within 0.01 in the base currency)
- Dated within 5 calendar days of each other
- Both unpaid, or one paid inside the window

Recurring expenses (`recurring_expense_id` set) and invoices created from a
recurring invoice (`recurring_invoice_id` set) are the usual false positive;
show the id so the owner sees why.

---

## Receipts: check the document, then the folder

`has_attachment` on invoices and expenses says whether a file is attached.
Above the attention threshold, read it first:

- `true` → "receipt on file (Zoho Books)"
- `false` → fall back to the folder scan, then to asking the owner

---

## Processor settlements: no bank feed, so the CSV match runs

The connector has no bank-transaction list, so a payout cannot be found as a
ledger line. Step 3 for a Zoho Books ledger goes straight to the CSV match in
[paypal-settlements.md](paypal-settlements.md): the processor's settlement
report against the **bank statement** the owner uploads. Ask for the
statement in the same breath as the P&L export.

Two things the connector does supply for this leg:

- `list_customer_payments` for the month — payments recorded against
  invoices, with `payment_mode` and `reference_number`. A processor payout
  that was recorded as a customer payment shows here.
- Invoices carry `payment_options.payment_gateways` — which gateways (Stripe,
  PayPal) the invoice was set up to accept. That tells you which processor's
  settlement to expect for it.

---

## Country, currency, and financial year

`get_organization` returns `country_code`, `currency_code`, and
`fiscal_year_start_month` as a zero-based month index (`0` = January, so the
year end is the last day of the month before the index). Read them at the
start of the close if the business context does not carry them, and use them
for every amount, the thresholds, and whether Step 9 offers `/tax-prep`. The
rule is `../../../shared/currency-and-locale.md`.

---

## Graceful degradation — Zoho Books not connected

Take this path only when no Zoho Books entry works. An unauthorized
`small-business:zoho-books` beside the owner's own live Zoho Books is connected —
call the owner's entry instead (`../../../shared/connector-neutrality.md`, "One
connector, two registrations").

Ask for **three exports**: the **Profit and Loss** report, the **Account
Transactions** report (all accounts, the month), and the **bank statement**.
The uncategorised count comes from the Banking screen; ask for it as a fourth
item or say in the packet that it was not available.

---

## Pagination and limits

`per_page` goes to 200 on invoices; the default is 10. Set it, and page on
`has_more_page`. Sums come cheaper from `response_option=3` (count and
totals only) than from listing every document.
