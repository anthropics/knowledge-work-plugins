# Recording Pipeline (Webhook -> Download -> Store)

Goal: automatically ingest cloud recordings after meetings end.

## High-Level Steps

1. Subscribe to recording-related webhooks (e.g. `recording.completed`).
2. On webhook: fetch recording files via the recordings endpoints.
3. Download files using authenticated requests (often `download_url` requires an Authorization header).
4. Store in your system (S3/GCS/etc) and track status.

## Common Pitfalls

- Following `download_url` without attaching a bearer token.
- Not handling redirect responses from `download_url`.
- Assuming recording is available immediately after meeting ends (processing delays).

