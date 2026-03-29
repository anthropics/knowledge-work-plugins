# Methodology Reference

Full 4-stage workflow detail. The SKILL.md is the trigger and overview — this is the operational guide.

---

## STAGE 1: PREPARATION

### 1.1 Tool Check

Verify in order:
1. Gmail MCP: call `gmail_get_profile` — if it works, Tier 1 is available
2. Claude in Chrome: ask if enabled (Settings → Desktop app → Claude in Chrome) — Tier 2
3. Python API: `python3 -c "import googleapiclient; print('OK')"` — install if missing: `pip install google-api-python-client google-auth-oauthlib --break-system-packages`
4. OAuth token: check if `token.json` exists with both scopes. If not, run `${CLAUDE_PLUGIN_ROOT}/scripts/oauth_setup.py` — Tier 3

Report what's available and what each tier unlocks. Continue even if some tools are missing.

### 1.2 Full Inbox Audit

**Tier 3 (preferred):** Run `build_sender_index.py` to group all inbox messages by sender. Produces `sender_index.json` — the foundation for all subsequent phases. Warn the user this takes several minutes for large inboxes.

**Tier 1 fallback:** Use `gmail_search_messages` in a loop to pull sender/subject metadata in batches. Slower but works without the API.

Report: total messages, unique senders, top 20 by volume, distribution.

**Reading Round 1 — All subject lines:**
Work sender-by-sender from highest volume. For each, read ALL subject lines (not a sample). Classify:
- Clear noise → recommend bulk delete
- Clear signal → recommend keep or label
- Ambiguous → flag for Round 2

**Reading Round 2 — Bodies for ambiguous senders:**
Use `gmail_read_message` to read 2-3 full emails per ambiguous sender. Enough to resolve classification. Reclassify accordingly.

After both rounds, present a summary: bulk-delete candidates by category, keep/label recommendations, senders needing user input.

### 1.3 Unread Audit

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
- Notifications the user is aware of

Present: "needs attention" list with enough detail to act, informational count, suggested default approach. Ask how they want to handle each category. Do not mark anything read without explicit approval.

Mark approved set as read:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action mark-read --ids-file approved_unread_ids.json
```

---

## STAGE 2: ACTION

### 2.1 Bulk Delete by Content Markers

Not a category delete. Decisions come from Claude's reading in Stage 1, not Gmail's category tabs.

Target: senders where every single email is clearly noise. Reference `decision-framework.md` for signals.

Present the plan grouped by type (job alerts, real estate alerts, social digests, re-engagement, marketing newsletters, etc.) with counts. Get explicit user approval before executing.

Execute:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action trash --ids-file bulk_delete_ids.json
```

Or via Claude in Chrome for search-based bulk select when Python API is unavailable.

### 2.2 Sender-by-Sender Review Loop

Load `sender_index.json`. Start from `next_sender_idx`. Skip senders already in `inbox_decisions.json`.

**Per sender:**
1. Show: name, domain, count, date range, ALL subject lines, Claude's recommended action + one-line reasoning
2. Offer to show email bodies before user decides (for ambiguous cases)
3. AskUserQuestion: Trash / Archive / Label + Archive / Keep / Split / Skip
4. If Label: show existing labels, offer to create a new one
5. Execute immediately — do not queue decisions
6. Save to `inbox_decisions.json`
7. Advance `next_sender_idx` in `sender_index.json`

**Always flag before suggesting trash:**
- Email contains receipt, invoice, or confirmation number
- Email addresses user by personal name (not "Dear Customer")
- Sender domain is a financial institution, government body, or legal firm
- User has replied to this sender (check `in:sent to:sender@domain.com`)
- Subject contains: contract, agreement, tax, visa, permit, renewal, deadline

After every 10 senders: report progress, ask to continue or pause.

---

## STAGE 3: FUTURE PROOFING

### 3.1 Label and Filter System

Run after sender review is substantially complete — the review is the research.

