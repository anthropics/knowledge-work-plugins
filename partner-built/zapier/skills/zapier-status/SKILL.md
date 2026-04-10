---
name: zapier-status
description: Check the health of your Zapier MCP setup. Three modes — health check (dashboard view), audit (find waste and duplicates), diagnose (systematic troubleshooting). Use when asking "is my MCP working?", "check my tools", "audit my setup", "what's broken?", or "zapier status".
---

# Zapier status

Three modes for monitoring and maintaining a Zapier MCP setup. Determine the mode from context, or ask if unclear.

**First, detect the server mode:** If `list_enabled_zapier_actions` is available, the user is on **Agentic mode**. Otherwise, the user is on **Classic mode** where each configured action is its own MCP tool (e.g., `slack_send_channel_message`, `gmail_find_email`).

## Mode 1: Health check

**Trigger:** "check my tools", "zapier status", "is everything working?", or any general status inquiry.

A quick dashboard view of the current state.

### Steps

1. Check the available tools:
   - **Agentic mode:** Call `list_enabled_zapier_actions` to get the inventory of enabled actions.
   - **Classic mode:** Inspect the available Zapier MCP tools. Each action tool follows the pattern `app_action_name`. The built-in `get_configuration_url` tool is always present when the server is connected.

2. If no Zapier tools are available: report the connection status and suggest running **zapier-setup** (Classic) or calling `get_zapier_skill` with name `"zapier-mcp-onboarding"` (Agentic).

3. If tools/actions are available, build a summary by grouping actions by app (Agentic: from the `list_enabled_zapier_actions` response; Classic: from each tool's description):

**For each app**, show:

- App name
- Number of actions
- Action types (infer read vs write from names: find/search/get/list = read, send/create/update/add = write)
- Quick status: working / needs auth / error

**Format as a dashboard:**

```
Zapier MCP status
=================
Server: connected
Total actions: 14 across 5 apps

Slack         3 actions (2 read, 1 write)     ✓ working
Gmail         3 actions (1 read, 2 write)     ✓ working
Google Cal    2 actions (1 read, 1 write)     ✓ working
Jira          3 actions (2 read, 1 write)     ✓ working
Google Docs   2 actions (1 read, 1 write)     ✓ working
```

4. If any actions appear broken (based on recent errors or auth issues), flag them.

5. End with: "Everything looks good." or "Found [N] issues. Want me to diagnose them?"

## Mode 2: Audit

**Trigger:** "audit my setup", "clean up my tools", "find duplicates", "what should I remove?"

Find inefficiencies: duplicate actions, unused tools, conflicts with native MCP servers.

### Steps

1. Get the full inventory:
   - **Agentic mode:** Call `list_enabled_zapier_actions`.
   - **Classic mode:** Inspect the available Zapier MCP action tools.

2. **Check for duplicates within Zapier MCP:**
   - Multiple actions for the same app that do similar things (e.g., both `slack_find_message` and `slack_search_messages`)
   - Recommend removing the less useful one

3. **Check for conflicts with native MCP servers:**
   - Look at other MCP servers configured in the client's MCP config file (e.g., `.cursor/mcp.json`, `claude_desktop_config.json`, `.mcp.json` — depends on the client)
   - If the user has both a native Slack MCP and Zapier Slack actions, flag it
   - Recommend: "You have Slack through both Zapier and a native Slack server. The native server is usually better for single-app use. Consider removing Zapier's Slack actions."

4. **Check for unused or low-value actions:**
   - Actions that are rarely useful as defaults (e.g., very specific write actions that are only needed occasionally)
   - Suggest removing actions that can be re-added on demand through the web UI

5. **Show the audit report:**

```
Audit results
=============
Duplicates:       1 found
  - Slack: "find_message" and "search_messages" overlap. Recommend removing "search_messages".

Native conflicts:  1 found
  - Slack: native Slack MCP also configured. Consider removing Zapier Slack actions.

Cleanup candidates: 2 found
  - Google Sheets "delete_row": rarely needed, can re-add on demand
  - Jira "add_attachment": niche action, add when needed

Recommended removals: 4 actions
Want me to show you how to clean these up?
```

6. If the user says yes:
   - **Agentic mode:** Use `disable_zapier_action` to remove the recommended actions directly in chat.
   - **Classic mode:** Call `get_configuration_url` and direct them to the web UI to remove the recommended actions. List exactly which ones to remove.

## Mode 3: Diagnose

**Trigger:** "what's broken?", "my tools aren't working", "debug my MCP", or when a specific tool call has failed.

Systematic troubleshooting with error pattern matching.

### Steps

1. **Gather context:** Ask what went wrong, or use the error from the current conversation.

2. **Run diagnostics in order:**

   a. **Connection check:** Try calling `get_configuration_url` or any available Zapier tool. If nothing works, the problem is server-level (auth, config, network).

   b. **Action check:**
      - **Agentic mode:** Call `list_enabled_zapier_actions` to see if the action is enabled. If not, use `discover_zapier_actions` to find it and `enable_zapier_action` to add it.
      - **Classic mode:** Is the specific action tool available? If not, the user needs to add it through the web UI.

   c. **Auth check:** Try calling a read action for the affected app (Agentic: `execute_zapier_read_action`; Classic: the specific read tool). If it returns an auth error, the app connection needs re-authentication.

   d. **Parameter check:** Review the failing call's parameters. Common issues:
   - Missing required fields
   - Wrong field format (IDs vs names)
   - Instructions that are too vague for the params resolver

3. **Match against known error patterns:**

| Symptom                                    | Likely cause                        | Fix                                                           |
| ------------------------------------------ | ----------------------------------- | ------------------------------------------------------------- |
| All tools fail                             | Server auth expired                 | Re-authenticate at mcp.zapier.com                             |
| One app fails, others work                 | App-level auth expired              | Re-connect that specific app                                  |
| Tool not found / unavailable               | Action not configured               | Agentic: `discover_zapier_actions` + `enable_zapier_action`. Classic: direct user to `get_configuration_url` to add it |
| "invalid params"                           | Wrong fields or format              | Check the tool's parameter schema                             |
| Results are empty but expected data exists | Search too narrow or wrong field    | Broaden the search or check field names                       |
| Timeout on execute                         | Server overloaded or action is slow | Retry once, then report if persistent                         |
| "rate limit exceeded"                      | Too many calls                      | Space out requests, wait 30 seconds                           |
| Works in one project, fails in another     | Project-level vs global config      | Check both project-level and global MCP config for the client |

4. **Report findings:**

"Here's what I found:

- **Connection**: OK (server responding)
- **Actions**: 14 tools available across 5 apps
- **Auth issue**: Gmail connection expired. You need to re-authenticate Gmail at mcp.zapier.com.
- **Recommendation**: [direct link or specific instruction]"

5. If the fix requires user action (re-auth, config change), provide the specific link or instruction. If it's something the AI can fix (adjust parameters, try a different tool), offer to do it.

## General notes

- Always check available Zapier MCP tools as the first diagnostic step in any mode. On Agentic, this means calling `list_enabled_zapier_actions`. On Classic, this means inspecting the available tool names.
- Don't dump raw error messages. Translate them into plain language.
- If a problem is beyond what the skill can diagnose (server-side bug, API outage), say so and suggest checking [status.zapier.com](https://status.zapier.com) or contacting support.
