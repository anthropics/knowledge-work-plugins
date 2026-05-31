---
description: TF3 morning sweep — prioritised brief from ClickUp + Notion on demand
---

# /sweep — TF3 Morning Sweep
Replicate Rex's morning sweep on demand.
1. Fetch open tasks via the ClickUp `clickup_filter_tasks` tool over spaces 90166324362 and 90166324354 and list 901614493497. The tool has no priority parameter, so filter client-side:
   - Keep only tasks whose priority is Urgent (1) or High (2).
   - Skip any task whose list name contains `[LEGACY]`.
   - Take the top 5 remaining.
2. Read the Session Log's recent entries: enumerate the child pages of Notion page 34f871f7633d815b8f2bf0dbbe6ed5df, take the 5 most recently updated, and read each one individually (do not fetch the parent page whole — it is too large).
3. Read pending entries from Notion page 364871f7633d81a5be74f181d076278c
4. Produce: today's date, top 3 priorities, pending handoffs, decisions needed
5. Ask: "Anything to add before I write the session log?"
