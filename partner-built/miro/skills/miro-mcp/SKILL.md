---
name: miro-mcp
description: This skill teaches how to use Miro MCP tools effectively for creating diagrams, documents, tables, and extracting context from Miro boards. Use when the user asks about Miro capabilities, wants to create content on Miro boards, or needs to work with Miro board data.
---

# Using Miro with Claude Code

## What is Miro MCP?

Miro MCP (Model Context Protocol) enables Claude to interact directly with Miro boards. Create diagrams, documents, and tables; read board content; and extract structured documentation from visual designs.

## Available Tools

### Content Creation
- **`diagram_get_dsl`** - Get the DSL format specification before creating diagrams
- **`diagram_create`** - Generate diagrams from DSL text descriptions
- **`doc_create`** - Create markdown documents on boards
- **`table_create`** - Create tables with text and select columns
- **`table_sync_rows`** - Add or update table rows

### Content Reading
- **`board_list_items`** - List items on a board with filtering by type or container
- **`context_explore`** - Discover high-level board contents (frames, documents, prototypes, tables, diagrams)
- **`context_get`** - Extract detailed text context from specific board items
- **`table_list_rows`** - Read table data with column-based filtering
- **`image_get_data`** - Get image content from boards
- **`image_get_url`** - Get download URL for an image

### Document Editing
- **`doc_get`** - Read document content and version
- **`doc_update`** - Edit document using find-and-replace

## Board URLs and IDs

Miro tools accept board URLs directly. Extract board_id and item_id automatically from URLs like:
- `https://miro.com/app/board/uXjVK123abc=/` - Board URL
- `https://miro.com/app/board/uXjVK123abc=/?moveToWidget=3458764612345` - URL with item focus

When a URL includes `moveToWidget` or `focusWidget` parameters, the item_id is extracted automatically.

## Creating Diagrams

Use `diagram_create` to create visual diagrams from text descriptions.

### Supported Diagram Types
- **flowchart** - Process flows, workflows, decision trees
- **mindmap** - Hierarchical ideas, brainstorming
- **uml_class** - Class structures, inheritance relationships
- **uml_sequence** - Interactions between components over time
- **entity_relationship** - Database schemas, data models

### Description Formats

Natural language works well:
```
User registration flow: start -> enter email -> validate email ->
send verification -> user confirms -> create account -> redirect to dashboard
```

Mermaid notation for precise control:
```
flowchart TD
    A[Start] --> B{Valid Email?}
    B -->|Yes| C[Send Verification]
    B -->|No| D[Show Error]
    C --> E[Wait for Confirm]
    E --> F[Create Account]
```

### Positioning Items on the Board

Board coordinates use a Cartesian system with center at `(0, 0)`. Positive X goes right, positive Y goes down.

**Spacing recommendations:**
- Diagrams: 2000-3000 units apart
- Documents: 500-1000 units apart
- Tables: 1500-2000 units apart

### Placing in Frames

Set `parent_id` to a frame ID to place content inside that frame.

## Creating Documents

Use `doc_create` to create Google Docs-style documents on boards.

### Supported Markdown
- Headings: `# H1` through `###### H6`
- Bold: `**text**`
- Italic: `*text*`
- Unordered lists: `- item`
- Ordered lists: `1. item`
- Links: `[text](url)`

### Example Document

```markdown
# Sprint Planning - Week 12

## Goals
- Complete user authentication module
- Fix critical bugs from QA

## Team Assignments
1. **Alice** - Auth backend
2. **Bob** - Frontend integration
3. **Carol** - Bug fixes

## Resources
- [Design specs](https://example.com/specs)
- [API documentation](https://example.com/api)
```

## Working with Tables

### Creating Tables

Use `table_create` to create tables with typed columns. Supports two column types: **text** for free-form entry and **select** for dropdowns with predefined color-coded options.

### Adding and Updating Rows

Use `table_sync_rows` to add or update table data. Set `key_column` to match existing rows for upsert behavior — matching rows are updated, non-matching rows are inserted as new.

### Reading Table Data

Use `table_list_rows` to read table contents. Filter by column value using `ColumnName=Value` format.

## Extracting Board Content

### Discovering Board Contents

Use `context_explore` to get a high-level view of what's on a board — returns frames, documents, prototypes, tables, and diagrams with their URLs and titles.

### Getting Item Details

Use `context_get` to extract detailed content from specific items:

| Item Type | Returns |
|-----------|---------|
| Documents | HTML markup of the document content |
| Prototype screens | HTML markup representing the UI/layout |
| Prototype containers | AI-generated map of all screens with navigation flow |
| Frames | AI-generated summary of frame contents |
| Tables | Formatted table data |
| Diagrams | AI-generated description and analysis |

### Workflow

1. Call `context_explore` to discover board contents
2. Identify items of interest from the results
3. Call `context_get` with specific item URLs (with moveToWidget parameter)

## Browsing Board Items

Use `board_list_items` to explore board contents. Filter by item type (frame, sticky_note, card, shape, text, image, document, embed) or by container to list items within a specific frame.

## Best Practices

### For Diagrams
- Be specific about elements and relationships
- Specify flow direction (top-down, left-right)
- Include decision points and conditions
- Let AI auto-detect diagram type or specify explicitly

### For Documents
- Structure with clear headings
- Keep content focused and scannable
- Use lists for multiple items
- Include links to related resources

### For Tables
- Choose meaningful column names
- Use select columns for status/priority fields
- Define clear, distinct option colors
- Use key_column for idempotent updates

### For Context Extraction
- Start with `context_explore` to discover board contents
- Focus on specific frames when boards are large
- Use `context_get` with item URLs for detailed content

## Quick Reference

| Task | Tool |
|------|------|
| Get diagram DSL spec | `diagram_get_dsl` |
| Create diagram | `diagram_create` |
| Create document | `doc_create` |
| Read document | `doc_get` |
| Edit document | `doc_update` |
| Create table | `table_create` |
| Add/update table rows | `table_sync_rows` |
| Read table data | `table_list_rows` |
| Discover board contents | `context_explore` |
| Extract item details | `context_get` |
| List board items | `board_list_items` |
| Get image data | `image_get_data` |
| Get image URL | `image_get_url` |
