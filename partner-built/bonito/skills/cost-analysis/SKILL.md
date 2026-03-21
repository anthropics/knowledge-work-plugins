---
name: cost-analysis
description: "Analyze AI spending across providers, identify expensive models, recommend cheaper alternatives, and optimize routing for cost savings. Triggers on 'what am I spending', 'cost breakdown', 'optimize my AI costs', 'which models cost the most', or 'reduce my AI costs'."
---

# Cost Analysis

Understand and optimize AI spending across all connected providers. Pull usage data, break down costs, identify expensive patterns, and recommend concrete savings.

## Step 1: Determine Scope

- "What am I spending?" -> full overview, current month
- "Costs by provider" -> provider breakdown
- "Most expensive models" -> model ranking
- "Compare months" -> trend analysis
- "Optimize costs" -> recommendations focus
- "Last 7 days" -> custom date range

## Step 2: Pull Usage Data

Query ~~bonito for:
1. Total requests, tokens, and costs for the period
2. Breakdown by provider
3. Breakdown by model
4. Breakdown by agent
5. Daily time series for trends

## Step 3: Analyze Patterns

- Which models account for the most spending?
- Are agents using expensive models for simple tasks?
- Is usage concentrated or spread across providers?
- Are there traffic spikes or retry storms?
- Is token usage efficient (prompt length vs response length)?

## Step 4: Generate Recommendations

**Model substitution:**
- Opus for simple tasks -> suggest Haiku or Sonnet
- GPT-4o for classification -> suggest GPT-4o-mini
- High-volume agent -> suggest Groq for speed + cost

**Routing optimization:**
- One provider consistently more expensive -> route to cheaper alternative
- Bursty traffic -> suggest response caching
- Quality varies -> A/B test cheaper models

## Step 5: Present Report

```
## AI Cost Analysis

Period: [Start] to [End]
Total Spend: $[Amount] | Requests: [Count] | Tokens: [Count]

### By Provider
| Provider | Requests | Cost | % of Total |
|----------|----------|------|------------|
| AWS Bedrock | [Count] | $[Amount] | [X]% |
| OpenAI | [Count] | $[Amount] | [X]% |

### By Model (Top 5)
| Model | Provider | Requests | Cost | $/1K Req |
|-------|----------|----------|------|----------|
| claude-sonnet | Bedrock | [Count] | $[Amount] | $[Amount] |

### Recommendations
1. [Action]: Switch [agent] from [expensive model] to [cheaper model]
   Estimated savings: $[Amount]/month ([X]%)

2. [Action]: [Description]
   Estimated savings: $[Amount]/month ([X]%)

Potential monthly savings: $[Amount] ([X]% reduction)
```
