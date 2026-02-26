---
description: Synthesize interview feedback into a hiring recommendation
argument-hint: "<candidate name or interview notes>"
---

# Interview Debrief

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Synthesize feedback from multiple interviewers into a structured hiring recommendation. Surfaces consensus, disagreements, and evidence gaps to drive a productive debrief conversation.

## Input

The user provides one or more of:
- Individual interviewer scorecards or notes (pasted, uploaded, or described)
- Candidate name and role
- Interview panel composition
- Any known concerns or highlights from the hiring manager

If no feedback is provided, ask: "Share the interview feedback — paste scorecards, notes from each interviewer, or describe the signals from the panel."

## Workflow

1. **Collect feedback** — Parse all interviewer input, attributing each signal to its source
2. **Map to competencies** — Organize feedback by the competencies being evaluated, not by interviewer
3. **Identify consensus** — Flag areas where all interviewers agree (both positive and negative)
4. **Surface disagreements** — Highlight competencies where interviewers diverge, with each side's evidence
5. **Find evidence gaps** — Note competencies that were insufficiently tested or have conflicting signals
6. **Assess against the bar** — Compare the composite signal against the role's hiring bar
7. **Generate recommendation** — Produce a clear recommendation with confidence level
8. **Prepare debrief agenda** — Structure the debrief discussion to focus on disagreements and gaps first

## Output Structure

```
## Debrief Summary: [Candidate Name] → [Role Title]

### Panel
| Interviewer | Stage | Overall rating |
|-------------|-------|---------------|
| [Name] | [Stage] | [Rating] |
| ... | ... | ... |

### Competency Heatmap

| Competency | [Interviewer 1] | [Interviewer 2] | [Interviewer 3] | Consensus |
|------------|----------------|----------------|----------------|-----------|
| [Comp 1] | ✅ Strong | ✅ Positive | ⚠️ Mixed | Positive |
| [Comp 2] | ❌ Concern | ⚠️ Mixed | ❌ Concern | Concern |
| ... | ... | ... | ... | ... |

### Areas of Consensus
**Strengths**: [What everyone agrees is strong, with evidence]
**Concerns**: [What everyone agrees is a gap, with evidence]

### Areas of Disagreement
**[Competency]**: [Interviewer A] saw [X signal] while [Interviewer B] saw [Y signal]. This likely reflects [possible explanation]. **Discuss in debrief.**

### Evidence Gaps
- [Competency not adequately tested — suggest follow-up]

### Recommendation: [Strong Hire / Hire / No Hire / Strong No Hire]
**Confidence**: [High / Medium / Low]
**Reasoning**: [2-3 sentences synthesizing the overall signal]

### Debrief Discussion Guide
1. **Start with**: [Key disagreement to resolve]
2. **Then discuss**: [Evidence gap to address]
3. **Decision point**: [What would move this from X to Y?]
```

## With Connectors

- **If ATS connected**: Pull submitted scorecards directly, update candidate disposition after the debrief
- **If chat connected**: Post the debrief summary to the hiring channel, notify the hiring manager
- **If calendar connected**: Check the scheduled debrief time and attendees

## Tips

- Best results when you have written feedback from every interviewer in the loop
- Include the role's leveling expectations if the decision hinges on "is this a senior or staff?"
- Flag if any interviewer has a known bias toward certain backgrounds or styles
