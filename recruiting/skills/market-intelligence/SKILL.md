---
name: market-intelligence
description: "Research talent market conditions, compensation benchmarks, competitor hiring activity, and talent availability for recruiting decisions. Trigger with \"what's the market like for\", \"comp benchmarks\", \"salary range for\", \"who's hiring for\", \"talent supply\", \"competitor hiring\", or when the user asks about compensation, market rates, talent scarcity, or competitive landscape for a role."
---

# Market Intelligence

Talent market research for informed recruiting decisions. Provides compensation benchmarks, talent supply analysis, competitor tracking, and market condition insights.

## How It Works

- **Standalone**: Uses web search to pull compensation data, competitor job postings, market trends, and talent supply signals. Great for quick market checks.
- **With connectors**: Enriches with data from compensation platforms, CRM contact databases, and ATS historical data on offer acceptance rates.

## Research Dimensions

### 1. Compensation Benchmarks

Sources to triangulate (via web search):
- levels.fyi (tech roles, equity-heavy)
- Glassdoor (broad coverage, self-reported)
- LinkedIn Salary Insights
- Blind (anonymous, skews tech)
- Pave, Radford, Mercer (if user has access)
- H1B salary data (public, employer-specific)
- Recent job postings with published ranges (Colorado, NYC, CA transparency laws)

When presenting comp data:
- Always show base, bonus, equity, and total compensation separately
- Adjust for geography — specify the adjustment methodology
- Show percentile ranges (25th, 50th, 75th, 90th), not just averages
- Note the data freshness and source quality
- Flag if the market is moving fast (hot roles where data lags reality)

### 2. Talent Supply Analysis

Assess availability by examining:
- Number of professionals with this title on LinkedIn
- Job posting volume vs. candidate volume
- Time-to-fill benchmarks for this role type
- Remote vs. in-office supply differences
- Adjacent talent pools (who could do this job with some ramp)

Supply ratings:
| Rating | Signal | Implication |
|--------|--------|------------|
| **Abundant** | Many qualified candidates, low competition | Standard sourcing, competitive offers |
| **Balanced** | Moderate supply, moderate competition | Active sourcing needed, market-rate comp |
| **Scarce** | Few candidates, high competition | Aggressive sourcing, above-market comp, creative approaches |
| **Critical shortage** | Near-zero available talent | Consider adjacent profiles, upskilling, contract-to-hire, acqui-hire |

### 3. Competitor Intelligence

Track what competitors are doing:
- Open roles (what they're hiring for and at what levels)
- Compensation signals (posted ranges, Glassdoor data, Blind reports)
- Employer brand moves (blog posts, conference talks, social media)
- Layoffs or freezes (talent becoming available)
- Office/remote policies (potential lever if competitors are mandating RTO)

### 4. Market Trends

- Role evolution (how this role is changing, new skills emerging)
- Emerging titles and functions
- Hot skills commanding premiums
- Industry shifts affecting talent flow
- Geographic talent migration patterns

## Output Format

When researching market conditions, produce:

1. **Market summary** — overall characterization of the market for this role
2. **Compensation benchmarks** — table with percentiles, adjusted for location
3. **Talent supply assessment** — availability rating with evidence
4. **Competitive landscape** — what competitors are doing in this space
5. **Recommendations** — how to position the role given market conditions

## Connectors

| Connector | Enhancement |
|-----------|------------|
| Data enrichment | Company employee counts, growth rates, funding data |
| ATS | Historical offer data, acceptance rates, time-to-fill by role |
| HRIS | Internal compensation data for equity analysis |
| Knowledge base | Past market research, compensation philosophy docs |
