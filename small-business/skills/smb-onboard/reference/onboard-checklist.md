# Onboard checklist

## The seven interview questions

Ask one at a time. Wait for the full answer before moving on. One follow-up is fine if an answer is vague; do not drill further.

1. **Industry and business type.** "What kind of business do you run? Give me the one-liner."
2. **Team size.** "How many people work with you, including yourself?"
3. **Top three headaches.** "What are your three biggest headaches right now — the things that eat your time or keep you up at night?"
4. **Tools already in use.** "Which tools do you already use day-to-day? Your bookkeeping software, email, online store or point of sale, a CRM, team chat…" Ask by category, never by product name. The owner names the vendors.
5. **Preferred cadence.** "How would you like me to check in — daily, weekly, or only when you ask?"
6. **Website and brand look.** Run the `brand-style` skill's capture-and-preview flow (Steps 2–3 there): a pasted website link auto-pulls logo, colors, and tagline; with no site, a plain-words description ("forest green and cream") is translated to colors. Never hex codes, pickers, or uploads. The welcome page in Step 6 doubles as the live preview.
7. **Output format.** Run `brand-style` Step 4 — the six-way multiple choice: visual artifacts (default) / Word docs / markdown / Notion pages / Canva Docs / best for the skill. Store the answer verbatim as one of: `visual artifacts`, `docx`, `md`, `notion`, `canva`, `best for skill`.

If the owner is short on time, compress to questions 1, 3, and 4 — those three feed the most downstream skills. Skipped questions keep their defaults (visual pages for output).

---

## Connector priority matrix

Map the owner's stated headache to the two **categories** of tool to link first. The plugin never recommends a vendor inside a category (`../../../shared/connector-neutrality.md`): it asks what the owner already uses, and connects that.

| Primary headache | First category | Second category | Prove-value recipe |
|---|---|---|---|
| Cash flow / invoicing | Accounting ledger | Payments or point of sale | `cash-flow-snapshot` |
| Customer follow-up | CRM | Mail | `lead-triage` — the growth quick-win, ranks who to call back first |
| Hiring / job posts | Mail | Calendar | `job-post-builder` |
| Staying organized | Desktop (folder setup) | Mail | Desktop folder structure demo |
| Scheduling overload | Calendar | Mail | `business-pulse` |
| Selling online / stock | Storefront or point of sale (holds orders and stock) | Accounting ledger | `inventory-planner` |
| General / unsure | Mail | Accounting ledger | `cash-flow-snapshot` |

One optional third category for the customer follow-up row: **lead data and enrichment**, which fills in company size and industry when the CRM's leads carry no company record. It is metered (credits per row), so it is never the first ask and never named by vendor here — if the owner already has one, connect it after the CRM and `lead-triage` uses it; if not, the recipe runs without it.

**How to fill a category.** Ask what the owner uses for it: *"What do you use for bookkeeping?"* Then one of three, in this order, said once with the trade-off in one line:

1. **We have the connector** (see the category table in `../../../shared/connector-neutrality.md`) — guide the connection.
2. **We do not** — offer `build-connector`, which checks the connector directory and connects through Zapier otherwise. Say what the connection unlocks and what it costs them in setup time.
3. **They do not want the Zapier connection, or have no tool in that category** — run the recipe's zero-connector path (CSV, pasted text) and move to the next category. Name the category, not a product, when saying what would make it deeper.

Never suggest the owner switch to a tool we support. If they ask "which one should I get?", that is an explicit invitation: describe what each connector in the category unlocks, in the same number of words each, alphabetically, and leave the choice with them.

---

## Recipe selection

Run the prove-value recipe immediately after the **first** connector is live — do not wait for the second. If connectors are already active at session start, run the matched recipe for the owner's primary headache before beginning the interview. Keyed by category, whichever connector fills it:

