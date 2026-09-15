---
name: report-pack
description: Delivers the owner's custom recurring report pack on a set cadence — runs the saved report definition from report-builder, wraps it in a business-pulse snapshot so the numbers have context, and hands over one chat summary plus the workbook. Defined once, then delivered on schedule without being asked again. Runs on any single connected data source, or entirely from an uploaded CSV or XLSX. Use it when the owner asks for their report pack, their weekly or monthly numbers, "send me the usual report," "run my report pack," "set this up to come every Monday," or "I want these numbers on a schedule."
allowed-tools: Read, WebFetch
---

# Report Pack

Chain two skills so the owner's recurring numbers arrive on their own, with enough context to act on: `report-builder` for the pack itself, `business-pulse` for the surrounding picture.

Owners already have the report they want in their head. What they do not have is it showing up on Monday without them chasing it. That is the whole job here.

## Step 1 — The report pack (report-builder)

Invoke `report-builder`. It owns the spec, the data pull, the math, and the workbook — do not rebuild any of that here.

- **Goes in:** the owner's description of the pack, or the name of a saved one.
- **Comes out:** a chat summary, an XLSX workbook, and a saved definition.

`report-builder` checks its saved definitions first. If the pack already exists, it reruns without re-interviewing the owner. If it does not, it builds the spec and confirms it once.

**Gate — spec confirmation.** A brand-new pack gets one confirmation from the owner before it runs. A pack that already has a saved definition does not. Re-asking someone to describe a report they defined last month is the fastest way to make this command feel broken.

## Step 2 — The context snapshot (business-pulse)

After the pack runs, invoke `business-pulse` for the same period.

- **Goes in:** the period the pack covered.
- **Comes out:** cash, sales trend, pipeline, watch list, and the one thing needing attention.

The pulse is context, not a second report. It answers the question the pack always raises: the numbers moved, but is the business fine?

**No gate here.** Both steps are read-only. Nothing is sent, posted, or written to a ledger, so there is nothing for the owner to approve between them.

## Step 3 — Deliver as one thing

One message, in this order: the pack summary, then the pulse in two or three lines, then the workbook.

Ray Okonkwo at Okonkwo Mechanical gets his Monday pack — revenue by crew versus last year, AR aging, labor as a percent of revenue — and under it: cash at USD 61,400, two invoices past 60 days, one van still down. He reads both in ninety seconds and knows what Monday is.

Never send two separate deliverables. A pack and a pulse arriving apart is two things to read; together it is one briefing.

Render that briefing as one HTML artifact using the house artifact style (`../../shared/artifact-style.md`) — additive to the chat summary and workbook, never a replacement. The pack's headline metrics are stat tiles with their comparisons as context lines; the grouped report rows are a table with tabular-nums; the pulse context sits in its own panel below, its watch-list items carrying status pills (warn or critical); down sources named in one quiet footer line.

## Step 4 — Set the cadence, once

**Offer the schedule one time, after a run the owner found useful.** Not before — a cadence offered on a pack nobody has seen yet is a subscription pitch.

Ask it plainly: "Want this every Monday morning?" On a yes, save the cadence with the report definition in `report-builder` and confirm in one line: "Saved. This runs every Monday morning."

Then honor it. Every scheduled run repeats Steps 1 through 3 with no questions, no re-confirmation, and no cadence offer. A scheduled report that asks the owner anything has stopped being scheduled.

On a no, or on silence, drop it and never ask again.

On an interactive run only — never a scheduled one — close with one line on what was delivered, then the single most relevant next step and at most two others nearby:

- If the pack raised a cash question: "cash forecast" runs `cash-flow-snapshot`.
- If the pulse flagged overdue AR: "who owes me money" runs `invoice-chase`.
- To change what the pack tracks: "build me a report" runs `report-builder`.

Max three offers. Never repeat an offer the owner declined this session.

## Step 5 — Handle a thin run without stopping it

A scheduled run happens whether or not every connector is healthy. If a source is down, `report-builder` marks that metric "n/a" and names the source; the pack still ships.

**Never skip a scheduled delivery because data was incomplete.** A pack with one gap and a note is useful. A silent Monday reads as the plugin being broken, and the owner stops expecting it.

If the owner has no connectors at all, the CSV path is the pack. Ask once for the export, run the identical report from the file, and keep the cadence.

## What not to do

- **Do not re-interview the owner about a saved pack.** Check the saved definition first, every run.
- **Do not rebuild the report logic here.** `report-builder` owns the spec, the math, and the workbook.
- **Do not recompute the pulse numbers.** `business-pulse` owns them, so there is one set of figures.
- **Do not offer the cadence twice.** Once, after a useful run, then never again.
- **Do not ask anything on a scheduled run.** Scheduled means it arrives without the owner in the loop.
- **Do not skip a run because a connector failed.** Ship it with the gap named.
- **Do not deliver the pack and the pulse as two messages.** One briefing, one read.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
