# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~LinkedIn` might mean LinkedIn Sales Navigator or any other LinkedIn tool with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (LinkedIn, job boards, email, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Data enrichment | `~~data enrichment` | — | Clay, Apollo, Clearbit, ZoomInfo |
| Email | `~~email` | — | Gmail, Microsoft 365 |
| File storage | `~~file storage` | — | Google Drive, Dropbox, Notion |
| Knowledge base | `~~knowledge base` | Notion | Confluence, Obsidian |
| LinkedIn | `~~LinkedIn` | — | LinkedIn MCP (when available) |
