---
name: interview-design
description: "Design structured interview processes with competency coverage, question banks, and interviewer assignments. Ensures every competency is assessed without redundancy. Trigger with \"design an interview loop\", \"set up interviews for this role\", \"what should we ask\", \"interview plan\", \"who should interview\", or when the user discusses structuring an interview process for a role."
---

# Interview Design

Framework for building structured interview loops that comprehensively assess candidates while respecting everyone's time. Ensures competency coverage across stages with no gaps or redundancy.

## How It Works

- **Standalone**: Describe the role and get a complete interview plan with stages, competencies, questions, and interviewer profiles.
- **With connectors**: Pull the existing interview plan from the ATS, check interviewer availability on the calendar, and reference the company's competency framework from the knowledge base.

## Interview Loop Architecture

### Standard Stages

| Stage | Purpose | Duration | Who | Competencies |
|-------|---------|----------|-----|-------------|
| **Recruiter screen** | Qualification, motivation, logistics | 30 min | Recruiter | Motivation, baseline qualification, logistics |
| **Hiring manager screen** | Role fit, scope, working style | 45 min | Hiring manager | Domain knowledge, scope/impact, collaboration |
| **Technical/skills assessment** | Core functional skills | 60 min | Technical peer | Technical skills, problem-solving, depth |
| **Cross-functional/collaboration** | Teamwork, communication, influence | 45 min | Cross-functional partner | Communication, stakeholder management, influence |
| **Culture and values** | Values alignment, growth mindset | 30-45 min | Culture interviewer | Values alignment, self-awareness, growth |
| **Executive/bar raiser** | Overall bar, strategic thinking | 30-45 min | Skip-level leader | Strategic thinking, judgment, leadership |

### Competency Coverage Matrix

When designing a loop, build a matrix ensuring every critical competency is assessed at least once, and the most important ones are assessed twice by different interviewers:

```
                    Recruiter  HM Screen  Technical  Collab  Culture  Exec
Technical skills       —         ○          ●         —       —       ○
Domain expertise       ○         ●          ○         —       —       —
Problem-solving        —         ○          ●         ○       —       —
Communication          ○         ○          —         ●       ○       —
Leadership/influence   —         ○          —         ●       —       ●
Values alignment       ○         —          —         —       ●       ○
Growth/learning        —         —          ○         —       ●       —
Strategic thinking     —         ○          —         —       —       ●

● = primary assessor    ○ = secondary signal    — = not assessed
```

### Question Design Principles

1. **Behavioral questions** — "Tell me about a time when..." with STAR follow-ups
2. **Situational questions** — "How would you approach..." for judgment and thinking style
3. **Technical questions** — Role-specific skills demonstration
4. **Case questions** — Real problems from the team (anonymized) to see their approach

For each question, define:
- The competency being assessed
- What "great" looks like (specific, observable behaviors)
- What "concerning" looks like
- Follow-up probes to go deeper

### Calibration Guide

Before the first candidate, align the interview panel:
- Review the role requirements and hiring bar together
- Walk through sample answers at each scoring level
- Clarify what "meets the bar" means for this specific role and level
- Assign specific competencies to each interviewer — no overlap except intentional double-coverage

## Output Format

When designing an interview loop, produce:

1. **Loop summary** — stages, interviewers, total candidate time
2. **Competency coverage matrix** — visual map of who assesses what
3. **Per-stage interview guide** — questions, rubrics, time allocation
4. **Calibration agenda** — what to align on before interviews start
5. **Logistics checklist** — scheduling, tools, candidate communication

## Connectors

| Connector | Enhancement |
|-----------|------------|
| ATS | Pull existing interview plans, submit scorecards, configure stages |
| Calendar | Check interviewer availability, schedule the loop, send invites |
| Knowledge base | Access competency frameworks, question banks, past interview guides |
| Video | Set up interview rooms and meeting links |
