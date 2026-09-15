---
name: close-month
description: Closes the books and turns them into a decision as a three-link chain — month-end-prep reconciles the ledger against every connected payment processor and writes the P&L narrative, cash-flow-snapshot then refreshes the 30/60/90-day forecast off the newly closed numbers rather than raw ones, and report-builder publishes and distributes the close packet. Requires a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) and uses Gusto, PayPal, Ramp, Shopify, Square, and Stripe when connected, falling back to statement or CSV uploads. Trigger on "close the month," "month-end," "close the books," "reconcile," "send the close packet to my accountant," or when the owner asks why revenue or margin moved last month. An owner who wants only the reconciliation and its flags, with no forecast refresh and no packet distribution, routes to month-end-prep directly.
allowed-tools: Read, WebFetch
---

Run the month-end chain. Close, then forecast off the closed books, then publish. The ordering is the product.

Parse arguments:
- `--month` (default: previous calendar month) — `YYYY-MM`
- `--save-to` (default `files`) — `files` (Drive / OneDrive), `desktop`, or `both`

**A ledger is required** — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, whichever is connected; they are peers (`../../shared/connector-neutrality.md`). If none is reachable, stop and say so. Reconciliation without a ledger is not a close. Offer the CSV path from `month-end-prep` rather than producing a partial packet. If two ledgers are connected, ask which holds the books being closed and name it in the packet.

## Step 1 — Close and reconcile (month-end-prep)

Run `month-end-prep` for the target month, start to finish.

- **In:** the target month.
- **Out:** the reconciliation table, the flagged items (uncategorized, suspicious duplicates, missing receipts), the P&L narrative, and the close packet XLSX plus one-page PDF.
- **Gate:** `month-end-prep`'s own Step 6 sign-off holds. The owner triages every flagged item — or explicitly skips it — before anything downstream runs.

**This step owns the numbers.** Nothing later in the chain recategorizes a transaction or restates revenue.

### The hard gate before Step 2

Do not start the forecast until the owner has signed off on the close. Say plainly what is waiting:

> "Books are closed for April — USD 3,200 in variances resolved, two receipts still missing. Ready to refresh your cash forecast off these closed numbers?"

If flagged items are still open, name them and ask whether to forecast anyway. A forecast built on eleven uncategorized transactions is a forecast built on a guess, and the owner deserves to know which they are getting.

## Step 2 — Forecast off the closed books (cash-flow-snapshot)

Run `cash-flow-snapshot` using the reconciled month as its historical base.

- **In:** the closed-month figures from Step 1 — actual AR collection timing, actual fixed costs as coded, actual settlement lag.
- **Out:** the 30/60/90-day forecast with confidence bands and named risks.
- **Gate:** none. The forecast is read-only.

**Say why this ordering matters, in the output.** A forecast run on raw books inherits every miscoded expense and every unmatched settlement. Running it after the close means the payment-timing history is real and the fixed-cost floor is right. One line is enough:

> "This forecast is built on April's closed books, so the collection timing and cost floor reflect reconciled numbers — not the raw register."

If the close surfaced something that moves the forecast — a duplicate vendor charge removed, a settlement finally matched — call out the delta against last month's forecast.

## Step 3 — Publish and distribute (report-builder)

Run `report-builder` to package and deliver the close.

- **In:** the P&L narrative and packet from Step 1, the forecast from Step 2.
- **Out:** the merged close packet — chat summary first, then the workbook. Save the definition so next month's close publishes the same pack without being described again.
- **Gate:** saving to the owner's own drive is automatic. **Sending to an accountant or anyone else is not** — draft the message, show it, and wait.

Merge, do not staple. The packet reads: what the month was, what the books say, what the next 90 days look like off those books, and what is still open.

Example, Okonkwo Mechanical: "April closed at USD 84,200, up 6% on March. Margin held at 38%. Two receipts outstanding. The 30-day forecast is USD 11,400 net at the midpoint — Rosewood's USD 12,400 is the swing."

## What not to do

- **Do not forecast before the close is signed off.** The ordering is the entire reason this is a chain.
- **Do not auto-fix a flagged item.** Show the gap, recommend the action, wait.
- **Do not delete a suspected duplicate without explicit confirmation.** Show both records side by side.
- **Do not restate a number downstream.** Step 1 owns the books; later steps cite them.
- **Do not send the packet to an accountant without approval.**
- **Do not proceed without a ledger.** Say what is missing, by category, and offer the CSV path.

## Output

End with a one-paragraph recap: revenue and margin, gaps still open, the 30-day forecast midpoint and its top risk, and the file paths. If anything was skipped rather than resolved, list it so the owner can come back to it.

Also render the merged close as one HTML artifact using the house artifact style (`../../shared/artifact-style.md`) — additive to the chat recap and the packet files, never instead of them. Revenue, margin percent, and the 30-day forecast midpoint are stat tiles with their comparison as context lines; the reconciliation and flagged items are a table with tabular-nums amounts and a status pill per row (good reconciled, warn skipped, critical unresolved); the 30/60/90 forecast gets its own panel; the open-items checklist closes the page.

## After the run

One line: the month is closed, forecast refreshed, packet published. Then the single most relevant next step, with at most two others nearby:

- If the forecast flagged a payroll risk: "can I make payroll" runs `/plan-payroll`.
- "Who owes me money?" runs `invoice-chase` on the AR the close just confirmed.
- "The weekly pack, on schedule" runs `/report-pack` so these numbers recur.

Max three offers. Never repeat an offer the owner declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
