---
description: Generate strategic consulting reports and recommendations. Use when producing formal client deliverables, assessment reports, strategy documents, or any comprehensive written analysis requiring professional structure and executive formatting.
argument-hint: "<report topic and key findings>"
---

# /report-generate -- Strategic Report Development

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate professional consulting reports using structured methodology and formatting standards. Creates formal deliverables that communicate complex analysis with clarity and impact.

## Invocation

```
/report-generate [report topic and key findings]
```

If no topic is provided, ask the user to describe the report purpose, audience, and key findings.

## Workflow

### Step 1: Define Report Parameters

Establish the report framework:

```
## Report Definition

### Purpose
- **Primary objective**: [What the report should achieve]
- **Audience**: [Who will read this - executives, board, team, etc.]
- **Decision to enable**: [What decision does this support?]

### Report Type
- [ ] Strategic assessment
- [ ] Due diligence report
- [ ] Implementation plan
- [ ] Performance review
- [ ] Recommendations document
- [ ] Status report
- [ ] White paper / thought leadership

### Structure Template
| Section | Purpose | Length |
|---------|---------|--------|
| Executive Summary | Bottom-line up front | 1-2 pages |
| Situation/Context | Establish common ground | 2-3 pages |
| Analysis | Evidence and findings | 8-12 pages |
| Recommendations | What to do | 3-5 pages |
| Implementation | How to do it | 4-6 pages |
| Appendices | Supporting detail | As needed |

### Tone and Style
- **Voice**: [Expert / Collaborative / Direct]
- **Technical level**: [Executive summary / Detailed / Technical]
- **Format**: [Formal report / Executive briefing / Working document]
- **Length**: [Total page target]
```

### Step 2: Structure the Narrative

Apply consulting report architecture:

```
## Report Narrative Structure

### The SCQA Framework
```
SITUATION    →  "This is where we are..."
   │                (Establish context)
   ▼
COMPLICATION →  "This is the problem..."
   │                (What's changed, what's at risk)
   ▼
QUESTION     →  "This is what we must answer..."
   │                (The central question)
   ▼
ANSWER       →  "This is what we recommend..."
                (The recommendation)
```

### Alternative: The "Answer First" Structure
```
[EXECUTIVE SUMMARY - full message here]

1. THE QUESTION
   [What we were asked to address]

2. THE ANSWER
   [Our recommendation in brief]

3. SUPPORTING EVIDENCE
   [Analysis section by section]

4. REQUIRED ACTIONS
   [What needs to happen]

5. APPENDICES
   [Supporting detail]
```

### Section Templates

#### Executive Summary Template
```
## Executive Summary

### Bottom Line
[One paragraph: the answer, the impact, the recommendation]

### Key Findings
1. [Finding 1 - quantified where possible]
2. [Finding 2 - quantified where possible]
3. [Finding 3 - quantified where possible]

### Recommendations
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

### Expected Outcomes
| Outcome | Impact | Timeline |
|---------|--------|----------|
| [Outcome 1] | $[Impact] | [Date] |
| [Outcome 2] | $[Impact] | [Date] |

### Next Steps
[Immediate actions required]
```

#### Analysis Section Template
```
## [Section Title]

### Headline
[One sentence capturing the key finding]

### Supporting Evidence
| Data Point | Source | Implication |
|------------|--------|-------------|
| [Point 1] | [Source] | [Implication] |
| [Point 2] | [Source] | [Implication] |

### Analysis
[Paragraph explaining the evidence and its meaning]

### Implications
- [Implication 1 for the business]
- [Implication 2 for the business]
```

#### Recommendation Section Template
```
## [Recommendation Title]

### The Recommendation
[Clear statement of what should be done]

### Rationale
[Why this is the right course of action]

### Supporting Evidence
| Evidence Type | Source | Key Insight |
|---------------|--------|-------------|
| [Market data] | [Source] | [Insight] |
| [Financial analysis] | [Source] | [Insight] |
| [Best practice] | [Source] | [Insight] |

