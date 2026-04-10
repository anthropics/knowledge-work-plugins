# Forge Platform Implementation

Implementation patterns for products running on Atlassian Forge. When `meta.platform: forge` is set in the tracking plan, use this reference instead of individual SDK guides. The Forge "SDK" is a combination of `@forge/events`, `@forge/api`, `@forge/bridge`, and `@forge/resolver`.

**Note:** `@forge/events`, `@forge/api`, `@forge/bridge`, and `@forge/resolver` are real npm packages provided by the Forge runtime. They are available in any Forge app without additional installation — they come with the Forge platform.

## Why This Architecture

Traditional frontend analytics are privacy nightmares. Browser-based tracking automatically transmits user IP addresses, referrer URLs (revealing internal Jira/Confluence navigation), full page URLs (containing project names and issue keys), user agent strings, session cookies, and can accidentally capture form data containing end user content. In Forge apps, this is both a compliance violation and a trust issue.

**The solution is complete backend control.** By routing ALL analytics through the Forge backend, the app controls exactly what information reaches the analytics provider. The frontend never talks directly to any external service — this is not just a best practice, it is a hard constraint of the Forge platform. Forge Custom UI frontends run in a sandboxed iframe and cannot make direct network calls to external services. All external communication must go through `invoke()` to a backend resolver, which then uses `@forge/api` fetch.

This architecture provides:
- **No accidental PII transmission** — only explicitly constructed payloads leave the system
- **Only Forge server IPs visible** to the analytics provider (not user IPs)
- **No URLs, referrers, user agents, or session data** ever transmitted
- **No user-generated content** in analytics payloads — only intentional business events

## Architecture

```
Frontend (Custom UI)
  │
  │  invoke('track-event', { event: 'form.submitted' })
  ▼
Backend Resolver (privacy barrier)
  │  Adds context: cloudId, accountId
  ▼
Queue Producer (events.js)
  │  Bundles identify + group + track
  ▼
Forge Queue (@forge/events)
  │  Async, automatic retry
  ▼
Queue Consumer (consumer.js)
  │  Routes by event type
  ▼
HTTP Dispatcher (dispatcher.js)
  │  @forge/api fetch()
  ▼
Analytics Provider
```

Frontend **never** talks directly to the analytics provider. All events route through the backend for privacy compliance and to protect "Runs on Atlassian" status.

### Three Data Flow Paths

**Frontend-Triggered Events:**
1. User interaction in Custom UI component
2. Component calls frontend event wrapper (e.g., `trackSearchPerformed()`)
3. `invoke('track-event', { event: 'search.performed' })` crosses to backend
4. Resolver receives event name + Forge context (cloudId, accountId added server-side)
5. Event bundled with identify + group data and pushed to queue
6. Consumer processes asynchronously, dispatcher sends to analytics provider

**Backend-Triggered Events:**
1. Business logic executes in a resolver (e.g., `resolver.define('create')`)
2. Resolver calls tracking function directly (e.g., `await trackFormCreated(context)`)
3. Same queue/consumer/dispatcher flow as frontend events

**Scheduled Events:**
1. Forge executes scheduled function (e.g., `dailyGroupAnalytics()`) on configured interval
2. Function collects instance-level metrics (license info, usage counts, domain)
3. Dispatches directly to provider (bypasses queue — already running asynchronously)

## File Structure

```
src/analytics/
├── dispatcher.js    # HTTP transport to analytics provider
├── consumer.js      # Queue event processor
├── events.js        # Backend event definitions + queue producer
├── resolvers.js     # Frontend → backend bridge
├── utils.js         # Identity extraction helpers
└── schedule.js      # Scheduled snapshot metrics

static/spa/src/
└── analytics.js     # Frontend event wrappers (invoke calls)
```

## Manifest Configuration

The `manifest.yml` must declare the queue consumer, scheduled triggers, and external fetch permissions:

