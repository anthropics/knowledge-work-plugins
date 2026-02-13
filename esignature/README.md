# E-Signature Plugin

An e-signature management plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Track pending documents, send reminders, search across your signature history, and manage templates — all from a single interface.

## Installation

```
claude plugins add knowledge-work-plugins/esignature
```

## Quick Start

### 1. Install the plugin

```
claude plugins add knowledge-work-plugins/esignature
```

### 2. Connect your e-signature tool

The plugin comes pre-configured with [Signeasy](https://signeasy.com). See [CONNECTORS.md](CONNECTORS.md) for the full list of supported options.

### 3. Check your signature dashboard

```
/signature-status
```

## Commands

### `/signature-status` -- Signature Dashboard

Get a real-time overview of your e-signature pipeline — documents pending your signature, documents awaiting others, recently signed, and expired requests.

```
/signature-status
```

### `/send-reminder` -- Send Signature Reminders

Send reminders to signers for pending documents. Works for individual documents or in bulk.

```
/send-reminder [document name]
/send-reminder all
```

### `/document-search` -- Search Documents

Search across all documents — signed, pending, expired, and templates — by name, signer, or status.

```
/document-search [query]
```

## Skills

| Skill | Description |
|-------|-------------|
| `document-tracking` | Monitor document lifecycle, detect stale requests, track signer status |
| `signature-workflows` | Sending best practices, reminder strategy, template management, troubleshooting |

## Example Workflows

### Morning Check-In

1. Run `/signature-status` to see your dashboard
2. Sign any documents pending your signature
3. Send reminders for documents that have been pending for others for more than 3 days
4. Resend any expired documents that are still needed

### Following Up on a Contract

1. Run `/document-search Acme NDA` to find the document
2. See who has signed and who hasn't
3. Run `/send-reminder Acme NDA` to nudge pending signers

### Bulk Reminder

1. Run `/send-reminder all` to see all pending documents
2. Confirm which documents to send reminders for
3. Reminders are sent to all pending signers

## MCP Integration

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

The plugin connects to your e-signature tool through MCP (Model Context Protocol):

| Category | Tool | Capabilities |
|----------|------|-------------|
| E-signature | [Signeasy](https://signeasy.com) | Track pending/signed/expired documents, send reminders, cancel requests, search signers, manage templates, view account summary |

### Available Operations

| Operation | Description |
|-----------|-------------|
| List pending documents | See all documents waiting for signatures |
| Pending for me | Documents that need your signature |
| Pending for others | Documents you sent that are waiting on recipients |
| List signed documents | All completed documents |
| Recently signed | Documents signed in the past N days |
| List expired | Documents that lapsed without being signed |
| Get signer details | See individual signer status for any document |
| Send reminder | Nudge signers on pending documents |
| Cancel request | Void a pending signature request |
| List templates | See all available document templates |
| Account summary | Document counts, subscription status, recent activity |

## File Structure

```
esignature/
├── .claude-plugin/plugin.json
├── .mcp.json
├── README.md
├── CONNECTORS.md
├── commands/
│   ├── signature-status.md
│   ├── send-reminder.md
│   └── document-search.md
└── skills/
    ├── document-tracking/SKILL.md
    └── signature-workflows/SKILL.md
```
