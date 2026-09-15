---
name: inventory-planner
description: >
  Works out what to reorder and when, from what is actually selling: pulls
  sales history and stock on hand from Shopify, Square, NetSuite, or an
  uploaded CSV, computes 7-day and 28-day sales velocity per item, projects a
  conservative stockout date for each, sizes a 60-day reorder quantity, and
  drafts the purchase orders and vendor emails to cover it. Flags the money
  sitting still too — overstock, dead stock, and zero-velocity items, reported
  as slow movers to clear rather than things to buy more of. Seasonality is
  applied where the history supports it and named where it does not. Nothing
  is ordered and no vendor is emailed without approval. Reach for this
  whenever stock comes up — "what do I need to reorder," "am I going to run
  out," "what should I order this month," "we keep running out of filters,"
  "how much cash is sitting in the warehouse," "what is not moving," or "draft
  a PO for my supplier."
allowed-tools: Read, WebFetch
---

# Inventory Planner

Buy what sells, before it runs out, and stop buying what doesn't.

Stock is cash the owner already spent. Two things go wrong: running out of the item customers came for, and sitting on a pallet of something nobody wants. Both are visible in the sales history well before they become a problem, which is what this skill reads for.

## Step 1 — Get sales and stock

**Preferred:** Shopify for sales and inventory levels. Square and NetSuite work the same way.

**Fallback, fully supported:** a CSV of sales history plus a stock-on-hand count. Two files, or one with both. This path works with zero connectors and gives the same output. Many businesses count on a clipboard, and that is a legitimate input.

You need, per item: SKU, name, units sold by date, current stock on hand, unit cost, unit price, vendor, and lead time if known. Missing lead time is asked for once and remembered — see `reference/data_sources.md`.

**Say what the count is as of.** A stock figure two weeks old produces a stockout date two weeks wrong.

## Step 2 — Compute velocity, both windows

For every item, compute:

- **7-day velocity** — units per day over the last week. Catches what is happening now.
- **28-day velocity** — units per day over four weeks. The stable baseline.

Both matter, and disagreement between them is information. An item selling three times its 28-day rate this week is either trending or had one bulk order, and those need different responses. `reference/velocity_and_reorder.md` covers how to tell them apart.

Exclude one-off distortions from the baseline where you can identify them: a single wholesale order, a returned batch, a stockout period where the item could not sell. **A period of zero sales because there was no stock is not zero demand**, and treating it as such is how an item gets under-ordered forever.

## Step 3 — Project stockout dates, conservatively

Stockout date is stock on hand divided by the daily velocity you trust least — the higher of the two windows. Being early is cheap; being late loses the sale.

Then compare against lead time. The number that matters is not when it runs out, it is whether there is still time to order:

- **Past the point of no return** — lead time exceeds days of cover. Already going to stock out. Say so plainly.
- **Order now** — cover is within lead time plus a safety buffer.
- **Order soon** — comfortable, but on the next cycle.
- **Fine** — no action.

**Never state a stockout date for an item with no reliable velocity.** New items with two weeks of history and items whose sales were interrupted get flagged as "not enough history," by name.

## Step 4 — Size the reorder

Default target is **60 days of cover plus the lead time**, sized on the **28-day rate** — not on the faster of the two. The stock has to last from the day it lands until the next order lands, so leaving the lead time out runs the item short by exactly that many days every cycle. Then adjust for pack size, minimum order quantity, and what is already on order.

The two rates do different jobs and both get named on the line: the higher one says when it runs out, the 28-day one says how much to buy. Sizing a 60-day order off a one-week spike is how cash ends up in a pallet.

Never size a reorder without subtracting inbound stock. Double-ordering a slow item is how a business ends up with three years of it.

Round to the vendor's pack size and say which direction you rounded. Show the dollar cost of every recommendation — the owner is deciding about cash, not units.

## Step 5 — Handle the items that are not moving

Zero-velocity and very slow items are a separate list with a separate purpose. **They are never reorder candidates.**

