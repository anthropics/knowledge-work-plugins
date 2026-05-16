---
name: refurb-pnl
description: >
  Per-unit profit-and-loss for refurbished inventory. Tracks each refurbished
  unit through acquisition cost → labor hours → parts → freight → sale price,
  and reports gross margin per unit and aggregate margin for the refurb program.
  Surfaces which refurbs make money and which don't, with enough cost-basis
  detail to support reasonable-comp justification, tax depreciation, or sale
  to a buyer. Use when the user says "refurb P&L", "did the refurbs make money",
  "is the refurb program working", "per-unit refurb", or "refurb margin".
compatibility: "Works against any inventory table that flags refurbished units. Examples assume Postgres with an `inventory.is_refurb` boolean and a `refurb_work_logs` time/parts table; QuickBooks Inventory works too with manual tagging."
---

# Refurb P&L

Per-unit P&L for refurbished inventory. Most SMB-accounting tools treat refurbs as undifferentiated inventory — same cost basis as new units, same margin math. That hides whether the refurb program is making money.

## Why this exists

A specialty retailer that takes used units in trade, brings them back into stock, sinks labor and parts into them, and resells them is running a different business inside the main business. Without per-unit P&L:

- You don't know whether refurbs make 40% margin or break even
- You can't justify the bench tech's time when ownership asks why margins are down
- Tax basis for trade-in inventory is murky (each refurbed unit has a different basis than its acquisition price)
- A future buyer or CPA can't audit the refurb program

This skill produces the per-unit P&L view.

## Data model assumption

The skill assumes you can read inventory rows with:

| Column | Purpose |
|---|---|
| Unit serial number | Primary key |
| `is_refurb` flag (boolean) | Distinguishes from new inventory |
| Acquisition cost | What you paid to bring it in (often $0 for trade-ins, but track the trade allowance) |
| Acquisition date | When you took it in |
| Sale price | What you sold it for (null if unsold) |
| Sale date | When delivered (null if unsold) |

Plus a refurb work log table with:

| Column | Purpose |
|---|---|
| Serial number (FK) | Joins to inventory |
| Date | Work date |
| Tech name / employee_id | Who worked on it |
| Hours | Labor time |
| Parts cost | Total parts/materials used |
| Notes | What was done |

If your system doesn't have a work log table yet, the skill can build one from a CSV the user fills out.

## Workflow

### Step 1 — Determine scope

Ask the user which lens they want:

| Lens | Output |
|---|---|
| **Single unit** | Full P&L for one specific serial number |
| **Sold this period** | All refurbs delivered in a date range — aggregate + per-unit |
| **In progress (bench)** | All refurbs currently on the bench with sunk cost YTD |
| **Full program lifetime** | All refurbs ever, sold + in-progress + abandoned |

### Step 2 — Pull unit cost basis

For each refurb in scope:

```sql
SELECT
  inv.serial_number,
  inv.product_id,
  p.brand,
  p.model,
  inv.acquired_at,
  inv.acquired_cost,
  inv.is_refurb,
  inv.sale_price,
  inv.sold_at
FROM inventory inv
JOIN products p ON p.id = inv.product_id
WHERE inv.is_refurb = TRUE
  AND ... (scope filter from Step 1);
```

### Step 3 — Sum the work logs

For each unit:

```sql
SELECT
  serial_number,
  SUM(hours) AS total_hours,
  SUM(hours * tech_hourly_rate) AS labor_cost,
  SUM(parts_cost) AS parts_cost,
  SUM(freight_cost) AS freight_cost,
  COUNT(*) AS work_entries
FROM refurb_work_logs
WHERE serial_number IN (...)
GROUP BY serial_number;
```

Tech hourly rate comes from your payroll system. If you can't map by tech name, use a default rate (ask the user — most shops use $25–$45/hr for refurb work depending on region).

### Step 4 — Compute per-unit P&L

For each unit:

| Line | Formula |
|---|---|
| Acquisition cost | From inventory.acquired_cost (or 0 for trade-ins) |
| Trade allowance given | If acquired as trade-in, what credit was applied |
| Labor cost | hours × tech rate |
| Parts cost | sum of work log parts |
| Freight | sum of work log freight + any pickup-from-customer cost |
| **Total cost basis** | Sum of the above |
| Sale price | inventory.sale_price (null if unsold) |
| **Gross profit** | Sale price − total cost basis |
| **Gross margin %** | (Gross profit ÷ Sale price) × 100 |

For in-progress units, mark sale price as "TBD" and show the cost basis sunk so far + a break-even sale price.

### Step 5 — Aggregate program P&L

Roll up:

| Metric | Calculation |
|---|---|
| Units sold in window | COUNT |
| Total refurb revenue | SUM of sale prices |
| Total cost basis | SUM of all acquisition + labor + parts + freight |
| Aggregate gross profit | Revenue − Total cost basis |
| Aggregate margin % | Gross profit ÷ Revenue |
| Average days on bench | AVG(sold_at − acquired_at) |
| In-progress units | COUNT where is_refurb=true AND sold_at IS NULL |
| Sunk cost in progress | SUM of cost basis on unsold |
| Abandoned/scrapped units | COUNT with status='scrapped' |
| Scrap loss | SUM of cost basis on scrapped |

Flag any unit with:
- Margin below 20% (low-yield refurb — investigate why)
- Days on bench > 180 (slow-mover — maybe trade allowance was too high)
- Cost basis exceeding original new-unit MSRP × 0.7 (over-invested — should have scrapped earlier)

### Step 6 — Output

**Chat summary** (always):

```
Refurb P&L — [scope]

Aggregate (sold in window):
  Units sold:         N
  Revenue:            $XXX,XXX
  Cost basis:         $XXX,XXX
  Gross profit:       $XX,XXX
  Gross margin:       XX%
  Avg days on bench:  XX days

Top 3 winners (best $ margin):
  • SN XXXXXX — [brand] [model] — sold $X for $X margin (X%)
  ...

Bottom 3 (low margin or loss):
  • SN XXXXXX — [brand] [model] — sold $X for $X margin (X%)
  ...

In progress:
  N units on bench, $XX,XXX sunk cost
  M units on bench > 180 days (review)
```

**XLSX export** (always):
Use the `xlsx` skill. Three sheets:

1. **Sold units** — one row per sold refurb, all P&L columns
2. **In progress** — one row per unsold refurb with sunk cost and target break-even
3. **Program summary** — aggregate rollup, monthly trend if window is long enough

Save as `refurb-pnl-YYYY-MM-DD.xlsx`.

## Approval gates

This skill is **read-only**. No GL writes, no inventory changes, no labor cost recalculation. If the user wants to revise tech rates or recategorize a unit, they do that in the source system — this skill re-reads and re-reports.

## Graceful degradation

| Missing piece | Fallback |
|---|---|
| No refurb_work_logs table | Ask user to upload a CSV with serial + hours + parts |
| No tech hourly rate mapping | Use a single default rate; flag in output |
| No trade allowance tracking | Treat acquisition cost as the trade credit value |
| Inventory table has no is_refurb flag | Ask user to provide a list of refurbed serial numbers |

## Reference

- `reference/per-unit-pnl-format.md` — Recommended P&L line structure for refurbs
- `reference/tech-rate-allocation.md` — How to allocate labor cost when techs work across new repair, refurb, and warranty
- `reference/examples/hot-tub-refurb.md` — Worked example: refurbed Jacuzzi J-385 from trade-in to delivery
