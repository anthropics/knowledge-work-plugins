---
name: vendor-pricing-sync
description: >
  Monthly pull of current-year wholesale + retail pricing from an OEM dealer
  portal (Watkins, Sundance, Bullfrog, Jacuzzi, Polaris, Sea-Doo, Ashley
  HomeStore, etc.), diff against the dealer's product table, surface changes
  for review, and apply on approval. Handles portal authentication, XLSX/PDF
  parsing, and effective-date verification so the dealer's cost basis stays
  current. Use when the user says "pull <vendor> pricing", "sync vendor
  pricing", "update MSRP", "is our wholesale current", or when the monthly
  trigger fires (typically first Monday).
compatibility: "Requires a product table with wholesale_cost and msrp columns and a way to write updates. Examples assume Postgres; QuickBooks Items work via the QuickBooks MCP. Vendor portal access via Playwright (preferred), API (if vendor offers one), or manual XLSX upload (fallback)."
---

# Vendor Pricing Sync

Monthly pull of OEM wholesale + retail pricing into the dealer's product table. Most specialty-retail dealers manually log into their OEM's dealer portal once a month, download a price sheet, and try to remember to update their POS or accounting system. Errors compound — old wholesale costs make COGS wrong, old MSRPs make customer quotes embarrassing.

This skill automates the pull + diff + apply cycle.

## Why this exists

Every OEM dealer program has a portal where current pricing lives. The mechanic is consistent:

1. **Authenticate** to the portal (username/password, occasionally 2FA)
2. **Navigate to the price-sheet download** (varies by portal)
3. **Download an XLSX or PDF** with current-year wholesale + retail by SKU/model
4. **Find the row for each of your stocked products** in the file
5. **Update your product table** with the new numbers
6. **Archive the file** in case you need to prove what the price was on a given date

Without this skill, the dealer does steps 1–6 by hand, monthly, across N OEM portals (most specialty retailers carry 3–8 OEMs). It takes hours; it gets skipped; it becomes a source of error.

This skill does steps 1–5 automatically, lets the dealer review the diff, and applies on approval.

## Portal coverage

Out of the box, the skill knows how to pull from:

| OEM | Category | Portal | Notes |
|---|---|---|---|
| **Watkins Manufacturing** | Hot tub, swim spa, sauna (Hot Spring, Endless Pools, Tylö) | watkinsaccess.com | XLSX, monthly updates |
| **Sundance Spas** | Hot tub | sundancespas.com/dealer | PDF + XLSX |
| **Bullfrog Spas** | Hot tub | dealer.bullfrogspas.com | XLSX |
| **Jacuzzi** | Hot tub | dealer.jacuzzi.com | XLSX |
| **Polaris** | Powersports | polarisstar.com | XLSX |
| **Sea-Doo / Can-Am** (BRP) | Powersports, marine | brp.com/dealer | XLSX |
| **Honda Marine** | Marine | honda.com/dealers | XLSX |
| **Ashley HomeStore** | Furniture | ashleydealer.com | XLSX |
| **Other** | — | — | User provides URL + login + format hint |

For a portal not on this list, the user provides the login flow once (URL, login selectors, navigation to the price sheet) and the skill stores it locally. Subsequent runs reuse the stored flow.

## Workflow

### Step 1 — Determine vendor + date

Ask which vendor's pricing to pull. Default to the calling dealer's primary vendor if known from a config file.

Check effective date:
- Today's date
- Most recent prior pull date (archived files)
- Vendor's typical update cadence (most are monthly, some quarterly)

If today is < 7 days since last successful pull, ask whether to skip (no change expected) or force.

### Step 2 — Authenticate to the portal

Use Playwright if installed. Credentials come from the OS keychain:

```bash
# macOS example — adapt for Linux (keyctl) or Windows (credman)
WATKINS_USER=$(security find-generic-password -s 'vendor-pricing/watkins-user' -w)
WATKINS_PASS=$(security find-generic-password -s 'vendor-pricing/watkins-pass' -w)
```

**Never** store credentials in this skill's files or in environment variables that ship with the plugin. The skill assumes the dealer has set up keychain entries (one-time setup per OEM).

If Playwright is not installed or login fails (2FA challenge, captcha, etc.), fall back to asking the user to download the file manually and upload it via the chat. Continue from Step 4 with the uploaded file.

### Step 3 — Download the current-year price sheet

Navigate the portal per the vendor-specific recipe in `reference/vendor-recipes/<vendor>.md`. Each recipe has:

- Login URL
- Selectors for username, password, login button
- Navigation path to the price sheet (clicks/page sequence)
- Download link selector
- Expected file format (XLSX/PDF/CSV)
- Effective-date column or header line to verify currency

