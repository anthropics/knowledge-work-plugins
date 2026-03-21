# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~bonito` refers to the Bonito MCP server, which provides access to the Bonito AI Gateway API.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (gateway, notifications, version control, etc.) rather than specific products. The `.mcp.json` pre-configures the Bonito MCP server, but optional connectors in other categories enhance the experience.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| AI Gateway | `~~bonito` | Bonito MCP | — |
| Version Control | `~~vcs` | — | GitHub, GitLab |
| Notifications | `~~notifications` | — | Slack, Microsoft Teams, Discord |
| Monitoring | `~~monitoring` | — | Datadog, Grafana, PagerDuty |

## Required connector

### Bonito MCP (`~~bonito`)

The core connector. Provides access to the Bonito AI Gateway API for managing providers, agents, routing, and infrastructure.

**Install:** `pip install bonito-mcp`

**What it provides:**
- Provider management (create, list, verify, delete)
- Agent configuration (BonBon agents, Bonobot orchestrators)
- Routing policy management (failover, cost-optimized, A/B testing)
- Cost and usage analytics
- Gateway health and diagnostics
- Knowledge base management

## Optional connectors

### GitHub (`~~vcs`)

Connect GitHub to enable infrastructure-as-code workflows, review bonito.yaml changes in PRs, and track deployment history.

**What it adds:**
- Read bonito.yaml configs from repos
- Review infrastructure changes in pull requests
- Track deployment commits and history
- Manage infrastructure configs alongside application code

### Slack (`~~notifications`)

Connect Slack to receive deployment notifications, cost alerts, and provider status updates in your team channels.

**What it adds:**
- Deployment success/failure notifications
- Cost threshold alerts
- Provider health status updates
- Agent error notifications
