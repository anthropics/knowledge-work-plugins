# One CRM of record

The same rule the ledger follows, applied to the CRM: **a business has one
CRM, and skills read it — not two blended together.** HubSpot, Monday.com,
Salesforce, and Zoho CRM are peers (`connector-neutrality.md`); whichever is connected is
the CRM of record. If two are connected, the owner names one (the router's
Step 5 multiple-choice), the skill says which, and reads only that one for
the lead pool and pipeline totals. Two CRMs merged produce duplicate
contacts, double-counted pipeline, and a call list with the same person on it
twice.

**Verify the org before any record contributes to an answer.** Zoho's
`getOrganization` returns the company name; if it doesn't match the business
you're working for, stop and say so rather than reporting another company's
pipeline.

**An auth banner is not an outage.** Probe with one cheap read before
declaring a CRM unavailable and falling back to CSV.

---

## Field mapping — HubSpot, Salesforce, Zoho CRM

These three model leads differently, and the difference matters more than the
field names. Monday.com has no lead object; its board-as-CRM shape is in the
crm-autopilot skill body. Salesforce names are the standard object and field API names;
they are reached through Headless 360's four tools (`discover`, `describe`,
`dispatch_readonly`, `dispatch`), never as tools of their own — see
`connector-call-shapes.md`.

| What the skill needs | HubSpot | Salesforce | Zoho CRM |
|---|---|---|---|
| The lead pool | Contacts filtered `lifecyclestage` = `Lead`/`MQL` | **The `Lead` object** with `IsConverted = false` — a converted lead's row persists and must be excluded | **The `Leads` module** — a separate module, not a stage on a contact |
| Lead status | `hs_lead_status` (exclude `Unqualified`) | `Status` (exclude the org's unqualified values; the picklist comes from an object-describe operation found with `discover`, described, then run with `dispatch_readonly` — `describe` itself describes operations, not objects) | `Lead_Status` (exclude `Not Qualified` / `Junk Lead`) |
| Company | An **associated company record** — a second hop | `Company`, a plain field on the lead; on a contact, `AccountId` → `Account.Name` | **`Company`, a plain field on the lead itself** — no hop |
| Where it came from | `hs_analytics_source` | `LeadSource` | `Lead_Source` |
| Last touch | `notes_last_contacted` | `LastActivityDate` — set by completed Tasks and Events, null on a record nothing was ever logged against | `Last_Activity_Time` — **populated on Deals, frequently null on Leads** (see below) |
| Created | `createdate` | `CreatedDate` | `Created_Time` |
| Deals | Deals: `dealname`, `dealstage`, `amount`, `closedate` | `Opportunity`: `Name`, `StageName`, `Amount`, `CloseDate`, `NextStep`, `IsClosed` | Deals: `Deal_Name`, `Stage`, `Amount`, `Closing_Date` |
| Deal's company | associated company | `AccountId` → `Account.Name` | `Account_Name` (a lookup — read `.name`) |
| Activity logging | note on the contact timeline | a `Task` (call, email) or `Event` (meeting) with `WhoId` = the contact and `WhatId` = the opportunity | a record in `Calls` / `Tasks`, or a Note |
| Free-text search | `search_crm_objects` | `discover` "search records", `describe` it, then `dispatch_readonly`; SOQL through the query operation, same three beats, for anything selective | `searchRecords`, or `executeCOQLQuery` for anything selective |

### The one structural difference worth knowing

**In Zoho, a lead carries its own company name.** HubSpot needs the contact's
associated company record to score company fit, and when that association is
missing the fit dimension silently scores flat. Zoho's flat
`Company` field means company fit is readable straight off the lead. Where
Zoho is the CRM of record, company fit is *more* reliable, not less.

### Two things that can be null or identical

Both make a dimension score flat if you
trust the field:

- **`Last_Activity_Time` can be null on every open lead** while being populated on
  every deal. Where that holds, the recency and engagement dimensions have
  nothing to rank on and the scores collapse — the same flat-score failure
  HubSpot hit from a different direction. Say the signals are empty rather than
  presenting the order as a ranking, and lean on the mailbox cross-check.
- **Every open lead can carry the same `Created_Time` to the second** — a bulk
  import stamp, not twelve leads that arrived at once. Lead age computed off it
  is meaningless. This is the same trap as HubSpot's `createdate` and Shopify's
  `createdAt`: **the date a record was imported is not the date the
  relationship started.** Check whether the timestamps are suspiciously
  identical before scoring anything on age.

### COQL needs a WHERE clause

`select Deal_Name, Amount from Deals limit 12` fails with
`SYNTAX_ERROR: missing clause`. Every COQL query needs a `where`, so give it a
permissive one (`where Amount > 0`, `where Lead_Status != 'Not Qualified'`)
rather than assuming the query is malformed.

### Converted leads

Zoho converts a lead into Contact + Account + Deal and the original leaves the
open pool. Pass `converted=false` (the default) when pulling a working lead
list, or a closed-won customer reappears as something to call.

### What Zoho does not replace

Zoho CRM holds contacts, leads, deals, and activity. It is **not** a substitute
for a mail connector, a calendar, or a revenue source. A skill needing email
context or open time slots still needs Gmail and Calendar regardless of which
CRM is behind it.
