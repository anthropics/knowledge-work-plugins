<!-- Last verified: 2026-03-10 against New Relic docs -->
# New Relic Implementation Reference

## Overview

New Relic is an application performance monitoring (APM) and observability platform. It provides real-time visibility into application health, error rates, transaction performance, and infrastructure metrics. New Relic is **not a product analytics tool** -- it does not provide funnels, retention analysis, or user journey tracking. It appears on the Forge approved list for application monitoring and is commonly deployed alongside product analytics tools to provide complementary operational visibility.

**Category:** Error / Performance Monitoring
**B2B Fit:** None -- not designed for user/account analytics

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | New Relic Browser Agent (`@newrelic/browser-agent`) | `npm install @newrelic/browser-agent` |
| Node.js | New Relic APM Agent (`newrelic`) | `npm install newrelic` |
| HTTP API | Event API / Metric API | No SDK -- raw `fetch()` calls |

## Initialization

### Browser

The Browser Agent can be installed via npm for SPAs or via the copy-paste snippet from the New Relic UI.

**npm (recommended for SPAs):**

```typescript
import { BrowserAgent } from '@newrelic/browser-agent/loaders/browser-agent';

const options = {
  init: {
    distributed_tracing: { enabled: true },
    privacy: { cookies_enabled: true },
    ajax: { deny_list: ['bam.nr-data.net'] },
  },
  info: {
    beacon: 'bam.nr-data.net',
    errorBeacon: 'bam.nr-data.net',
    licenseKey: 'YOUR_BROWSER_LICENSE_KEY',
    applicationID: 'YOUR_APP_ID',
    sa: 1,
  },
  loader_config: {
    accountID: 'YOUR_ACCOUNT_ID',
    trustKey: 'YOUR_TRUST_KEY',
    agentID: 'YOUR_AGENT_ID',
    licenseKey: 'YOUR_BROWSER_LICENSE_KEY',
    applicationID: 'YOUR_APP_ID',
  },
};

const agent = new BrowserAgent(options);
```

The `info` and `loader_config` values are provided by New Relic when you create a Browser application in the UI. Copy them from the generated snippet rather than constructing them manually.

**Loader tiers:**

New Relic offers different loader tiers. As of browser agent v1.307.0, the old SPA feature has been removed and replaced by "Soft Navigations," which is now the only SPA monitoring method. The loader tiers are:

- **Lite** -- page views and JavaScript errors only (~10 KB loader, ~15 KB downloaded, gzipped)
- **Pro** -- adds AJAX tracking, session traces (~15.5 KB loader, ~21 KB downloaded, gzipped)
- **Pro+SPA** -- adds Soft Navigations route change tracking (~17.5 KB loader, ~25 KB downloaded, gzipped)
- **MicroAgent** -- smallest loader for controlled API-only capture; can run multiple instances per page

```typescript
// All tiers use the same import path
import { BrowserAgent } from '@newrelic/browser-agent/loaders/browser-agent';

// MicroAgent -- smallest, API-only capture (multiple instances supported)
import { MicroAgent } from '@newrelic/browser-agent/loaders/micro-agent';
```

When using npm, you can selectively enable features via a `features` array in the options. For example, to use `addPageAction()` or `recordCustomEvent()` with a MicroAgent, import and include `GenericEvents`:

```typescript
import { MicroAgent } from '@newrelic/browser-agent/loaders/micro-agent';
import { GenericEvents } from '@newrelic/browser-agent/features/generic_events';

const agent = new MicroAgent({
  // ...init, info, loader_config as above...
  features: [GenericEvents],
});
```

### Node.js

The Node.js agent must be required as the **very first line** in your application entry point, before any other imports:

```javascript
// server.js -- MUST be the first require/import
require('newrelic');

// Now import everything else
const express = require('express');
const app = express();
```

Or with ES modules (requires Node.js v16.12.0+):

```bash
# Start your ESM application with the New Relic loader
node --import newrelic/esm-loader.mjs -r newrelic your-program.mjs
```

```javascript
// your-program.mjs -- use the default import for custom instrumentation
import newrelic from 'newrelic';

import express from 'express';
```

**Important:** For ESM applications, rename your configuration file from `newrelic.js` to `newrelic.cjs` so the agent (which is CommonJS) can load it. The file contents remain the same.

Configuration is done via `newrelic.js` (or `newrelic.cjs` for ESM apps) in your project root:

