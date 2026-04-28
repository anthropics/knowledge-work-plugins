---
description: Create a diagram on a Miro board from a text description
argument-hint: "[board-url] [description]"
---

# Create Diagram on Miro Board

Create a diagram on the specified Miro board using the provided description.

## Arguments

Parse the user's input to extract:
1. **board-url** (required): Miro board URL (e.g., `https://miro.com/app/board/uXjVK123abc=/`)
2. **description** (required): What to diagram - can be natural language or Mermaid/PlantUML notation

## Diagram Types

Automatically detect or let the user specify:
- **flowchart** - Processes, workflows, decision trees
- **mindmap** - Hierarchical ideas, brainstorming structures
- **uml_class** - Class diagrams, OOP relationships
- **uml_sequence** - Sequence diagrams, component interactions
- **entity_relationship** - Database schemas, ER diagrams

## Workflow

1. If board URL is missing, ask the user for it
2. If description is missing or unclear, ask what they want to diagram
3. Determine the appropriate diagram type from the description (or ask if ambiguous)
4. Call `diagram_create` with the board URL, the diagram description, and optionally the diagram type if specified.
5. Report success with a link to the board

## Examples

**User input:** `/miro:diagram https://miro.com/app/board/abc= user login authentication flow`

**Action:** Create a flowchart showing the user login authentication process.

---

**User input:** `/miro:diagram https://miro.com/app/board/abc= database schema for e-commerce: users, products, orders, reviews`

**Action:** Create an entity-relationship diagram for the e-commerce database.

---

**User input:** `/miro:diagram https://miro.com/app/board/abc=`

**Action:** Ask the user what they want to diagram.

## Tips for Better Diagrams

When crafting the description:
- Be specific about elements and their relationships
- Mention flow direction if important (top-down, left-right)
- Include decision points and conditions
- Name the key components clearly

For complex diagrams, suggest using Mermaid notation for precise control.