1. Any accounting ledger, or any payments / point-of-sale connector → `cash-flow-snapshot`
2. Any CRM → `lead-triage` (rank the open leads, recommend today's callbacks — nothing is written back)
3. Any storefront or point-of-sale connector that holds orders and stock → `inventory-planner` (a payments-only connector with no stock data belongs under rung 1)
4. Any mail connector → search for unread invoice-related emails, surface top 3
5. Calendar → `business-pulse`
6. Desktop only → walk Desktop folder setup, create recommended structure

### Connector-specific setup notes

These are technical steps one connector needs before its recipe can run. They are not preferences.

- **QuickBooks `profile_info_required`:** if QuickBooks returns this status (missing business_name or industry), use the `quickbooks-profile-info-update` tool with the owner's business name from interview question 1 before running `cash-flow-snapshot`. Do not skip the recipe — collect the missing info first.
- **HubSpot portal readiness:** before running `lead-triage` as the recipe, count contacts with one `search_crm_objects` call (limit 1; read `total`). Zero means the recipe would rank an empty list: say so in one line, offer `manage_onboarding` (action `SET_GOAL`) to start HubSpot's own setup, and run the recipe only once contacts exist — or on a pasted lead list if the owner prefers. `get_user_details` also returns an `onboarded` flag; treat it as a hint about HubSpot's guided setup, not as the test, because a portal with hundreds of contacts can still report `onboarded: false`. This is a technical readiness step for one connector, not a preference.

### Country, currency, and financial year — read from the ledger first, then the storefront

Once the first ledger connector is live, read the organisation record before the recipe runs and fill the three locale fields in the profile without asking: QuickBooks `company_info`; Xero `get_organisation_info` and `get_organisation_financial_year`; MYOB `myob_get_financial_year_dates`; NetSuite `ns_getSubsidiaries` (country and currency; ask for the year end if the connector does not expose it); Zoho Books `get_organization` (`country_code`, `currency_code`, and `fiscal_year_start_month`, a zero-based month index — the year end is the last day of the month before it). Take what the connector exposes.

If no ledger is connected but a storefront or point-of-sale connector is, read its shop record instead — Shopify `get-shop-info` (country and currency); Square the merchant record via `make_api_request` (`country`, `currency`). Neither holds a financial year end, so ask that one field alone during the interview: *"When does your financial year end?"* — do not re-ask country or currency. Storefronts are peers here as everywhere (`../../../shared/connector-neutrality.md`): read whichever is connected.

If neither a ledger nor a storefront is connected, or the record is missing a field, ask one question during the interview: *"Which country is the business in, and what currency do you invoice in?"* Financial year end defaults to the country's common convention only after the owner confirms it. The rule and the field formats are in `../../../shared/currency-and-locale.md`.

---

## Owner profile — storage format

Write this block to the Cowork session memory directory under the heading `## Business context`. Every other skill reads this section by heading match. Do not rename the heading or change the field names.

```markdown
## Business context

- **Business:** <one-liner — industry, product/service>
- **Size:** <number of people, including owner>
- **Top headaches:** <headache 1> · <headache 2> · <headache 3>
- **Connected tools:** <comma-separated list of active connectors, by product name — "Trello", never a registration name like "small-business:trello">
- **Country:** <ISO 3166 two-letter code, e.g. GB, AU, NZ, US, CA>
- **Currency:** <ISO 4217 code the business invoices in, e.g. GBP, AUD, USD>
- **Financial year end:** <day and month, e.g. 30 June, 31 March, 31 December>
- **Weekly cadence:** <trigger phrase and day, e.g. "weekly check-in every Monday">
- **Website:** <URL, if any>
- **Brand colors:** <primary and secondary colors, from the website or the owner's plain-words description, if any>
- **Logo:** <logo image URL pulled from the website, if any>
- **Output preference:** <"visual artifacts" (default), "docx", "md", "notion", "canva", or "best for skill">
- **Notion destination:** <the parent page or database the owner named for skill output, if the preference is "notion"; asked once, the first time a skill needs it>
- **Canva brand kit:** <the name and id of the Canva brand kit the owner chose for skill output, or "none", if the preference is "canva"; asked once, by brand-style Step 4 or the first time a skill needs it>
- **Onboarded:** <YYYY-MM-DD>
```

If a memory file already exists, append or update only the `## Business context` section. Do not touch other content.

**Return sessions with an older profile.** If the block exists but has no Country, Currency, or Financial year end line (profiles written before these fields existed), read them from the ledger if one is connected, otherwise ask the one locale question, and update only those three fields. Do not re-interview.
