# Error Codes — Zoom MCP Server

Errors can surface from the MCP protocol layer or from the underlying Zoom API-style behavior
behind a tool call.

## MCP Protocol Errors

| Code | Message | Cause | Fix |
|------|---------|-------|-----|
| `-32001` | `Access token is required` | Missing Authorization header because the bundled connector has no token | Set `ZOOM_MCP_ACCESS_TOKEN`, then restart Claude Code or re-enable the plugin |
| `-32001` | `Invalid access token` | Expired, revoked, malformed, or missing required scopes | Refresh the token and verify the MCP-specific scopes |
| `-32602` | `Can not found tool: ... in this MCP Server` | Wrong tool name or wrong MCP server surface | Re-run `tools/list` and use the current live tool names for that endpoint |
| `-32603` | `Call handle error` | Missing required parameter or server-side call handling failure | Re-check required arguments against the live schema and retry |

## Exact Scope Errors Observed in Testing

| Tool | Exact missing-scope error |
|------|---------------------------|
| `search_meetings` | `meeting:read:search` |
| `get_meeting_assets` | `meeting:read:assets` or `meeting:read:assets:admin` |
| `recordings_list` | `cloud_recording:read:list_user_recordings` or admin/master variants |
| `get_recording_resource` | `cloud_recording:read:content` |
| `create_file_with_content` | `docs:write:import` worked with user OAuth; S2S runtime error surfaced `docs_import:write` aliasing |
| `get_file_content` | `docs:read:export` |

## Recording and Transcript Failures

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `get_recording_resource` fails on scope | Missing `cloud_recording:read:content` | Add the scope and mint a new token |
| Recording search/list works but transcript-capable retrieval fails | Token has list scope but not content scope | Add `cloud_recording:read:content` |
| Returned resource URL gives `401` | Bearer token not included on the follow-up fetch | Include the same bearer token on the direct request |

## Upstream API Validation Errors

Some tool calls can succeed at the MCP protocol layer but surface a downstream Zoom API
validation error in the result payload.

Common downstream validation response:

| Tool | Error shape | Cause | Fix |
|------|-------------|-------|-----|
| `create_file_with_content` | `Upstream API returned error status code: 400 ... "message":"invalid param"` | Invalid parameter value such as a bogus `parent_id` | Fix the argument value and retry |

## Whiteboard Server Split

The Zoom MCP server (`mcp-us.zoom.us/mcp/zoom/streamable`), the Zoom Docs MCP server
(`mcp.zoom.us/mcp/docs/streamable`), and the Whiteboard MCP server
(`mcp-us.zoom.us/mcp/whiteboard/streamable`) are separate surfaces.

Use the dedicated Whiteboard MCP skill for Whiteboard-specific auth, scopes, and identifier mapping:
- [../whiteboard/SKILL.md](../whiteboard/SKILL.md)

## Debugging Checklist

1. Confirm the client can discover the current MCP tool list through `tools/list`.
2. Confirm the bearer token is fresh.
3. Verify the exact MCP-specific scopes, not just adjacent REST scopes.
4. Re-discover the target meeting or recording instead of reusing guessed IDs.
