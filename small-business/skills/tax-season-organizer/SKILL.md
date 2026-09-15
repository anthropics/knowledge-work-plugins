---
name: tax-season-organizer
description: >
  Prepares tax-season materials for the owner's accountant, not tax advice.
  US federal tax; a non-US business gets its closed-books packet instead. Two
  modes: (1) quarterly estimated tax from YTD net income in the ledger (MYOB,
  NetSuite, QuickBooks, Xero, or Zoho Books); (2) year-end 1099 prep, scanning
  the ledger, PayPal, and Stripe for contractors paid over USD 600 into a
  1099-NEC list with missing W-9 flags.

  Any tax request routes first to /tax-prep, which confirms the books are
  closed and reconciled before running this skill. Use this skill directly
  only when the owner says the period's books are already closed: "books are
  closed, now do the 1099s," "run the quarterly estimate off the closed
  numbers," or "just the contractor W-9 list."
allowed-tools: Read, WebFetch
---

# Tax Season Organizer

> **Framing:** This skill produces prep material for a CPA, not tax advice. Say so early
> and state every assumption explicitly so the accountant can adjust.

## Quick start

Determine which mode the user needs, pull the relevant data, calculate or compile,
and deliver a structured document the accountant can work from directly.

```
User: "what do I owe for estimated taxes this quarter?"
→ Pull YTD P&L from QuickBooks
→ Calculate estimated federal income tax + SE tax
→ Subtract payments already made this year
→ Show Q-specific amount due with due date and assumptions stated
→ Output: "Estimated Q2 payment due June 16: USD X — see full breakdown below"

User: "I need to send out 1099s"
→ Pull all contractor/vendor payments from QuickBooks + PayPal + Stripe
→ Identify contractors paid ≥ USD 600 YTD
→ Flag records missing W-9 / EIN
→ Output: 1099-NEC candidate list + missing W-9 action list
```

## Step 0 — Check the country first

Both paths below are **US federal tax**: self-employment tax, the federal bracket table, 1099-NEC and W-9. Before choosing a mode, read `Country` from the `## Business context` block (rule: `../../shared/currency-and-locale.md`). If it is absent, ask.

- **US** → continue to Determine mode.
- **Anything else** → say so in one line and stop the US math: *"The quarterly-estimate and 1099 paths here are built for US federal tax. Your books are in the UK, so I'll get your closed-books packet ready for your accountant instead of a US estimate."* Then offer `/close-month` for the periods in scope. Do not run a US calculation on a non-US business, and do not relabel one as a generic estimate.

Every amount in the output is in the business's currency code; the USD 600 line is US law and is named as such.

## Determine mode

Read the user's message and context to decide which path applies:

- **Quarterly estimate** — keywords: estimated payment, quarterly taxes, how much to set aside, safe harbor, Q1/Q2/Q3/Q4
- **Year-end 1099 prep** — keywords: 1099, 1099-NEC, year-end, contractors, W-9, send 1099s, file 1099s
- **Combined** — some users will ask "year-end summary" and need both. Run quarterly last; run 1099 prep first since it drives the most action items.

If the intent is ambiguous, ask: "Are you looking at your estimated tax payment for this quarter, or are you preparing 1099s for your contractors — or both?"

---

## Path 1: Quarterly estimated tax

### 1. Pull YTD financials

Use the connected ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books — peers, per `../../shared/connector-neutrality.md`) to pull a Profit & Loss report from January 1 of the current year through the last day of the most recently completed quarter. Capture:
- **Gross revenue** (total income)
- **Total expenses** (operating expenses, COGS, etc.)
- **Net ordinary income** = revenue − expenses

If no ledger is connected, ask the user to upload a P&L as CSV or paste the key numbers. For field names and query approach per ledger, see [reference/connector-queries.md](reference/connector-queries.md).

### 2. Ask about prior estimated payments

Before calculating, ask: "How much have you already paid in estimated taxes so far this year?" If the user doesn't know, note that you'll calculate total liability — they can subtract payments themselves or check with their accountant.

### 3. Calculate estimated liability

