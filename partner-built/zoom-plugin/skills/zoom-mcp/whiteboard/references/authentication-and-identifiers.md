# Authentication and Identifiers — Whiteboard MCP

Guidance for `https://mcp-us.zoom.us/mcp/whiteboard/streamable` and
`https://mcp-us.zoom.us/mcp/whiteboard/sse`.

## Authentication Behavior

### User OAuth

User OAuth with Whiteboard scopes was the verified working path for:

- `list_whiteboards`
- `get_a_whiteboard`

The required user OAuth scope set includes:
- `whiteboard:read:list_whiteboards`
- `whiteboard:read:whiteboard`

### Server-to-Server OAuth

S2S OAuth can reach the Whiteboard MCP gateway and complete protocol discovery through
`tools/list`, but Whiteboard read-tool execution must be validated separately for your app.

One possible runtime error shape when S2S lacks the expected scopes is:

```text
Invalid access token, does not contain scopes:[whiteboard:read:admin,whiteboard:read]
```

Protected-resource metadata for Whiteboard MCP advertised these supported scopes:
- `whiteboard:write:whiteboard`
- `whiteboard:read:list_whiteboards`
- `whiteboard:read:whiteboard`

Practical guidance:
- Use user OAuth first for Whiteboard MCP.
- Only rely on S2S after you have confirmed the app can mint and execute with the required Whiteboard scopes.

## Whiteboard ID Mapping

The MCP-facing `whiteboard_id` matches the URL segment after `/wb/db/`.

Example:

```text
https://us05whiteboard.zoom.us/wb/db/6iktP8hJT3e5qaCuwFuAGg/p/180968285929472
```

- Correct MCP `whiteboard_id`: `6iktP8hJT3e5qaCuwFuAGg`
- The numeric `/p/...` segment is not the Whiteboard MCP identifier.

## Response Shape

`get_a_whiteboard` returned a list-style payload containing the matched whiteboard rather than
an obviously single-object payload. Parse the response shape you actually receive from the live
server instead of assuming the tool name implies a unique-object response.
