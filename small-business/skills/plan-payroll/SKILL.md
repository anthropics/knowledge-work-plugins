---
name: plan-payroll
description: Runs the payroll-confidence chain end to end — forecasts cash across the payroll window with cash-flow-snapshot, ranks and drafts overdue-invoice reminders with invoice-chase to close any gap, then assembles timesheets, flags every anomaly, and stages the run with payroll-prep. On Gusto the run is staged for the owner to submit; on QuickBooks Payroll, or with no payroll system, the last step is a validated run sheet the owner keys in. This chain never presses the payroll button. Builds on the ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books), with Gmail or M365, PayPal, Square, Stripe, and either Gusto or QuickBooks Payroll adding detail, and falls back to CSV and timesheet uploads. Use it whenever payroll is the worry, including "can I make payroll," "payroll is due Friday," "plan payroll," "will I have enough to pay the crew," or "I need to run payroll but money is tight." Accepts optional horizon and payroll-date arguments.
allowed-tools: Read, WebFetch
---

# Plan Payroll

Three skills in order: know payroll is covered, close the gap if it is not, then run it.

Owners do not ask two separate questions here. "Can I make payroll" and "run payroll" are one worry, and splitting them across two sessions is how a run gets keyed in at 11pm without anyone checking the bank balance first.

Parse arguments:

- `--horizon` (default `30`) — forecast window in days: 30, 60, or 90
- `--payroll-date` (optional) — the date payroll runs; defaults to the next scheduled pay date

## Step 1 — Is payroll covered? (cash-flow-snapshot)

Invoke `cash-flow-snapshot`. It owns the forecast math, the confidence bands, and the CSV fallback — do not rebuild any of it here.

- **Goes in:** the horizon and the payroll date.
- **Comes out:** a 30/60/90-day forecast, named risk flags, a chat summary, and an XLSX.

Say the verdict in one line before anything else: covered, tight, or short by a named dollar amount on a named date.

**Gate — where the chain goes next.** If payroll is comfortably covered, ask whether to skip the collection step and go straight to the run. If there is a gap, present it and wait for an explicit "see what we can collect" before Step 2.

## Step 2 — Close the gap (invoice-chase)

Invoke `invoice-chase`. It owns the ranking, the tone matching, and the send path per invoice type.

- **Goes in:** the gap amount and the date it lands, from Step 1.
- **Comes out:** ranked overdue invoices with a drafted reminder each, PayPal-issued invoices queued as PayPal sends and the rest as mail drafts.

Tie the ranking back to Step 1: show what gets collected inside the horizon and whether that actually closes the payroll gap. A reminder that pays in 45 days does nothing for a Friday run — say so.

**Gate — nothing sends without approval.** Drafts only until the owner says send, per reminder or as a batch they name.

## Step 3 — Stage the run (payroll-prep)

Invoke `payroll-prep`. It owns the period setup, the hour totals, the anomaly checks, and the books sync.

- **Goes in:** the pay period, the roster, and the cash verdict from Step 1.
- **Comes out:** a run sheet person by person, every anomaly flagged against the person it belongs to, totals, and the cash needed on the pay date.

Carry Step 1 forward instead of recomputing it. When `payroll-prep` reports whether the run clears, it uses the forecast this chain already produced, plus anything Step 2 is expected to collect.

**Gate — the flags, one at a time.** `payroll-prep` walks each anomaly separately. Do not collapse them into a single "looks good?" — each one is a person's pay.

**Gate — the run itself.** With Gusto connected, the run is staged in Gusto (`payroll-prep` writes the approved inputs with `update_payroll`; `run_payroll` is never called). With QuickBooks Payroll connected, the connector holds the reads and no run-staging write, so the outcome is the validated run sheet the owner keys in — what the connector holds today, not a lesser path. Staging holds only when the source actually returned a roster and a schedule: payroll-prep stops the staging path when a connected source reports employees but delivers none, and the chain then ends on the run sheet, stated plainly. **The owner submits it.** With neither, the deliverable is a validated run sheet for manual entry, and that is a complete outcome, not a degraded one. This includes when Gusto reports blockers — the run sheet inherits the blocker list from `payroll-prep`.

## Step 4 — Close the loop

One recap, in this order: the cash verdict, what was sent and to whom, the projected position if the reminders convert, and the staged run — headcount, total hours, total gross, cash leaving the account, pay date, and any flags left open.

Ray Okonkwo sees it in four lines: cash short USD 4,200 on the 15th, three reminders sent covering USD 6,800, two likely inside the window, run staged for 9 people at USD 18,340 with one missing punch still open on Marcus.

## Output

**Deliver the Step 4 recap per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the recap as an HTML page in the house style — the cash verdict as the lead stat tile, the reminders sent and their projected collections in tabular-nums, and the staged run's totals with a pill on any flag left open. Projected cash is labeled projected.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is one screen that answers "can I make payroll".

## Connector failures

If no ledger is reachable (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books — whichever the owner uses), stop and say so by category — the forecast is the foundation of the chain. If a payment connector or the mail connector (Gmail or M365) fails, name it and continue with the rest. If the payroll system fails, fall to the run sheet path rather than aborting; the owner still gets a payroll they can run. When the run cannot be staged or synced into the books — blockers, missing write access — say so in the Step 4 recap and deliver the run sheet plus the journal-entry summary for the bookkeeper to key in; `payroll-prep`'s blocker check decides which path applies.

## What not to do

- **Do not submit payroll.** The chain stages; the owner submits. This holds even when the owner asks it to go ahead.
- **Do not send a reminder without approval.** Drafts until told otherwise.
- **Do not skip Step 1 because the owner asked to "just run payroll."** The cash check is thirty seconds and it is the reason this chain exists.
- **Do not recompute the forecast inside Step 3.** One set of cash numbers, from one place.
- **Do not batch the anomaly review.** One decision per person per issue.
- **Do not treat a missing payroll connector as a blocker.** The run sheet is a designed path. Check for QuickBooks Payroll before concluding there is no payroll source; a business on QuickBooks often has it without having Gusto.
- **Do not promise collected cash as if it landed.** Projected is projected; label it.
- **Do not reproduce anyone's SSN, date of birth, home address, or bank number** anywhere in the chain's outputs (`../../shared/personal-data.md`).

## After the chain

Payroll is covered, the reminders are out, and the run is staged for the owner to submit. The natural next step is "pay the bills" — `/pay-the-bills` handles the vendor side with the same cash picture on screen. Also nearby: "cash forecast" (`cash-flow-snapshot`) to watch the position as the reminders convert, and "close the month" (`/close-month`) when the period wraps. Offer at most three, and skip any offer the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
