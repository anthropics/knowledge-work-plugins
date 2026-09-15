# QuickBooks report traps

**Connector-specific.** This file documents real behaviour of one connector;
it is a gotcha list, not a preference for or against QuickBooks
(`connector-neutrality.md`). For MYOB, NetSuite, and Xero
the same read-the-rows discipline
almost certainly applies, but nothing here has been verified against them.

Seven ways a QuickBooks tool will hand you a confident, wrong number.
Every skill that calls
any QuickBooks tool — reports, aging, payroll — must apply every rule here.

The theme: **a QuickBooks tool's convenience answer — a `summary` object, a
readiness flag — is not trustworthy when the rows say otherwise. Total the
rows yourself, and believe the call that returned rows.**

---

## Trap 1 — a constrained call reports its own subset as the whole book

Aging reports must be constrained or they overflow the output limit. But the
`summary` block on a constrained call is computed over **only the rows that came
back**, and it is not labelled as partial.

Measured on the same ledger, same day:

| Call | `summary.totalReceivables` | Customers | 91+ bucket |
|---|---|---|---|
| `top_n = 10` | USD 25,907.38 | 10 | USD 0 |
| no `top_n` | USD 37,054.65 | 20 | USD 467.00 |

The top-10 call understates receivables by 30% and reports the 91-day bucket as
empty. The one genuinely bad debt on the book — the customer the skill exists to
surface — disappears silently. Nothing in the response says it was truncated.

**The rule.** A constrained call answers "who are the biggest offenders," never
"what is the total." When a skill needs both a ranked list and a true total, it
takes two calls:

1. A constrained call for the names and the ranking.
2. A separate call for the total — the balance-sheet A/R or A/P line, which is
   always the whole book and always small.

Never quote `summary.totalReceivables` or `summary.totalPayables` from a
constrained call. If only the constrained call is available, label the figure
"top N only" in the output and say so out loud.

## Trap 2 — the P&L summary reports expenses as zero

The profit-and-loss response carries a top-level summary that disagrees with its
own rows. For example:

- Rows: `Expenses` total `USD 984,590.63`
- Summary: `totalExpenses: 0`, `summaryBreakdown.expenses: 0`
- Summary: `grossProfit` equal to total income, `grossProfitMargin: 100`

`netIncome` is correct, because it is computed from the real expense figure. So
the error is invisible unless a skill reads `totalExpenses`, `grossProfit`, or
`grossProfitMargin` directly — and any skill that does will report a business
with no costs and a perfect margin.

**The rule.** Take income, expenses and COGS from the report rows, or from
`monthlyBreakdown`, which is also correct. Treat `totalExpenses`, `grossProfit`
and `grossProfitMargin` on the summary as unset. Only `netIncome` and
`totalIncome` may be read from the summary.

**Sanity check before publishing any margin figure:** a gross margin of exactly
100%, or a business showing zero expenses against real revenue, means this trap
fired. Recompute from the rows rather than reporting it.

## Trap 3 — sales by customer double-counts parents

The sales-by-customer summary returns two rows for any customer with
sub-customers underneath it: a summary row for the parent, and a separate total
row carrying the same figure. The report's own top-customer list contains both.

Read naively, a customer appears twice in the ranking and every concentration
figure derived from it is overstated. This matters most where concentration is
reported to a board.

**The rule.** Drop rows whose metadata type marks them as a total before you
rank, sum, or compute concentration. Keep the parent summary row; it is the real
one. Sales-by-**product** is unaffected — it has no parent/child structure.

---

## Trap 4 — sales by product ignores the dates you asked for

`qbo_accounting_get_sales_by_product_summary` accepts `startDate` and `endDate`
and then discards them. It always returns year-to-date, and it says so quietly:
the payload carries `"period": "This Year"` while the request asked for a
quarter.

Same call, two different ranges:

| Requested range | Returned |
|---|---|
| 2026-04-01 → 2026-06-30 | USD 36,587.65, 22 units, `period: "This Year"` |
| 2026-01-01 → 2026-01-31 | USD 36,587.65, 22 units, `period: "This Year"` |

Identical to the cent. The parameters do nothing.

