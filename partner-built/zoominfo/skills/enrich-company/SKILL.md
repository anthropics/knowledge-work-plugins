---
name: enrich-company
description: Look up a company's full profile. Provide a company name, domain, ticker symbol, or ZoomInfo company ID. Returns firmographics, financials, corporate structure, growth signals, and contact counts.
---

# Enrich Company

Look up a single company's full profile in ZoomInfo.

## Input

The user will provide via `$ARGUMENTS` one of:
- A domain or website (e.g., `stripe.com` or `https://stripe.com`)
- A company name (e.g., `Stripe`)
- A stock ticker (e.g., `SNOW`)
- A ZoomInfo company ID

## Workflow

1. **Lookup metadata first** — before calling any other MCP tool, use `lookup` to load reference data for any fields relevant to the request. Use the returned `id` values (not display names) in all subsequent API calls. This ensures accurate parameter resolution, especially if a fallback search is needed.

2. **Identify the best match key** from the user's input:
   - URL or domain → use `domain` or `companyWebsite` parameter
   - Company name → use `companyName`
   - Ticker → use `companyTicker`
   - Company ID → use `companyId`

3. **Enrich the company** using `enrich_companies` with the identified parameters.

4. **If no match**, try a fallback:
   - Use `search_companies` with `companyName` for fuzzy matching — use lookup `id` values for any filters
   - Suggest alternatives from the search results

## Output Format

**[Company Name]** — [One-line description]

| Field | Value |
|-------|-------|
| Website | |
| Industry | |
| Sub-Industries | |
| Employee Count | |
| Revenue | |
| Founded | |
| HQ Location | |
| Company Type | (Public/Private/etc.) |
| Ticker | |
| Business Model | (B2B/B2C/B2G) |
| Phone | |
| SIC Codes | |
| NAICS Codes | |
| ZoomInfo Company ID | |

**Corporate Structure**
- Ultimate Parent: [if applicable]
- Parent: [if applicable]
- Subsidiaries: [count if available]

**Growth Signals**
- 1-Year Employee Growth: X%
- 2-Year Employee Growth: X%
- Recent Funding: [if available]

**ZoomInfo Coverage**
- Contacts in Database: [count]

Include the ZoomInfo Company ID — users will need it for follow-up commands like `/zoominfo:find-buyers` or `/zoominfo:find-similar`.
