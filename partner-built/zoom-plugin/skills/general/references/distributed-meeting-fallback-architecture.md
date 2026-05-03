# Distributed Meeting Creation and Event Processing with Fallbacks

Use this architecture for high-volume meeting creation with resilient event processing.

## Core Architectural Considerations

1. **Separation of planes**
- Command plane: REST meeting creation/update APIs.
- Event plane: webhook ingestion and async projection.

2. **Idempotency and dedupe**
- Require caller-provided idempotency key per create request.
- Dedupe webhook events by stable event key.

3. **Token isolation**
- Central token broker with distributed lock (Redis/Postgres advisory lock).

4. **Backpressure and queueing**
- Queue all webhook events and meeting commands.
- Use DLQ for poison messages.

5. **Fallback mechanisms**
- Retry with exponential backoff + jitter for retriable failures (`429/5xx/network`).
- Circuit breaker around Zoom API dependency.
- Reconciliation poller when webhook delivery is delayed/missed.

## Reference Topology

```text
API Gateway
  -> Meeting Command Service
      -> Idempotency Store (Redis/Postgres)
      -> Token Broker
      -> Zoom REST API
      -> Outbox/Event Bus

Webhook Ingress
  -> Signature Verify + URL Validation
  -> Queue (Kafka/SQS/Rabbit)
  -> Projection Workers
  -> Meeting State Store

Recovery Services
  -> Retry Worker
  -> Reconciliation Poller (REST pull)
  -> Dead Letter Reprocessor
```

## Command Plane Example (Meeting Creation Service)

```ts
type CreateMeetingInput = {
  idempotencyKey: string;
  hostUserId: string; // explicit user for S2S
  topic: string;
  startTime: string;
  duration: number;
};

type QueuePublisher = { publish: (topic: string, payload: object) => Promise<void> };
type IdempotencyStore = {
  get: (key: string) => Promise<object | null>;
  put: (key: string, value: object, ttlSec: number) => Promise<void>;
};

export async function createMeetingCommand(
  input: CreateMeetingInput,
  deps: {
    tokenBroker: { getToken: () => Promise<string> };
    idempotency: IdempotencyStore;
    queue: QueuePublisher;
    breaker: CircuitBreaker;
  },
) {
  const cached = await deps.idempotency.get(input.idempotencyKey);
  if (cached) return cached;

  if (!deps.breaker.canCall()) {
    // degraded mode: queue command for delayed processing
    await deps.queue.publish('meeting.create.delayed', input);
    return { accepted: true, mode: 'degraded_queued' };
  }

  const op = async () => {
    const token = await deps.tokenBroker.getToken();
    const res = await fetch(
      `https://api.zoom.us/v2/users/${encodeURIComponent(input.hostUserId)}/meetings`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: input.topic,
          type: 2,
          start_time: input.startTime,
          duration: input.duration,
        }),
      },
    );
    if (!res.ok) {
      const err = new Error(`zoom_create_failed:${res.status}`);
      (err as any).status = res.status;
      throw err;
    }
    return res.json();
  };

  try {
    const created = await retry(
      op,
      { retries: 4, baseMs: 300, maxMs: 5000 },
      (e) => [429, 500, 502, 503, 504].includes((e as any).status),
    );

    deps.breaker.recordSuccess();
    await deps.idempotency.put(input.idempotencyKey, created, 3600);
    await deps.queue.publish('meeting.created', { meetingId: created.id, hostUserId: input.hostUserId });
    return created;
  } catch (e) {
    deps.breaker.recordFailure();
    throw e;
  }
}
```

## Event Plane Example (Webhook Ingress + Queue + Projection)

```ts
import crypto from 'crypto';

export function verifyWebhook(rawBody: string, ts: string, sig: string, secret: string): boolean {
  // reject stale requests to reduce replay risk
  const nowSec = Math.floor(Date.now() / 1000);
  const tsSec = Number(ts || 0);
  if (!Number.isFinite(tsSec) || Math.abs(nowSec - tsSec) > 300) return false;

  const msg = `v0:${ts}:${rawBody}`;
  const expected = `v0=${crypto.createHmac('sha256', secret).update(msg).digest('hex')}`;
  return sig === expected;
}

export async function ingestWebhook(req: any, res: any, queue: QueuePublisher, secret: string) {
  if (req.body.event === 'endpoint.url_validation') {
    const plainToken = req.body.payload?.plainToken;
    const encryptedToken = crypto.createHmac('sha256', secret).update(plainToken).digest('hex');
    return res.json({ plainToken, encryptedToken });
  }

  const ts = String(req.headers['x-zm-request-timestamp'] || '');
  const sig = String(req.headers['x-zm-signature'] || '');
  const raw = String(req.rawBody || '');
  if (!verifyWebhook(raw, ts, sig, secret)) return res.status(401).send('invalid_signature');

  try {
    // durable write first, then ack
    await queue.publish('zoom.webhook.raw', req.body);
    return res.status(200).send('ok');
  } catch {
    // non-200 triggers Zoom retry for at-least-once delivery
    return res.status(503).send('queue_unavailable');
  }
}

