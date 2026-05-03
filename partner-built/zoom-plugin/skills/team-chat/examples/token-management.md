# Token Management (Team Chat API)

## Storage

Store per-user:

- `access_token`
- `refresh_token`
- `expires_at` (absolute timestamp)

## Refresh Strategy

- Refresh "just-in-time" when an API call fails with token expiry, or
- Refresh proactively when `now >= expires_at - 60s`.

## Pitfalls

- Refresh tokens can expire or be revoked (user removes app, admin blocks app).
- When you change scopes, existing users may need to reauthorize.

