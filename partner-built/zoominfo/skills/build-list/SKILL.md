---
name: build-list
description: Build a list of contacts or companies matching specific criteria. Describe what you're looking for in natural language and get a structured, tabular list you can export. Supports filtering by title, seniority, department, industry, company size, location, tech stack, growth rate, and more. Outputs a clean table artifact.
---

# Build List

Build a targeted list of contacts or companies from ZoomInfo and output as a structured table.

## Input

The user will describe what they want via `$ARGUMENTS`. Examples:
- "CTOs at Series B+ startups in SF with 50-200 employees"
- "VP of Sales at healthcare companies using Salesforce with 500+ employees"
- "All SaaS companies in EMEA with $10M-$50M revenue"
- "Directors of Engineering at companies similar to Datadog"
- "Marketing leaders at Fortune 500 companies in financial services"

The user may also specify:
- How many results they want (default: 25)
- Whether they want contacts, companies, or both
- Specific fields to include in the output

## Workflow

1. **Determine list type**: Is the user asking for contacts, companies, or both? Default to contacts if they mention titles/roles, companies if they mention firmographics only.

2. **Parse criteria** from natural language into structured filters:
   - Job titles, management levels, departments, job functions → contact filters
   - Industry, employee count, revenue, geography, tech stack, company type → company filters
   - Growth rate, funding, rankings → company filters

3. **Resolve all filter values** using `lookup` before searching. This is critical — do NOT guess values. For every filter you plan to use, call `lookup` with the corresponding field name to get the valid values and use the returned `id` values in your search parameters.

4. **Execute the search**:
   - For **contacts**: Use `search_contacts` with all resolved filters. Sort by `-contactAccuracyScore`. Request up to 100 results.
   - For **companies**: Use `search_companies` with all resolved filters. Sort by `-employeeCount` or `-revenue`. Request up to 100 results.
   - For **both**: Search companies first, then search contacts at the top results.

5. **Enrich top results** if the search returns limited detail:
   - Use `enrich_contacts` (batch of 10) or `enrich_companies` (batch of 10) on the top results to fill in emails, phones, and other details.

6. **Output as a clean table artifact.** Create a markdown or CSV artifact the user can copy or export.

## Output Format

### Search Criteria Applied

Show the user exactly what filters were used so they can verify:

| Filter | Value |
|--------|-------|
| Management Level | Vice President |
| Industry | Computer Software |
| Employee Count | 51-100, 101-250 |
| Metro Region | San Francisco-Oakland-Hayward, CA |
| ... | ... |

### Contact List (if contact search)

| # | Name | Title | Company | Email | Direct Phone | Accuracy | Location |
|---|------|-------|---------|-------|-------------|----------|----------|
| 1 | | | | | | | |
| 2 | | | | | | | |

### Company List (if company search)

| # | Company | Industry | Employees | Revenue | HQ Location | Website | ZoomInfo ID |
|---|---------|----------|-----------|---------|-------------|---------|-------------|
| 1 | | | | | | | |
| 2 | | | | | | | |

### List Summary
- **Total results found**: X (showing top Y)
- **Filters applied**: [summary]
- **Average accuracy score**: X (contacts only)
- **Data quality**: Flag any concerns (low accuracy, stale records)

### Refinement Options
If the list is too broad or too narrow, suggest specific filter adjustments:
- "Add `revenue` filter to narrow from 847 to ~200 results"
- "Remove metro region filter to expand from 12 to ~150 results"
- "Try adjacent industries: Information Technology Services, Internet"

If the user wants to iterate, they can re-run with adjusted criteria. Suggest the exact modified command.
