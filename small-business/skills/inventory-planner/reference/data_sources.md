# Data Sources

Where sales and stock come from, and what has to be in the data before any of the math is trustworthy.

---

## Required fields

Everything downstream depends on these. Anything missing gets asked for once and remembered.

| Field | Needed for | If missing |
|---|---|---|
| SKU or item ID | Everything | Cannot proceed for that item |
| Item name | The report being readable | Use the SKU and say the name is missing |
| Units sold, by date | Velocity | No velocity, no stockout date. Flag the item |
| Stock on hand | Days of cover | Flag; velocity alone cannot tell you when it runs out |
| As-of date for the count | Accuracy of everything | Ask. A stale count is the most common silent error here |
| Unit cost | Dollar figures on the buy list | Report units only for that item and say why |
| Unit price | Overstock cash and margin context | Optional, useful |
| Vendor | PO drafting | Group as "vendor unknown" and ask |
| Lead time | Whether there is still time to order | Ask once per vendor and remember |
| Units on order | Not double-ordering | Ask. This one is worth chasing — it causes real over-buying |
| Pack size / MOQ | Realistic quantities | Round to whole units and note it was not applied |

---

## Shopify

The preferred source. Pull:

- Orders with line items over the lookback window, at least 90 days, 400 days if seasonality is in scope
- Inventory levels per variant per location (`get-inventory-levels` takes one `productId` per call; loop the products the run needs — `../../../shared/connector-call-shapes.md`)
- Product and variant records for cost, price, and vendor

Watch for:

- **Multi-location inventory.** Total across locations only if the owner sells from one pool. Otherwise stockouts are per location and a total hides them.
- **Variants.** Velocity belongs at the variant level. A shirt that sells fine in medium and never in XL looks healthy at the product level.
- **Cancelled and refunded orders.** Exclude them from units sold.
- **Bundles and kits.** A bundle sale consumes component stock. If the store uses bundles, ask how components are tracked before trusting the numbers.

## Square

Same shape, different names. Sales come from transactions, stock from the item catalog inventory counts. Square inventory tracking is often partially enabled — check which items actually have counts before treating a zero as a zero.

## NetSuite

The ERP path for the top end. Item records carry cost, preferred vendor, lead time, and reorder points already set by someone. **Use the existing reorder points as context, not as truth** — they are frequently years stale, and pointing out where the computed number diverges from the stored one is genuinely useful.

---

## The CSV path

A fully supported first-class mode. Two files or one.

**Sales history file**, one row per sale or per item-day:

```
sku, date, units_sold
```

**Stock file:**

```
sku, name, on_hand, unit_cost, vendor, lead_time_days, on_order
```

Accept whatever column names came out of their system and map them. Report the mapping back so the owner can catch a wrong guess before it becomes a purchase order.

**Ask for the as-of date of the stock count.** It is almost never in the file, and it is the difference between a stockout date that is right and one that is two weeks late.

---

## Data quality checks before any math

Run these and report what they find:

1. **Negative stock.** Real in most systems, and it means the count is wrong. Flag it.
2. **Items with sales and no stock record**, or stock and no sales record.
3. **Duplicate SKUs** with different names.
4. **A history window shorter than 28 days** — say so; the 28-day velocity will not be reliable.
5. **Zero-sales stretches** that coincide with zero stock. These are stockouts, not demand. See `velocity_and_reorder.md`.

---

## Worked example

Okonkwo Mechanical stocks common parts on the trucks and in the shop. No Shopify — Ray exported two CSVs from his supply-house portal and counted the shop shelf on a Saturday.

- 84 SKUs, 120 days of usage history
- Stock count as of 3/15, confirmed with Ray
- Lead times missing for all of them; Ray gave two by vendor: Ferguson 3 days, Watsco 10 days
- 6 SKUs had usage but no stock line — parts pulled straight to jobs, never shelved. Excluded and reported
- 2 negative counts flagged, both compressors, both recounted
