---
description: Run Future Proofing stage — label/filter system and unsubscribe sweep
allowed-tools: Bash, Read, Write
---

Run the Future Proofing Stage. Run after the Action Stage is complete or substantially complete.

## Step 1 — Label and Filter System

The sender review loop gives Claude everything it needs to suggest intelligent filter categories. Do not build filters before the review — the review is the research.

Analyze `inbox_decisions.json` for keep/label patterns. Propose label categories with:
- Suggested label name (user renames freely)
- What goes in it and why (derived from the review, not pre-defined)
- Sender domains/addresses to match
- Skip inbox? (ask per label)
- Mark as read on arrival? (**always ask explicitly — default is no**)

Wait for user approval before creating each label.

**Always back up existing filters first:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_filters.py \
  --token token.json backup --output filters_backup.json
```

**Create labels:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_labels.py \
  --token token.json create --name "Label Name"
```

Note the returned label ID for the filter step.

**Create filters:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_filters.py --token token.json create \
  --from "sender1.com sender2@domain.com" --label-id Label_XXXXX [--skip-inbox] [--mark-read]
```

Filter notes:
- `--from` is space-separated — Gmail OR's the list automatically
- Never pass `--mark-read` unless user explicitly confirmed it
- Senders where emails sometimes need action should stay in inbox even if labeled

After creating, list all active filters to confirm:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_filters.py --token token.json list
```

## Step 2 — Unsubscribe Sweep

From `inbox_decisions.json` (trashed senders), identify marketing ones. Build the target list — exclude regulatory/legal senders and transactional-only senders (receipts, bookings).

For each candidate, get the unsubscribe URL:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/get_unsubscribe_url.py \
  --token token.json --sender sender@domain.com --index sender_index.json
```

Present the full plan to the user before executing: sender, URL found (or "none found"), execution method (GET / Chrome click / form). Let user remove any senders they want to stay subscribed to.

Execute based on method (see `references/unsubscribe-patterns.md`):
- Direct GET: `WebFetch` the URL, check response for confirmation text
- Button click: Claude in Chrome — navigate, find button, real click
- Form-based: Claude in Chrome — navigate, select reason, submit

Log all results. Present the completed log to the user.
