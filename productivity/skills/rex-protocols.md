# Rex Protocols — TF3 Operational Standards

## Morning Sweep Protocol
1. Fetch urgent + high priority open tasks from ClickUp spaces 90166324362 and 90166324354
2. Read Session Log (34f871f7633d815b8f2bf0dbbe6ed5df) — 5 most recent child pages
3. Read Handoff Log (364871f7633d81a5be74f181d076278c) — pending items only
4. Produce: date, top 3 priorities, pending handoffs, decisions needed
5. Ask Paskal if anything to add before writing the session log entry

## Session Log Format
[AgentName] · [Date] · One-line summary
Completed: list
Decisions confirmed: list
For Rex: what to sync
CLAUDE.md updated: yes/no
ClickUp tasks to close: list

## Handoff Log Format
[From → To] · [Date] · Context | Action required | Reference URL | Priority

## Signal Protocol
[STATE:working/idle/blocked/waiting:description]
[HANDOFF:agent] context | action | url | priority
[DECISION:title] body | context | priority
[ACTIVITY:action description]

## Standing Rules
- Tasks in ClickUp — descriptions under 300 characters
- Escalate enterprise commitments to Paskal always
- Never send external comms without Paskal confirmation
