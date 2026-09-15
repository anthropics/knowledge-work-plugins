# More sources

More systems reconciled. Same close sequence, same packet.

---

## Ledger — whichever is connected

Ledgers are peers (`../../../shared/connector-neutrality.md`). Whichever is connected runs the close.

| Source | What it supplies |
|---|---|
| MYOB | P&L, AR and AP balances, sales totals. No bank balances: the bank side comes from a statement upload |
| NetSuite | P&L and register via reports and SuiteQL. Common at the larger end of the segment |
| QuickBooks | P&L and transaction list; mapped in [quickbooks-reconcile.md](quickbooks-reconcile.md) |
| Xero | P&L, bills, invoices, bank-transaction queue; mapped in [xero-reconcile.md](xero-reconcile.md) |
| Zoho Books | Invoices, expenses, purchase orders, customer payments, bank and cash balances with an uncategorised count per account. No bill object, no bank-transaction feed, no report endpoints: the P&L and the bank statement come as exports; mapped in [zoho-books-reconcile.md](zoho-books-reconcile.md) |

**Two ledgers connected: read both, total from one.** Ask which holds the books being closed and name it in the packet as the source of record. Read the other for anything it uniquely holds (a bank feed the first one lacks, a bill register), but every total, and the reconciliation itself, runs against the named ledger. Never reconcile against both, and never sum a figure across two — that double-counts.

---

## Shopify settlement reconciliation

A first-class leg, and a common source of unexplained gaps.

The trap: an order, its payout, and its fees all land on different dates and in different amounts. Reconciling gross order value against a net payout will never tie, and the difference is not an error.

Pull three things separately:

- **Orders** — gross, by date
- **Payouts** — net, by settlement date
- **Fees and refunds** — the difference between the two

Then reconcile payout to bank, and orders to revenue. Those are two different reconciliations and conflating them produces a phantom discrepancy every month.

If the payout read fails (the connector's scopes exclude Shopify Payments), the orders-to-revenue leg still runs; the payout-to-bank leg takes the payout report the owner exports from Shopify, or is listed as not reconciled this month. Say which.

```
Shopify: USD 38,400 in orders, USD 36,910 paid out, USD 1,490 in fees and refunds.
Payouts tie to the bank. Fees are coded to merchant fees.
```

---

## Ramp and Expensify

Card spend and expense detail. These close the gap between what was actually spent and what has been coded.

Pull outstanding transactions and unsubmitted expenses, and flag anything uncoded as an open item in the close packet rather than letting it disappear:

```
Open items:
  USD 4,180 in Ramp card spend, 23 transactions, not yet coded
  USD 610 in Expensify reports submitted but not approved
```

An owner who closes the month without seeing those closes on a number that is wrong.

Two things to hold on to while pulling them:

- **Expensify is read-only search.** It reports expenses, reports, receipts, and approval states; it changes nothing. The has-receipt filter is what surfaces the substantiation gap — "USD 2,140 across 17 expenses with no receipt attached" is a close-packet line an accountant will actually use.
- **Ramp can write, and the close is not where it writes.** Approving a bill or marking it ready to sync belongs to `ap-processor` behind its own payment gate. Here, Ramp is read only: card spend, bill status, and account balances. Reimbursements overlap Expensify — count them once.

---

## Payroll — whichever is connected

Gusto and QuickBooks Payroll are peers. Step 5a reads the month's totals from
whichever is connected and checks them against the ledger's payroll expense.

**Gusto.** Two reads:

| Read | Parameters | Fields used |
|---|---|---|
| `list_payrolls` | `include=totals`; filter on `check_date` within the month (the list may also carry `pay_period.start_date` / `end_date`) | `totals.gross_pay`, `totals.employer_taxes`, `totals.employee_taxes`, `totals.net_pay`, `check_date` |
| `list_contractor_payments` | `start_date`, `end_date` = first and last day of the month; `group_by_date=true` | `total.wages`, `total.reimbursements` |

Keep only processed payrolls; an unprocessed run in the list is a plan, not a
payment, and belongs to `payroll-prep`. Contractor payments cover US
contractors only — say so in the footnote when the row is non-zero, and say it
is absent when the business pays international contractors.

**QuickBooks Payroll.** `qbo_payroll_get_company_last_payroll_run` returns the
most recent run with its totals; runs earlier in the month are in the payroll
summary export. Confirm the field names before the first close.

**The cross-check.** Net pay + employer taxes + contractor wages, compared to
the ledger's payroll expense lines for the month:

```
Payroll (Gusto): 2 runs, GBP 18,420 gross, GBP 1,660 employer taxes,
GBP 14,210 net. Contractors: GBP 2,400.
Ledger payroll expense: GBP 18,270. Delta GBP 150 — the 28 Mar run posted to April.
```

**What never enters the packet:** employee names, rates, hours, deductions,
home addresses, or any per-person amount. The connector returns them; the
close does not need them and does not reproduce them.

---

## What doesn't change

- The reconcile sequence, the P&L narrative, and the close packet format
- Duplicate detection and split-transaction handling
- The CSV and statement-upload path, which still produces a full close
- Never invent a number. An unavailable source is named as unavailable, and the packet says so

---

## Naming the sources in the packet

The close packet gets forwarded to accountants and lenders. It has to say what it was built from and what wasn't available:

```
Reconciled: Xero (ledger: bills, invoices, and bank transactions), Shopify
(settlements), PayPal, Ramp (cards).
Not available: Stripe — auth expired Jul 24. Stripe activity is not included
in this close.
```

Name the ledger and, where its register was assembled from parts, say which parts.

The second line protects the owner. A close packet that silently omits a processor is worse than one that says it did.