See [reference/calculation-assumptions.md](reference/calculation-assumptions.md) for the full math and the assumptions table you must include in output.

**First, annualize.** The math runs on projected full-year net profit, not YTD:
`annualized net = YTD net ÷ months elapsed × 12`. Show both, labeled. Seasonal
business: ask rather than straight-lining.

Short version, all six steps running on **annualized** net profit:
1. **SE tax** = annualized net profit × 0.9235 × 0.153 (then halve it — the deductible half offsets income)
2. **Adjusted net** = annualized net profit − (SE tax / 2)
3. **Federal income tax** = apply the bracket rate appropriate to the user's business type and estimated annual income (default to 22% unless the user tells you their bracket; note this assumption explicitly)
4. **Total annual liability** = federal income tax + SE tax
5. **Quarterly payment** = (total annual liability − payments made) ÷ quarters still ahead
6. **Safe harbor check** — note whether the user should verify against prior-year tax (100% of prior year, or 110% if AGI > USD 150k)

**If a due date has already passed unpaid**, name it and show the catch-up on its own
line, separate from the next payment. Penalty and interest go to the accountant — flag
that they apply, never estimate them. With no quarters left, it is due with the return.

### 4. State assumptions and deliver output

The full section-by-section document structure is in
[reference/output-formats.md](reference/output-formats.md).

Two things that are not negotiable: the **tax year appears in the header**, and the
**Assumptions section lists every assumption** — bracket rate, business structure, state
taxes excluded, deductible SE half, and the deductions not applied. The accountant adjusts
from those levers, so leaving one out costs them a rebuild.

---

## Path 2: Year-end 1099 prep

### 1. Pull contractor payments from all sources

Query each connected source for **all payments made to individuals or businesses for services** in the tax year. Do not include payments for goods, refunds, or internal transfers.

**The ledger — try the live connector first, fall back to a CSV export.** QuickBooks
may return only category-level totals with no payee breakdown, in which case you need the
user to export a Transaction List by Vendor. Xero supplies bills and payments by contact,
and a 1099 report summary for US organisations. The detection logic, the exact wording to
ask with, and the column mapping per ledger are in
[reference/connector-queries.md](reference/connector-queries.md).

**PayPal:** Pull all "Goods & Services" payments sent. Note: PayPal issues its own 1099-K to contractors above the threshold — flag these separately in output so the accountant can determine whether a 1099-NEC is also needed.

**Stripe:** Pull all transfers/payouts made to external parties. Same 1099-K caveat as PayPal applies.

