# Recruiting Plugin

An AI-powered recruiting specialist for talent acquisition professionals, hiring managers, and HR teams. Built for [Claude Cowork](https://claude.ai) but also compatible with Claude Code.

## What It Does

The Recruiting plugin helps you move faster from job opening to hired candidate without sacrificing quality.

| Skill | How it helps |
|-------|-------------|
| **Candidate Screen** | Screen resumes against job requirements; produce structured evaluations and shortlists |
| **Job Description** | Write compelling, inclusive JDs that attract the right candidates |
| **Interview Prep** | Build structured interview guides with role-specific questions and scorecards |
| **Offer Letter** | Draft competitive offer letters tailored to candidate and role |

## Connectors

| Connector | What it adds |
|-----------|-------------|
| Slack | Hiring team communication and candidate notifications |
| Greenhouse | Pull applications, update candidate stages, log activities |
| Lever | ATS integration for pipeline management |
| LinkedIn | Source passive candidates and research profiles |
| Notion | Hiring documentation, interview feedback, and offer tracking |
| Microsoft 365 | Calendar scheduling and offer letter delivery |

## Quick Start

### Claude Cowork
Install from [claude.com/plugins](https://claude.com/plugins).

### Claude Code
```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install recruiting@knowledge-work-plugins
```

## Example Prompts

- "Screen this resume against our senior product designer JD: [paste both]"
- "Write a job description for a mid-level data engineer, remote, fintech company"
- "Create an interview guide for a customer success manager role, 4 rounds"
- "Draft an offer letter for Sofia Chen: $145k base, 0.2% equity, start date July 1"
- "Compare these 3 final-round candidates and recommend who to hire"

## Making It Yours

**Connect your ATS** — Update `.mcp.json` with your Greenhouse or Lever credentials to pull live candidate data.

**Add your rubrics** — Include your company's competency frameworks and leveling criteria in the skill files.

**Customize for inclusion** — Add your DEI guidelines to the JD and screening skills.

**Build new workflows** — Add skills for reference checks, recruiter sourcing, or onboarding handoffs.

## Contributing

Fork the repo, improve the skills, and send a pull request.
