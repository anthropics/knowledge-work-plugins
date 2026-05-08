# OAuth Issues (Team Chat API)

## "Invalid redirect" / redirect mismatch

- The redirect URL in the token exchange must exactly match what's configured in Marketplace.
- Keep endpoint split correct:
  - authorize: `https://zoom.us/oauth/authorize`
  - token exchange: `https://zoom.us/oauth/token`

## "Invalid access token, does not contain scopes"

- Add the scope in Marketplace.
- Ensure the user re-authorizes after scope changes.
- Confirm you're using the user token for Team Chat API calls.

## Token Expired

- Refresh access tokens using the refresh token.
- If refresh fails, the user likely needs to reauthorize.

## Callback succeeds but app still has no token

- Verify callback route actually exchanges `code` server-side.
- Verify `state` is validated and not expired.
- Verify token is persisted where your UI expects it (session/database/local storage for demo).
