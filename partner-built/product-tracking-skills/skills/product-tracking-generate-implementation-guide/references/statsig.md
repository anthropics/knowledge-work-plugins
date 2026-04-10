<!-- Last verified: 2026-03-10 against Statsig docs -->

# Statsig Implementation Reference

## Overview

Statsig is a feature flag, experimentation, and product analytics platform. Unlike LaunchDarkly (which is primarily a flag tool), Statsig includes built-in analytics and metrics — it can track custom events, compute experiment results, and provide usage dashboards natively. It can function as both a flag tool and a lightweight analytics tool, though most teams still pair it with a dedicated product analytics platform (Amplitude, Mixpanel, etc.) for deeper behavioral analysis. Proprietary, cloud-only.

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | JS Client SDK (`@statsig/js-client`) | `npm install @statsig/js-client` |
| Node.js | Node Server Core SDK (`@statsig/statsig-node-core`) | `npm install @statsig/statsig-node-core` |
| Node.js (legacy) | Legacy Node Server SDK (`statsig-node`) | `npm install statsig-node` |
| React | React Bindings (`@statsig/react-bindings`) | `npm install @statsig/react-bindings` |

**Important:** The browser SDK uses a **client API key** (safe to expose, prefixed with `client-`). The Node.js server SDK uses a **server secret key** (never expose client-side).

**Note:** The `statsig-node` package is now the **legacy** Node.js server SDK. The recommended replacement is `@statsig/statsig-node-core`, which is built on a Rust core and offers 5-10x faster evaluations. The legacy SDK examples below remain valid for existing integrations. New projects should use `@statsig/statsig-node-core`.

## Initialization

### Browser

```typescript
import { StatsigClient } from '@statsig/js-client';

const client = new StatsigClient(
  'client-YOUR_CLIENT_API_KEY',
  {
    userID: 'usr_123',
    email: 'jane@example.com',
    custom: {
      role: 'admin',
      plan: 'pro'
    }
  }
);

await client.initializeAsync();
```

### Node.js (recommended — Node Core SDK)

```typescript
import { Statsig, StatsigUser } from '@statsig/statsig-node-core';

const statsig = new Statsig('secret-YOUR_SERVER_SECRET_KEY');
await statsig.initialize();

// With options
const statsig = new Statsig('secret-YOUR_SERVER_SECRET_KEY', {
  environment: 'production'
});
await statsig.initialize();
```

### Node.js (legacy — statsig-node)

```typescript
import Statsig from 'statsig-node';

await Statsig.initialize('secret-YOUR_SERVER_SECRET_KEY', {
  // Optional configuration
  environment: { tier: 'production' }
});
```

## User Context (identify equivalent)

Statsig uses a **StatsigUser** object for flag evaluation and event attribution. This is the equivalent of `identify()` in product analytics tools. The user object determines which gates and experiments the user is assigned to.

**Browser:**

The initial user is set during initialization. To change the user, call `updateUserAsync()`:

```typescript
// Initial user set during init (see Initialization above)

// Switch user context (e.g., after login)
await client.updateUserAsync({
  userID: 'usr_123',
  email: 'jane@example.com',
  custom: {
    role: 'admin',
    plan: 'pro',
    created_at: '2024-01-15T10:30:00Z'
  }
});

// Synchronous variant (uses cached values, fetches in background)
client.updateUserSync({
  userID: 'usr_123',
  email: 'jane@example.com'
});
```

**Node.js (Core SDK):**

Server-side, the user object is passed per evaluation — there is no persistent user state:

```typescript
const user = new StatsigUser({
  userID: 'usr_123',
  email: 'jane@example.com',
  custom: {
    role: 'admin',
    plan: 'pro'
  }
});

// User is passed to each check
const gateEnabled = statsig.checkGate(user, 'new_checkout');
```

**Node.js (legacy):**

```typescript
const user = {
  userID: 'usr_123',
  email: 'jane@example.com',
  custom: {
    role: 'admin',
    plan: 'pro'
  }
};

// User is passed to each check
const gateEnabled = Statsig.checkGate(user, 'new_checkout');
```

**StatsigUser fields:**