- **Zero velocity** — no units in 28 days. Report as a slow mover with the cash tied up in it. **Never compute days of cover for these** — nothing is selling, so nothing is running out, and the number is either an error or nonsense. The one exception is an item inside a season the owner has named, which goes on a dated watch list instead of the clear-out list.
- **Overstock** — more than 120 days of cover. Report the excess units and the dollars.
- **Dead stock** — no movement in 90 days. Suggest clearing, bundling, or discounting.

Total the cash sitting in these. That figure is usually the most surprising number in the whole report and often the most useful one.

## Step 6 — Apply seasonality only where history supports it

With at least a year of history, compare the coming period against the same period last year and adjust.

**With less than a year, say so and do not adjust.** A seasonal multiplier invented from nine months of data is a guess wearing a suit. Ask the owner instead — they know their season better than a short history does. `reference/seasonality.md` covers both paths.

## Step 7 — Present the buy list

Lead with the total dollar amount and the count of items about to stock out. Then: order now, order soon, slow movers, and anything with too little history to judge.

Every line carries the numbers behind it — velocity, days of cover, lead time, quantity, cost. An owner who can see the reasoning approves in a minute; one who cannot rebuilds the whole thing by hand.

Render the buy list as an HTML artifact using the house artifact style (`../../shared/artifact-style.md`): a stockout table sorted by stockout date with mono tabular-nums numerals, urgency status pills (order now / order soon / fine / past the point of no return), a reorder panel with quantities and dollar totals, and a slow-movers section with the cash tied up in it. The chat summary stays — the artifact is the full picture, not the only one.

## Step 8 — Draft POs and vendor emails, with approval

Purchase orders commit money and vendor emails go out under the owner's name, so both wait for an explicit yes.

State the vendor, the line items, and the total before asking. Draft the vendor email in the owner's voice per [the shared voice profile](../../shared/voice-profile.md). **If no profile exists yet, follow that file's "When there is no sample" instruction** — ask for three emails they have already sent a supplier. If they would rather not, write the email plain and neutral and say it is not in their voice. Never invent a personality for someone's vendor relationship.

With Google Calendar connected, offer a recurring block for the restock decision — this works far better as a rhythm than as a fire drill. Keep the approved PO document here — this skill owns it. With QuickBooks or NetSuite connected, hand `ap-processor` the coded memo for each one (vendor, PO number, total, expected date, and the account, class, and job), so the bill three-way-matches against a real record when it arrives. `ap-processor` reads POs; it does not create them.

## Closing offer

Close with one line on what was decided — the total buy and the items about to run out. Then offer the most relevant next step with its exact trigger phrase: "reorder" (`/restock`) when the owner wants the POs drafted and sent end to end. Up to two more from the router's table, such as "cash forecast" (`cash-flow-snapshot`) or "pay the bills" (`/pay-the-bills`). Three offers at most, and never repeat one the owner already declined this session.

## What not to do

- **Do not invent a velocity, a lead time, or a stockout date.** Too little history is reported by SKU, not smoothed over.
- **Do not treat an out-of-stock period as zero demand.** It is suppressed demand and it biases everything downstream.
- **Do not recommend reordering a zero-velocity item.** No sales means stop buying, not buy more.
- **Do not size a reorder without subtracting what is already inbound.**
- **Do not apply seasonality without a year of history.** Ask the owner instead.
- **Do not send a PO or a vendor email without approval.** Both spend money or spend goodwill.
- **Do not report units without dollars.** The owner thinks in cash.

## Reference files

- `reference/data_sources.md` — Shopify, Square, NetSuite, and the CSV path, with required fields
- `reference/velocity_and_reorder.md` — the 7/28-day math, distortion handling, and reorder sizing
- `reference/seasonality.md` — when to adjust, when to ask, and how to say which you did
- `reference/po_drafting.md` — purchase order structure and vendor email drafting
- `reference/gotchas.md` — the mistakes that stock out a bestseller or bury cash in a pallet

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
