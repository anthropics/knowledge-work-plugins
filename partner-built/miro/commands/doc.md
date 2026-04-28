---
description: Create a document (Google Docs-style) on a Miro board
argument-hint: "[board-url] [content]"
---

# Create Document on Miro Board

Create a markdown-formatted document on the specified Miro board.

## Arguments

Parse the user's input to extract:
1. **board-url** (required): Miro board URL
2. **content** (optional): Document content or topic to write about

## Supported Markdown

The document supports:
- `# Heading 1` through `###### Heading 6`
- `**bold**` and `*italic*`
- `- unordered lists` and `1. ordered lists`
- `[link text](url)`

**Not supported:** Code blocks, tables, images, horizontal rules

## Workflow

1. If board URL is missing, ask the user for it
2. If content is provided:
   - If it's actual document content, use it directly
   - If it's a topic/request, generate appropriate document content
3. If content is missing, ask what document they want to create
4. Call `doc_create` with the board URL and the markdown content.
5. Report success with a link to the board

## Examples

**User input:** `/miro:doc https://miro.com/app/board/abc= # Meeting Notes\n\n## Attendees\n- Alice\n- Bob`

**Action:** Create document with the provided markdown content.

---

**User input:** `/miro:doc https://miro.com/app/board/abc= sprint planning notes template`

**Action:** Generate a sprint planning notes template document with appropriate sections.

---

**User input:** `/miro:doc https://miro.com/app/board/abc=`

**Action:** Ask the user what document they want to create.

## Document Templates

When generating content, consider these common document types:
- **Meeting notes** - Date, attendees, agenda, action items
- **Project brief** - Overview, goals, timeline, stakeholders
- **Sprint planning** - Sprint goal, backlog items, capacity
- **Retrospective** - What went well, improvements, action items
- **Decision log** - Context, options, decision, rationale
