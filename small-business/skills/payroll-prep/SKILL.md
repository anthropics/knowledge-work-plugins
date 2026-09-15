---
name: payroll-prep
description: >
  Gets payroll ready to run without anyone getting shorted: pulls timesheets
  from Gusto, QuickBooks Payroll, or an uploaded spreadsheet, totals regular,
  overtime, and PTO
  hours by person, flags every anomaly it finds — missed punches, overtime
  spikes, rate changes, mid-period hires and terminations, hours off the
  schedule — and stages the run for the owner to approve line by line before
  a dollar moves. Anomalies are always raised, never quietly corrected. Once
  the owner runs it, the journal posts to the ledger or goes to the
  bookkeeper. Reach for this whenever payroll comes up at all
  — "run payroll," "payroll is due," "check the timecards," "did everyone
  clock out," "how many hours did the crew put in," "why is payroll so high
  this week," "I need to pay the guys Friday" — and use it after
  cash-flow-snapshot when the owner is worried about whether payroll clears.
allowed-tools: Read, WebFetch
---

# Payroll Prep

Get the hours right before anyone gets paid.

Payroll is the finance workflow with the least room for error. A wrong invoice gets corrected next week. A wrong paycheck is a person who cannot cover rent, and it is the fastest way for an owner to lose a crew. Everything in this skill is built around that asymmetry: the machine assembles and checks, the owner decides.

## Step 1 — Fix the period before anything else

Confirm the pay period start and end dates, the pay date, and who is in this run. Getting the period wrong duplicates or skips a week of someone's pay, and it is a surprisingly easy mistake when a period straddles a month end.

Confirm the roster too: new hires who started mid-period, anyone terminated, anyone on leave. See `reference/timesheet_intake.md`.

## Step 2 — Pull the timesheets

**With Gusto connected**, first ask Gusto itself what stands in the way: call its payroll-blockers check (`list_payroll_blockers`) before building anything. If blockers come back, translate each into plain English — what it means, who fixes it, and where. For example: "check payments unsupported" means this company pays by paper check, which the integration cannot stage, so the owner runs that part in Gusto directly; "bank account not connected via Plaid" means the owner connects the bank in Gusto's settings; "hourly employees unsupported" can block at the account level even when this run is salaried-only. Blockers are a routing signal, not a failure — the run still gets built and validated here, and the deliverable becomes the run sheet with the blocker list riding along.

Then pull the period's inputs, each from its own tool. **Hours:** `list_time_records` for the pay period; read its `source` field before anything else. `native` returns shifts with clock-in, clock-out, and breaks; `third_party` returns timesheets from the company's time-tracking partner, and `get_time_sheet` gives the per-day line items for any one of them (it refuses native shift ids); `none` means Gusto holds no hours for this company, so the spreadsheet path below supplies them. **Leave:** `list_time_off_requests` for the period with `status: approved` — every approved day is paid as PTO or sick, never as worked, and a pending request is a flag, not a paid day. **Balances:** `get_time_off_balances`, which is what the "PTO beyond available balance" check in Step 4 reads against. **Rates and classifications:** the roster from `list_employees` with each person's compensations. Rates come from Gusto, never from a timesheet. Call shapes for these are in `../../shared/connector-call-shapes.md`.

**A missing punch the owner can fill.** When Step 4 flags a shift with no clock-out and the owner gives the real times, `record_time` writes them — only the times the owner stated, shown to them first, and as an `update` of the existing shift rather than a second entry. The parameters that refuse if missing (timezone, job on Gusto's own tracking, which id counts as the shift) and the one re-read trap (a contractor's confirmed hours come back with blank clock times; do not write again) are in the `record_time` row of `../../shared/connector-call-shapes.md`. Read that row before the call. This is the only way the skill ever changes a punch; an assumed time is never written.

**Then prove the source is returning its data before anything is staged.** Pull the roster (`list_employees`) and the schedules (`list_pay_schedules`). A company that reports a headcount while either list comes back empty, or a blockers call that errors instead of answering, is a payroll source that is connected but not delivering. Stop the staging path, say so in one line ("Gusto is connected but returned no employees or pay schedules, so I cannot stage a run against it"), and offer the spreadsheet path below. Never build a run from an empty roster, and never treat a green connection badge as proof the data is there.

