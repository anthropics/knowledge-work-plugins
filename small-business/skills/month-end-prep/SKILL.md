---
name: month-end-prep
description: >
  Reconciles the accounting ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho
  Books) against PayPal, Shopify, Square, and Stripe settlements, flags
  transactions that need attention, suspicious duplicates, and missing
  receipts, then writes a plain-English P&L narrative and exports a close
  packet (xlsx + one-page PDF). This is the first link of the /close-month
  command; a request to close the month or the books routes there, and the
  command runs this skill before refreshing the forecast and distributing
  the packet. Use this skill directly only when the owner wants the
  reconciliation alone, with no forecast refresh and no distribution: "just
  reconcile, no packet," "what's missing from the books," "flag the
  duplicates and missing receipts," or "write the P&L narrative for this
  month."
allowed-tools: Read, WebFetch
---

# Month End Prep

## Quick start

Connect your bookkeeping ledger and at least one payment processor, then say "let's
close the month." Claude walks you through each step of the checklist, pausing for
your input at each gate before moving forward.

Any connected ledger runs the close. Each has a reference file for its reads and
its "needs attention" signal: [reference/quickbooks-reconcile.md](reference/quickbooks-reconcile.md),
[reference/xero-reconcile.md](reference/xero-reconcile.md),
[reference/zoho-books-reconcile.md](reference/zoho-books-reconcile.md); NetSuite and MYOB
are in [reference/v2_sources.md](reference/v2_sources.md). Ledgers are peers
(`../../shared/connector-neutrality.md`): if two are connected, ask which holds the
books being closed, read the other only for what it uniquely holds, and never sum a
figure across both.

Every amount is in the business's currency (`../../shared/currency-and-locale.md`).
The thresholds below (0.50, 0.01, 25) are in that currency.

If a connector is missing, Claude falls back to asking for a CSV export — it won't
silently skip a step.

## Workflow

Work through these steps in order. Each step has a completion state; don't advance
until the current step is settled.

### Step 1 — Agree on the target month

Ask the user which month to close. Default to the prior calendar month if they don't
specify. Confirm before pulling any data.

### Step 2 — Pull the ledger's P&L and register

Fetch:
- Profit & Loss report for the target month (revenue, COGS, gross margin, operating
  expenses, net income)
- The register, as the ledger's reference file defines it. QuickBooks: the
  transaction list, every income and expense line. Xero: bills, invoices, and the
  bank-transaction queue, with that scope stated in the packet. Zoho Books: invoices,
  expenses, and purchase orders, with the P&L itself coming from an export because the
  connector has no report endpoint.

Flag immediately, using the ledger's own "needs attention" signal:
- **QuickBooks** — uncategorized lines ("Uncategorized," blank, "Ask My Accountant")
  and its Needs Review flag
- **Xero** — bank lines still unreconciled at month end
- **Zoho Books** — the `uncategorized_transactions` count on each bank account

Present the count ("14 transactions need attention") and list them for the user to
resolve in the ledger before proceeding. Don't advance with open items unless the
user explicitly says "skip for now."

See [reference/quickbooks-reconcile.md](reference/quickbooks-reconcile.md),
[reference/xero-reconcile.md](reference/xero-reconcile.md), and
[reference/zoho-books-reconcile.md](reference/zoho-books-reconcile.md) for field
mappings and API notes.

### Step 3 — Pull payment processor settlements

Fetch settlement reports from PayPal, Square, Stripe, or Shopify — whichever are
connected — for the same calendar month.

**Check the bank feed first.** When a processor pays out through a bank feed, the
payout is already a ledger line and the question is whether it has been matched.
Find unreconciled bank lines naming a processor and list them per processor as the
action items before doing any CSV match. This applies to any ledger that carries a
bank feed with a reconciled state — the usual case in Xero, and QuickBooks bank-feed
lines when the connector exposes them. MYOB holds no bank side, and Zoho Books exposes
balances but no bank-transaction list, so a MYOB or Zoho Books close goes straight to
the CSV match below.

**Compare net to net, or every line looks broken.** The ledger records the net bank
deposit; the processor's report shows the gross sale. Match those directly and every
row shows a discrepancy the exact size of the fee. Use the processor's **net payout**
(gross minus fees) — see [reference/gotchas.md](reference/gotchas.md).

