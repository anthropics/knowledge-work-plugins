# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Jira, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, chat, cloud storage, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams |
| Cloud storage | `~~cloud storage` | Box, Egnyte | Google Drive, SharePoint, Dropbox |
| Office suite | `~~office suite` | Microsoft 365 | Google Workspace |
| Project tracker | `~~project tracker` | Atlassian (Jira, Confluence) | Asana, Monday.com |
| Data warehouse | `~~data warehouse` | Snowflake, BigQuery | Databricks, Redshift |
| BI / Visualization | `~~bi` | — | Tableau, Power BI |

## Graceful degradation

When a connector is not available:

- **Chat unavailable**: Note that real-time notifications cannot be sent; offer to draft messages for later sending
- **Cloud storage unavailable**: Work with local files; warn that version history is unavailable
- **Project tracker unavailable**: Track tasks manually; note gaps in status visibility
- **Data warehouse unavailable**: Work with user-provided data; note inability to query live data sources
- **BI unavailable**: Describe recommended visualizations; note inability to generate interactive dashboards

The plugin will always note which tools were unavailable and what manual steps the user may need to take.
