---
description: Run Action Stage — bulk delete then sender review loop
allowed-tools: Bash, Read, Write
---

Run the Action Stage. Requires `/gmail-prepare` to have completed first (`sender_index.json` and `inbox_decisions.json` must exist).

## Step 1 — Bulk Delete by Content Markers

**This is NOT a category delete.** Do not mass-delete Gmail's Promotions, Social, or Forums tabs — important emails land there regularly. The bulk delete is based on Claude's reading of actual content from the Preparation Stage.

Load the sender index and Claude's Round 1/2 classifications. Identify senders recommended for bulk delete: those where every email is clearly noise (all promotional subjects, bulk email infrastructure domains, completely inactive relationships, pure notification digests with no actionable content).

Present the bulk delete plan grouped by type (job alerts, real estate alerts, social digests, re-engagement, marketing newsletters, etc.) with counts. Get explicit user approval before executing.

Execute:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action trash --ids-file bulk_delete_ids.json
```

Report how many emails were trashed and the updated inbox count.

## Step 2 — Sender-by-Sender Review Loop

Every sender NOT covered by the bulk delete goes through this loop — one sender at a time, all emails from that sender reviewed before moving to the next.

**Why sender-first**: Processing emails in time order catches the same sender across multiple batches, making decisions inconsistent and preventing you from seeing the complete relationship per sender.

Load `sender_index.json`. Start from `next_sender_idx`. Skip senders already in `inbox_decisions.json`.

**For each sender:**

1. Show: name, domain, count, date range, ALL subject lines, Claude's recommended action + one-line reasoning
2. Offer to show email bodies before user decides (for ambiguous cases)
3. Present via AskUserQuestion: Trash / Archive / Label + Archive / Keep / Split / Skip
4. If Label: show existing labels, offer to create a new one
5. Execute immediately — do not queue decisions
6. Save to `inbox_decisions.json`:
   ```bash
   # Trash:
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
     --token token.json --action trash --ids-file sender_ids.json

   # Archive:
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
     --token token.json --action archive --ids-file sender_ids.json

   # Label + Archive:
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
     --token token.json --action label --label-id Label_XXX --ids-file sender_ids.json
   ```
7. Advance `next_sender_idx` in `sender_index.json`

**Always flag before suggesting trash:**
- Email contains receipt, invoice, or confirmation number
- Email addresses user by personal name (not "Dear Customer")
- Sender domain is a financial institution, government body, or legal firm
- User has replied to this sender (check `in:sent to:sender@domain.com`)
- Subject contains: contract, agreement, tax, visa, permit, renewal, deadline

**After every 10 senders:** report progress, ask to continue or pause.

**Session resume**: `next_sender_idx` in `sender_index.json` is the resume pointer. Any new session picks up exactly where the last left off.