Save the downloaded file to:
```
finance/vendor-pricing/<vendor>/<vendor>-YYYY-MM-DD.xlsx
```

### Step 4 — Parse the price sheet

Use the `xlsx` skill (or `pdf` for PDF formats) to extract a tidy table:

| SKU | Model | Wholesale | MSRP | Effective Date |
|---|---|---|---|---|

The column mapping is vendor-specific. Each recipe in `reference/vendor-recipes/` includes the parse rules.

**Verify effective date.** If the sheet's effective date is older than today's date, log a warning — the vendor may not have updated this month. Some OEMs ship the same sheet for 2–3 months at a time.

### Step 5 — Diff against current product table

For each row in the parsed sheet, look up the matching SKU in the dealer's product table:

```sql
SELECT id, sku, model, brand, wholesale_cost, msrp, updated_at
FROM products
WHERE brand = '<vendor brand>'
  AND active = TRUE;
```

Build a diff:

| SKU | Model | Old Wholesale | New Wholesale | Δ | Old MSRP | New MSRP | Δ |
|---|---|---|---|---|---|---|---|
| WS01 | Grandee 2026 | $8,200 | $8,450 | +$250 | $15,500 | $16,000 | +$500 |
| ... | | | | | | | |

Show the diff to the user in chat. Sort by absolute price change descending.

### Step 6 — Get approval, apply updates

Ask: "Apply these updates? [yes / no / select specific rows]"

On approval:

```sql
UPDATE products
SET wholesale_cost = <new>, msrp = <new>, updated_at = NOW(), pricing_effective_date = '<effective_date>'
WHERE id = <product_id>;
```

For QuickBooks, use the QB MCP to update Item records similarly.

Log every update to an audit table or markdown log:

```
finance/vendor-pricing/changelog.md
```

Append entries:
```
2026-05-01 — Watkins Manufacturing — 47 SKUs updated, $X aggregate wholesale change, $X aggregate MSRP change. Source: watkins-2026-05-01.xlsx. Approved by: <user>.
```

### Step 7 — Archive the file

The file from Step 3 is already saved. Confirm it's in the right path and committed to source control if the dealer keeps `finance/` in git. Past price sheets are evidence for IRS audits, vendor disputes, and customer pricing disputes ("you charged me $14,000 in March, why is it $14,500 now?" → "here's the Watkins effective-date column").

### Step 8 — Report

```
Vendor Pricing Sync — <vendor> — <date>

Source: <filename>
Effective date in sheet: <date>
SKUs in sheet: N
SKUs matched in product table: M
SKUs unmatched (in sheet but not in our table): K
SKUs missing (in our table, not in sheet): L (discontinued? renamed?)

Applied:
  Wholesale changes: N SKUs, $XXX aggregate
  MSRP changes: M SKUs, $XXX aggregate

Top 5 wholesale increases:
  • [SKU] [Model] — $X → $Y (+$Z)
  ...

Top 5 MSRP increases:
  • ...

File archived: finance/vendor-pricing/<vendor>/<vendor>-YYYY-MM-DD.xlsx
Changelog updated: finance/vendor-pricing/changelog.md
```

## Approval gates

- **Never apply updates without explicit user approval.** Show the full diff first.
- **Never lower a price unless explicitly approved.** Most vendors only raise; a wholesale decrease should trigger a "verify this is real" prompt.
- **Never overwrite custom dealer pricing.** If `products.dealer_custom_price = TRUE`, skip the MSRP update for that SKU.
- **Verify effective date.** Don't apply a sheet that's older than the currently stored `pricing_effective_date`.
- **Archive before applying.** The price sheet file must be saved before any DB writes happen, in case rollback is needed.

## Graceful degradation

| Missing piece | Fallback |
|---|---|
| Playwright not installed | Ask user to download the file manually and upload to chat |
| Portal 2FA / captcha | Same — fall back to manual upload |
| Vendor recipe not in `reference/vendor-recipes/` | Ask user for portal URL, login selectors, file path; offer to write a new recipe file |
| Parsed file column layout doesn't match recipe | Show the header row and ask user to map columns interactively |
| No keychain entry for credentials | Walk user through `security add-generic-password` (macOS) one-time setup |

## Reference

- `reference/vendor-recipes/watkins.md` — Watkins Access login + navigation + parse rules
- `reference/vendor-recipes/sundance.md` — Sundance Spas dealer portal
- `reference/vendor-recipes/_template.md` — How to write a recipe for a new vendor
- `reference/effective-date-checking.md` — How to verify which "current" sheet is actually current
- `reference/examples/watkins-may-2026.md` — Worked example of a Watkins monthly pull
