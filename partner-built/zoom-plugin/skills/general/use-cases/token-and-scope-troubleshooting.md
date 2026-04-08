# Token and Scope Troubleshooting (Highest-Frequency Pattern)

This is the most common failure mode across Zoom REST API integrations and SDK backends:

- `Invalid access token`
- `Access token is expired`
- `does not contain scopes:[...]`
- "works for me but not for other users/accounts"

## Skills Needed

| Order | Skill | Purpose |
|------:|------|---------|
| 1 | **zoom-oauth** | Understand which grant type you are using and why |
| 2 | **zoom-rest-api** | Tie the failing endpoint to required scopes and app type |
| 3 | **zoom-webhooks** (optional) | Verify you are validating webhook requests correctly |

## Triage Checklist

### 1. Identify Which Token You Are Using

Ask:

- Which app type: **Server-to-Server OAuth**, **General App (User OAuth)**, **Chatbot**, **Meeting SDK**, **Video SDK**?
- Which token: user OAuth access token, S2S OAuth access token, bot token, SDK JWT?

Rule of thumb:

- REST calls generally require **OAuth access tokens** (S2S or user-based depending on endpoint).
- SDK join flows require **SDK JWT/signature** plus product-specific tokens (for some cases).

### 2. Confirm the Exact Endpoint and Operation

Token scope errors are endpoint-specific. Capture:

- HTTP method + path (example: `GET /v2/users/me/token?type=zak`)
- full error response body from Zoom
- the token’s `scope` string (if present in token response)

### 3. Map Endpoint -> Required Scopes

Do not guess scopes.

- Use `zoom-rest-api` references for the endpoint.
- Use `general/references/authorization-patterns.md` for RBAC and scope validation strategies.

### 4. Scope Changes Require Re-Consent (User OAuth)

If you add scopes after users already installed/authorized:

- existing users may need to reauthorize so the new scopes are granted

### 5. “Works on My Account” Usually Means One of These

- different account plan/features enabled
- missing admin role / privilege
- endpoint requires `:admin` scope but token only has user scope
- using the wrong `me` semantics for the app type

## Common Fix Patterns

- Add missing scopes, then reauthorize users (User OAuth).
- Ensure you are using the correct grant (S2S for backend automation across an account; User OAuth when acting on behalf of users).
- Validate that the endpoint actually supports your app type (some endpoints are not usable with some token types).

## Links

- `../references/authorization-patterns.md`
- `../../rest-api/troubleshooting/token-scope-playbook.md`
- `../../oauth/SKILL.md`

