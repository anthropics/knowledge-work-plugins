---
name: install-messenger
license: MIT
description: >
  Install the Intercom Messenger on a website or web application with
  secure JWT-based identity verification. Generates backend and frontend
  code for React, Next.js, Vue.js, Angular, Ember, and plain JavaScript.
  Supports Node.js, Python (Flask/Django), PHP, and Ruby backends. Use when
  the user asks to "install Intercom", "add the Intercom Messenger", "set up
  Intercom chat widget", "add customer chat to my website", or "integrate Intercom".
disable-model-invocation: true
argument-hint: "[framework]"
---

# Install Intercom Messenger

Help the user install the Intercom Messenger on their website or application with JWT-based identity verification. This is the secure default — it prevents user impersonation by cryptographically signing user identity on the server.

Only use the insecure (non-JWT) installation if the user explicitly asks for an "insecure installation". Never default to it.

## Requirements

Gather these from the user before proceeding:

1. **Workspace ID** (also called App ID) — A short alphanumeric string like `abc12345`.
   - Found on the [Intercom Messenger install page](https://app.intercom.com/a/apps/_/settings/channels/messenger/install)
   - Or in the URL bar: `https://app.intercom.com/a/apps/<workspace_id>/...`

2. **Identity Verification Secret** (also called Messenger API Secret) — Found on the [Messenger Security page](https://app.intercom.com/a/apps/_/settings/channels/messenger/security). This is the HMAC secret used to sign JWTs. It must never appear in frontend code.

Ask the user for both values. Do not proceed without the Workspace ID. If they don't have the Identity Verification Secret yet, direct them to the [Messenger Security page](https://app.intercom.com/a/apps/_/settings/channels/messenger/security) to enable it.

In all generated code, replace `YOUR_WORKSPACE_ID` with the user's actual Workspace ID. Do not leave placeholders — substitute the real values they provided.

## Installation Overview

The secure installation has two parts:

1. **Backend**: Create an API endpoint that generates a signed JWT for the current authenticated user
2. **Frontend**: Boot the Messenger with the JWT from the backend

Always implement both parts. The backend generates the JWT; the frontend passes it to the Messenger.

## Step 1: Backend — JWT Generation Endpoint

Create a server-side endpoint that the frontend calls to get a signed JWT for the currently authenticated user. The JWT must be signed with **HS256** using the Identity Verification Secret.

### Required JWT Claims

| Claim | Required | Description |
|-------|----------|-------------|
| `user_id` | Yes | Stable, unique identifier for the user. Must match across sessions. |
| `email` | Recommended | User's email address |
| `name` | Recommended | User's display name |
| `exp` | Recommended | Expiration timestamp (Unix seconds). Use short-lived tokens — 2 hours is reasonable. |

**Important**: `user_id` is mandatory. If multiple users share the same email and you only pass `email` without `user_id`, Intercom will reject the request with a conflict error.

### Node.js / Express Example

```javascript
const jwt = require('jsonwebtoken');

const INTERCOM_SECRET = process.env.INTERCOM_IDENTITY_SECRET; // Never hardcode this

app.get('/api/intercom-jwt', requireAuth, (req, res) => {
  const token = jwt.sign(
    {
      user_id: req.user.id,
      email: req.user.email,
      name: req.user.name,
      exp: Math.floor(Date.now() / 1000) + (2 * 60 * 60), // 2 hours
    },
    INTERCOM_SECRET,
    { algorithm: 'HS256' }
  );

  res.json({ token });
});
```

For Python (Flask/Django), PHP, and Ruby/Rails examples, see `references/backend-examples.md`. The pattern is identical across languages.

Adapt the example to the user's backend language and framework. The key requirements are:
- The endpoint is authenticated (only the logged-in user can get their own JWT)
- The secret comes from an environment variable, never hardcoded
- The token includes `user_id` and has a short expiration

## Step 2: Frontend — Boot Messenger with JWT

The frontend fetches the JWT from the backend and passes it to the Messenger via `intercom_user_jwt`.

### Basic JavaScript (No Framework)

Add before the closing `</body>` tag:

```html
<script>
  // Fetch JWT from your backend, then boot the Messenger
  fetch('/api/intercom-jwt', { credentials: 'include' })
    .then(res => res.json())
    .then(({ token }) => {
      window.Intercom('boot', {
        app_id: 'YOUR_WORKSPACE_ID',
        intercom_user_jwt: token,
      });
    });
</script>
<script>
  (function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/YOUR_WORKSPACE_ID';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
</script>
```

### Anonymous Visitors

For unauthenticated pages, boot without a JWT: `Intercom('boot', { app_id: 'YOUR_WORKSPACE_ID' })`. Intercom tracks anonymous visitors as leads.

## Framework-Specific Installation

If the user is using React, Next.js, Vue.js, Angular, Ember, or another SPA framework, refer to `references/framework-guides.md` for JWT-integrated installation code. Ask the user what framework they are using if it is not obvious from their codebase.

After reading the framework guide, adapt the code to the user's specific project structure — find their main layout component, app entry point, or equivalent, and integrate the Messenger there.

## Regional Data Centers

Most Intercom workspaces are in the US region, which is the default — no `api_base` is needed. Only add `api_base` if the user's workspace is hosted in EU or Australia:

| Region | `api_base` | Required? |
|--------|------------|-----------|
| US (default) | *(not needed)* | No |
| EU (Ireland) | `https://api-iam.eu.intercom.io` | Yes |
| Australia | `https://api-iam.au.intercom.io` | Yes |

If the user mentions EU or Australian hosting, GDPR compliance, or data residency requirements, add the appropriate `api_base` to every `Intercom('boot', ...)` call. Otherwise, omit it.

## Security Best Practices

### Logout and Shutdown

When a user logs out, shut down the Messenger to clear session cookies and prevent data leakage:

```javascript
// Call this in your logout handler, BEFORE clearing session data
Intercom('shutdown');
```

After shutdown, re-initialize for the next user or as anonymous:

```javascript
Intercom('boot', {
  app_id: 'YOUR_WORKSPACE_ID',
});
```

Always include the shutdown call. Skipping it leaks conversation data between users on shared devices.

### Token Expiration

Set short JWT expiration times — two hours is a good default. To refresh an expired token, re-fetch the JWT from the backend and call `Intercom('boot', ...)` again with the new token.

## Troubleshooting

### JWT Library Not Installed
Error: `Cannot find module 'jsonwebtoken'` (Node.js), `ModuleNotFoundError: No module named 'jwt'` (Python), or `LoadError: cannot load such file -- jwt` (Ruby)
Solution: Install the JWT library for the user's language — `npm install jsonwebtoken`, `pip install PyJWT`, or `gem install jwt`.

### Wrong Identity Verification Secret
Symptom: Messenger loads but shows "Identity verification failed" or user attributes don't appear.
Cause: The secret used to sign JWTs doesn't match the workspace's Identity Verification Secret.
Solution: Verify the secret on the [Messenger Security page](https://app.intercom.com/a/apps/_/settings/channels/messenger/security). Ensure the environment variable holds the correct value for this workspace.

### Plan Doesn't Support Identity Verification
Symptom: Identity Verification Secret not available in Intercom settings.
Cause: Identity verification is a paid feature not available on all Intercom plans.
Solution: Check the workspace's Intercom plan on the [Messenger Security page](https://app.intercom.com/a/apps/_/settings/channels/messenger/security). If identity verification is unavailable, the user may need to upgrade or use the insecure installation (with explicit acknowledgment of the security trade-off).

### JWT `exp` in the Past
Symptom: Messenger rejects the token immediately after creation.
Cause: Server clock is wrong or `exp` calculation is incorrect.
Solution: Check the server's system time (`date` command). Ensure NTP is configured. Verify the `exp` value is a future Unix timestamp in seconds (not milliseconds).

### CORS Errors on JWT Endpoint
Symptom: Browser console shows `Access-Control-Allow-Origin` errors when fetching the JWT.
Cause: The backend JWT endpoint doesn't allow requests from the frontend's origin.
Solution: Configure CORS on the JWT endpoint to allow the frontend origin. For Express: `cors({ origin: 'https://your-app.com', credentials: true })`. For other frameworks, add the appropriate CORS headers.

## Single-Page App (SPA) Route Changes

In SPAs, call `Intercom('update')` after each client-side route change. See `references/framework-guides.md` for framework-specific placement (React Router, Next.js, Vue Router, Angular, Ember).

## Third-Party Integrations

Intercom also supports code-free installation via WordPress, Shopify, Google Tag Manager, and Segment. Direct users to the [Messenger install page](https://app.intercom.com/a/apps/_/settings/channels/messenger/install) for setup instructions.

## Verifying the Installation

After generating the code, verify the installation before considering the task complete.

**With browser automation** (Playwright MCP, playwright-cli, etc.): Navigate to the app, confirm `typeof window.Intercom === 'function'`, check the script tag for `widget.intercom.io/widget/WORKSPACE_ID`, and verify the JWT endpoint returns HTTP 200 with `{ "token": "..." }` for an authenticated user. Note: in headless/sandboxed environments, the widget iframe may not load due to CDN restrictions — this is not a code problem.

**With Intercom MCP tools** (`search_contacts`): After a user logs in and loads a page with the Messenger, search for the user by name or `external_id`. Confirm the contact exists with `role: "user"` and the correct `external_id` — this proves the full chain from JWT signing to Intercom identity creation.

**Manual verification** (instruct the user): Open the app in a browser, confirm the Messenger bubble appears, log in, click the bubble, send a test message, then check the [Intercom Inbox](https://app.intercom.com/a/inbox/_/inbox/) to confirm the conversation appears attributed to the correct user.

## Post-Installation: Enforce JWT Authentication

After the code is deployed, the user must enable and enforce identity verification in Intercom. Direct them to complete these steps:

1. Go to the [Messenger Security page](https://app.intercom.com/a/apps/_/settings/channels/messenger/security)
2. **Enable Identity Verification** if not already enabled — this activates JWT-based authentication for the Messenger
3. **Enforce Identity Verification** — once enabled and confirmed working, switch to "Enforced" mode so that unauthenticated Messenger sessions are rejected
4. **Mark identifying attributes as protected** — on the same page, mark attributes like email, phone, and account IDs as protected so only server-signed JWTs can set them

This is a critical step. Without enforcement, the JWT signing is optional and users can still be impersonated via the browser console. Enforcement ensures only server-signed identities are accepted.

## Insecure Installation (Only If Explicitly Requested)

If the user explicitly asks for an "insecure installation" (no JWT, no identity verification), provide the basic snippet that passes user attributes directly in `intercomSettings` without server-side signing:

```html
<script>
  window.intercomSettings = {
    app_id: "YOUR_WORKSPACE_ID",
    name: "Jane Doe",
    email: "jane@example.com",
    created_at: 1312182000
  };
</script>
<script>
  (function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/YOUR_WORKSPACE_ID';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
</script>
```

Warn the user that this is insecure: anyone can impersonate any user by modifying the `email` or `name` values in the browser console. Recommend switching to JWT-based authentication for production use.
