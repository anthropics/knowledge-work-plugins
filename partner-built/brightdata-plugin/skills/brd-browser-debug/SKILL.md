---
name: brd-browser-debug
description: "Debug Bright Data Scraping Browser sessions using the Browser Sessions API. Use this skill when the user encounters a Bright Data browser session error, puppeteer stack trace, failed scraper run, or asks about session bandwidth, duration, captchas, or connection issues. Also use when a Bright Data scraper produces unexpected results such as empty data, 0 items found, missing products, or fewer results than expected — session data can reveal whether the issue is network/proxy-side (blocks, captchas, redirects, timeouts) or client-side (selectors, extraction logic). Triggers on phrases like 'why did my session fail', 'debug my bright data session', 'check my scraping browser sessions', 'how much bandwidth did my scraper use', 'got 0 results', 'found 0', 'scraper returned empty', 'scraper not working', 'script didn't work', or when a Bright Data error code or brd.superproxy.io stack trace appears in the conversation. Requires BRIGHTDATA_API_KEY environment variable."
user-invocable: true
---

# Bright Data — Browser Session Debugger

Diagnose Bright Data Scraping Browser sessions using the Browser Sessions API. Fetches live session data and performs smart triage: error diagnosis, bandwidth analysis, captcha reporting, and pattern detection across recent sessions.

## Setup

**Set your API key:**
```bash
export BRIGHTDATA_API_KEY="your-api-key"
```

Get a key from [Bright Data Dashboard → API Tokens](https://brightdata.com/cp/setting/users).

No zone configuration needed — zone is returned as a field in session data.

## Usage

### List & triage recent sessions

Invoked as `/brd-browser-debug` with no arguments.

**API reference:** [GET /browser_sessions](https://docs.brightdata.com/api-reference/browser-api/get-sessions)

#### Fetching sessions

Start with a single call using `limit=100` (the maximum) sorted by most recent:
```
GET https://api.brightdata.com/browser_sessions?limit=100&sort=timestamp&order=desc
Authorization: Bearer $BRIGHTDATA_API_KEY
```

**Pagination:** The response includes `total`, `has_more`, and `next_offset`. If `has_more` is true and the analysis requires more data (e.g. bandwidth outlier detection needs a larger sample), fetch the next page using `offset=<next_offset>`. Continue until you have enough data or `has_more` is false.

**Available filters** — apply when the user specifies a scope:
- `status=failed|finished|running` — narrow to a specific session state
- `api_name=<zone>` — filter to a specific Bright Data zone
- `target_url=<domain>` — filter by target domain (e.g. `ksp.co.il`)
- `start_date` / `end_date` — ISO 8601 datetime range
- `sort=timestamp|duration|bandwidth` with `order=asc|desc`

If the user asks about a specific zone, date range, or domain — apply the relevant filter rather than fetching all sessions and filtering client-side.

#### Triage steps

1. Present a **health summary**: `total` from the response, counts of finished / failed / running.
2. **Most recent session** — always highlight it regardless of status (same detail level as single-session mode).
3. **Failed sessions** — for each failure: session ID, timestamp, duration, bandwidth, then reason about the cause using the signals in the Diagnosing Failed Sessions section below.
4. **Pattern detection** — if 3+ sessions share the same `error.code`, call it a systemic issue:
   > "3 sessions failed with `custom_headers` — you are overriding a header Bright Data forbids. Remove `page.setExtraHTTPHeaders()` from your code."
5. **Bandwidth outliers** — group sessions by `target_url` domain. For each domain with 3+ sessions, calculate the median bandwidth. Flag any session whose bandwidth exceeds 2× the median for that domain as an outlier, and note if it was a failed session that burned unusually high bandwidth before dying.
6. **Captcha activity** — report how many sessions hit captchas and whether they were solved.
7. Close with a **one-line verdict**: the most important finding and the most impactful fix.

### Inspect a single session

Invoked as `/brd-browser-debug <session_id>`.

**API reference:** [GET /browser_sessions/{session_id}](https://docs.brightdata.com/api-reference/browser-api/get-session)

1. Call:
   ```
   GET https://api.brightdata.com/browser_sessions/<session_id>
   Authorization: Bearer $BRIGHTDATA_API_KEY
   ```
   Returns 404 if the session ID is not found — tell the user and stop.

2. Present a **deep-dive** using the response fields:
   - **Status** (`status`): `running` / `finished` / `failed`
   - **Zone** (`api_name`): the Bright Data zone that handled the session
   - **Timestamp** (`timestamp`): ISO 8601 — show in local-friendly format
   - **Duration** (`duration`): seconds (nullable) — flag if < 2 s on failure (session barely started)
   - **Bandwidth** (`bandwidth`): convert bytes → MB
   - **Navigations** (`navigations`): flag if 0 (nothing was loaded)
   - **Captcha** (`captcha`): one of `solved` / `none` / `detected` / `failed` — `detected` means a challenge appeared but was not solved; `failed` means solving was attempted but unsuccessful
   - **Route**: `target_url` → `end_url` — note significant drift (different domain, login wall, error page)
   - **Error** (`error.code` + `error.message`): reason about the cause using the signals in Diagnosing Failed Sessions below
3. Close with a **one-line verdict**.

### Auto-detect from conversation context

When a Bright Data browser issue appears in the conversation — including puppeteer stack traces, error codes, mention of `brd.superproxy.io`, the user describing a session failure, OR a scraper producing empty/unexpected results (e.g. "Found 0 categories", "Got 0 products", fewer items than expected):

- If a session ID is visible in the output → run **single-session** deep-dive on it.
- If no session ID is visible → run **list & triage**, filtering by the relevant target domain. Highlight the most recent session as the likely culprit.
- Cross-reference the error or unexpected behavior seen in the conversation with what the API returns. A session that finished successfully with normal bandwidth but the scraper got 0 results points to a client-side selector/extraction bug, not a proxy issue.

## Features

- **Smart triage**: automatically groups sessions by failure pattern, not just lists them
- **Dynamic bandwidth outliers**: compares sessions per domain using median, flags sessions exceeding 2× the median
- **Captcha reporting**: shows captcha hit rate and solve rate
- **Error reasoning**: reads session signals holistically to infer what went wrong
- **Zero config**: reads API key from env var, no zone setup needed

## Diagnosing Failed Sessions

Do not rely on the error code alone. Cross-reference all available session signals to reason about what went wrong:

- **Duration + navigations**: a session that failed in < 2 s with 0 navigations never got past the connection phase — likely a configuration or auth issue. A session that ran for minutes before failing points to a runtime problem (blocked mid-scrape, idle timeout, network drop).
- **Bandwidth relative to other sessions**: a failed session that consumed bandwidth similar to successful ones likely reached the target but failed during extraction. A failed session with near-zero bandwidth never loaded anything.
- **Captcha field**: if `captcha` is `detected` but not `solved`, the session was stopped by an unsolved challenge — suggest enabling captcha solving on the zone.
- **target_url vs end_url**: significant drift (different domain, login page, error page) means the session was redirected away from the intended target.
- **error.message**: use the raw message text as-is to describe what happened — do not guess or invent meaning beyond what the message says. If the cause is unclear, direct the user to [Bright Data support](https://help.brightdata.com).
