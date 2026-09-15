# Currency, country, and financial year — plugin-wide rule

Scope: **every skill that emits an amount, a date in prose, or a period
("this quarter," "year to date").** The plugin is global. Nothing it emits
assumes US dollars, a calendar-year business, or US tax law unless the
business context says the business is in the US.

---

## Where the values come from

Three fields in the `## Business context` block, captured by `smb-onboard`
(format in `skills/smb-onboard/reference/onboard-checklist.md`):

```
- **Country:** <ISO 3166 two-letter code, e.g. GB, AU, NZ, US, CA>
- **Currency:** <ISO 4217 code the business invoices in, e.g. GBP, AUD, USD>
- **Financial year end:** <day and month, e.g. 30 June, 31 March, 31 December>
```

**Read them from the ledger before asking.** When a ledger connector is
live, the organisation record carries all three: QuickBooks `company_info`,
Xero `get_organisation_info` and `get_organisation_financial_year`, MYOB
`myob_get_financial_year_dates`, NetSuite `ns_getSubsidiaries` (the
subsidiary record carries country and base currency; the financial year end
comes from the accounting-period setup, so ask if the connector does not
expose it), Zoho Books `get_organization` (`country_code`, `currency_code`,
and `fiscal_year_start_month` as a zero-based month index — `0` is January,
so the year end is the last day of the month before that index). Field names
differ per connector; pull what the connector exposes and ask only for what
it does not.

**If they are absent when a skill runs,** ask once, in one question: *"Which
country is the business in, and what currency do you invoice in?"* Store the
answer in the block so it is never asked again. Do not block the deliverable
on it: run with the answer for this session if the owner is mid-task and
would rather store it later.

**Never guess a country from a vendor.** A Xero org is not automatically
Australian; a QuickBooks company is not automatically American. Read the
record or ask.

---

## Amounts

- **ISO code prefix, always.** `GBP 1,240`, `AUD 18,400`, `USD 0.50`. Never a
  bare `$`, `£`, or `€` in anything a skill emits: a bare symbol is ambiguous
  across four dollar currencies and renders wrong in a mono column.
- **The currency is the stored one.** Every amount a skill emits is in the
  business's `Currency`. A processor that settles in another currency (a
  Stripe payout in EUR to a GBP business) is shown in its own currency with
  the settlement currency named, never silently converted.
- **Spreadsheet number formats use the code, not a symbol.** `"GBP "#,##0.00`
  in place of `$#,##0.00`. Negative values in red still applies.
- **Abbreviations keep the code.** `GBP 43k`, `AUD 1.2m`.

---

## Thresholds

Skills carry rounding and attention thresholds ("flag a difference over
0.50," "expenses over 25 with no receipt," "vendors paid 600 or more").

- **Write thresholds as numbers in the stored currency,** not as USD figures.
  `0.50`, `25`, and `200` are the plugin's rounding and attention cut-offs in
  whatever the business invoices in. They are judgment lines, not legal ones,
  and they do not need converting.
- **A legal threshold names its law.** The 1099-NEC 600 line is US federal
  law. A skill that uses it says so, and applies it only when `Country` is US.
  There is no generic "contractor threshold"; the number belongs to a regime.

---

## Country-scoped flows

Some skills are built for one country's rules today. They do not pretend
otherwise:

- **Check `Country` before running the country-specific path.** If it is not
  the country the path was built for, say so in one line, say what the skill
  can still do, and stop the country-specific math. Example: *"The quarterly
  estimate and 1099 paths are built for US federal tax. Your books are in the
  UK, so I'll hand your accountant the closed-books packet instead of a US
  estimate."*
- **Never run a US calculation on a non-US business and label it an
  estimate.** A wrong tax number with a confident label is the failure this
  rule exists to prevent.
- **Flows scoped this way today:** `tax-season-organizer` and `/tax-prep`
  (US federal estimates and 1099s), `grant-rfp-writer`'s opportunity
  sources (US federal and state portals), `hiring-screener`'s onboarding
  paperwork list (US forms), `job-post-builder`'s offer letter (US
  employment terms, already carrying a jurisdiction disclaimer).

---

## Periods and dates

- **"This quarter," "year to date," "FYTD," "last financial year" resolve
  against `Financial year end`,** not the calendar year, unless the owner
  says calendar. Resolve the financial-year dates once per run and reuse
  them. A 30 June year-end business asking for "Q1" means July to September.
- **Dates in prose follow the owner's country convention** ("14 March" for
  most of the world, "March 14" for the US). Dates in filenames stay ISO
  `YYYY-MM-DD` everywhere.
- **Deadlines belong to a regime.** "Due 15 September" is a US federal
  estimated-tax date. It appears only on the US path.

---

## Worked examples in reference files

The plugin's reference files carry hundreds of illustrative figures written
as `USD 1,240`. They are examples of shape and tone, not output. They may
stay in USD. The rule above governs what a skill emits for a real business,
not what a reference file shows as an illustration. New examples may use any
currency; a mix across the plugin is fine and mildly preferable.
