---
description: Generate a standup update from recent activity
argument-hint: "[yesterday | today | blockers]"
---

# /standup

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a standup update by pulling together recent activity across your tools.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        STANDUP                                    │
├─────────────────────────────────────────────────────────────────┤
│  STANDALONE (always works)                                       │
│  ✓ Tell me what you worked on and I'll structure it             │
│  ✓ Format for daily standup (yesterday / today / blockers)      │
│  ✓ Keep it concise and action-oriented                          │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect your tools)                      │
│  + Source control: Recent commits and PRs                        │
│  + Project tracker: Ticket status changes                        │
│  + Chat: Relevant discussions and decisions                      │
│  + CI/CD: Build and deploy status                                │
└─────────────────────────────────────────────────────────────────┘
```

## What I Need From You

**Option A: Let me pull it**
If your tools are connected, just say `/standup` and I'll gather everything automatically.

**Option B: Tell me what you did**
"Worked on the auth migration, reviewed 3 PRs, got blocked on the API rate limiting issue."

## Output

```markdown
## Standup — [Date]

### Yesterday
- [Completed item with ticket reference if available]
- [Completed item]

### Today
- [Planned item with ticket reference]
- [Planned item]

### Blockers
- [Blocker with context and who can help]
```

## If Connectors Available

If **~~source control** is connected:
- Pull recent commits and PRs (opened, reviewed, merged)
- Summarize code changes at a high level

If **~~project tracker** is connected:
- Pull tickets moved to "in progress" or "done"
- Show upcoming sprint items

If **~~chat** is connected:
- Scan for relevant discussions and decisions
- Flag threads needing your response

## Tips

1. **Run it every morning** — Build a habit and never scramble for standup notes.
2. **Add context** — After I generate, add any nuance about blockers or priorities.
3. **Share format** — Ask me to format for Slack, email, or your team's standup tool.
