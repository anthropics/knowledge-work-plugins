---
description: Analyze RFP requirements, evaluation criteria, win themes, and response strategy
argument-hint: "<RFP document or summary>"
---

# /rfp-analyze -- RFP Analysis and Response Strategy

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Analyze a Request for Proposal to understand requirements, evaluation criteria, and develop a winning response strategy. Identifies win themes, competitive positioning, and key pursuits.

## Invocation

```
/rfp-analyze [RFP document or URL]
```

If no document is provided, ask the user to provide the RFP content (paste, upload, or link).

## Workflow

### Step 1: Parse RFP Structure

Accept and parse the RFP document. Identify:

- **Client organization** and background
- **Problem statement** — what challenge are they trying to solve?
- **Scope of work** — what are they asking for?
- **Deliverables** — what will be required?
- **Timeline** — key dates and deadlines
- **Budget** — if disclosed
- **Evaluation criteria** — how will responses be scored?
- **Submission requirements** — format, length, required sections

### Step 2: Analyze Evaluation Criteria

Break down the evaluation framework:

```
## RFP Evaluation Criteria Analysis

| Criterion | Weight | Interpretation | Our Strength |
|-----------|--------|----------------|---------------|
| [Criterion 1] | X% | [What they really want] | [High/Med/Low] |
| [Criterion 2] | X% | [What they really want] | [High/Med/Low] |
| ... | ... | ... | ... |
```

**Key questions:**
- What matters most? (highest weight)
- What is differentiated vs. table stakes?
- What are they explicitly vs. implicitly evaluating?

### Step 3: Identify Win Themes

Develop 3-5 compelling win themes that are laser-locked to what the client explicitly stated they're evaluating. Each theme should focus on the "why" rather than just the "what":

```
## Win Themes

### Theme 1: [Differentiator]
- **Why it wins**: [Client pain point] is their #1 priority — address this directly
- **Evidence**: [Quantifiable case study or statistic with measurable outcomes]
- **Alignment**: [Explicitly maps to evaluation criterion X]

### Theme 2: [Methodology]
- **Why it wins**: They need [specific approach] to solve [their problem]
- **Evidence**: [Methodology track record with specific results]
- **Alignment**: [Maps to evaluation criterion Y]

### Theme 3: [Team]
- **Why it wins**: They value [team characteristics] for [specific reason]
- **Evidence**: [Relevant experience with measurable impact]
- **Alignment**: [Maps to evaluation criterion Z]
```

### Step 4: Assess Competitive Position

Analyze the competitive landscape:

- **Known competitors**: Who is likely bidding?
- **Our advantages**: Where do we win against each?
- **Our vulnerabilities**: Where do we need to mitigate?
- **Gaps**: What do we need to address in our response?

### Step 5: Develop Response Strategy

Create a response strategy document following the strength-based approach: compliance + responsiveness + persuasion + credibility.

```
## Response Strategy

### Foundation: Compliance and Responsiveness
- **Must-pass requirements**: [Non-negotiable criteria that must be addressed]
- **Scored requirements**: [Weighted criteria we must address well]

### Strength-Based Strategy (Tier 1 - Primary Win Themes)
- [Win theme 1] → directly addresses highest-weighted criterion
- [Win theme 2] → addresses second-highest criterion
- [Win theme 3] → differentiator that sets us apart

### Persuasion Elements (Tier 2 - Supporting Evidence)
- [Relevant case study with quantifiable results]
- [Methodology credentials]

### Credibility Markers (Tier 3 - Trust Building)
- [Relevant certifications]
- [Team credentials]

### Response Approach
- **Structure**: Lead with their priorities, not your history — open with solution, not capabilities
- **Length**: [Page/section limits]
- **Tone**: Client-focused, outcome-oriented, specific
- **Visuals**: Use data visualization to demonstrate impact, not decorative graphics

### Timeline
- [Milestone 1]: [Date]
- [Milestone 2]: [Date]
- Submission deadline: [Date]

### Resource Requirements
- [Role 1]: [Effort estimate]
- [Role 2]: [Effort estimate]
```

## Output Format

```
# RFP Analysis: [Client Name] - [Project Name]

## Executive Summary
[2-3 sentence overview of what they want and how we should respond]

## Opportunity Assessment
- **Fit score**: [High / Medium / Low]
- **Estimated value**: [Range if available]
- **Win probability**: [Initial assessment with rationale]
- **Resource requirement**: [High / Medium / Low]

## Client Context
### Problem Statement
[What challenge they're solving]

### Key Stakeholders
[Who is involved in decision]

### Constraints & Considerations
[Any budget, timeline, or scope constraints]

## Evaluation Breakdown
[Criteria analysis table]

## Win Themes
[2-4 differentiated themes]

## Competitive Landscape
[Known competitors and positioning]

## Response Strategy
[Recommended approach]

## Recommended Next Steps
1. [Immediate action]
2. [Short-term action]
3. [Go/No-Go decision point]
```

## Notes

- Always note if evaluation criteria weightings are explicit or inferred
- If budget is not disclosed, flag this as a risk factor
- For complex RFPs, recommend breaking response development into sections with review gates
- If multiple stakeholders are involved, note different evaluation perspectives (technical vs. commercial)
- Flag any unusual or restrictive requirements that may indicate a preferred vendor
