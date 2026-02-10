# Job Search Plugin

A job search productivity plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Helps you identify decision-makers, tailor your resume, and craft personalized outreach to land your next role faster.

## Installation

```bash
claude plugins add knowledge-work-plugins/job-search
```

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---|---|
| `/find-decision-makers` | Identify hiring managers and key decision-makers at a target company |
| `/customize-resume` | Tailor your resume to a specific job listing or company |
| `/generate-loom-script` | Generate a personalized video script for outreach to a hiring manager |

All commands work **standalone** (paste job listings, describe your situation, or provide company names) and get **supercharged** with MCP connectors.

## Example Workflows

### Finding the Right People

```
/find-decision-makers
```

Provide a company name or job listing URL. Get a list of likely hiring managers, recruiters, and relevant contacts with suggested outreach approaches.

### Tailoring Your Resume

```
/customize-resume
```

Upload your resume and a job listing. Get a tailored version that highlights relevant experience and optimizes for ATS keywords.

### Recording a Standout Outreach Video

```
/generate-loom-script
```

Provide a target company, role, and recipient. Get a concise, natural-sounding script you can record and send to stand out from other applicants.

## Standalone + Supercharged

Every command works without any integrations:

| What You Can Do | Standalone | Supercharged With |
|-----------------|------------|-------------------|
| Find decision-makers | Web search + your context | LinkedIn, Enrichment MCPs |
| Customize resume | Paste resume + job listing | Knowledge base, File storage MCPs |
| Generate loom script | Web search + your context | LinkedIn, Knowledge base MCPs |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **Data enrichment** | Clay, Apollo, ZoomInfo | Contact and company data enrichment |
| **Knowledge base** | Notion, Obsidian | Store your master resume, portfolio, and notes |
| **Chat** | Slack, Teams | Networking context, referral requests |
| **LinkedIn** | LinkedIn MCP | Profile data, mutual connections, recent activity |

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations.
