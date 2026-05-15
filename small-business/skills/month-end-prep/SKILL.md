---
name: month-end-prep
description: >
  Walks an SMB owner through month-end close: reconciles QuickBooks against
  PayPal (and Square/Stripe) settlements, flags uncategorized transactions,
  suspicious duplicates, and missing receipts, then writes a plain-English
  P&L narrative and exports a close packet (xlsx + one-page PDF). Use when
  the user says "close the month," "month-end," "reconcile," "what's missing,"
  "P&L," or asks why revenue or margin changed this month.
---

# Month End Prep

## Quick start

Connect QuickBooks and at least one payment processor (PayPal, Square, or Stripe),
then say "let's close the month." Claude walks you through each step of the checklist,
pausing for your input at each gate before moving forward.

If a connector is missing, Claude falls back to asking for a CSV export — it won't
silently skip a step.

## Workflow

Work through these steps in order. Each step has a completion state; don't advance
until the current step is settled.

### Step 1 — Agree on the target month

Ask the user which month to close. Default to the prior calendar month if they don't
specify. Confirm before pulling any data.

### Step 2 — Pull QuickBooks P&L and transaction register

Fetch:
- Profit & Loss report for the target month (revenue, COGS, gross margin, operating
  expenses, net income)
- Transaction register: every income and expense line item

Flag immediately:
- **Uncategorized transactions** — any line with category "Uncategorized" or blank
- **Ask Questions / Needs Review** — QB's own flag

Present the count ("14 transactions need a category") and list them for the user to
classify before proceeding. Don't advance with open uncategorized items unless the
user explicitly says "skip for now."

See [reference/quickbooks-reconcile.md](reference/quickbooks-reconcile.md) for field
mappings and API notes.

### Step 3 — Pull payment processor settlements

Fetch settlement reports from PayPal, Square, or Stripe — whichever are connected —
for the same calendar month.

Match each settlement deposit against the QuickBooks bank deposit line:
- **Match** — amount and date agree within 2 days → mark as reconciled
- **Difference < $0.50** — rounding/fee; note but don't flag
- **Difference ≥ $0.50** — flag with the delta amount
- **Settlement exists, no QB deposit** — flag as "missing in QuickBooks"
- **QB deposit exists, no settlement** — flag as "deposit not in processor data"

See [reference/paypal-settlements.md](reference/paypal-settlements.md) for settlement
report field mappings (PayPal, Square, Stripe).

### Step 4 — Detect suspicious duplicates

Scan the transaction register for likely duplicate charges or deposits. Flag a
transaction as a suspicious duplicate when **all three** match:
- Same amount (within $0.01)
- Same vendor or customer name
- Posted within 5 calendar days of each other

Present flagged pairs to the user. They decide whether each is legitimate (e.g., a
recurring weekly subscription) or a real duplicate to void.

See [reference/gotchas.md](reference/gotchas.md) for common false-positive patterns
and how to distinguish them.

### Step 5 — Receipts check (Desktop connector)

If the Desktop connector is available, scan the receipts folder (ask the user for the
path; default `~/Documents/Receipts`) for the target month.

For each expense transaction in QuickBooks above $25 with no attached document:
- Check for a matching receipt file (match by amount ± $0.50 and date within 3 days)
- **Matched** → note as "receipt on file"
- **Not matched** → flag as "missing receipt"

List missing receipts. The user can supply the file or mark as "receipt not required"
(e.g., a recurring auto-pay with no receipt).

If Desktop connector is not available, ask the user to confirm which expenses they have
receipts for — don't silently skip this step.

### Step 6 — Owner sign-off gate

Present a summary before going further:

```
Uncategorized transactions:  X of X resolved
Settlement discrepancies:    X flagged, X resolved
Suspicious duplicates:       X flagged, X cleared
Missing receipts:            X outstanding
```

Ask: "Ready to write the P&L summary and export the close packet?"

**Do not proceed to Steps 7–8 without explicit confirmation.**

### Step 7 — Write the P&L narrative

Write a plain-English summary of the month — the kind an owner would share with their
spouse or accountant, not a CFO memo. Aim for 150–250 words.

Structure:
1. **Headline** — one sentence: "March came in at $X net, up/down Y% from February."
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

**`close-packet-[YYYY-MM].xlsx`** — three sheets:
- `P&L` — the QuickBooks P&L data, formatted
- `Reconciliation` — matched and flagged transactions side by side
- `Action Items` — any outstanding flags (uncategorized, missing receipts, etc.)

**`close-packet-[YYYY-MM]-summary.pdf`** — one page:
- Month and business name at the top
- Key figures (revenue, gross margin %, net income)
- The P&L narrative from Step 7
- Count of open action items, if any

Save both to the Desktop (or a path the user specifies). Confirm the file locations.

See [reference/close-packet-format.md](reference/close-packet-format.md) for column
specs and PDF layout details.

## Approval gates

- **Never run reconciliation on a month that has been filed.** Confirm the books are
  still open before pulling data.
- **Never void or modify a QuickBooks transaction directly.** Surface flags; the owner
  makes changes in QuickBooks.
- **Always pause at Step 6** before producing outputs. Unresolved flags must be
  acknowledged or explicitly skipped.

## Graceful degradation

| Missing connector | Fallback |
|---|---|
| QuickBooks | Ask for a QB export CSV (P&L + transaction detail) |
| Payment processor | Ask for a settlement CSV from the processor's website |
| Desktop (receipts) | Ask the user to confirm receipt status for each flagged expense |

## Reference files

- [reference/quickbooks-reconcile.md](reference/quickbooks-reconcile.md) — QB field
  mappings, API pagination, common data issues
- [reference/paypal-settlements.md](reference/paypal-settlements.md) — settlement
  report structure for PayPal, Square, and Stripe
- [reference/close-packet-format.md](reference/close-packet-format.md) — xlsx column
  specs, PDF layout, file naming convention
- [reference/gotchas.md](reference/gotchas.md) — duplicate false positives, split
  transactions, partial-month edge cases
- [reference/examples/pl-narrative.md](reference/examples/pl-narrative.md) — worked
  P&L narrative example
