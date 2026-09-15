# Connector Map

Required and optional connectors per skill, plus each skill's zero-connector fallback. The router uses this to avoid recommending something that will partially fail, and to offer the fallback path instead.

**The lists below are the tested paths, not a wall.** When the owner wants a skill to use a tool that is not listed for it, route to `build-connector` first — it checks the connector directory, then connects through Zapier. Once the connection exists, the tool joins that skill like any other optional connector, with the same approval gates.

Every skill works with zero connectors. "Required" below means required for the *connected* path — the fallback column is always available.

**Call shapes.** Parameter shapes that connectors require and tool descriptions do not make obvious are collected in [`../../../shared/connector-call-shapes.md`](../../../shared/connector-call-shapes.md); a skill reads the row for a connector before its first call to it.

**One product, possibly two entries.** The owner's own connector and the plugin's manifest registration of it (`small-business:<name>`) count as one; a gate opens if either is authorized (`../../../shared/connector-neutrality.md`, "One connector, two registrations").

**Gates are categories, not vendors.** Where a row says "a ledger," any of MYOB, NetSuite, QuickBooks, Xero, or Zoho Books opens the gate; "a payments connector" is any of PayPal, Square, or Stripe; "a CRM" is any of HubSpot, Monday.com, Salesforce, or Zoho CRM (Salesforce is owner-added as a custom connector, not in the manifest); "a storefront" is either of Shopify or Square (the connectors that hold orders and stock); "Mail" is either of Gmail or Microsoft 365; "a file store" is either of Google Drive or Microsoft 365 (Microsoft 365 is one connector covering both of those categories, and is owner-added as a custom connector, not in the manifest); and none ranks above another (`../../../shared/connector-neutrality.md`). Vendor lists are alphabetical. Capability limits that matter to a gate are in the footnotes under each table, stated as what the connector holds, not as a ranking.

---

## Run the business

| Skill | Required | Optional | Zero-connector fallback |
|---|---|---|---|
| `report-builder` | any one data source | Expensify, HubSpot, MYOB, NetSuite, PayPal, QuickBooks, Ramp, Shopify, Square, Stripe, Xero, Zoho Books | CSV/XLSX upload — fully functional |
| `business-pulse` | none | Calendar, DocuSign, Expensify, Gmail or M365, Gusto, HubSpot, MYOB, NetSuite, PayPal, QuickBooks, Ramp, RingEx Chat, Shopify, Slack, Stripe, TikTok Ads, Xero, Zoho Books, Zoho Desk | builds from whatever exists, or pasted data |
| `cash-flow-snapshot` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) or a payments connector (PayPal, Square, or Stripe) | Gusto, Ramp, Shopify | CSV upload |
| `month-end-prep` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) | Expensify, Gusto, PayPal, Ramp, Shopify, Square, Stripe | statement/CSV uploads |
| `invoice-chase` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) | Airwallex, Gmail, Microsoft 365, PayPal, Shopify, Square, Stripe | AR CSV in, drafted reminders out |
| `ap-processor` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) + Mail (Gmail or M365) | Expensify, Ramp | PDF/photo bill upload, entries exported |
| `payroll-prep` | Gusto or QuickBooks Payroll | a ledger with a write path, for the journal post | timesheet upload → validated run sheet |
| `inventory-planner` | Shopify or Square | Calendar, NetSuite, QuickBooks | sales + stock CSV |
| `inbox-manager` | Gmail or M365 | Slack | pasted/forwarded email text |
| `hiring-screener` | Mail (Gmail or M365) + Calendar | DocuSign, Drive or M365, Gusto, Trello | resume uploads, drafts for manual send |
| `job-post-builder` | none | DocuSign, Drive or M365 | fully standalone |
| `contract-review` | none (file upload) | DocuSign, Drive or M365, Gmail or M365 | file upload is the primary mode |
| `tax-season-organizer` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) | Expensify, Gusto, PayPal, Ramp, Square, Stripe | CSV/document upload; the tax math is US-only (`../../../shared/currency-and-locale.md`) |
| `ticket-deflector` | a payments connector (PayPal, Square, or Stripe), a CRM, or Mail | Atlassian, RingEx Chat, Shopify, Zoho Desk | pasted text |

Ledger capability notes (what each holds, per its own reference files):
- **MYOB** — P&L, AR and AP balances, sales totals, payment terms. No bank or cash balances, no vendor or payee detail, no customer email addresses. A skill that needs those asks the owner or uses another source, and says so.
- **Xero** — P&L, bank transactions, bills, invoices, aged receivables, organisation record. Bill and invoice attachments are visible. See `../../month-end-prep/reference/xero-reconcile.md`.
- **NetSuite** — full ledger via reports and SuiteQL. Common at the larger end of the segment.
- **QuickBooks** — full ledger, with the report traps in `../../../shared/quickbooks-report-traps.md`.
- **Zoho Books** — invoices, estimates, sales orders, expenses, purchase orders, customer payments, bank and cash account balances, contacts with a 1099 flag, organisation record. No bill object, no bank-transaction feed, no journals, no report endpoints (P&L, cash flow, aging). A skill that needs those asks for the export and says so; see `../../month-end-prep/reference/zoho-books-reconcile.md`.
- Two ledgers connected: read both, one named as the source of record for totals, never summed.