```yaml
modules:
  consumer:
    - key: analytics-consumer
      queue: analytics-queue
      resolver:
        function: analytics-consumer-func
        method: analytics-listener

  scheduledTrigger:
    - key: daily-analytics-scheduled-trigger
      function: daily-analytics
      interval: day

  function:
    - key: analytics-consumer-func
      handler: analytics/consumer.handler
    - key: daily-analytics
      handler: analytics/schedule.dailyGroupAnalytics

permissions:
  external:
    fetch:
      backend:
        - address: "in.accoil.com"
          category: analytics
          inScopeEUD: false
```

**Important: use the structured object format**, not the simple URL string format. The simple format (`- "https://in.accoil.com"`) does not carry `category` or `inScopeEUD` metadata. Without this metadata, the app cannot pass Atlassian's compliance review.

```yaml
# WRONG — simple format, no compliance metadata
permissions:
  external:
    fetch:
      backend:
        - "https://in.accoil.com"

# RIGHT — structured format with required metadata
permissions:
  external:
    fetch:
      backend:
        - address: "in.accoil.com"
          category: analytics
          inScopeEUD: false
```

Key settings:
- `inScopeEUD: false` — declares no in-scope End User Data is transmitted. Required for "Runs on Atlassian" compliance. Analytics payloads must not contain user-generated content, PII, or customer business data. Site hostname/domain (e.g., `acme.atlassian.net`) is acceptable — it is instance context, not in-scope EUD.
- `category: analytics` — classifies the external fetch for Atlassian review. Only pre-approved domains may use this category (see Approved Analytics Domains below).
- `address` — hostname only (no `https://` prefix, no path).
- Queue key must match between producer (`events.js`) and consumer manifest entry.

### Approved Analytics Domains

Forge enforces an allowlist of pre-approved domains for `category: analytics` egress. Apps declaring unlisted domains will be **blocked from deployment** (enforced since August 2025).

**Requirements:** Analytics tools must be cloud-only (no self-hosted), have a public website and privacy policy, and use a recognized fixed domain.

Common pre-approved domains for tracking plan destinations:

| Destination | Address for manifest |
|---|---|
| **Accoil** | `in.accoil.com` |
| **Amplitude** | `*.amplitude.com` |
| **Mixpanel** | `*.mixpanel.com` |
| **PostHog** | `*.posthog.com` |
| **Segment** | `*.api.segment.io` |
| **Google Analytics** | `*.google-analytics.com` |
| **Sentry** | `*.ingest.sentry.io` |

