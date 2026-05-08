# Rivet Event-Driven API Orchestrator

Use Rivet to build a Node.js backend that combines webhook event handling with Zoom REST API actions using typed module clients.

## When to Use

- You need both event-driven workflows and API calls in one service.
- You want to reduce custom OAuth/webhook boilerplate.
- You are composing multiple Zoom surfaces (Team Chat, Meetings, Users, Phone, Video SDK API).

## Skill Chain

- [rivet-sdk](../../rivet-sdk/SKILL.md)
- [oauth](../../oauth/SKILL.md)
- [rest-api](../../rest-api/SKILL.md)
- [team-chat](../../team-chat/SKILL.md)

## Architecture

```text
Zoom Events -> Rivet webEventConsumer -> business logic -> Rivet endpoints.* -> Zoom APIs
```

## High-Level Flow

1. Instantiate one or more Rivet module clients.
2. Register webhook event handlers.
3. Start receiver(s) and expose `/zoom/events` endpoint(s).
4. Call typed endpoint wrappers from event handlers.
5. Persist state/tokens and return user-visible results.

## Key Risks

- Incorrect per-module endpoint port mapping.
- OAuth redirect/state mismatch.
- Scope mismatch for endpoint calls.
- Event payload drift across versions.

## See Also

- [rivet-sdk examples](../../rivet-sdk/examples/getting-started-pattern.md)
- [rivet-sdk multi-client pattern](../../rivet-sdk/examples/multi-client-pattern.md)
- [rivet-sdk runbook](../../rivet-sdk/RUNBOOK.md)
