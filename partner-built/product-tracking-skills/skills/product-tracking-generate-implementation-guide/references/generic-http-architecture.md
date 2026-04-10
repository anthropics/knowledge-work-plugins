# Generic HTTP Architecture for Analytics Instrumentation

This architecture works for any backend language (Ruby, Python, Go, Java, etc.) and any analytics destination that accepts HTTP POST requests (which is all of them).

## Architecture Overview

```
Frontend (Browser/Mobile)
    │
    ▼
Backend API Endpoint (/api/analytics/track)
    │
    ▼
Async Queue (Redis, SQS, DB-backed, in-memory)
    │
    ▼
Queue Consumer / Worker
    │
    ▼
Analytics Destination(s) via HTTP POST
```

## Core Principles

1. **Frontend never calls analytics directly.** The browser/mobile app calls your own backend endpoint. This keeps API keys server-side, allows validation, and works regardless of client technology.

2. **All track calls are async and fire-and-forget.** The API endpoint accepts the event, enqueues it, and returns immediately (202 Accepted). Analytics should never block user-facing requests.

3. **Queue-based delivery.** Events go into a queue (Redis, SQS, database table, or even an in-memory queue for simple setups). A background worker processes the queue and dispatches to analytics destinations.

4. **Retry with backoff.** The queue consumer retries failed HTTP POSTs with exponential backoff. Analytics APIs have rate limits — respect them.

5. **Batch where possible.** Most analytics APIs accept batch endpoints. Accumulate events and send in batches (e.g., every 5 seconds or every 50 events) to reduce HTTP overhead.

## Backend API Endpoint

The endpoint accepts track, identify, and group calls from the frontend:

```
POST /api/analytics/track
POST /api/analytics/identify
POST /api/analytics/group
```

Each endpoint:
- Validates the payload shape (reject malformed events)
- Enriches with server-side context (user ID from session, IP, timestamp)
- Enqueues for async processing
- Returns 202 Accepted immediately

## Single Delivery Job

Use **one** delivery job class with a method parameter — not separate classes per call type:

```
# GOOD: One job, method parameter
DeliveryJob.perform(method: 'track', payload: { userId: '...', event: '...' })
DeliveryJob.perform(method: 'identify', payload: { userId: '...', traits: {...} })
DeliveryJob.perform(method: 'group', payload: { groupId: '...', traits: {...} })

# BAD: Separate job classes
TrackJob.perform(payload)
IdentifyJob.perform(payload)
GroupJob.perform(payload)
```

The delivery logic (HTTP POST, auth headers, retry) is identical for all three call types. The only difference is the API endpoint path (`/track`, `/identify`, `/group`). One job class handles this with a simple conditional or URL mapping. Three classes means three places to maintain retry logic, error handling, and auth — for no benefit.

## Centralized Event Definitions

Even without TypeScript, maintain a central registry of valid event names and their expected properties. This serves the same purpose as TypeScript interfaces — a single source of truth that prevents typos and drift.

**In TypeScript/JavaScript:** Export typed wrapper functions from a `tracking/` module.

**In Ruby:** A module or class with class methods per event, or a YAML/JSON schema file validated at call time.

**In Python:** A module with typed dataclasses or Pydantic models per event, or a schema file.

**In Go:** A package with typed structs and constructor functions per event.

The key principle: no raw string event names scattered through the codebase. Every track call goes through a central definition.

## Snapshot Metrics via Scheduled Jobs

Some analytics data can't be captured as events — it's state, not actions. Examples: seat count, storage used, active integrations, MRR.

Use scheduled jobs (cron, background workers) to:
1. Query current state from the database
2. Send identify() or group() calls with updated traits
3. Run on a regular cadence (daily or hourly depending on the metric)

```
Scheduled Job (e.g., daily at 2am)
    │
    ▼
Query: SELECT account_id, COUNT(users) as seat_count, plan, mrr FROM accounts
    │
    ▼
For each account: group(account_id, { seat_count, plan, mrr, updated_at })
    │
    ▼
Analytics Destination
```

This is the same queue-based delivery as event tracking — scheduled jobs enqueue trait updates, the worker dispatches them.

## HTTP POST to Analytics APIs

Most analytics destinations accept simple HTTP POST with JSON body and an API key header:

**Segment HTTP Tracking API:**
```
POST https://api.segment.io/v1/track
Authorization: Basic <base64(write_key:)>
Content-Type: application/json

{ "userId": "usr_123", "event": "report.created", "properties": {...}, "timestamp": "..." }
```

**Amplitude HTTP API:**
```
POST https://api2.amplitude.com/2/httpapi
Content-Type: application/json

{ "api_key": "...", "events": [{ "user_id": "usr_123", "event_type": "report.created", ... }] }
```

**Mixpanel HTTP API:**
```
POST https://api.mixpanel.com/track
Content-Type: application/json

{ "event": "report.created", "properties": { "token": "...", "distinct_id": "usr_123", ... } }
```

**PostHog HTTP API:**
```
POST https://app.posthog.com/capture/
Content-Type: application/json

{ "api_key": "...", "event": "report.created", "distinct_id": "usr_123", "properties": {...} }
```

Each destination has its own field names and auth patterns, but they're all JSON over HTTP POST. The queue consumer maps from your internal event format to each destination's API format.

## Error Handling

- **Non-blocking:** Never let analytics failures affect the user experience
- **Retry:** Transient failures (5xx, timeout) get retried with exponential backoff
- **Dead letter:** After max retries, events go to a dead letter queue for manual inspection
- **Logging:** Log failures but don't alert on every one — analytics data loss is tolerable in small amounts

## Environment Configuration

```
ANALYTICS_ENDPOINT=https://api.segment.io/v1    # or your destination
ANALYTICS_API_KEY=...                            # write key / API key
ANALYTICS_QUEUE=redis://localhost:6379/1         # queue connection
ANALYTICS_BATCH_SIZE=50                          # events per batch
ANALYTICS_FLUSH_INTERVAL_MS=5000                 # max time between flushes
```
