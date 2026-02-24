# Common Room Prospector — Usage Guide

## The Two Object Types (Critical)

Never conflate these — they have different fields and filter sets.

| | `ProspectorOrganization` (Net-New) | `Organization` (Already in CR) |
|---|---|---|
| **Source** | Common Room's external data graph | CR workspace (full enrichment + signal history) |
| **Available fields** | Company name, domain, size, industry, capital raised, revenue, location | Everything — signals, scores, CRM data, RoomieAI, community activity |
| **Available filters** | Firmographic and technographic only | All firmographic plus signal-based, score-based, segment-based, and CRM filters |
| **Use for** | Territory planning, top-of-funnel list building | Prioritizing warm accounts, expansion candidates, intent signals |

## Deciding Which Object Type to Use

| User says... | Likely object type |
|-------------|-------------------|
| "Which of my accounts are showing buying signals?" | `Organization` |
| "Find fintech companies in London I haven't talked to" | `ProspectorOrganization` |
| "Find new companies matching our ICP" | `ProspectorOrganization` |
| "Show accounts that haven't engaged in 90 days" | `Organization` |
| Ambiguous — could apply to both | Ask: "Are you looking for net-new companies, or filtering accounts already in your workspace?" |

## Iterative Refinement

- Start with the user's initial criteria
- For large results (50+), return count first: "I found 500 results. Want to narrow by size or tech stack?"
- Accept follow-up refinements as filter adjustments — not a fresh search
- Suggest relaxing criteria if results are fewer than 5

## Common Pitfalls

- **Conflating object types** — Never mix ProspectorOrganization and Organization results in the same list.
- **Not scoping to "My Segments"** — When querying Organization records, scope to the user's segments by default.
- **Over-filtering** — If under 5 results, suggest relaxing one criterion.
