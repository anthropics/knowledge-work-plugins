# Connectors

## How tool references work

Plugins are **tool-agnostic**. They describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

Many plugins use `~~category` placeholders in their files. The skills in this plugin name the category in plain words instead ("the CRM", "email", "the calendar", "call transcripts"). Either way, a skill refers to the category, so any connector in that category works. The placeholder column below maps each category to the shared naming used across plugins.

Every skill also works with nothing connected: upload an export or paste notes, and the skill works from that.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM | `~~CRM` | HubSpot, Salesforce\*, Close, Monday | Pipedrive, Attio, Zoho CRM, Copper |
| Email | `~~email` | Gmail, Microsoft 365 (Outlook)\* |  |
| Calendar | `~~calendar` | Google Calendar, Calendly, Microsoft 365 (Outlook)\* |  |
| Chat | `~~chat` | Slack, Microsoft 365 (Teams)\* |  |
| Docs and knowledge base | `~~knowledge base` | Google Drive, Notion, Atlassian (Confluence), Microsoft 365 (SharePoint)\* | Box, Dropbox, Guru |
| Conversation intelligence | `~~conversation intelligence` | Gong, Fireflies, Zoom, Otter.ai | Granola, Fathom, Chorus |
| Data enrichment | `~~data enrichment` | Clay, ZoomInfo, Apollo, Lusha, Crunchbase | Clearbit |
| Sales engagement | `~~sales engagement` | Outreach, Apollo | Salesloft |
| Competitive intelligence | `~~competitive intelligence` | Similarweb | Crayon, Klue |
| Project tracker | `~~project tracker` | Atlassian (Jira) | Linear, Asana |

## Salesforce and Microsoft 365

**Salesforce and Microsoft 365 (marked \* above) are included, and both need setup at the organization level: an admin enables the connector in Claude before people can sign in. For Salesforce, that includes setting up your org's Salesforce app.**

Once connected, the skills use them the same way as any other tool in their category.

Google Calendar, Gmail and Google Drive are listed in `.mcp.json` without a URL. Connect them in Claude's connector settings.

## Permissions

What a connector is allowed to do is set on the connector itself: allow, ask or block for each tool. The skills never go beyond those settings. See the README for recommended settings for scheduled runs.
