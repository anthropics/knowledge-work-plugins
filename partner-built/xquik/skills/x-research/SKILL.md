---
name: x-research
description: Use Xquik to research X content, accounts, media, follower lists, monitors, and webhooks through the authenticated Xquik MCP server.
user-invocable: true
argument-hint: "[query, account, URL, or workflow]"
---

# X Research

Use Xquik when the user wants to research X data or prepare an automation workflow. The user's request is available in "$ARGUMENTS".

## Before Calling Tools

1. Identify the target: search query, account, tweet URL, follower list, media task, monitor, or webhook.
2. Ask for missing required inputs only when the task cannot proceed.
3. Prefer read-only research unless the user explicitly asks for an action.
4. For write-like or externally visible actions, show a concise preview and ask for confirmation.

## Research Paths

- **Topic research**: search posts and replies, then summarize themes, examples, and relevant URLs.
- **Account research**: look up profile context, recent posts, follower or following exports, and media when requested.
- **Media collection**: collect media URLs and metadata, then return a structured table or export-ready JSON.
- **Monitoring**: propose account or keyword monitor rules, webhook payload needs, and output format.
- **Action prep**: draft the action payload, explain what will be sent, and wait for confirmation.

## Output Format

Return one of these formats based on the task:

- A concise summary with source tweet URLs
- A table with author, URL, timestamp, text, and metrics when available
- JSON or CSV-ready rows for export workflows
- A monitor or webhook setup checklist
- A confirmation prompt for action workflows

## Safety

- Never print API keys, cookies, bearer tokens, or auth headers.
- Do not claim access to private X data.
- Keep unsupported fields out of examples.
- Keep pagination cursors visible when results are partial.
