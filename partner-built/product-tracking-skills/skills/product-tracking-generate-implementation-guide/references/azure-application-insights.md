<!-- Last verified: 2026-03-10 against Azure Application Insights docs -->
# Azure Application Insights Implementation Reference

## Overview

Azure Application Insights is a feature of Azure Monitor that provides application performance monitoring (APM), diagnostics, and telemetry collection. It tracks request rates, response times, failure rates, dependency calls, exceptions, and custom events. Application Insights is **not a product analytics tool** -- it does not provide user journey funnels, retention analysis, or account-level behavioral segmentation. It appears on the Forge approved list for application monitoring and is commonly deployed alongside product analytics tools.

**Category:** Error / Performance Monitoring
**B2B Fit:** None -- not designed for user/account analytics

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | Application Insights JavaScript SDK (`@microsoft/applicationinsights-web`) | `npm install @microsoft/applicationinsights-web` |
| Node.js | Application Insights Node.js SDK (`applicationinsights`) | `npm install applicationinsights` |
| HTTP API | Track API (v2) | No SDK -- raw `fetch()` calls |

## Initialization

### Browser

```typescript
import { ApplicationInsights } from '@microsoft/applicationinsights-web';

const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
    // instrumentationKey is deprecated -- support for ikey-based ingestion
    // ended March 31, 2025. Always use connectionString instead.

    // Auto-collection settings
    enableAutoRouteTracking: true,  // Track SPA route changes as page views
    enableCorsCorrelation: true,    // Correlate AJAX calls across origins
    enableRequestHeaderTracking: true,
    enableResponseHeaderTracking: true,

    // Sampling -- reduce volume in high-traffic apps
    samplingPercentage: 100, // 100 = send everything, 50 = send half

    // Disable cookie usage if needed for privacy
    disableCookiesUsage: false,
  },
});

appInsights.loadAppInsights();
appInsights.trackPageView(); // Manually track the initial page view
```

**Connection string vs instrumentation key:** Instrumentation key-based ingestion is deprecated -- support ended March 31, 2025. Always use connection strings, which include the ingestion endpoint and are required for regional endpoints. The format is: `InstrumentationKey=xxx;IngestionEndpoint=https://xxx.applicationinsights.azure.com/;LiveEndpoint=https://xxx.monitor.azure.com/`.

> **Note:** Microsoft now recommends the **Azure Monitor OpenTelemetry Distro** for new Node.js applications. The classic `applicationinsights` npm package (SDK 3.x) continues to work via a compatibility shim but routes telemetry through OpenTelemetry internally. The code patterns below use the classic API, which remains supported for existing applications.

### Node.js

```javascript
const appInsights = require('applicationinsights');

appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING)
  .setAutoCollectRequests(true)
  .setAutoCollectPerformance(true, true) // (enabled, enableExtendedMetrics) -- note: extended metrics not supported in SDK 3.x
  .setAutoCollectExceptions(true)
  .setAutoCollectDependencies(true)
  .setAutoCollectConsole(true, true)     // (enabled, collectConsoleLog)
  .setAutoCollectPreAggregatedMetrics(true)
  .setSendLiveMetrics(false)             // Enable for Live Metrics Stream
  .setUseDiskRetryCaching(true)
  .start();

const client = appInsights.defaultClient;
```

Or with ES modules:

```typescript
import * as appInsights from 'applicationinsights';

appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING).start();
const client = appInsights.defaultClient;
```

**Environment variable auto-detection:** If you set `APPLICATIONINSIGHTS_CONNECTION_STRING` as an environment variable, calling `appInsights.setup()` without arguments will pick it up automatically.

## User Context (identify equivalent)

Application Insights does not have a full `identify()` method. Instead, you set **user context** and **account context** to tag telemetry with identity information. This allows filtering in the Azure portal by user or account.

**Browser:**

```javascript
// Set authenticated user context
// Parameters: authenticatedUserId, accountId, storeInCookie
appInsights.setAuthenticatedUserContext('usr_123', 'acc_456', true);

// This tags all subsequent telemetry with:
//   user.authenticatedId = 'usr_123'
//   user.accountId = 'acc_456'
```

Clear on logout:

