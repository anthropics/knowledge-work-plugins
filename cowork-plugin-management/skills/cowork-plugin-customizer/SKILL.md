---
name: cowork-plugin-customizer
description: >
  Customize a Claude Code plugin for a specific organization's tools and workflows.
  Use when users want to customize a plugin — whether it's a generic template with placeholders or an already-configured plugin they want to tweak.
  Also use when users want to customize a specific part of a plugin (e.g., connectors, skill, commands, agents).
  This skill requires Cowork mode with mounted plugin directories and will not work in remote or standard CLI sessions.
compatibility: Requires Cowork desktop app environment with access to mounted plugin directories (mnt/.local-plugins, mnt/.plugins).
---

# Cowork Plugin Customization

Customize a plugin for a specific organization — either by setting up a generic plugin template for the first time, or by tweaking and refining an already-configured plugin.

> **Finding the plugin**: To find the plugin's source files, run `find mnt/.local-plugins mnt/.plugins -type d -name "*<plugin-name>*"` to locate the plugin directory, then read its files to understand its structure before making changes. If you cannot find the plugin directory, the user is likely running this conversation in a remote container. Abort and let them know: "Customizing plugins is currently only available in the desktop app's Cowork mode."

## Determining the Customization Mode

After locating the plugin, determine what kind of customization is needed:

**1. Scoped customization** — The user asked to customize a specific part of the plugin (e.g., "customize the connectors", "update the standup command", "change the ticket tool"). Read the plugin files to find the relevant section(s) and focus only on those. Do not scan the entire plugin or present unrelated customization items.

**2. Generic plugin setup** — The plugin contains `~~`-prefixed placeholders (check with `grep -rn '~~\w' /path/to/plugin --include='*.md' --include='*.json'`). These are customization points in a template that need to be replaced with real values (e.g., `~~Jira` → `Asana`, `~~your-team-channel` → `#engineering`).

