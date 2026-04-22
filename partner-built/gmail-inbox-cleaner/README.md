# Gmail Inbox Cleaner

A Claude plugin for systematically overhauling a Gmail inbox. Not a one-click cleaner. Not a bulk-delete tool. A structured four-stage process where Claude reads your actual email, builds a complete picture of every sender relationship in your inbox, and works through decisions with you one sender at a time — with persistent state, a safety net before permanent deletion, and a filter system built from what it learned about your inbox rather than generic categories.

---

## The Problem With How People Clean Inboxes

The standard approaches all have the same failure mode: they don't read the mail.

**Bulk delete by Gmail category** nukes Promotions, Social, Updates. Sounds reasonable until you remember that invoices from freelancers land in Promotions, that security alerts go to Updates, that the rental agreement your landlord sent shows up in Social. Gmail's category tabs are routing heuristics, not intent signals. Trusting them for permanent deletion means you're one missed invoice away from a problem.

**Manual scrolling** works but takes hours, makes inconsistent decisions across sessions, and still misses the full picture — you'll decide to keep an email from a sender without realizing they've sent you 60 others you'd want to trash.

**Unsubscribe-first approaches** solve the wrong problem. Reducing future email doesn't address the existing backlog, and you end up unsubscribing from things that weren't actually bothering you while the real noise stays.

---

## What This Plugin Does Instead

Claude reads every email before touching anything.

The preparation stage works through your entire inbox — not a sample, not the first N messages, every sender — in two passes. First pass: all subject lines for every sender, classified into clear noise (uniform promotional/automated subjects), clear signal (financial, transactional, legal, personal), and ambiguous (mixed or unclear subjects). Second pass: for ambiguous senders, Claude opens 2-3 actual emails and reads the body to resolve classification. By the end, Claude has a recommended action for every sender relationship in your inbox, grounded in reading the actual content.

Then it presents that to you and asks for approval before doing anything.

---

## Why Sender-First, Not Time-First

Most email tools process messages in chronological order — newest first, or batches of 1000. This creates a real problem: the same sender appears across multiple batches, so you make decisions without seeing the full relationship. You decide to keep a message from `noreply@company.com` without realizing that sender has also emailed you 40 times with promotional content you'd want to trash.

This plugin groups every message in your inbox by sender before doing anything. When it comes time to act, you see the complete picture for each sender: how many emails, the full date range, all subject lines, Claude's recommended action and the reasoning behind it. You make one decision per sender relationship, not one decision per email.

That decision is then persisted immediately to `inbox_decisions.json`. Not batched, not held in memory — written to disk after every single sender. LLM sessions time out. Context windows fill up. The sender index stores your resume pointer so any new session picks up exactly where the last one left off, with no repeated decisions.

---

## The Action Stage Logic

Once preparation is done, the action stage runs in two phases.

**Phase 1: bulk delete by content markers.** Claude identifies senders where every single email is unambiguously noise — uniform promotional subjects, bulk email infrastructure domains (sendgrid, mailchimp, klaviyo in the From header), re-engagement campaigns, pure digest senders with no actionable content. These are grouped by type, shown to you with counts, and you approve the list before anything moves to trash. This typically handles 30-60% of inbox volume in one shot.

