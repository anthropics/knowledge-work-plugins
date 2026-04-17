---
description: List and explore items on a Miro board
argument-hint: "[board-url] [item-type?]"
---

# Browse Miro Board Contents

List and explore items on a Miro board with optional filtering.

## Arguments

Parse the user's input to extract:
1. **board-url** (required): Miro board URL
2. **item-type** (optional): Type of items to filter

## Item Types

- `frame` - Frames/containers
- `sticky_note` - Sticky notes
- `card` - Card widgets
- `shape` - Shapes
- `text` - Text elements
- `image` - Images
- `document` - Documents
- `embed` - Embedded content

## Workflow

1. If board URL is missing, ask the user for it
2. Call `board_list_items` with the board URL, requesting up to 50 items. Apply type filter if the user specified one. If the URL contains a moveToWidget parameter, scope to that container.
3. Present the items in a readable format:
   - Show item type, ID, and relevant content/title
   - Group by type if showing mixed items
4. If there are more items (cursor returned), offer to load more
5. Offer follow-up actions:
   - Focus on a specific frame
   - Filter by a different type
   - Get details about a specific item

## Examples

**User input:** `/miro:browse https://miro.com/app/board/abc=`

**Action:** List all items on the board (first page).

---

**User input:** `/miro:browse https://miro.com/app/board/abc= frame`

**Action:** List only frames on the board.

---

**User input:** `/miro:browse https://miro.com/app/board/abc=/?moveToWidget=123`

**Action:** List items within the specified frame/container.

## Output Format

Present items clearly:

```
## Frames (3 found)
- **Design Specs** (ID: 3458764612345)
- **User Flows** (ID: 3458764612346)
- **Component Library** (ID: 3458764612347)

## Sticky Notes (12 found)
- "User feedback: navigation confusing" (ID: 3458764612350)
- "TODO: Update color palette" (ID: 3458764612351)
...
```

## Follow-up Actions

After listing items, suggest relevant next steps:
- "Would you like to explore items inside a specific frame?"
- "Should I get the content/summary of this board?"
- "Want to see images or download any specific item?"
