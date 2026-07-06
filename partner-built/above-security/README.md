# Above Security Plugin

Connects Claude to the [Above Security](https://above.security) MCP server for insider threat
and identity investigations — surface incidents, investigate identities, and validate findings
against telemetry directly from Claude.

## Setup

The MCP server is hosted and authenticates via OAuth — no local installation required. On first
use Claude signs you in via your Above Security account (OAuth 2.1 + PKCE). Client registration is
dynamic, so there's nothing to configure.

## Connector

| Server | URL | Transport | Auth |
|--------|-----|-----------|------|
| `above-security` | `https://mcp.app.abovesec.com/mcp` | HTTP | OAuth (dynamic registration) |

> **EU data residency:** EU-residency customers connect to `https://mcp.app.eu.abovesec.com/mcp`
> instead. This listing points at the US resource server.
