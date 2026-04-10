---
name: nimble-error-handling-reference
description: |
  Error codes and troubleshooting guide. Load when a nimble command fails unexpectedly.
  Contains: HTTP error codes, empty content signals, captcha/blocked responses, known site quirks,
  render tier escalation tips, debug patterns.
---

# Error Handling & Known Limitations

## Error codes

| Error                             | Cause                                                         | Solution                                                                                                |
| --------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `NIMBLE_API_KEY not set`          | Missing env variable                                          | `export NIMBLE_API_KEY="your-key"`                                                                      |
| `401 Unauthorized`                | Invalid or expired API key                                    | Verify key at nimbleway.com → Account Settings                                                          |
| `402 Payment Required`            | Premium feature (e.g. `--include-answer`) not on current plan | Retry the same query without `--include-answer` and continue                                            |
| `403 Forbidden`                   | Same as 402 for some endpoints                                | Same — retry without the premium flag                                                                   |
| `429 Too Many Requests`           | Rate limit exceeded                                           | Reduce frequency; wait before retrying; upgrade API tier if needed                                      |
| `404` from `nimble tasks results` | Using the crawl_id instead of task_id                         | Use the per-page task_ids from `nimble crawl status`, not the crawl job id                              |
| Timeout (search)                  | Deep mode or too many results                                 | Add `--search-depth lite`; reduce `--max-results`                                                       |
| Timeout (extract, no render)      | Slow server or large page                                     | Add `--request-timeout 60000`                                                                           |
| Timeout (extract, with render)    | Page JS takes too long to settle                              | Retry with increased `--render-options '{"timeout": 60000}'`, then 90000. See timeout escalation below. |
| Empty or minimal content          | JavaScript-rendered page                                      | Add `--render` flag to execute JavaScript before extraction                                             |
| No results                        | Query too narrow or wrong focus                               | Try different `--focus`; broaden query; remove domain filters                                           |
| CLI not found                     | Nimble CLI not installed                                      | `npm i -g @nimble-way/nimble-cli`                                                                       |

## Known site limitations

| Site / Scenario            | Issue                                                       | Workaround                                                                                                                |
| -------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **LinkedIn profiles**      | Auth wall — returns redirect/JS, status 999                 | Use `--focus social` search instead — returns LinkedIn data directly via subagents. Never try to `extract` LinkedIn URLs. |
| **X (Twitter) profiles**   | Auth wall or rate limiting                                  | Use `--focus social` search — returns X data via subagents                                                                |
| **Sites behind login**     | Extract returns login page, not content                     | No workaround — use search snippets from `--include-answer` instead                                                       |
| **Heavy SPAs**             | Extract returns empty or minimal HTML                       | Add `--render` to execute JavaScript before extraction                                                                    |
| **Crawl results**          | Returns raw HTML (60–115KB/page), no markdown option        | Use `map` + `extract  --format markdown` for LLM-friendly output                                                          |
| **Crawl status**           | May misreport task statuses as "failed" when they succeeded | Always try `nimble tasks results --task-id` before assuming failure                                                       |
| **PDF pages**              | Standard extract may return binary                          | Use ` --format markdown`; if still fails, use `--render`                                                                  |
| **Cookie consent banners** | Blocks content on first load                                | Add `--consent-header` to auto-handle consent dialogs                                                                     |

## Crawl-specific issues

**Using crawl_id in `nimble tasks results`:**

```bash
# WRONG — returns 404
nimble tasks results --task-id "abc-123"   # abc-123 is the crawl_id

# RIGHT — use the per-page task_ids from crawl status
nimble crawl status --id "abc-123"         # returns task_ids: ["task-456", "task-789", ...]
nimble tasks results --task-id "task-456"  # correct
```

**Crawl running forever:**

- Check status: `nimble crawl status --id "<crawl-id>"`
- Cancel if needed: `nimble crawl terminate --id "<crawl-id>"`
- Always set `--limit` to prevent unbounded crawls

**Crawl shows "failed" tasks:**

- `crawl status` occasionally misreports task statuses
- Try retrieving the "failed" task anyway: `nimble tasks results --task-id "<task-id>"`
- If it returns data, the task actually succeeded

## `--include-answer` returns 402/403

This is a premium feature on Enterprise plans. When it fails:

1. Do NOT treat it as a fatal error
2. Retry the **exact same query** without `--include-answer`
3. Continue with the search results — they are still valuable without the synthesized answer

```bash
# If this fails with 402/403:
nimble search --query "..." --include-answer --search-depth lite

# Retry without --include-answer:
nimble search --query "..." --search-depth lite
```

## Render timeout escalation

Never give up after a single timeout. Retry with increasing timeouts:

```bash
# Attempt 1 — default 30s
nimble extract --url "https://example.com" --render  --format markdown

# Attempt 2 — 60s
nimble extract --url "https://example.com" --render \
  --render-options '{"timeout": 60000}'  --format markdown

# Attempt 3 — 90s, wait for full network idle
nimble extract --url "https://example.com" --render \
  --render-options '{"render_type": "idle0", "timeout": 90000}'  --format markdown
```

If all 3 attempts timeout, move to Tier 3 (browser-use investigation → browser actions / network capture).

---

## Slow responses

| Cause                               | Fix                                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| Using default search depth          | Add `--search-depth lite` or `fast` — default `deep` is slowest                    |
| Too many results                    | Reduce `--max-results` (start with 5–10)                                            |
| `shopping`/`social`/`location` mode | These use subagents — slightly slower by design; reduce `--max-subagents` if needed |
| Rendering JS                        | `--render` adds 3–5s — only use when content is actually dynamic                    |
