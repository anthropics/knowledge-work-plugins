# Productivity — TF3 Configuration
See tf3-context.md for full company context, ClickUp list IDs, and Notion page IDs.
See rex-protocols.md for session log format and signal protocol.

## Tools
This plugin connects to TF3's stack only:
- **ClickUp** — all tasks (full details in the description). Never create Notion pages for tasks.
- **Notion** — session logs, briefs, specs, and knowledge.

## Skills
- `start` — initialize the task and memory systems and open the dashboard
- `update` — sync ClickUp tasks, read the Ops Note and Handoff Log, summarise what needs Paskal today

## Commands
- `/productivity:sweep` — replicate Rex's morning sweep on demand
- `/productivity:handoff` — write a Handoff Log entry
- `/productivity:log` — write a Session Log entry
- `/productivity:task` — create a ClickUp task in the correct list
- `/productivity:brief` — scaffold a Forge brief page in Notion
