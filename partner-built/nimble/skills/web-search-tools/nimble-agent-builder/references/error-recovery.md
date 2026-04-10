# Error Recovery Reference

Detailed error handling patterns for Nimble agent workflows.

## Table of Contents

- [Authentication failure (401/403)](#authentication-failure-401403-from-any-tool-call)
- [Agent not found (404)](#agent-not-found-404-from-nimble-agent-get)
- [Empty results](#empty-results-run-returns-no-records)
- [Application-level run error](#application-level-run-error-error-field-in-response)
- [Rate limiting / transient errors (429, 5xx)](#rate-limiting--transient-errors-429-500-504)
- [Persistent data source failures](#persistent-data-source-failures-2-consecutive-500s)
- [Generation stuck](#generation-stuck-repeated-processing-status)
- [Publish conflict (409)](#publish-conflict-409-from-nimble_agents_publish)
- [Async task polling errors](#async-task-polling-errors)
- [Ambiguous agent match](#ambiguous-agent-match-no-clear-fit)
- [Unknown SDK errors](#unknown-sdk-errors)

---

## Authentication failure (401/403 from any tool call)

> Could not connect to Nimble. Please set your `NIMBLE_API_KEY` environment variable and retry.
> Get a key at [online.nimbleway.com/signup](https://online.nimbleway.com/signup) → Account Settings → API Keys.

Do not proceed until auth is valid.

## Agent not found (404 from `nimble agent get`)

> Agent "{name}" was not found. It may have been removed or renamed.

Fall back to `nimble agent list --limit 100` (CLI) to search for available agents.

## Empty results (run returns no records)

> The agent returned no results. Possible causes:
> - The target URL may be unreachable or behind authentication.
> - The page structure may have changed since the agent was created.
> - Required parameters may be missing — check the agent's `input_properties`.

## Application-level run error (`error` field in response)

> The agent run returned an error: "{error message}".
> This is an application-level failure, not an HTTP error.
> Common causes: page not found, access denied, invalid URL format.

For batch operations, log the error and continue with remaining items. Do not abort the entire batch.

## Rate limiting / transient errors (429, 500-504)

> For `nimble_agents_generate` or `nimble_agents_update_from_agent`: if 429/quota is returned, stop and report quota exhaustion. Do NOT create a new session or fallback to another session-creation call.
> For `nimble_agents_update_session`/`nimble_agents_status` on transient errors, wait briefly and retry once using the same `session_id`.
> For generated scripts, the SDK handles retry automatically.

See `sdk-patterns.md` > "Retry Behavior" for SDK retry configuration.

### Persistent data source failures (2+ consecutive 500s)

When the same data source fails repeatedly (e.g., all LinkedIn agents return 500), the entire data pipeline for that source is likely down. **Stop retrying and pivot through this hierarchy:**

1. **Use `nimble search`** (CLI) — the preferred tool for all information-finding tasks:
   - LinkedIn down → `nimble search --query "CTO fintech NYC site:linkedin.com"`
   - Crunchbase agent missing → `nimble search --query "Series B startup site:crunchbase.com"`
   - Any site → `nimble search --query "<keywords> site:<domain>"`

2. **Generate a custom agent** — if `nimble search` results lack the structure or depth needed, generate a dedicated agent for the target site via `nimble_agents_generate`.

3. **Present the pivot to the user** via `AskUserQuestion` — offer `nimble search` exploration, generating a custom agent, or waiting for the service to recover.

**`google_search` is NOT a fallback for failed agents.** It is a SERP analysis tool — only appropriate when the user's *intent* is to analyze Google's results page itself (rank/position tracking, SEO competitive analysis, SERP feature monitoring). The question to ask: "Does the user want to *find information*, or *analyze where things rank on Google*?" If the former, use `nimble search` (CLI). If the latter, use `google_search`.

**Important:** When pivoting to a fallback agent, always repeat the full discovery cycle: `nimble agent get --template-name` → present schema → confirm → run. Never skip schema inspection when switching agents.

## Generation stuck (repeated `processing` status)

Poll with `nimble_agents_status` (read-only GET endpoint) from a background Task agent. After 20 consecutive `processing` responses (~10 minutes), inform the user:

> Agent generation is taking longer than expected. You can wait or try a simpler prompt.

For transient errors during polling (timeouts, 5xx), retry the status check — do not restart generation. For persistent errors, analyze the error and retry via `nimble_agents_update_session` with the same `session_id` and an improved or simplified prompt. Max 2 consecutive retries.

## Publish conflict (409 from `nimble_agents_publish`)

The agent was already published in a previous session. The tool will automatically
fetch and return the existing agent details. If it cannot resolve the name,
suggest using `nimble agent list --limit 100` (CLI) to find the agent.

## Async task polling errors

### Task stuck at `pending`

If a task stays `pending` beyond 60 seconds, it may be queued behind other jobs or the API may be under load.

**For batch scripts:** This is why the smoke test is mandatory. If the smoke test passes but batch tasks are pending, the API is likely queuing — continue polling. If the smoke test itself times out at `pending`, stop immediately and diagnose:

1. Verify API key is valid (try a sync `nimble.agent.run()` call).
2. Try a different agent or simpler query.
3. Wait 5 minutes and retry — the API may be temporarily overloaded.

**Do not launch 100+ jobs without first confirming one completes.** A batch of pending jobs wastes time and API quota.

For individual stuck tasks within a running batch, the `task_timeout` parameter handles expiry automatically — see `sdk-patterns.md` > "Tuning parameters".

### Task not yet finished

The task has not reached a terminal state. Continue calling `nimble.tasks.get(task_id)` and checking `task.task.state` until it reaches `"success"` or `"error"`.

**IMPORTANT:** The terminal success state is `"success"`, NOT `"completed"`. The actual SDK type is `Literal['pending', 'success', 'error']`. Always check `task.task.state == "success"`. Results are **not inline** in the task object — after `state == "success"`, call `await nimble.tasks.results(task_id)` separately; parsed data is at `results['data']['parsing']`.

### Task state `"error"`

The async task failed server-side. Retry by submitting a new `nimble.agent.run_async()` call. If failures persist, fall back to the sync `nimble.agent.run()` method.

## Ambiguous agent match (no clear fit)

When `nimble agent list --limit 100` returns 0 matches or only partial matches:

1. **Explore with `nimble search`** (CLI) first. Before generating a custom agent, search the target domain to understand what data exists and how pages are structured. This reduces ambiguity and prevents generating agents for the wrong page type.
   - Example: `nimble search --query "site:crunchbase.com fintech series B NYC"` to see what Crunchbase pages look like for this use case.
   - `nimble search` is often sufficient on its own — if results satisfy the user's need, stop here.

2. **Generate a custom agent** when:
   - The target site has a consistent page structure (e.g., product pages, profiles).
   - A specific URL can be provided as an example for the generator.
   - The data needed goes beyond what `nimble search` provides.

3. **`google_search` is NOT a fallback for missing agents.** See the [Persistent data source failures](#persistent-data-source-failures-2-consecutive-500s) section for the full `google_search` vs `nimble search` distinction.

4. **When generating fails or produces poor results**, ask the user to clarify:
   - What specific data fields are needed.
   - An example URL of a page that has the desired data.
   - Whether an alternative data source is acceptable.

## Unknown SDK errors

The SDK raises typed exceptions: `RateLimitError` (429), `InternalServerError` (5xx), `APITimeoutError`, `APIConnectionError`. For unfamiliar errors, consult documentation sources listed in SKILL.md.
