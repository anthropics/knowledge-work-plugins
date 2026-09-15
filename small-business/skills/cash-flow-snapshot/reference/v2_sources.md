# More sources

Additional data legs into the same forecast model. The logic is unchanged — these widen what it can see.

Pull everything in one parallel batch. A forecast that touches five systems serially is a forecast the owner stops waiting for.

---

## Ledger sources — whichever is connected

Ledgers are peers (`../../../shared/connector-neutrality.md`). Whichever is connected supplies the ledger legs.

| Source | What it supplies |
|---|---|
| MYOB | **AR and AP legs only** — read-only, no bank or cash balances, and reporting reaches back three financial years |
| NetSuite | AR, AP, fixed costs, and the cash balance, via reports and SuiteQL |
| QuickBooks | AR aging, AP in two calls: the balance sheet's A/P line for the total, and `qbo_accounting_get_ap_aging_detail` with `due_before` set to the forecast horizon for the timing of what leaves (rows bucketed by due date, credits kept apart); the AP aging summary nets vendor credits and goes negative, so it is never the source, and an unconstrained detail call overflows (Trap 1). Plus recurring costs and the balance sheet |
| Xero | Aged receivables, bills, bank account balances, and the organisation record (currency, financial year) |
| Zoho Books | Cash from `list_bank_accounts` (`current_balance`, summed across active accounts); AR from `list_invoices` `status=unpaid` with `due_date` per invoice (`response_option=1` for the summed balance); AP from open `list_purchase_orders` plus `list_expenses` `status=unbilled`; the organisation record via `get_organization`. **No bill object and no cash-flow report:** recurring fixed costs come from the owner or from recurring expenses, and the forecast is built from invoice due dates and purchase-order expected dates, not from a ledger projection — say so in the sources line |

**Two ledgers connected: read both, total from one.** Ask which is the source of record, say which in the output, and take every total (opening balance, AR, AP) from that one. Read the other only for detail it uniquely holds. Never sum the same figure across two ledgers.

**MYOB is the one ledger that cannot give you the opening balance.** Pull AR aging, payables, sales totals, and standard payment terms from it, then ask the owner for the bank balance or take it from a processor. Heading the forecast "no opening balance — net change only" is the honest outcome when nobody can supply one.

From the ledger: AR aging with due dates, AP with due dates, recurring fixed costs, and the cash balance.

---

## Shopify — inflow timing

For a commerce business this is often the largest single inflow, and it does not arrive when the order does.

Pull orders, payouts, and the payout schedule. The gap between order date and payout date is the thing that matters — a business with USD 40,000 in orders this week and a two-day payout delay has a very different 30-day picture than one on a weekly settlement cycle.

Model the payout dates, not the order dates. Using order dates makes a forecast that is optimistic by exactly the settlement lag, every time.

**Payouts may not be readable.** The Shopify connector's scopes exclude Shopify Payments, so payout reads fail while orders succeed. When that happens, ask the owner for their payout schedule (daily, weekly, the lag in days) and model from that, and say in the Sources line that the timing came from the owner. Never infer a settlement lag from order dates or from another store's norm.

---

## Ramp — the spend that hasn't landed

The most common reason a cash forecast is quietly wrong: card spend that has been made but not yet coded into the books.

Pull outstanding card transactions and unsubmitted expenses. Add them as a known outflow even where they have no ledger entry yet.

**Ramp also answers the opening-balance question.** It exposes business and treasury account balances with history. For an owner banking on Ramp that turns "what's in the account right now" from a question into a sourced figure — which is the difference between a payroll answer and a payroll guess.

Reimbursements pulled from Ramp may also live in the owner's expense tool (Expensify). Count them once.

Say what was added and where it came from:

```
Outflows include USD 4,180 in card spend from Ramp that hasn't hit QuickBooks
yet. Without it this forecast would be about USD 4k optimistic.
```

That sentence is often the single most useful line in the output.

---

## What doesn't change

- Confidence bands still come from each customer's historical payment variance
- Risk flags still name the specific customer, amount, and days overdue
- The CSV path is still fully supported and still produces the same forecast
- Never invent a number. A source that returned nothing is reported by name as unavailable

---

## Reporting sources

Always say what the forecast was built from. Owners take these to lenders, and "based on QuickBooks and Shopify payouts through Jul 27" is what makes it defensible.

List anything unavailable too:

```
Built from: QuickBooks (AR, AP, fixed costs), Shopify (payout timing), Ramp
(uncoded card spend).
Not available this run: Stripe — auth expired. Any Stripe revenue is missing
from these inflows.
```

The second half matters more than the first. An owner who knows what's missing can judge the number. One who doesn't will trust it completely.