Match each settlement deposit against the ledger's bank deposit line:
- **Match** — amount and date agree within 2 days → mark as reconciled
- **Difference < 0.50** — rounding/fee; note but don't flag
- **Difference ≥ 0.50** — flag with the delta amount
- **Settlement exists, no ledger deposit** — flag as "missing in the ledger"
- **Ledger deposit exists, no settlement** — flag as "deposit not in processor data"

See [reference/paypal-settlements.md](reference/paypal-settlements.md) for settlement
report field mappings (PayPal, Square, Stripe) and
[reference/v2_sources.md](reference/v2_sources.md) for Shopify.

### Step 4 — Detect suspicious duplicates

Scan the register for likely duplicate charges or deposits. Flag a transaction as a
suspicious duplicate when **all three** match:
- Same amount (within 0.01)
- Same vendor or customer name
- Posted within 5 calendar days of each other

Scan what the ledger actually holds. In QuickBooks that is the transaction list,
with split rows grouped by transaction id first. In Xero a bill keyed twice makes two
unpaid documents and no bank line, so scan bills and invoices (same contact, same
total, within 5 days, both unpaid or one paid inside the window) rather than bank
lines — the mapping is in [reference/xero-reconcile.md](reference/xero-reconcile.md).
Zoho Books is the same shape: scan invoices and expenses as documents
([reference/zoho-books-reconcile.md](reference/zoho-books-reconcile.md)).

Present flagged pairs to the user. They decide whether each is legitimate (e.g., a
recurring weekly subscription) or a real duplicate to void.

**The 5-day window is a filter, not a guarantee.** It catches the same charge keyed
twice without drowning the owner in recurring weekly bills, but a real double payment
three weeks apart slips through. Say what was scanned ("repeats within 5 days"), and
widen the window for a vendor they're suspicious about rather than calling it clean.

See [reference/gotchas.md](reference/gotchas.md) for common false-positive patterns
and how to distinguish them.

### Step 5 — Receipts check

Check the ledger first: an attachment on the transaction counts as a receipt on file
(`AttachmentCount` in QuickBooks; `has_attachments` in Xero, returned only with
`include_line_items=true`; `has_attachment` on Zoho Books invoices and expenses). Then,
if the Desktop connector is available, scan the
receipts folder (ask the user for the path; default `~/Documents/Receipts`) for the
target month.

For each expense transaction above 25 with no attached document:
- Check for a matching receipt file (match by amount ± 0.50 and date within 3 days)
- **Matched** → note as "receipt on file"
- **Not matched** → flag as "missing receipt"

List missing receipts. The user can supply the file or mark as "receipt not required"
(e.g., a recurring auto-pay with no receipt).

If Desktop connector is not available, ask the user to confirm which expenses they have
receipts for — don't silently skip this step.

### Step 5a — Payroll cross-check

Runs only when a payroll connector is connected (Gusto or QuickBooks Payroll — peers,
whichever is connected). Otherwise skip it and say the packet carries no payroll column.

Pull what was actually paid in the month, totals only:

- **Gusto** — `list_payrolls` with `include=totals`, keeping the payrolls whose
  `check_date` falls in the target month. From each `totals`: `gross_pay`,
  `employer_taxes`, `employee_taxes`, `net_pay`. Then `list_contractor_payments` for
  the same date range with `group_by_date=true`, taking `total.wages` and
  `total.reimbursements`. Contractor totals cover US contractors only — say so in the
  packet footnote.
- **QuickBooks Payroll** — `qbo_payroll_get_company_last_payroll_run` for the most
  recent run; earlier runs in the month come from the payroll summary export.
  (Confirm before the first close.)

Cross-check against the ledger: net pay plus employer taxes plus contractor wages should
appear as the month's payroll expense lines. A difference above 0.50 is a reconciliation
item — usually a run posted to the wrong month, or a payroll journal not yet posted.

**Totals only, never people.** The packet carries the month's totals and the count of
runs. No employee name, rate, or per-person amount leaves the connector — that is
payroll data, and `payroll-prep` is where it belongs. See
[reference/v2_sources.md](reference/v2_sources.md) for the field mapping.

