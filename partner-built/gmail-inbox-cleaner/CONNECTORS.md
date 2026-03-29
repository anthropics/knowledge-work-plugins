# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. This plugin is Gmail-specific by design, but references `~~browser` for any browser automation that may be needed.

## Connectors for this plugin

| Category | Placeholder | Included | Required? |
|----------|-------------|----------|-----------|
| Email | `~~email` | Gmail (via MCP) | Yes — core functionality |
| Browser | `~~browser` | Claude in Chrome | For unsubscribe clicks and bulk UI actions |

## Capability Tiers

The plugin degrades gracefully based on what's connected. `/gmail-prepare` reports exactly what's available before starting.

### Tier 1 — Gmail MCP only
- Inbox audit (counts, top senders by volume)
- Reading email subjects and bodies for classification
- Unread audit and flagging actionable emails
- Searching inbox and trash

**Not available**: Bulk delete, filter management, label creation, mark-as-read operations, unsubscribes requiring button clicks

### Tier 2 — Gmail MCP + Claude in Chrome
Everything in Tier 1, plus:
- Bulk delete via Gmail web UI (select all → trash by search)
- Unsubscribe button clicks on pages that require `isTrusted: true` events
- OAuth authorization flow (reading auth code from browser URL bar)

**Not available**: Filter management (create/delete), precise bulk label operations at scale

### Tier 3 — Gmail MCP + Claude in Chrome + Python Gmail API
Full capability:
- All Tier 1 and Tier 2 features
- Sender index building (batch metadata fetch — much faster than MCP search loops)
- Precise bulk operations via `batchModify` (1000 messages per call)
- Filter create, backup, audit, delete via `gmail.settings.basic` scope
- Label create and management
- Accurate trash search (MCP search does not reliably isolate trash)
- All script-based operations in `scripts/`

## Gmail MCP

Pre-configured in `.mcp.json`. Provides read access to Gmail:
- `gmail_get_profile` — account info and total message count
- `gmail_search_messages` — search inbox with query strings
- `gmail_read_message` / `gmail_read_thread` — read email content
- `gmail_list_labels` — list all Gmail labels

**Limitation**: The Gmail MCP is read-only and does not reliably isolate `in:trash` searches. Use Python API scripts for trash operations.

## Python Gmail API (Tier 3 Setup)

Requires:
1. A Google Cloud project with Gmail API enabled
2. An OAuth 2.0 client ID (download as `credentials.json`)
3. Running `scripts/oauth_setup.py` to generate a dual-scope token

The token needs two scopes:
- `gmail.modify` — message operations (trash, label, archive, mark read)
- `gmail.settings.basic` — filter and label management

See `scripts/oauth_setup.py` for the full setup flow. The standard local-server redirect does not work in this environment — the script uses a manual code-capture pattern via the browser URL bar.
