---
description: Screen a candidate against job requirements
argument-hint: "<resume or candidate info>"
---

# Screen Candidate

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Evaluate a candidate's fit against specific role requirements. Produces a structured assessment with clear signal on whether to advance, with reasoning for every dimension.

## Input

The user provides one or more of:
- Resume (pasted text, uploaded file, or link)
- LinkedIn profile summary
- Candidate notes from a recruiter screen
- Job description or role requirements to screen against

If no job requirements are provided, ask: "What role are you screening for? Paste the JD or describe the key requirements."

If no candidate info is provided, ask: "Share the candidate's resume, LinkedIn summary, or any background info you have."

## Workflow

1. **Extract requirements** — Parse the job description into must-have qualifications, nice-to-haves, and disqualifiers
2. **Parse candidate profile** — Extract work history, skills, education, achievements, and career trajectory from the provided materials
3. **Assess fit by dimension** — Score each requirement dimension: technical skills, domain experience, seniority level, culture indicators, career trajectory
4. **Identify signals and gaps** — Flag strong positive signals, concerning gaps, and areas needing clarification
5. **Generate recruiter screen questions** — Write 3-5 targeted questions to validate gaps or ambiguous areas
6. **Produce recommendation** — Strong advance / Advance / Hold for discussion / Pass, with clear reasoning
7. **If ATS connected** — Check for prior applications, referral source, and any existing notes

## Output Structure

```
## Candidate Screen: [Candidate Name] → [Role Title]

### Overall Assessment: [Strong Advance / Advance / Hold / Pass]

### Fit Matrix

| Dimension | Requirement | Candidate signal | Fit |
|-----------|------------|-----------------|-----|
| [Technical skill] | [what's needed] | [what they have] | ✅/⚠️/❌ |
| [Domain experience] | ... | ... | ... |
| [Seniority/scope] | ... | ... | ... |
| [Education/certs] | ... | ... | ... |

### Strong Signals
- [Positive indicator with evidence]

### Gaps & Risks
- [Gap or concern with context on severity]

### Recruiter Screen Questions
1. [Question targeting a specific gap]
2. [Question to validate a claim]
3. [Question about motivation/fit]

### Recommendation
[2-3 sentence summary of recommendation with key reasoning]
```

## With Connectors

- **If ATS connected**: Check application history, source attribution, and prior interview feedback
- **If data enrichment connected**: Enrich with current title, company details, tenure, and social profiles
- **If knowledge base connected**: Pull the team's screening rubric and hiring manager preferences

## Tips

- For best results, provide both the resume AND the job description
- Mention any dealbreakers upfront (e.g., "must be willing to relocate", "no agency candidates")
- If screening multiple candidates for the same role, run this command for each and compare outputs
