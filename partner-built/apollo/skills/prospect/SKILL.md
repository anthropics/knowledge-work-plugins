---
name: prospect
description: "Full ICP-to-leads pipeline. Describe your ideal customer in plain English and get a ranked table of enriched decision-maker leads with emails and phone numbers."
user-invocable: true
argument-hint: "[describe your ideal customer]"
---

# Prospect

Go from an ICP description to a ranked, enriched lead list in one shot. The user describes their ideal customer via "$ARGUMENTS".

## Examples

- `/apollo:prospect VP of Engineering at Series B+ SaaS companies in the US, 200-1000 employees`
- `/apollo:prospect heads of marketing at e-commerce companies in Europe`
- `/apollo:prospect CTOs at fintech startups, 50-500 employees, New York`
- `/apollo:prospect procurement managers at manufacturing companies with 1000+ employees`
- `/apollo:prospect SDR leaders at companies using Salesforce and Outreach`

## Step 1 — Parse the ICP

Extract structured filters from the natural language description in "$ARGUMENTS":

**Company filters:**
- Industry/vertical keywords → `q_organization_keyword_tags`
- Employee count ranges → `organization_num_employees_ranges`
- Company locations → `organization_locations`
- Specific domains → `q_organization_domains_list`

**Person filters:**
- Job titles → `person_titles`
- Seniority levels → `person_seniorities`
- Person locations → `person_locations`

If the ICP is vague, ask 1-2 clarifying questions before proceeding. At minimum, you need a title/role and an industry or company size.

## Step 2 — Search for Companies

Use `mcp__claude_ai_Apollo_MCP__apollo_mixed_companies_search` with the company filters:
- `q_organization_keyword_tags` for industry/vertical
- `organization_num_employees_ranges` for size
- `organization_locations` for geography
- Set `per_page` to 25

## Step 3 — Enrich Top Companies

Use `mcp__claude_ai_Apollo_MCP__apollo_organizations_bulk_enrich` with the domains from the top 10 results. This reveals revenue, funding, headcount, and firmographic data to help rank companies.

## Step 4 — Find Decision Makers

Use `mcp__claude_ai_Apollo_MCP__apollo_mixed_people_api_search` with:
- `person_titles` and `person_seniorities` from the ICP
- `q_organization_domains_list` scoped to the enriched company domains
- `per_page` set to 25

## Step 5 — Enrich Top Leads

> **Credit warning**: Tell the user exactly how many credits will be consumed before proceeding.

Use `mcp__claude_ai_Apollo_MCP__apollo_people_bulk_match` to enrich up to 10 leads per call with:
- `first_name`, `last_name`, `domain` for each person
- `reveal_personal_emails` set to `true`

If more than 10 leads, batch into multiple calls.

## Step 6 — Present the Lead Table

Show results in a ranked table:

### Leads matching: [ICP Summary]

| # | Name | Title | Company | Employees | Revenue | Email | Phone | ICP Fit |
|---|---|---|---|---|---|---|---|---|

**ICP Fit** scoring:
- **Strong** — title, seniority, company size, and industry all match
- **Good** — 3 of 4 criteria match
- **Partial** — 2 of 4 criteria match

**Summary**: Found X leads across Y companies. Z credits consumed.

## Step 7 — Offer Next Actions

Ask the user:

1. **Save all to Apollo** — Bulk-create contacts via `mcp__claude_ai_Apollo_MCP__apollo_contacts_create` with `run_dedupe: true` for each lead
2. **Load into a sequence** — Ask which sequence and run the sequence-load flow for these contacts
3. **Deep-dive a company** — Run `/apollo:company-intel` on any company from the list
4. **Refine the search** — Adjust filters and re-run
5. **Export** — Format leads as a CSV-style table for easy copy-paste
