# Gotchas

The mistakes that stock out a bestseller or bury cash in a pallet. Inventory errors are slow and expensive — they show up as a missed sale or a shelf nobody touches for two years.

---

## Gotcha: counting a stockout as zero demand

**Why it matters:** This is the most damaging error in the whole skill, and it is self-reinforcing. The item ran out because it sells. The zero-sales days drag the velocity down. The next order is smaller. It runs out sooner. Repeat.

### Bad

```
Merv 11 filter: 12 units sold in 28 days = 0.43/day. Slow mover, no reorder.
```
(the shelf was empty for 20 of those 28 days)

### Good

```
Merv 11 filter: 12 units in the 8 days it was actually in stock = 1.5/day.
Out of stock 20 of the last 28 days — that is suppressed demand, not slow sales.
Planning on 1.5/day.
```

---

## Gotcha: ordering into a one-week spike

**Why it matters:** A single bulk order makes an ordinary item look like a runaway for exactly seven days. Sixty days of cover sized off that number is a pallet the owner paid for and will look at for a year.

### Bad

7-day velocity 5.8/day vs 28-day 0.4/day. Size 60 days at 5.8/day.

### Good

```
7-day rate is 14x the 28-day rate. Looking at the orders: one sale of 40 units
on the 9th. That is a job, not a trend. Sizing on the 28-day rate and noting
it in case that customer comes back.
```

---

## Gotcha: recommending a reorder for a zero-velocity item

**Why it matters:** Zero sales in 28 days means stop buying. A reorder point set years ago in the ERP will happily say otherwise, and following it converts working capital into shelf decoration.

### Bad

NetSuite reorder point says 24, on hand is 6, so order 18.

### Good

```
Zero units sold in 28 days. The stored reorder point says 24 — that is stale.
Not a reorder. Six units, USD 340 tied up. Worth clearing.
```

---

## Gotcha: forgetting what is already on order

**Why it matters:** Two orders for the same item three weeks apart is the classic double-buy, and it usually happens right after a stockout scare when the owner is paying attention.

### Bad

On hand 38, target 258, order 240.

### Good

```
On hand 38, 160 already inbound from the 3/2 order, target 258 total.
That leaves 60 — 2 cases of 40, so 80 units. If that inbound number is
wrong tell me, it changes this.
```

---

## Gotcha: a stock count with no as-of date

**Why it matters:** Everything downstream is stock divided by velocity. A two-week-old count on a fast mover produces a stockout date that has already passed.

### Bad

Take the uploaded count at face value and project from today.

### Good

Ask when it was counted. If the count is from the 1st and today is the 15th, either net out two weeks of sales or ask for a fresh count on the fast movers, and say which you did.

---

## Gotcha: seasonality invented from partial history

**Why it matters:** A multiplier computed from nine months looks exactly like one computed from three years. It gets used to buy real stock, and nobody can tell later which kind it was.

### Bad

```
June factor: 1.6x (computed)
```
(from 120 days of data that do not include a June)

### Good

```
120 days of history — no June in there, so I cannot compute a season.
You know this better than the data does. Roughly how much heavier is June?
```

---

## Gotcha: velocity at the product level instead of the variant

**Why it matters:** A product that sells well in one size and never in another looks healthy in aggregate. The good size stocks out while the bad size accumulates, and the product-level number shows neither.

### Bad

Filter, 20x25: 4.1/day, 38 on hand, healthy.

### Good

Split by variant. The 1-inch is running out in four days; the 4-inch has nine months of cover. Two different problems, one product line.

---

## Gotcha: reporting units without dollars

**Why it matters:** Owners decide about cash. "Order 240 filters" is not a decision they can make; "USD 888" is.

### Bad

A buy list of quantities with no cost column.

### Good

Every line costed, every vendor subtotaled, and the total stated before the approval question.

---

## Gotcha: quietly accepting a vendor substitution

**Why it matters:** A different part number goes onto a customer's equipment. That is the owner's call and sometimes a warranty question, never a shipping detail.

### Bad

Vendor swaps a compatible capacitor, order updated, nothing said.

### Good

Report the substitution, the part numbers both ways, and the effect on cover if the owner rejects it. Then let them decide.