```javascript
// newrelic.js
'use strict';

exports.config = {
  app_name: ['Your Application Name'],
  license_key: process.env.NEW_RELIC_LICENSE_KEY,
  distributed_tracing: {
    enabled: true,
  },
  logging: {
    level: 'info',
  },
  allow_all_headers: true,
  attributes: {
    exclude: [
      'request.headers.cookie',
      'request.headers.authorization',
      'request.headers.proxyAuthorization',
      'request.headers.setCookie*',
      'request.headers.x*',
      'response.headers.cookie',
      'response.headers.authorization',
      'response.headers.proxyAuthorization',
      'response.headers.setCookie*',
    ],
  },
};
```

Alternatively, set all configuration via environment variables (common in containerized deployments):

```bash
NEW_RELIC_APP_NAME="Your Application Name"
NEW_RELIC_LICENSE_KEY="your_license_key_here"
NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
NEW_RELIC_LOG_LEVEL=info
```

## User Context (identify equivalent)

New Relic does not have a full `identify()` method like product analytics tools. Instead, you set **custom attributes** on the session or transaction to tag monitoring data with user identity. This allows you to filter errors, performance data, and traces by user.

**Browser -- `setUserId` (recommended, v1.230.0+):**

```javascript
// Set a dedicated user ID that persists across page loads within a session
// Call after login or when user identity is known
newrelic.setUserId('usr_123');

// Clear user ID on logout (pass null)
newrelic.setUserId(null);
```

The `setUserId` API records the value as the `enduser.id` attribute on all events. It persists in browser storage across page loads within the same-origin session. As of v1.307.0, passing `{ resetSession: true }` as a second argument resets the browser agent session when the user ID changes.

**Browser -- `setCustomAttribute` (for additional context):**

```javascript
// Set additional user context on the browser session
newrelic.setCustomAttribute('account_id', 'acc_456');
newrelic.setCustomAttribute('user_role', 'admin');
newrelic.setCustomAttribute('plan', 'enterprise');
```

These attributes are attached to all subsequent page views, AJAX calls, JavaScript errors, and session traces until the page unloads or attributes are cleared.

**Node.js:**

```javascript
const newrelic = require('newrelic');

// Inside a request handler -- attributes apply to the current transaction
app.use((req, res, next) => {
  if (req.user) {
    newrelic.addCustomAttributes({
      user_id: req.user.id,       // e.g., 'usr_123'
      account_id: req.user.accountId, // e.g., 'acc_456'
      user_role: req.user.role,
      plan: req.user.plan,
    });
  }
  next();
});
```

Server-side, `addCustomAttributes()` applies to the current transaction only. You must call it within a transaction context (typically inside a request handler or middleware).

## Custom Events / Metrics

Custom events in New Relic are monitoring events -- they appear in NRQL queries and dashboards, not in product analytics funnels.

**Browser -- `addPageAction` (creates PageAction events):**

```javascript
// Record a custom event (appears in NRQL as PageAction type)
newrelic.addPageAction('form_submitted', {
  form_id: 'rpt_789',
  form_type: 'report',
  duration_ms: 1250,
  user_id: 'usr_123',
  account_id: 'acc_456',
});

// Query in NRQL:
// SELECT * FROM PageAction WHERE actionName = 'form_submitted'
```

**Browser -- `recordCustomEvent` (v1.277.0+, creates custom-named event types):**

```javascript
// Record a custom event with a user-defined eventType (not PageAction)
newrelic.recordCustomEvent('FormSubmission', {
  form_id: 'rpt_789',
  form_type: 'report',
  duration_ms: 1250,
});

// Query in NRQL:
// SELECT * FROM FormSubmission WHERE form_type = 'report'
```

`recordCustomEvent` requires the **GenericEvents** feature. If using npm, import and include it in the features array (see Initialization above). Limit total custom event types to approximately five -- they are meant for high-level categories, not per-action granularity. Use `addPageAction` for action-level tracking.

**Node.js:**

```javascript
const newrelic = require('newrelic');

// Record a custom event
newrelic.recordCustomEvent('FormSubmission', {
  form_id: 'rpt_789',
  form_type: 'report',
  duration_ms: 1250,
  user_id: 'usr_123',
  account_id: 'acc_456',
});

// Query in NRQL:
// SELECT * FROM FormSubmission WHERE form_type = 'report'
```

**Custom Metrics (Node.js):**

```javascript
// Record a custom metric value
newrelic.recordMetric('Custom/ReportGeneration/Duration', 1250);

// Increment a counter
newrelic.incrementMetric('Custom/ReportGeneration/Count');
```

**HTTP Event API (direct):**

```bash
POST https://insights-collector.newrelic.com/v1/accounts/{ACCOUNT_ID}/events
Content-Type: application/json
Api-Key: YOUR_INSERT_KEY

[{
  "eventType": "FormSubmission",
  "form_id": "rpt_789",
  "form_type": "report",
  "user_id": "usr_123",
  "account_id": "acc_456",
  "timestamp": 1706745600
}]
```

