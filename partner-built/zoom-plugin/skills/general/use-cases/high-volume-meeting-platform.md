# High-Volume Meeting Platform

Design a distributed system that creates large numbers of meetings and keeps meeting state accurate under retries, webhook delay, and partial outages.

## Skills Needed

- Primary: [../../rest-api/SKILL.md](../../rest-api/SKILL.md)
- Events: [../../webhooks/SKILL.md](../../webhooks/SKILL.md)
- Auth/token broker: [../../oauth/SKILL.md](../../oauth/SKILL.md)
- Deep implementation reference: [../references/distributed-meeting-fallback-architecture.md](../references/distributed-meeting-fallback-architecture.md)

## Architecture Summary

```text
API Gateway
  -> Command Service
      -> Idempotency Store
      -> Token Broker
      -> Zoom REST API
      -> Outbox / Queue

Webhook Ingress
  -> Signature Verification
  -> Durable Queue
  -> Projection Workers
  -> Meeting State Store

Recovery
  -> Retry Workers
  -> Reconciliation Poller
  -> DLQ Replay
```

## Core Rules

1. Keep command and event planes separate.
2. Require idempotency keys on all meeting-creation requests.
3. Queue everything that touches Zoom when you need backpressure control.
4. Verify webhook signatures before durable write.
5. Reconcile state from REST when event delivery is delayed or incomplete.

## Concrete Fallbacks

- `429` / `5xx` from Zoom REST API -> retry with jitter, then queue for delayed retry.
- Token refresh contention -> single token broker refresh under distributed lock.
- Webhook processor outage -> accept only after queue write, use DLQ replay.
- Missing lifecycle events -> scheduled reconciliation poller repairs the projection.
- Downstream Zoom outage -> circuit breaker opens and create commands stay queued.

## When to Use This

Use this pattern when:
- multiple workers or services create meetings concurrently
- you need durable event processing
- missed webhook events are unacceptable
- you need a degraded-but-safe mode during Zoom or network instability
