# Meeting + Webhooks + OAuth Refresh Orchestration

This guide implements one solution that handles all three simultaneously:
1. create meeting,
2. process webhook updates,
3. refresh OAuth tokens safely.

## Direct Answer

Use this skill chain:

1. `zoom-general` to classify the request
2. `zoom-oauth` for token brokerage and refresh control
3. `zoom-rest-api` to create the meeting
4. `zoom-webhooks` to receive real-time updates

Minimal flow:

```text
client request
  -> TokenBroker.getToken()
  -> POST /v2/users/{userId}/meetings
  -> persist meeting + idempotency key
  -> Zoom sends webhooks to your ingress
  -> verify signature
  -> enqueue event
  -> projection worker updates meeting state
```

Webhook subscription note:
- the receiver implementation lives in your app code
- the actual Zoom event subscription is configured at the Marketplace app level
- do not model webhook subscription enablement as a per-request runtime API step unless Zoom exposes a product-specific admin API for that exact surface

## Skill Chain

1. `zoom-general`
2. `zoom-oauth`
3. `zoom-rest-api`
4. `zoom-webhooks`

## Component Design

- `TokenBroker`: central access token cache + refresh lock.
- `MeetingService`: REST calls using broker.
- `WebhookIngress`: signature validation + URL validation + event enqueue.
- `ProjectionWorker`: applies events to meeting state.

## Token Broker with Refresh Lock (TypeScript)

```ts
type TokenState = { accessToken: string; expiresAt: number; refreshing?: Promise<string> };

export class TokenBroker {
  private state: TokenState = { accessToken: '', expiresAt: 0 };

  constructor(
    private accountId: string,
    private clientId: string,
    private clientSecret: string,
  ) {}

  async getToken(): Promise<string> {
    const now = Date.now();
    if (this.state.accessToken && now < this.state.expiresAt - 60_000) {
      return this.state.accessToken;
    }

    if (!this.state.refreshing) {
      this.state.refreshing = this.refresh();
      this.state.refreshing.finally(() => { this.state.refreshing = undefined; });
    }

    return this.state.refreshing;
  }

  invalidate() {
    this.state.accessToken = '';
    this.state.expiresAt = 0;
  }

  async forceRefresh(): Promise<string> {
    this.invalidate();
    return this.getToken();
  }

  private async refresh(): Promise<string> {
    const q = new URLSearchParams({ grant_type: 'account_credentials', account_id: this.accountId });
    const basic = Buffer.from(`${this.clientId}:${this.clientSecret}`).toString('base64');

    const res = await fetch(`https://zoom.us/oauth/token?${q.toString()}`, {
      method: 'POST',
      headers: { Authorization: `Basic ${basic}` },
    });

    if (!res.ok) throw new Error(`token_refresh_failed:${res.status}`);
    const data = await res.json() as { access_token: string; expires_in: number };

    this.state.accessToken = data.access_token;
    this.state.expiresAt = Date.now() + data.expires_in * 1000;
    return this.state.accessToken;
  }
}
```

## Meeting Service with 401 Retry-once

```ts
export async function createMeeting(tokenBroker: TokenBroker, userId: string, payload: object) {
  async function call(): Promise<Response> {
    const token = await tokenBroker.getToken();
    return fetch(`https://api.zoom.us/v2/users/${encodeURIComponent(userId)}/meetings`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  }

  let res = await call();
  if (res.status === 401) {
    await tokenBroker.forceRefresh();
    res = await call(); // retry once with fresh token
  }

  if (!res.ok) throw new Error(`create_meeting_failed:${res.status}`);
  return res.json();
}
```

## Webhook Ingress Skeleton

```ts
import crypto from 'crypto';
import type { Request, Response } from 'express';

export function verifyZoomSignature(req: Request, secret: string): boolean {
  const ts = String(req.headers['x-zm-request-timestamp'] || '');
  const sig = String(req.headers['x-zm-signature'] || '');
  const rawBody = (req as any).rawBody || JSON.stringify(req.body);
  const msg = `v0:${ts}:${rawBody}`;
  const expected = `v0=${crypto.createHmac('sha256', secret).update(msg).digest('hex')}`;
  return sig === expected;
}

export async function handleWebhook(req: Request, res: Response, secret: string, enqueue: (e: any) => Promise<void>) {
  if (req.body?.event === 'endpoint.url_validation') {
    const plainToken = req.body.payload?.plainToken;
    const encryptedToken = crypto.createHmac('sha256', secret).update(plainToken).digest('hex');
    return res.json({ plainToken, encryptedToken });
  }

  if (!verifyZoomSignature(req, secret)) {
    return res.status(401).send('invalid_signature');
  }

  await enqueue(req.body); // durable queue write
  return res.status(200).send('ok');
}
```

## Event Processing Rules

- Apply idempotency key to avoid duplicate state updates.
- Accept out-of-order events; keep `last_event_ts` and reject stale writes when necessary.
- Add reconciliation worker that polls REST meeting status if webhook lag or failures are detected.

## Runtime Setup Notes

- For Server-to-Server OAuth meeting creation, pass an explicit host `userId`/email instead of relying on `me`.
- In Express, capture raw request body in `express.json({ verify })` and use it for signature verification.