## Performance Monitoring

This is New Relic's core capability. Most performance monitoring is automatic once the agent is installed.

### Browser Performance (automatic)

The Browser Agent automatically captures:
- **Page load timing** -- Time to First Byte, DOM processing, page render
- **AJAX/fetch call timing** -- duration, status codes, response sizes
- **JavaScript errors** -- stack traces, source maps (if configured)
- **Session traces** -- detailed waterfall of a user session
- **Core Web Vitals** -- LCP, INP, CLS
- **Soft Navigations** -- SPA route change tracking (replaces the old SPA feature as of v1.307.0)

### Node.js APM (automatic)

The Node.js agent automatically instruments:
- **HTTP transactions** -- inbound request timing, response codes
- **Database queries** -- SQL timing for PostgreSQL, MySQL, MongoDB, Redis
- **External HTTP calls** -- outbound request timing and status
- **Express/Koa/Fastify middleware** -- per-middleware timing breakdown
- **Distributed traces** -- cross-service request tracking

### Custom Transactions (Node.js)

For background work not tied to HTTP requests:

```javascript
const newrelic = require('newrelic');

// Wrap background work in a custom transaction
newrelic.startBackgroundTransaction('processReport', 'Reports', () => {
  const transaction = newrelic.getTransaction();

  // Add segments for sub-operations
  newrelic.startSegment('fetchData', true, async () => {
    const data = await fetchReportData('rpt_789');
    return data;
  });

  newrelic.startSegment('generatePDF', true, async () => {
    await generatePDF(data);
  });

  transaction.end();
});
```

### Custom Spans

```javascript
// Add a custom span to the current transaction
newrelic.startSegment('calculateMetrics', true, () => {
  // Timed automatically
  const result = heavyComputation();
  return result;
});
```

## What New Relic Is NOT

New Relic is an observability platform for monitoring application health. It is **not a product analytics replacement**:

- **No user journey funnels** -- cannot build "signup -> onboard -> activate" funnels
- **No retention cohort analysis** -- no Day 1 / Day 7 / Day 30 retention curves
- **No group/account analytics** -- no native concept of "accounts" with aggregated behavior
- **No A/B test analysis** -- no experiment evaluation or statistical significance
- **No event-based segmentation** -- NRQL queries are powerful but oriented around performance, not behavioral patterns

**Use New Relic alongside a product analytics tool** (Amplitude, Mixpanel, PostHog, etc.). New Relic tells you "the API is slow" or "JavaScript errors spiked." Product analytics tells you "users who complete onboarding retain 3x better."

A common pattern is to share the `user_id` and `account_id` as custom attributes in New Relic so you can correlate performance issues with specific users or accounts when investigating product analytics anomalies.

## Forge Compatibility

New Relic is on the Atlassian Forge approved analytics domain list.

**Approved domains:**
- `*.newrelic.com`

**Manifest configuration:**

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.newrelic.com"
          category: analytics
          inScopeEUD: false
```

For the Event API specifically, the ingestion endpoint is `insights-collector.newrelic.com`. For the Metric API, it is `metric-api.newrelic.com`. Both are covered by the `*.newrelic.com` wildcard.

**Note:** The full APM agent (`newrelic` npm package) is unlikely to work in Forge's sandboxed runtime due to its deep instrumentation of Node.js internals. For Forge apps, use the HTTP Event API or Metric API via `@forge/api` fetch to send custom events and metrics directly.

## Common Pitfalls

1. **Agent not loaded first (Node.js)** -- The `newrelic` module must be the very first `require()` or `import` in your entry point. If other modules load first, the agent cannot instrument them. This is the single most common setup mistake.

2. **Custom attributes outside transaction context (Node.js)** -- `addCustomAttributes()` only works inside a transaction. Calling it outside a request handler or background transaction silently does nothing. Verify you are within a transaction context before setting attributes.

3. **Confusing New Relic events with product analytics events** -- `addPageAction()` and `recordCustomEvent()` create monitoring events queryable via NRQL. They do not feed into funnels, retention, or user journey analysis. Do not use New Relic as your product analytics tool.

4. **Missing source maps for browser errors** -- JavaScript errors in production will have minified stack traces unless you upload source maps to New Relic. Configure source map uploads in your build pipeline.

5. **Browser agent bundle size** -- The Lite loader adds ~10 KB (gzipped), Pro ~15.5 KB, Pro+SPA ~17.5 KB (loader sizes; additional scripts are downloaded asynchronously). Use the Lite loader if you only need page views and error tracking. Choose the Pro+SPA loader only if you need Soft Navigations route change detection. The MicroAgent loader is even smaller for API-only capture.

6. **Sensitive data in custom attributes** -- Custom attributes are visible to all New Relic users in your account. Do not set PII (email, name, IP) as custom attributes unless your data governance policies allow it. Use opaque IDs (`usr_123`, `acc_456`) instead.

7. **`createTracer` is deprecated** -- The `createTracer` SPA API has been deprecated. For tracking task duration, use the standard browser Performance `mark()` and `measure()` APIs instead, which will gain native detection support from the agent in a future update.

8. **ESM config file extension** -- When using the Node.js agent with ES modules, you must rename `newrelic.js` to `newrelic.cjs`. Failing to do so produces `ERR_REQUIRE_ESM` errors at startup.

## Debugging

### Verify Browser Agent Is Running

Open browser DevTools console:

```javascript
// Check if the agent is loaded
typeof newrelic !== 'undefined'; // should be true

