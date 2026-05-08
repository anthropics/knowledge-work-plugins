---
name: rivet-sdk
description: "Reference skill for Zoom Rivet SDK. Use after routing to a Rivet-based server workflow when implementing auth handling, webhook consumers, API wrappers, multi-module composition, or Lambda receiver patterns."
user-invocable: false
triggers:
  - "rivet"
  - "zoom rivet"
  - "@zoom/rivet"
  - "rivet javascript"
  - "rivet sdk"
  - "rivet webhook"
  - "rivet oauth"
  - "rivet lambda"
  - "rivet team chat"
  - "rivet chatbot"
---

# Zoom Rivet SDK

Background reference for Zoom Rivet as a JavaScript and TypeScript server framework for Zoom integrations.

Implementation guidance for Zoom Rivet (JavaScript/TypeScript) as a server-side framework for:
- OAuth and token handling
- Webhook event consumption
- Typed REST API endpoint wrappers
- Multi-module server composition

Official docs:
- https://developers.zoom.us/docs/rivet/
- https://developers.zoom.us/docs/rivet/javascript/
- https://zoom.github.io/rivet-javascript/

Reference samples:
- https://github.com/zoom/rivet-javascript-sample
- https://github.com/zoom/isv-rivet-starter
- https://github.com/zoom/Rivet-Server-Sample
- https://github.com/zoom/rivet-javascript

## Routing Guardrail

- Rivet SDK is a Node.js framework that bundles Zoom auth handling, webhook receivers, and typed API wrappers.
- Rivet is recommended for faster server-side scaffolding, but it is not mandatory.
- At planning start, confirm preference:
- `Do you want Rivet SDK, or direct OAuth + REST without Rivet?`
- Use Rivet when the user wants a Node.js server that combines Zoom auth + webhooks + API calls with minimal glue code.
- If the user only needs direct API calls from an existing backend, chain with [../rest-api/SKILL.md](../rest-api/SKILL.md).
- If the user is focused on Zoom Team Chat app cards/commands behavior, chain with [../team-chat/SKILL.md](../team-chat/SKILL.md).
- If the user needs SDK embed (Meeting SDK/Video SDK client runtime), route to [../meeting-sdk/SKILL.md](../meeting-sdk/SKILL.md) or [../video-sdk/SKILL.md](../video-sdk/SKILL.md).

## Quick Links

Start here:
1. [concepts/architecture-and-lifecycle.md](concepts/architecture-and-lifecycle.md)
2. [scenarios/high-level-scenarios.md](scenarios/high-level-scenarios.md)
3. [examples/getting-started-pattern.md](examples/getting-started-pattern.md)
4. [examples/multi-client-pattern.md](examples/multi-client-pattern.md)
5. [references/rivet-reference-map.md](references/rivet-reference-map.md)
6. [references/versioning-and-compatibility.md](references/versioning-and-compatibility.md)
7. [references/samples-validation.md](references/samples-validation.md)
8. [references/source-map.md](references/source-map.md)
9. [references/environment-variables.md](references/environment-variables.md)
10. [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
11. [RUNBOOK.md](RUNBOOK.md)
12. [rivet-sdk.md](rivet-sdk.md)

## Common Lifecycle Pattern

1. Choose modules and auth model per module (Client Credentials, User OAuth, S2S OAuth, Video SDK JWT).
2. Instantiate client(s) with credentials, webhook secret, and per-module port.
3. Register event handlers (`webEventConsumer.event(...)` or shortcuts).
4. Implement API calls through `client.endpoints.*`.
5. Start receiver(s) and expose webhook endpoint(s) (`/zoom/events`) to Zoom.
6. Persist tokens/state for OAuth workloads and enforce signature verification.
7. Monitor module-specific failures and rotate secrets/version with changelog cadence.

## High-Level Scenarios

- Team Chat slash-command bot + Team Chat data API enrichment.
- Multi-module backend (Users + Meetings + Team Chat + Phone) sharing one process.
- Video SDK telemetry backend using `videosdk` module event stream + API surfaces.
- ISV orchestration layer with tenant-aware token storage and per-module webhooks.
- AWS Lambda webhook processor with Rivet `AwsLambdaReceiver`.

See [scenarios/high-level-scenarios.md](scenarios/high-level-scenarios.md) for details.

## Chaining

- OAuth architecture and grant selection: [../oauth/SKILL.md](../oauth/SKILL.md)
- API endpoint semantics and request payload details: [../rest-api/SKILL.md](../rest-api/SKILL.md)
- Team Chat app cards, command and bot UX: [../team-chat/SKILL.md](../team-chat/SKILL.md)
- Video SDK API-specific behavior and BYOS context: [../video-sdk/SKILL.md](../video-sdk/SKILL.md)

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.

## Operations

- [RUNBOOK.md](RUNBOOK.md) - 5-minute preflight and debugging checklist.