| Field | Type | Purpose |
|---|---|---|
| `userID` | string | Unique user identifier. Optional on client SDKs (falls back to Stable ID); effectively required on server SDKs |
| `email` | string | Targeting by email or domain |
| `ip` | string | IP address (auto-inferred on some SDKs) |
| `country` | string | 2-letter ISO country code (auto-inferred from IP) |
| `locale` | string | User locale, e.g. `en_US` |
| `appVersion` | string | Application version |
| `custom` | object | Custom attributes for targeting rules |
| `customIDs` | object | Additional ID types (e.g., `companyID`) |
| `privateAttributes` | object | Used for targeting but stripped from logs |

**When to call (browser):**
- On login — switch from anonymous to identified user
- On user switch — when a different user takes over the session
- When user attributes change that affect targeting rules

## Group / Organization Context

Statsig supports group-level targeting via `customIDs` on the user object. This allows flag rules like "enable for all users in enterprise accounts."

**Browser:**

```typescript
await client.updateUserAsync({
  userID: 'usr_123',
  email: 'jane@example.com',
  custom: {
    role: 'admin'
  },
  customIDs: {
    companyID: 'acc_456',
    workspaceID: 'ws_789'
  }
});
```

**Node.js (Core SDK):**

```typescript
const user = new StatsigUser({
  userID: 'usr_123',
  custom: {
    role: 'admin'
  },
  customIDs: {
    companyID: 'acc_456',
    workspaceID: 'ws_789'
  }
});

const showFeature = statsig.checkGate(user, 'enterprise_dashboard');
```

**Node.js (legacy):**

```typescript
const user = {
  userID: 'usr_123',
  custom: {
    role: 'admin'
  },
  customIDs: {
    companyID: 'acc_456',
    workspaceID: 'ws_789'
  }
};

const showFeature = Statsig.checkGate(user, 'enterprise_dashboard');
```

**Using `customIDs` for account-level experiments:**

Statsig can randomize experiments at the account level (not user level) by configuring the experiment to use a `customID` as the unit type. This ensures all users in the same account see the same variation.

In the Statsig console, create a custom ID type (e.g., `companyID`) and configure experiments to use it as the ID type. Then pass it in the user object:

```typescript
// Node.js Core SDK
const user = new StatsigUser({
  userID: 'usr_123',
  customIDs: {
    companyID: 'acc_456'  // Experiment randomizes by this ID
  }
});

// All users with companyID 'acc_456' see the same variation
const experiment = statsig.getExperiment(user, 'pricing_experiment');
```

## Flag Evaluation (Feature Gates)

Statsig calls boolean flags **Feature Gates**.

### Boolean Gates

**Browser:**
```typescript
const showNewCheckout = client.checkGate('new_checkout');

if (showNewCheckout) {
  renderNewCheckout();
} else {
  renderOldCheckout();
}

// With manual exposure control (suppress automatic exposure logging)
const result = client.checkGate('new_checkout', { disableExposureLog: true });
```

**Node.js (Core SDK):**
```typescript
const user = new StatsigUser({ userID: 'usr_123' });
const showNewCheckout = statsig.checkGate(user, 'new_checkout');
```

**Node.js (legacy):**
```typescript
const user = { userID: 'usr_123' };
const showNewCheckout = Statsig.checkGate(user, 'new_checkout');
```

### Experiments (Multivariate)

```typescript
// Browser
const experiment = client.getExperiment('pricing_experiment');
const variant = experiment.get('variant', 'control');
// Returns the parameter value configured in the Statsig console

// Access multiple parameters
const ctaText = experiment.get('cta_text', 'Sign Up');
const ctaColor = experiment.get('cta_color', 'blue');
const showBanner = experiment.get('show_banner', false);

// With manual exposure control
const experiment = client.getExperiment('pricing_experiment', {
  disableExposureLog: true
});
```

```typescript
// Node.js (Core SDK) — uses .getValue() instead of .get()
const user = new StatsigUser({ userID: 'usr_123' });
const experiment = statsig.getExperiment(user, 'pricing_experiment');
const variant = experiment.getValue('variant', 'control');
```

```typescript
// Node.js (legacy) — uses .get()
const user = { userID: 'usr_123' };
const experiment = Statsig.getExperiment(user, 'pricing_experiment');
const variant = experiment.get('variant', 'control');
```

### Dynamic Configs

