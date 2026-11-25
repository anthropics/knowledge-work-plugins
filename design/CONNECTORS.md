# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~design tool` might mean Figma, Sketch, or any other design tool with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (design tool, project tracker, user feedback, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams |
| Design tool | `~~design tool` | Figma | Sketch, Adobe XD, Framer |
| Knowledge base | `~~knowledge base` | Notion | Confluence, Guru, Coda |
| Project tracker | `~~project tracker` | Linear, Asana, Atlassian (Jira/Confluence) | Shortcut, ClickUp |
| User feedback | `~~user feedback` | Intercom | Productboard, Canny, UserVoice, Dovetail |
| User research | `~~user research platform` | *(not pre-configured)* | Any MCP server that runs interviews and returns cited findings |
| Product analytics | `~~product analytics` | — | Amplitude, Mixpanel, Heap, FullStory |

`~~user research platform` plans an interview study, recruits participants (a panel or the user's own customers), runs the interviews, and returns findings with quotes traceable to each interview. `~~user feedback` stays the source for feedback that already exists. Any launch that spends money stops until the user approves the plan and the cost.
