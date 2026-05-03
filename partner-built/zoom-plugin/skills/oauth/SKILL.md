---
name: zoom-oauth
description: Reference skill for Zoom authentication. Use after routing to an auth workflow when choosing app credentials, grant types, scopes, token refresh behavior, or debugging Zoom OAuth failures.
user-invocable: false
triggers:
  - zoom oauth
  - zoom authentication
  - zoom authorization
  - server to server oauth
  - s2s oauth
  - zoom access token
  - zoom refresh token
  - authorization code flow
  - device authorization
  - pkce
  - zoom api authentication
  - oauth error 4709
  - oauth error 4733
  - oauth error 4735
  - redirect uri mismatch
---

# Zoom OAuth

Background reference for Zoom auth and token lifecycle behavior. Prefer `setup-zoom-oauth` first, then use this skill for the exact flow, scope, and error details.

# Zoom OAuth

Authentication and authorization for Zoom APIs.

## 📖 Complete Documentation

For comprehensive guides, production patterns, and troubleshooting, see **Integrated Index section below**.

Quick navigation:
- **[5-Minute Runbook](RUNBOOK.md)** - Preflight checks before deep debugging
- **[OAuth Flows](concepts/oauth-flows.md)** - Which flow to use and how each works
- **[Token Lifecycle](concepts/token-lifecycle.md)** - Expiration, refresh, and revocation
- **[Production Examples](examples/s2s-oauth-redis.md)** - Redis caching, MySQL storage, auto-refresh
- **[Troubleshooting](troubleshooting/common-errors.md)** - Error codes 4700-4741

## Prerequisites

