# Rate Limiting Strategy

Zoom API rate limits by plan, category, and strategies for handling them in production.

## Rate Limits by Account Plan

Rate limits are **per-account** (shared by all users and all apps on the account):

### Main REST API

| Category | Free | Pro | Business+ |
|----------|------|-----|-----------|
| **Light** | 4/sec, 6,000/day | 30/sec | 80/sec |
| **Medium** | 2/sec, 2,000/day | 20/sec | 60/sec |
| **Heavy** | 1/sec, 1,000/day | 10/sec* | 40/sec* |
| **Resource-Intensive** | 10/min, 30,000/day | 10/min* | 20/min* |

**\* Combined daily limits:**
- **Pro**: 30,000/day (Heavy + Resource-Intensive shared)
- **Business+**: 60,000/day (Heavy + Resource-Intensive shared)

**Business+** includes: Business, Education, Enterprise, and Partners.

### Zoom Phone API

| Category | Pro | Business+ |
|----------|-----|-----------|
| **Light** | 20/sec | 40/sec |
| **Medium** | 10/sec | 20/sec |
| **Heavy** | 5/sec, 15,000/day* | 10/sec, 30,000/day* |
| **Resource-Intensive** | 5/min, 15,000/day* | 10/min, 30,000/day* |

**\* Daily limit shared** between Heavy and Resource-Intensive.

### Zoom Contact Center API

| Category | Pro | Business+ |
|----------|-----|-----------|
| **Light** | 20/sec | 40/sec |
| **Medium** | 10/sec | 20/sec |
| **Heavy** | 5/sec, 15,000/day* | 10/sec, 30,000/day* |

**\* Daily limit shared** with Resource-Intensive APIs.

### Video SDK Account Rate Limits

| Plan | Uses Limits |
|------|-------------|
| Pay As You Go (Deprecated) | Pro |
| Annual Prepay Monthly Usage | Pro |
| All other plans | Business+ |

## Endpoint Category Examples

| Light | Medium | Heavy |
|-------|--------|-------|
| Get A Meeting | Create Meeting | Get Daily Usage Report |
| Get Meeting Recordings | List All Recordings | List Devices |
| Add Meeting Registrant | Get Past Meeting Participants | — |
| Update A Meeting | List Meetings | — |

## Per-User Daily Limits

These are separate from account-level rate limits:

| Operation | Limit | Reset |
|-----------|-------|-------|
| Meeting/Webinar Create/Update | **100/day per user** | 00:00 UTC |
| Registrant Addition | **3/day per registrant** | 00:00 UTC |
| Registrant Status Updates | **10/day per registrant** | 00:00 UTC |

**The 100/day limit** applies to all Meeting/Webinar IDs hosted by a specific user. To bulk-create meetings, distribute across multiple host users.

## Concurrent Request Limits (Lock-Key)

Zoom enforces single-concurrency on certain resource operations:

| Scenario | Behavior |
|----------|----------|
| Multiple DELETE on same userId | Only 1 concurrent DELETE allowed |
| POST to `/v2/users` | Blocks GET/PATCH/PUT/DELETE until complete |

**Error:**
```json
{
  "code": 429,
  "message": "Too many concurrent requests. A request to disassociate this user has already been made."
}
```

## Response Headers

Every API response includes rate limit information:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Category` | `Light`, `Medium`, `Heavy`, or `Resource-intensive` |
| `X-RateLimit-Type` | `QPS` (per-second) or `Daily-limit` |
| `X-RateLimit-Limit` | Max requests in current window |
| `X-RateLimit-Remaining` | Requests remaining |
| `X-RateLimit-Reset` | Unix timestamp when per-second limit resets |
| `Retry-After` | ISO 8601 datetime when daily limit resets |

### Example — Normal Response

```
X-RateLimit-Category: Medium
X-RateLimit-Type: QPS
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 55
```

### Example — Per-Second Rate Limited

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Category: Light
X-RateLimit-Type: QPS
X-RateLimit-Limit: 80
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312800
```

### Example — Daily Rate Limited

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Category: Heavy
X-RateLimit-Type: Daily-limit
X-RateLimit-Limit: 60000
X-RateLimit-Remaining: 0
Retry-After: 2025-01-20T00:00:00Z
```

## Strategy 1: Exponential Backoff with Jitter

The simplest retry strategy for handling 429 responses:

```javascript
async function callZoomAPI(url, options, maxRetries = 5) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fetch(url, options);

    if (response.status === 429) {
      // Check for daily limit (Retry-After header)
      const retryAfter = response.headers.get('Retry-After');
      if (retryAfter) {
        const waitMs = new Date(retryAfter) - Date.now();
        console.warn(`Daily limit hit. Retry after: ${retryAfter}`);
        if (waitMs > 0 && waitMs < 86400000) {
          await sleep(waitMs);
          continue;
        }
        throw new Error(`Daily rate limit hit. Retry after ${retryAfter}`);
      }

      // Per-second limit — exponential backoff with jitter
      const baseDelay = Math.pow(2, attempt) * 1000;
      const jitter = baseDelay * 0.2 * Math.random();
      const delay = baseDelay + jitter;
      console.warn(`Rate limited. Retrying in ${Math.round(delay)}ms (attempt ${attempt + 1})`);
      await sleep(delay);
      continue;
    }

    return response;
  }
  throw new Error('Max retries exceeded for Zoom API');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

