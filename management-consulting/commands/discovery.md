---
description: Conduct discovery phase with stakeholder interviews, data gathering, and current state assessment
argument-hint: "<project name> <focus area>"
---

# /discovery -- Discovery and Current State Assessment

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Execute a comprehensive discovery phase to understand the current state, gather requirements, and build the foundation for analysis and recommendations.

## Invocation

```
/discovery [project name] [focus area]
```

If parameters are not provided, ask for:
- Project/engagement name
- Discovery focus areas (operations, organization, technology, etc.)
- Stakeholder list
- Available data sources

## Workflow

### Step 1: Plan Discovery Activities

Design the discovery approach:

```
## Discovery Plan

### Objectives
1. [Objective 1: understand current state]
2. [Objective 2: identify pain points]
3. [Objective 3: gather requirements]
4. [Objective 4: build stakeholder alignment]

### Methods

| Method | Purpose | Participants | Timing |
|--------|---------|--------------|--------|
| Executive interviews | Strategic context | C-suite | Week 1 |
| Working sessions | Detailed requirements | Middle management | Week 1-2 |
| Data review | Quantitative baseline | N/A | Week 1-2 |
| Process observation | Workflow understanding | Operations | Week 2 |
| Survey | Broad feedback | Organization | Week 2 |

### Data Sources

| Source | What we'll gather | Owner |
|--------|-------------------|-------|
| [Source 1] | [Data type] | [Contact] |
| [Source 2] | [Data type] | [Contact] |
```

### Step 2: Design Interview Guides

Create structured interview guides:

#### Executive Interview Guide

```
## Executive Interview Guide

### Introduction (5 min)
- Thank participant
- Explain purpose and process
- Confirm confidentiality

### Strategic Context (15 min)
1. What is your vision for [area] over the next [X] years?
2. What are the biggest challenges preventing you from achieving this?
3. How does [project] fit into your strategic priorities?
4. What does success look like for this initiative?

### Current State (15 min)
5. How would you describe the current state of [area]?
6. What processes or capabilities work well?
7. What are the most significant pain points?
8. What has been tried before? What worked/didn't?

### Stakeholder & Organization (10 min)
9. Who are the key stakeholders for this initiative?
10. What organizational changes might be needed?
11. What concerns or resistance might we encounter?

### Closing (5 min)
12. What questions should we be asking that we haven't?
13. Is there anyone else we should speak with?
14. Any documents or data you'd recommend we review?
```

#### Process Interview Guide

```
## Process Interview Guide

### Process Overview
1. Walk me through how [process] works today
2. What are the key steps and hand-offs?
3. Who is involved at each stage?

### Pain Points
4. Where does the most time get spent?
5. Where do errors or rework happen most often?
6. What constraints or bottlenecks exist?

### Requirements
7. What would the "ideal" process look like?
8. What capabilities are must-haves vs. nice-to-haves?
9. What systems or tools are critical?

### Volume & Metrics
10. How many [transactions/cases] per period?
11. What are current cycle times?
12. What metrics are tracked today?
```

### Step 3: Execute Data Gathering

Structure data collection:

```
## Data Request List

### Financial Data
- [Data type 1]
- [Data type 2]

### Operational Data
- [Data type 1]
- [Data type 2]

### Organizational Data
- [Data type 1]
- [Data type 2]

### External Data
- [Data type 1]
- [Data type 2]

### Data Templates
If needed, create templates for:
- Financial summary
- Process inventory
- Organizational chart
- Technology inventory
```

### Step 4: Synthesize Findings

Create discovery output:

```
# Discovery Summary: [Project Name]

## Executive Summary
[2-3 paragraphs on what we learned and the implications]

## Current State Assessment

### Strengths
- [What works well 1]
- [What works well 2]

### Pain Points
- [Pain point 1: impact and root cause]
- [Pain point 2: impact and root cause]

### Opportunities
- [Opportunity 1]
- [Opportunity 2]

## Stakeholder Perspectives

| Stakeholder Group | Priorities | Concerns | Influence |
|-------------------|-----------|----------|-----------|
| [Group 1] | [Priorities] | [Concerns] | [High/Med/Low] |
| [Group 2] | [Priorities] | [Concerns] | [High/Med/Low] |

## Key Findings

### Finding 1: [Title]
**Evidence**: [Interview quote / data point]
**Implication**: [What this means for the project]

### Finding 2: [Title]
[...]

## Data Analysis

### Quantitative Highlights
| Metric | Current State | Industry Benchmark | Gap |
|--------|---------------|-------------------|-----|
| [Metric 1] | [Value] | [Benchmark] | [Gap] |
| [Metric 2] | [Value] | [Benchmark] | [Gap] |

## Initial Hypotheses

Based on discovery, we hypothesize:
1. [Hypothesis 1]
2. [Hypothesis 2]
3. [Hypothesis 3]

## Risks & Issues Identified
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] |

## Recommendations for Next Phase
[What we should focus on in analysis and recommendations]
```

## Output Format

Generate:

1. **Discovery Plan** — Activities, timeline, participants
2. **Interview Guides** — Structured questions for each stakeholder level
3. **Data Request** — List of needed data with owners
4. **Discovery Summary** — Synthesized findings and implications

After generating, ask:

> "Would you like me to:
> - Create specific interview guides for different stakeholder levels?
> - Develop a data collection template?
> - Build a stakeholder mapping matrix?
> - Synthesize specific interview findings into themes?"

## Notes

- Discovery is about UNDERSTANDING, not jumping to solutions
- Interview more people than you think you need to — breadth matters
- Cross-validate findings — don't take one person's word
- Look for patterns across stakeholders — triangulate perspectives
- Follow the "ask one thoughtful question, listen deeply, then follow-up" approach — avoid rapid-fire questioning
- Share interview plan with client's main contact in advance for better preparation
- Focus on root causes, not just symptoms — ask "why" multiple times
- Document assumptions explicitly and update throughout
- Flag gaps early — don't wait until analysis phase to identify missing information
- Keep discovery outputs living — they'll evolve as you learn more
