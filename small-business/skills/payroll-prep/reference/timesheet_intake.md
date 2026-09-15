# Timesheet Intake

Setting the period, the roster, and getting hours in from wherever they live.

---

## Period setup

Confirm all four before pulling anything:

- **Period start and end** — inclusive dates
- **Pay date** — when money actually lands
- **Pay frequency** — weekly, biweekly, semimonthly, monthly
- **Who is in this run** — hourly crew, salaried staff, or both

Biweekly and semimonthly get mixed up constantly. Biweekly is every two weeks, 26 runs a year. Semimonthly is the 15th and the last day, 24 runs. If the owner says "twice a month" and the last period ran the 1st through the 14th, ask rather than assume.

**Period boundaries matter most at month end.** A week that straddles the 31st has hours in two months for job costing but one paycheck. Keep the pay period whole and let the books sync handle the split.

---

## Roster

Pull the active employee list and compare it to the last run.

| Change | What to do |
|---|---|
| New hire mid-period | Confirm the start date and that hours before it are excluded |
| Termination | Confirm the final date, unused PTO payout if owed, and whether a final check has different timing under state rules |
| On leave | Confirm paid or unpaid, and whether PTO is being drawn |
| Someone paid last period, absent now | Flag it. This is either a termination nobody recorded or a missing timesheet |
| Someone new with no hire record | Flag it. Never pay a person who is not on the roster |

---

## Source: Gusto

Before pulling anything, call `list_payroll_blockers` and translate any blockers to plain English per Step 2 of the SKILL.md — they decide whether the run stages in Gusto or ships as a run sheet.

Then pull `list_employees` and `list_pay_schedules`. Either empty on a company that reports a headcount, or a blockers call that errors, means the source is not delivering — stop the Gusto path and say so; the run sheet path is the outcome.

Pull, tool by tool:

| Input | Tool | Read it like this |
|---|---|---|
| Hours | `list_time_records` (period start and end) | Check `source` first. `native`: shifts with clock-in, clock-out, breaks. `third_party`: timesheets; `get_time_sheet` on a timesheet's top-level id for per-day lines. `none`: no hours here, use the spreadsheet path. |
| Leave taken | `list_time_off_requests` (period, `status: approved`) | Each approved day is paid as PTO or sick, not as worked. Pending is a flag. Notes are withheld by the tool; do not ask for them. |
| Balances | `get_time_off_balances` | Available, accrued, used, pending per policy. Policy names need the time-off-policies scope; without it match on policy uuid. Feeds the over-balance check. |
| Roster, rates, classifications | `list_employees` and its compensations | Employment status and the active flag are separate fields (below). |
| Prior run | `list_payrolls`, `get_payroll` | The last processed run's per-person totals, for the comparison. |

A missing punch the owner fills in is written with `record_time`, per Step 2 of the SKILL.md — owner-stated times only, shown first. The required parameters and the id and re-read traps are in the `record_time` row of `../../../shared/connector-call-shapes.md`; this file does not repeat them.

Rates come from Gusto, never from the timesheet. A rate written on a paper timesheet is a note, not a record.

---

## Source: QuickBooks Payroll

Equal footing with Gusto, not a lesser path. Pull the employee roster, pay type and rate with its frequency, employment status, PTO policy balances, the pay schedule and frequency, and the last completed run for the prior-period comparison. The run detail carries per-employee gross pay, hours, and the source of those hours, so a timesheet-sourced entry is distinguishable from a manual one.

Rates come from the payroll record here too, never from the timesheet.

Three things to get right on this source:

- **Employment status and the active flag are separate fields.** Someone flagged active can still be not-on-payroll or on paid leave. Read both before including anyone.
- **One employee can carry many pay rates.** Most sit at zero hours. Total from the rate with hours against it, not the first one returned.
- **The employee roster pages.** Read every page before totaling; a partial roster silently shorts whoever fell off the end.

---

## Source: spreadsheet upload

The fallback path, and a common one. Small crews run on paper, a shared sheet, or a photo of a whiteboard.

Accept any reasonable layout and map it. Expected columns, however they are named:

- Employee name or ID
- Date
- Time in, time out
- Break minutes, or a flag that breaks are already deducted
- Hours, if the sheet is already totaled
- Job, class, or cost code, if tracked
- Pay type: regular, PTO, holiday, unpaid

**Ask which convention the sheet uses for breaks.** A sheet that already nets out lunch, processed as though it doesn't, shortchanges everyone by half an hour a day. This one question prevents the most common upload error there is.

When the sheet is already totaled, still recompute from the punches when punches exist. When only totals exist, use them and say so — the anomaly checks that depend on punch times will not run, and the owner should know which safety nets are off.

---

## Normalizing

Produce one row per person per day:

```
person | date | in | out | break_min | regular | ot | pto | holiday | job
```

Rules that keep this honest:

- A shift crossing midnight belongs to the day it started, unless the owner's policy says otherwise
- Overlapping entries for one person are never merged automatically — they are flagged
- A row with an in and no out gets hours recorded as unknown, not estimated
- Rounding follows the owner's stated policy; with no policy, do not round at all

---

## Worked example

Okonkwo Mechanical, week ending 3/15, five on the crew.

- Gusto not connected. Ray uploaded a shared sheet with in and out times, breaks not deducted.
- Confirmed: breaks are 30 minutes unpaid, taken daily, not punched.
- Roster matched last period except one new apprentice, Dee, started Wednesday.
- One row for Marcus on 3/12 has a 6:40 AM in and no out.

Reported: 5 people, 214 hours readable, 1 shift with no clock-out (Marcus, Thursday), 1 new hire to confirm hours for (Dee, started 3/12).
