---
name: cash-flow-snapshot
description: >
  Reads AR/AP, historical cash timing, and known fixed costs from the ledger
  (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) or from PayPal, Square, or Stripe — or
  a CSV upload — and produces a 30/60/90-day cash flow forecast with
  percentage-variance confidence bands and named risk flags. Delivers a chat
  summary and a downloadable XLSX. Use when the user asks "forecast my cash
  flow," "will I make payroll," mentions "runway," or says "cash crunch."
  Falls back to CSV upload when no connector is live.
compatibility: "Requires one or more of: a ledger MCP (MYOB, NetSuite, QuickBooks, Xero, Zoho Books), PayPal MCP, Shopify MCP, Square MCP, Stripe MCP, file upload (CSV fallback). Output uses xlsx skill."
allowed-tools: Read, WebFetch
---

# Cash Flow Snapshot

Produces a 30/60/90-day cash flow forecast with percentage-variance confidence
bands and named risk flags. Delivers a two-part output: a concise chat summary
and a downloadable XLSX workbook.

**Quick start**

> "Will I make payroll next month?"

Claude pulls the current bank balance, AR/AP, and fixed costs from connected
sources, calculates expected inflows and outflows across 30, 60, and 90-day
windows, applies confidence bands from each customer's payment variance, and
flags specific risks by name.

---

## Workflow

### Step 1 — Identify available data sources

Check which connectors are live. Pull from every one that is, in one batch:

1. The ledger — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, whichever is connected — for AR aging, AP, fixed costs, and the cash balance. Ledgers are peers (`../../shared/connector-neutrality.md`); if two are connected, ask which is the source of record and take totals from that one only
2. PayPal — transaction history and settlement timing
3. Square — sales and payout history
4. Stripe — charge and payout history
5. Shopify — orders (`list-orders`) as the inflow, plus payout timing. Shopify on its own is enough to run: for a commerce business it is often the largest inflow. The payout read may fail because the connector's scopes exclude Shopify Payments — then ask the owner for their payout schedule and model from that; never infer a lag (`reference/v2_sources.md`)
6. CSV upload — when no connector is connected

If no connector is live and no file is attached, ask the user to either connect
a source or upload a CSV (income/expense tabular data, any reasonable format).
Note which sources were used in the output — this affects confidence band width.

**Always establish the starting cash balance** — "will I make payroll" is a
question about the balance, not the net. Pull it in Step 2, or ask: "What's in
the business account right now, and as of what date?" **Never assume one.** If
nobody knows, head the output "no opening balance — net change only" and drop
cash-on-hand from the risk flags.

### Step 2 — Pull the data

**From the ledger:**
- Balance sheet: bank and cash balances with the as-of date — the opening balance
  (MYOB holds none; see `reference/v2_sources.md`)
- AR aging report: customer name, invoice amount, invoice date, due date, days outstanding
- AP: vendor name, amount due, due date
- Recurring fixed costs: rent, payroll, subscriptions (look for recurring transactions)

**From Gusto, when connected:**
- The next payroll run's date and expected amount, and the regular pay-schedule
  cadence — the real numbers for the biggest fixed cost, instead of inferring
  payroll from recurring transactions. When Gusto and the ledger disagree on
  payroll, trust Gusto for timing and amount and say so in the output

**From PayPal / Stripe / Square:**
- Settlement history: transaction date, amount, settlement date
- Use settlement lag (transaction date → payout date) to compute each source's
  average and variance payment delay

**From CSV upload:**
- Parse as income/expense tabular data
- Required columns (flexible naming): date, amount, type (income or expense), description
- If columns are ambiguous, show the header row and ask the user to confirm mapping

### Step 3 — Compute historical payment timing

For each AR customer (or income source from CSV), calculate:
- **Mean payment lag** — average days from invoice/transaction date to receipt
- **Payment variance** — standard deviation of payment lag across last 6–12 payments
- Use variance to set confidence band width (see Step 4)

If fewer than 3 payments exist for a customer, use the population mean as the
point estimate and apply a ±30% variance band as the default. When running on
CSV data with sufficient history (≥3 payments per source), compute the band
from the actual payment variance — do not assume ±30%.

### Step 4 — Build the 30/60/90-day forecast

Produce three time windows: 0–30 days, 31–60 days, 61–90 days.

For each window, compute:

| Line | Method |
|---|---|
| Expected inflows | AR due in window, adjusted for mean payment lag |
| Expected outflows | AP due in window + fixed costs falling in window |
| Net cash position | Inflows − Outflows |
| Confidence band | ± weighted average payment variance as a % of expected inflows |

Confidence band formula:
```
band_pct = weighted_avg_stddev_days / avg_payment_lag_days
low  = net_cash × (1 − band_pct)
high = net_cash × (1 + band_pct)
```

Round band_pct to one decimal place. Cap at ±50% — higher variance means the
data is too thin to model; flag it instead (see Step 5).

### Step 5 — Flag named risks

Scan for conditions that push the low-band estimate negative or create a
liquidity crunch. For each risk found, produce a one-line flag:

- **Late-payer risk:** "Customer X historically pays 18 days late; that shifts
  their USD 8,400 invoice out of the 30-day window into day 48."
- **Payroll crunch:** "Payroll (USD 22,000) hits April 15. Opening balance USD 31,000
  on April 1, plus inflows, minus outflows, puts low-band cash on hand April 14
  at USD 19,200. Shortfall risk: USD 2,800." Needs a sourced balance.
