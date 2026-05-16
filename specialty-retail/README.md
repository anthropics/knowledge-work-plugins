# Specialty Retail Plugin

Workflows for specialty retailers that carry **floorplan-financed inventory** — hot tub and spa dealers, pool builders, furniture stores, powersports, RV, marine, appliance retailers, and similar. The generic `small-business` plugin assumes you bill customers and pay vendors and that's it. Specialty retail has extra moving parts the generic plugin can't see:

- **Inventory floorplan financing** — units sit on someone else's balance sheet (Wells Fargo CDF, Synchrony, dealer credit lines) until you sell them, with interest and free-flooring windows you have to track.
- **Refurbished inventory** — you bring used units back into stock, sink labor + parts into them, and need per-unit cost-basis tracking so you know if refurbs make money.
- **Deposit-at-sale, recognize-at-delivery** — large-ticket items collect deposits weeks or months before delivery. Per ASC 606 the revenue doesn't book until you deliver, but most small-business accounting tools treat the deposit as revenue immediately.
- **OEM pricing portals** — Watkins (Hot Spring/Endless Pools/Tylö), Sundance, Bullfrog, Coast Spas, Ashley HomeStore, Polaris, Honda Marine, Sea-Doo, etc. all have dealer portals where you pull current-year wholesale + retail pricing monthly. Most dealers do this by hand.

This plugin pairs with the existing `small-business` plugin — it doesn't replace it. Use `small-business` for the generic close + cash + AR flows, and add `specialty-retail` for the dealer-specific operations.

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install specialty-retail@knowledge-work-plugins
```

## What's in this plugin

### Skills (4)

| Skill | What it does | Just say... |
|---|---|---|
| **floorplan-accounting** | Reconciles your dealer floorplan against your GL, accrues per-unit interest after the free-flooring window expires, and posts paydowns when units sell. Supports Wells Fargo CDF, Synchrony, and dealer-specific credit lines. | "reconcile the floorplan", "WF CDF statement", "free-flooring", "floorplan interest" |
| **refurb-pnl** | Per-unit P&L for refurbished inventory. Tracks labor hours, parts costs, freight, and sale price against the original acquisition cost. Surfaces which refurbs actually make money and which don't. | "refurb P&L", "how did the refurbs do this month", "is the refurb program working" |
| **delivery-revenue-recognition** | ASC 606-compliant revenue recognition for deposit-at-sale, recognize-at-delivery transactions. Posts deposits to Customer Deposits liability until delivery, then recognizes revenue + sales tax + COGS at delivery. Flags any deposit aged > 180 days for review. | "recognize the revenue", "what's stuck in deposits", "ASC 606", "delivery posting" |
| **vendor-pricing-sync** | Monthly pull of current-year wholesale + retail pricing from an OEM dealer portal (Watkins, Sundance, Bullfrog, etc.), diff against your product table, surface changes for review, apply on approval. Handles authentication, XLSX/PDF parsing, and effective-date verification. | "pull Watkins pricing", "sync vendor pricing", "is our wholesale current", "update MSRP" |

There are no commands yet in this plugin — the skills auto-trigger by description, and the four jobs they cover are each one-shot enough that they don't need a multi-step command wrapper. (PRs welcome to add them if you want them as explicit slash commands.)

## What you'll need to connect

**Core:**
- **QuickBooks** — your GL. Required for `floorplan-accounting` and `delivery-revenue-recognition`. Optional for `refurb-pnl` (the skill can also read a Supabase/Postgres ledger directly via SQL if your shop is on a custom ERP).

**Optional, depending on which skills you use:**
- **Stripe** — for `delivery-revenue-recognition` (matches Stripe payment intents to invoice deliveries).
- **Google Drive / OneDrive** — for `vendor-pricing-sync` (download archive of monthly OEM price sheets) and `floorplan-accounting` (filing dealer statements).

**Vendor portal credentials** (kept in your OS keychain, never in plugin files):
- Watkins Access (Hot Spring, Endless Pools, Tylö)
- Wells Fargo CDF (sec2.financeaccess.com)
- Synchrony Dealer Portal (if used)
- Any other OEM portal your shop uses

The `vendor-pricing-sync` skill is the only one that hits a vendor portal directly (via Playwright if you have it installed, or a CSV/XLSX upload fallback otherwise).

## How it pairs with `small-business`

The generic `small-business` plugin handles:
- `/close-month`, `/plan-payroll`, `/run-campaign`, etc.
- Generic AR/AP, cash flow, margin, 1099 prep

This plugin adds the layer specific to dealers carrying floorplan-financed inventory:
- The floorplan reconciliation that `small-business`'s `month-end-prep` doesn't know how to do
- The per-unit refurb tracking that doesn't exist in generic SMB accounting
- The deposit-to-delivery revenue recognition that prevents misclassifying customer deposits as sales income
- The OEM portal pricing sync that keeps your inventory cost basis current

Install both. They complement each other.

## Adapting for your dealer category

These skills were authored against a hot-tub-and-spa dealer's actual books, but the patterns generalize. To adapt:

1. **Floorplan accounting** — swap "Wells Fargo CDF" for your floorplan lender. The math (free-flooring window → accrue interest → paydown at sale) is identical across dealer credit programs.
2. **Refurb P&L** — works as-is for any used-inventory program. The skill reads cost basis + labor + parts + sale price.
3. **Delivery revenue recognition** — works for any large-ticket deposit-at-sale model. Furniture (couch delivered 6 weeks later), powersports (special order), RV (factory build).
4. **Vendor pricing sync** — swap "Watkins Access" for your OEM portal. The skill is portal-agnostic; you provide the login flow and the XLSX/PDF parsing rules.

Skill files are markdown. Fork, edit, deploy. No code required.

## Background

Built and contributed by [East Texas Hot Tub Company](https://easttexashottub.com), a hot-tub-and-spa dealer in Tyler, Texas running on Claude as their AI bookkeeper and operating system. Released under Apache 2.0.

We built these workflows for our own books and decided that other floorplan-carrying SMB dealers would benefit from the same patterns. If you adapt these for your category and want to contribute back, PRs welcome.
