# Velocity and Reorder Sizing

The math, and the judgment around the math.

---

## The two windows

**7-day velocity** = units sold in the last 7 days ÷ 7
**28-day velocity** = units sold in the last 28 days ÷ 28

Both, always, for every item. The point is not to pick one — it is that the gap between them tells you something.

| Pattern | Reading | Action |
|---|---|---|
| 7-day ≈ 28-day | Steady | Plan on the 28-day rate. Easy |
| 7-day much higher | Trending up, or one bulk order | Check the order detail before believing it |
| 7-day much lower | Cooling, or a stockout mid-week | Check whether stock was available all week |
| 7-day zero, 28-day positive | Stopped selling, or stocked out | Check stock history before calling it dead |

**When the two disagree by more than 50%, look at the underlying orders before recommending anything.** One wholesale order of 40 units makes a slow item look like a bestseller for exactly one week, and ordering into that spike is how a pallet gets bought.

---

## Which velocity to plan on

Two different numbers, and they must not be mixed up:

- **`stockout_velocity`** = the **higher** of the 7-day and 28-day rates. Used for days of cover and the stockout date.
- **`sizing_velocity`** = the **28-day** rate. Used for the reorder quantity.

That asymmetry is deliberate:

- Stockout dates should be pessimistic. Being early costs a little carrying cost. Being late costs the sale and sometimes the customer.
- Reorder quantities should be sober. Sizing 60 days of stock off a one-week spike is how cash gets buried.

Say which rate went into each number. An owner who can see "running out on the 5.8 rate, ordered on the 4.1 rate" can override either one in seconds. Never use one word — "planning velocity" — for both, because the two numbers are different on exactly the items that matter most.

---

## Distortions to strip out

**Stockout periods.** Days with zero stock are not days of zero demand. Exclude them from the denominator: velocity is units sold ÷ days the item was actually available. Failing to do this permanently under-orders exactly the items that keep running out.

**Bulk or wholesale orders.** A single order well outside the normal order size distorts the window it lands in. Identify it, report it, and offer both numbers — with and without.

**Returns.** Net them out of the period they were sold in, not the period they came back in.

**Promotions.** A period with a discount running is not a baseline. If promotion data is available, mark those periods. If it is not, and the owner mentions a sale, ask.

**New items.** An item with under 28 days of history has no reliable 28-day velocity. Say "not enough history" by SKU rather than annualizing a week.

---

## Days of cover and the order decision

```
days_of_cover = (stock_on_hand + units_on_order) ÷ stockout_velocity
```

Inbound stock counts. An item with 4 days on the shelf and a pallet landing Thursday is not about to stock out, and flagging it as urgent teaches the owner to ignore the urgent list.

**Zero velocity has no days of cover.** Dividing by zero produces either an error or an absurd number, and either way the item does not belong on this ladder — nothing is selling, so nothing is running out. Skip the cover calculation entirely and send it straight to the slow-mover list with the cash tied up in it. The one exception is a season the owner has named; see below.

Compare against lead time plus a safety buffer. Default buffer is 7 days, or half the lead time, whichever is larger — long lead times need proportionally more room. **Cap the buffer at 30 days.**

```
buffer = min(30, max(7, lead_time_days ÷ 2))
```

The cap matters on slow imports. A 120-day lead time would otherwise produce a 60-day buffer, which quietly turns a 60-day order into a 150-day one and buries a quarter of the year's cash in a container. Past 30 days the right answer is ordering more often, not ordering more.

| Condition | Status | Wording |
|---|---|---|
| cover < lead time | Too late | "Will stock out before an order can land. Ordering now shortens the gap, it does not close it" |
| cover < lead time + buffer | Order now | "X days of cover, Y-day lead time. This is the week" |
| cover < 45 days | Order soon | "Fine for now, put it on the next cycle" |
| cover 45–120 days | Fine | No action |
| cover > 120 days | Overstock | Not a reorder. See the slow-mover list |

### The one carve-out for zero velocity

A pool heater sells nothing in February and that is not dead stock — it is February. When the owner has named a season for an item or a category, a zero-velocity item inside that season does not go on the slow-mover list as something to clear.

It goes on a **dated watch list** instead: the item, the date the owner says its season starts, and the date the decision has to be made, which is the season start minus the lead time.

```
Pool heater, 400k BTU        SKU PHT-400
  Velocity      0/day (28d) — Ray says the season starts around May 15
  On hand       4 units
  Decide by     April 10 — 35-day lead time from the season start
  Status        WATCH, not a slow mover
```

Two rules keep this honest. **The owner names the season; it is never inferred** from a quiet month or from what the item sounds like. And **the watch entry carries a date**, because an undated "seasonal, check later" is how a business misses the first hot week entirely. When the decide-by date arrives with still no sales history, ask — do not size an order from a season that has not started.

---

## Reorder quantity

Sized on the 28-day rate, never on the hot one.

```
target    = (60 + lead_time_days) × sizing_velocity
order_qty = target − stock_on_hand − units_on_order
```

The target covers 60 days of selling **plus** the lead time, because the stock has to last from the day it lands until the next order lands. Sizing 60 days flat means running short by the length of the lead time on every single cycle.

Then adjust:

- Round **up** to pack size, unless that overshoots 90 days of cover at the sizing velocity, in which case round down and say so
- Respect minimum order quantity — see below
- Never return a negative quantity. Below zero means there is already enough; that item goes on the no-action list
- **Always subtract units on order.** When inbound quantity is unknown, say the number assumes nothing is inbound

### Minimum order quantity

**An MOQ is almost always a floor on the whole vendor order, not on each line.** Vendors set a minimum dollar or unit amount per shipment. Check the total against it first — three items that each fall short may clear it together, and splitting one line to hit a shipment minimum orders stock nobody needs.

When the order still falls short and the vendor will not ship, the owner has a real decision, so give them the real numbers rather than quietly padding the order:

```
Ferguson's minimum is USD 1,000. The order as sized comes to USD 888.
Clearing the minimum means one more case — 40 filters, USD 148, about 10 extra
days of stock at the 4.1/day rate.
Order the extra case, hold the order until the next item comes due, or
split it across two vendors?
```

Excess units, excess dollars, and excess days — all three, every time. Then the owner decides. **Never silently round an order up to a vendor minimum.**

---

## Every line shows its work

```
Merv 11 filter, 20x25x1        SKU FLT-2025
  Velocity      4.1/day (28d), 5.8/day (7d) — running hot
  On hand       38 units, none inbound
  Runs out      6.6 days of cover on the 5.8 rate (38 ÷ 5.8)
  Lead time     3 days (Ferguson) + 7-day buffer
  Status        ORDER NOW
  Sized on      4.1/day, the 28-day rate — the 7-day spike is one week old
  Target        258 units — 63 days (60 + 3 lead) × 4.1
  Order         240 units (258 − 38 on hand = 220, rounded up to 6 cases of 40)
  Cost          USD 888 at USD 3.70/unit
```

Two different rates in one block, each labeled. The item runs out on the fast rate because being late loses the sale; it is ordered on the slow rate because a one-week spike is not a reason to buy a pallet. An owner who thinks the spike is real says so and the order gets resized in one step.

The rounding check: 38 on hand plus 240 ordered is 278 units, about 68 days at 4.1/day. Under the 90-day ceiling, so rounding up to a full case is fine. Had it landed over 90 days, the order drops to 5 cases and the line says why.

The owner approves this in ten seconds because the reasoning is visible. A bare "order 240" gets rebuilt by hand every time.