```javascript
appInsights.clearAuthenticatedUserContext();
```

**Node.js:**

```javascript
const client = appInsights.defaultClient;

// Set on a per-request basis using tagOverrides
// In Express middleware:
app.use((req, res, next) => {
  if (req.user) {
    client.context.tags[client.context.keys.userId] = req.user.id;         // 'usr_123'
    client.context.tags[client.context.keys.userAccountId] = req.user.accountId; // 'acc_456'
  }
  next();
});
```

For multi-tenant Node.js apps where the default client's tags would be overwritten per request, use `getCorrelationContext()` or create per-request envelopes:

```javascript
app.use((req, res, next) => {
  if (req.user) {
    const correlationContext = appInsights.getCorrelationContext();
    if (correlationContext) {
      correlationContext.customProperties.setProperty('user_id', req.user.id);
      correlationContext.customProperties.setProperty('account_id', req.user.accountId);
    }
  }
  next();
});
```

## Custom Events / Metrics

Custom events in Application Insights are monitoring events -- they appear in Azure Monitor queries and workbooks, not in product analytics funnels.

**Browser:**

```javascript
// Track a custom event
appInsights.trackEvent({
  name: 'form_submitted',
  properties: {
    form_id: 'rpt_789',
    form_type: 'report',
    user_id: 'usr_123',
    account_id: 'acc_456',
  },
  measurements: {
    duration_ms: 1250,
  },
});
```

**Node.js:**

```javascript
const client = appInsights.defaultClient;

// Track a custom event
client.trackEvent({
  name: 'form_submitted',
  properties: {
    form_id: 'rpt_789',
    form_type: 'report',
    user_id: 'usr_123',
    account_id: 'acc_456',
  },
  measurements: {
    duration_ms: 1250,
  },
});
```

**Custom Metrics (Node.js):**

```javascript
// Track a metric value
client.trackMetric({
  name: 'report_generation_duration_ms',
  value: 1250,
  properties: {
    report_type: 'standard',
  },
});

// Track aggregated metrics (pre-aggregated for efficiency)
client.trackMetric({
  name: 'active_users',
  value: 42,
  count: 1,
  min: 42,
  max: 42,
  stdDev: 0,
});
```

**HTTP Track API (direct):**

```bash
POST https://{ingestion-endpoint}/v2/track
Content-Type: application/json

{
  "name": "AppEvents",
  "iKey": "YOUR_INSTRUMENTATION_KEY",
  "time": "2024-01-15T10:30:00.000Z",
  "data": {
    "baseType": "EventData",
    "baseData": {
      "name": "form_submitted",
      "properties": {
        "form_id": "rpt_789",
        "form_type": "report",
        "user_id": "usr_123",
        "account_id": "acc_456"
      },
      "measurements": {
        "duration_ms": 1250
      }
    }
  }
}
```

The ingestion endpoint is found in your connection string (e.g., `https://westus2-1.in.applicationinsights.azure.com`).

## Performance Monitoring

This is Application Insights' core capability. Most monitoring is automatic once the SDK is initialized.

### Browser Performance (automatic)

The JavaScript SDK automatically captures:
- **Page load timing** -- navigation timing API data (DNS, TCP, server response, DOM processing)
- **AJAX/fetch dependency tracking** -- outbound HTTP calls with timing, status, and correlation
- **JavaScript exceptions** -- unhandled errors with stack traces
- **Page views** -- with `enableAutoRouteTracking` for SPAs
- **Core Web Vitals** -- LCP, FID/INP, CLS (when using the performance plugin)

### Node.js APM (automatic)

The Node.js SDK automatically instruments:
- **HTTP/HTTPS requests** -- inbound request timing, response codes
- **Database calls** -- MongoDB, MySQL, PostgreSQL, Redis via dependency tracking
- **External HTTP calls** -- outbound request timing, correlation headers
- **Exceptions** -- unhandled exceptions and promise rejections
- **Console logging** -- `console.log`, `console.error` as trace telemetry

### Custom Request Tracking (Node.js)

For operations not tied to HTTP requests:

