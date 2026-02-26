# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~cloud storage` might mean SharePoint, Box, or any other storage provider with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Cloud storage | `~~cloud storage` | SharePoint | Google Drive, OneDrive, Box |
| Legislative database | `~~legislation` | AustLII / NZLII | Westlaw, LexisNexis |
| Hansard / Parliament | `~~hansard` | ParlInfo | OpenAustralia, TheyWorkForYou |
| Media sentiment | `~~media sentiment` | GNews | Meltwater, Cision |
| Social media | `~~social media` | openclaw | Twitter/X API, LinkedIn |
| Budgetary data | `~~budget data` | Treasury.gov | World Bank, OECD |
