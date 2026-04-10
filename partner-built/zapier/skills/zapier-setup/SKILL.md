---
name: zapier-setup
description: Set up Zapier MCP and add tools to your AI assistant. Introduces what Zapier can do, walks through authentication, detects your server mode, then branches into the right flow — summary for healthy setups, reconnect for broken auth, onboarding for fresh installs, or config help when the server is missing. Use when getting started, troubleshooting connection issues, adding new tools, or when the user asks "what can I do now", "what can I do with Zapier", "show me how the Zapier plugin works", "what is Zapier MCP", "how does Zapier work", or "tell me about Zapier".
---

# Zapier setup

Introduce Zapier MCP, get the user authenticated, detect their server mode, then guide them through the appropriate setup flow.

## Step 1: Introduction

Start by describing what Zapier MCP can do for the user, then get them authenticated.

### Pitch

"Zapier MCP connects your AI assistant to 9,000+ apps — Slack, Gmail, Google Calendar, Jira, Notion, HubSpot, and thousands more. Once set up, you can search across your tools, take actions, and automate workflows, all through natural conversation. It's personalized to your workflow — you pick the apps and actions that matter to you, and your AI learns to use them."

### Check connection

Check if any Zapier MCP tools are available:

- **Tools are available** (either Agentic meta-tools or Classic action tools): The user is already authenticated. Give a shorter version of the pitch — "You've got Zapier MCP installed and connected. Let me check what you have set up." — then proceed to Step 2.

- **No Zapier tools available at all**: The server is installed but needs authentication. First, attempt to authenticate directly in the chat by calling `mcp_auth` on the Zapier MCP server. If that succeeds, re-check available tools and proceed to Step 2.

  If `mcp_auth` fails or is unavailable, fall back to manual instructions based on their client:

  - **In Cursor:** "Let's get you connected. Go to **Settings > Cursor Settings > Tools & MCP** and click **Connect** next to the Zapier MCP server. You can also press **Cmd+Shift+P** and search for 'MCP' to get there quickly."
  - **In Claude Desktop:** "Let's get you connected. Go to **Customize > Connectors > Zapier** and click **Connect**."
  - **In other clients:** "Let's get you connected. Find the Zapier MCP server in your client's MCP settings and click Connect. This will redirect you to mcp.zapier.com to sign in."

  Detect which client is in use from the environment or conversation context. If unclear, give the generic instructions.

  Wait for the user to confirm ("done"), then re-check available tools and proceed to Step 2.

## Step 2: Detect mode

Check which tools are available to determine the server mode:

- **Agentic mode**: `list_enabled_zapier_actions` is available as a tool. Call `get_zapier_skill` with name `"zapier-mcp-onboarding"` on the Zapier MCP server and follow its instructions. If authentication is needed, help the user through it, then retry the call. **Do not continue with the steps below** — the Zapier-hosted onboarding skill handles the entire Agentic setup flow.

- **Classic mode**: `get_configuration_url` and/or individual `app_action_name` tools are present, but `list_enabled_zapier_actions` is not. Continue to Step 3.

## Step 3: Diagnose

This step applies only to **Classic mode**.

Try calling `get_configuration_url` or any Zapier tool. The result determines which branch to follow:

| Result                                                        | Branch              |
| ------------------------------------------------------------- | ------------------- |
| Zapier action tools are available (e.g., `gmail_send_email`)  | **Healthy**         |
| Only `get_configuration_url` is available (no action tools)   | **Fresh install**   |
| Fails with auth/401 error                                     | **Auth broken**     |
| No Zapier tools available at all (server not connected)       | **Not connected**   |

## Branch: Healthy

The server is connected and has action tools configured. Show a summary and offer next steps.

1. Look at the available Zapier MCP tools. Each action tool follows the naming pattern `app_action_name` (e.g., `slack_send_channel_message`, `gmail_find_email`). Identify the app from the tool description (e.g., "Send a **Slack** channel message" → Slack).
2. Group tools by app and show a clean summary:

"Your Zapier MCP is connected with [N] tools across [app list]:

- **Slack**: `slack_send_channel_message`, `slack_find_message`, `slack_get_message`
- **Gmail**: `gmail_find_email`, `gmail_send_email`
- **Google Calendar**: `google_calendar_find_events`, `google_calendar_create_event`

Everything's working. What would you like to do?"

3. Offer options:
   - "Add more tools" → call `get_configuration_url` and direct the user there
   - "Run a health check" → trigger the **zapier-status** skill
   - "Create my tools profile" → trigger the **create-my-tools-profile** skill
   - Or just start using the tools

## Branch: Auth broken

The server exists in the config but authentication has expired or is invalid.

1. Tell the user:

"Your Zapier MCP server is configured but the connection is broken (authentication expired).