This is worse than a wrong total, because it destroys every comparison built on
it. Ask for this quarter and last quarter and you get the same number twice, so
**every product's growth rate computes to exactly zero** and the trend reads as
flat no matter what actually happened. A "top and bottom performers this
quarter" section is silently a year-to-date list.

**The rule.** Never present this report as covering a period. Read `period` off
the payload and label the figures with what actually came back. When a skill
genuinely needs product revenue for a window — a quarterly review, a reorder
cycle, a price check — get it from a source that honours dates (the invoice
list, or Shopify's sales dataset for the online slice) and say which was used.
Never report period-over-period product growth from this call.

---

## Trap 5 — product detail covers a fraction of revenue

The same call returns one product, Wholesale Coffee, at USD 36,587.65. The P&L for
the same quarter reports USD 971,794.04 of income. **The product report covers 3.8%
of the business.** The rest is revenue booked without product detail — deposits,
journal entries, café takings — and it is invisible to every product-level view.

Nothing in the payload says so. `% of Sales` reads `100.0%`, because it means
100% of the rows returned, not 100% of the company.

**The rule.** Before reasoning from any product breakdown, total it and compare
against income for the same period. When the breakdown covers materially less
than the P&L, say what share it covers before the first conclusion:

> *"Product-level detail covers USD 36,588 of the quarter's USD 971,794 — about 4%.
> These rankings describe the wholesale line only, not the business."*

A margin analysis, a price recommendation, or a board-facing "top products"
section built on 4% of revenue while implying it describes the whole company is
the same error as a 100% gross margin, arriving by a different door.

---

## Trap 6 — the AP aging summary nets vendor credits into the buckets

`qbo_accounting_get_ap_aging_summary` subtracts a vendor's credits (credit
memos, overpayments, returns) inside the aging buckets instead of showing
them separately. A vendor with a large credit drags a whole bucket negative,
and the report's overdue total goes with it. For example, an overdue total of
**USD -10,976.21**. The detail call for the same day
(`qbo_accounting_get_ap_aging_detail`) lists every open bill and credit as
its own row with the right sign.

**The rule.** The summary is not a source for anything, including a
ranking: its per-vendor totals are already netted, so a vendor with USD 2.4M
overdue and a USD 1.5M credit ranks at USD 911k. For what is overdue, what is
due this week, what a vendor is owed, and who is owed the most, read the
detail report and total the rows yourself: bills by due date, credits kept
apart and reported as credits. Constrain it (Trap 1): `due_before` for a
window, `vendor_name` for one vendor; the whole-book total is the balance
sheet's A/P line. A negative figure anywhere in a summary means this trap
fired; say the vendor holds a credit rather than reporting negative overdue
money.

This is the payables twin of `ap-processor`'s "a vendor total is a net figure"
rule, which applies the same reading to any aging source.

---

## Trap 7 — payroll readiness contradicts the employee list

`qbo_payroll_get_company_payroll_readiness` and `qbo_payroll_get_employees`
are answered from different places, and they disagree. On one
company, same minute:

| Call | Answer |
|---|---|
| `qbo_payroll_get_employees` | `total_count: 50` |
| `qbo_payroll_get_company_payroll_readiness` | `has_employees: false`, `run_payroll_ready: false` |

This is not thin data — fifty employees came back — it is the readiness
tool reporting a state its sibling disproves. It is a different failure from
a payroll source that simply returns nothing,
and `payroll-prep` treats the two differently.

**The rule.** Read both calls. Take the roster from the employee list, since
it is the call that returned rows. Never stage a run while readiness says
not ready, whatever the list says. Say both answers to the owner in one line
so the contradiction is on record, and raise it with the connector rather
than working around it.

---

## Also worth knowing

**COGS may be empty even when costs exist.** Costs booked to an operating
expense account never reach `totalCogs`, so gross margin reads 100% while the
business plainly has costs. When `totalCogs` is 0 and expenses are not, say the
books have no cost-of-goods split rather than reporting a 100% margin.

**The connector cannot write purchases.** QuickBooks' write surface is
sales-side only: invoices, estimates, customers, products, payment links,
recurring invoices, payroll. There is no create-bill, create-vendor or
create-expense tool. A skill must never offer to enter a bill, create a vendor,
or record an expense in QuickBooks — it can only read them and stage the work
elsewhere.
