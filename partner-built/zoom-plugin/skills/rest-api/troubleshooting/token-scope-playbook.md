---
title: "Token + Scope Playbook (Invalid Access Token / Missing Scopes)"
---

# Token + Scope Playbook (Invalid Access Token / Missing Scopes)

This covers the most common REST API forum failures:

- `401` / `403`
- `"Invalid access token"`
- `"does not contain scopes"`
- `"Access token is expired"`

## Step 1: Identify the OAuth App Type

- **Server-to-Server OAuth**: backend automation, no user consent screen
- **User OAuth (authorization_code / PKCE)**: per-user actions, user consent

Wrong app type is the #1 cause of “token works for endpoint A but not endpoint B”.

## Step 2: Verify `me` Keyword Rules

- User OAuth: use `users/me/...`
- S2S OAuth: do **not** use `me` (use a real userId/email where required)

If they get `1001 user does not exist` or “invalid access token” on `users/{id}` calls, this is often the reason.

## Step 3: Confirm Scopes Match the Endpoint

If the error says missing scopes, you must:

1. enable the scopes in Marketplace for the app
2. obtain a **new** token (tokens won’t gain scopes retroactively)

## Step 4: Token Expiry and Refresh

- S2S OAuth access tokens expire quickly; refresh on the server and cache with a buffer.
- User OAuth: refresh tokens and retry on `code=201` “Access token is expired.”

## Step 5: Confirm the Token’s Account/App

If tokens are created from multiple environments (dev/stage/prod) or accounts, mixups happen.

Ask for:
- the app type
- the account id (human-readable)
- the exact endpoint being called