```javascript
const client = appInsights.defaultClient;

// Track a dependency call (external service)
client.trackDependency({
  target: 'payment-service',
  name: 'POST /charge',
  data: 'https://api.stripe.com/v1/charges',
  duration: 245,
  resultCode: 200,
  success: true,
  dependencyTypeName: 'HTTP',
});

// Track a custom request
client.trackRequest({
  name: 'ProcessReport',
  url: '/internal/process-report',
  duration: 1250,
  resultCode: 200,
  success: true,
});
```

### Distributed Tracing

Application Insights supports W3C Trace Context for cross-service correlation:

```javascript
// Node.js -- distributed tracing is enabled by default
// The SDK automatically propagates trace context headers:
//   traceparent, tracestate

// Access current operation context
const correlationContext = appInsights.getCorrelationContext();
if (correlationContext) {
  const operationId = correlationContext.operation.id;
  const parentId = correlationContext.operation.parentId;
}
```

## What Application Insights Is NOT

Application Insights is an observability and diagnostics platform. It is **not a product analytics replacement**:

- **No user journey funnels** -- cannot build "signup -> activate -> convert" funnels (the "Funnels" feature in Azure is based on page views and custom events, not behavioral product analytics)
- **No retention cohort analysis** -- no Day 1 / Day 7 / Day 30 retention curves
- **No group/account analytics** -- `accountId` is a tag for filtering, not a first-class entity with properties and aggregated behavior
- **No A/B test analysis** -- no experiment framework or statistical significance testing
- **No behavioral segmentation** -- KQL queries are powerful but oriented around performance and diagnostics, not product usage patterns

**Use Application Insights alongside a product analytics tool** (Amplitude, Mixpanel, PostHog, etc.). Application Insights tells you "the API returned 500 errors for 3% of requests" or "database query latency increased." Product analytics tells you "users who complete the onboarding wizard retain at 2x the rate."

A common pattern is to share the `user_id` and `account_id` as custom properties so you can correlate performance issues with specific users or accounts when investigating anomalies.

## Forge Compatibility

Azure Application Insights is on the Atlassian Forge approved analytics domain list.

**Approved domains:**
- `*.applicationinsights.azure.com`
- `*.monitor.azure.com`

**Manifest configuration:**

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.applicationinsights.azure.com"
          category: analytics
          inScopeEUD: false
        - address: "*.monitor.azure.com"
          category: analytics
          inScopeEUD: false
```

**Note:** The full Node.js SDK (`applicationinsights` npm package) performs deep auto-instrumentation of Node.js modules and may not work in Forge's sandboxed runtime. For Forge apps, use the HTTP Track API via `@forge/api` fetch to send custom events and metrics directly to your Application Insights ingestion endpoint.

## Common Pitfalls

1. **Using instrumentation key instead of connection string** -- Instrumentation key-based ingestion is deprecated (support ended March 31, 2025). Connection strings include the regional ingestion endpoint and are required for sovereign clouds and regional data residency. Always use `connectionString` in configuration, not `instrumentationKey`.

2. **Not calling `flush()` before process exit (Node.js)** -- The Node.js SDK batches telemetry. If your process exits (serverless functions, CLI tools, queue consumers), data in the buffer is lost. Always flush before exit:
   ```javascript
   client.flush({
     callback: () => {
       process.exit(0);
     },
   });
   ```

3. **Setting user context globally on default client (Node.js)** -- In multi-tenant or multi-user server apps, setting `client.context.tags[userId]` on the default client creates a race condition where one request's user context overwrites another's. Use `getCorrelationContext()` or telemetry initializers for per-request context.

4. **Confusing Application Insights events with product analytics events** -- `trackEvent()` creates monitoring events queryable via KQL in Azure Monitor. They are not product analytics events. Do not use Application Insights as your product analytics tool.

5. **Sampling dropping critical events** -- The default SDK sampling may drop events in high-traffic apps. If you track custom events for operational alerting, configure fixed-rate sampling or use telemetry initializers to exclude critical event types from sampling:
   ```javascript
   // Node.js (classic SDK 2.x): Ensure specific events are never sampled out
   client.addTelemetryProcessor((envelope) => {
     // Return true to send, false to drop
     return true;
   });
   // Note: TelemetryProcessors are NOT supported in SDK 3.x.
   // Use OpenTelemetry SpanProcessors instead if on SDK 3.x.
   ```

6. **Bundle size impact (Browser)** -- The full `@microsoft/applicationinsights-web` package adds ~36 KB (gzipped) to your bundle. Consider lazy-loading it after initial page render if bundle size is a concern. Tree-shakeable sub-packages are available for specific features.

## Debugging

### Verify Browser SDK Is Running

```javascript
// Check if SDK is loaded and sending telemetry
// Open browser DevTools console:
appInsights.config; // Shows current configuration

