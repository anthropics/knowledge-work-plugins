# REST API - Rate Limits

Understanding and handling Zoom API rate limits for reliable integrations.

## Overview

Zoom APIs enforce rate limits to ensure fair usage. Limits vary by endpoint category, account type, and are shared across all apps on an account.

## Rate Limit Categories

### Main REST API

| Category | Free | Pro | Business+ |
|----------|------|-----|-----------|
| **Light** | 4/sec, 6,000/day | 30/sec | 80/sec |
| **Medium** | 2/sec, 2,000/day | 20/sec | 60/sec |
| **Heavy** | 1/sec, 1,000/day | 10/sec* | 40/sec* |
| **Resource-Intensive** | 10/min, 30,000/day | 10/min* | 20/min* |

**\* Daily limits (shared):**
- **Pro**: 30,000/day (Heavy + Resource-Intensive combined)
- **Business+**: 60,000/day (Heavy + Resource-Intensive combined)

### Zoom Phone API

| Category | Pro | Business+ |
|----------|-----|-----------|
| **Light** | 20/sec | 40/sec |
| **Medium** | 10/sec | 20/sec |
| **Heavy** | 5/sec, 15,000/day* | 10/sec, 30,000/day* |
| **Resource-Intensive** | 5/min, 15,000/day* | 10/min, 30,000/day* |

### Zoom Contact Center API

| Category | Pro | Business+ |
|----------|-----|-----------|
| **Light** | 20/sec | 40/sec |
| **Medium** | 10/sec | 20/sec |
| **Heavy** | 5/sec, 15,000/day* | 10/sec, 30,000/day* |

**\* Daily limit shared with Resource-Intensive APIs**

## Endpoint Category Examples

| Light | Medium | Heavy |
|-------|--------|-------|
| Add Meeting Registrant | Create Meeting | Get Daily Usage Report |
| Get A Meeting | Get Past Meeting Participants | List Devices |
| Get Meeting Recordings | List All Recordings | |
| Update A Meeting | List Meetings | |
| Delete Meeting Recordings | List Webinars | |

## Special Per-User Limits

### Meeting/Webinar Operations

| Operation | Limit | Reset |
|-----------|-------|-------|
| Meeting/Webinar Create/Update | **100/day per user** | 00:00 UTC |
| Registrant Addition | **3/day per registrant** | 00:00 UTC |
| Registrant Status Updates | **10/day per registrant** | 00:00 UTC |

**Note:** The 100/day limit applies to all Meeting/Webinar IDs hosted by a specific user.

### Lock-Key Limits (Concurrent Operations)

Zoom enforces lock-key limits for user resource operations:

| Scenario | Behavior |
|----------|----------|
| Multiple DELETE on same userId | Only 1 concurrent DELETE allowed |
| POST to `/v2/users` | Blocks GET/PATCH/PUT/DELETE until complete |

**Error Response:**
```json
{
  "code": 429,
  "message": "Too many concurrent requests. A request to disassociate this user has already been made."
}
```

## Response Headers

Every API response includes rate limit headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Category` | Light, Medium, Heavy, or Resource-intensive |
| `X-RateLimit-Type` | `QPS` (per-second) or `Daily-limit` |
| `X-RateLimit-Limit` | Maximum requests in current window |
| `X-RateLimit-Remaining` | Requests remaining in current window |

### On Per-Second/Minute Limit Hit

| Header | Description |
|--------|-------------|
| `X-RateLimit-Reset` | Unix timestamp when limit resets |

### On Daily Limit Hit

| Header | Description |
|--------|-------------|
| `Retry-After` | ISO8601 datetime when you can retry |

### Example Headers

**Normal response:**
```
X-RateLimit-Category: Medium
X-RateLimit-Type: QPS
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 55
```

**Rate limited (per-second):**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Category: Light
X-RateLimit-Type: QPS
X-RateLimit-Limit: 80
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312800
```

