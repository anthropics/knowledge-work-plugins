# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~e-signature` might mean Signeasy, DocuSign, or any other e-signature provider with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (e-signature, cloud storage, chat, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| E-signature | `~~e-signature` | [Signeasy](https://signeasy.com) | DocuSign, Adobe Sign |