// Check agent info
newrelic.info; // shows applicationID, licenseKey, etc.
```

Check the Network tab for requests to `bam.nr-data.net` -- these are the agent's data collection calls.

### Verify Node.js Agent Is Running

Check the application log on startup for:

```
newrelic info - Connected to collector.newrelic.com
newrelic info - Reporting to: https://rpm.newrelic.com/accounts/{id}/applications/{id}
```

Enable verbose logging for troubleshooting:

```javascript
// newrelic.js
exports.config = {
  logging: {
    level: 'trace', // Options: fatal, error, warn, info, debug, trace
    filepath: 'stdout',
  },
};
```

Or via environment variable:

```bash
NEW_RELIC_LOG_LEVEL=trace
```

### Verify Custom Events

In the New Relic UI, go to **Query Your Data** and run:

```sql
-- Browser custom events
SELECT * FROM PageAction WHERE actionName = 'form_submitted' SINCE 1 hour ago

-- Node.js custom events
SELECT * FROM FormSubmission SINCE 1 hour ago

-- Check for user context
SELECT * FROM Transaction WHERE user_id = 'usr_123' SINCE 1 hour ago
```

### Common Issues

| Symptom | Likely Cause |
|---|---|
| No data in New Relic UI | Agent not loaded first, wrong license key, or firewall blocking `*.newrelic.com` |
| Custom attributes missing | `addCustomAttributes()` called outside transaction context |
| Browser errors have minified stacks | Source maps not uploaded |
| Node.js transactions not appearing | Framework not auto-instrumented; check supported frameworks list |

## Further Documentation

This reference covers the essentials for integrating New Relic as an application monitoring layer alongside product analytics. For advanced topics, consult New Relic's official documentation:

- **Getting Started:** https://docs.newrelic.com/docs/new-relic-solutions/get-started/intro-new-relic/
- **Browser Agent (npm):** https://docs.newrelic.com/docs/browser/browser-monitoring/installation/install-browser-monitoring-agent/
- **Browser Agent npm Package:** https://www.npmjs.com/package/@newrelic/browser-agent
- **Node.js APM Agent:** https://docs.newrelic.com/docs/apm/agents/nodejs-agent/installation-configuration/install-nodejs-agent/
- **Custom Attributes:** https://docs.newrelic.com/docs/data-apis/custom-data/custom-events/collect-custom-attributes/
- **Browser setUserId API:** https://docs.newrelic.com/docs/browser/new-relic-browser/browser-apis/setuserid/
- **Browser addPageAction API:** https://docs.newrelic.com/docs/browser/new-relic-browser/browser-apis/addpageaction/
- **Browser recordCustomEvent API:** https://docs.newrelic.com/docs/browser/new-relic-browser/browser-apis/recordcustomevent/
- **Custom Events (Node.js - recordCustomEvent):** https://docs.newrelic.com/docs/apm/agents/nodejs-agent/api-guides/nodejs-agent-api/#recordCustomEvent
- **Node.js ESM Support:** https://docs.newrelic.com/docs/apm/agents/nodejs-agent/installation-configuration/es-modules/
- **NRQL Reference:** https://docs.newrelic.com/docs/nrql/get-started/introduction-nrql-new-relics-query-language/
- **Event API (HTTP):** https://docs.newrelic.com/docs/data-apis/ingest-apis/event-api/introduction-event-api/
- **Metric API (HTTP):** https://docs.newrelic.com/docs/data-apis/ingest-apis/metric-api/introduction-metric-api/
- **Distributed Tracing:** https://docs.newrelic.com/docs/distributed-tracing/concepts/introduction-distributed-tracing/