- Zoom app created in [Marketplace](https://marketplace.zoom.us/)
- Client ID and Client Secret
- For S2S OAuth: Account ID

## Four Authorization Use Cases

| Use Case | App Type | Grant Type | Industry Name |
|----------|----------|------------|---------------|
| **Account Authorization** | Server-to-Server | `account_credentials` | Client Credentials Grant, M2M, Two-legged OAuth |
| **User Authorization** | General | `authorization_code` | Authorization Code Grant, Three-legged OAuth |
| **Device Authorization** | General | `urn:ietf:params:oauth:grant-type:device_code` | Device Authorization Grant (RFC 8628) |
| **Client Authorization** | General | `client_credentials` | Client Credentials Grant (chatbot-scoped) |

### Industry Terminology

| Term | Meaning |
|------|---------|
| **Two-legged OAuth** | No user involved (client ↔ server) |
| **Three-legged OAuth** | User involved (user ↔ client ↔ server) |
| **M2M** | Machine-to-Machine (backend services) |
| **Public client** | Can't keep secrets (mobile, SPA) → use PKCE |
| **Confidential client** | Can keep secrets (backend servers) |
| **PKCE** | Proof Key for Code Exchange (RFC 7636), pronounced "pixy" |

### Which Flow Should I Use?

```
                              ┌─────────────────────┐
                              │  What are you       │
                              │  building?          │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │  Backend        │  │  App for other  │  │  Chatbot only   │
          │  automation     │  │  users/accounts │  │  (Team Chat)    │
          │  (your account) │  │                 │  │                 │
          └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
                   │                    │                    │
                   ▼                    │                    ▼
          ┌─────────────────┐           │           ┌─────────────────┐
          │    ACCOUNT      │           │           │     CLIENT      │
          │   (S2S OAuth)   │           │           │   (Chatbot)     │
          └─────────────────┘           │           └─────────────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │  Does device have   │
                              │  a browser?         │
                              └──────────┬──────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │ NO                         YES│
                         ▼                               ▼
          ┌─────────────────────────┐         ┌─────────────────┐
          │        DEVICE           │         │      USER       │
          │     (Device Flow)       │         │  (Auth Code)    │
          │                         │         │                 │
          │ Examples:               │         │ + PKCE if       │
          │ • Smart TV              │         │   public client │
          │ • Meeting SDK device    │         │                 │
          └─────────────────────────┘         └─────────────────┘
```

---

## Account Authorization (Server-to-Server OAuth)

For backend automation without user interaction.

### Request Access Token

```bash
POST https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "user:read:user:admin",
  "api_url": "https://api.zoom.us"
}
```

### Refresh

Access tokens expire after **1 hour**. No separate refresh flow - just request a new token.

---

## User Authorization (Authorization Code Flow)

For apps that act on behalf of users.

### Step 1: Redirect User to Authorize

```
https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}
```

Use `https://zoom.us/oauth/authorize` for consent, but `https://zoom.us/oauth/token` for token exchange.

**Optional Parameters:**

| Parameter | Description |
|-----------|-------------|
| `state` | CSRF protection, maintains state through flow |
| `code_challenge` | For PKCE (see below) |
| `code_challenge_method` | `S256` or `plain` (default: plain) |

### Step 2: User Authorizes

- User signs in and grants permission
- Redirects to `redirect_uri` with authorization code:
  ```
  https://example.com/?code={AUTHORIZATION_CODE}
  ```

### Step 3: Exchange Code for Token

```bash
POST https://zoom.us/oauth/token?grant_type=authorization_code&code={CODE}&redirect_uri={REDIRECT_URI}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

**With PKCE:** Add `code_verifier` parameter.

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "refresh_token": "eyJ...",
  "expires_in": 3600,
  "scope": "user:read:user",
  "api_url": "https://api.zoom.us"
}
```

### Refresh Token

```bash
POST https://zoom.us/oauth/token?grant_type=refresh_token&refresh_token={REFRESH_TOKEN}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

- Access tokens expire after **1 hour**
- Refresh token lifetime can vary; ~90 days is common for some user-based flows. Treat it as configuration/behavior that can change and rely on runtime errors + re-auth fallback.
- Always use the latest refresh token for the next request
- If refresh token expires, redirect user to authorization URL to restart flow

### User-Level vs Account-Level Apps

| Type | Who Can Authorize | Scope Access |
|------|-------------------|--------------|
| **User-level** | Any individual user | Scoped to themselves |
| **Account-level** | User with admin permissions | Account-wide access (admin scopes) |

---

## Device Authorization (Device Flow)

For devices without browsers (e.g., Meeting SDK apps).

### Prerequisites

Enable "Use App on Device" in: Features > Embed > Enable Meeting SDK

### Step 1: Request Device Code

```bash
POST https://zoom.us/oauth/devicecode?client_id={CLIENT_ID}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "device_code": "DEVICE_CODE",
  "user_code": "abcd1234",
  "verification_uri": "https://zoom.us/oauth_device",
  "verification_uri_complete": "https://zoom.us/oauth/device/complete/{CODE}",
  "expires_in": 900,
  "interval": 5
}
```

### Step 2: User Authorization

Direct user to:
- `verification_uri` and display `user_code` for manual entry, OR
- `verification_uri_complete` (user code prefilled)

User signs in and allows the app.

### Step 3: Poll for Token

Poll at the `interval` (5 seconds) until user authorizes:

```bash
POST https://zoom.us/oauth/token?grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code={DEVICE_CODE}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "refresh_token": "eyJ...",
  "expires_in": 3599,
  "scope": "user:read:user user:read:token",
  "api_url": "https://api.zoom.us"
}
```

### Polling Responses

| Response | Meaning | Action |
|----------|---------|--------|
| Token returned | User authorized | Store tokens, done |
| `error: authorization_pending` | User hasn't authorized yet | Keep polling at interval |
| `error: slow_down` | Polling too fast | Increase interval by 5 seconds |
| `error: expired_token` | Device code expired (15 min) | Restart flow from Step 1 |
| `error: access_denied` | User denied authorization | Handle denial, don't retry |

### Polling Implementation

```javascript
async function pollForToken(deviceCode, interval) {
  while (true) {
    await sleep(interval * 1000);
    
    try {
      const response = await axios.post(
        `https://zoom.us/oauth/token?grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=${deviceCode}`,
        null,
        { headers: { 'Authorization': `Basic ${credentials}` } }
      );
      return response.data; // Success - got tokens
    } catch (error) {
      const err = error.response?.data?.error;
      if (err === 'authorization_pending') continue;
      if (err === 'slow_down') { interval += 5; continue; }
      throw error; // expired_token or access_denied
    }
  }
}
```

### Refresh

Same as User Authorization. If refresh token expires, restart device flow from Step 1.

---

## Client Authorization (Chatbot)

For chatbot message operations only.

### Request Token

```bash
POST https://zoom.us/oauth/token?grant_type=client_credentials

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "imchat:bot",
  "api_url": "https://api.zoom.us"
}
```

### Refresh

Tokens expire after **1 hour**. No refresh flow - just request a new token.

---

## Using Access Tokens

### Call API

```bash
GET https://api.zoom.us/v2/users/me

