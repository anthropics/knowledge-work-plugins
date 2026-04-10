# Zapier Plugin

Connect 9,000+ apps to your AI workflow. Configure your actions at mcp.zapier.com, and each one becomes a tool your AI can call directly — no config files, no tokens, no setup scripts.

## Quick Start

After installing:

1. Connect the Zapier MCP server in your client's settings:
   - **Cursor:** Settings > Cursor Settings > Tools & MCP > click **Connect**
   - **Claude Desktop:** Customize > Connectors > Zapier > click **Connect**
   - **Other clients:** Find the Zapier MCP server in your MCP settings and connect
2. Sign in to your Zapier account when prompted
3. Open a chat and say **"setup zapier"** to get started

Your server will be in one of two modes — the plugin detects which one automatically and guides you through the right flow.

## What's Included

| Component                         | Description                                                                                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **zapier-lifecycle** rule         | Enforces the safety model for reads vs writes, duplicate detection with native MCP servers, and error handling. Always active.                                    |
| **zapier-setup** skill            | Onboarding and connection management. Diagnoses your setup, branches into the right flow (fresh install, reconnect, add tools), and walks you through end-to-end. |
| **zapier-status** skill           | Three modes: health check (dashboard of connected tools), audit (find duplicates and waste), diagnose (systematic troubleshooting).                               |
| **create-my-tools-profile** skill | Scans your configured action tools and generates a personalized tools profile so your AI knows what tools you have and when to use them.                          |

## How Tools Work

Zapier MCP operates in one of two modes depending on your server configuration. The plugin detects the mode automatically.

### Agentic (Beta)

The Agentic configuration is currently in Beta and being rolled out to all users. In this mode, your server provides 14 static meta-tools for managing and executing actions directly in chat. You can discover apps, enable/disable actions, and execute reads and writes without leaving the conversation. Onboarding is handled by a Zapier-hosted skill — just say "setup zapier" and the plugin will walk you through it.

Key tools: `list_enabled_zapier_actions`, `discover_zapier_actions`, `enable_zapier_action`, `execute_zapier_read_action`, `execute_zapier_write_action`, `list_zapier_skills`, `get_zapier_skill`, and more.

### Classic

In Classic mode, each action you configure at [mcp.zapier.com](https://mcp.zapier.com) becomes its own MCP tool, named with the pattern `app_action_name`:

- **`gmail_send_email`** — Send an email via Gmail
- **`slack_find_message`** — Search for a Slack message
- **`jira_create_issue`** — Create a Jira issue
- **`google_calendar_find_events`** — Look up calendar events

There is also one built-in tool:

- **`get_configuration_url`** — Returns the URL to manage your actions (add, remove, authenticate)

## Links

- [Zapier MCP Dashboard](https://mcp.zapier.com) — Manage your server, authenticate apps, view connected tools
- [Zapier](https://zapier.com) — Learn more about Zapier
- [Zapier Status](https://status.zapier.com) — Check for outages

## Support

For issues with the plugin or Zapier MCP, contact [support@zapier.com](mailto:support@zapier.com).