**Phase 2: sender-by-sender review loop.** Every sender not caught by the bulk phase gets individual review. Claude shows the full sender picture and its recommendation, flags anything that warrants caution (receipts, confirmation numbers, government or legal domains, emails you've ever replied to), and asks what you want to do: trash, archive, label and archive, keep, split by date, or skip for now. You decide; Claude executes immediately and saves the decision.

---

## The Flag System

Before recommending trash for any sender, Claude checks:

- Does any email from this sender contain a receipt number, invoice, confirmation code, or booking reference?
- Does any email address you by name rather than "Dear Customer"?
- Is the sender domain a financial institution, government body, or legal firm?
- Have you ever replied to this sender? (Checked against sent mail)
- Do any subject lines contain: contract, agreement, tax, visa, permit, renewal, deadline?

If any of these are true, Claude raises it explicitly before suggesting action. The goal is to make sure you're making an informed decision, not rubber-stamping a recommendation.

---

## The Filter System Is Built From Your Inbox, Not Templates

After the action stage, you have a complete record in `inbox_decisions.json` of every sender and what you decided to do with them. The future-proofing stage uses that as its source of truth.

Claude analyzes the senders you chose to keep or label, identifies patterns (what types of email do you actually want to receive and organize?), and proposes label names with the specific sender domains/addresses that should route to each. No pre-defined categories. No assumptions about what matters to you. The labels and filters are a direct output of reading your inbox and learning your preferences.

For each proposed label, Claude asks two questions before creating anything: should emails from these senders skip your inbox, and should they arrive pre-marked as read? Both questions have defaults of no. The plugin never assumes routing behavior or marks emails as read without explicit confirmation.

Existing filters are always backed up before any filter operation (`filters_backup.json`). The backup step is not optional.

---

## The Unsubscribe Sweep

After decisions are made, Claude builds an unsubscribe list from the senders marked for trash. It fetches the most recent email from each and extracts the unsubscribe mechanism — in priority order: `List-Unsubscribe` header (fastest, works via GET or POST), then HTML body links (the last unique non-tracking URL in the email body is usually unsubscribe).

Platform-specific behavior matters here. Some platforms (Loops, HubSpot) route through redirect chains before hitting the actual unsubscribe endpoint. Some require a real browser button click because they block synthetic JavaScript events (`isTrusted: false`). Some use multi-step forms. The plugin handles each case with the right tool — direct GET for simple links, Claude in Chrome for real clicks and form submissions.

The full list is shown to you before any request is sent. You remove anyone you want to stay subscribed to. Outcomes are logged.

---

## The Bin Audit

Before you empty your trash, this plugin runs a targeted scan to catch false positives from the bulk delete phase — emails that looked like noise by sender but contained something important.

The scan runs targeted searches against the trash (using the Python API directly, because the Gmail MCP does not reliably isolate `in:trash`): financial keywords, government and legal keywords, personal sender domains, transactional keywords. For each hit, it cross-checks `inbox_decisions.json`. If you explicitly decided to trash that sender in the review loop, it stays trashed — you made an informed decision. If it was caught by the bulk delete before individual review, Claude surfaces it as a potential false positive with subject samples and a restore plan.

The restore plan is presented to you before anything moves. You approve what gets restored and where it goes. Only after your approval does Claude execute restores.

Then the final report: before/after counts, everything trashed, archived, labeled, unsubscribed, restored. At that point, it's safe to empty your trash.

---

## Tool Tiers

The plugin degrades gracefully depending on what tools you have connected:

| Tier | Tools | What's available |
|------|-------|-----------------|
| 1 | Gmail MCP | Read-only audit, subject and body reading, search |
| 2 | + Claude in Chrome | Bulk UI operations, unsubscribe button clicks, OAuth code capture |
| 3 | + Python Gmail API | Sender index, batch operations, filter management, accurate trash search |

`/gmail-prepare` checks what's available and reports before starting. You can run a meaningful cleanup with Tier 1 alone; Tier 3 unlocks everything.

---

## Installation

```bash
claude plugin marketplace add siddhantkalra/gmail-inbox-cleaner-plugin
claude plugin install gmail-inbox-cleaner@gmail-inbox-cleaner-plugin
```

### Prerequisites

- **Gmail MCP** — connect from Cowork settings or add to `.mcp.json`
- **Claude in Chrome** — enable at Settings → Desktop app → Claude in Chrome (Tier 2)
- **Python + Gmail API client** for Tier 3:
  ```bash
  pip install google-api-python-client google-auth-oauthlib
  ```
- **Google Cloud credentials** — `credentials.json` from Google Cloud Console with an OAuth 2.0 client configured for Gmail

### OAuth Setup

Two scopes are required: `gmail.modify` (message operations) and `gmail.settings.basic` (filter management). Standard local OAuth redirect doesn't work here — sandbox localhost is a different network namespace from your browser. The plugin handles this with a manual code-capture flow:

1. Claude generates the authorization URL
2. You open it and click Allow
3. Browser shows "connection refused" — that's expected
4. Claude reads the auth code from your browser's address bar
5. Token is exchanged and saved with your refresh token

```bash
python3 scripts/oauth_setup.py --credentials credentials.json --token token.json
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/gmail-prepare` | Tool check → full two-pass inbox audit → unread review |
| `/gmail-cleanup` | Bulk delete by content markers → sender-by-sender review loop |
| `/gmail-future-proof` | Label/filter system from review data → unsubscribe sweep |
| `/gmail-bin-audit` | Trash scan → restore plan → final report |

---

## Scripts

All Python scripts have a CLI interface with `argparse`:

| Script | What it does |
|--------|--------------|
| `oauth_setup.py` | OAuth flow with dual-scope token, manual code-capture mode |
| `gmail_service.py` | Shared authenticated service, auto-refreshes expired tokens |
| `build_sender_index.py` | Groups all inbox messages by sender with batch metadata fetch |
| `batch_action.py` | Trash / archive / label / mark-read / restore via batchModify |
| `manage_labels.py` | Create, list, get label IDs |
| `manage_filters.py` | Create, backup, audit, list, delete filters; ghost filter detection |
| `search_trash.py` | Accurate trash search using `labelIds: ['TRASH']` parameter |
| `get_unsubscribe_url.py` | Extracts List-Unsubscribe header or HTML body hrefs |

---

## State Files

| File | Contents | Persists across sessions |
|------|----------|--------------------------|
| `sender_index.json` | All inbox messages grouped by sender + `next_sender_idx` resume pointer | Yes |
| `inbox_decisions.json` | Every sender decision, append-only | Yes |
| `filters_backup.json` | Filter snapshot before any bulk operation | Yes |
| `unsub_log.json` | Unsubscribe outcomes | Yes |
| `token.json` | OAuth token with refresh_token | Yes |

---

## License

MIT — see [LICENSE](LICENSE) for details.

Built by [Siddhant Kalra](https://github.com/siddhantkalra).
