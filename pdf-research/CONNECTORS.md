# Connectors

## Local MCP Server

This plugin uses a **local MCP server** instead of a remote connector.
The PDF server runs on your machine via `npx`.

| Category | Server | How it runs |
|----------|--------|-------------|
| PDF viewer | `@modelcontextprotocol/server-pdf` | Local stdio via `npx` (auto-installed) |

### Requirements
- Node.js >= 18
- Internet access for remote PDFs (arXiv, bioRxiv, etc.)
- No API keys or authentication needed
