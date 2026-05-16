# Source Discovery

Use this skill when the user wants to understand what enterprise knowledge sources are available to them through ContextIQ.

## When to use

- User asks "what sources do I have access to?"
- User wants to know what knowledge bases or document collections are available
- User needs to understand the scope of content they can query
- User asks about specific document types, departments, or topics available

## How to use

1. Call the `contextiq` MCP server's `list_sources` tool to retrieve available sources
2. Present the sources with their descriptions, types, and scope
3. Help the user understand what kinds of questions each source can answer

## Important behavior

- Only show sources the user is entitled to access
- Group sources by type or domain when presenting multiple sources
- If no sources are available, guide the user to contact their administrator
- If the MCP server is not connected, guide the user to run `./contextiq-setup` — they need a setup URL or config file from their admin. If they are the admin, point them to the quickstart guide: https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md
