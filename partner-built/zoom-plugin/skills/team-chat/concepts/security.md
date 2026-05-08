# Security Best Practices

## Webhooks

- Verify webhook requests using Zoom’s verification mechanism for Team Chat subscriptions.
- Treat webhook payloads as untrusted input; validate fields before using them.

## OAuth

- Store refresh tokens securely (encrypt at rest).
- Rotate client secrets if they leak.
- Use least-privilege scopes.

## Operational

- Add rate limiting on your webhook endpoint.
- Log request IDs and correlation IDs (but avoid logging tokens / PII).