Analyze `inbox_decisions.json` for keep/label patterns. Propose label categories with:
- Suggested label name (user renames freely)
- What goes in it and why (derived from the review, not pre-defined)
- Sender domains/addresses to match
- Skip inbox? (ask per label)
- Mark as read on arrival? (always ask explicitly — default is no)

Backup first:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_filters.py \
  --token token.json backup --output filters_backup.json
```

Create labels:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_labels.py \
  --token token.json create --name "Label Name"
```

Create filters:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage_filters.py --token token.json create \
  --from "sender1.com sender2@domain.com" --label-id Label_XXXXX [--skip-inbox] [--mark-read]
```

`criteria.from` is space-separated — Gmail OR's the list automatically. Never pass `--mark-read` unless user explicitly confirmed it.

### 3.2 Unsubscribe Sweep

From `inbox_decisions.json` (trashed senders), identify marketing ones. For each:

1. Get unsubscribe URL:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/get_unsubscribe_url.py \
  --token token.json --sender sender@domain.com --index sender_index.json
```

2. Execute based on platform (see `unsubscribe-patterns.md`):
   - Direct GET: `WebFetch` the URL, check response for confirmation text
   - Button click required: Claude in Chrome — navigate, find button, real click
   - Form-based: Claude in Chrome — navigate, select reason, submit

3. Log result to `unsub_log.json`

Present plan before executing. Skip: regulatory senders, transactional-only, dead links.

---

## STAGE 4: SAFETY REVIEW — BIN AUDIT

Remind user: this is why they held off emptying trash.

### 4.1 Scan Trash

Always use Python API — MCP search is unreliable for trash:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search_trash.py \
  --token token.json \
  --query "invoice OR receipt OR contract OR statement OR booking OR visa" \
  --output trash_hits.json
```

Run multiple targeted searches:
- Personal domains: `gmail.com OR hotmail.com OR outlook.com OR yahoo.com`
- Financial: `invoice OR statement OR payment OR balance OR refund`
- Government/legal: `tax OR permit OR visa OR notice OR compliance`
- Two-way relationships: check `in:sent to:` for each flagged sender domain

### 4.2 Cross-Check Decisions

For each flagged item: check `inbox_decisions.json`.
- Explicitly decided trash by the user → keep trashed (informed decision)
- Not in decisions (caught by bulk delete before review) → surface as potential false positive

### 4.3 Restore Plan + Approval

Do not restore anything without presenting the plan first:
- What was found (sender, subject samples, date range, why flagged)
- Whether it was explicitly decided or caught by bulk delete
- Where it will be restored (inbox, or a specific label)

Get explicit approval, then execute:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/batch_action.py \
  --token token.json --action restore --ids-file restore_ids.json [--label-id Label_XXX]
```

### 4.4 Final Report

Present full summary across all stages. Tell the user it is safe to empty trash if they choose. Do not empty it on their behalf.

---

## State Files

| File | Contents | Survives session reset? |
|------|----------|------------------------|
| `sender_index.json` | Full inbox by sender, `next_sender_idx` pointer | Yes |
| `inbox_decisions.json` | `sender → action` map — append only | Yes |
| `filters_backup.json` | Filter snapshot before bulk operations | Yes |
| `unsub_log.json` | Unsubscribe outcomes | Yes |
| `token.json` | OAuth token with refresh_token | Yes |

---

## Common Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| 403 on filter operations | Token missing `gmail.settings.basic` | Re-run `oauth_setup.py` with both scopes |
| Gmail UI click does nothing | `isTrusted: false` blocks synthetic events | Use Claude in Chrome for real clicks |
| OAuth redirect unreachable | Sandbox localhost ≠ browser localhost | Navigate Chrome to auth URL; read code from tab URL |
| Trash search returns inbox/sent/draft | Gmail MCP ignores `in:trash` | Use `search_trash.py` with Python API |
| "Select all conversations" banner missing | Must be in category tab, not search view | Navigate to category tab URL directly |
| Session reset loses decisions | Decisions not persisted per sender | `inbox_decisions.json` is the fix — write after every sender |
| Filter system wiped | "Delete all" included real filters | Always `backup` before any filter bulk operation |
