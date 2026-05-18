---
name: tax-season-organizer
description: >
  Prepares tax-season materials for small business owners — framed as deliverables
  for their accountant, not tax advice. Two modes: (1) quarterly estimated tax
  calculation — pulls YTD net income from QuickBooks and calculates the federal
  income tax + self-employment tax liability and quarterly payment due; (2)
  year-end 1099 prep — scans QuickBooks, PayPal, and Stripe for contractors paid
  over $600, builds a 1099-NEC candidate list with missing W-9 flags, and
  produces a plain-English summary a CPA can work from directly.

  Trigger this skill whenever the user mentions: quarterly taxes, estimated tax
  payment, how much to set aside for taxes, 1099s, 1099-NEC, year-end tax prep,
  contractor payments, W-9s, or any phrase suggesting they are preparing for a
  tax deadline or handing materials to an accountant. Also trigger proactively
  when a user asks about net profit or YTD income in a context that suggests
  they are worried about their tax bill.
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
→ Output: "Estimated Q2 payment due June 16: $X — see full breakdown below"

User: "I need to send out 1099s"
→ Pull all contractor/vendor payments from QuickBooks + PayPal + Stripe
→ Identify contractors paid ≥ $600 YTD
→ Flag records missing W-9 / EIN
→ Output: 1099-NEC candidate list + missing W-9 action list
```

## Determine mode

Read the user's message and context to decide which path applies:

- **Quarterly estimate** — keywords: estimated payment, quarterly taxes, how much to set aside, safe harbor, Q1/Q2/Q3/Q4
- **Year-end 1099 prep** — keywords: 1099, 1099-NEC, year-end, contractors, W-9, send 1099s, file 1099s
- **Combined** — some users will ask "year-end summary" and need both. Run quarterly last; run 1099 prep first since it drives the most action items.

If the intent is ambiguous, ask: "Are you looking at your estimated tax payment for this quarter, or are you preparing 1099s for your contractors — or both?"

---

## Path 1: Quarterly estimated tax

### 1. Pull YTD financials

Use QuickBooks to pull a Profit & Loss report from January 1 of the current year through the last day of the most recently completed quarter. Capture:
- **Gross revenue** (total income)
- **Total expenses** (operating expenses, COGS, etc.)
- **Net ordinary income** = revenue − expenses

If QuickBooks is not connected, ask the user to upload a P&L as CSV or paste the key numbers. For field names and query approach, see [reference/connector-queries.md](reference/connector-queries.md).

### 2. Ask about prior estimated payments

Before calculating, ask: "How much have you already paid in estimated taxes so far this year?" If the user doesn't know, note that you'll calculate total liability — they can subtract payments themselves or check with their accountant.

### 3. Calculate estimated liability

See [reference/calculation-assumptions.md](reference/calculation-assumptions.md) for the full math and the assumptions table you must include in output.

Short version:
1. **SE tax** = net profit × 0.9235 × 0.153 (then halve it — the deductible half offsets income)
2. **Adjusted net** = net profit − (SE tax / 2)
3. **Federal income tax** = apply the bracket rate appropriate to the user's business type and estimated annual income (default to 22% unless the user tells you their bracket; note this assumption explicitly)
4. **Total annual liability** = federal income tax + SE tax
5. **Quarterly payment** = (total annual liability − payments made) ÷ quarters remaining
6. **Safe harbor check** — note whether the user should verify against prior-year tax (100% of prior year, or 110% if AGI > $150k)

### 4. State assumptions and deliver output

Use this output structure:

Structure the output as a document with these sections in order:

1. **Header** — H2 with "Estimated tax summary" followed by the quarter and year.
   Subline: prepared date and "For review by your accountant."

2. **YTD snapshot** — Bold lines showing YTD net profit with date range,
   estimated annual net profit (annualized from YTD), and assumed business type
   (sole proprietor, S-corp, etc. — flag as assumed, not confirmed).

3. **Self-employment tax** — Show the SE tax calculation: net profit times
   92.35% times 15.3%, and the deductible SE half.

4. **Federal income tax estimate** — Adjusted net income, assumed bracket
   (default 22%, note to confirm with accountant), and the federal estimate.

5. **Total estimated annual liability** — SE tax plus federal income tax.

6. **Quarterly payment** — Total liability minus payments already made, divided
   by quarters remaining, with the specific dollar amount due and the due date.

7. **Safe harbor note** — Remind the owner to ensure total payments meet 100%
   of prior-year tax (or 110% if AGI exceeded $150k).

8. **Assumptions** — Bullet list of every assumption: bracket rate, business
   structure, state taxes excluded, deductible SE half included, and deductions
   not applied (home office, QBI, depreciation).

---

## Path 2: Year-end 1099 prep

### 1. Pull contractor payments from all sources

Query each connected source for **all payments made to individuals or businesses for services** in the tax year. Do not include payments for goods, refunds, or internal transfers.

**QuickBooks — try live connector first, fall back to CSV if needed:**

1. **Try live connector.** Attempt to pull vendor-level payment records via the QuickBooks MCP. If the connector returns individual payee records with name, amount, and account category, use them directly and skip the CSV step.

2. **Detect aggregate-only response.** If the MCP returns only category-level totals (e.g. "Contract labor: $7,500" with no payee breakdown), the connector does not yet support vendor-level queries. In this case, prompt the user:

   > "QuickBooks returned summary data only — I need payee-level detail to build your 1099 list. Please export a **Transaction List by Vendor** report (QuickBooks → Reports → Expenses → Transaction List by Vendor, filtered to this tax year) and upload the CSV here. I'll process it automatically."

3. **Process CSV via Desktop connector.** Map columns: payee name, amount, date, payment method, EIN/SSN status. Follow the same aggregation and threshold logic below regardless of whether data came from the live connector or CSV.

> **Note for future connector versions:** If the QuickBooks MCP is upgraded to expose vendor payment records directly, step 1 will succeed and the CSV fallback will be skipped automatically. No changes to this skill are needed — the try-first logic handles it.

For field names and query approach, see [reference/connector-queries.md](reference/connector-queries.md).

**PayPal:** Pull all "Goods & Services" payments sent. Note: PayPal issues its own 1099-K to contractors above the threshold — flag these separately in output so the accountant can determine whether a 1099-NEC is also needed.

**Stripe:** Pull all transfers/payouts made to external parties. Same 1099-K caveat as PayPal applies.

**Desktop/CSV:** If the user uploads a CSV directly (without going through QuickBooks export), map columns: payee name, amount, date, payment method, EIN/SSN status.

### 2. Aggregate by payee

Combine across sources and sum payments by individual or business entity. Deduplicate by name (watch for "John Smith" vs "John A. Smith" — flag likely duplicates for human review rather than auto-merging).

### 3. Apply the $600 threshold

- **Flag for 1099-NEC:** any payee paid ≥ $600 for services (contractors, freelancers, consultants)
- **Flag for 1099-MISC:** any payee paid ≥ $600 for rent, attorney fees, prizes/awards
- **Near-threshold alert:** flag payees paid $400–$599 — close to the threshold, accountant may want to verify

Corporations (Inc., Corp., LLC taxed as C or S corp) generally do not need a 1099-NEC — note this but flag for accountant confirmation.

### 4. Check W-9 status

For each flagged payee, note whether a W-9 / EIN is on file in QuickBooks. Mark as:
- ✅ W-9 on file (EIN/SSN recorded in QuickBooks)
- ⚠️ Missing — W-9 not on file; must collect before filing
- ❓ Unknown — cannot determine from available data

### 5. Deliver the 1099 prep package

Use this structure:

Structure the 1099 prep output as a document with these sections:

1. **Header** — H2 with "1099 prep list" and the tax year. Subline: prepared
   date, "For review by your accountant," and "Not tax advice."

2. **Summary** — Bullet counts: total contractors paid, number requiring
   1099-NEC (at or above $600 for services), number missing W-9 (with filing
   deadline note for Jan 31), and number near-threshold flagged for review.

3. **1099-NEC candidates table** — Columns: payee name, total paid, data
   sources, W-9 status (on file / missing / unknown), and notes. Flag any
   payee paid via PayPal or Stripe with a note that the platform may issue
   its own 1099-K.

4. **Missing W-9 action list** — Numbered list of contractors who need to
   provide a W-9 before filing, with amounts paid and a reminder to request
   the form.

5. **Near-threshold table** — Payees paid $400-$599 flagged for accountant
   review, with a note to verify no additional payments were missed.

6. **Payment processor note** — Explain that PayPal and Stripe issue their own
   1099-K forms and the accountant should confirm whether a 1099-NEC is also
   needed for contractors paid exclusively through those platforms.

7. **Next steps checklist** — Action items for the accountant: collect missing
   W-9s, confirm unknowns, review near-threshold payees, verify corporation
   exemptions, confirm 1099-K overlap handling, file by January 31.

---

## Guardrails

- **Not tax advice.** Open every deliverable with this: "Prepared for review by your accountant — not tax advice." Include it in the document header, not just in chat.
- **State every assumption.** If you assumed a 22% bracket, say so. If you excluded state taxes, say so. The accountant will adjust; give them the levers.
- **Don't merge payees automatically.** Flag likely duplicates for human review.
- **Don't file anything.** The output is prep material. Filing is out of scope.
- **Corporation exemption is a judgment call.** Note it; don't auto-exclude.

## Reference files

- [reference/calculation-assumptions.md](reference/calculation-assumptions.md) — full tax math, bracket table, and SE tax walkthrough
- [reference/connector-queries.md](reference/connector-queries.md) — how to pull data from QuickBooks, PayPal, and Stripe
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for common failure modes
- [reference/examples/quarterly-estimate.md](reference/examples/quarterly-estimate.md) — worked quarterly estimate example
- [reference/examples/year-end-1099.md](reference/examples/year-end-1099.md) — worked year-end 1099 prep example