Statsig also has **Dynamic Configs** — key-value configurations that can be targeted to specific users/groups without running an experiment:

```typescript
// Browser
const config = client.getDynamicConfig('feature_limits');
const maxReports = config.get('max_reports', 10);
const exportFormats = config.get('export_formats', ['csv']);

// Node.js (Core SDK) — uses getDynamicConfig + .getValue()
const config = statsig.getDynamicConfig(user, 'feature_limits');
const maxReports = config.getValue('max_reports', 10);

// Node.js (legacy) — uses getConfig + .get()
const config = Statsig.getConfig(user, 'feature_limits');
const maxReports = config.get('max_reports', 10);
```

## Tracking Flag Exposures as Events

Statsig **automatically tracks gate checks and experiment exposures** internally. Every call to `checkGate()` or `getExperiment()` generates an exposure event in Statsig's analytics. This is a key difference from LaunchDarkly — you do not need to manually track exposures for Statsig's own experiment analysis.

However, to analyze experiment impact in an **external** analytics tool (Amplitude, Mixpanel, etc.), you still need to forward exposure data:

### Manual Exposure Forwarding Pattern

```typescript
// Helper: evaluate gate and forward exposure to product analytics
function checkGateAndTrack(gateName: string) {
  const result = client.checkGate(gateName);

  // Forward to product analytics (e.g., Segment)
  analytics.track('experiment.exposure', {
    gate_name: gateName,
    gate_value: result,
    user_id: 'usr_123'
  });

  return result;
}

// Helper: get experiment and forward exposure
function getExperimentAndTrack(experimentName: string) {
  const experiment = client.getExperiment(experimentName);

  analytics.track('experiment.exposure', {
    experiment_name: experimentName,
    group_name: experiment.getGroupName(),
    user_id: 'usr_123'
  });

  return experiment;
}
```

### Statsig Data Warehouse Export

Statsig can export all exposure and event data to your data warehouse (BigQuery, Snowflake, Redshift, Databricks). This gives you raw exposure logs without needing to instrument forwarding in your application code.

## Custom Events / Metrics

Statsig has **built-in event tracking** that feeds directly into its experiment metrics and analytics dashboards. This is a notable difference from LaunchDarkly, where custom events only feed experiment metrics.

**Browser:**
```typescript
// Simple event
client.logEvent('checkout_completed');

// Event with value (for numeric metrics like revenue)
client.logEvent('purchase', 149.99);

// Event with metadata
client.logEvent('feature_used', null, {
  feature_name: 'export',
  format: 'csv',
  report_id: 'rpt_789'
});

// Event with both value and metadata
client.logEvent('cart_total', 149.99, {
  item_count: 3,
  currency: 'usd'
});

// Object syntax (alternative)
client.logEvent({
  eventName: 'add_to_cart',
  value: 'SKU_12345',
  metadata: {
    price: '9.99',
    item_name: 'diet_coke_48_pack'
  }
});
```

**Node.js (Core SDK):**
```typescript
const user = new StatsigUser({ userID: 'usr_123' });

// Simple event
statsig.logEvent(user, 'checkout_completed');

// Event with value
statsig.logEvent(user, 'purchase', 149.99);

// Event with metadata
statsig.logEvent(user, 'feature_used', null, {
  feature_name: 'export',
  format: 'csv'
});
```

**Node.js (legacy):**
```typescript
const user = { userID: 'usr_123' };

// Simple event
Statsig.logEvent(user, 'checkout_completed');

// Event with value
Statsig.logEvent(user, 'purchase', 149.99);

// Event with metadata
Statsig.logEvent(user, 'feature_used', null, {
  feature_name: 'export',
  format: 'csv'
});
```

**Statsig Metrics:**

Events logged via `logEvent()` automatically feed into:
- **Experiment metrics** — conversion rates, mean values, percentiles
- **Pulse** — Statsig's built-in analytics dashboard showing metric trends
- **Metric Lifts** — automatic computation of how experiments affect key metrics
- **Custom Metrics** — define composite metrics (ratios, funnels, retention) from raw events

## Analytics Integration Pattern

Statsig can act as both a flag tool and a lightweight analytics tool. The integration pattern depends on how much you rely on Statsig's built-in analytics vs. an external tool.

