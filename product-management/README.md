# Product Management Plugin

A product management plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Covers the full PM workflow: writing feature specs, managing roadmaps, communicating with stakeholders, synthesizing user research, analyzing competitors, and tracking product metrics.

## Installation

```
claude plugins add knowledge-work-plugins/product-management
```

## What It Does

This plugin gives you an AI-powered product management partner that can help with:

- **Feature Specs & PRDs** — Generate structured product requirements documents from a problem statement or feature idea. Includes user stories, requirements prioritization, success metrics, and scope management.
- **Roadmap Planning** — Create, update, and reprioritize your product roadmap. Supports Now/Next/Later, quarterly themes, and OKR-aligned formats with dependency mapping and decision memos.
- **Stakeholder Updates** — Generate status updates tailored to your audience (executives, engineering, customers). Pulls context from connected tools to save you the weekly update grind.
- **User Research Synthesis** — Turn interview notes, survey data, and support tickets into structured insights. Identifies themes, builds personas, and surfaces opportunity areas with supporting evidence.
- **Competitive Analysis** — Research competitors and generate briefs with feature comparisons, positioning analysis, and strategic implications.
- **Metrics Review** — Analyze product metrics, identify trends, compare against targets, and surface actionable insights.
- **Sprint Reviews** — Summarize sprint accomplishments with velocity metrics, demo highlights, and retrospective themes. Connects the dots between delivered work and product goals.
- **Meeting Preparation** — Prepare for customer meetings, QBRs, and stakeholder calls with account context, talking points, risk assessment, and follow-up actions.
- **Daily Briefs** — Start each day with a synthesis of overnight activity across Slack, project trackers, support tickets, and community channels.
- **Prototyping** — Generate standalone interactive HTML prototypes from PRDs or feature descriptions. No dependencies, no build tools — just open in a browser.
- **Release Notes** — Turn completed Jira tickets and PRD excerpts into polished, customer-facing release notes with proper categorization and tone.
- **Feature Ideation** — Structure raw ideas from Slack threads, customer feedback, and brainstorms into validated feature concepts ready for a PRD.
- **Executive Summaries** — Distill complex information into one-pagers (under 500 words) and TL;DRs (3-5 bullets) optimized for busy stakeholders.

## Commands

| Command | What It Does |
|---|---|
| `/write-spec` | Write a feature spec or PRD from a problem statement |
| `/roadmap-update` | Update, create, or reprioritize your roadmap |
| `/stakeholder-update` | Generate a stakeholder update (weekly, monthly, launch) |
| `/synthesize-research` | Synthesize user research from interviews, surveys, and tickets |
| `/competitive-brief` | Create a competitive analysis brief |
| `/metrics-review` | Review and analyze product metrics |
| `/daily-brief` | Synthesize overnight activity into a morning brief |
| `/meeting-prep` | Prepare for customer meetings with context and talking points |
| `/sprint-review` | Generate a sprint review summary with metrics and demos |
| `/prototype` | Generate an interactive HTML prototype from a PRD or feature description |
| `/release-notes` | Create customer-facing release notes from completed work |
| `/feature-ideation` | Structure raw ideas into validated feature concepts |
| `/one-pager` | Synthesize complex information into a one-page executive summary |
| `/tldr` | Create a quick 3-5 bullet summary for Slack or email |

## Skills

| Skill | What It Covers |
|---|---|
| `feature-spec` | PRD structure, user stories, requirements categorization, acceptance criteria, idea structuring |
| `roadmap-management` | Prioritization frameworks (RICE, MoSCoW), roadmap formats, dependency mapping, decision memos |
| `stakeholder-comms` | Update templates by audience, risk communication, decision documentation |
| `user-research-synthesis` | Thematic analysis, affinity mapping, persona development, opportunity sizing |
| `competitive-analysis` | Feature comparison matrices, positioning analysis, win/loss analysis |
| `metrics-tracking` | Product metrics hierarchy, goal setting (OKRs), dashboard design, review cadences |
| `sprint-execution` | Sprint metrics, velocity analysis, demo preparation, burndown interpretation, retrospectives |
| `meeting-preparation` | Account review methodology, talking point frameworks, risk identification, QBR planning |
| `release-communication` | Customer-facing writing, changelog categorization, version conventions, deprecation lifecycle |
| `executive-synthesis` | Pyramid principle, one-pager framework, TL;DR writing, audience adaptation |
| `html-prototyping` | Design defaults, responsive layout patterns, interactive components, accessibility basics |

## Example Workflows

### Writing a PRD

```
You: /write-spec
Claude: What feature or problem are you speccing out?
You: We need to add SSO support for enterprise customers
Claude: [Asks about target users, constraints, success metrics]
Claude: [Generates full PRD with problem statement, user stories, requirements, success metrics, open questions]
```

### Preparing a Stakeholder Update

```
You: /stakeholder-update
Claude: What type of update? (weekly, monthly, launch, ad-hoc)
You: Weekly update for the exec team
Claude: [Pulls context from project management tool, chat, and docs]
Claude: [Generates executive summary with progress, decisions, risks, and next milestones]
```

### Synthesizing User Research

```
You: /synthesize-research
Claude: What research do you want to synthesize? You can paste interview notes, upload files, or I can pull from connected sources.
You: [Pastes 8 interview transcripts]
Claude: [Identifies themes, patterns, and insights across interviews]
Claude: [Generates synthesis with key findings, personas, opportunity areas, and evidence]
```

### Competitive Analysis

```
You: /competitive-brief
Claude: Which competitor(s) or feature area do you want to analyze?
You: Compare our onboarding flow to [competitor A] and [competitor B]
Claude: [Researches competitor onboarding approaches]
Claude: [Generates brief with feature comparison, strengths/weaknesses, and strategic implications]
```

### Sprint Review

```
You: /sprint-review
Claude: What sprint are we reviewing? I'll also need the dates and team name.
You: Sprint 42, Jan 6-17, Search Pod
Claude: [Pulls completed tickets from project tracker, team discussion from Slack]
Claude: [Generates sprint summary with velocity metrics, demo highlights, blockers, and customer feedback]
```

### Morning Brief

```
You: /daily-brief
Claude: Good morning! What's your name and company? I'll synthesize what happened overnight.
You: Jane, Acme Corp
Claude: [Scans Slack channels, project tracker updates, support tickets]
Claude: [Generates prioritized brief: what needs attention today, what's blocked, what shipped overnight]
```

### Interactive Prototype

```
You: /prototype
Claude: What feature or flow should I prototype?
You: A search results page with filters for content type, date range, and author
Claude: [Generates a complete standalone HTML file with interactive filters, realistic data, and responsive layout]
Claude: [Save as .html and open in your browser — no build tools needed]
```

## Data Sources

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your project management and communication tools for the best experience. Without them, provide context manually.

**Included MCP connections:**
- Chat (Slack) for team context and stakeholder threads
- Project tracker (Linear, Asana, monday.com, ClickUp, Atlassian) for roadmap integration, ticket context, and status tracking
- Knowledge base (Notion) for existing specs, research, and meeting notes
- Design (Figma) for design context and handoff
- Product analytics (Amplitude, Pendo) for usage data, metrics, and behavioral analysis
- User feedback (Intercom) for support tickets, feature requests, and user conversations
- Meeting transcription (Fireflies) for meeting notes and discussion context

**Additional options:**
- See [CONNECTORS.md](CONNECTORS.md) for alternative tools in each category
