---
description: Generate documentation or summary from a Miro board
argument-hint: "[board-url] [doc-type?]"
---

# Summarize Miro Board Content

Extract structured documentation from a Miro board's visual content.

## Arguments

Parse the user's input to extract:
1. **board-url** (required): Miro board URL
2. **doc-type** (optional): Type of documentation to generate

## Workflow

1. If board URL is missing, ask the user for it
2. Call `context_explore` to discover high-level items on the board:
   - Returns frames, documents, prototypes, tables, and diagrams with their URLs
3. Present the discovered items to the user
4. For specific items the user wants to explore:
   - Call `context_get` with the item URL (includes moveToWidget parameter)
   - Returns detailed content based on item type (HTML for docs, summaries for frames, etc.)
5. Present the extracted documentation to the user

## Examples

**User input:** `/miro:summarize https://miro.com/app/board/abc=`

**Action:** Use context_explore to discover board contents, then offer to get details on specific items.

---

**User input:** `/miro:summarize https://miro.com/app/board/abc=/?moveToWidget=123`

**Action:** Use context_get to extract content from the specific item indicated in the URL.

## Tips

- **Start with context_explore** - Discover what's on the board before diving into details
- **Use moveToWidget URLs** - Get detailed content from specific items using context_get
- **Prototypes** - Images are returned as Miro URLs that can be downloaded with `image_get_url`
