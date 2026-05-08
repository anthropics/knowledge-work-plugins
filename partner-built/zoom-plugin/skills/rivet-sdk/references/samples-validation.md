# Rivet Sample Validation and Observed Drift

Validated sources:
- `zoom/rivet-javascript-sample`
- `zoom/isv-rivet-starter`
- `zoom/Rivet-Server-Sample`
- `zoom/rivet-javascript`

## Lifecycle Patterns Confirmed

- Module clients are instantiated with auth + receiver options.
- Handlers are registered before or near startup.
- `client.start()` bootstraps receiver/server.
- Multi-module samples use unique ports per module.
- `/zoom/events` endpoint suffix is required for webhook callbacks.

## Architecture Patterns Confirmed

- Rivet acts as an orchestration layer:
- Typed endpoint wrappers for API operations.
- Webhook consumer methods for events.
- OAuth helper behavior embedded in client lifecycle.

## Useful Additions Incorporated into Skill

- Multi-module port segregation and webhook endpoint mapping.
- Distinct auth patterns by module.
- Sample-derived operational gotchas for ngrok and OAuth install.

## Contradictions and Drift Notes

- Some docs/samples reference older Team Chat doc paths (`team-chat-apps`) while current docs may use updated routing.
- Sample env variable naming is inconsistent across repos (`StS_*`, `WEBHOOK_SECRET_TOKEN`, per-module keys). This skill standardizes names in `environment-variables.md`.
- Some sample README commands imply one port while module receivers may actually use `base+1` or per-module ports.
- User OAuth behavior depends on receiver choice; `AwsLambdaReceiver` limitations must be handled explicitly.

## Recommendations

- Keep a local compatibility table: `rivet_version` x `modules_used` x `auth_flows` x `receiver_type`.
- Treat sample repos as patterns, not strict source of truth.
- Re-check TypeDoc and changelog before each release.
