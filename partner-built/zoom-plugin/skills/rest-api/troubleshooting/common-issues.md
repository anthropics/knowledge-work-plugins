# Common Issues (REST API)

This complements `common-errors.md` (HTTP codes and Zoom error codes).

## Pagination

- Some endpoints use `next_page_token`.
- Others use `page_number` + `page_size`.
- For large accounts, always code defensively for partial results.

## Token Expiry / Scopes

- `Access token is expired`: refresh or request a new S2S token.
- `does not contain scopes`: add scopes in Marketplace and re-authorize users (User OAuth).

## Webhooks

- Webhooks are at-least-once delivery: design idempotent handlers.
- Verify signatures and handle `endpoint.url_validation`.

## Also See

- `common-errors.md`
- `token-scope-playbook.md`

