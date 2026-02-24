# Operations Plugin

A business operations plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Helps with vendor management, process documentation, change management, capacity planning, compliance tracking, and resource planning. Works with any ops team — standalone with your input, supercharged when you connect your ITSM, project tracker, and other tools.

## Installation

```bash
claude plugins add knowledge-work-plugins/operations
```

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---|---|
| `/vendor-review` | Evaluate a vendor — cost analysis, risk assessment, contract summary, and renewal recommendation |
| `/process-doc` | Document a business process — flowcharts, RACI matrices, SOPs, and runbooks |
| `/change-request` | Create a change management request — impact analysis, rollback plan, approval routing |
| `/capacity-plan` | Plan resource capacity — workload analysis, headcount modeling, utilization forecasting |
| `/status-report` | Generate a status report — project updates, KPIs, risks, and action items for leadership |
| `/runbook` | Create or update an operational runbook — step-by-step procedures for recurring tasks |

All commands work **standalone** (provide context and details) and get **supercharged** with MCP connectors.

## Skills

Domain knowledge Claude uses automatically when relevant:

| Skill | Description |
|---|---|
| `vendor-management` | Evaluate, compare, and manage vendor relationships — contracts, performance, risk |
| `process-optimization` | Analyze and improve business processes — identify bottlenecks, reduce waste, streamline workflows |
| `change-management` | Plan and execute organizational or technical changes — communication, training, adoption |
| `risk-assessment` | Identify, assess, and mitigate operational risks — risk registers, impact analysis, controls |
| `compliance-tracking` | Track compliance requirements — audits, certifications, regulatory deadlines, policy adherence |
| `resource-planning` | Plan and optimize resource allocation — capacity, utilization, forecasting, budget |

## Example Workflows

### Evaluating a Vendor

```
/vendor-review
```

Provide the vendor name, contract details, or upload a proposal. Get a structured evaluation with cost analysis, risk flags, and a recommendation.

### Documenting a Process

```
/process-doc employee offboarding
```

Describe the process or walk me through it. Get a complete SOP with flowchart, RACI matrix, and step-by-step procedures.

### Submitting a Change Request

```
/change-request
```

Describe the change. Get an impact analysis, risk assessment, rollback plan, and communication template ready for approval.

### Planning Capacity

```
/capacity-plan
```

Upload team data or describe your resources. Get utilization analysis, bottleneck identification, and headcount recommendations.

### Leadership Status Report

```
/status-report
```

I'll pull updates from your connected tools (or ask you for input) and generate a polished status report with KPIs, risks, and next steps.

### Creating a Runbook

```
/runbook monthly close process
```

Walk me through the process once. I'll document it as a repeatable runbook with checklists, troubleshooting, and escalation paths.

## Standalone + Supercharged

Every command and skill works without any integrations:

| What You Can Do | Standalone | Supercharged With |
|-----------------|------------|-------------------|
| Vendor reviews | Provide details, upload proposals | Procurement, Knowledge base |
| Process documentation | Describe the process | Knowledge base (existing docs) |
| Change requests | Describe the change | ITSM, Project tracker |
| Capacity planning | Upload data, describe team | Project tracker (workload data) |
| Status reports | Provide updates manually | Project tracker, Chat, Calendar |
| Runbooks | Walk through the process | Knowledge base, ITSM |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **ITSM** | ServiceNow, Zendesk | Ticket management, change requests, incident tracking |
| **Project tracker** | Asana, Jira, monday.com | Project status, resource allocation, task tracking |
| **Knowledge base** | Notion, Confluence | Process docs, runbooks, policies |
| **Chat** | Slack, Teams | Team coordination, approvals, status updates |
| **Calendar** | Google Calendar, Microsoft 365 | Meeting scheduling, deadline tracking |
| **Email** | Gmail, Microsoft 365 | Vendor communications, approvals |

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations.

## Settings

Create a local settings file at `operations/.claude/settings.local.json` to personalize:

```json
{
  "company": "Your Company",
  "team": "Operations",
  "reportingCadence": "weekly",
  "approvalChain": ["Manager", "Director", "VP"],
  "complianceFrameworks": ["SOC 2", "ISO 27001"],
  "fiscalYearStart": "January"
}
```

The plugin will ask you for this information interactively if it's not configured.
