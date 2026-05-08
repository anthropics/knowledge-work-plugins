# APIs vs MCP Routing

Decide whether to route a request to Zoom APIs, Zoom MCP, or both.

## Overview

Zoom APIs and Zoom MCP are complementary:

- Zoom APIs are best for deterministic system integrations.
- Zoom MCP is best for AI-driven tool-based workflows.
- Use both for enterprise AI systems that need a stable automation core and an adaptive AI layer.
- Zoom-hosted MCP follows a product-scoped server model; access is OAuth-scoped and governed.

## Decision Matrix

| Primary requirement | Route | Notes |
|---------------------|-------|-------|
| Deterministic automation, configuration, reporting, scheduled jobs, strict retries/error handling | **zoom-rest-api** | Direct control over requests, retries, and idempotency |
| AI interaction, dynamic tool discovery, AI Companion workflows, external AI interoperability | **zoom-mcp** | Agent chooses tools contextually through MCP |
| High-volume production automation plus AI assistant workflows | **zoom-rest-api + zoom-mcp** | Keep core actions in APIs; expose curated tool surfaces via MCP |

## Typical Routing Examples

| User request | Route |
|--------------|-------|
| "Create meetings nightly and sync metrics to BI" | **zoom-rest-api** |
| "Let my assistant search meeting content and fetch transcripts" | **zoom-mcp** |
| "Automate meeting lifecycle, then let agents answer questions from summaries" | **zoom-rest-api + zoom-mcp** |

## Chaining Patterns

### Pattern A: API-only deterministic backend

1. `zoom-oauth` for app auth/token lifecycle.
2. `zoom-rest-api` for create/read/update/reporting endpoints.
3. `zoom-webhooks` for async event processing if needed.

### Pattern B: MCP-first AI tool workflows

1. `zoom-oauth` for user OAuth token required by MCP server.
2. `zoom-mcp` for semantic meeting search, summaries, recordings/transcripts, and tool invocation.

### Pattern C: Hybrid enterprise AI architecture

1. `zoom-rest-api` handles provisioning, policy/configuration, and scheduled ingestion jobs.
2. `zoom-webhooks` or `zoom-websockets` handles event ingestion.
3. `zoom-mcp` exposes curated higher-level tools for AI Companion or external agents.

## MCP Fit Checklist (FAQ-Aligned)

Use `zoom-mcp` when you are:

- Building custom tools for AI models.
- Creating data integration services for AI assistants.
- Developing specialized assistants that need tool discovery.
- Extending AI capabilities with external services via MCP.
- Building enterprise AI solutions that need interoperable agent tooling.

## MCP Client and Transport Constraints

- Zoom remote MCP server is consumed over Streamable HTTP/SSE.
- Typical supported MCP clients include Claude and VS Code MCP-capable tooling.
- A local stdio mode may be available depending on client setup, but remote Zoom MCP routing assumes HTTP/SSE transport.
- Endpoint model is shared by instance/cluster; do not assume per-customer dedicated endpoint generation.
- MCP server surfaces can be product-scoped (for example Meetings, Team Chat, Whiteboard). Route by product when those surfaces are available.

## Routing Guardrails

- Do not route deterministic backend automation to MCP only.
- Do not route AI-agent tool discovery tasks to REST only.
- Prefer hybrid routing when both deterministic backend operations and AI-driven interactions are required.

## Related Skills

- [zoom-rest-api](../../rest-api/SKILL.md)
- [zoom-mcp](../../zoom-mcp/SKILL.md)
- [zoom-oauth](../../oauth/SKILL.md)
- [zoom-webhooks](../../webhooks/SKILL.md)
- [zoom-websockets](../../websockets/SKILL.md)

## Source

- https://developers.zoom.us/docs/mcp/library/resources/apis-vs-mcp/
