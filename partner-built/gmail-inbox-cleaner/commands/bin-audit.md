---
description: Run Safety Review — bin audit before user clears trash
allowed-tools: Bash, Read, Write
---

Run the Safety Review (Bin Audit). This is the final stage. Remind the user: this is why they held off emptying trash.

## Step 1 — Scan Trash

**Always use the Python API for trash searches** — the Gmail MCP does not reliably isolate `in:trash` and may return inbox/sent/draft results.

Run targeted searches:
```bash
# Financial
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search_trash.py \
  --token token.json \
  --query "invoice OR receipt OR statement OR payment OR balance OR refund" \
  --output trash_financial.json

# Government and legal
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search_trash.py \
  --token token.json \
  --query "tax OR permit OR visa OR notice OR compliance OR deadline" \
  --output trash_legal.json

# Personal senders (gmail.com, hotmail.com, outlook.com, yahoo.com)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search_trash.py \
  --token token.json \
  --query "from:gmail.com OR from:hotmail.com OR from:outlook.com OR from:yahoo.com" \
  --output trash_personal.json

# Transactional
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search_trash.py \
  --token token.json \
  --query "confirmation OR booking OR itinerary OR reservation OR ticket OR \"your order\"" \
  --output trash_transactional.json
```

Also check two-way relationships: for any flagged sender domain, run `gmail_search_messages` with `in:sent to:sender@domain.com` — if the user ever replied, flag it.

## Step 2 — Cross-Check Decisions

For each flagged item, check `inbox_decisions.json`:
- **Explicitly decided trash by the user** → keep trashed (informed decision)
- **Not in decisions** (caught by bulk delete before review) → surface as potential false positive

## Step 3 — Present Restore Plan to User

Do not restore anything without presenting the plan first:
- What was found (sender, subject samples, date range, why flagged)
- Whether it was explicitly decided or caught by bulk delete
- Where it will be restored (inbox, or a specific label)

Get explicit approval, then execute:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action restore --ids-file restore_ids.json

# To restore directly into a label:
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action restore --ids-file restore_ids.json --label-id Label_XXX
```

## Step 4 — Final Report

Present full summary across all stages:
- **Before / After**: message counts
- **Trashed**: count by category
- **Archived**: count
- **Labeled**: count, by label
- **Unsubscribed**: count and list
- **Restored from bin**: count
- **Labels created**: list
- **Filters created**: list

Then tell the user: "The bin audit is complete. It is now safe to empty your trash if you choose." Do not empty it on their behalf — that is a permanent deletion and must be a deliberate user action.
