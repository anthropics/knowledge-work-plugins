# HR Plugin

A people operations plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Helps with recruiting, onboarding, performance management, policy guidance, and compensation analysis. Works with any HR team — standalone with your input, supercharged when you connect your HRIS, ATS, and other tools.

## Installation

```bash
claude plugins add knowledge-work-plugins/human-resources
```

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---|---|
| `/draft-offer` | Draft an offer letter with compensation details, start date, and terms |
| `/onboarding` | Generate an onboarding checklist and first-week plan for a new hire |
| `/performance-review` | Structure a performance review — self-assessment prompts, manager template, calibration prep |
| `/policy-lookup` | Find and explain company policies — PTO, benefits, expense, travel, remote work |
| `/comp-analysis` | Analyze compensation data — benchmarking, band placement, equity refresh modeling |
| `/people-report` | Generate headcount, attrition, diversity, or org health reports |

All commands work **standalone** (provide context and details) and get **supercharged** with MCP connectors.

## Skills

Domain knowledge Claude uses automatically when relevant:

| Skill | Description |
|---|---|
| `recruiting-pipeline` | Track and manage recruiting pipeline — source, screen, interview, offer stages |
| `employee-handbook` | Answer questions about company policies, benefits, and procedures |
| `compensation-benchmarking` | Benchmark compensation against market data — base, equity, total comp |
| `org-planning` | Headcount planning, org design, and team structure optimization |
| `people-analytics` | Analyze workforce data — attrition trends, engagement signals, diversity metrics |
| `interview-prep` | Create structured interview plans — competency-based questions, scorecards, debrief templates |

## Example Workflows

### Drafting an Offer

```
/draft-offer
```

Tell me the role, level, location, and comp details. Get a complete offer letter draft with terms, equity breakdown, and benefits summary.

### Onboarding a New Hire

```
/onboarding
```

Provide the new hire's name, role, team, and start date. Get a comprehensive onboarding checklist, first-week calendar, tool access list, and buddy assignment template.

### Preparing for Performance Reviews

```
/performance-review
```

Get templates for self-assessments, manager reviews, and calibration. I'll help structure feedback that's specific, actionable, and fair.

### Understanding Benefits

Just ask naturally:
```
What's our parental leave policy?
```

The `employee-handbook` skill triggers automatically and searches your connected knowledge base for the answer.

### Compensation Benchmarking

```
/comp-analysis
```

Upload comp data or describe your bands. Get market comparisons, band placement analysis, and recommendations for adjustments.

## Standalone + Supercharged

Every command and skill works without any integrations:

| What You Can Do | Standalone | Supercharged With |
|-----------------|------------|-------------------|
| Draft offers | Provide details manually | HRIS, ATS for auto-fill |
| Onboarding checklists | Describe your process | HRIS, Knowledge base for templates |
| Performance reviews | Manual input | HRIS for review history |
| Policy lookup | Paste handbook content | Knowledge base |
| Comp analysis | Upload CSV, describe bands | Compensation data MCP |
| People reports | Upload data | HRIS for live data |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **HRIS** | Workday, BambooHR, Rippling | Employee data, org structure, PTO balances |
| **ATS** | Greenhouse, Lever, Ashby | Candidate pipeline, interview schedules, offer tracking |
| **Compensation** | Pave, Radford | Market benchmarks, comp band data |
| **Chat** | Slack, Teams | Team announcements, candidate coordination |
| **Calendar** | Google Calendar, Microsoft 365 | Interview scheduling, onboarding calendar |
| **Email** | Gmail, Microsoft 365 | Offer letters, candidate communications |

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations.

## Settings

Create a local settings file at `human-resources/.claude/settings.local.json` to personalize:

```json
{
  "company": "Your Company",
  "headquarters": "City, State",
  "employeeCount": 500,
  "benefits": {
    "healthInsurance": "Provider Name",
    "pto": "Unlimited / X days",
    "parentalLeave": "X weeks"
  },
  "compensation": {
    "currency": "USD",
    "equityType": "RSU / Options",
    "vestingSchedule": "4 years, 1 year cliff"
  }
}
```

The plugin will ask you for this information interactively if it's not configured.