Storefront and point-of-sale capability notes (what each holds, per its own reference files; the category is defined in `../../../shared/connector-neutrality.md`):
- **Shopify** — orders, customers, products with images, stock levels, and ShopifyQL analytics; shop record carries country and currency. No payouts: the connector's scopes exclude Shopify Payments, so settlement timing is asked of the owner, never inferred (`../../cash-flow-snapshot/reference/v2_sources.md`). One `productId` per inventory read (`../../../shared/connector-call-shapes.md`).
- **Square** — orders with line items, catalog with images, inventory counts, payments, and payouts; merchant record carries country and currency. Payments list one location per call, so skills iterate locations. Payouts can be structurally absent on a production account.
- A storefront alone satisfies any gate written as "a CRM, a payments connector, or a storefront": order history is who bought what and when.
- Storefront and payments connectors both connected: an order and its settlement are one sale. Revenue comes from the one the owner names as source of record; the other supplies timing, fees, or stock.

## Grow the business

| Skill | Required | Optional | Zero-connector fallback |
|---|---|---|---|
| `lead-finder` | Apollo or Clay | HubSpot | web research + customer CSV |
| `outreach-composer` | Gmail or M365 | Apollo, Clay, HubSpot, Mailchimp | draft-only, paste anywhere |
| `speed-to-lead` | HubSpot + Mail (Gmail or M365) | Calendar, RingEx Chat | forwarded/pasted inquiries |
| `lead-triage` | HubSpot | Apollo, Calendar, Clay, Gmail or M365 | pasted/uploaded lead list |
| `proposal-builder` | Drive or M365 | Apollo, Atlassian, Canva, DocuSign, Notion, Trello, Zoom; a ledger or a payments connector for pricing history and the deposit invoice | uploads in, DOCX/PDF out |
| `crm-autopilot` | a CRM (HubSpot, Monday.com, Salesforce, or Zoho CRM) | Calendar, Notion, RingEx Chat, Trello, Zoom | built-in spreadsheet CRM |
| `growth-pulse` | HubSpot + one revenue source | Mailchimp, PayPal, Shopify, Square, Stripe, TikTok Ads | CSV exports |
| `content-strategy` | QuickBooks or PayPal | Shopify, Square | sales CSV |
| `social-content-engine` | Canva | HubSpot, Mailchimp, Notion, Shopify, Trello | calendar + copy + briefs for manual posting |
| `canva-creator` | Canva, HubSpot | Shopify, Square — product photos and prices read from the store before the owner is asked for them | brief in; calendar, copy, and asset briefs out for manual design and posting |
| `review-reputation` | a CRM, a payments connector (PayPal, Square, or Stripe), or a storefront (Shopify or Square) | Gmail or M365, Zoho Desk | pasted/exported reviews + web |
| `ad-manager` | TikTok Ads (native); other ad platforms via a `build-connector` Zapier connection | Canva | CSV performance exports — the common path today |
| `seo-ai-visibility` | none (web-native) | Shopify, Wix | crawls any public site |
| `grant-rfp-writer` | Drive or M365 | DocuSign, Calendar, Trello | document upload + web search |

## Build & meta

| Skill | Required | Optional | Fallback |
|---|---|---|---|
| `build-agent` | none | whatever it builds against | native |
| `build-connector` | none | Emergent, Zapier | it builds the fallback |
| `smb-onboard` | none | all | interview-based, recommends what to connect |
| `brand-style` | none | website via WebFetch | plain-words brand description; house default on skip |

## Commands (11 folders + 1 in-skill chain)

The eleven command folders are listed below. The twelfth flow is the scheduled inquiry chain that lives inside the `speed-to-lead` skill rather than in its own folder, and its gate matches `speed-to-lead` (HubSpot + Gmail).

Commands inherit the requirements of the skills they chain. The lead skill's requirement decides whether the command can start; optional legs degrade per skill.

| Command | Gate to start |
|---|---|
| `/report-pack` | any one data connector, or CSV |
| `/pay-the-bills` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) + Mail (Gmail or M365) |
| `/restock` | Shopify, Square, or CSV |
| `/grow-pipeline` | Apollo or Clay, + HubSpot |
| `/marketing-monday` | any one of PayPal / Shopify / HubSpot; TikTok Ads adds the paid-spend layer |
| `/reactivate` | a CRM, a payments connector (PayPal, Square, or Stripe), or a storefront (Shopify or Square); a ledger and a support desk add invoice and service history |
| `/plan-payroll` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books); Gusto or QuickBooks Payroll for the timesheet leg |
| `/close-month` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) |
| `/tax-prep` | a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books); the tax math runs only for a US business |
| `/monday-brief` | none — degrades gracefully |
| `/call-list` | HubSpot; Mail (Gmail or M365) adds email context, Google Calendar adds the blocks, Apollo or Clay adds company fit (metered, asked once) |
