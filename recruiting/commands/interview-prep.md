---
description: Generate interview questions and scorecards
argument-hint: "<role and interview stage>"
---

# Interview Prep

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a complete interview kit: structured questions, evaluation rubrics, and scorecards tailored to a specific role and interview stage.

## Input

The user provides one or more of:
- Role title and level
- Interview stage (phone screen, technical, behavioral, hiring manager, executive, culture)
- Specific competencies to assess
- Job description
- Candidate resume (to customize questions)
- Interview duration

If minimal input, ask: "What role and interview stage are you prepping for? (e.g., 'Senior Backend Engineer - technical interview, 60 minutes')"

## Workflow

1. **Define the interview scope** — Identify the stage, duration, competencies to assess, and interviewer role
2. **Select competencies** — Map 3-5 competencies this interview should evaluate, avoiding overlap with other stages if the user describes the full loop
3. **Generate questions** — Write 4-6 primary questions with follow-up probes, calibrated to the role level
4. **Build scoring rubric** — Define what "strong hire", "hire", "no hire", and "strong no hire" look like for each competency
5. **Create the scorecard** — Structured template the interviewer can fill out during or after the interview
6. **Add interviewer guidance** — Time allocation, red/green flags to watch for, and common biases to avoid
7. **If candidate resume provided** — Customize questions to probe specific claims, career transitions, or gaps

## Output Structure

```
## Interview Kit: [Role] — [Stage]
**Duration**: [X minutes] | **Competencies**: [list]

### Opening (5 min)
- Introduce yourself and the role
- Set expectations for the interview format

### Questions

#### Q1: [Question text] ([competency], [X min])
**Follow-ups**:
- [Probe deeper on X]
- [Ask for a counter-example]

| Rating | Signal |
|--------|--------|
| Strong hire | [specific observable behavior] |
| Hire | [specific observable behavior] |
| No hire | [specific observable behavior] |
| Strong no hire | [specific observable behavior] |

#### Q2: [Question text] ([competency], [X min])
...

### Scorecard

| Competency | Rating (1-4) | Notes |
|------------|-------------|-------|
| [Competency 1] | ___ | |
| [Competency 2] | ___ | |
| ... | | |

**Overall recommendation**: Strong hire / Hire / No hire / Strong no hire

**Key evidence for recommendation**:

### Interviewer Guidance
- **Time management**: [allocation suggestions]
- **Green flags**: [what to look for]
- **Red flags**: [concerning signals]
- **Bias watch**: [common biases for this interview type]

### Closing (5 min)
- Allow candidate questions
- Explain next steps and timeline
```

## With Connectors

- **If ATS connected**: Pull the interview plan, see what other interviewers are covering, and submit the scorecard directly
- **If knowledge base connected**: Reference the company's competency framework, leveling rubrics, and past interview guides
- **If calendar connected**: Check the scheduled interview time and interviewer details

## Tips

- Specify the full interview loop if possible so questions don't overlap across stages
- Include the candidate's resume for targeted questions that validate specific claims
- For panel interviews, note how many interviewers and their roles