## Strategy 2: Proactive Throttling

Monitor remaining quota and slow down before hitting limits:

```javascript
async function throttledRequest(url, options) {
  const response = await fetch(url, options);

  const remaining = parseInt(response.headers.get('X-RateLimit-Remaining') || '999');
  const limit = parseInt(response.headers.get('X-RateLimit-Limit') || '999');
  const category = response.headers.get('X-RateLimit-Category');

  // Proactive throttling when under 10% quota
  if (remaining < limit * 0.1) {
    const resetTs = response.headers.get('X-RateLimit-Reset');
    if (resetTs) {
      const waitMs = (parseInt(resetTs) * 1000) - Date.now();
      if (waitMs > 0 && waitMs < 10000) {
        console.warn(`[${category}] ${remaining}/${limit} remaining — throttling ${waitMs}ms`);
        await sleep(waitMs);
      }
    } else {
      await sleep(1000);
    }
  }

  return response;
}
```

## Strategy 3: Request Queue (High-Volume)

For applications making many concurrent requests:

```javascript
class ZoomRateLimitedQueue {
  constructor(requestsPerSecond = 10, minDelayMs = 100) {
    this.queue = [];
    this.running = 0;
    this.maxConcurrent = requestsPerSecond;
    this.minDelayMs = minDelayMs;
    this.processing = false;
  }

  async add(requestFn) {
    return new Promise((resolve, reject) => {
      this.queue.push({ requestFn, resolve, reject });
      this.process();
    });
  }

  async process() {
    if (this.processing) return;
    this.processing = true;

    while (this.queue.length > 0) {
      if (this.running >= this.maxConcurrent) {
        await sleep(this.minDelayMs);
        continue;
      }

      const { requestFn, resolve, reject } = this.queue.shift();
      this.running++;

      requestFn()
        .then(resolve)
        .catch(reject)
        .finally(() => {
          this.running--;
        });

      await sleep(this.minDelayMs);
    }

    this.processing = false;
  }
}

// Usage — process 10 requests/sec max
const queue = new ZoomRateLimitedQueue(10, 100);

const userIds = ['user1', 'user2', 'user3', /* ... */];
const results = await Promise.all(
  userIds.map(id =>
    queue.add(() => zoom.request('GET', `/users/${id}`))
  )
);
```

## Best Practices

### 1. Cache GET Responses

```javascript
const cache = new Map();

async function cachedGet(path, ttlMs = 60000) {
  const cached = cache.get(path);
  if (cached && Date.now() - cached.time < ttlMs) {
    return cached.data;
  }
  const data = await zoom.request('GET', path);
  cache.set(path, { data, time: Date.now() });
  return data;
}
```

### 2. Use Webhooks Instead of Polling

```javascript
// DON'T: Poll for meeting status changes
setInterval(async () => {
  const meetings = await zoom.request('GET', `/users/${userId}/meetings`);
}, 60000);

// DO: Receive webhook events
app.post('/webhook', (req, res) => {
  handleEvent(req.body);
  res.status(200).send();
});
```

> See **[zoom-webhooks](../../webhooks/SKILL.md)** for webhook implementation.

### 3. Use List Endpoints with Pagination

```javascript
// DON'T: Fetch users one by one (N API calls)
for (const id of userIds) {
  const user = await zoom.request('GET', `/users/${id}`);
}

// DO: Fetch in bulk (1 API call per page)
const allUsers = await zoom.request('GET', '/users?page_size=300');
```

### 4. Distribute Bulk Creates Across Users

```javascript
// Avoid hitting the 100/day per-user limit
const hosts = ['host1@co.com', 'host2@co.com', 'host3@co.com'];
let hostIndex = 0;

for (const meeting of meetingsToCreate) {
  const host = hosts[hostIndex % hosts.length];
  await zoom.request('POST', `/users/${host}/meetings`, meeting);
  hostIndex++;
  await sleep(100); // Prevent per-second burst
}
```

### 5. Use QSS for Quality Data

For Quality of Service data, use QSS (push-based) instead of polling Reports API:
- Streams telemetry via webhooks/WebSocket
- Pushes data 4-6 times per minute
- Drastically reduces API call volume

## Common Gotchas

| Issue | Solution |
|-------|----------|
| 429 on first request of the day | Another app on account used quota |
| Different limits than documented | Check account type (Free/Pro/Business+) |
| Meeting create fails at 100/day | Per-user limit — distribute across hosts |
| Concurrent DELETE errors | Serialize DELETE operations on same user |
| Daily limit hit unexpectedly | Heavy + Resource-Intensive share quota |

## Resources

- **Rate Limits Documentation**: https://developers.zoom.us/docs/api/rest/rate-limits/
- **Detailed Reference**: [references/rate-limits.md](../references/rate-limits.md)
