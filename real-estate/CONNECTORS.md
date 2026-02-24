# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~cloud storage` might mean SharePoint, Box, or any other storage provider with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM / Leads | `~~contact database` | Vault RE / NurtureCloud | Salesforce, HubSpot, Propertybase |
| Webhooks | `~~webhook listener` | Private Admin API | Zapier, Make, Custom |
| Property Data | `~~property database` | CoreLogic / PropertyValue | Trade Me API, REINZ Stats |
| Cloud storage | `~~cloud storage` | Google Workspace (Admin) | SharePoint, OneDrive, Box |
| Legislative database | `~~legislation` | NZLII / REA | Westlaw, LexisNexis |
| Budgetary data | `~~budget data` | Hutt City Council | Stats NZ, Treasury.gov |
| Social media | `~~social media` | **OpenClaw** | Twitter/X API, LinkedIn |
| Digital Signing | `~~signing service` | Secure Sign / DocuSign | Adobe Sign, HelloSign |

## Shadow Workflow Setup

To maintain a shadow workflow, it is recommended to:
1.  Use a **private Google Workspace Admin** account for `~~cloud storage`.
2.  Set up a webhook listener to pipe **Vault RE** events into your private account.
3.  Use **OpenClaw** for all personal brand management.
