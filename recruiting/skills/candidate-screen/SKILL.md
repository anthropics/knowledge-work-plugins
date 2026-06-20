---
name: Candidate Screen
stability: stable
description: Screen resumes and candidates quickly against job requirements. Produce structured summaries, red flags, and interview recommendations to help prioritize your pipeline.
triggers:
  - "screen this resume"
  - "evaluate this candidate"
  - "review these applications"
  - "rank these candidates"
  - "shortlist candidates for"
---

# Candidate Screen

Move faster from applications to interviews. Screen candidates against role requirements and produce consistent, structured evaluations in seconds.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│ CANDIDATE SCREEN                                                │
├─────────────────────────────────────────────────────────────────┤
│ ALWAYS (works standalone)                                       │
│ ✓ Paste resume + job description                               │
│ ✓ Evaluate against must-have and nice-to-have criteria        │
│ ✓ Identify gaps, strengths, and red flags                     │
│ ✓ Recommend: advance / hold / reject with rationale           │
├─────────────────────────────────────────────────────────────────┤
│ SUPERCHARGED (when you connect your tools)                      │
│ + ATS (Greenhouse, Lever): pull applications automatically    │
│ + Notion/Slack: post screening summaries to team channel      │
│ + Calendar: auto-schedule interviews for advanced candidates  │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

Share the job description and candidate materials:
- "Screen this resume for our senior backend engineer role: [paste JD + resume]"
- "Review these 5 applications for the product manager position and rank them"
- "Does this candidate meet the minimum requirements for our data scientist role?"

**Required:**
- Job description or role requirements
- Candidate resume or application materials

## Output Format

```markdown
# Candidate Screen: [Name] — [Role]

**Recommendation:** ✅ Advance | ⚠️ Hold | ❌ Reject

## Summary
[2-3 sentence overview of the candidate]

## Requirements Match

| Requirement | Status | Evidence |
|-------------|--------|----------|
| [Must-have 1] | ✅ Met | [Quote or note from resume] |
| [Must-have 2] | ⚠️ Partial | [Explanation] |
| [Must-have 3] | ❌ Missing | [What's absent] |
| [Nice-to-have 1] | ✅ Met | [Evidence] |

## Strengths
- [Specific strength with evidence]
- [Specific strength with evidence]

## Concerns
- [Concern or gap]
- [Concern or gap]

## Red Flags
- [Any serious concerns: gaps, inconsistencies, misrepresentation]

## Suggested Interview Focus
If advancing: explore these areas in the interview:
1. [Probing question for a gap]
2. [Probing question for a strength to validate]
3. [Situational question based on role needs]

## Notes for Hiring Manager
[Any context, comparison to other candidates, or special considerations]
```

## Screening Multiple Candidates

When screening 5+ candidates for the same role:
1. Provide the job description once
2. Paste all resumes together
3. Request: "Screen all of these and rank them 1-N with a comparison table"

Output will include:
- Individual screen for each candidate
- Comparative ranking table
- Recommended shortlist (typically top 3-5)

## Related Skills
- **job-description** — Write the JD before screening candidates
- **interview-prep** — Prepare structured interview questions for shortlisted candidates
- **offer-letter** — Draft offer letters for selected candidates
