---
name: restock
description: Turns what is actually selling into a reorder decision and gets it all the way into the books — computes sales velocity and conservative stockout dates per item, sizes the reorder, drafts the purchase order and the vendor email, and then stages the matching entry so the bill matches against the PO when it arrives. Flags the money sitting still too, so dead stock gets cleared instead of reordered. Runs on Shopify, Square, or an uploaded sales and stock CSV, and deepens with QuickBooks, Gmail or M365, Calendar, and NetSuite. No PO is sent and no vendor is emailed without approval. Use it when the owner says "what do I need to reorder," "am I going to run out," "restock," "we keep running out of filters," "draft a PO for my supplier," or "how much cash is sitting in the warehouse."
allowed-tools: Read, WebFetch
---

# Restock

Chain two skills so reordering ends in the books rather than in a forgotten email: `inventory-planner` decides what to buy, `ap-processor` stages what it will cost.

The gap this closes is small and expensive. The reorder gets figured out, the PO gets drafted, the email gets sent — and then nothing is recorded anywhere, so when the bill lands six weeks later nobody can tell whether the price or the quantity was right.

## Step 1 — Work out what to buy (inventory-planner)

Invoke `inventory-planner`.

- **Goes in:** sales history and stock on hand from Shopify, Square, or NetSuite, or an uploaded CSV of both.
- **Comes out:** 7-day and 28-day velocity per item, conservative stockout dates, a sized 60-day reorder with dollar costs, and a separate slow-mover list.

`inventory-planner` owns all of the math — the two velocity windows, the distortion handling, the lead-time comparison, the seasonality rule. Do not redo any of it here.

Two of its rules matter enough to name in the chain:

- **Zero-velocity items are never reorder candidates.** They come through as slow movers with the cash tied up in them. No sales means stop buying, not buy more.
- **An out-of-stock period is not zero demand.** It is suppressed demand, and treating it as zero under-orders the item forever.

**Gate — the buy list.** Show the total dollars and the count of items about to stock out before anything is drafted. The owner approves the list, trims it, or changes quantities. Every line carries its velocity, days of cover, lead time, quantity, and cost, so the decision takes a minute instead of a rebuild.

## Step 2 — Draft the PO and the vendor email (inventory-planner)

For the approved lines, `inventory-planner` drafts a purchase order per vendor and the email to go with it, written in the owner's voice.

**Gate — both wait for an explicit yes, separately from Step 1.** Approving the buy list is agreeing on what to order. Sending the PO is committing the money and spending the vendor relationship. State the vendor, the line items, and the total before asking.

Without a mail connector (Gmail or Microsoft 365) connected, the PO and the email are files the owner sends by hand. That is a complete outcome.

## Step 3 — Leave a record the future bill can match against

Two different things happen here, and it matters which skill owns which.

**`inventory-planner` keeps the purchase order itself.** The approved PO is its document — vendor, line items, quantities, prices, expected date. It is saved and handed to the owner in Step 2, and that is the record of what was ordered.

**`ap-processor` takes the coded memo, not the PO.** Hand it the vendor, the PO number, the total, the expected date, and the account, class, and job the spend belongs to. `ap-processor` does not create purchase orders in the ledger — it reads them when a bill arrives, to run the three-way match of bill against PO against receiving ticket. What it needs from this step is a coded record sitting where that match will look for it.

- **Goes in:** vendor, PO number, total, expected date, and the coding.
- **Comes out:** a coded memo filed against the vendor, so when the bill lands in six weeks the price and the quantity can be checked against what was actually approved.

**Gate — the coding approval.** This is `ap-processor`'s own gate and it holds here. Nothing is written to the ledger until the owner says yes, and nothing lands as a bill and never as a payment. **No money moves in this command at all** — paying for what arrives is `/pay-the-bills`.

If a code is uncertain on a new vendor, `ap-processor` asks rather than guessing. One question now beats a miscoded year.

Without a ledger connector, the coded memo comes out as an import file and a summary alongside the PO. The three-way match still happens later, by hand, against a record that exists.

## Step 4 — Make it a rhythm

Ray Okonkwo runs Okonkwo Mechanical off a parts shelf he checks when something is missing, which is always too late. With Google Calendar connected, offer once — after a restock the owner found useful — to put a recurring block on the calendar for the reorder decision.

This works far better as a rhythm than as a fire drill. Offer it once. On a no or on silence, drop it.

## Fallback path

A sales CSV plus a stock count is a fully supported input. Many businesses count on a clipboard, and that is legitimate data. Velocity, stockout dates, reorder sizing, the PO, and the vendor email all come out the same. The books entry becomes an import file.

## What not to do

- **Do not send a PO or a vendor email without approval.** One spends money, the other spends goodwill.
- **Do not treat the buy-list approval as approval to send.** Two gates, two decisions.
- **Do not reorder a zero-velocity item.**
- **Do not size a reorder without subtracting what is already inbound.** Double-ordering a slow item buries cash for years.
- **Do not invent a velocity, a lead time, or a stockout date.** Too little history is reported by SKU.
- **Do not pay anything here.** POs are staged, not paid. Payment is `/pay-the-bills`.
- **Do not report units without dollars.** The owner is deciding about cash, not pieces.

## Output

**Deliver the reorder plan per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the plan as an HTML page in the house style — total committed as the lead stat tile in dollars, each SKU a row with velocity, stockout date, and reorder size in tabular-nums, and a pill on anything already inbound. The PO documents and any import file ride along as working files, not second deliverables.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a buy decision, not prose.

## After the run

The POs are out and a coded record is waiting for the bills to match against. When those bills land, the natural next step is "pay the bills" — `/pay-the-bills` runs the match, the cash check, and the payment gate. Also nearby: "cash forecast" (`cash-flow-snapshot`) to see what the committed orders do to the next 60 days, and "close the month" (`/close-month`) when the period ends. Offer at most three, and skip any offer the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