- **Thin data warning:** "Only 2 payments on record for Customer Y — confidence
  band set to default ±30%."
- **No-connector warning:** "Running on CSV data only — no real-time AP or
  recurring cost data. Confidence bands are wider than normal."

Limit to the top 5 risks by severity (largest dollar impact first).

### Step 6 — Deliver outputs

**Chat summary** (always). Use a markdown table for the forecast, not a fenced
code block — the chat surface renders markdown tables; a fenced block shows up
as raw monospace text. Shape:

- Title line: Cash Flow Snapshot — <date range>
- Source(s): <connectors used>
- Opening balance: AUD X,XXX as of <date> (or: none on file — net change only)

Then the forecast as a markdown table, amounts carrying the business's currency
code (`../../shared/currency-and-locale.md`), never a bare symbol:

| Window | Expected | Low | High |
|---|---|---|---|
| 30-day net | AUD X,XXX | AUD X,XXX | AUD X,XXX |
| 60-day net | AUD X,XXX | AUD X,XXX | AUD X,XXX |
| 90-day net | AUD X,XXX | AUD X,XXX | AUD X,XXX |

Then risks as a short bulleted list under "⚠ Risks flagged: <count>".

**XLSX workbook** (always): read `xlsx/SKILL.md` first, then produce three sheets:

1. **Summary** — the 30/60/90 forecast table with confidence bands. Beneath
   each window row, expand inline sub-rows showing the individual transactions
   that make up its inflows (green) and outflows (red). This makes the estimates
   auditable without leaving the Summary sheet.

2. **Detail** — all transactions grouped by window, sorted by date within each
   group. Include a running net column (cumulative inflows minus outflows within
   the window) and a subtotal row at the bottom of each window showing total
   inflows, total outflows, and net. Grey out past transactions in a separate
   section at the bottom for reference. Ensure all three windows have rows even
   if one is empty — show a "No transactions in this window" placeholder row.

3. **Risks** — the flagged risks with dollar impact and affected window.

Save as `cash-flow-snapshot-[YYYY-MM-DD].xlsx`.

**The forecast page** (always, alongside the chat summary — never instead of
it), delivered per the owner's stored output preference — never default to a
markdown file. Check the `## Business context` block's `Output preference`
(shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the full forecast as an HTML page
  in the house style. The 30/60/90-day nets are stat tiles with the confidence
  range as each tile's context line; the transaction detail is a table with
  right-aligned tabular-nums amounts; each risk flag carries a status pill —
  critical for a projected shortfall, warn for late-payer and thin-data flags;
  sources and opening balance sit in a small header panel.
- **docx / md / notion / canva preference:** deliver the same content in that
  form — a DOCX or markdown file, a Notion page created via the connector
  (named destination, never overwriting), or a Canva Doc created via the Canva
  connector (a new design each run, named with the date; tables become
  lists); fall back to the visual artifact if Notion or Canva is not
  connected — and say that is why. The XLSX still ships alongside.
- **Best for skill:** use the visual artifact — a forecast is read at a glance
  and re-run often.

---

## After the run

One line on what just happened: the forecast is built and the risks are named.
Then offer the single most relevant next step, plus at most two others nearby:

- If a payroll crunch was flagged: "can I make payroll" runs `/plan-payroll`.
- "Who owes me money?" runs `invoice-chase` to pull collections forward.
- "Close the month" runs `/close-month` so next forecast runs on clean books.

Max three offers, and never repeat an offer the owner declined this session.

## Approval gates

This skill is read-only — no approval gate before generating the forecast.

Remind the user after delivery:
> "This forecast is based on [sources listed]. It is not a substitute for
> accounting advice — verify with your bookkeeper before making financing decisions."

---

## More sources, and a schedule

Read `reference/v2_sources.md` for the full mapping:

- **Shopify** — payments inflow timing, which is often the largest single inflow for a commerce business and settles on a delay worth modeling
- **NetSuite** — a ledger of record, common at the larger end of the segment: AR, AP, fixed costs, and the cash balance via reports and SuiteQL
- **Xero** — a ledger of record: aged receivables, bills, bank balances, and the organisation's currency and financial year
- **Ramp** — card spend that hasn't hit the books yet, which is the most common reason a forecast is quietly optimistic
- **Ramp balances** — real business and treasury account balances with history. When the owner banks with Ramp this is a sourced opening balance rather than a number they had to remember
- **MYOB** — AR and AP legs for MYOB shops. Read-only, and it holds **no bank or cash balances at all** — never source an opening balance from it

Nothing about the forecast logic changes. These are additional legs into the same model.

### Running on a schedule

This skill is schedulable. The monthly preset is a cash heads-up before the month turns.

Offer it once, after a forecast the owner found useful:

```
Want this monthly, a few days before month end? That's when it's most useful,
and it's the same forecast you just got.
```

Scheduling is a property of this skill. There is no separate command for it.

**QuickBooks summary fields lie.** Read `../../shared/quickbooks-report-traps.md` before quoting any total from a QuickBooks summary object: the AP aging summary nets vendor credits into its buckets and can show a negative overdue figure, and the P&L summary can report expenses as zero against real rows. Total the rows, or use the detail call.

## Reference files

| File | Load when |
|---|---|
| `reference/gotchas.md` | When a connector returns unexpected data or variance is extreme |
| `reference/examples/worked-example.md` | When modeling the output format for a new data shape |

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
