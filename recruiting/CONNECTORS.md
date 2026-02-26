# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~ATS` might mean Greenhouse, Lever, Ashby, or any other applicant tracking system with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (ATS, email, calendar, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| ATS | `~~ATS` | Greenhouse, Lever | Ashby, Workday Recruiting, iCIMS, Jobvite, SmartRecruiters |
| Calendar | `~~calendar` | Google Calendar, Microsoft 365 | Calendly |
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Cloud storage | `~~cloud storage` | — | Google Drive, Dropbox, SharePoint |
| CRM | `~~CRM` | — | HubSpot, Salesforce, Bullhorn |
| Data enrichment | `~~data enrichment` | Apollo, Clay, LinkedIn | Clearbit, ZoomInfo, Lusha, People Data Labs |
| Email | `~~email` | Gmail, Microsoft 365 | — |
| HRIS | `~~HRIS` | — | BambooHR, Workday, Rippling, Gusto |
| Knowledge base | `~~knowledge base` | Notion, Atlassian (Confluence) | Guru, Slite, Coda |
| Video conferencing | `~~video` | Zoom | Google Meet, Microsoft Teams |
