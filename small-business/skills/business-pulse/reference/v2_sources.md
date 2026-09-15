# More sources

Two more legs into the same pulse. The pulse still builds from whatever is connected and degrades gracefully.

---

## Shopify

For a commerce business this is the difference between a pulse that describes their day and one that doesn't.

| Pull | Section it feeds |
|---|---|
| Orders and revenue, today and trailing 7 days | Revenue & Sales |
| Fulfillment status | Watch List — unfulfilled past SLA is the most actionable thing in the pulse |
| Refunds and returns | Watch List |
| Low-stock alerts on moving products | Watch List |

Unfulfilled orders past their promised window belong near the top. They are time-sensitive, they turn into complaints, and no other section surfaces them.

---

## The ledger — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books

Whichever is connected is the system of record for cash, revenue, and AR, and the pulse reports the number the owner's bookkeeper or controller sees. Ledgers are peers (`../../../shared/connector-neutrality.md`): none takes precedence over another. Same metrics, same sections; only the tool names change (`data_sources.md`).

**Two ledgers connected: read both, total from one.** Ask which is the source of record, say which in the Appendix, and take cash, revenue, and AR totals from that one. The other supplies only what it uniquely holds.

---

## The double-count rule

The pulse potentially sees revenue in four places: the ledger, a processor, a storefront, and a POS.

**Pick one revenue source and say which.** Summing them inflates the number, sometimes by more than double, and an owner who spots that stops trusting the whole pulse.

Order: the ledger first (whichever is connected; if two, the owner's named source of record), then the processor, then the storefront. Everything below the chosen source supplies detail — channel splits, product splits, settlement timing — not totals.

```
Revenue — AUD 43,200 MTD (source: Xero; Shopify used for product mix)
```

### One source double-counts too

Picking a single source is not enough. QuickBooks own sales-by-customer summary returns two rows for any customer that has sub-customers or jobs beneath it: a summary row for the parent, and a separate total row carrying the identical figure. The report's built-in top-customer list includes both.

So a customer appears twice in any ranking built straight off those rows — once under its own name, once as "Total for" that name — and every concentration figure computed from them is overstated.

Drop rows whose metadata type marks them as a total before ranking or summing. Keep the parent summary row. This is a guaranteed error on any book that uses jobs or sub-customers, which in the trades is most of them.

---

## Scheduled presets

| Preset | When | Shape |
|---|---|---|
| Monday | Start of week | Full pulse, forward-looking. What's coming, what needs attention |
| Friday | End of week | Recap. What moved, what closed, what slipped |

Same skill, different framing.

**The two are genuinely different documents.** Monday should lead with the week's commitments and the single most important thing to act on. Friday should lead with what actually happened against what was expected. A Friday recap that reads like a Monday brief is a Monday brief sent on the wrong day.

Offer a cadence once, after a pulse the owner found useful. Don't ask twice.