Other approved providers include HotJar, LaunchDarkly, New Relic, Plausible, Azure Application Insights, Cloudflare Web Analytics, Fathom, Statsig, UserPilot, and more. See the [Atlassian analytics tool policy](https://developer.atlassian.com/platform/forge/analytics-tool-policy/) for the full list.

**RudderStack is not on the approved list.** If the tracking plan specifies RudderStack, use an approved alternative or raise a support request with Atlassian.

To request approval for an unlisted tool, raise a support request with Atlassian.

## Identity Utilities

Extract accountId and cloudId from the Forge context object:

```javascript
// src/analytics/utils.js
export const userIdFromContext = (context) => {
    return context.accountId;
};

export const groupIdFromContext = (context) => {
    return context.cloudId;
};
```

cloudId is always the group ID (maps to Marketplace billing). accountId is the user ID.

## Backend Event Module

The core tracking layer. Each call bundles identify + group + track into a single queue push for atomic processing:

```javascript
// src/analytics/events.js
import { Queue } from '@forge/events';
import { groupIdFromContext, userIdFromContext } from './utils';

const analyticsQueue = new Queue({ key: 'analytics-queue' });

export const track = async (context, eventName) => {
    const userId = userIdFromContext(context);
    const groupId = groupIdFromContext(context);

    const events = [
        { body: { type: 'identify', userId, groupId, traits: { name: userId } } },
        { body: { type: 'group', groupId, traits: { name: groupId } } },
        { body: { type: 'track', userId, event: eventName } },
    ];
    await analyticsQueue.push(events);
};

// Named exports per event — one function per event
export const trackFormSubmitted = (context) => track(context, 'form.submitted');
export const trackFormCreated = (context) => track(context, 'form.created');
export const trackFormPublished = (context) => track(context, 'form.published');
```

Pattern:
- `track()` is the core function. It always bundles identify + group + track.
- Each event gets a named export. This maintains the one-function-per-event rule.
- **Dynamic dispatch exception:** When event names depend on runtime state (e.g., a tab index, feature flag, or computed identifier), a single function that accepts constrained inputs is the right pattern. Use a lookup table or union type — don't accept arbitrary strings.
- Group traits should include `domain` and license info when available (see Scheduled Analytics below for trait enrichment).

### Using Backend Events in Resolvers

Call tracking functions directly from your business logic resolvers:

```javascript
// src/index.js
import Resolver from '@forge/resolver';
import { trackFormCreated, trackFormSubmitted } from './analytics/events';
import { trackEvent } from './analytics/resolvers';

const resolver = new Resolver();

resolver.define('create-form', async ({ payload, context }) => {
    const form = await createForm(payload);
    await trackFormCreated(context);
    return form;
});

// Frontend analytics bridge
resolver.define('track-event', trackEvent);

export const handler = resolver.getDefinitions();
```

Backend events use direct function imports — no resolver bridge needed. Only frontend events need the `invoke()` → resolver path.

## Resolver Bridge

The privacy barrier between frontend and backend. Receives minimal data from frontend, adds backend context (cloudId, accountId), and forwards to the queue:

```javascript
// src/analytics/resolvers.js
import { track } from './events';

export const trackEvent = async ({ payload, context }) => {
    await track(context, payload.event);
};
```

The resolver adds `context` (containing cloudId and accountId) server-side. The frontend never has access to these identifiers and cannot influence what gets sent to the analytics provider.

## Frontend Event Module

**This module is optional.** If every trackable user action already routes through a backend resolver (common in Forge apps where UI interactions trigger resolver calls for business logic), you don't need a separate frontend analytics module. Just call tracking functions directly from the existing resolvers. The frontend module is only needed when there are UI-only actions (e.g., search, filter, navigation) that don't already have a resolver.

Frontend wrappers use `invoke()` from `@forge/bridge` to call the backend resolver. The payload is minimal — just the event name:

```javascript
// static/spa/src/analytics.js
import { invoke } from '@forge/bridge';

export const track = async (eventName) => {
    try {
        await invoke('track-event', { event: eventName });
    } catch (error) {
        console.error('[Analytics] Failed to track event:', error);
    }
};

// Named exports per event
export const trackSearchPerformed = () => track('search.performed');
export const trackFilterApplied = () => track('filter.applied');
export const trackExportGenerated = () => track('export.generated');
```

Rules:
- **Zero payload beyond event name.** No properties, no user data, no context. The backend adds everything needed.
- **Error handling is silent.** Analytics failures must never break the UI.
- **Named exports per event** to maintain consistency with backend pattern.

### React Component Usage

```javascript
import { trackSearchPerformed } from './analytics';

function SearchComponent() {
    const handleSearch = (query) => {
        if (query.length > 2) {
            trackSearchPerformed();
            // ... perform search
        }
    };
    // ...
}
```

## Queue Consumer

Processes events asynchronously from the Forge queue. Routes by event type and re-throws on failure to trigger Forge's automatic retry:

```javascript
// src/analytics/consumer.js
import Resolver from '@forge/resolver';
import { handleTrackEvent, handleIdentify, handleGroup } from './dispatcher';

const resolver = new Resolver();

resolver.define('analytics-listener', async ({ payload }) => {
    const event = payload.body;
    switch (event.type) {
        case 'identify':
            await handleIdentify(event.userId, event.groupId, event.traits);
            break;
        case 'group':
            await handleGroup(event.groupId, event.traits);
            break;
        case 'track':
            await handleTrackEvent(event.userId, event.event);
            break;
        default:
            console.log(`analytics-listener: unknown type ${event.type}`);
    }
});

export const handler = resolver.getDefinitions();
```

Retry behavior: if the consumer throws, Forge automatically retries the event. Re-throw errors from the dispatcher to leverage this.

## HTTP Dispatcher

Sends events to the analytics provider using `@forge/api` (Forge-specific — standard `fetch` does not work in Forge backend):

```javascript
// src/analytics/dispatcher.js
import { fetch } from '@forge/api';

export const handleTrackEvent = async (userId, event) => {
    await dispatch('/v2/track', { userId, event });
};

export const handleIdentify = async (userId, groupId, traits) => {
    await dispatch('/v2/identify', { userId, groupId, traits });
};

export const handleGroup = async (groupId, traits) => {
    await dispatch('/v2/group', { groupId, traits });
};

const dispatch = async (path, payload) => {
    const apiKey = process.env.ANALYTICS_API_KEY;
    const url = `https://in.accoil.com${path}`;
    const body = JSON.stringify({
        ...payload,
        timestamp: new Date().toISOString(),
    });

    if (process.env.ANALYTICS_DEBUG?.toLowerCase() === 'true') {
        console.log(`[Analytics Debug] ${url}:\n${body}`);
        return;
    }

    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Basic ${apiKey}`,
        },
        body,
    });
};
```

Key detail: `import { fetch } from '@forge/api'` — this is the Forge-specific fetch. Standard `node-fetch` or global `fetch` will fail in Forge's sandboxed runtime.

## Scheduled Analytics (Snapshot Metrics)

Daily scheduled triggers collect instance-level metrics and send them as group traits. These bypass the queue since they are already running asynchronously on a schedule:

```yaml
# manifest.yml (relevant section)
modules:
  scheduledTrigger:
    - key: daily-analytics-scheduled-trigger
      function: daily-analytics
      interval: day

  function:
    - key: daily-analytics
      handler: analytics/schedule.dailyGroupAnalytics
```

```javascript
// src/analytics/schedule.js
import { handleGroup } from './dispatcher';
import { groupIdFromContext } from './utils';

export const dailyGroupAnalytics = async ({ context }) => {
    const groupId = groupIdFromContext(context);

    const hostname = context.siteUrl;           // e.g., "acme.atlassian.net"
    const company = hostname?.split('.')[0];    // e.g., "acme"
    const licensetype = context?.license?.isEvaluation
        ? 'evaluation'
        : context?.license?.isActive
            ? 'paid'
            : 'FREE';

    // When destination is Accoil, use am.* prefixed traits to align with
    // the Atlassian Marketplace connector built into Accoil.
    // When destination is NOT Accoil, use standard trait names instead
    // (company, domain, license_type) — the am.* prefix is Accoil-specific.
    const traits = {
        name: groupId,
        domain: hostname,
        is_active: context?.license?.isActive,
        is_evaluation: context?.license?.isEvaluation,
        last_daily_sync: new Date().toISOString(),
        // Accoil destination: am.* traits match Marketplace connector
        'am.contactdetails.company': company,
        'am.cloudsitehostname': hostname,
        'am.licensetype': licensetype,
        // Non-Accoil destination: use these instead of the am.* traits above
        // company: company,
        // domain: hostname,
        // license_type: licensetype,
        // Add app-specific snapshot metrics:
        // total_form_count: `${await getFormCount()}`,
        // active_user_count: `${await getActiveUserCount()}`,
    };

    // Direct dispatch — skip queue for scheduled jobs
    await handleGroup(groupId, traits);
};
```

This is where group traits like `domain`, license status, and snapshot metrics get updated. The scheduled trigger runs daily and sends a group call with current state.

Numeric snapshot values should be converted to strings for consistent data types across analytics providers.

## Environment Variables

Set via Forge CLI:

```bash
# Required: API key for analytics provider
forge variables set ANALYTICS_API_KEY your_key_here

# Optional: debug mode (logs instead of sending)
forge variables set ANALYTICS_DEBUG true

# Per-environment configuration
forge variables set --environment production ANALYTICS_API_KEY your_prod_key
forge variables set --environment development ANALYTICS_DEBUG true
```

## Differences from Standard SDK Implementation

| Standard SDK | Forge |
|---|---|
| `npm install analytics-sdk` | `@forge/events` + `@forge/api` + `@forge/bridge` + `@forge/resolver` |
| Direct SDK calls | Queue-based async dispatch |
| Frontend can call SDK | Frontend must go through `invoke()` → resolver |
| `fetch()` or SDK HTTP | `import { fetch } from '@forge/api'` |
| ENV vars via `.env` | `forge variables set` |
| Standard init/shutdown | Manifest-declared consumers and triggers |
| Any HTTP endpoint | Only addresses declared in `permissions.external.fetch` |

## Privacy Protection and End User Data

This architecture eliminates entire classes of data leakage by design, ensuring `inScopeEUD: false` compliance:

| Risk Category | Frontend Analytics | This Architecture |
|---|---|---|
| **IP Addresses** | User's real IP sent to provider | Only Forge server IP visible |
| **URLs/Referrers** | Internal Jira/Confluence URLs leaked | Never transmitted to provider |
| **Browser Data** | Full user agent sent | Server-controlled data only |
| **Session Data** | Cookies, localStorage exposed | No client-side data access |
| **Form Inputs** | Accidentally captured PII | Only intentional business events |
| **Navigation Patterns** | Full browsing history | Meaningful business actions only |

**What must NOT be sent** (in-scope End User Data):
- User-generated content: issue titles, descriptions, form inputs, comments, labels, search queries
- Customer business data: custom field values, page content

**What IS acceptable** (not in-scope EUD):
- System identifiers: cloudId, accountId, project IDs
- Site hostname/domain: e.g., `acme.atlassian.net` — this is instance context, not end user data
- Enumerated values: status, type, category, license type
- Counts and aggregates: item_count, member_count
- Boolean states: is_active, has_custom_fields
- Timestamps

## Key Architecture Principles

1. **Privacy by Design** — No accidental PII transmission is possible
2. **Provider Abstraction** — Easy switching between analytics services (only dispatcher changes)
3. **Central Event Management** — Single source of truth for all tracked events
4. **Queue-Based Reliability** — Enterprise-grade event delivery with automatic retry
5. **Customer Control** — Customers can disable analytics via Atlassian controls
6. **Compliance First** — Built to exceed Atlassian's privacy requirements and protect "Runs on Atlassian" status

## Implementation Checklist

- [ ] `manifest.yml` has consumer, queue, scheduled trigger, and external fetch permissions
- [ ] Analytics destination address is on the [Atlassian approved list](https://developer.atlassian.com/platform/forge/analytics-tool-policy/)
- [ ] `inScopeEUD: false` is set on all analytics fetch permissions
- [ ] No in-scope End User Data in any event properties or traits (user-generated content, PII, customer business data)
- [ ] Site hostname/domain used only as instance context (acceptable, not in-scope EUD)
- [ ] Queue key matches between `events.js` producer and manifest consumer
- [ ] `@forge/api` fetch is used (not standard fetch)
- [ ] Frontend sends only event names via `invoke()` — no properties, no context
- [ ] Backend adds cloudId and accountId from Forge context
- [ ] Scheduled analytics send group traits with domain and license status
- [ ] Debug mode works via `ANALYTICS_DEBUG` environment variable
- [ ] Error handling: consumer re-throws to trigger Forge retry
