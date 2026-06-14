# MIT Presentation Coach

Turn Claude into a presentation coach based on Patrick Winston's MIT method — helping you create memorable, clear, and persuasive talks.

## What it does

Automatically detects what you need and delivers it directly:

| Trigger | Output |
|---|---|
| "Help me start my talk" | Opening + training promise + first 60 seconds word-for-word |
| Attach a deck or paste slides | Slide audit against Winston's 10 crimes + redesign |
| "Make this idea memorable" | STAR framework: Symbol → Slogan → Surprise → Salient idea → Story |
| "Help me convince / sell / pitch" | Persuasion structure: Vision → Proof → 5-min opening → Contributions slide |
| "Explain this complex concept" | Physical prop design + 3-act story + verbal script |
| "Create my presentation" (default) | Full structure delivered immediately — no extra questions |

## Core rules (applied automatically)

- **No "thank you for having me"** openings — weak and forgettable
- **No jokes** at the start — the audience is not ready
- **Opening = training promise:** not "you'll learn X" but "you'll be able to do Y"
- **Font minimum 40pt** — no exceptions for body text
- **Final slide = "Contributions"** — never "Thank you" or "Questions?"
- **No laser pointer** — move to the screen instead

## Closing design step

After every delivery, asks: *"Which tool will you use to design these slides?"* Then generates the specific prompt or code to speed up creation in that tool (NotebookLM, PowerPoint, Canva, etc.).

## No external tools required

This skill works standalone with no MCP connections needed.
