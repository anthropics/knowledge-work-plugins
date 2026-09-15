# Output Formats

The document structure for each of the two paths. Both open with the not-tax-advice line
in the header itself, not just in chat.

---

## Path 1 — Quarterly estimated tax summary

Sections in this order:

1. **Header** — H2 reading "Estimated tax summary", the quarter, and the **tax year**.
   Subline: prepared date, the year the rate tables came from, and "For review by your
   accountant."

2. **YTD snapshot** — Bold lines showing YTD net profit with its date range, estimated
   annual net profit annualized from YTD, and the assumed business type (sole proprietor,
   S-corp, and so on). Flag the business type as assumed, not confirmed.

3. **Self-employment tax** — The SE tax calculation on **annualized** net profit: times
   92.35%, times 15.3%, and the deductible SE half.

4. **Federal income tax estimate** — Adjusted net income, the assumed bracket (default 22%,
   with a note to confirm with the accountant), and the federal estimate.

5. **Total estimated annual liability** — SE tax plus federal income tax.

6. **Quarterly payment** — Total liability minus payments already made, divided by the
   quarters still ahead, with the dollar amount due and the due date. Any missed quarter
   gets its own catch-up line, separate from the next payment.

7. **Safe harbor note** — Remind the owner to ensure total payments meet 100% of
   prior-year tax, or 110% if AGI exceeded USD 150k.

8. **Assumptions** — Bullet every assumption: bracket rate, business structure, state
   taxes excluded, deductible SE half included, and deductions not applied (home office,
   QBI, depreciation).

---

## Path 2 — 1099 prep package

Sections in this order:

1. **Header** — H2 reading "1099 prep list" and the tax year. Subline: prepared date,
   "For review by your accountant," and "Not tax advice."

2. **Summary** — Bullet counts: total contractors paid, number requiring a 1099-NEC (at or
   above USD 600 for services), number missing a W-9 with the January 31 filing deadline
   noted, and number near-threshold flagged for review.

3. **1099-NEC candidates table** — Columns: payee name, total paid, data sources, W-9
   status (on file, missing, unknown), and notes. Flag any payee paid via PayPal or Stripe
   with a note that the platform may issue its own 1099-K.

4. **Missing W-9 action list** — Numbered list of contractors who need to provide a W-9
   before filing, with amounts paid and a reminder to request the form.

5. **Near-threshold table** — Payees paid USD 400 to USD 599, flagged for accountant review,
   with a note to verify no additional payments were missed.

6. **Payment processor note** — Explain that PayPal and Stripe issue their own 1099-K
   forms, and the accountant should confirm whether a 1099-NEC is also needed for
   contractors paid exclusively through those platforms.

7. **Next steps checklist** — Action items for the accountant: collect missing W-9s,
   confirm unknowns, review near-threshold payees, verify corporation exemptions, confirm
   1099-K overlap handling, and file by January 31.
