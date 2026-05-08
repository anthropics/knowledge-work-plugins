# Server-to-Server OAuth With Webhooks (Common Enterprise Pattern)

This pattern shows up constantly in high-frequency forum clusters:

- "Can I use Server-to-Server OAuth with webhooks?"
- "How do I validate webhook requests?"
- "How do I automate meeting/user/report operations across the account?"

## Skills Needed

| Order | Skill | Purpose |
|------:|------|---------|
| 1 | **zoom-rest-api** | Make server-side API calls using S2S tokens |
| 2 | **zoom-oauth** | Correctly mint S2S access tokens (`account_credentials`) |
| 3 | **zoom-webhooks** | Receive events, handle URL validation, verify signatures |

## Architecture

1. Your backend periodically requests an S2S access token.
2. Your backend calls REST API endpoints to create/update resources.
3. Zoom calls your webhook endpoint for events (meeting/webinar/recording/etc).
4. Your webhook handler verifies authenticity and enqueues async work.

## Key Clarifications

- **Webhooks do not "use" your S2S token**. Webhooks are pushed to your endpoint and verified via webhook secrets/signatures.
- REST API calls and webhook ingestion are separate authentication planes.

## Hard Requirements

- Public HTTPS webhook endpoint
- Handle `endpoint.url_validation`
- Verify request signatures (and/or follow Zoom verification guidance)
- Respond `200` quickly; do heavy processing asynchronously

## Links

- `../../rest-api/concepts/authentication-flows.md`
- `../../rest-api/examples/webhook-server.md`
- `../../webhooks/references/verification.md`
- `../references/automatic-skill-chaining-rest-webhooks.md`
- `../references/meeting-webhooks-oauth-refresh-orchestration.md`
- `../references/distributed-meeting-fallback-architecture.md`
