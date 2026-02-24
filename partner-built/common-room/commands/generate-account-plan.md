---
description: Generate a comprehensive strategic account plan
argument-hint: <company name or domain>
---

Generate a comprehensive account plan for "$ARGUMENTS".

## Process

1. **Full account research** — Follow the account-research skill to produce a complete account overview. Pull all available first-party (product), second-party (community), and third-party (intent) signals, CRM data, scores, and RoomieAI research.

2. **Stakeholder mapping** — Fetch the top 5 contacts at this company sorted by member score descending. Classify each into: Champion, Economic Buyer, Influencer, End User, or Unknown. Use Spark persona data if available; if Spark is unavailable, infer from engagement patterns and activity recency. If no activity data exists either, classify as Unknown.

3. **Engagement analysis** — Pull all organization activity for the last 90 days (up to 50 activities). Identify trends: is engagement growing, stable, or declining? Which contacts are most active? What channels are they engaging through?

4. **Web search (supplementary)** — If CR data is rich, skip. If data is thin or the user requests it, search for recent company news (last 30 days): funding, acquisitions, product launches, leadership changes, competitive moves.

5. **Synthesis** — Combine all data into a structured account plan. When the user's company context is available (see `references/my-company-context.md`), tailor the executive summary, opportunities, and action items to the user's product and ICP.

## Output Format

```
## Account Plan: [Company Name]

### Executive Summary
[3-4 sentences: relationship status, key opportunity, primary risk, recommended priority]

### Account Overview
| Field | Value |
|-------|-------|
| Industry | ... |
| Size | ... |
| Domain | ... |
| CRM Owner | ... |
| Opp Stage | ... |
| ARR | ... |
| Scores | ... |

### Stakeholder Map

**Champions**
- [Name] — [Title] — [Key signals, last activity date]

**Economic Buyers**
- [Name] — [Title] — [Key signals]

**Influencers**
- [Name] — [Title] — [Key signals]

**End Users**
- [Name] — [Title] — [Key signals]

### Engagement Analysis
[Trend summary: growing/stable/declining, most active contacts, top channels, comparison to 90 days prior if data available]

### Recent News [If web search was run]
[Web search findings with sources and dates]

### Opportunities
1. [Signal-backed opportunity with specific next step]
2. ...

### Risks
1. [Signal-backed risk with mitigation]
2. ...

### Prioritized Action Items
1. [Specific action] — [Owner suggestion] — [Timeline]
2. ...
3. ...
```

Ground every insight in actual data. Flag explicitly when data is thin or unavailable.

**If Common Room returns sparse data for this account**, produce an abbreviated plan that covers only the sections with real data. Do not generate a full account plan from minimal input — a short honest plan with gaps clearly noted is far more useful than a comprehensive-looking plan built on fabricated details. Omit sections (Stakeholder Map, Engagement Analysis, Opportunities, Risks) entirely if there is no data to support them.
