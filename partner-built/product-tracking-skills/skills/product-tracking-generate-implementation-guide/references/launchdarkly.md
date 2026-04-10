<!-- Last verified: 2026-03-10 against LaunchDarkly docs -->
# LaunchDarkly Implementation Reference

## SDK Version Note

The JavaScript Client SDK v4 is available as `@launchdarkly/js-client-sdk` with a significantly different API (e.g., `createClient()` + `start()` instead of `initialize()`, typed variation methods). This reference currently documents v3.x patterns (`launchdarkly-js-client-sdk`), which remain supported.

## Overview

LaunchDarkly is a feature flag and experimentation platform. It is not a product analytics tool, but it manages user and group targeting context for flag evaluation and tracks flag exposure events. Typically paired with a product analytics tool (Amplitude, Mixpanel, Segment, etc.) for experiment analysis and behavioral metrics. Proprietary, cloud-only.

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | JS Client SDK (`launchdarkly-js-client-sdk`) | `npm install launchdarkly-js-client-sdk` |
| Node.js | Node Server SDK (`@launchdarkly/node-server-sdk`) | `npm install @launchdarkly/node-server-sdk` |
| React | React SDK (`launchdarkly-react-client-sdk`) | `npm install launchdarkly-react-client-sdk` |

**Important:** The browser SDK uses a **client-side ID** (safe to expose). The Node.js server SDK uses an **SDK key** (secret, never expose client-side).

## Initialization

### Browser

```typescript
import * as LDClient from 'launchdarkly-js-client-sdk';

// Client-side ID from LaunchDarkly dashboard → Environments
const client = LDClient.initialize('YOUR_CLIENT_SIDE_ID', {
  kind: 'user',
  key: 'usr_123',
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'admin',
  plan: 'pro'
});

// Wait for flags to load before evaluating
client.on('ready', () => {
  console.log('LaunchDarkly flags loaded');
});

// Or use waitForInitialization()
await client.waitForInitialization();
```

### Node.js

```typescript
import * as LaunchDarkly from '@launchdarkly/node-server-sdk';

const client = LaunchDarkly.init('YOUR_SDK_KEY');

// Wait for initialization before evaluating flags
await client.waitForInitialization();
```

## User Context (identify equivalent)

LaunchDarkly uses a **context** object for flag evaluation. The context determines which flags and variations a user sees. This is the equivalent of `identify()` in product analytics tools.

**Browser:**

The initial context is passed at initialization. To change the user (e.g., on login or user switch), call `identify()`:

```typescript
// Initial context set during init (see Initialization above)

// Switch user context (e.g., after login)
await client.identify({
  kind: 'user',
  key: 'usr_123',
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'admin',
  plan: 'pro',
  created_at: '2024-01-15T10:30:00Z'
});
```

**Node.js:**

Server-side, context is passed per flag evaluation — there is no persistent user state:

```typescript
const context = {
  kind: 'user',
  key: 'usr_123',
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'admin',
  plan: 'pro'
};

// Context is passed to each variation call
const showFeature = await client.variation('new-checkout', context, false);
```

**When to call (browser):**
- On login — switch from anonymous to identified user
- On user switch — when a different user takes over the session
- When user attributes change that affect targeting rules

## Group / Organization Context

LaunchDarkly supports **multi-kind contexts** for targeting by both user and organization. This enables flag rules like "enable for all users in enterprise accounts."

**Browser:**

```typescript
await client.identify({
  kind: 'multi',
  user: {
    key: 'usr_123',
    name: 'Jane Smith',
    email: 'jane@example.com',
    role: 'admin'
  },
  organization: {
    key: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    industry: 'technology',
    employee_count: 150
  }
});
```

**Node.js:**

```typescript
const context = {
  kind: 'multi',
  user: {
    key: 'usr_123',
    name: 'Jane Smith',
    role: 'admin'
  },
  organization: {
    key: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    employee_count: 150
  }
};

const showFeature = await client.variation('enterprise-dashboard', context, false);
```

You can define any context kind names — `organization`, `workspace`, `project`, etc. These map to your product's group hierarchy. Multi-kind contexts allow targeting rules that combine user attributes with group attributes.

## Flag Evaluation

### Boolean Flags

**Browser:**
```typescript
// Browser flags are evaluated locally (cached from server)
const showNewCheckout = client.variation('new-checkout', false);

if (showNewCheckout) {
  renderNewCheckout();
} else {
  renderOldCheckout();
}
```

**Node.js:**
```typescript
const context = { kind: 'user', key: 'usr_123' };

const showNewCheckout = await client.variation('new-checkout', context, false);
// Third argument is the default value if flag is not found
```

### Multivariate Flags

