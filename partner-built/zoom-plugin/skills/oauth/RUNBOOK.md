# OAuth 5-Minute Preflight Runbook

Use this before deep debugging. It catches common OAuth failures fast.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm You Chose the Right Flow

- S2S (`account_credentials`) for backend automation on your own account.
- User OAuth (`authorization_code`) for acting on behalf of users.
- Device flow for browserless devices.
- Client credentials for chatbot-only scenarios.

Wrong flow choice causes scope and token errors later.

## 2) Confirm Endpoint Split

- Authorize URL: `https://zoom.us/oauth/authorize`
- Token URL: `https://zoom.us/oauth/token`

If token requests return 404/HTML, verify you are not calling `/oauth/token`.

## 3) Confirm Redirect URI Exact Match

- `redirect_uri` in token exchange must exactly match Marketplace config.
- Match scheme, host, path, and trailing slash.

### State Parameter Guardrail

- Always generate and verify `state` for user OAuth flows.
- Expire state quickly and consume once.
- If callback has `code` but state is missing/invalid, reject and restart auth.

## 4) Confirm Scope and App Type Alignment

- Verify required scopes are added to app.
- Re-authorize after scope changes.
- Ensure app type supports requested behavior.

## 5) Confirm Token Lifecycle Handling

- Access token expires ~1 hour.
- Store latest refresh token after each refresh.
- Handle refresh failure with re-auth fallback.

### Refresh Rotation Reminder

- Treat refresh tokens as rotating credentials.
- Persist new refresh token returned by refresh response.
- Using stale refresh tokens causes intermittent auth failures later.

## 6) Quick Probes

- Token endpoint returns JSON with `access_token`.
- API call to `/v2/users/me` succeeds with bearer token.
- Redirect callback receives `code` and valid `state`.

### Copy/Paste Validation Commands

Use these to verify OAuth plumbing in under a minute.

```bash
# 1) S2S token request
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(printf '%s:%s' "$ZOOM_CLIENT_ID" "$ZOOM_CLIENT_SECRET" | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id=$ZOOM_ACCOUNT_ID"

# 2) User auth-code exchange
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(printf '%s:%s' "$ZOOM_CLIENT_ID" "$ZOOM_CLIENT_SECRET" | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=$ZOOM_AUTH_CODE&redirect_uri=$ZOOM_REDIRECT_URI"

# 3) Token health check
curl -X GET "https://api.zoom.us/v2/users/me" \
  -H "Authorization: Bearer $ZOOM_ACCESS_TOKEN"
```

## 7) Fast Decision Tree

- **4709 redirect mismatch** -> fix exact redirect URI.
- **4702/4704 invalid client** -> wrong client credentials or app.
- **4733/4734 code errors** -> auth code expired/invalid, restart consent flow.
- **Scopes missing** -> add scopes + re-authorize.

## 8) Flow-to-App-Type Guardrail

- If using `account_credentials`, app must support S2S flow.
- If using `authorization_code`, app and redirect configuration must support user consent.
- If auth appears valid but API fails, verify app type, scope level, and account ownership assumptions.
