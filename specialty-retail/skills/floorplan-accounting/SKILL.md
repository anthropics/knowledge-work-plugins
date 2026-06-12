---
name: floorplan-accounting
description: >
  Reconciles a dealer floorplan against the general ledger, accrues per-unit
  interest after the free-flooring window expires, and posts paydowns when
  units sell. Designed for SMB retailers using Wells Fargo Commercial Distribution
  Finance (CDF), Synchrony Dealer Finance, or similar inventory-financing programs.
  Use when the user says "reconcile the floorplan", "WF CDF statement", "free
  flooring expired", "floorplan interest", "inventory financing", or "Synchrony
  dealer". Read-only against the GL until the user explicitly approves posting.
compatibility: "Requires QuickBooks (primary GL) OR a Postgres ledger with double-entry posting tables. Vendor floorplan statement (PDF or CSV) as input."
---

# Floorplan Accounting

Reconciles your inventory floorplan against the general ledger and produces the journal entries the books need each month: free-flooring expiry accruals, interest accruals, and unit paydowns at sale.

## Why this exists

Specialty retailers (hot tub, pool, furniture, powersports, RV, marine) often carry inventory on a third-party balance sheet via a floorplan credit program. Wells Fargo CDF, Synchrony Dealer Finance, and Bank of America's dealer-finance arm are the big three in the US. The mechanic is consistent:

1. **OEM ships a unit to the dealer** → lender advances the wholesale cost
2. **Unit sits on the showroom floor** for a free-flooring window (usually 90–180 days)
3. **Free-flooring expires** → lender starts charging interest on the unit's balance
4. **Unit sells** → dealer pays down the unit's principal
5. **Lender sends a monthly statement** with current balances, interest accrued, and units past free-flooring

The generic SMB-accounting `month-end-prep` skill doesn't understand this. This skill does.

## Workflow

### Step 1 — Confirm which floorplan

Ask the user which floorplan lender's statement they're reconciling:
- Wells Fargo CDF (most common — hot tub, pool, furniture, powersports, RV, marine)
- Synchrony Dealer Finance
- Bank of America Dealer Financial Services
- Other (ask for the lender name and statement format)

If multiple floorplans, run one reconciliation per lender — don't merge them.

### Step 2 — Load the statement

The user should provide the monthly statement as a PDF or CSV. Most lender portals export both. Wells Fargo CDF: log in at sec2.financeaccess.com → Reports → Dealer Inventory Summary → export PDF. The PDF includes:

- Current balance per unit (serial number)
- Original advance amount
- Advance date
- Days on floor
- Free-flooring expiry date (or "PAST FREE FLOORING" flag)
- Interest accrued this period
- Paydowns this period

Use the `pdf` skill (Anthropic's pdf plugin) to extract the table. Synchrony uses a similar CSV.

### Step 3 — Reconcile vs the GL

Pull the floorplan liability balance from the GL:

```sql
-- QuickBooks (via QB MCP):
{quickbooks query for the Floorplan Payable account ending balance as of statement date}

-- Postgres ledger (alternative):
SELECT a.account_code, a.name, SUM(l.credit - l.debit) AS balance
FROM gl_journal_lines l
JOIN gl_journal_entries e ON e.id = l.journal_entry_id
JOIN gl_accounts a ON a.id = l.account_id
WHERE e.entry_date <= '<statement_date>'
  AND e.status = 'posted'
  AND a.name ILIKE '%floorplan%'
GROUP BY a.account_code, a.name;
```

Compare:

| Floorplan statement balance | GL balance | Variance |
|---|---|---|
| $XXX,XXX | $XXX,XXX | $X,XXX |

If variance is $0, the floorplan is reconciled and you skip to Step 5 (just post the interest accrual). If variance ≠ $0, investigate before posting anything.

### Step 4 — Identify the variance source

Common variances:
- **Unit sold but paydown not posted** — your GL still shows the unit on floor; the lender already cleared it. Post the paydown JE.
- **Unit advanced but receipt not posted** — your GL doesn't show the unit; the lender already has it on the floor. Post the receipt JE.
- **Statement timing** — statement period ends mid-month, GL is end-of-month. Adjust the cutoff.
- **Interest accrual missed in prior periods** — back-accrue per the statement's interest column, oldest first.

Show the variance breakdown and propose JEs for each line. **Wait for explicit user approval** before posting any of them. Per-unit variance > $10K should trigger a CPA review flag.

### Step 5 — Accrue free-flooring expiry interest

For each unit on the statement marked "PAST FREE FLOORING" with interest accrued this period:

```
DR  Floorplan Interest Expense (6630 or similar)    [interest amount per unit]
  CR Floorplan Interest Payable (2610 or similar)     [same]
```

Or, if you accrue interest directly into the floorplan liability:

```
DR  Floorplan Interest Expense                        [interest amount per unit]
  CR Floorplan Payable (2510 or similar)              [same]
```

Aggregate to a single JE per statement period with a description naming the lender, statement date, and units past free-flooring count.

### Step 6 — Post paydowns

For each unit that the lender shows as paid down this period that hasn't already been posted in the GL:

```
DR  Floorplan Payable                                 [paydown amount]
  CR Bank Operating (1100 / 1110 / wherever you wire)  [same]
```

Match the lender's paydown date to the bank statement line in your operating account. Most floorplans auto-wire from a designated bank account weekly.

### Step 7 — Verify clean state

After all entries are posted:

| Check | Expected |
|---|---|
| Floorplan Payable ending balance | Matches statement to the penny |
| Interest Expense YTD | Matches statement's YTD interest |
| Bank operating account | Matches statement deductions for paydowns |
| Variance from Step 3 | $0 |

If anything doesn't tie, **stop and surface it as an audit finding** — never plug.

### Step 8 — Archive the statement

Save the lender's monthly statement to:

```
finance/statements/<lender-slug>/<lender-slug>-YYYY-MM.pdf
```

Examples:
- `finance/statements/wf-cdf/wf-cdf-2026-04.pdf`
- `finance/statements/synchrony/synchrony-2026-04.pdf`

Statements are part of the close packet and required for an outside CPA's review.

## Approval gates

- **Never auto-post.** Always show proposed JEs with full descriptions and wait for the user's explicit approval per batch.
- **Never plug to make it tie.** If there's a variance you can't explain from the statement, surface it.
- **Never post into a closed period.** Check `accounting_periods.status` (Postgres) or QuickBooks closed-period locks before queueing.
- **Flag per-unit variance > $10K** for CPA review. Floorplan amounts on a single unit are unusual at that scale and likely indicate a data issue.

## Graceful degradation

| Missing piece | Fallback |
|---|---|
| Floorplan statement PDF | Ask for CSV export from the lender portal |
| Both unavailable | Ask user to enter the per-unit data manually (small dealers) |
| GL connection | Ask for a Trial Balance CSV export |
| Multiple floorplans | Run one reconciliation per lender; do not merge |

## Reference files

- `reference/wf-cdf-statement-format.md` — Wells Fargo CDF statement structure, column mappings, common gotchas
- `reference/synchrony-statement-format.md` — Synchrony Dealer Finance CSV format
- `reference/free-flooring-windows.md` — Typical free-flooring windows by OEM (Watkins, Sundance, Jacuzzi, Polaris, Sea-Doo, RV manufacturers)
- `reference/examples/wf-cdf-reconciliation.md` — Worked example: WF CDF April 2026 close
