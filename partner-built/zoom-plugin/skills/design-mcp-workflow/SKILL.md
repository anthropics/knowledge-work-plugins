---
name: design-mcp-workflow
description: Design a Zoom MCP workflow for Claude. Use when deciding whether Zoom MCP fits a task, when planning tool-based AI workflows, or when separating MCP responsibilities from REST API responsibilities.
user-invocable: false
---

# Design MCP Workflow

Use this skill when the user wants Claude or another MCP-capable client to interact with Zoom via tool calls instead of only deterministic API code.

## Covers

- MCP fit assessment
- REST API vs MCP boundaries
- Hybrid architectures
- Connector expectations
- Whiteboard-specific MCP routing

## Workflow

1. Decide whether the problem is agentic tooling, deterministic automation, or both.
2. Route MCP-only tasks to [zoom-mcp](../zoom-mcp/SKILL.md).
3. Route hybrid tasks to both [zoom-mcp](../zoom-mcp/SKILL.md) and [rest-api](../rest-api/SKILL.md).
4. If Whiteboard is central, route to [zoom-mcp/whiteboard](../zoom-mcp/whiteboard/SKILL.md).
5. Call out transport, auth, and client capability assumptions explicitly.

## Common Mistakes

- Using MCP for deterministic backend jobs that should stay in REST
- Treating MCP as a replacement for all API design
- Ignoring client transport support and auth requirements