**Square:** holds no payments to external parties through the connector (payouts go to the owner's own bank; contractor pay is in Square Payroll, which it does not reach). Name it as a source with nothing to contribute rather than dropping it silently; the 1099-K note applies to the business's own receipts. Detail in [reference/connector-queries.md](reference/connector-queries.md).

**Desktop/CSV:** If the user uploads a CSV directly (without going through QuickBooks export), map columns: payee name, amount, date, payment method, EIN/SSN status.

### 2. Aggregate by payee

Combine across sources and sum payments by individual or business entity. Deduplicate by name (watch for "John Smith" vs "John A. Smith" — flag likely duplicates for human review rather than auto-merging).

### 3. Apply the USD 600 threshold

- **Flag for 1099-NEC:** any payee paid ≥ USD 600 for services (contractors, freelancers, consultants)
- **Flag for 1099-MISC:** any payee paid ≥ USD 600 for rent, attorney fees, prizes/awards
- **Near-threshold alert:** flag payees paid USD 400–USD 599 — close to the threshold, accountant may want to verify

Corporations (Inc., Corp., LLC taxed as C or S corp) generally do not need a 1099-NEC — note this but flag for accountant confirmation.

### 4. Check W-9 status

For each flagged payee, note whether a W-9 / EIN is on file in the ledger. Mark as:
- ✅ W-9 on file (EIN/SSN recorded in the ledger's vendor or contact record)
- ⚠️ Missing — W-9 not on file; must collect before filing
- ❓ Unknown — cannot determine from available data

### 5. Deliver the 1099 prep package

The full section-by-section structure is in
[reference/output-formats.md](reference/output-formats.md).

The parts that carry the most weight: the **missing-W-9 action list**, because those block
filing and the deadline is January 31, and the **payment processor note**, because a
contractor paid only through PayPal or Stripe may already be getting a 1099-K and the
accountant has to decide whether a 1099-NEC is also needed.

---

## Guardrails

- **Name the tax year in every output.** The brackets, wage base, and due dates in
  [reference/calculation-assumptions.md](reference/calculation-assumptions.md) are
  **2025 figures**. Preparing a different year: say so loudly before showing any number,
  then cite current figures from IRS.gov or ask the owner. **Never invent a bracket,
  a wage base, or a due date.**
- **Not tax advice.** Open every deliverable with this: "Prepared for review by your accountant — not tax advice." Include it in the document header, not just in chat.
- **State every assumption.** If you assumed a 22% bracket, say so. If you excluded state taxes, say so. The accountant will adjust; give them the levers.
- **Don't merge payees automatically.** Flag likely duplicates for human review.
- **Don't file anything.** The output is prep material. Filing is out of scope.
- **Corporation exemption is a judgment call.** Note it; don't auto-exclude.
- **Never reproduce a contractor's SSN or a full bank or card number** in the packet, the chat, or a rendered page. A business EIN on a 1099 is the one designed exception (`../../shared/personal-data.md`).

## More sources

- **Gusto** — payroll actually run: wages, withholdings, and contractor payments. This deepens both modes — quarterly estimates stop guessing at payroll figures, and 1099 prep can reconcile contractor payments against what Gusto already filed. When Gusto shows a 1099 was already issued for a payee, flag it rather than double-preparing.
- **Xero** — P&L for the quarterly path; bills and payments by contact for the payee list; and, for a US organisation, a 1099 report summary that is the expected output of Path 2 in one read. Queries in `reference/connector-queries.md`.
- **Ramp, Expensify** — card spend and expense detail for the deduction side of the quarterly estimate, and vendor payment detail that helps confirm the 1099 list is complete. Expensify's receipt filter finds the expenses that will not survive substantiation, which is the flag an accountant most wants before filing.
- **MYOB** — P&L only, for MYOB shops. Read-only, three financial years of history, **and no contractor or vendor payee detail** — so it feeds the quarterly estimate and plays no part in 1099 prep.

Same tax math, same accountant packet. More sources, fewer assumptions to state.

## Output

**Deliver the estimate or 1099 package per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the summary as an HTML page in the house style — the estimate or 1099 count as the lead stat tile, the assumptions table, missing W-9s as rows with a pill each, and the deadline up top. Open with the not-tax-advice line. The accountant documents themselves keep the structure in `reference/output-formats.md`.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a status page over accountant-bound documents.

## After the packet

The estimate or the 1099 package is in the accountant's hands, assumptions stated. The natural next step is "close the month" — `/close-month` keeps the next estimate running on reconciled numbers instead of the raw register. Also nearby: "cash forecast" (`cash-flow-snapshot`) to confirm the payment clears on its due date, and "who owes me money" (`invoice-chase`) if collections need to cover it. Offer at most three, and skip any offer the owner already declined this session.

## Reference files

- [reference/calculation-assumptions.md](reference/calculation-assumptions.md) — full tax math, 2025 bracket table, SE tax walkthrough, YTD-vs-annualized, missed quarters
- [reference/output-formats.md](reference/output-formats.md) — document structure for both the quarterly summary and the 1099 package
- [reference/connector-queries.md](reference/connector-queries.md) — how to pull data from each ledger (MYOB, NetSuite, QuickBooks, Xero, Zoho Books), PayPal, Square, and Stripe, including the vendor-level fallback
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for common failure modes
- [reference/examples/quarterly-estimate.md](reference/examples/quarterly-estimate.md) — worked quarterly estimate example
- [reference/examples/year-end-1099.md](reference/examples/year-end-1099.md) — worked year-end 1099 prep example

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
