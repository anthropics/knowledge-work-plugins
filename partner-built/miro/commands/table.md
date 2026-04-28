---
description: Create a table on a Miro board with specified columns
argument-hint: "[board-url] [table-name]"
---

# Create Table on Miro Board

Create a structured table with text and select columns on the specified Miro board.

## Arguments

Parse the user's input to extract:
1. **board-url** (required): Miro board URL
2. **table-name** (optional): Name/title for the table

## Column Types

- **text** - Free-form text entry
- **select** - Dropdown with predefined options (each option needs a label and hex color)

## Workflow

1. If board URL is missing, ask the user for it
2. If table name is missing, ask what kind of table they want
3. Based on the table purpose, suggest appropriate columns using AskUserQuestion:
   - Propose a default column structure
   - Let user customize or accept defaults
4. Call `table_create` with the board URL, table name, and column definitions.
5. Report success and offer to add initial rows

## Common Table Templates

### Task Tracker
Text columns for Task and Assignee. Select columns for Status (To Do / In Progress / Done) and Priority (Low / Medium / High) with traffic-light colors.

### Decision Log
Text columns for Decision, Date, and Owner. Select column for Status (Proposed / Approved / Rejected).

### Risk Register
Text columns for Risk and Mitigation. Select columns for Impact (Low / Medium / High) and Likelihood (Unlikely / Possible / Likely) with traffic-light colors.

## Examples

**User input:** `/miro:table https://miro.com/app/board/abc= Project Tasks`

**Action:** Create a task tracking table with Task, Assignee, Status, and Priority columns.

---

**User input:** `/miro:table https://miro.com/app/board/abc=`

**Action:** Ask what kind of table the user wants to create, then suggest appropriate columns.

## Color Reference

| Color | Hex | Typical Use |
|-------|-----|-------------|
| Gray | #E0E0E0 | Not started, backlog |
| Yellow | #FFD700 | In progress |
| Green | #00FF00 | Done, approved |
| Light Green | #90EE90 | Low priority/risk |
| Orange | #FFA500 | Medium priority/risk |
| Red/Tomato | #FF6347 | High priority, blocked |
