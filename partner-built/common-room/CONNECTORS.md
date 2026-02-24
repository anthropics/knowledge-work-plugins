# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. This plugin is built around Common Room as the primary data source — but some workflows benefit from an optional calendar integration.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Calendar | `~~calendar` | Google Calendar (via MCP) | Outlook / Microsoft 365 Calendar |

## Common Room MCP

The Common Room MCP server (`mcp.commonroom.io/mcp`) is the primary data source for all skills and commands in this plugin. It is listed in `.mcp.json` and must be connected and authenticated for the plugin to function.

## Calendar (Optional)

The `~~calendar` connector is used in two skills:
- **call-prep** — to automatically pull attendee names from upcoming meetings
- **weekly-prep-brief** — to fetch all external meetings scheduled in the next 7 days

If no calendar is connected, both skills gracefully fall back to asking the user for meeting details manually. The calendar connector is entirely optional.

To connect a calendar, install a compatible calendar MCP server and ensure it is authenticated. The plugin will automatically detect and use it when available.
