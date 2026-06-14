# Connectors

This plugin integrates with the following MCP servers. If a command references a tool or resource you don't see available, the corresponding MCP server may not be connected.

## Connected MCP Servers

| Server | Purpose | Status Check |
|--------|---------|-------------|
| **Google Calendar** | Schedule client sessions, set follow-up reminders, manage consulting calendar | Check if `gcal_list_events` is available |
| **Gmail** | Send diagnostic reports, follow-up emails, and client deliverables | Check if `gmail_search_messages` is available |
| **Google Drive** | Access and upload client session transcripts, forms, and deliverable documents | Check if Drive tools are available |
| **Notion** | Access and store client briefs, session notes, and methodology documents | Check if Notion tools are available |

## If a connector is not available

If you see a reference to a tool that is not connected:
1. The command will still work — it will ask you to provide the relevant information manually
2. To connect MCP servers, follow your Claude Code or Cowork setup guide
3. For Google Workspace connections (Calendar, Gmail, Drive), authentication is handled through your Google account

## What works without connectors

All core Land Grow pipelines work without any external connectors:
- `/grow-start` — just paste the session transcript
- `/grow-360` — just paste the form export and transcript
- `/min` — just paste the BIN and phase form
- `/client-session` — works entirely from context you provide

Connectors add convenience (scheduling, file access, sending) but are not required to run any pipeline.
