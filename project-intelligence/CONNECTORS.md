# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Jira, Linear, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, code repository, chat, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Project tracker | `~~project tracker` | Linear, Atlassian (Jira/Confluence), Asana | monday.com, ClickUp, Shortcut, Trello |
| Code repository | `~~code repository` | GitHub, GitLab | Bitbucket, Azure DevOps |
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Testing & QA | `~~testing` | — | SonarQube (via API), Codecov (via API) |
| Incident tracking | `~~incident tracking` | — | PagerDuty, Sentry, Opsgenie |

**Note:** Skills work with manual input (CSV exports, pasted data) when MCP servers aren't available.