Headers:
Authorization: Bearer {ACCESS_TOKEN}
```

### Me Context

Replace `userID` with `me` to target the token's associated user:

| Endpoint | Methods |
|----------|---------|
| `/v2/users/me` | GET, PATCH |
| `/v2/users/me/token` | GET |
| `/v2/users/me/meetings` | GET, POST |

---

## Revoke Access Token

Works for all authorization types.

```bash
POST https://zoom.us/oauth/revoke?token={ACCESS_TOKEN}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "status": "success"
}
```

---

## PKCE (Proof Key for Code Exchange)

For public clients that can't securely store secrets (mobile apps, SPAs, desktop apps).

### When to Use PKCE

| Client Type | Use PKCE? | Why |
|-------------|-----------|-----|
| Mobile app | **Yes** | Can't securely store client secret |
| Single Page App (SPA) | **Yes** | JavaScript is visible to users |
| Desktop app | **Yes** | Binary can be decompiled |
| Meeting SDK (client-side) | **Yes** | Runs on user's device |
| Backend server | Optional | Can keep secrets, but PKCE adds security |

### How PKCE Works

```
┌──────────┐                              ┌──────────┐                    ┌──────────┐
│  Client  │                              │   Zoom   │                    │   Zoom   │
│   App    │                              │  Auth    │                    │  Token   │
└────┬─────┘                              └────┬─────┘                    └────┬─────┘
     │                                         │                              │
     │ 1. Generate code_verifier (random)      │                              │
     │ 2. Create code_challenge = SHA256(verifier)                            │
     │                                         │                              │
     │ ─────── /authorize + code_challenge ──► │                              │
     │                                         │                              │
     │ ◄────── authorization_code ──────────── │                              │
     │                                         │                              │
     │ ─────────────── /token + code_verifier ─┼────────────────────────────► │
     │                                         │                              │
     │                                         │     Verify: SHA256(verifier) │
     │                                         │            == challenge      │
     │                                         │                              │
     │ ◄───────────────────────────────────────┼─────── access_token ──────── │
     │                                         │                              │
```

### Implementation (Node.js)

```javascript
const crypto = require('crypto');

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto.createHash('sha256').update(verifier).digest('base64url');
  return { verifier, challenge };
}

const pkce = generatePKCE();

const authUrl = `https://zoom.us/oauth/authorize?` +
  `response_type=code&` +
  `client_id=${CLIENT_ID}&` +
  `redirect_uri=${REDIRECT_URI}&` +
  `code_challenge=${pkce.challenge}&` +
  `code_challenge_method=S256`;

// Store pkce.verifier in session for callback
```

### Token Exchange with PKCE

```bash
POST https://zoom.us/oauth/token?grant_type=authorization_code&code={CODE}&redirect_uri={REDIRECT_URI}&code_verifier={VERIFIER}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

---

## Deauthorization

When a user removes your app, Zoom sends a webhook to your Deauthorization Notification Endpoint URL.

### Webhook Event

```json
{
  "event": "app_deauthorized",
  "event_ts": 1740439732278,
  "payload": {
    "account_id": "ACCOUNT_ID",
    "user_id": "USER_ID",
    "signature": "SIGNATURE",
    "deauthorization_time": "2019-06-17T13:52:28.632Z",
    "client_id": "CLIENT_ID"
  }
}
```

### Requirements

- **Delete all associated user data** after receiving this event
- **Verify webhook signature** (use secret token, verification token deprecated Oct 2023)
- Only public apps receive deauthorization webhooks (not private/dev apps)

---

## Pre-Approval Flow

Some Zoom accounts require Marketplace admin pre-approval before users can authorize apps.

