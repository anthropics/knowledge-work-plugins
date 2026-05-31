# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

TF3 stack only — Notion + ClickUp.

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Knowledge base | `~~knowledge base` | Notion | — |
| Project tracker | `~~project tracker` | ClickUp | — |

Tokens are sourced from Claude Code environment variables: `NOTION_TOKEN`, `CLICKUP_API_KEY`.
