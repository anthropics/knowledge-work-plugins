---
description: Run full preparation stage — tools, audit, and unread review
allowed-tools: Bash, Read, Write
---

Run the full Preparation Stage. This must complete before any action is taken on the inbox.

**Tell the user immediately**: Do not empty your trash/bin until the Safety Review stage at the very end. Items deleted during cleanup are recoverable until that final stage.

## Step 1 — Tool Check

Verify in order:

1. **Gmail MCP**: call `gmail_get_profile` — if it works, Tier 1 is available
2. **Claude in Chrome**: ask if enabled (Settings → Desktop app → Claude in Chrome) — Tier 2
3. **Python API**: `python3 -c "import googleapiclient; print('OK')"` — if missing, install:
   ```bash
   pip install google-api-python-client google-auth-oauthlib --break-system-packages
   ```
4. **OAuth token**: check if `token.json` exists with both scopes. If not, run:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/oauth_setup.py \
     --credentials credentials.json --token token.json
   ```

Report what's available and what each tier unlocks. Proceed even if some tools are missing.

## Step 2 — Full Inbox Audit

1. Use `gmail_get_profile` to get total message count and account address.
2. Build the sender index (Tier 3 preferred):
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_sender_index.py \
     --token token.json --output sender_index.json
   ```
   Warn the user this takes several minutes for large inboxes. Tier 1 fallback: use `gmail_search_messages` in a loop to pull sender/subject metadata in batches.

3. Report: total messages, unique senders, top 20 by volume, distribution.

**Reading Round 1 — All subject lines per sender:**

Work sender-by-sender from highest volume. For each, read ALL subject lines (not a sample). Classify:
- **Clear noise** → recommend bulk delete
- **Clear signal** → recommend keep or label
- **Ambiguous** → flag for Round 2

**Reading Round 2 — Bodies for ambiguous senders:**

For each Round 1 ambiguous sender, use `gmail_read_message` to read 2-3 full emails. Reclassify accordingly.

After both rounds, present a summary: bulk-delete candidates by category, keep/label recommendations, senders needing user input.

## Step 3 — Unread Audit

Fetch all unread inbox messages. Classify:

**Needs attention** (surface explicitly):
- Requires response, action, or signature
- Invoice, contract, deadline, outstanding balance
- Government or regulatory notice
- Account security alert
- Time-sensitive items

**Informational unread** (can bulk-mark-read):
- Newsletters, digests the user already knows about
- Automated reports with no required action
- Notifications with no action required

Present: "needs attention" list with enough detail to act, informational count, suggested default approach. Ask how the user wants to handle each category. **Do not mark anything read without explicit approval.**

When approved, mark the confirmed set as read:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action mark-read --ids-file approved_unread_ids.json
```

## Output

At end of preparation:
- Total messages and senders audited
- Bulk delete candidates: count and categories
- Unread status: handled / pending user decision
- Recommendation for how to proceed into Action Stage