- Users can request pre-approval from their admin
- Account-level apps (admin scopes) require appropriate role permissions

---

## Active Apps Notifier (AAN)

In-meeting feature showing apps with real-time access to content.

- Displays icon + tooltip with app info, content type being accessed, approving account
- Supported: Zoom client 5.6.7+, Meeting SDK 5.9.0+

---

## OAuth Scopes

### Scope Types

| Type | Description | For |
|------|-------------|-----|
| **Classic scopes** | Legacy scopes (user, admin, master levels) | Existing apps |
| **Granular scopes** | New fine-grained scopes with optional support | New apps |

### Classic Scopes

For previously-created apps. Three levels:
- **User-level**: Access to individual user's data
- **Admin-level**: Account-wide access, requires admin role
- **Master-level**: For master-sub account setups, requires account owner

Full list: https://developers.zoom.us/docs/integrations/oauth-scopes/

### Granular Scopes

For new apps. Format: `<service>:<action>:<data_claim>:<access>`

| Component | Values |
|-----------|--------|
| **service** | `meeting`, `webinar`, `user`, `recording`, etc. |
| **action** | `read`, `write`, `update`, `delete` |
| **data_claim** | Data category (e.g., `participants`, `settings`) |
| **access** | empty (user), `admin`, `master` |

Example: `meeting:read:list_meetings:admin`

Full list: https://developers.zoom.us/docs/integrations/oauth-scopes-granular/

### Optional Scopes

Granular scopes can be marked as **optional** - users choose whether to grant them.

**Basic authorization** (uses build flow defaults):
```
https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}
```

**Advanced authorization** (custom scopes per request):
```
https://zoom.us/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={required_scopes}&optional_scope={optional_scopes}
```

**Include previously granted scopes:**
```
https://zoom.us/oauth/authorize?...&include_granted_scopes&scope={additional_scopes}
```

### Migrating Classic to Granular

1. Manage > select app > edit
2. Scope page > Development tab > click **Migrate**
3. Review auto-assigned granular scopes, remove unnecessary, mark optional
4. Test
5. Production tab > click **Migrate**

**Notes:**
- No review needed if only migrating or reducing scopes
- Existing user tokens continue with classic scope values until re-authorization
- New users get granular scopes after migration

---

## Common Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 4700 | Token cannot be empty | Check Authorization header has valid token |
| 4702/4704 | Invalid client | Verify Client ID and Client Secret |
| 4705 | Grant type not supported | Use: `account_credentials`, `authorization_code`, `urn:ietf:params:oauth:grant-type:device_code`, or `client_credentials` |
| 4706 | Client ID or secret missing | Add credentials to header or request params |
| 4709 | Redirect URI mismatch | Ensure redirect_uri matches app configuration exactly (including trailing slash) |
| 4711 | Refresh token invalid | Token scopes don't match client scopes |
| 4717 | App has been disabled | Contact Zoom support |
| 4733 | Code is expired | Authorization codes expire in 5 minutes - restart flow |
| 4734 | Invalid authorization code | Regenerate authorization code |
| 4735 | Owner of token does not exist | User was removed from account - re-authorize |
| 4741 | Token has been revoked | Use the most recent token from latest authorization |

See `references/oauth-errors.md` for complete error list.

---

## Quick Reference

| Flow | Grant Type | Token Expiry | Refresh |
|------|------------|--------------|---------|
| Account (S2S) | `account_credentials` | 1 hour | Request new token |
| User | `authorization_code` | 1 hour | Use refresh_token (90 day expiry) |
| Device | `urn:ietf:params:oauth:grant-type:device_code` | 1 hour | Use refresh_token (90 day expiry) |
| Client (Chatbot) | `client_credentials` | 1 hour | Request new token |

---

## Demo Guidance

If you build an OAuth demo app, document its runtime base URL in that demo project's own
README or `.env.example`, not in this shared skill.

## Resources

- **OAuth docs**: https://developers.zoom.us/docs/integrations/oauth/
- **S2S OAuth docs**: https://developers.zoom.us/docs/internal-apps/s2s-oauth/
- **PKCE blog**: https://developers.zoom.us/blog/pcke-oauth-with-postman-rest-api/
- **Classic scopes**: https://developers.zoom.us/docs/integrations/oauth-scopes/
- **Granular scopes**: https://developers.zoom.us/docs/integrations/oauth-scopes-granular/

