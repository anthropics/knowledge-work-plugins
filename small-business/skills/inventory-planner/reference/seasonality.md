# Seasonality

When to adjust for the season, when to ask instead, and how to say which you did.

---

## The threshold

**Adjust only with at least 400 days of history.** That gives a full year plus enough overlap to compare the same weeks year over year.

With less than that, do not compute a multiplier. Ask the owner.

The reason is simple: a seasonal factor derived from nine months of data is arithmetic performed on an assumption. It comes out looking like a real number — "1.6x for June" — and it will be used to buy real stock. The owner already knows their season better than that number does, and asking takes one line.

---

## With a year or more

Compare the upcoming planning window against the same calendar window last year, per item or per category.

```
seasonal_factor = units_sold(same window, last year) ÷ units_sold(trailing 28d, last year)
```

Apply the factor to the sizing velocity (the 28-day rate), and to the stockout velocity when projecting into the season. Cap it — anything above 3x or below 0.3x gets shown to the owner rather than applied silently, because factors that extreme usually mean a promotion, a stockout, or a one-time event in last year's data rather than a real season.

Prefer **category-level factors** for items with thin individual history. A single SKU's year-ago numbers are noisy; the category's are not.

**Check for a stockout in last year's comparison window.** If the item was out of stock last June, last June's units understate demand, and the factor built from them will under-order this June. Say so instead of applying it.

---

## Without a year

Say what you have and ask one question:

> I have 120 days of history, so I cannot see your season in the data. You are heading into summer — do filters and capacitors move differently for you then? Give me a rough multiple and I will size the order to it. Otherwise I will plan on the current rate and we adjust as it moves.

Then use whatever they say and **label the buy list with where the number came from**:

> Sized at 1.8x current velocity per your estimate, not from history.

That label is what lets the owner recalibrate next quarter. An unlabeled adjusted number is indistinguishable from a computed one six weeks later.

---

## When the owner names an end to the season

A season has two dates and the second one does the damage. Sizing 60 days of stock at the busy rate, six weeks before the busy period ends, buys a month of stock for a month that will not happen — and it stays on the shelf until next year at the old cost.

**When the owner names an end date, cap the order at the days left in the season.** Do not cap silently:

```
days_left       = season_end_date − expected_arrival_date
target_uncapped = (60 + lead_time_days) × sizing_velocity
target_capped   = days_left × sizing_velocity
```

Show both numbers and say which one is being ordered:

> Ray says the AC season winds down at the end of August — 47 days after this
> order lands, not 60. At 7.0/day with 20 on hand, that's 309 units, so 8 cases:
> USD 1,184. The uncapped number would have been 11 cases at USD 1,628 — the extra
> three cases would sit until next May.

The owner overrides this whenever they want to. Some items are worth carrying over — a filter keeps fine and the price only goes up. Others do not, and a slow tail into the off-season is exactly where the cash gets stuck. **Their call, made with both numbers in front of them.**

Carrying a few days of tail past the end date is fine when the owner asks for it — say the sentence, do not add it silently.

Where the season ends before the stock could even land, do not order at all. Say so plainly and put the item on the watch list for next season with the decide-by date already on it.

---

## Known-event adjustments

Seasonality is not only the calendar. Ask about, and record:

- A big job, contract, or event coming up that will draw down stock
- A promotion or sale planned
- A vendor price increase announced, which sometimes justifies buying early
- A vendor shutdown — many suppliers close for a stretch and lead times double around it

These are one-time adjustments, applied to specific items, and always labeled as owner-supplied rather than computed.

---

## Reporting the adjustment

Every seasonally adjusted line shows both numbers:

```
Compressor, 3-ton                SKU CMP-3T
  Current velocity   0.4/day (28d)
  Seasonal           1.9x — June ran 1.9x the spring rate last year
  Sizing at          0.76/day
  On hand            11 units, 14 days of cover at the seasonal rate
  Status             ORDER NOW
```

Showing the unadjusted rate next to the adjusted one is what makes the adjustment reviewable. An owner who thinks 1.9x is too hot can say so before the PO goes out.

---

## Worked example

Ray's shop, planning into June.

- 120 days of history only. No computed factors.
- Asked Ray directly. His answer: "Filters and capacitors go crazy the first hot week. Compressors maybe double. Everything else is the same."
- Applied 2.0x to filters, capacitors, and compressors on Ray's estimate. Everything else planned at the current 28-day rate.
- Buy list labeled: three categories sized on Ray's seasonal estimate, the rest on trailing velocity.
- Noted for next year: with a full year of history by next spring, these factors can be computed and checked against what he guessed.
