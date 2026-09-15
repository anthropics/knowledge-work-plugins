# Coding Rules

Getting each bill to the right account, class, and job.

---

## The order of evidence

Use the strongest available signal and stop. Stacking weak signals produces confident nonsense.

1. **This vendor's history in this ledger.** If the last eight Ferguson bills went to Materials and Supplies, the ninth almost certainly does too.
2. **The PO.** A PO written against a job carries the job code with it.
3. **The line detail.** "Compressor, 3-ton" reads differently from "shop towels."
4. **The owner's stated rule.** If Ray said once that anything from the uniform service is Overhead, that holds until he changes it.
5. **Nothing above applies.** Ask.

---

## Confidence threshold

Code it automatically when vendor history agrees across at least three prior bills and nothing on this bill contradicts it.

Everything else goes on the "needs your call" list with a proposed code and one line of reasoning. Keep that list short and specific — an owner will answer four questions and will ignore forty.

---

## Job and class splits

A single supply-house invoice covering three jobs is normal in the trades and is the most common source of bad margin data.

- **Split by line when the lines carry job references.** Many suppliers print the job name or PO on each line.
- **Split by the owner's allocation when they give one**, and record it so the same vendor gets the same treatment next time.
- **Do not spread evenly as a default.** An even split across three jobs is a fabricated allocation that will show up later as a margin number nobody can explain.

When the split is genuinely unknown, code the whole bill to the most likely job, flag it as unsplit, and say so. A flagged single-job coding is fixable; an invented three-way split looks correct and never gets revisited.

---

## Categories that routinely go wrong

| Situation | Right answer | Why |
|---|---|---|
| Equipment over the owner's capitalization threshold | Fixed asset, not expense | It changes the P&L and the tax return. Ask for the threshold once and remember it |
| Sales tax on a resale purchase | Flag it | The owner may be paying tax they are exempt from |
| Freight on materials for a job | Job cost, with the materials | Freight parked in overhead hides real job cost |
| Deposit or prepayment to a vendor | Prepaid or vendor deposit | Expensing a deposit understates the month and double-counts on delivery |
| Credit memo | Negative bill against the same vendor | Never net it silently into an unrelated invoice |
| Card charge from Ramp or Expensify | Already paid — code it, do not stage a payment | Paying it again is a real duplicate payment |

---

## Recurring bills

Recurring vendors — rent, insurance, the phone bill — code themselves reliably and should. What they do **not** do is approve themselves for payment. Recurrence is evidence about the account code, not consent to spend.

Flag a recurring bill whose amount moved more than 10% from the prior period. That change is often the only visible sign of a rate increase the owner never agreed to.

---

## Worked example

Ferguson invoice 88231, USD 3,417.02, four lines.

- Lines 1–2, condenser and line set, USD 2,980 — job reference "Maple St" printed on the line, coded to Materials, job Maple St
- Line 3, shop consumables, USD 196 — no job reference, coded to Shop Supplies, overhead
- Line 4, freight, USD 241.02 — allocated to Maple St with the materials it carried

No question raised. Vendor history and printed line references agreed.

Contrast: a first bill from a new sheet-metal fabricator, USD 8,900, single line reading "fabrication per quote." That one goes to Ray with a proposed code of Subcontractor and the note that it is a new vendor with no history and an amount large enough to matter.
