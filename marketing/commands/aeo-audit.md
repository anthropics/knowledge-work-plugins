---
description: Run a comprehensive AEO (Answer Engine Optimization) audit — brand visibility, citation analysis, sentiment tracking, and AI search performance across ChatGPT, Gemini, Perplexity, Google AIO, Google AI Mode, and other AI engines
argument-hint: "<brand or topic> [audit type]"
---

# /aeo-audit

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Audit your brand's visibility and performance in AI search engines. Analyze brand mentions, citation market share, sentiment, and competitive positioning across ChatGPT, Gemini, Perplexity, Google AIO, Google AI Mode, and other AI-powered search experiences. Produces actionable insights to improve your AI discoverability.

## Trigger

User runs `/aeo-audit` or asks for an AI visibility audit, AEO analysis, brand mention tracking, AI citation analysis, or AI search performance review.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Brand or domain** — your brand name or website to analyze

2. **Audit type** — one of:
   - **Full AEO audit** — comprehensive AI visibility review covering all sections below
   - **Brand visibility** — track brand mention share across AI engines
   - **Citation analysis** — identify which websites AI engines cite for your topics
   - **Sentiment analysis** — analyze positive/negative/neutral brand mentions
   - **Competitive positioning** — compare your AI presence vs competitors
   
   If not specified, default to **full AEO audit**.

3. **Topics or prompts** (optional) — specific topics, questions, or search queries to analyze

4. **AI search engines** (optional) — which AI engines to analyze (ChatGPT, Gemini, Perplexity, Google AIO, Google AI Mode). If not specified, analyze all available engines.

5. **Competitors** (optional) — competitor brands to benchmark against. If not provided and audit requires competitor data, use available data from the tools.

6. **Time period** (optional) — date range to analyze (defaults to most recent 7 days)

## Process

### 0. Authentication & Setup

**If ~~AEO tools are connected, handle any tool-specific requirements:**
- Account selection or API key verification
- Remember authentication context for all subsequent calls throughout the audit

### 1. Brand Visibility Analysis

**If ~~AEO tools are connected:**
- Pull brand mention data across AI search engines
- Calculate brand market share by mentions
- Identify which AI engines feature your brand
- Analyze by dimensions: topics, personas, intents, languages, locales

**Key metrics:**
- Brand mention count and market share percentage
- Performance breakdown by AI engine
- Topic and prompt coverage
- Persona and intent patterns (Marketing Manager, Developer; Informational, Transactional)
- Geographic and language variations
- Branded vs unbranded query performance

### 2. Citation Market Share

Analyze which websites AI engines cite when answering questions in your domain.

**If ~~AEO tools are connected:**
- Pull citation data at domain or subdomain granularity
- Calculate your website's citation market share
- Identify competitor domains being cited
- Drill down to URL level to see which prompts cite which specific URLs

**Key insights:**
- Citation count and market share
- Domain and subdomain aggregation (citation_granularity: domain or subdomain)
- URL drill-down mode to view specific cited pages for each prompt
- Prompt-to-URL mapping (which questions cite which pages)
- Citation depth per prompt (how many URLs cited)
- Competitive citation gaps

### 3. Sentiment Analysis

Analyze the sentiment of brand mentions in AI responses.

**If ~~AEO tools are connected:**
- Overall brand sentiment score (1-10 scale)
- Positive/neutral/negative mention distribution
- Sentiment by category (quality, price, features, service, etc. — categories are dynamic)
- Sentiment by source (which domains drive positive vs negative sentiment)
- Optional: Extract actual quotes/snippets from AI responses

**Advanced sentiment capabilities:**
- Discover available sentiment categories dynamically
- Source-level attribution at domain, subdomain, or URL granularity (which websites contribute to each sentiment type)
- Quote extraction showing WHY sentiment is positive/negative
- Cross-engine sentiment comparison
- Persona and intent-based sentiment patterns

### 4. Competitive Positioning

**For each competitor, analyze:**
- Brand mention gaps and opportunities
- Citation gaps (topics where they're cited but you're not)
- Sentiment comparison
- AI engine dominance patterns
- Persona and intent coverage differences

### 5. Multi-Dimensional Insights

**Break down performance across:**
- AI engines (ChatGPT, Gemini, Perplexity, Google AIO, Google AI Mode)
- Personas (Marketing Manager, Developer, Executive, SEO Specialist)
- Intents (Informational, Transactional, Navigational, Commercial)
- Languages and locales
- Branded vs unbranded queries

## Output

### Executive Summary

Open with 3-5 sentences summarizing overall AI visibility:
- Current AI presence strength (strong, moderate, weak)
- Top 3 opportunities to improve discoverability
- Most significant competitive threats
- Overall trend direction

### Brand Visibility Dashboard

| Metric | Your Brand | Top Competitor | Opportunity |
|--------|-----------|----------------|-------------|
| Brand Mentions | [count] | [count] | [gap %] |
| Market Share | [%] | [%] | [growth potential] |
| Citation Share | [%] | [%] | [gap %] |
| Sentiment Score | [1-10] | [1-10] | [difference] |

### AI Engine Breakdown

| Engine | Mentions | Citations | Market Share | Sentiment | Status |
|--------|----------|-----------|--------------|-----------|--------|
| ChatGPT | ... | ... | ... | ... | Strong/Moderate/Weak |
| Gemini | ... | ... | ... | ... | Strong/Moderate/Weak |
| Perplexity | ... | ... | ... | ... | Strong/Moderate/Weak |
| Google AIO | ... | ... | ... | ... | Strong/Moderate/Weak |
| Google AI Mode | ... | ... | ... | ... | Strong/Moderate/Weak |

### Citation Analysis

**Most-cited content:**
| URL | Citations | Prompts | Engines |
|-----|-----------|---------|---------|
| [your-url] | [count] | [examples] | [engines] |

**Citation gaps:**
- [Topic/prompt] — Competitors cited [X times], you: [Y times]

### Sentiment Analysis

**Overall:**
- Positive: [X%], Neutral: [X%], Negative: [X%]
- Sentiment Score: [1-10]

**By category** (if available):
| Category | Positive | Neutral | Negative |
|----------|----------|---------|----------|
| Quality | ... | ... | ... |
| Price | ... | ... | ... |
| Features | ... | ... | ... |

**Sentiment sources** (if available):
- [Domain] — [positive %], [negative %]

**Sample quotes** (if available):
> "Positive quote from AI response..."
> — Source: [domain] | Engine: [engine]

### Competitive Summary

| Competitor | Market Share | Sentiment | Key Strengths | Opportunities |
|------------|--------------|-----------|---------------|---------------|
| [Brand A] | [%] | [score] | [strengths] | [your advantages] |
| [Brand B] | [%] | [score] | [strengths] | [your advantages] |

### Prioritized Action Plan

**Quick Wins (this week):**
- Fix items that can immediately improve AI visibility
- Examples: Target specific prompts, create FAQ content, address negative sentiment

**Strategic Investments (this quarter):**
- Longer-term initiatives to improve AI search presence
- Examples: Content strategy for gap topics, brand positioning refinement, citation-worthy content

For each recommendation:
- What to do (specific and actionable)
- Expected impact (mention growth, citation increase, sentiment improvement)
- Effort estimate and priority

## Follow-Up

After presenting the audit, ask:

"Would you like me to:
- Deep dive into any specific AI engine's performance?
- Extract actual quotes to understand sentiment drivers?
- Drill down into specific domain citations to see cited URLs?
- Create content briefs for top opportunity prompts?
- Draft messaging to improve sentiment in specific categories?
- Analyze competitors in more detail?
- Track trends across multiple time periods?"