**[Click here to reconnect](https://mcp.zapier.com)**

Sign in, find your server, and re-authenticate. Come back and say **done** when you're finished."

2. Wait for the user to confirm.
3. Try calling a Zapier tool again to verify.
4. If it works: show the Healthy summary.
5. If it still fails: suggest deleting and recreating the server config. Offer to help update the MCP config file with a fresh token (see "MCP config by client" below).

## Branch: Not connected

The Zapier MCP server is installed via the plugin but hasn't been authenticated yet. This is the most common state on a fresh install — zero Zapier tools are visible because the server hasn't been connected.

1. Tell the user the Zapier plugin is installed but needs to be connected first.

2. Attempt to authenticate directly in the chat by calling `mcp_auth` on the Zapier MCP server. If that succeeds, skip to step 5.

3. If `mcp_auth` fails or is unavailable, fall back to manual instructions based on their client:

   - **In Cursor:** "Go to **Settings > Cursor Settings > Tools & MCP** and click **Connect** next to the Zapier MCP server. You can also press **Cmd+Shift+P** and search for 'MCP' to get there quickly."
   - **In Claude Desktop:** "Go to **Customize > Connectors > Zapier** and click **Connect**."
   - **In other clients:** "Find the Zapier MCP server in your client's MCP settings and connect it. This will redirect you to mcp.zapier.com to sign in."

   Detect which client is in use from the environment or conversation context. If unclear, give the generic instructions.

4. Wait for the user to confirm ("done").

5. Re-diagnose by checking available Zapier MCP tools. Proceed to the appropriate branch — most likely **Fresh install** (server connected, no action tools yet).

## Branch: Fresh install

The server is connected but has no action tools. The user needs to add actions through the web UI.

### Step 1: Workflow-first discovery

Don't ask "what apps do you use?" Start with what they're trying to accomplish.

"You're connected but don't have any tools set up yet. Let's add some."

Call `get_configuration_url` and share the returned URL so the user can go directly to their server's tool config page.

Then help them pick what to add based on their workflow:

**Starter kits by workflow:**

| Workflow                 | Apps                                                          | Why these                                              |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------ |
| **Dev workflow**         | Jira + GitLab + Slack + Google Docs                           | Issue tracking, code review, team comms, documentation |
| **PM workflow**          | Jira + Slack + Google Docs + Google Calendar + Notion         | Planning, updates, writing, scheduling, knowledge base |
| **Sales workflow**       | HubSpot + Gmail + Google Calendar + Slack                     | CRM, outreach, scheduling, team updates                |
| **Marketing workflow**   | Google Sheets + Slack + Notion + Gmail                        | Data, coordination, content, campaigns                 |
| **General productivity** | Gmail + Google Calendar + Slack + Google Docs + Google Sheets | The essentials for anyone                              |

"Pick a starter kit, or tell me what you're working on and I'll suggest the right tools."

### Step 2: Guide configuration

Recommend specific actions the user should add for each app in the web UI. Aim for 2-4 actions per app: one or two search actions and one or two write actions.

**Recommended starters by app:**

| App             | Search actions                         | Write actions            |
| --------------- | -------------------------------------- | ------------------------ |
| Slack           | Find Message, Get Message              | Send Channel Message     |
| Gmail           | Find Email                             | Send Email, Create Draft |
| Google Calendar | Find Events                            | Create Detailed Event    |
| Google Docs     | Get Document Content                   | Create Document          |
| Google Sheets   | Get Data Range, Lookup Row             | Add Row                  |
| Jira            | Find Issue by Key, Find Issues via JQL | Create Issue             |
| Linear          | Find Issue                             | Create Issue             |
| GitLab          | Find Merge Requests                    | (read-heavy by nature)   |
| GitHub          | Find Issue, Find Pull Request          | Create Issue             |
| HubSpot         | Find Contact, Find Company             | Create Contact           |
| Notion          | Find Page, Find Database Item          | Create Page              |
| Zoom            | Find Meeting                           | (read-heavy)             |
| Coda            | Find Row                               | Create Row               |
| Airtable        | Find Record                            | Create Record            |

Tell the user which actions to add for their chosen apps, then wait for them to configure and authenticate everything in the web UI.

"Add those actions and connect your app accounts in the Zapier dashboard. Come back and say **done** when you're finished."

### Step 3: Verify

After the user confirms, check the available Zapier MCP tools to see what was added. If new action tools appeared, show a summary. If nothing changed, the user may need to reload their client (see "Reload instructions by client" below).

### Step 4: Generate profile

Once everything is connected:

1. Show a final summary of the setup.
2. Offer to generate personalized instructions:

"Want me to create a tools profile? It teaches your AI exactly when and how to use each of these tools in future conversations."

If yes, follow the **create-my-tools-profile** skill.

## MCP config by client

| Client         | Config file location                                                      | Scope          |
| -------------- | ------------------------------------------------------------------------- | -------------- |
| Cursor         | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)             | Project/Global |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) | Global         |
| Claude Code    | `.mcp.json` (project) or `~/.claude/mcp.json` (global)                    | Project/Global |
| Windsurf       | `~/.codeium/windsurf/mcp_config.json`                                     | Global         |

Detect which client is in use from the environment or conversation context. If unclear, ask.

## Reload instructions by client

| Client         | How to reload                                 |
| -------------- | --------------------------------------------- |
| Cursor         | Cmd+Shift+P → "Reload Window"                 |
| Claude Desktop | Quit and reopen the app                       |
| Claude Code    | Run `/mcp` to check status, restart if needed |
| Windsurf       | Cmd+Shift+P → "Reload Window"                 |

## Tone

Casual and efficient. Don't explain MCP or protocol details. Just get them to the right place fast. If something breaks, be direct: "That didn't work. Let's try..."
