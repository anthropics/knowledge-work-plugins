# Common Errors

See [../references/oauth-errors.md](../references/oauth-errors.md) for complete error reference.

Common OAuth error codes: 4700-4741

For specific error details, consult the error reference documentation.

## High-Frequency Endpoint Mistake

- Use `https://zoom.us/oauth/authorize` for user consent.
- Use `https://zoom.us/oauth/token` for token exchange.
- If token calls return HTML or 404, check that you are not calling `/oauth/token`.