// Check the Network tab for requests to your ingestion endpoint
// Look for POST requests to *.applicationinsights.azure.com/v2/track
```

Enable verbose logging (prefer `loggingLevelConsole` over `enableDebug` to avoid dropped telemetry):

```typescript
const appInsights = new ApplicationInsights({
  config: {
    connectionString: '...',
    // enableDebug: true,  // Caution: throws exceptions on internal errors, drops telemetry
    loggingLevelConsole: 2, // 0=off, 1=critical, 2=warnings+ (recommended for debugging)
    loggingLevelTelemetry: 2,
  },
});
```

### Verify Node.js SDK Is Running

Check for startup messages in the console. Enable internal logging:

```javascript
appInsights.setup(connectionString)
  .setInternalLogging(true, true) // (enableDebugLogging, enableWarningLogging)
  .start();
```

Or via environment variable:

```bash
APPLICATIONINSIGHTS_DEBUG_LOGGING=true
```

### Verify Data in Azure Portal

In the Azure portal, navigate to your Application Insights resource:

1. **Transaction Search** -- search for specific events, requests, exceptions
2. **Live Metrics** -- real-time view of incoming telemetry (enable `setSendLiveMetrics(true)`)
3. **Logs (KQL)** -- query telemetry directly:

```kusto
// Find custom events
customEvents
| where name == "form_submitted"
| where timestamp > ago(1h)
| project timestamp, name, customDimensions

// Find events for a specific user
customEvents
| where customDimensions.user_id == "usr_123"
| order by timestamp desc
| take 50

// Check for errors
exceptions
| where timestamp > ago(1h)
| order by timestamp desc
| take 20
```

### Common Issues

| Symptom | Likely Cause |
|---|---|
| No data in Azure portal | Wrong connection string, firewall blocking `*.applicationinsights.azure.com`, or SDK not started |
| User context missing on events | `setAuthenticatedUserContext()` not called, or called after events fire |
| Duplicate events | SDK initialized multiple times (common in SPA hot-reload during development) |
| High data costs | Sampling not configured; set `samplingPercentage` < 100 for high-traffic apps |
| Node.js telemetry stops after deploy | `flush()` not called before process exit in serverless/container environments |

## Further Documentation

This reference covers the essentials for integrating Application Insights as an application monitoring layer alongside product analytics. For advanced topics, consult Microsoft's official documentation:

- **Getting Started:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
- **JavaScript SDK:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/javascript-sdk
- **JavaScript SDK Configuration:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/javascript-sdk-configuration
- **JavaScript SDK npm Package:** https://www.npmjs.com/package/@microsoft/applicationinsights-web
- **Node.js SDK (Classic API):** https://learn.microsoft.com/en-us/azure/azure-monitor/app/classic-api
- **Node.js SDK npm Package:** https://www.npmjs.com/package/applicationinsights
- **Node.js OpenTelemetry Migration:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-nodejs-migrate
- **Connection Strings:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/connection-strings
- **Custom Events and Metrics:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/api-custom-events-metrics
- **User Context (setAuthenticatedUserContext):** https://learn.microsoft.com/en-us/azure/azure-monitor/app/api-custom-events-metrics#authenticated-users
- **Sampling (Classic API):** https://learn.microsoft.com/en-us/previous-versions/azure/azure-monitor/app/sampling-classic-api
- **Sampling (OpenTelemetry):** https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-sampling
- **KQL (Kusto Query Language):** https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/
- **Distributed Tracing:** https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-trace-data
- **Track API (HTTP):** https://learn.microsoft.com/en-us/azure/azure-monitor/app/api-custom-events-metrics#trackEvent