### Pattern 1: Statsig + External Analytics (most common)

Use Statsig for flags and experiments. Use an external tool for full product analytics.

```
┌──────────────────────────────────────────────────────────┐
│                     Your Application                     │
│                                                          │
│   1. Check gate / get experiment → Statsig SDK           │
│   2. Track exposure → Product Analytics (optional)       │
│   3. Track behavior → Product Analytics + Statsig        │
│   4. Experiment metrics → Statsig (automatic via events) │
│                                                          │
└──────────┬──────────────────┬──────────────────┬─────────┘
           │                  │                  │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │   Statsig   │   │   Segment   │   │  Amplitude  │
    │ (flags +    │   │  (routing)  │   │ (analysis)  │
    │ experiments │   │             │   │             │
    │ + metrics)  │   │             │   │             │
    └─────────────┘   └─────────────┘   └─────────────┘
```

### Pattern 2: Statsig as Primary Analytics

For smaller teams, Statsig's built-in Pulse dashboards and metrics can serve as a lightweight product analytics tool. In this case, `logEvent()` replaces `track()`:

```typescript
// Track product events in Statsig only
client.logEvent('report_created', null, {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});

client.logEvent('checkout_completed', 149.99, {
  payment_method: 'credit_card'
});
```

**Limitation:** Statsig's analytics is optimized for experiment analysis and metric tracking. It does not have the full behavioral analytics capabilities (funnels, cohorts, user journeys, retention charts) of dedicated product analytics tools like Amplitude or Mixpanel.

### Combined Example (Pattern 1)

```typescript
// 1. Check the gate
const showNewCheckout = client.checkGate('new_checkout_flow');
// Statsig automatically records this exposure internally

// 2. Optionally forward exposure to external analytics
analytics.track('experiment.exposure', {
  gate_name: 'new_checkout_flow',
  gate_value: showNewCheckout
});

// 3. User completes the action — track in both systems
analytics.track('checkout.completed', {
  order_value: 149.99,
  checkout_variant: showNewCheckout ? 'new' : 'control'
});

// 4. Track metric in Statsig for experiment analysis
client.logEvent('checkout_completed', 149.99);
```

## Forge Compatibility

Statsig is on the Atlassian Forge approved analytics domain list.

**Approved domains:**
- `*.statsigapi.net`
- `statsigapi.net`
- `*.featureassets.org`
- `featureassets.org`
- `*.prodregistryv2.org`
- `prodregistryv2.org`

**Manifest configuration:**
```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.statsigapi.net"
          category: analytics
          inScopeEUD: false
        - address: "statsigapi.net"
          category: analytics
          inScopeEUD: false
        - address: "*.featureassets.org"
          category: analytics
          inScopeEUD: false
        - address: "featureassets.org"
          category: analytics
          inScopeEUD: false
        - address: "*.prodregistryv2.org"
          category: analytics
          inScopeEUD: false
        - address: "prodregistryv2.org"
          category: analytics
          inScopeEUD: false
```

**Note:** Statsig uses multiple domains — `statsigapi.net` for API calls, `featureassets.org` and `prodregistryv2.org` for SDK config and gate/experiment definitions. All must be declared. In Forge apps, use the Node.js server SDK in backend resolvers. Flag evaluations should happen server-side, with results passed to the frontend via `invoke()`.

## Common Pitfalls

1. **Using the server secret key client-side** — The server secret key must never be exposed in browser code. Browser apps must use the client API key (prefixed with `client-`). Exposing the server key allows anyone to modify gates, experiments, and configs.

2. **Not awaiting initialization** — Both browser and server SDKs require initialization before gate checks or experiment evaluations work. Calling `checkGate()` before `initializeAsync()` resolves returns `false` for all gates. Always `await` initialization:
   ```typescript
   // Wrong
   const client = new StatsigClient(key, user);
   client.checkGate('feature'); // Always returns false

   // Right
   const client = new StatsigClient(key, user);
   await client.initializeAsync();
   client.checkGate('feature'); // Correct value
   ```

3. **Forgetting `customIDs` for account-level experiments** — If an experiment is configured to randomize by `companyID` but you do not include `companyID` in `customIDs`, all users are assigned to the default group. Account-level experiments require matching `customIDs` on every evaluation.