---

## Integrated Index

_This section was migrated from `SKILL.md`._

## Quick Start Path

**If you're new to Zoom OAuth, follow this order:**

1. **Run preflight checks first** → [RUNBOOK.md](RUNBOOK.md)

2. **Choose your OAuth flow** → [concepts/oauth-flows.md](concepts/oauth-flows.md)
   - 4 flows: S2S (backend), User (SaaS), Device (no browser), Chatbot
   - Decision matrix: Which flow fits your use case?

3. **Understand token lifecycle** → [concepts/token-lifecycle.md](concepts/token-lifecycle.md)
   - **CRITICAL**: How tokens expire, refresh, and revoke
   - Common pitfalls: refresh token rotation

4. **Implement your flow** → Jump to examples:
   - Backend automation → [examples/s2s-oauth-redis.md](examples/s2s-oauth-redis.md)
   - SaaS app → [examples/user-oauth-mysql.md](examples/user-oauth-mysql.md)
   - Mobile/SPA → [examples/pkce-implementation.md](examples/pkce-implementation.md)
   - Device (TV/kiosk) → [examples/device-flow.md](examples/device-flow.md)

5. **Fix redirect URI issues** → [troubleshooting/redirect-uri-issues.md](troubleshooting/redirect-uri-issues.md)
   - Most common OAuth error: Redirect URI mismatch

6. **Implement token refresh** → [examples/token-refresh.md](examples/token-refresh.md)
   - Automatic middleware pattern
   - Handle refresh token rotation

7. **Troubleshoot errors** → [troubleshooting/common-errors.md](troubleshooting/common-errors.md)
   - Error code tables (4700-4741 range)
   - Quick diagnostic workflow

---

## Documentation Structure

```
oauth/
├── SKILL.md                           # Main skill overview
├── SKILL.md                           # This file - navigation guide
│
├── concepts/                          # Core OAuth concepts
│   ├── oauth-flows.md                # 4 flows: S2S, User, Device, Chatbot
│   ├── token-lifecycle.md            # Expiration, refresh, revocation
│   ├── pkce.md                       # PKCE security for public clients
│   ├── scopes-architecture.md        # Classic vs Granular scopes
│   └── state-parameter.md            # CSRF protection with state
│
├── examples/                          # Complete working code
│   ├── s2s-oauth-basic.md            # S2S OAuth minimal example
│   ├── s2s-oauth-redis.md            # S2S OAuth with Redis caching (production)
│   ├── user-oauth-basic.md           # User OAuth minimal example
│   ├── user-oauth-mysql.md           # User OAuth with MySQL + encryption (production)
│   ├── device-flow.md                # Device authorization flow
│   ├── pkce-implementation.md        # PKCE for SPAs/mobile apps
│   └── token-refresh.md              # Auto-refresh middleware pattern
│
├── troubleshooting/                   # Problem solving guides
│   ├── common-errors.md              # Error codes 4700-4741
│   ├── redirect-uri-issues.md        # Most common OAuth error
│   ├── token-issues.md               # Expired, revoked, invalid tokens
│   └── scope-issues.md               # Scope mismatch errors
│
└── references/                        # Reference documentation
    ├── oauth-errors.md                # Complete error code reference
    ├── classic-scopes.md              # Classic scope reference
    └── granular-scopes.md             # Granular scope reference
```

---

## By Use Case

