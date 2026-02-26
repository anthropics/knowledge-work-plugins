---
description: Prepare and analyze a compensation offer
argument-hint: "<role, level, and candidate expectations>"
---

# Offer Prep

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Build a competitive compensation offer with market analysis, internal equity considerations, and negotiation guidance. Produces a complete offer package recommendation.

## Input

The user provides one or more of:
- Role title and level
- Candidate name and current compensation (if known)
- Candidate's expectations or competing offers
- Company compensation bands or philosophy
- Location (for geo-adjusted comp)
- Equity/stock component details
- Sign-on bonus budget

If minimal input, ask: "What role and level is the offer for? Share any comp data you have — bands, candidate expectations, or competing offers."

## Workflow

1. **Define the offer parameters** — Role, level, location, and any constraints from `$ARGUMENTS`
2. **Research market rates** — Use web search for comp benchmarks at this role/level/location (levels.fyi, Glassdoor, Blind, Pave, Radford data)
3. **Analyze the candidate's position** — Current comp, competing offers, and likely expectations
4. **Build the package** — Base salary, equity, bonus, sign-on, and benefits mapped against market data
5. **Assess internal equity** — Flag if this offer would create compression or inversion risks with existing team members
6. **Model scenarios** — Present a low/mid/high range with trade-offs for each
7. **Prepare negotiation guidance** — Anticipate likely counterpoints and prepare responses
8. **If HRIS connected** — Pull approved compensation bands, existing team comp data, and benefits details

## Output Structure

```
## Offer Analysis: [Candidate Name] → [Role Title, Level]
**Location**: [Location] | **Market**: [market characterization]

### Market Benchmarks

| Component | 25th %ile | 50th %ile | 75th %ile | 90th %ile |
|-----------|----------|----------|----------|----------|
| Base salary | $[X] | $[X] | $[X] | $[X] |
| Total cash (base + bonus) | $[X] | $[X] | $[X] | $[X] |
| Total comp (incl. equity) | $[X] | $[X] | $[X] | $[X] |

*Sources: [list data sources used]*

### Recommended Offer

| Component | Recommended | Range | Notes |
|-----------|------------|-------|-------|
| Base salary | $[X] | $[low]-$[high] | [reasoning] |
| Annual bonus | $[X] ([%]) | — | [target %] |
| Equity | [X shares/units] | — | [vesting schedule, current value] |
| Sign-on bonus | $[X] | — | [if applicable, why] |
| **Total Year 1** | **$[X]** | | |
| **Annual ongoing** | **$[X]** | | |

### Candidate Analysis
- **Current comp**: [if known]
- **Expected uplift**: [typical move premium is 10-20%]
- **Competing offers**: [if known]
- **Offer positioning**: [where this sits relative to their expectations]

### Internal Equity Check
- **Team range for this level**: [if known]
- **Compression risk**: [Yes/No — details]
- **Recommendation**: [any adjustments needed]

### Negotiation Playbook
| If they say... | Respond with... | Lever to pull |
|---------------|----------------|---------------|
| "Base is too low" | [response] | [equity, sign-on, review cycle] |
| "I have a competing offer at $X" | [response] | [total comp comparison, non-monetary value] |
| "I need more equity" | [response] | [refresher schedule, grant structure] |

### Approval Checklist
- [ ] Within approved compensation band
- [ ] Internal equity reviewed
- [ ] Hiring manager sign-off
- [ ] Total comp budget approved
- [ ] Start date confirmed
```

## With Connectors

- **If HRIS connected**: Pull compensation bands, team comp data, and benefits package details
- **If ATS connected**: Update the candidate to "offer" stage, attach the offer analysis
- **If email connected**: Draft the offer letter email
- **If knowledge base connected**: Pull the offer letter template, benefits one-pager, and equity plan details

## Tips

- Always present total compensation, not just base salary
- Include the candidate's current comp if available — it anchors the negotiation analysis
- Mention competing offers or other leverage the candidate has for realistic guidance
- For equity-heavy offers, show the value at different stock price scenarios
