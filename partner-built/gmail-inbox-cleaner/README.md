# Gmail Inbox Cleaner

A systematic Gmail inbox overhaul plugin. Four stages — Preparation, Action, Future Proofing, Safety Review — designed for any inbox, any user. Claude does the reading and recommending; you make every final decision.

## The Flow

```
PREPARATION          → /gmail-prepare
  Tool check
  Full inbox audit (read ALL subject lines, then email bodies for ambiguous senders)
  Unread audit (surface actionable emails, ask user how to manage unreads)

ACTION               → /gmail-cleanup
  Bulk delete by Claude's content analysis (NOT by Gmail category)
  Sender-by-sender review loop (one sender at a time, full picture before deciding)

FUTURE PROOFING      → /gmail-future-proof
  Label + filter system (Claude suggests based on review; user decides everything)
  Unsubscribe sweep (trashed marketing senders)

SAFETY REVIEW        → /gmail-bin-audit
  Bin audit for false positives
  Restore plan presented to user before execution
  Final report + safe to empty trash
```

**Important**: Tell the user at the start — do not empty the trash until the Safety Review stage is complete.

## Commands

| Command | Stage | What it does |
|---------|-------|-------------|
| `/gmail-prepare` | Preparation | Tool check, full audit (subjects + bodies), unread review |
| `/gmail-cleanup` | Action | Bulk delete by content, then sender-by-sender review loop |
| `/gmail-future-proof` | Future Proofing | Label/filter system + unsubscribe sweep |
| `/gmail-bin-audit` | Safety Review | Trash audit, restore plan, final report |

## Prerequisites

1. **Gmail MCP connected** — for reading and searching emails
2. **Claude in Chrome enabled** — for bulk UI actions and button-click unsubscribes (Settings → Desktop app → Claude in Chrome)
3. **Python + Gmail API client** — for precision operations
   ```
   pip install google-api-python-client google-auth-oauthlib
   ```
4. **Google Cloud credentials** — a `credentials.json` from Google Cloud Console with a configured OAuth 2.0 client
5. **OAuth token with dual scopes** — `gmail.modify` + `gmail.settings.basic`

The plugin works without Python/API access but with reduced capability (no filter management, limited bulk operations). `/gmail-prepare` will tell you exactly what's available before starting.

## OAuth Setup

Two OAuth scopes are required — `gmail.modify` for message operations and `gmail.settings.basic` for filter management. The standard local-server OAuth flow doesn't work in this environment (sandbox localhost ≠ your browser's localhost). The plugin uses a manual code-capture flow instead:

1. Claude generates the auth URL
2. You open it in your browser and click Allow
3. The browser shows "connection refused" — expected
4. Claude reads the auth code from your browser's URL bar automatically
5. Token is exchanged and saved with your refresh token

Run `scripts/oauth_setup.py --credentials credentials.json --token token.json` and follow the prompts.

## State Files

The plugin maintains persistent state across sessions:

| File | Contents |
|------|----------|
| `sender_index.json` | Full inbox grouped by sender, resume pointer (`next_sender_idx`) |
| `inbox_decisions.json` | Every sender decision — survives session resets |
| `filters_backup.json` | Filter snapshot before any bulk filter operation |
| `token.json` | OAuth token with refresh_token |

## Key Design Principles

- **Never delete by Gmail category** — important emails land in Promotions and Social. Decisions are based on reading actual content.
- **Sender-first, always** — processing emails in sequential order misses the full picture per sender. Every sender is reviewed as a complete unit.
- **User approves before every bulk action** — no autonomous mass deletions. Claude presents a plan; you approve.
- **Persist after every sender** — session timeouts are real. Decisions are saved immediately, not batched.
- **Back up before filter operations** — always snapshot filters before any bulk delete.
- **Bin audit before emptying trash** — the safety net for false positives from bulk delete.
