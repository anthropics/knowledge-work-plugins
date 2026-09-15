# Run Sheet Format

What the owner looks at before saying yes.

---

## Design principle

The owner is checking two things, in this order: does anyone's line look wrong, and can the business afford the total. Everything on the sheet serves one of those. Anything else is clutter that makes the skim less careful.

---

## Per-person block

One block per person. Flags attached to the person, not collected in a separate section at the bottom where they get skipped.

```
Marcus Reyes
  Regular      32.0 h @ USD 34.00      USD 1,088.00
  Overtime      0.0 h
  PTO           8.0 h               $  272.00
  Gross                             USD 1,360.00
  FLAG  Thursday 3/12 — clocked in 6:40 AM, no clock-out. Hours unknown.
        Gross above excludes that shift.
```

**When a shift has unknown hours, say what the gross excludes.** Otherwise the number reads as final and the owner approves an incomplete check.

---

## Totals block

```
Pay period      Mar 2 – Mar 15
Pay date        Mar 20

People                    5
Regular hours         182.0
Overtime hours         32.0
PTO hours              16.0

Gross wages       $ 9,840.00
Employer taxes    $   812.00
Total cash        USD 10,652.00

Prior period      $ 8,960.00   (+9.8%)
Open flags                 2
```

Employer taxes appear only when the payroll provider supplies them. **Never estimate the tax figure.** If no payroll provider is connected, the line reads "not available — no payroll provider connected" and the total is labeled gross wages only. Gusto and QuickBooks Payroll both supply the figure; name whichever one it came from. An owner planning cash around an estimated tax number is being misled by a number that looks precise.

---

## The variance line

Any move over 10% from the prior period gets one sentence naming the driver.

> Up USD 880 from last period. Dee's first full week accounts for USD 640 of it; the rest is Marcus's overtime on the Maple St callback.

If the driver cannot be identified from the data, say that instead of offering a theory.

---

## Cash line

With cash data available:

> Account balance is USD 31,400. This run takes USD 10,652 on the 20th. The Ferguson payment run of USD 22,140 is also queued for the 18th, which would leave USD 8,608 — tight but clear.

Without it:

> I do not have a current balance. This run needs USD 10,652 in the account by the 20th.

---

## The approval question

Last thing on the sheet, stated as a total and a date:

> 5 people, 230 hours, USD 10,652 out on March 20, with 2 flags still open. Stage it?

Two flags still open means the owner chose to leave them. Say the count anyway — it is their last chance to change their mind before the sheet becomes a paycheck.

---

## Output formats

- **Chat summary** — the totals block, the variance line, the cash line, flag count
- **XLSX run sheet** — one row per person per pay type, plus a detail tab with every punch, so the owner or their bookkeeper can audit any line
- **Manual-entry sheet** when no payroll connector is present — the same data laid out in the order the owner's provider asks for it, so keying it in is transcription rather than translation