**With QuickBooks Payroll connected**, pull the same fields from there. Two different failures look alike here, and the owner hears them differently. An **empty source** (Gusto's lists come back with no rows on a company that reports a headcount) is a data gap: say so and use the run sheet. A **self-contradicting source** is a tool defect: `qbo_payroll_get_company_payroll_readiness` answering `has_employees: false` and `run_payroll_ready: false` while `qbo_payroll_get_employees` on the same company returns a `total_count` of 50 cannot both be true. This is independent of how much data the company has. When that happens, use the employee list for the roster (it is the call that returned rows), do not stage a run while readiness says not ready, and say both numbers to the owner in one line so the contradiction is on record rather than hidden behind "not ready." Then take the spreadsheet path below with that roster: a validated run sheet the owner keys into QuickBooks Payroll is the outcome, the same as for an empty source. This is a first-class source, not a fallback. It carries the full employee roster with pay type, rate and frequency, employment status, and PTO policy balances; the pay schedule and its frequency; and the last completed run with per-employee gross pay, hours, and the tax lines. Where hours came from a timesheet the record says so, which is what the anomaly checks in Step 4 need.

Two cautions specific to this source. Employees carry an employment status separate from an active flag, so someone marked active can still be not-on-payroll or on paid leave; read both before putting anyone in the run. And a single employee can hold a dozen or more pay rates, most sitting at zero hours, so total from the rate that actually has hours against it rather than the first rate listed.

**Without either**, take an uploaded spreadsheet or CSV. This is a fully supported path — a validated run sheet the owner keys into their payroll provider is a complete outcome. Many small crews still run on a paper timesheet photographed at the end of the week, and that works too.

Normalize into one row per person per day: date, in, out, break, regular hours, overtime hours, PTO, and the job or class if the business tracks labor to jobs.

## Step 3 — Total the hours

Compute regular, overtime, double time, PTO, holiday, and unpaid time per person, then per crew, then for the run.

Overtime rules vary by state and by how the business classifies people, and getting them wrong underpays someone. Use the owner's stated rule, and when there isn't one, use the plain weekly-overtime default and say which rule you applied. `reference/anomaly_rules.md` covers the calculation edges — mid-week rate changes, multi-job days, and shifts crossing midnight.

**Never fill a missing punch with an assumed time.** A shift with a clock-in and no clock-out has unknown hours, and unknown hours is what gets reported.

## Step 4 — Flag every anomaly

This is the core of the skill. Run the full check in `reference/anomaly_rules.md` and surface everything it finds, each with the person's name, the date, and what specifically looks wrong:

- Missing punches and shifts with no clock-out
- Overtime above this person's normal pattern, with both numbers
- Zero hours for someone who normally works
- Hours well above what the schedule called for
- Rate changes since the last run
- Duplicate or overlapping entries
- PTO taken beyond the available balance
- Someone paid last period who is missing from this one
- A new person appearing with no hire record

**Flags go to the owner. They never get silently corrected.** A missed punch has a real answer that only the employee and the owner know, and a plausible guess in the middle of that becomes a wrong paycheck that looks correct on the report.

## Step 5 — Show the run before approving it

Present the run sheet: person by person, hours by type, gross pay, and every flag attached to the person it belongs to. Then the totals — total hours, total gross, employer taxes and contributions if available, total cash needed, and the pay date.

Compare against the prior period and explain any move over 10%. A payroll that jumped USD 4,000 has a reason, and the owner should hear it from this skill rather than find it in the bank balance.

If cash data is available, say whether the run clears. If it is not available, say that plainly instead of implying it is fine.

## Step 6 — Resolve the flags, one at a time

Walk the owner through each flag. For each: what was found, what it would mean if left as is, and what they want done. Record the answer and apply it.

Do not batch flags into a single "looks good?" question. Each one is a person's pay.

## Step 7 — The approval gate

**Nothing stages until the owner explicitly approves the run.**

State plainly before asking: number of people, total hours, total gross, total cash leaving the account, the pay date, and the count of any flags they chose to leave open.

Then ask. An owner who wants to skip this gate should be told, once and without lecturing, that it stays because a wrong run is not something they can take back after direct deposit lands.

With Gusto connected, stage the run: find the unprocessed payroll with `list_payrolls` filtered to `processing_statuses: unprocessed` and an `end_date` a few weeks ahead (its date filter is on the pay period, and a bare call can miss a period that has not ended yet), take the one with the nearest check date, read it with `get_payroll`, then write the approved hours, PTO, and any bonus lines with `update_payroll`. Two shapes matter and both are in `../../shared/connector-call-shapes.md`: values **replace** rather than add, so "give Maria five more hours" means sending her new total, shown to the owner as "40 → 45" first; and a payroll whose roster is not yet materialized takes one empty `update_payroll` call to populate it before the real one. Leave `run_payroll` alone — that is the owner's button, in Gusto. With QuickBooks Payroll connected, the connector holds the reads (roster, rates, schedules, readiness, last run) and no run-staging write, so the outcome there is the validated run sheet the owner keys in; that is what the connector holds today, not a lesser path. **The owner submits it** in either system. With neither, produce the validated run sheet for manual entry. If Gusto's blockers from Step 2 prevent staging through the connection, the validated run sheet plus the plain-English blocker list is the outcome — say so without treating it as a failure.

## Step 8 — Sync to the books

After the run is submitted, post the journal entry to the ledger: gross wages, employer taxes, and any labor allocated to jobs. Test the capability, not the logo: a connected ledger whose connector has no journal-write path cannot take the post, so say so in one line and hand the balanced entry to the owner or bookkeeper to key in — a complete outcome, not a failure. Confirm the amounts match what actually ran, not what was proposed — those differ whenever the owner edited something at the last step.

## What not to do

- **Do not guess a punch, a rate, or a classification.** Unknown hours get named with the person and the date.
- **Do not correct an anomaly silently,** even an obvious-looking one. The owner may know something you do not.
- **Do not submit payroll.** Stage it; the owner submits. `run_payroll` is never called by this skill. This holds for QuickBooks Payroll exactly as it holds for Gusto — a connected payroll system is not permission to run payroll.
- **Do not send a delta to `update_payroll`.** Its values replace. Compute the new total from `get_payroll`, show both numbers, send the total.
- **Do not write a punch the owner did not state.** `record_time` carries only times the owner gave, and only after they saw the entry.
- **Do not read a pay rate without checking the hours against it.** In QuickBooks Payroll one person can carry many rates with zero hours on most of them.
- **Do not bury flags in a summary.** Attach each one to the person it affects.
- **Do not batch the flag review.** One decision per person per issue.
- **Do not treat a missing connector as a blocker.** A spreadsheet in, a validated run sheet out, is a designed path.
- **Do not skip the prior-period comparison.** A large move with no explanation is the most useful warning available.
- **Do not stage a run from a payroll source that reports employees but returns none.** A connected badge is not data. Say the source is not delivering, and use the spreadsheet path.
- **Do not reproduce an employee's SSN, date of birth, home address, or bank or card number** in the run sheet, the chat, or any rendered page. Gusto and QuickBooks Payroll payloads carry them; read past them (`../../shared/personal-data.md`).

## Output

**Deliver the validated run sheet per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the run sheet as an HTML page in the house style — headcount, total gross, and cash leaving the account as stat tiles, each person a row with hours and pay in tabular-nums, and a pill on every flag attached to the person it belongs to. Blockers, when Gusto reports them, get their own plain-English panel.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a sheet the owner approves person by person.

## After the run

The run is staged, the flags are resolved, and the books entry is posted. If cash was the worry going in, the natural next step is "can I make payroll" — `/plan-payroll` runs the forecast and the invoice chase in front of the next run. Also nearby: "cash forecast" (`cash-flow-snapshot`) to see what this run does to the next 30 days, and "taxes" (`/tax-prep`) when quarterly estimates or 1099s are coming due. Offer at most three, and skip any offer the owner already declined this session.

## Reference files

- `reference/timesheet_intake.md` — Gusto pull, spreadsheet upload, roster and period setup
- `reference/anomaly_rules.md` — every check, its threshold, and how it is worded
- `reference/run_sheet_format.md` — the run sheet layout and the totals block
- `reference/books_sync.md` — journal entry structure and job-cost allocation
- `reference/gotchas.md` — the mistakes that shortchange a person or double-pay a period

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
