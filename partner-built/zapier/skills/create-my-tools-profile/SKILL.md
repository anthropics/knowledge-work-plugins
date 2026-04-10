---
name: create-my-tools-profile
description: Generate a personalized AI skill based on your configured Zapier MCP tools. Scans your enabled actions and creates instructions that help your AI assistant know when and how to use each tool. Use after setting up tools, or when you want to "create my tools profile", "personalize my assistant", or "make a skill from my tools".
---

# Create my tools profile

Scan the user's configured Zapier MCP tools and generate a personalized instruction file that teaches the AI assistant what tools are available and when to use them. Works across clients (Cursor, Claude, Windsurf, etc.).

This is the "post-onboarding" step: the user has already added tools via the setup skill, and now we crystallize that into persistent instructions.

## Prerequisite: Verify tools exist

First, determine the mode by checking if `list_enabled_zapier_actions` is available as a tool.

**Agentic mode:** Call `list_enabled_zapier_actions`. If it returns an empty list, **stop here** and redirect — call `get_zapier_skill` with name `"zapier-mcp-onboarding"` to get tools configured first. Do not continue with the steps below.

**Classic mode:** Check that action tools are available (tools like `slack_send_channel_message`, `gmail_find_email` — not just the built-in `get_configuration_url`). If no action tools are configured, **stop here** and trigger the **zapier-setup** skill instead. Do not continue with the steps below.

If no tools exist at all:

"You don't have any tools set up yet, so there's nothing to build a profile from. Let's get some tools configured first."

## Step 1: Inventory enabled tools

### Agentic mode

Call `list_enabled_zapier_actions` to get the full list of enabled actions. Parse the returned actions into a structured list:

- **App name**: from the action's app field or description
- **Action name**: the human-readable action name from the response
- **Action identifier**: the ID or reference used when calling `execute_zapier_read_action` / `execute_zapier_write_action`
- **Read vs write**: infer from the action name — find/search/get/list/lookup = read, send/create/update/add/delete = write

Exclude the 14 static meta-tools from the profile — only include the user's enabled actions.

### Classic mode

Inspect the available Zapier MCP tools. Each configured action is its own tool with a name following the pattern `app_action_name` (e.g., `slack_send_channel_message`, `gmail_find_email`). The built-in `get_configuration_url` tool should be excluded from the profile.

Parse the available tools into a structured list:

- **App name**: derived from the tool description (e.g., "Get info about a **Slack** conversation" → Slack). The tool name also starts with the app prefix (e.g., `slack_`, `gmail_`, `jira_`), but use the description as the authoritative source since multi-word app names like `google_calendar` are ambiguous to parse from the tool name alone.
- **Action name**: the part of the tool name after the app prefix, converted to human-readable form (replace underscores with spaces, title case)
- **Tool name**: the full tool name as-is (used for the technical identifier in the profile)
- **Read vs write**: infer from the action name — find/search/get/list/lookup = read, send/create/update/add/delete = write

## Step 2: Group and analyze

