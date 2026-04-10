---
name: find-similar
description: Find companies or contacts similar to a given reference. Provide a company name/domain or a person's name/email and get a ranked list of lookalikes scored by similarity. Useful for territory expansion, TAM analysis, competitive mapping, expanding buyer networks, and building targeted prospecting lists.
---

# Find Similar

Find companies or contacts similar to a reference entity using ZoomInfo's ML-powered similarity model.

## Input

The user will provide via `$ARGUMENTS`:
- **For companies**: a company name, domain, or ZoomInfo company ID
- **For contacts**: a person's name and company (e.g., "Jane Smith at Acme Corp"), email address, or ZoomInfo person ID
  - Optionally: a target company to scope results to (e.g., "at Microsoft" or "within Salesforce")
  - Optionally: how many results they want (defaults to 25, max 100)

Determine whether the user is looking for similar **companies** or **contacts** based on what they provide, then follow the appropriate workflow below.

---

## Company Workflow

1. **Lookup metadata first** — before calling any other MCP tool, use `lookup` to load reference data for any fields relevant to the request. Use the returned `id` values (not display names) in all subsequent API calls.

2. **Find similar companies** using `find_similar_companies`. This returns up to 100 results ranked by similarity score.
   - If you have a ZoomInfo company ID, pass `companyId`.
   - If you only have a company name, pass `companyName` — the API can resolve it directly.

### Company Output Format

**Similar companies to [Reference Company Name]:**

| Rank | Company | Industry | Employees | Revenue | Country | Similarity Score |
|------|---------|----------|-----------|---------|---------|-----------------|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |

Show the top 25 by default. If the user asks for more, show up to 100.

After the table:
- Note the total number of similar companies returned
- Call out any patterns (e.g., "heavily weighted toward mid-market SaaS in North America")
- Suggest next steps: use `/zoominfo:enrich-company` to get full details on any result, or `/zoominfo:find-buyers` to identify contacts at a target

---

## Contact Workflow

1. **Lookup metadata first** — before calling any other MCP tool, use `lookup` to load reference data for fields relevant to interpreting the results:
   - `lookup` with `fields: [{"fieldName": "management-levels"}, {"fieldName": "departments"}, {"fieldName": "job-functions"}]`
   - Use the returned `id` values (not display names) in all subsequent API calls and for categorizing results.

2. **Resolve the reference person** if the user did not provide a ZoomInfo person ID:
   - If the user gave an email → use `enrich_contacts` with `email` to get the person's ZoomInfo person ID.
   - If the user gave a name and company → use `enrich_contacts` with `firstName`, `lastName`, and `companyName` to get the person's ZoomInfo person ID.
   - If enrichment fails, fall back to `search_contacts` with `fullName` and `companyName` to find a match.
   - Extract the ZoomInfo person ID from the result.

3. **Resolve the target company** if the user specified one:
   - Use `search_companies` with `companyName` or `companyWebsite` to get the ZoomInfo company ID — use lookup `id` values for any filters.

4. **Find similar contacts** using `find_similar_contacts` with:
   - `referencePersonId`: the resolved ZoomInfo person ID (required)
   - `targetCompanyId`: the resolved ZoomInfo company ID (only if the user specified a target company)
   - `pageSize`: user-specified count or 25

### Contact Output Format

#### Reference Person
**[Full Name]** — [Title] at [Company]
Brief profile summary: department, management level, job function. This anchors the similarity analysis.

#### Similar Contacts

| Rank | Name | Title | Company | Department | Management Level | Score |
|------|------|-------|---------|------------|-----------------|-------|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |

Show the top 25 by default. If the user asks for more, show up to 100.

For each contact, use the `meta` field from the response to explain WHY they are a match. The meta describes the reference person used to form the similarity — use this to connect the recommendation back to the reference person's attributes.

#### Pattern Analysis
- **By Title/Function**: What roles dominate the results? (e.g., "Heavily weighted toward revenue operations and sales leadership")
- **By Seniority**: What management levels appear most? Use the lookup values to categorize accurately.
- **By Company Profile**: What types of companies do these contacts work at? (e.g., "Mostly mid-market SaaS, 200-1000 employees")
- **If scoped to a target company**: Note which departments and levels within that company have the strongest matches.

After the table:
- Note the total number of similar contacts returned
- Call out any patterns in the results
- Suggest next steps: use `/zoominfo:enrich-contact` to get full details on any result, or `/zoominfo:find-buyers` to identify other contacts at a specific company from the list