```typescript
// Browser
const pricingTier = client.variation('pricing-experiment', 'control');
// Returns: 'control' | 'variant-a' | 'variant-b'

// Node.js
const pricingTier = await client.variation('pricing-experiment', context, 'control');
```

### Variation Detail (with reason)

```typescript
// Browser
const detail = client.variationDetail('new-checkout', false);
// detail.value — the flag value
// detail.variationIndex — which variation was served
// detail.reason — why this variation was chosen (e.g., rule match, fallthrough)

// Node.js
const detail = await client.variationDetail('new-checkout', context, false);
```

## Tracking Flag Exposures as Events

LaunchDarkly automatically tracks flag evaluations internally. To pipe these exposure events to external analytics tools for experiment analysis, use **Data Export** or **integrations**.

### Data Export Destinations

LaunchDarkly can export flag evaluation events to:
- **Segment** — sends `$ld:flag` events as Segment track calls
- **mParticle** — forwards evaluation data
- **Kinesis, Pub/Sub, Azure Event Hubs** — raw event streams for data warehouses

Configure these in LaunchDarkly dashboard → Integrations → Data Export.

### Listening to Flag Changes (Browser)

```typescript
// React to flag value changes in real-time
client.on('change:new-checkout', (newValue, oldValue) => {
  console.log(`Flag changed from ${oldValue} to ${newValue}`);

  // Forward to your analytics tool
  analytics.track('experiment.exposure', {
    flag_key: 'new-checkout',
    variation: newValue,
    previous_variation: oldValue
  });
});

// Listen to all flag changes
client.on('change', (changes) => {
  // changes is an object of { flagKey: { current, previous } }
  Object.entries(changes).forEach(([flagKey, { current, previous }]) => {
    analytics.track('experiment.exposure', {
      flag_key: flagKey,
      variation: current
    });
  });
});
```

### Manual Exposure Tracking Pattern

For experiment analysis, manually forward flag evaluations to your product analytics tool:

```typescript
// Helper: evaluate flag and track exposure
function evaluateAndTrack(flagKey: string, defaultValue: any) {
  const detail = client.variationDetail(flagKey, defaultValue);

  // Send exposure event to product analytics (e.g., Segment, Amplitude)
  analytics.track('experiment.exposure', {
    flag_key: flagKey,
    variation_value: detail.value,
    variation_index: detail.variationIndex,
    reason: detail.reason?.kind
  });

  return detail.value;
}

// Usage
const variant = evaluateAndTrack('pricing-experiment', 'control');
```

## Custom Events / Metrics

LaunchDarkly supports custom events for experiment goal metrics. These events are used within LaunchDarkly to measure experiment outcomes — they do NOT replace product analytics events.

**Browser:**
```typescript
// Simple event (for conversion metrics)
client.track('checkout-completed');

// Event with numeric value (for numeric metrics)
client.track('cart-total', undefined, 149.99);

// Event with custom data
client.track('feature-used', { feature_name: 'export', format: 'csv' });
```

**Node.js:**
```typescript
const context = { kind: 'user', key: 'usr_123' };

// Simple event
client.track('checkout-completed', context);

// Event with numeric value
client.track('cart-total', context, undefined, 149.99);

// Event with custom data
client.track('feature-used', context, { feature_name: 'export' });
```

These metric events are used in LaunchDarkly's Experimentation to calculate statistical significance of experiment outcomes. They do not flow to external analytics tools automatically.

## Analytics Integration Pattern

LaunchDarkly is a flag/experimentation tool that works **alongside** product analytics, not as a replacement. The typical integration pattern:

```
┌─────────────────────────────────────────────────────────┐
│                     Your Application                    │
│                                                         │
│   1. Evaluate flag → LaunchDarkly SDK                   │
│   2. Track exposure → Product Analytics (Segment, etc.) │
│   3. Track behavior → Product Analytics                 │
│   4. Track metric → LaunchDarkly SDK (for experiments)  │
│                                                         │
└──────────┬──────────────────┬──────────────────┬────────┘
           │                  │                  │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │ LaunchDarkly │   │   Segment   │   │  Amplitude  │
    │  (flags +    │   │  (routing)  │   │ (analysis)  │
    │  experiments)│   │             │   │             │
    └─────────────┘   └─────────────┘   └─────────────┘
```

**Two-way data flow:**
1. **Flag exposure → Analytics tool** — Send which variation the user saw so you can segment behavior by experiment group
2. **Product events → LaunchDarkly metrics** — Track conversion events via `client.track()` so LaunchDarkly can calculate experiment results

### Combined Example

