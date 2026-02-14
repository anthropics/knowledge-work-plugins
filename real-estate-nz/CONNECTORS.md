# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~cloud storage` might mean SharePoint, Box, or any other storage provider with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM / Leads | `~~contact database` | NurtureCloud | Salesforce, HubSpot, Propertybase |
| Property Data | `~~property database` | CoreLogic / PropertyValue | Trade Me API, REINZ Stats |
| Cloud storage | `~~cloud storage` | SharePoint | Google Drive, OneDrive, Box |
| Legislative database | `~~legislation` | NZLII / REA | Westlaw, LexisNexis |
| Budgetary data | `~~budget data` | Hutt City Council | Stats NZ, Treasury.gov |
| Social media | `~~social media` | openclaw | Twitter/X API, LinkedIn |
