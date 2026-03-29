---
name: inbox-cleanup
description: >
  Full Gmail inbox overhaul methodology. Use this skill when the user says
  "clean my inbox", "audit my Gmail", "clear out my email", "help me
  unsubscribe from everything", "set up Gmail filters", "rebuild my Gmail
  filters", "go through my emails", or "help me get to inbox zero". This
  skill encodes a four-stage methodology — Preparation, Action, Future
  Proofing, Safety Review — designed to work for any inbox with Claude's
  intelligence driving decisions and the user making final calls.
version: 0.3.0
---

# Gmail Inbox Cleaner

Four-stage systematic Gmail cleanup. Claude reads and recommends; the user decides everything.

**Tell the user at the start**: Do not empty your trash until the Safety Review stage at the end.

## Stages and Commands

```
PREPARATION     → /gmail-prepare
  Tool check → Full audit (all subject lines, then bodies for ambiguous senders) → Unread audit

ACTION          → /gmail-cleanup
  Bulk delete by content markers (not by Gmail category) → Sender-by-sender review loop

FUTURE PROOFING → /gmail-future-proof
  Label + filter system (Claude suggests from review; user decides) → Unsubscribe sweep

SAFETY REVIEW   → /gmail-bin-audit
  Trash scan for false positives → Restore plan with user approval → Final report
```

## Tool Tiers

See `CONNECTORS.md` for what each tier enables.

| Tier | Tools | Capability |
|------|-------|------------|
| 1 | Gmail MCP | Read-only audit, subject/body reading |
| 2 | + Claude in Chrome | Bulk delete UI, unsubscribe clicks, OAuth flow |
| 3 | + Python Gmail API | Sender index, batch operations, filter management, accurate trash search |

Scripts are in `${CLAUDE_PLUGIN_ROOT}/scripts/`. Full methodology detail is in `references/methodology.md`. Decision heuristics are in `references/decision-framework.md`. Unsubscribe patterns are in `references/unsubscribe-patterns.md`.

## Key Rules

- Never bulk-delete by Gmail category — read content first
- Sender-first always — see the full relationship before deciding
- Execute and persist after every individual sender — don't queue decisions
- Backup filters before any filter operation — use `manage_filters.py backup`
- Use `search_trash.py` for trash searches — MCP search does not reliably isolate trash
- Never mark emails as read without explicit user confirmation
- Never restore from trash without presenting the plan and getting approval first
