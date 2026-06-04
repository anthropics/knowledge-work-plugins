# Recruiting Plugin

A recruiting and talent acquisition plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Source candidates, screen resumes, design interviews, run debriefs, write job descriptions, and manage your hiring pipeline. Works with any recruiting team — standalone with web search and your input, supercharged when you connect your ATS, email, and other tools.

## Installation

```bash
claude plugins add knowledge-work-plugins/recruiting
```

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---|---|
| `/source` | Build a targeted sourcing strategy — channels, Boolean strings, outreach angles |
| `/screen` | Screen a candidate against job requirements — fit matrix, signals, and recommendation |
| `/interview-prep` | Generate interview questions, scorecards, and loop structure for a role |
| `/debrief` | Synthesize interview feedback into a structured hiring recommendation |
| `/pipeline-review` | Analyze pipeline health — conversion rates, bottlenecks, and action plan |
| `/write-jd` | Write or improve a job description with inclusive language and clear requirements |
| `/outreach` | Draft personalized candidate outreach messages with research-backed hooks |
| `/offer-prep` | Prepare and analyze a compensation offer with market benchmarks |

All commands work **standalone** (paste resumes, JDs, notes, or describe your situation) and get **supercharged** with MCP connectors.

## Skills

Domain knowledge Claude uses automatically when relevant:

| Skill | Description |
|---|---|
| `candidate-evaluation` | Structured rubrics and scorecards for consistent, evidence-based assessment with bias mitigation |
| `interview-design` | Build interview loops with competency coverage mapping and format selection |
| `job-architecture` | Leveling frameworks, competency models, and role scoping across functions |
| `market-intelligence` | Talent market conditions, compensation benchmarks, and competitor intel |
| `pipeline-analytics` | Funnel metrics, conversion rates, time-to-fill analysis, and bottleneck diagnosis |
| `sourcing-strategy` | Boolean strings, channel mix optimization, and passive candidate engagement |
| `diversity-recruiting` | Inclusive hiring practices, bias mitigation, and diverse sourcing strategies |
| `employer-branding` | EVP messaging, job marketing, and candidate experience optimization |

## Example Workflows

### Writing a Job Description

```
/write-jd
```

Describe the role you're hiring for. Get a polished job description with clear requirements, inclusive language, and a compelling pitch. If your knowledge base is connected, it pulls your company's JD template and values.

### Screening a Candidate

```
/screen
```

Paste a resume and job description. Get a structured fit matrix scoring every dimension, strong signals, gaps, recruiter screen questions, and a clear advance/hold/pass recommendation.

### Building a Sourcing Plan

```
/source
```

Describe the role and target profile. Get a multi-channel sourcing strategy with Boolean search strings, outreach templates, and channel prioritization based on the talent market.

### Running a Debrief

```
/debrief
```

Paste interview feedback from your panel. Get a synthesized recommendation with dimension-by-dimension analysis, consensus view, and a clear hire/no-hire recommendation with reasoning.

### Researching the Market

Just ask naturally:
```
What's the market rate for a senior backend engineer in Austin?
```

The `market-intelligence` skill triggers automatically and gives you compensation benchmarks, talent supply data, and competitive landscape.

### Improving Your Pipeline

```
/pipeline-review
```

Paste pipeline data or describe your funnel. Get conversion rates benchmarked against industry standards, bottleneck diagnosis, and a prioritized action plan.

## Standalone + Supercharged

Every command and skill works without any integrations:

| What You Can Do | Standalone | Supercharged With |
|-----------------|------------|-------------------|
| Screen candidates | Paste resume + JD | ATS MCP (e.g. Greenhouse, Lever) |
| Write job descriptions | Describe the role | Knowledge base MCP (templates, values) |
| Build sourcing plans | Describe target profile | Enrichment MCP (e.g. Apollo, Clay) |
| Design interviews | Describe role + competencies | Knowledge base MCP (rubrics, guides) |
| Run debriefs | Paste interview feedback | ATS MCP (scorecards, history) |
| Draft outreach | Web search + your context | Email, Enrichment MCPs |
| Analyze pipeline | Paste data or describe funnel | ATS MCP (live pipeline data) |
| Prep offers | Describe role + candidate | HRIS MCP (comp bands, approvals) |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **ATS** | Greenhouse, Lever | Live candidate pipelines, stage updates, scorecards, duplicate detection |
| **Enrichment** | Apollo, Clay, LinkedIn | Candidate profile enrichment, contact info, company research |
| **Chat** | Slack, Teams | Hiring channel updates, hiring manager notifications, scorecard sharing |
| **Calendar** | Google Calendar, Microsoft 365 | Interviewer availability, loop scheduling, invite management |
| **Email** | Gmail, Microsoft 365 | Candidate outreach, follow-ups, offer letters |

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations, including HRIS, knowledge base, and video conferencing options.

## Settings

Create a local settings file at `recruiting/.claude/settings.local.json` to personalize:

```json
{
  "company": "Your Company",
  "industry": "Your Industry",
  "team_size": "Approximate headcount",
  "hiring_bar": "Key attributes your company values",
  "interview_process": "Your standard interview loop structure",
  "tools": {
    "ats": "Greenhouse",
    "hris": "Workday"
  }
}
```

The plugin will ask you for this information interactively if it's not configured.