export async function projectEvent(evt: any, stateStore: any, dedupe: IdempotencyStore) {
  const dedupeKey = `${evt.event}:${evt.event_ts}:${evt.payload?.object?.uuid || evt.payload?.object?.id || 'unknown'}`;
  const seen = await dedupe.get(dedupeKey);
  if (seen) return;

  const id = String(evt.payload?.object?.id || '');
  const current = (await stateStore.get(id)) || { status: 'unknown', participants: 0, lastEventTs: 0 };
  if (evt.event_ts < current.lastEventTs) {
    await dedupe.put(dedupeKey, { stale: true }, 86400);
    return;
  } // stale event guard

  if (evt.event === 'meeting.started') current.status = 'in_progress';
  if (evt.event === 'meeting.ended') current.status = 'ended';
  if (evt.event === 'meeting.participant_joined') current.participants += 1;
  if (evt.event === 'meeting.participant_left') current.participants = Math.max(0, current.participants - 1);
  current.lastEventTs = evt.event_ts;

  await stateStore.put(id, current);
  await dedupe.put(dedupeKey, { ok: true }, 86400);
}
```

### Express raw-body setup (required for signature verification)

```ts
app.use(express.json({
  verify: (req: any, _res, buf) => {
    req.rawBody = buf.toString('utf8');
  },
}));
```

## Retry + Circuit Breaker Example (TypeScript)

```ts
type RetryOptions = {
  retries: number;
  baseMs: number;
  maxMs: number;
};

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

function backoff(attempt: number, baseMs: number, maxMs: number) {
  const exp = Math.min(maxMs, baseMs * 2 ** attempt);
  const jitter = Math.floor(Math.random() * Math.min(250, exp / 4));
  return exp + jitter;
}

export async function retry<T>(fn: () => Promise<T>, opts: RetryOptions, isRetriable: (e: any) => boolean): Promise<T> {
  let lastErr: any;
  for (let i = 0; i <= opts.retries; i += 1) {
    try {
      return await fn();
    } catch (e) {
      lastErr = e;
      if (i === opts.retries || !isRetriable(e)) break;
      await sleep(backoff(i, opts.baseMs, opts.maxMs));
    }
  }
  throw lastErr;
}

export class CircuitBreaker {
  private failures = 0;
  private openUntil = 0;

  constructor(private threshold = 5, private coolDownMs = 15_000) {}

  canCall() {
    return Date.now() > this.openUntil;
  }

  recordSuccess() {
    this.failures = 0;
  }

