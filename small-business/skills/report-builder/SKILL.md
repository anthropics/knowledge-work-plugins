---
name: report-builder
description: >
  Turns a plain-English description of a recurring report into a real, repeatable
  report — defines the metrics, pulls them from whatever data sources are
  connected, delivers a chat summary plus an XLSX workbook, and saves the
  definition so the same report reruns on demand or on a schedule. Handles
  anything from "sales by location versus last year" to AR aging to labor as a
  percentage of revenue. Works fully from an uploaded CSV or XLSX when no
  connector is available. Use this whenever the owner asks for a report,
  dashboard, KPI pack, metrics summary, or recurring numbers — including
  phrasings like "can you track this every week," "I need to see these numbers
  monthly," "build me a report on," "same report as last time," or "put together
  a KPI dashboard." Reach for it even when the owner names the metrics without
  using the word report.
allowed-tools: Read, WebFetch
---

# Report Builder

The owner describes a report once. You build it, run it, and save the definition so it never has to be described again.

Owners are pulling numbers out of three dashboards by hand and trying to find the story themselves. The job is to end that.

## Step 1 — Check for an existing definition

Before anything else, read `reference/saved_reports.md` and check whether this report already exists. Also check for a `report-definitions.md` in the working directory — that's where definitions land when the skill folder isn't writable (see Step 7).

If the owner says "same report as last time," "run the weekly one," or names a report you have a definition for, skip straight to Step 4 and run it. Re-interviewing someone about a report they already defined is the fastest way to make this skill feel broken.

If nothing matches, continue.

## Step 2 — Turn the description into a spec

Owners describe reports loosely: "every Monday, sales by location versus last year, AR aging, and labor percent." That sentence contains four separate decisions. Resolve them into a spec using the format in `reference/report_spec.md`:

- **Metrics** — each one named, with its formula and source
- **Grouping** — by location, product, customer, channel, rep
- **Comparison** — versus prior period, versus last year, versus target
- **Period** — the window each run covers
- **Cadence** — one-off, weekly, monthly, quarterly

Infer what you reasonably can. "Sales by location vs last year" gives you the metric, the grouping, and the comparison — don't ask about those. Ask only about what's genuinely ambiguous, and ask it in one batch rather than one question at a time.

The two questions worth asking almost every time:

- Which period does each run cover — calendar month, trailing 30 days, month-to-date?
- Is a number like "labor percent" measured against revenue or against total costs?

Getting these wrong produces a report that looks right and is quietly wrong, which is worse than asking.

## Step 3 — Confirm the spec, once

Show the resolved spec back in a compact block. Ask for one confirmation, then build. Do not walk the owner through the spec field by field — they described this in one sentence and expect one answer.

If they correct something, apply it and go. Do not re-confirm a second time.

## Step 4 — Pull the data

Dispatch every source call in a single parallel batch. See `reference/data_sources.md` for the metric-to-tool mapping.

Sources, tried simultaneously:

- **The ledger** — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, whichever is connected; peers per `../../shared/connector-neutrality.md`. P&L lines, revenue, expenses, AR aging, AP, class and location splits. MYOB is P&L, AR, and payables only, three financial years back. If two ledgers are connected, ask which is the source of record and take totals from that one
- **HubSpot** — deals, stages, owners, close dates, pipeline value
- **PayPal, Square, Stripe** — settlements, fees, refunds, transaction detail
- **Shopify** — orders, SKU-level revenue, fulfillment status
- **Ramp, Expensify** — card spend and expense detail. Both are read sources here; Expensify is read-only search

If a source errors or returns nothing, record it and move on. Never block the whole report on one bad connector.

**No connectors at all is a supported path, not a failure.** Ask for a CSV or XLSX export, read it, and build the identical report from the file. Say so plainly: "I don't see a connected data source. Export the sales report from your system and drop it here — I'll build the same report from that." Owners with tool sprawl live in this mode, and the report is just as good.

## Step 5 — Compute and sanity-check

Compute every metric named in the spec. Then check the results before showing them. Read `reference/gotchas.md` for the failure modes that actually happen.

The checks that catch real errors:

- **Period boundaries.** A partial current month compared against a full prior month always looks like a collapse. Either compare like-for-like or label the partial period explicitly.
- **Double-counting.** A Shopify order and its Stripe settlement are one sale. If both sources are connected, pick one as the revenue source and note which.
- **Empty groups.** A location with no sales this period should appear with a zero, not vanish. A disappearing row reads as a data problem.
- **Totals that don't tie.** If the grouped rows don't sum to the total, say so rather than publishing a number you can't defend.

## Step 6 — Deliver

Two artifacts, always, in this order.

**The chat summary comes first.** Follow `reference/output_template.md`. Lead with what changed and what it means, not with a table dump. The owner asked for a report because they want a decision, not a spreadsheet.

Writing rules, same as every reporting skill in this plugin:

- Numbers lead, words follow. Not "sales were strong" — "USD 43,200, up 8% versus last year."
- Every number carries its comparison. A figure with no baseline is a missed insight.
- Name the outlier. "Portland is down 22%, the only location below last year" beats "results were mixed."
- Three findings maximum in the summary. The workbook holds everything else.

**Then the XLSX.** One tab per metric group, a summary tab first, raw pulled data on a final tab so the owner can check your math. Build it with a script rather than by hand.

**Then the report page, per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the report as an HTML page in the house style — each headline metric is a stat tile with its comparison as the context line; the grouped rows (by location, product, rep) are a table with right-aligned tabular-nums; any metric versus target carries a status pill (good on target, warn slipping, critical missed); the three findings open the page in their own panel; "n/a" sources go in one quiet footer line. Additive to the chat summary and the workbook, never a replacement.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why. The XLSX still ships alongside.
- **Best for skill:** use the visual artifact — a report is read on screen and compared week to week.

## Step 7 — Save the definition

Append the spec to `reference/saved_reports.md` with the date it was created and the cadence. This is what makes the report recurring instead of one-off.

If that file can't be written — the skill folder is read-only in most installed runtimes — write the definition to `report-definitions.md` in the owner's working directory instead and say where it went. A definition that silently failed to save is the same bug as never saving it.

If the owner asked for a cadence, confirm it in one line: "Saved. I'll run this the first Monday of each month." Scheduling is a property of this skill — no separate command needed.

## After the run

One line: the report ran and the definition is saved. Then the single most relevant next step, with at most two others nearby:

- "The weekly pack, on schedule" runs `/report-pack` to wrap this in context on a cadence.
- "How's the business doing?" runs `business-pulse` for the picture around these numbers.
- "Cash forecast" runs `cash-flow-snapshot` when the report raised a cash question.

Max three offers. Never repeat an offer the owner declined this session.

## What not to do

- **Do not interview the owner about a report they already defined.** Check `saved_reports.md` first, every time.
- **Do not ask permission to pull data.** The skill was invoked. Run it.
- **Do not invent a number.** If a source returned nothing, write "n/a" and name the source. A plausible-looking guess in a report the owner forwards to their bank is a serious failure.
- **Do not lead with the table.** The summary is the product; the workbook is the appendix.
- **Do not treat "no connectors" as a blocker.** The CSV path is a first-class mode.

## Reference files

- `reference/report_spec.md` — the spec format, with worked examples
- `reference/data_sources.md` — metric to connector mapping, with fallbacks
- `reference/output_template.md` — exact structure for the chat summary and the workbook
- `reference/saved_reports.md` — stored report definitions, appended to over time
- `reference/gotchas.md` — the failure modes that produce confidently wrong reports

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
