# Create a Zoom Doc

Use the dedicated `zoom-docs-mcp` server for Zoom Docs creation and retrieval.
The official documented docs tools are `create_file_with_content` and `get_file_content`.

## Required Scope

- `docs:write:import`

## Basic Flow

### Step 1: Gather the source content

If the source is meeting content, first use the current Zoom MCP retrieval tools.

```text
search_meetings
  q: "Q1 planning"
  from: "2026-03-01"
  to: "2026-03-06"
```

```text
get_meeting_assets
  meetingId: "MEETING_ID_OR_UUID"
```

### Step 2: Create the Zoom Doc

```text
create_file_with_content
  file_name: "Q1 Planning — Action Items"
  content: "# Action Items\n\n- Owner: ..."
```

Optional parameter:
- `parent_id` to place the document under a specific folder or parent object

## Verified Result Shape

Successful calls return:
- `file_id`
- `file_link`

Expect clients to expose at least the created file ID, and in practice often a direct Docs link.
Always parse the actual response you receive from the MCP client.

## Example Prompts

- "Create a Zoom Doc with the action items from today's planning meeting."
- "Search for the product review and publish the recap as a Zoom Doc."
- "Turn these Markdown notes into a Zoom Doc."