### I want to automate Zoom tasks on my own account
1. [OAuth Flows](concepts/oauth-flows.md#server-to-server-s2s-oauth) - S2S OAuth explained
2. [S2S OAuth Redis](examples/s2s-oauth-redis.md) - Production pattern with Redis caching
3. [Token Lifecycle](concepts/token-lifecycle.md) - 1hr token, no refresh

### I want to build a SaaS app for other Zoom users
1. [OAuth Flows](concepts/oauth-flows.md#user-authorization-oauth) - User OAuth explained
2. [User OAuth MySQL](examples/user-oauth-mysql.md) - Production pattern with encryption
3. [Token Refresh](examples/token-refresh.md) - Automatic refresh middleware
4. [Redirect URI Issues](troubleshooting/redirect-uri-issues.md) - Fix most common error

### I want to build a mobile or SPA app
1. [PKCE](concepts/pkce.md) - Why PKCE is required for public clients
2. [PKCE Implementation](examples/pkce-implementation.md) - Complete code example
3. [State Parameter](concepts/state-parameter.md) - CSRF protection

### I want to build an app for devices without browsers (TV, kiosk)
1. [OAuth Flows](concepts/oauth-flows.md#device-authorization-flow) - Device flow explained
2. [Device Flow Example](examples/device-flow.md) - Complete polling implementation
3. [Common Errors](troubleshooting/common-errors.md) - Device-specific errors

### I'm building a Team Chat bot
1. [OAuth Flows](concepts/oauth-flows.md#client-authorization-chatbot) - Chatbot flow explained
2. [S2S OAuth Basic](examples/s2s-oauth-basic.md) - Similar pattern, different grant type
3. [Scopes Architecture](concepts/scopes-architecture.md) - Chatbot-specific scopes

### I'm getting redirect URI errors (4709)
1. [Redirect URI Issues](troubleshooting/redirect-uri-issues.md) - **START HERE!**
2. [Common Errors](troubleshooting/common-errors.md#4709-redirect-uri-mismatch) - Error details
3. [User OAuth Basic](examples/user-oauth-basic.md) - See correct pattern

### I'm getting token errors (4700-4741)
1. [Token Issues](troubleshooting/token-issues.md) - Diagnostic workflow
2. [Token Lifecycle](concepts/token-lifecycle.md) - Understand expiration
3. [Token Refresh](examples/token-refresh.md) - Implement auto-refresh
4. [Common Errors](troubleshooting/common-errors.md) - Error code tables

### I'm getting scope errors (4711)
1. [Scope Issues](troubleshooting/scope-issues.md) - Mismatch causes
2. [Scopes Architecture](concepts/scopes-architecture.md) - Classic vs Granular
3. [Classic Scopes](references/classic-scopes.md) - Complete scope reference
4. [Granular Scopes](references/granular-scopes.md) - Granular scope reference

### I need to refresh tokens
1. [Token Lifecycle](concepts/token-lifecycle.md#refresh-strategy) - When to refresh
2. [Token Refresh](examples/token-refresh.md) - Middleware pattern
3. [Token Issues](troubleshooting/token-issues.md#refresh-token-problems) - Common mistakes

### I want to understand the difference between Classic and Granular scopes
1. [Scopes Architecture](concepts/scopes-architecture.md) - **Complete comparison**
2. [Classic Scopes](references/classic-scopes.md) - `resource:level` format
3. [Granular Scopes](references/granular-scopes.md) - `service:action:data_claim:access` format

### I need to secure my OAuth implementation
1. [PKCE](concepts/pkce.md) - Public client security
2. [State Parameter](concepts/state-parameter.md) - CSRF protection
3. [User OAuth MySQL](examples/user-oauth-mysql.md#token-encryption) - Token encryption at rest

### I want to migrate from JWT app to S2S OAuth
1. [S2S OAuth Redis](examples/s2s-oauth-redis.md) - Modern replacement
2. [Token Lifecycle](concepts/token-lifecycle.md) - Different token behavior

> **Note**: JWT App Type was deprecated in June 2023. Migrate to S2S OAuth for server-to-server automation.

---

## Most Critical Documents

### 1. OAuth Flows (DECISION DOCUMENT)
**[concepts/oauth-flows.md](concepts/oauth-flows.md)**

Understand which of the 4 flows to use:
- **S2S OAuth**: Backend automation (your account)
- **User OAuth**: SaaS apps (users authorize you)
- **Device Flow**: Devices without browsers
- **Chatbot**: Team Chat bots only

### 2. Token Lifecycle (MOST COMMON ISSUE)
**[concepts/token-lifecycle.md](concepts/token-lifecycle.md)**

99% of OAuth issues stem from misunderstanding:
- Token expiration (1 hour for all flows)
- Refresh token rotation (must save new refresh token)
- Revocation behavior (invalidates all tokens)

### 3. Redirect URI Issues (MOST COMMON ERROR)
**[troubleshooting/redirect-uri-issues.md](troubleshooting/redirect-uri-issues.md)**

Error 4709 ("Redirect URI mismatch") is the #1 OAuth error.
Must match EXACTLY (including trailing slash, http vs https).

---

## Key Learnings

### Critical Discoveries:

1. **Refresh Token Rotation**
   - Each refresh returns a NEW refresh token
   - Old refresh token becomes invalid
   - Failure to save new token causes 4735 errors
   - See: [Token Refresh](examples/token-refresh.md)

2. **S2S OAuth Uses Redis, User OAuth Uses Database**
   - S2S: Single token for entire account → Redis (ephemeral)
   - User: Per-user tokens → Database (persistent)
   - See: [S2S OAuth Redis](examples/s2s-oauth-redis.md) vs [User OAuth MySQL](examples/user-oauth-mysql.md)

3. **Redirect URI Must Match EXACTLY**
   - Trailing slash matters: `/callback` ≠ `/callback/`
   - Protocol matters: `http://` ≠ `https://`
   - Port matters: `:3000` ≠ `:3001`
   - See: [Redirect URI Issues](troubleshooting/redirect-uri-issues.md)

4. **PKCE Required for Public Clients**
   - Mobile apps CANNOT keep secrets
   - SPAs CANNOT keep secrets
   - PKCE prevents authorization code interception
   - See: [PKCE](concepts/pkce.md)

5. **State Parameter Prevents CSRF**
   - Generate random state before redirect
   - Store in session
   - Verify on callback
   - See: [State Parameter](concepts/state-parameter.md)

6. **Token Storage Must Be Encrypted**
   - NEVER store tokens in plain text
   - Use AES-256 minimum
   - See: [User OAuth MySQL](examples/user-oauth-mysql.md#token-encryption)

7. **JWT App Type is Deprecated (June 2023)**
   - No new JWT apps can be created
   - Existing apps still work but will eventually be sunset
   - Migrate to S2S OAuth or User OAuth

8. **Scope Levels Determine Authorization Requirements**
   - No suffix (user-level): Any user can authorize
   - `:admin`: Requires admin role
   - `:master`: Requires account owner (multi-account)
   - See: [Scopes Architecture](concepts/scopes-architecture.md)

9. **Authorization Codes Expire in 5 Minutes**
   - Exchange code for token immediately
   - Don't cache authorization codes
   - See: [Token Lifecycle](concepts/token-lifecycle.md#authorization-code-expiration)

10. **Device Flow Requires Polling**
    - Poll at interval returned by `/devicecode` (usually 5s)
    - Handle `authorization_pending`, `slow_down`, `expired_token`
    - See: [Device Flow](examples/device-flow.md)

---

## Quick Reference

### "Which OAuth flow should I use?"
→ [OAuth Flows](concepts/oauth-flows.md)

### "Redirect URI mismatch error (4709)"
→ [Redirect URI Issues](troubleshooting/redirect-uri-issues.md)

### "Token expired or invalid"
→ [Token Issues](troubleshooting/token-issues.md)

### "Refresh token invalid (4735)"
→ [Token Refresh](examples/token-refresh.md) - Must save new refresh token

### "Scope mismatch error (4711)"
→ [Scope Issues](troubleshooting/scope-issues.md)

### "How do I secure my OAuth app?"
→ [PKCE](concepts/pkce.md) + [State Parameter](concepts/state-parameter.md)

### "How do I implement auto-refresh?"
→ [Token Refresh](examples/token-refresh.md)

### "What's the difference between Classic and Granular scopes?"
→ [Scopes Architecture](concepts/scopes-architecture.md)

### "What error code means what?"
→ [Common Errors](troubleshooting/common-errors.md)

---

## Document Version

Based on **Zoom OAuth API v2** (2024+)

**Deprecated:** JWT App Type (June 2023)

---

**Happy coding!**

Remember: Start with [OAuth Flows](concepts/oauth-flows.md) to understand which flow fits your use case!

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.