### Step 6 — Owner sign-off gate

Present a summary before going further:

```
Needs attention (uncategorized or unreconciled):  X of X resolved
Settlement discrepancies:                        X flagged, X resolved
Suspicious duplicates:                           X flagged, X cleared
Missing receipts:                                X outstanding
Payroll cross-check:                             matched / X difference / no payroll connector
```

Ask: "Ready to write the P&L summary and export the close packet?"

**Do not proceed to Steps 7–8 without explicit confirmation.**

### Step 7 — Write the P&L narrative

Write a plain-English summary of the month — the kind an owner would share with their
spouse or accountant, not a CFO memo. Aim for 150–250 words.

Structure:
1. **Headline** — one sentence: "March came in at AUD 12,400 net, up 6% from February." Currency code, never a bare symbol.
2. **Revenue** — what drove the number; name products, services, or customers if
   the data shows concentration.
3. **Gross margin** — whether it held, rose, or compressed, and the main reason why.
4. **Key expenses** — any line that moved more than 10% MoM or is outside the normal
   range; one sentence each.
5. **Bottom line** — net income vs. prior month; ask if they have a target to compare.
6. **Watch list** — 1–3 things to monitor next month.

Avoid jargon; define anything that isn't plain English ("MoM" = month over month).

See [reference/examples/pl-narrative.md](reference/examples/pl-narrative.md) for a
worked example.

### Step 8 — Export the close packet

Produce two files:

**`close-packet-[YYYY-MM].xlsx`** — three sheets, four when a payroll connector is connected:
- `P&L` — the ledger's P&L data, formatted
- `Reconciliation` — matched and flagged transactions side by side
- `Action Items` — any outstanding flags (uncategorized, missing receipts, etc.)
- `Payroll` — the Step 5a totals beside the ledger's payroll expense, with the delta

**`close-packet-[YYYY-MM]-summary.pdf`** — one page:
- Month and business name at the top
- Key figures (revenue, gross margin %, net income)
- The P&L narrative from Step 7
- Count of open action items, if any

Save both to the Desktop (or a path the user specifies). Confirm the file locations.

See [reference/close-packet-format.md](reference/close-packet-format.md) for column
specs and PDF layout details.

