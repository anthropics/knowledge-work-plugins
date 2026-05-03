# Error Codes (Common Patterns)

## Auth Errors

- `Invalid access token`
  - wrong token type (bot token used for user API, or vice versa)
  - missing scopes
  - token expired / revoked

## Webhook Errors

- No events received:
  - endpoint not reachable publicly
  - verification failing
  - wrong event subscription / wrong app/account

## Message Rendering Issues

- Card not rendering:
  - invalid JSON payload
  - unsupported component types