**Rate limited (daily):**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Category: Heavy
X-RateLimit-Type: Daily-limit
X-RateLimit-Limit: 60000
X-RateLimit-Remaining: 0
Retry-After: 2025-01-20T00:00:00Z
```

## Error Responses

### Per-Second Limit

```json
{
  "code": 429,
  "message": "You have reached the maximum per-second rate limit for this API. Try again later."
}
```

### Daily Limit

```json
{
  "code": 429,
  "message": "You have reached the maximum daily rate limit for this API. Refer to the response header for details on when you can make another request."
}
```

## Handling Rate Limits

### Basic Retry with Backoff

```javascript
async function callZoomAPI(url, options, maxRetries = 5) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
      // Check for Retry-After (daily limit)
      const retryAfter = response.headers.get('Retry-After');
      if (retryAfter) {
        const retryDate = new Date(retryAfter);
        const waitMs = retryDate - Date.now();
        console.log(`Daily limit hit. Retry after: ${retryAfter}`);
        await sleep(waitMs);
        continue;
      }
      
      // Per-second limit - use exponential backoff
      const delay = Math.pow(2, attempt) * 1000;
      const jitter = delay * 0.2 * Math.random();  // 20% jitter
      console.log(`Rate limited. Retrying in ${delay + jitter}ms`);
      await sleep(delay + jitter);
      continue;
    }
    
    return response;
  }
  
  throw new Error('Max retries exceeded');
}
```

### Monitor Rate Limit Headers

```javascript
async function callAPIWithMonitoring(url, options) {
  const response = await fetch(url, options);
  
  const remaining = parseInt(response.headers.get('X-RateLimit-Remaining'));
  const limit = parseInt(response.headers.get('X-RateLimit-Limit'));
  const category = response.headers.get('X-RateLimit-Category');
  const type = response.headers.get('X-RateLimit-Type');
  
  console.log(`[${category}/${type}] ${remaining}/${limit} remaining`);
  
  // Proactive throttling
  if (remaining < limit * 0.1) {  // Less than 10% remaining
    console.warn('Approaching rate limit - throttling requests');
    await sleep(1000);  // Slow down
  }
  
  return response;
}
```

### Request Queue Pattern

For high-volume applications:

```javascript
class RateLimitedQueue {
  constructor(maxConcurrent = 10, minDelayMs = 100) {
    this.queue = [];
    this.running = 0;
    this.maxConcurrent = maxConcurrent;
    this.minDelayMs = minDelayMs;
  }
  
  async add(requestFn) {
    return new Promise((resolve, reject) => {
      this.queue.push({ requestFn, resolve, reject });
      this.process();
    });
  }
  
  async process() {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }
    
    const { requestFn, resolve, reject } = this.queue.shift();
    this.running++;
    
    try {
      const result = await requestFn();
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.running--;
      await sleep(this.minDelayMs);
      this.process();
    }
  }
}

// Usage
const queue = new RateLimitedQueue(10, 100);  // 10 concurrent, 100ms min delay

const results = await Promise.all([
  queue.add(() => fetch('/api/users/1')),
  queue.add(() => fetch('/api/users/2')),
  queue.add(() => fetch('/api/users/3')),
  // ... more requests
]);
```

## Best Practices

### 1. Cache GET Responses

```javascript
const cache = new Map();
const CACHE_TTL = 60000;  // 1 minute

async function cachedGet(url, options) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const response = await fetch(url, options);
  const data = await response.json();
  
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

### 2. Use Webhooks Instead of Polling

Instead of polling for changes:
```javascript
// DON'T: Poll every minute
setInterval(async () => {
  const meetings = await getMeetings();  // Uses API quota
}, 60000);
```

Use webhooks:
```javascript
// DO: Receive webhook events
app.post('/webhook', (req, res) => {
  const event = req.body;
  if (event.event === 'meeting.started') {
    handleMeetingStarted(event.payload);
  }
  res.status(200).send();
});
```

### 3. Batch Operations

Use list endpoints with pagination instead of individual fetches:
```javascript
// DON'T: Fetch users one by one
for (const userId of userIds) {
  const user = await getUser(userId);  // N API calls
}

// DO: Fetch users in batches
const users = await listUsers({ page_size: 300 });  // 1 API call
```

### 4. Use QSS for Quality Data

For Quality of Service data, use QSS (push-based) instead of polling:
- QSS streams telemetry via webhooks/WebSocket
- Pushes data 4-6 times per minute
- Reduces need for Reports API polling

### 5. Distribute Requests Over Time

```javascript
// DON'T: Burst all requests at once
await Promise.all(users.map(u => updateUser(u)));  // May hit rate limit

// DO: Distribute over time
for (const user of users) {
  await updateUser(user);
  await sleep(100);  // 100ms between requests
}
```

## Account Type Notes

### Rate Limits Are Per-Account

- Limits are shared by ALL users and ALL apps on the account
- Upgrading account increases limits for everyone
- Not per-app - one heavy app can impact others

### Business+ Includes

- Business
- Education
- Enterprise
- Partners

### Video SDK Accounts

| Plan | Uses Limits |
|------|-------------|
| Pay As You Go (Deprecated) | Pro |
| Annual Prepay Monthly Usage | Pro |
| All other plans | Business+ |

## Event Subscription Limits

- **Maximum 10 event subscriptions** per application
- **No limit** on events per subscription
- Event subscription API has **Heavy** rate limit
- WebSocket: Only 1 subscription connection at a time (new connection closes previous)

## Common Gotchas

| Issue | Solution |
|-------|----------|
| 429 on first request of the day | Another app on account used quota |
| Different limits than documented | Check account type (Free/Pro/Business+) |
| Meeting create fails at 100/day | Per-user limit - use different host |
| Concurrent DELETE errors | Serialize DELETE operations on same user |
| Daily limit hit unexpectedly | Heavy + Resource-Intensive share quota |

## Resources

- **Rate limits docs**: https://developers.zoom.us/docs/api/rest/rate-limits/
- **QSS docs**: https://developers.zoom.us/docs/api/rest/qss-api/
- **Webhooks docs**: https://developers.zoom.us/docs/api/rest/webhook-reference/