Also deliver the close as a page, per the owner's stored output preference —
never default to a markdown file. Check the `## Business context` block's
`Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the close as an HTML page in the
  house style — additive to the chat summary and the files, never a
  replacement. Revenue, gross margin percent, and net income are stat tiles
  with their month-over-month change as context lines; the reconciliation
  results are a table with tabular-nums amounts; each flag carries a status
  pill — good for reconciled, warn for missing receipts and uncategorized
  items, critical for unresolved settlement gaps and duplicates; the P&L
  narrative and the open-items checklist each get a panel.
- **docx / md / notion / canva preference:** deliver the same content in that
  form — a DOCX or markdown file, a Notion page created via the connector
  (named destination, never overwriting), or a Canva Doc created via the Canva
  connector (a new design each run, named with the date; tables become
  lists); fall back to the visual artifact if Notion or Canva is not
  connected — and say that is why. The packet xlsx and PDF keep their
  formats.
- **Best for skill:** use the visual artifact — the close is reviewed on
  screen before the packet goes to the accountant.

### Step 9 — After the close

Say in one line what closed and what is still open. Then offer the single most
relevant next step, plus at most two others nearby:

- "Cash forecast" runs `cash-flow-snapshot` off the freshly closed numbers.
- "Build me a report" runs `report-builder` to publish and distribute the packet.
- "Taxes" runs `/tax-prep` when quarter or year end is near — offered only when the
  business context says Country is US, since that chain's tax math is US federal.

Max three offers. Never repeat an offer the owner declined this session.

## Approval gates

- **Never run reconciliation on a month that has been filed.** Confirm the books are
  still open before pulling data.
- **Never void or modify a ledger transaction directly.** Surface flags; the owner
  makes changes in the ledger.
- **Always pause at Step 6** before producing outputs. Unresolved flags must be
  acknowledged or explicitly skipped.
- **Never reproduce per-person pay, SSNs, or bank numbers** in the close package
  beyond the journal totals (`../../shared/personal-data.md`).

## Graceful degradation

| Missing connector | Fallback |
|---|---|
| QuickBooks | Ask for **two separate exports** — the Profit & Loss report, and the Transaction Detail by Account report. One file will not carry both; asking for "a QB export" gets you one of them and a second round trip |
| Xero | Ask for **two exports** — the Profit and Loss report, and the Account Transactions report with all accounts selected — plus the unreconciled line count from the bank reconciliation screen, which no export carries |
| NetSuite or MYOB | Ask for the P&L and the transaction detail for the month as two exports; MYOB holds no bank balances, so the bank side comes from a statement |
| Zoho Books | Even when connected, ask for the **Profit and Loss** export (no report endpoint) and a **bank statement** (no bank-transaction feed); the register and the uncategorised count come from the connector. Not connected: add the Account Transactions export |
| Payment processor | Ask for a settlement CSV from the processor's website. It must include the fee column, not just the gross amount, or the net-to-net match in Step 3 can't be done |
| Payment processor connected but returns zero payouts for the period | Treat as a data gap, not a clean zero. Say the connector returned nothing for the month, ask for the same settlement CSV (fee column included), and name the gap in the report rather than reconciling against an empty set |
| Payroll connector (Gusto, QuickBooks Payroll) | Skip Step 5a. The packet has no Payroll sheet and the summary says "no payroll connector"; the ledger's payroll expense lines still appear in the P&L unchecked |
| Desktop (receipts) | Ask the user to confirm receipt status for each flagged expense |

## More sources

Read `reference/v2_sources.md` for the mapping:

- **Shopify** — settlement reconciliation as a first-class leg. Orders, payouts, and fees each land differently, and it's a common source of unexplained gaps
- **NetSuite** — a ledger of record, common at the larger end of the segment; reports and SuiteQL supply the P&L and register
- **Xero** — a ledger of record with its own register shape (bills, invoices, bank queue) and its own attention signal (unreconciled bank lines); mapped in `reference/xero-reconcile.md`
- **MYOB** — P&L and AR/AP balances; no bank balances, so the bank side of the close comes from a statement
- **Zoho Books** — a ledger of record with a document register (invoices, expenses, purchase orders), bank balances with an uncategorised count as the attention signal, and no report or bank-feed endpoints, so the P&L and the payout match come from exports; mapped in `reference/zoho-books-reconcile.md`
- **Ramp, Expensify** — card and expense detail, which closes the gap between what was spent and what was coded
- **Gusto, QuickBooks Payroll** — payroll actually run: gross pay, employer taxes, net pay, and contractor payments as month totals, so Step 5a reconciles the ledger's payroll expense against what was paid rather than what was planned. Totals only; no per-person data enters the packet

Same close sequence, same packet. More sources reconciled.

**QuickBooks summary fields lie.** Read `../../shared/quickbooks-report-traps.md` before quoting any total from a QuickBooks summary object: the AP aging summary nets vendor credits into its buckets and can show a negative overdue figure, and the P&L summary can report expenses as zero against real rows. Total the rows, or use the detail call.

## Reference files

- [reference/quickbooks-reconcile.md](reference/quickbooks-reconcile.md) — QB field
  mappings, API pagination, common data issues
- [reference/xero-reconcile.md](reference/xero-reconcile.md) — Xero register
  definition, unreconciled-line signal, document-level duplicate scan, attachments
- [reference/zoho-books-reconcile.md](reference/zoho-books-reconcile.md) — Zoho Books
  register definition, uncategorised-count signal, what needs an export
- [reference/paypal-settlements.md](reference/paypal-settlements.md) — settlement
  report structure for PayPal, Square, and Stripe
- [reference/close-packet-format.md](reference/close-packet-format.md) — xlsx column
  specs, PDF layout, file naming convention
- [reference/gotchas.md](reference/gotchas.md) — duplicate false positives, split
  transactions, partial-month edge cases
- [reference/examples/pl-narrative.md](reference/examples/pl-narrative.md) — worked
  P&L narrative example

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