**3. General customization** — The plugin is already configured (no `~~` placeholders or they've already been filled in) and the user wants to modify it. Read the plugin's files to understand its current configuration, then ask the user what they'd like to change.

> **Important**: Never change the name of the plugin or skill being customized. Do not rename directories, files, or the plugin/skill name fields.

> **Nontechnical output**: All user-facing output (todo list items, questions, summaries) must be written in plain, nontechnical language. Never mention `~~` prefixes, placeholders, or customization points to the user. Frame everything in terms of the plugin's capabilities and the organization's tools.

## Customization Workflow

### Phase 0: Gather User Intent (scoped and general customization only)

For **scoped customization** and **general customization** (not generic plugin setup), check whether the user provided free-form context alongside their request (e.g., "customize the standup command — we do async standups in #eng-updates every morning").

- **If the user provided context**: Record it and use it to pre-fill answers in Phase 3 — skip asking questions that the user already answered here.
- **If the user did not provide context**: Ask a single open-ended question using AskUserQuestion before proceeding. Tailor the question to what they asked to customize — e.g., "What changes do you have in mind for the brief command?" or "What would you like to change about how this plugin works?" Keep it short and specific to their request.

  Use their response (if any) as additional context throughout the remaining phases.

### Phase 1: Gather Context from Knowledge MCPs

Use company-internal knowledge MCPs to collect information relevant to the customization scope. See `references/search-strategies.md` for detailed query patterns by category.

**What to gather** (scope to what's relevant):
- Tool names and services the organization uses
- Organizational processes and workflows
- Team conventions (naming, statuses, estimation scales)
- Configuration values (workspace IDs, project names, team identifiers)

**Sources to search:**
1. **Chat/Slack MCPs** — tool mentions, integrations, workflow discussions
2. **Document MCPs** — onboarding docs, tool guides, setup instructions
3. **Email MCPs** — license notifications, admin emails, setup invitations

Record all findings for use in Phase 3.

### Phase 2: Create Todo List

Build a todo list of changes to make, scoped appropriately:

- **For scoped customization**: Only include items related to the specific section the user asked about.
- **For generic plugin setup**: Run `grep -rn '~~\w' /path/to/plugin --include='*.md' --include='*.json'` to find all placeholder customization points. Group them by theme.
- **For general customization**: Read the plugin files, understand the current config, and based on the user's request, identify what needs to change.

Use user-friendly descriptions that focus on the plugin's purpose:

- **Good**: "Learn how standup prep works at Company"
- **Bad**: "Replace placeholders in commands/standup-prep.md"

### Phase 3: Complete Todo Items

Work through each item using context from Phase 0 and Phase 1.

**If the user's free-form input (Phase 0) or knowledge MCPs (Phase 1) provided a clear answer**: Apply directly without confirmation.

**Otherwise**: Use AskUserQuestion. Don't assume "industry standard" defaults are correct — if neither the user's input nor knowledge MCPs provided a specific answer, ask. Note: AskUserQuestion always includes a Skip button and a free-text input box for custom answers, so do not include `None` or `Other` as options.

**Types of changes:**

1. **Placeholder replacements** (generic setup): `~~Jira` → `Asana`, `~~your-org-channel` → `#engineering`
2. **Content updates**: Modifying instructions, commands, workflows, or references to match the organization
3. **URL pattern updates**: `tickets.example.com/your-team/123` → `app.asana.com/0/PROJECT_ID/TASK_ID`
4. **Configuration values**: Workspace IDs, project names, team identifiers

If user doesn't know or skips, leave the value unchanged (or the `~~`-prefixed placeholder, for generic setup).

### Phase 4: Search for Useful MCPs

After customization items have been resolved, connect MCPs for any tools that were identified or changed. See `references/mcp-servers.md` for the full workflow, category-to-keywords mapping, and config file format.

For each tool identified during customization:
1. Search the registry: `search_mcp_registry(keywords=[...])` using category keywords from `references/mcp-servers.md`, or search for the specific tool name if already known
2. If unconnected: `suggest_connectors(directoryUuids=["chosen-uuid"])` — user completes auth
3. Update the plugin's MCP config file (check `plugin.json` for custom location, otherwise `.mcp.json` at root)

Collect all MCP results and present them together in the summary output (see below) — don't present MCPs one at a time during this phase.

**Note:** First-party integrations (Gmail, Google Calendar, Google Drive) are connected at the user level and don't need plugin `.mcp.json` entries.

## Packaging the Plugin

After all customizations are applied, package the plugin as a `.plugin` file for the user:

1. **Zip the plugin directory** (excluding `setup/` since it's no longer needed):
   ```bash
   cd /path/to/plugin && zip -r /tmp/plugin-name.plugin . -x "setup/*" && cp /tmp/plugin-name.plugin /path/to/outputs/plugin-name.plugin
   ```
2. **Present the file to the user** with the `.plugin` extension so they can install it directly. (Presenting the .plugin file will show to the user as a rich preview where they can look through the plugin files, and they can accept the customization by pressing a button.)

> **Important**: Always create the zip in `/tmp/` first, then copy to the outputs folder. Writing directly to the outputs folder may fail due to permissions and leave behind temporary files.

> **Naming**: Use the original plugin directory name for the `.plugin` file (e.g., if the plugin directory is `coder`, the output file should be `coder.plugin`). Do not rename the plugin or its files during customization — only replace placeholder values and update content.

## Summary Output

After customization, present the user with a summary of what was learned grouped by source. Always include the MCPs sections showing which MCPs were connected during setup and which ones the user should still connect:

```markdown
## From searching Slack
- You use Asana for project management
- Sprint cycles are 2 weeks

## From searching documents
- Story points use T-shirt sizes

## From your answers
- Ticket statuses are: Backlog, In Progress, In Review, Done
```

Then present the MCPs that were connected during setup and any that the user should still connect, with instructions on how to connect them.

If no knowledge MCPs were available in Phase 1, and the user had to answer at least one question manually, include a note at the end:
> By the way, connecting sources like Slack or Microsoft Teams would let me find answers automatically next time you customize a plugin.

## Additional Resources

- **`references/mcp-servers.md`** — MCP discovery workflow, category-to-keywords mapping, config file locations
- **`references/search-strategies.md`** — Knowledge MCP query patterns for finding tool names and org values
- **`examples/customized-mcp.json`** — Example fully configured `.mcp.json`