### Impact
| Metric | Current | Projected | Change |
|--------|---------|-----------|--------|
| [Revenue] | $[X] | $[Y] | [Z%] |
| [Cost] | $[X] | $[Y] | [Z%] |
| [Margin] | [X%] | [Y%] | [Z pts] |

### Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [L/M/H] | [L/M/H] | [Mitigation] |
```
```

### Step 3: Develop Content

Create the report content:

```
## Content Development

### Writing Standards
| Element | Standard |
|---------|----------|
| Sentence length | Max 25 words |
| Paragraph length | Max 4 sentences |
| Headlines | Action-oriented, specific |
| Numbers | Always quantify where possible |
| Dates | Always specify, avoid "soon", "later" |
| Names | Use full names for people, full for orgs |
| Jargon | Avoid or define all technical terms |

### Evidence Standards
| Type | Requirement |
|------|-------------|
| Data | Source, date, methodology noted |
| Quotes | Named sources, verified |
| Benchmarks | Comparable sources cited |
| Expert opinions | Named experts where possible |
| Case studies | Specific examples with results |

### Visual Elements
| Element | When to Use |
|---------|-------------|
| Tables | Comparing multiple options/items |
| Charts | Showing trends, proportions, relationships |
| Diagrams | Explaining processes, structures |
| Maps | Geographic data, locations |
| Infographics | Complex data stories |
| Images | Human element, real examples |
```

### Step 4: Format and Polish

Ensure professional presentation:

```
## Formatting Standards

### Document Structure
```
[Company/Firm Logo]
[Report Title]
[Date]
[Classification: Confidential / Internal / Public]

Table of Contents

Executive Summary

1. Introduction / Context
2. Methodology (if applicable)
3. Findings / Analysis
4. Recommendations
5. Implementation Plan
6. Appendices
```

### Typography
- Headlines: Bold, 14-16pt
- Body text: Regular, 11-12pt
- Captions: Italic, 10pt
- Line spacing: 1.15-1.5

### Charts and Tables
- Always have a title
- Include source notes
- Highlight key data visually
- Use consistent color schemes
- No chartjunk - remove unnecessary elements

### Quality Checklist
- [ ] Executive summary stands alone
- [ ] Every finding has evidence
- [ ] Every recommendation has rationale
- [ ] All numbers are sourced
- [ ] All terms are defined
- [ ] Formatting is consistent
- [ ] Grammar and spelling perfect
- [ ] Page numbers present
- [ ] Table of contents accurate
- [ ] Version control noted
```

## Output Format

```
# Strategic Report: [Report Title]

## Document Control
| Field | Value |
|-------|-------|
| Version | [X.X] |
| Date | [Date] |
| Classification | [Level] |
| Author | [Name] |
| Reviewer | [Name] |

## Executive Summary
[1-2 pages, standalone summary of entire report]

## 1. Introduction
### Purpose
[Why this report was commissioned]

### Scope
[What is and isn't covered]

### Methodology
[How the analysis was conducted]

## 2. [Section Title]
### [Subsection]
[Content...]

[Repeat for all sections]

## N. Recommendations
### Priority Recommendations
[Ranked list]

### Supporting Analysis
[Key findings that support recommendations]

## N+1. Implementation
### Roadmap
[Phased approach]

### Resource Requirements
[People, budget, timeline]

### Success Metrics
[How to measure success]

## Appendices
### A: [Appendix Title]
[Detailed supporting content]

### B: [Appendix Title]
[Detailed supporting content]
```

## Notes

- Always write the executive summary last
- The executive summary should be readable in 5 minutes
- Every recommendation needs clear rationale
- Quantify everything: time, money, impact
- Use the "elevator test" - can someone understand the gist from scanning?
- Be direct - avoid hedge words like "perhaps", "might", "may"
- Use active voice: "We recommend" not "It is recommended"
- Include specific owners and dates for all actions
- Always consider what could go wrong and address it
- Professional reports are about clarity, not impressing with complexity
- Have someone else review before finalizing
- Check that the conclusion matches the evidence
- Ensure the report answers the original question
- Add ESG/sustainability considerations where relevant
- Use data visualization tools for charts
- Consider interactive/digital report formats for client portals
- Include scenario analysis for uncertainty quantification