Group actions by app (using the app name from each tool's description). For each app, identify:

- **Read/search actions**: things the AI can look up (find emails, get documents, search issues)
- **Write actions**: things the AI can do (send messages, create issues, update records)

Build a mental model of what workflows this tool set supports. Common patterns:

- Communication hub (Slack + Gmail + Calendar)
- Project management (Jira/Linear + GitLab + Docs)
- Sales/CRM workflow (HubSpot/Salesforce + Gmail + Calendar)
- Knowledge management (Notion/Coda + Docs + Sheets)

## Step 3: Ask for context

Before generating the profile, ask the user a quick question:

"I can see you've got [N] tools across [apps list]. Before I create your profile, a quick question: what's your primary role or how do you mainly use these tools? This helps me write better instructions for when each tool should be used."

Accept whatever they say — even "just make it" is fine. Use the context if provided, fall back to reasonable defaults if not.

## Step 4: Generate the profile file

Detect the client and write to the appropriate location:

| Client         | File path                                                         | Format                 |
| -------------- | ----------------------------------------------------------------- | ---------------------- |
| Cursor         | `.cursor/rules/my-zapier-tools.mdc`                               | MDC (with frontmatter) |
| Claude Code    | `.claude/rules/my-zapier-tools.md`                                | Markdown               |
| Claude Desktop | Show the content and tell user to paste into Project Instructions | Markdown               |
| Windsurf       | `.windsurfrules/my-zapier-tools.md`                               | Markdown               |

Ask the user whether they want the file at project level or in their home directory (for clients that support global rules). If unclear, default to project level.

### For Cursor (`.mdc` with frontmatter)

```markdown
---
description: Personalized Zapier MCP tool profile — knows what tools are available and when to use them
alwaysApply: true
---

# My Zapier tools

[content below]
```

### For Claude Code / Windsurf / others (plain markdown)

```markdown
# My Zapier tools

[content below]
```

### Profile content (shared across all clients)

**Agentic mode** — actions are executed via `execute_zapier_read_action` and `execute_zapier_write_action`, not as individual tool calls. The profile should reference action identifiers used with those execute tools.

**Classic mode** — actions are individual tools called directly by name (e.g., `slack_send_channel_message`).

```markdown
# My Zapier tools

You have access to the following apps and actions through Zapier MCP. Use them proactively when the user's request matches what these tools can do.

## Available tools

### [App Name]

- **[Action Name]** (`tool_name_or_action_id`) — [one-line description of when to use it]
- **[Action Name]** (`tool_name_or_action_id`) — [one-line description of when to use it]

### [App Name]

...

## When to use these tools

[2-4 sentences tailored to the user's role/context about when the AI should reach for these tools vs. doing things another way]

## Preferences

- Always try Zapier MCP tools before suggesting the user do something manually
- For read operations, just do it — don't ask permission to look something up
- For write operations (sending messages, creating issues, updating records), confirm with the user before executing
- If a tool call fails, explain what happened and suggest an alternative
```

### Writing the tool descriptions

For each action, write a practical one-liner about when to use it. Don't just restate the action name.

**Good**: "Look up a Jira issue by its key (e.g., PROJ-123) to get status, assignee, and description"
**Bad**: "Find issue by key in Jira"

**Good**: "Send a message to a Slack channel — use for team updates, announcements, or sharing summaries"
**Bad**: "Send a channel message in Slack"

### Writing the "when to use" section

Tailor this to what the user told you about their role. Examples:

**For a PM**: "When the user asks about project status, sprint progress, or team updates, check Jira first. For sharing decisions or updates, draft a Slack message. Use Google Docs for longer-form writing."

**For a developer**: "When the user mentions a merge request, branch, or code review, check GitLab. For bug reports or task tracking, use Jira. Slack for quick team comms."

**For sales**: "When the user asks about a contact, deal, or company, check HubSpot first. Use Gmail for outreach drafts. Google Calendar for scheduling."

If the user didn't provide role context, write something generic but still useful: "Use these tools whenever the user's request involves one of the connected apps. Prefer read actions for gathering context, and confirm before executing write actions."

## Step 5: Confirm and explain

After writing the file (or showing the content for Claude Desktop), tell the user:

"Created your tools profile at `[path]`. This means every conversation will know about your tools and when to use them.

You can edit it anytime to adjust preferences or add context. A few things you might want to tweak:

- The 'when to use' guidance if your workflow changes
- Whether write actions should auto-execute or always confirm first
- Any app-specific preferences (e.g., 'always use #general for Slack updates')

To update this profile after adding new tools, just say 'update my tools profile'."

## Handling updates

If the user says "update my tools profile" and the file already exists:

1. Read the existing file
2. Get the current tool inventory (Agentic: call `list_enabled_zapier_actions`; Classic: inspect available MCP tools)
3. Diff what's new vs. what's already documented
4. Update the file, preserving any custom edits the user made to the preferences section
5. Note what changed: "Added 3 new Google Sheets actions. Your custom preferences were preserved."