  recordFailure() {
    this.failures += 1;
    if (this.failures >= this.threshold) {
      this.openUntil = Date.now() + this.coolDownMs;
    }
  }
}
```

## Reconciliation Poller Example (Fallback for Missed Events)

```ts
export async function reconcileMeetingState(
  meetingId: string,
  hostUserId: string,
  deps: {
    tokenBroker: { getToken: () => Promise<string> };
    stateStore: { get: (id: string) => Promise<any>; put: (id: string, v: any) => Promise<void> };
  },
) {
  const token = await deps.tokenBroker.getToken();
  const res = await fetch(`https://api.zoom.us/v2/meetings/${encodeURIComponent(meetingId)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return;

  const apiState = await res.json();
  const projected = (await deps.stateStore.get(meetingId)) || {};
  const merged = {
    ...projected,
    status: apiState.status || projected.status,
    topic: apiState.topic || projected.topic,
    hostId: hostUserId,
    reconciledAt: Date.now(),
  };
  await deps.stateStore.put(meetingId, merged);
}
```

## Distributed Coordination and Load-Balancing Considerations

- Partition command/event streams by `meetingId` or `hostUserId` so all updates for one meeting land on the same consumer shard.
- Use a distributed lock for shared singleton jobs (token refresh rotation, reconciliation scheduler leader).
- Keep webhook ingress stateless so horizontal autoscaling is safe behind L4/L7 load balancers.
- Apply queue consumer concurrency limits to protect downstream Zoom API quotas.

### Redis-Style Lock Skeleton

```ts
export async function withLock(lock: { acquire: (k: string, ttlMs: number) => Promise<boolean>; release: (k: string) => Promise<void> }, key: string, fn: () => Promise<void>) {
  const got = await lock.acquire(key, 10_000);
  if (!got) return;
  try {
    await fn();
  } finally {
    await lock.release(key);
  }
}
```

## Token Broker Example (Cached Refresh + Distributed Lock)

```ts
type CachedToken = { accessToken: string; expiresAtMs: number };

export class TokenBroker {
  constructor(
    private cache: { get: (k: string) => Promise<CachedToken | null>; put: (k: string, v: CachedToken, ttlSec: number) => Promise<void> },
    private lock: { acquire: (k: string, ttlMs: number) => Promise<boolean>; release: (k: string) => Promise<void> },
    private fetchToken: () => Promise<{ access_token: string; expires_in: number }>,
  ) {}

  async getToken(): Promise<string> {
    const cached = await this.cache.get('zoom:s2s-token');
    const now = Date.now();
    if (cached && cached.expiresAtMs - now > 60_000) {
      return cached.accessToken;
    }

    const gotLock = await this.lock.acquire('zoom:s2s-token:refresh', 10_000);
    if (!gotLock) {
      await sleep(200);
      const retryCached = await this.cache.get('zoom:s2s-token');
      if (retryCached && retryCached.expiresAtMs - Date.now() > 30_000) {
        return retryCached.accessToken;
      }
      throw new Error('token_refresh_lock_contention');
    }

    try {
      const fresh = await this.fetchToken();
      const value = {
        accessToken: fresh.access_token,
        expiresAtMs: Date.now() + fresh.expires_in * 1000,
      };
      await this.cache.put('zoom:s2s-token', value, Math.max(60, fresh.expires_in - 90));
      return value.accessToken;
    } finally {
      await this.lock.release('zoom:s2s-token:refresh');
    }
  }
}
```

## High-Volume Create Worker (Concurrency + Rate Protection)

```ts
type CreateJob = CreateMeetingInput & { attempts: number };

class TokenBucket {
  private tokens: number;
  private lastRefill = Date.now();

  constructor(private readonly capacity: number, private readonly refillPerSec: number) {
    this.tokens = capacity;
  }

  async take() {
    while (true) {
      const now = Date.now();
      const elapsedSec = (now - this.lastRefill) / 1000;
      this.tokens = Math.min(this.capacity, this.tokens + elapsedSec * this.refillPerSec);
      this.lastRefill = now;
      if (this.tokens >= 1) {
        this.tokens -= 1;
        return;
      }
      await sleep(100);
    }
  }
}

export async function runCreateWorker(
  queue: { receiveBatch: (n: number) => Promise<CreateJob[]>; ack: (job: CreateJob) => Promise<void>; retryLater: (job: CreateJob, delayMs: number) => Promise<void> },
  deps: {
    createMeeting: (job: CreateJob) => Promise<void>;
    breaker: CircuitBreaker;
    limiter: TokenBucket;
  },
  concurrency = 8,
) {
  while (true) {
    const jobs = await queue.receiveBatch(concurrency);
    await Promise.all(jobs.map(async (job) => {
      if (!deps.breaker.canCall()) {
        await queue.retryLater(job, 30_000);
        return;
      }

      try {
        await deps.limiter.take();
        await deps.createMeeting(job);
        deps.breaker.recordSuccess();
        await queue.ack(job);
      } catch (e: any) {
        deps.breaker.recordFailure();
        const delay = backoff(job.attempts, 500, 60_000);
        await queue.retryLater({ ...job, attempts: job.attempts + 1 }, delay);
      }
    }));
  }
}
```

## Reconciliation Scheduler (Lag Detection + Leader Election)

```ts
export async function reconcileLaggingMeetings(
  deps: {
    lock: { acquire: (k: string, ttlMs: number) => Promise<boolean>; release: (k: string) => Promise<void> };
    stateStore: { listLagging: (ageMs: number, limit: number) => Promise<Array<{ meetingId: string; hostUserId: string }>> };
    reconcile: (meetingId: string, hostUserId: string) => Promise<void>;
  },
) {
  await withLock(deps.lock, 'zoom:reconcile:leader', async () => {
    const lagging = await deps.stateStore.listLagging(5 * 60_000, 250);
    for (const item of lagging) {
      await deps.reconcile(item.meetingId, item.hostUserId);
    }
  });
}
```

## DLQ Replay Worker

```ts
export async function replayDlq(
  dlq: { receiveBatch: (n: number) => Promise<any[]>; ack: (msg: any) => Promise<void>; moveBack: (topic: string, msg: any) => Promise<void> },
  topic = 'meeting.create.delayed',
) {
  const failed = await dlq.receiveBatch(100);
  for (const msg of failed) {
    await dlq.moveBack(topic, { ...msg, replayedAt: Date.now() });
    await dlq.ack(msg);
  }
}
```

## Distributed State Rules

- Meeting state is event-sourced or projection-based, not only request-response based.
- Persist `last_seen_event_ts` and status transitions to handle out-of-order events.
- Add monotonic transition guards (e.g., do not move `ended -> in_progress`).

## Fallback Matrix

| Failure | Primary response | Fallback |
|---|---|---|
| Token refresh failure | Retry token exchange | Fail fast + alert + pause new create requests |
| REST `429` / `5xx` | Retry w/ backoff | Queue command for delayed retry |
| Webhook verification failure | Reject `401` | Alert security pipeline |
| Webhook processor down | Buffer in queue | DLQ + replay job |
| Missing webhook event | Detect via reconciliation lag | REST poll and repair projection |
| Dependency outage | Open circuit breaker | Serve degraded status + queued commands |