4. **Logging events without a user context (server-side)** — The Node.js SDK requires a user object on every `logEvent()` call. Without a `userID`, events cannot be attributed to users or counted toward experiment metrics. Anonymous events are effectively lost.

5. **Not shutting down the server SDK** — Call `shutdown()` on process exit to flush pending events. Without this, the last batch of events may be lost:
   ```typescript
   // Node Core SDK
   process.on('SIGTERM', async () => {
     await statsig.shutdown();
     process.exit(0);
   });

   // Legacy SDK
   process.on('SIGTERM', async () => {
     await Statsig.shutdown();
     process.exit(0);
   });
   ```

6. **Assuming Statsig replaces product analytics** — While Statsig has built-in event tracking and Pulse dashboards, it is optimized for experiment metrics, not full behavioral analytics. Teams needing funnels, cohorts, retention analysis, or user journey mapping should pair Statsig with a dedicated product analytics tool.

7. **Using the legacy `statsig-node` for new projects** — The `statsig-node` package is now legacy. New Node.js projects should use `@statsig/statsig-node-core`, which is faster (Rust core) and actively maintained. The legacy SDK remains functional for existing integrations but will not receive new features.

## Debugging

### Browser
```typescript
import { LogLevel, StatsigClient } from '@statsig/js-client';

// Enable debug logging during initialization
const client = new StatsigClient(
  'client-YOUR_KEY',
  user,
  { logLevel: LogLevel.Debug }
);

// Inspect current gate values
console.log(client.checkGate('feature_gate'));

// Inspect experiment values
const exp = client.getExperiment('experiment_name');
console.log(exp.getGroupName()); // Which group the user is in
console.log(exp.getValue()); // All parameter values

// Browser console: access __STATSIG__ global for inspection
```

### Node.js (Core SDK)
```typescript
const user = new StatsigUser({ userID: 'usr_123' });

// Check gate with logging
const result = statsig.checkGate(user, 'feature_gate');
console.log('Gate result:', result);

// Get experiment details
const exp = statsig.getExperiment(user, 'experiment_name');
console.log('Group:', exp.getGroupName());
```

### Node.js (legacy)
```typescript
// Check gate with logging
const result = Statsig.checkGate(user, 'feature_gate');
console.log('Gate result:', result);

// Get experiment details
const exp = Statsig.getExperiment(user, 'experiment_name');
console.log('Group:', exp.getGroupName());
console.log('Value:', exp.getValue());
```

### Statsig Console
- **Diagnostics** tab on each gate/experiment — shows evaluation results by user
- **Log Stream** — real-time feed of exposures and custom events
- **Pulse** — automated metric analysis for running experiments
- **Test Gate** — manually test a gate evaluation for a specific user context

### Verifying Events
```typescript
// Browser: check that events are being sent
// Open Network tab → filter for "statsigapi.net"
// Look for POST requests to /v1/rgstr (event registration)

// Node.js Core SDK: verify initialization
const statsig = new Statsig('secret-KEY');
statsig.initialize().then(() => {
  console.log('Statsig initialized successfully');
}).catch((err) => {
  console.error('Statsig initialization failed:', err);
});
```

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Statsig's official documentation:

- **SDK Overview:** https://docs.statsig.com/sdks/getting-started
- **JavaScript Client SDK:** https://docs.statsig.com/client/javascript-sdk
- **Node.js Server Core SDK:** https://docs.statsig.com/server-core/node-core
- **Node.js Server SDK (legacy):** https://docs.statsig.com/server/nodejsServerSDK
- **React SDK:** https://docs.statsig.com/client/javascript-sdk/react
- **Feature Gates:** https://docs.statsig.com/feature-gates/working-with
- **Experiments:** https://docs.statsig.com/experiments-plus
- **Custom Metrics:** https://docs.statsig.com/metrics
- **Pulse (Analytics):** https://docs.statsig.com/pulse
- **Custom Event Logging:** https://docs.statsig.com/guides/logging-events
- **Data Warehouse Export:** https://docs.statsig.com/integrations/data-exports/data_warehouse_exports
- **StatsigUser Object:** https://docs.statsig.com/sdks/user
- **JS SDK Migration Guide:** https://docs.statsig.com/client/javascript-sdk/migrating-from-statsig-js/
