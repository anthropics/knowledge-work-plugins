# Dimension Research Agent Prompt

Use this template when spawning per-dimension `nimble-researcher` agents in Step 2.
Replace all `[placeholders]` with actual values before passing to the Agent tool.

Every agent prompt should start with the shared preamble below, followed by the
dimension-specific queries.

---

## Shared Preamble

Prepend this to every dimension prompt:

```
Research [Company] ([domain]) — [DIMENSION NAME] dimension.

KNOWN FACTS (skip these — already reported):
[paste known facts from memory, or "None" if first run]

RULES:
- Use the **Bash tool** to execute each nimble command.
- Do NOT use run_in_background. All Bash calls must be synchronous.
- Max 8 Bash tool calls total. Keep scope tight.
- Run searches in two groups to stay under API rate limits (10 req/sec shared across
  all agents): first group = queries 1-2 simultaneously, second group = remaining
  queries simultaneously after the first group returns.
- If < 3 total results from the first two queries, retry those without --start-date.

DATE EXTRACTION — follow the "Signal Date Validation" rules in references/nimble-playbook.md.
For each result, determine ARTICLE_DATE, EVENT_DATE, and SOURCE_TYPE using the extraction
rules and source hierarchy defined there.

Return results in this EXACT format (one per signal, no commentary):

SIGNAL: [description]
ARTICLE_DATE: [YYYY-MM-DD or ~YYYY-MM]
EVENT_DATE: [YYYY-MM-DD or ~YYYY-MM]
URL: [source url]
SOURCE_TYPE: [PRIMARY|MAJOR|DERIVATIVE]
TYPE: [type from dimension list below]
---
```

---

## Dimension-Specific Queries

Append one of these query blocks after the shared preamble.

### Funding & Financials

Types: `funding|revenue|valuation|investor|ipo`

```
SEARCHES:
1. nimble search --query "[Company] funding OR Series OR raised" --focus news --start-date "[start-date]" --max-results 10 --search-depth lite
2. nimble search --query "[Company] revenue OR valuation OR ARR" --max-results 5 --search-depth lite
3. nimble search --query "[Company] investors OR venture capital" --max-results 5 --search-depth lite
4. nimble search --query "[Company] Crunchbase OR Pitchbook funding" --max-results 3 --search-depth lite
```

### Product & Technology

Types: `product|feature|tech-stack|open-source|engineering`

```
SEARCHES:
1. nimble search --query "product OR features OR platform" --include-domain '["[domain]"]' --max-results 5 --search-depth lite
2. nimble search --query "[Company] product launch OR new feature OR release" --focus news --start-date "[start-date]" --max-results 10 --search-depth lite
3. nimble search --query "[Company] tech stack OR engineering OR architecture" --max-results 5 --search-depth lite
4. nimble search --query "[Company] open source OR GitHub" --max-results 3 --search-depth lite
5. nimble search --query "blog engineering OR tech" --include-domain '["[domain]"]' --max-results 3 --search-depth lite
```

### Leadership & Team

Types: `leadership|hire|departure|culture|team-size|executive-quote`

```
SEARCHES:
1. nimble search --query "[Company] CEO OR founder OR leadership" --max-results 5 --search-depth lite
2. nimble search --query "[Company] hired OR appointment OR CTO OR VP" --focus news --start-date "[start-date]" --max-results 10 --search-depth lite
3. nimble search --query "[Company] employees OR team size OR culture OR glassdoor" --max-results 5 --search-depth lite
4. nimble search --query "[Company] CEO OR founder interview OR podcast OR keynote" --max-results 5 --search-depth lite
5. nimble search --query "[Company]" --include-domain '["linkedin.com"]' --max-results 5 --search-depth lite
```

### Recent News & Events

Types: `news|partnership|acquisition|award|event|social`

```
SEARCHES:
1. nimble search --query "[Company] news" --focus news --start-date "[start-date]" --max-results 10 --search-depth lite
2. nimble search --query "[Company] partnership OR acquisition OR expansion" --focus news --start-date "[start-date]" --max-results 5 --search-depth lite
3. nimble search --query "[Company] conference OR award OR recognition" --start-date "[start-date]" --max-results 5 --search-depth lite
4. nimble search --query "[Company]" --include-domain '["x.com"]' --max-results 5 --search-depth lite --time-range week
5. nimble search --query "[Company] announcement OR press release" --focus news --start-date "[start-date]" --max-results 5 --search-depth lite
```

### Market Position

Types: `competitor|market-share|review|analyst|customer`

```
SEARCHES:
1. nimble search --query "[Company] competitors OR alternatives OR vs" --max-results 10 --search-depth lite
2. nimble search --query "[Company] market share OR market position OR industry leader" --max-results 5 --search-depth lite
3. nimble search --query "[Company] reviews" --include-domain '["g2.com", "capterra.com", "trustradius.com"]' --max-results 5 --search-depth lite
4. nimble search --query "[Company] analyst report OR Gartner OR Forrester" --max-results 5 --search-depth lite
5. nimble search --query "[Company] customers OR case study OR testimonial" --max-results 5 --search-depth lite
```
