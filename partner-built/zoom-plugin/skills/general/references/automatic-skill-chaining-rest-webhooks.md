# Automatic Skill Chaining: REST API + Webhooks

This guide provides executable patterns for handling a multi-faceted workflow that needs both:
- synchronous REST API operations (`zoom-rest-api`)
- asynchronous event processing (`zoom-webhooks`)

## Chain Selection Logic

```ts
export type SkillChain = {
  selectedSkills: string[];
  executionOrder: string[];
};

export function chooseRestWebhookChain(query: string): SkillChain {
  const q = query.toLowerCase();
  const needsRest = /create meeting|update meeting|list users|rest api|\/v2\//.test(q);
  const needsWebhook = /webhook|event|meeting\.started|participant|real-time update/.test(q);

  const selectedSkills = ['zoom-general'];
  if (needsRest || needsWebhook) selectedSkills.push('zoom-oauth');
  if (needsRest) selectedSkills.push('zoom-rest-api');
  if (needsWebhook) selectedSkills.push('zoom-webhooks');

  return {
    selectedSkills,
    executionOrder: selectedSkills,
  };
}
```

## Reference Architecture

```text
Client/API Caller
  -> Orchestrator API
      -> OAuth token manager
      -> REST API worker (create/update meetings)
      -> Persistence (meeting state + idempotency keys)
  <- immediate REST result

Zoom Event Pipeline
  Zoom -> Webhook ingress (signature verify + URL validation)
      -> Queue
      -> Event processors
      -> State projection / downstream notifications
```

## Minimal Runnable Example (Node.js)

```js
import express from 'express';
import crypto from 'crypto';

const app = express();
app.use(express.json({
  verify: (req, _res, buf) => {
    req.rawBody = buf.toString('utf8');
  },
}));

const tokenCache = { accessToken: '', expiresAt: 0 };
const meetingStore = new Map();

async function getAccessToken() {
  const now = Date.now();
  if (tokenCache.accessToken && now < tokenCache.expiresAt - 60_000) {
    return tokenCache.accessToken;
  }

  const params = new URLSearchParams({
    grant_type: 'account_credentials',
    account_id: process.env.ZOOM_ACCOUNT_ID,
  });

  const basic = Buffer.from(`${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`).toString('base64');
  const res = await fetch(`https://zoom.us/oauth/token?${params}`, {
    method: 'POST',
    headers: { Authorization: `Basic ${basic}` },
  });

  if (!res.ok) throw new Error(`token_exchange_failed:${res.status}`);
  const data = await res.json();

  tokenCache.accessToken = data.access_token;
  tokenCache.expiresAt = now + data.expires_in * 1000;
  return tokenCache.accessToken;
}

app.post('/api/meetings', async (req, res) => {
  try {
    const token = await getAccessToken();
    const hostUserId = process.env.ZOOM_HOST_USER_ID;
    if (!hostUserId) {
      return res.status(500).json({ error: 'missing_host_user_id', detail: 'Set ZOOM_HOST_USER_ID for S2S meeting creation' });
    }

    const body = {
      topic: req.body.topic || 'Auto Meeting',
      type: 2,
      start_time: req.body.start_time,
      duration: req.body.duration || 30,
      timezone: req.body.timezone || 'UTC',
    };

    const z = await fetch(`https://api.zoom.us/v2/users/${encodeURIComponent(hostUserId)}/meetings`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await z.json();
    if (!z.ok) return res.status(z.status).json(data);

    meetingStore.set(String(data.id), { status: 'scheduled', topic: data.topic, participants: 0 });
    return res.status(201).json(data);
  } catch (err) {
    return res.status(500).json({ error: 'create_meeting_failed', detail: String(err) });
  }
});

function verifySignature(req) {
  const ts = req.headers['x-zm-request-timestamp'];
  const sig = req.headers['x-zm-signature'];
  const msg = `v0:${ts}:${req.rawBody || ''}`;
  const expected = `v0=${crypto.createHmac('sha256', process.env.ZOOM_WEBHOOK_SECRET).update(msg).digest('hex')}`;
  return sig === expected;
}

app.post('/webhooks/zoom', (req, res) => {
  if (req.body.event === 'endpoint.url_validation') {
    const plainToken = req.body.payload?.plainToken;
    const encryptedToken = crypto.createHmac('sha256', process.env.ZOOM_WEBHOOK_SECRET).update(plainToken).digest('hex');
    return res.json({ plainToken, encryptedToken });
  }

  if (!verifySignature(req)) return res.status(401).send('invalid_signature');

  const evt = req.body.event;
  const id = String(req.body.payload?.object?.id || '');
  if (id && !meetingStore.has(id)) meetingStore.set(id, { status: 'unknown', participants: 0 });

  const state = meetingStore.get(id);
  if (state) {
    if (evt === 'meeting.started') state.status = 'in_progress';
    if (evt === 'meeting.ended') state.status = 'ended';
    if (evt === 'meeting.participant_joined') state.participants += 1;
    if (evt === 'meeting.participant_left') state.participants = Math.max(0, state.participants - 1);
  }

  return res.status(200).send('ok');
});

app.listen(process.env.PORT || 3001, () => {
  console.log('orchestrator listening');
});
```

## Failure Handling Minimums

- REST call failures: retry with jitter for `429/5xx`; do not retry `4xx` business errors blindly.
- Webhook ingestion: always return `200` after durable enqueue or local persistence.
- Idempotency: dedupe by `event_id` or (`event`,`event_ts`,`meeting_uuid`) composite key.
- Reconciliation: periodic REST poll to repair missed webhook events.

## Environment Variables

- `ZOOM_ACCOUNT_ID`
- `ZOOM_CLIENT_ID`
- `ZOOM_CLIENT_SECRET`
- `ZOOM_HOST_USER_ID` (required for S2S meeting creation; do not rely on `me`)
- `ZOOM_WEBHOOK_SECRET`
- `PORT`
