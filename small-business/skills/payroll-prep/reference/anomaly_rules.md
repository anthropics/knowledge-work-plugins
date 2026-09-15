# Anomaly Rules

Every check, when it fires, and the words to use. All of them raise a flag to the owner. **None of them fix anything.**

---

## Why flags never auto-correct

A missed clock-out has exactly one right answer, and it lives with the employee and the owner. A system that fills in 5:00 PM because that is the usual time produces a paycheck that looks completely normal and is wrong. Nobody catches it, because the report shows a clean 8-hour day.

Flagging costs the owner ten seconds. Guessing costs someone their correct pay and costs the owner the crew's trust in the whole system.

---

## The checks

### Missing or broken punches

- **Clock-in, no clock-out.** Hours unknown for that shift. Fires always.
- **Clock-out, no clock-in.** Same treatment.
- **Zero-length shift.** In and out within a few minutes. Usually a double-tap; still asked.
- **Overlapping shifts for one person.** Two entries covering the same clock time. Never merged.

> Marcus, Thursday 3/12: clocked in 6:40 AM, never clocked out. Hours unknown. What did he work?

### Hours anomalies

- **Overtime above this person's own pattern** — fires above 125% of their trailing 4-period average OT, or any OT for someone who normally has none.
- **Total hours above the schedule** by more than 10%, when a schedule exists.
- **Zero hours for someone who normally works.** Often a missing timesheet, sometimes a quiet termination.
- **Over 16 hours in a day.** Almost always a punch error, occasionally real.
- **Any single shift over 12 hours — fires on the first run, with nothing on file.**
  Every other hours check needs a baseline, a schedule, or a stated policy to compare
  against, so on a first run they all sit silent and a 19-hour shift sails straight
  through into a paycheck. This one needs none of that. Twelve hours is long enough
  to be worth a sentence even when it turns out to be real, and it is the rule that
  catches the missed clock-out that every other rule cannot see yet.

  > Marcus shows a 19-hour shift Tuesday, 5:10 AM to 12:20 AM. This is your first
  > run so I have nothing to compare it against — real long day, or a punch he
  > forgot to close?
- **Seven consecutive days worked** — matters for both fatigue and, in some states, premium pay.

> Dee logged 14.5 OT hours. Her four-period average is 2. That is 12.5 hours above normal, about USD 560 extra. Real, or a punch problem?

### Pay setup anomalies

- **Rate changed since last run.** Fires on any change, up or down, with both rates and the effective date.
- **Classification changed** — hourly to salary, or employee to contractor.
- **New person with no hire record.**
- **Person on the last run missing from this one.**
- **PTO taken beyond the available balance.** The balance is the payroll source's figure (Gusto `get_time_off_balances`; QuickBooks Payroll policy balances), never an estimate from accrual rules.
- **Salaried person with logged hours** that suggest an unpaid partial week.

> Luis's rate reads USD 32.00 this period, USD 29.50 last period. If that raise is real I'll use it. If not, it is USD 100 a week I would rather ask about.

### Cross-checks

- **Gross pay moved more than 10% from the prior period** at the run level, with the driver named.
- **Labor hours that do not reconcile to job hours**, when the business tracks labor to jobs.
- **A job with labor charged but no active work order.**

---

## How a flag is worded

Four parts, always:

1. **Who** — the person's name
2. **When** — the specific date or shift
3. **What** — both numbers where two numbers exist
4. **What it costs** — the dollar impact, when it can be computed honestly

A flag without a name and a date is noise. A flag without a dollar figure is hard to prioritize. A flag with an invented dollar figure is worse than no flag at all — if the hours are unknown, the cost is unknown, and that is what to say.

---

## Presenting flags

Group by person, not by flag type. The owner thinks in people: "what is going on with Marcus," not "show me all the missed punches."

Order people by the size of the open question — unknown hours first, then large dollar variances, then everything else.

Ask about each one separately and record the answer. Batching them into one confirmation defeats the purpose, because the owner will skim.

---

## Overtime calculation edges

| Situation | Handling |
|---|---|
| Rate change mid-week | OT premium uses the weighted average rate for the week unless the owner specifies otherwise |
| Two rates in one week (shop vs field) | Same — weighted average, and say which rates went in |
| Daily OT states | The owner's rule wins. If they have not stated one, apply weekly OT and say so explicitly |
| Shift crossing midnight | Hours belong to the start day unless the owner's policy differs |
| PTO in an OT week | PTO usually does not count toward OT hours. State the assumption |
| Holiday premium | Only if the owner has a stated policy. Never assumed |

**Whenever a rule is assumed rather than stated, say which one was applied.** An owner who sees "applied weekly overtime, no daily rule on file" can correct it in five seconds. An owner who sees only a total cannot.