```typescript
// 1. Evaluate the flag
const checkoutVariant = client.variation('new-checkout-flow', 'control');

// 2. Track exposure in product analytics
analytics.track('experiment.exposure', {
  experiment_key: 'new-checkout-flow',
  variation: checkoutVariant,
  user_id: 'usr_123'
});

// 3. User completes the action — track in both systems
analytics.track('checkout.completed', {
  order_value: 149.99,
  checkout_variant: checkoutVariant  // Include variant for segmentation
});

// 4. Track metric in LaunchDarkly for experiment analysis
client.track('checkout-completed', undefined, 149.99);
```

## Forge Compatibility

LaunchDarkly is on the Atlassian Forge approved analytics domain list.

**Approved domains:**
- `*.launchdarkly.com`

**Manifest configuration:**
```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.launchdarkly.com"
          category: analytics
          inScopeEUD: false
```

**Note:** In Forge apps, use the Node.js server SDK in backend resolvers. The browser client SDK cannot be used in Forge Custom UI iframes because direct external network calls are blocked. Flag evaluations should happen server-side, with results passed to the frontend via `invoke()`.

## Common Pitfalls

1. **Using the SDK key client-side** — The server SDK key is secret. Browser apps must use the client-side ID. Exposing the SDK key allows anyone to read all flag configurations and targeting rules.

2. **Evaluating flags before initialization** — Both browser and server SDKs require initialization before flag values are available. Always `await client.waitForInitialization()` or use the `ready` event before calling `variation()`. Evaluating early returns the default value silently.

3. **Not passing context on server-side evaluations** — The Node.js SDK has no persistent user context. Every `variation()` call requires an explicit context object. Forgetting this returns the default value for all users.

4. **Forgetting to track exposures in analytics** — LaunchDarkly tracks flag evaluations internally, but your product analytics tool does not know about them unless you explicitly send exposure events. Without exposure tracking in your analytics, you cannot segment user behavior by experiment variation.

5. **Mixing up `track()` purposes** — LaunchDarkly's `client.track()` sends events to LaunchDarkly for experiment metrics. It does NOT send events to your product analytics tool. You need to call both `client.track()` (for LaunchDarkly experiments) and `analytics.track()` (for product analytics) when an event matters to both systems.

6. **Not shutting down the server SDK** — The Node.js SDK maintains a streaming connection. Call `client.close()` on process exit to flush pending events and cleanly disconnect:
   ```typescript
   process.on('SIGTERM', async () => {
     await client.close();
     process.exit(0);
   });
   ```

## Debugging

### Browser
```typescript
// Enable debug logging
const client = LDClient.initialize('YOUR_CLIENT_SIDE_ID', context, {
  logger: LDClient.basicLogger({ level: 'debug' })
});

// Inspect all flag values
const allFlags = client.allFlags();
console.log(allFlags);

// Inspect a specific flag with reason
const detail = client.variationDetail('new-checkout', false);
console.log(detail.reason);
// e.g., { kind: 'RULE_MATCH', ruleIndex: 0, ruleId: 'rule-123' }
```

### Node.js
```typescript
const client = LaunchDarkly.init('YOUR_SDK_KEY', {
  logger: LaunchDarkly.basicLogger({ level: 'debug' })
});

// Evaluate with reason
const detail = await client.variationDetail('new-checkout', context, false);
console.log(detail.reason);
```

### LaunchDarkly Dashboard
- **Flag Insights** — shows evaluation counts per variation, per environment
- **Live Events** — real-time stream of flag evaluations and custom events
- **Debugger** — filter events by user key, flag key, or context kind

### Flag Status Check
```typescript
// Browser: check connection status
console.log(client.getContext()); // current context
console.log(client.variation('flag-key', 'default')); // current value

// Node.js: verify client is initialized
client.waitForInitialization().then(() => {
  console.log('SDK initialized and connected');
}).catch((err) => {
  console.error('SDK failed to initialize:', err);
});
```

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult LaunchDarkly's official documentation:

- **Getting Started:** https://launchdarkly.com/docs/home/getting-started
- **JavaScript Client SDK:** https://launchdarkly.com/docs/sdk/client-side/javascript
- **Node.js Server SDK:** https://launchdarkly.com/docs/sdk/server-side/node-js
- **React SDK:** https://launchdarkly.com/docs/sdk/client-side/react
- **Contexts and Targeting:** https://launchdarkly.com/docs/home/flags/contexts/intro
- **Multi-Kind Contexts:** https://launchdarkly.com/docs/home/observability/multi-contexts
- **Experimentation:** https://launchdarkly.com/docs/home/experimentation
- **Custom Metrics:** https://launchdarkly.com/docs/home/metrics/create-metrics
- **Data Export:** https://launchdarkly.com/docs/integrations/data-export
- **Integrations (Segment, Amplitude, etc.):** https://launchdarkly.com/docs/integrations
