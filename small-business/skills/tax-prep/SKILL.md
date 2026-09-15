---
name: tax-prep
description: Prepares tax materials as a two-link chain — month-end-prep confirms the books are closed and reconciled first, then tax-season-organizer calculates the quarterly estimated payment or builds the year-end 1099-NEC list and accountant packet from those closed numbers. Requires a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books); uses Gusto, PayPal, and Stripe when connected, else CSV upload. US federal tax math; a non-US business gets the closed-books packet. Prep material for a CPA, never tax advice, nothing filed. Trigger on "quarterly taxes," "estimated tax payment," "how much should I set aside," "1099s," "1099-NEC," "W-9s," "year-end tax prep," "get my books ready for my accountant," any phrasing that suggests a tax deadline is coming, or a question about net profit or YTD income that sounds like worry about a tax bill. An owner who says the period's books are already closed routes to tax-season-organizer directly.
allowed-tools: Read, WebFetch
---

Run the tax chain. Books first, then tax materials. The dependency is not optional — an estimate calculated on unreconciled books is a number the owner will send to the IRS.

Parse arguments:
- `--mode` (default: infer from the date — Oct through Jan defaults to `both`, otherwise `quarterly`) — `quarterly`, `1099`, or `both`
- `--year` (default: current year)

**Framing:** open every deliverable with "Prepared for review by your accountant — not tax advice."

**A ledger is required** — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, whichever is connected (`../../shared/connector-neutrality.md`). Without one, ask for a P&L export and a payee-level payment export before starting.

**Check the country before Step 1.** Read `Country` from the `## Business context` block (`../../shared/currency-and-locale.md`). The tax math in Step 2 is US federal. If the business is not in the US, say so in one line, run Step 1 so the books are closed, and hand the owner the closed-books packet for their accountant in place of a US estimate or 1099 list. Do not run the US calculation.

**Expensify, when connected, is read-only and adds one thing worth having:** the expenses with
no receipt attached. Surface that total and count alongside the estimate — an unsubstantiated
deduction is the item the accountant will ask about first, and it is cheaper to find now than
in April.

## Step 0 — Confirm the mode

If `--mode` was not given, state the inferred mode in one line and let the owner redirect: "It's late January, so I'll prepare both the Q4 estimate and your 1099 list. Want something different?" Do not run a discovery interview — the owner typed /tax-prep.

## Step 1 — Books first (month-end-prep)

Run `month-end-prep` over the periods the tax work depends on: year-to-date through the last completed quarter for `quarterly`, the full tax year for `1099`.

**Verify before you re-close.** Check whether each month in scope is already closed — reconciled, no open flagged items, packet produced.

- **Already closed** → verify only. Confirm the reconciliation stands, confirm nothing was posted after the close, and say so in one line: "March through June are already closed and still reconcile. Moving to the estimate." Do not re-run the full close on a month the owner finished last week.
- **Not closed** → run the close for the open periods. `month-end-prep`'s own Step 6 sign-off gate holds.
- **Partially closed** → close only the open months and verify the rest.

**In:** the periods in scope. **Out:** reconciled YTD net income, reconciled vendor and contractor payment detail, and a list of anything still unresolved.

### The gate before Step 2

Do not calculate anything until the books in scope are settled. If items are still open, say what they are and what they do to the tax number:

> "Eleven transactions are still uncategorized, totalling USD 6,800. Until those are coded, your estimate could be off by roughly USD 1,500 either way. Categorize them, or tell me to proceed and I'll state it as an assumption."

If the owner proceeds anyway, that becomes a stated assumption in the deliverable — not a footnote.

## Step 2 — Tax materials (tax-season-organizer)

Run `tax-season-organizer` in the chosen mode, using only Step 1's reconciled figures.

- **In:** closed-books YTD net income (quarterly path) or reconciled payee-level payment detail (1099 path).
- **Out:** the estimated-payment breakdown with due date and full assumptions table, or the 1099-NEC candidate list with W-9 status and the missing-W-9 action list — or both.
- **Gate:** none for producing the packet. Nothing is filed, ever.

When both modes run, do 1099 prep first — it generates the action items with the earliest deadline — then the quarterly estimate.

Say where the number came from: "This estimate is built on closed books through June 30, not the raw register." That sentence is what makes the chain worth running.

Example, Okonkwo Mechanical: "Q3 estimate: USD 7,240, due September 15. Built on USD 92,000 YTD net through the June close. Assumes a 22% bracket and sole proprietorship — confirm both with your accountant."

## What not to do

- **Do not calculate a tax number off unreconciled books.** That is the entire reason this is a chain.
- **Do not re-close a month that is already closed.** Verify it and move on.
- **Do not give tax advice.** Every output is prep material for a CPA and says so in its header.
- **Do not hide an assumption.** Bracket, business type, excluded state taxes, deductions not applied — list them all so the accountant has the levers.
- **Do not merge payees automatically.** "John Smith" and "John A. Smith" get flagged for a human.
- **Do not file anything, ever.**

## Output

**Deliver the accountant packet per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the packet cover as an HTML page in the house style — the estimate as the lead stat tile with its due date, the assumptions table, and the accountant checklist as rows. Open with the not-tax-advice line. The packet documents themselves keep their formats.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a review page for the owner before it goes to the accountant.

End with a next-steps checklist for the accountant: missing W-9s to collect, assumptions to verify, open book items that could move the number, and the deadlines to hit.

Then one short close: the packet is ready for the accountant, built on closed books. The natural next step is "cash forecast" — `cash-flow-snapshot` shows whether the estimated payment clears on its due date. Also nearby: "close the month" (`/close-month`) to keep the next quarter's estimate on reconciled numbers, and "build me a report" (`report-builder`) to track the tax set-aside over time. Offer at most three, and skip any offer the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
