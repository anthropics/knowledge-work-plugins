# REST API 5-Minute Preflight Runbook

Use this before deep debugging. It catches common Zoom REST API integration failures fast.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm Auth Flow and Endpoint

- Choose matching OAuth flow for use case (S2S/User/PKCE/Device).
- Use token URL `https://zoom.us/oauth/token`.

Wrong flow or token endpoint causes immediate auth failures.

## 2) Confirm Scope and Account Context

- Verify token contains required scopes.
- For admin/account-level operations, verify app/account permissions.
- Re-authorize after scope changes.

## 3) Confirm ID Semantics

- Distinguish Meeting ID vs Meeting UUID.
- Apply required URL encoding (double-encoding for UUID where needed).

### ID Sanity Rules

- Use numeric Meeting ID for many standard meeting operations.
- Use Meeting UUID for some past-instance/recording/report operations.
- If endpoint docs mention UUID and your value contains `/` or `+`, encode carefully.

If a resource "exists" in UI but API returns not found, ID type/encoding mismatch is a top cause.

## 4) Confirm Pagination and Rate Limits

- Handle `next_page_token` where applicable.
- Implement retry/backoff on 429 and transient 5xx.

### Minimal Retry Policy

- 429 or 5xx: exponential backoff with jitter.
- Respect retry headers when provided.
- Put high-volume endpoints behind queue/batch workers.

## 5) Confirm Webhook-Driven Workflows

- If pipeline is event-driven, validate webhook signatures and retry behavior.
- Respond quickly and process asynchronously.

## 6) Quick Probes

- `GET /v2/users/me` succeeds with current token.
- Representative endpoint (e.g., list meetings) returns expected schema.
- Error payload includes actionable code/details (not HTML response).

### Copy/Paste Validation Commands

```bash
# 1) Get S2S access token
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(printf '%s:%s' "$ZOOM_CLIENT_ID" "$ZOOM_CLIENT_SECRET" | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id=$ZOOM_ACCOUNT_ID"

# 2) Validate token can access account context
curl -X GET "https://api.zoom.us/v2/users/me" \
  -H "Authorization: Bearer $ZOOM_ACCESS_TOKEN"

# 3) List meetings for current user (quick schema sanity)
curl -X GET "https://api.zoom.us/v2/users/me/meetings?page_size=30" \
  -H "Authorization: Bearer $ZOOM_ACCESS_TOKEN"
```

Expected: JSON responses with HTTP 200 (or clear JSON error codes), not HTML error pages.

## 7) Fast Decision Tree

- **401/invalid token** -> wrong flow, expired token, or scope mismatch.
- **404-like behavior** -> wrong endpoint path/version or wrong resource ID.
- **429 spikes** -> missing backoff/queue strategy.

## 8) Common Integration Mixups

- REST `join_url` is a browser link, not a Meeting SDK join payload.
- REST API creates/manages Zoom resources; Meeting SDK and Video SDK are separate integration surfaces.
- If auth works but operation fails, check scope and resource ownership before endpoint debugging.
