<!-- Last verified: 2026-03-10 against Hotjar docs -->
# Hotjar Implementation Reference

## Overview

Hotjar is a session recording, heatmap, and user feedback tool. It provides qualitative behavioral data — watching what users actually do on the page — to supplement quantitative product analytics. Hotjar is proprietary and cloud-only.

**Category: Session / Behavior Tool.** Hotjar supplements product analytics with qualitative data. It is not a replacement for event tracking, funnels, or account-level analytics.

## Integration

### Script Tag (Standard Installation)

Add the Hotjar tracking code to the `<head>` of every page. The Site ID is found in Hotjar under Organization > Tracking Code.

```html
<script>
  (function(h,o,t,j,a,r){
    h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
    h._hjSettings={hjid:YOUR_SITE_ID,hjsv:6};
    a=o.getElementsByTagName('head')[0];
    r=o.createElement('script');r.async=1;
    r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
    a.appendChild(r);
  })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
```

Replace `YOUR_SITE_ID` with your numeric Hotjar Site ID.

### npm Package

Hotjar provides an official npm package (`@hotjar/browser`) — see the next section. For cases where you prefer to avoid a dependency, the script can also be injected programmatically:

```typescript
// Initialize Hotjar programmatically
export function initHotjar(siteId: number): void {
  (function(h: any, o: Document, t: string, j: string) {
    h.hj = h.hj || function() { (h.hj.q = h.hj.q || []).push(arguments); };
    h._hjSettings = { hjid: siteId, hjsv: 6 };
    const a = o.getElementsByTagName('head')[0];
    const r = o.createElement('script');
    r.async = true;
    r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
    a.appendChild(r);
  })(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');
}

// Call on app init
initHotjar(YOUR_SITE_ID);
```

### @hotjar/browser (Official npm Package)

Hotjar also offers an official npm package:

```bash
npm install @hotjar/browser
```

```typescript
import Hotjar from '@hotjar/browser';

Hotjar.init(YOUR_SITE_ID, 6); // siteId, hotjarVersion

// Optional: enable debug mode or pass a CSP nonce
Hotjar.init(YOUR_SITE_ID, 6, { debug: true });
Hotjar.init(YOUR_SITE_ID, 6, { nonce: 'your-csp-nonce' });
```

## Initialization

Hotjar initializes automatically when the script loads. The `hj()` function becomes available globally. All API calls use the `hj()` function with a command string as the first argument.

```typescript
// Verify Hotjar is loaded
if (typeof hj === 'function') {
  // Hotjar is ready
}
```

With the npm package:

```typescript
import Hotjar from '@hotjar/browser';

Hotjar.init(YOUR_SITE_ID, 6);

if (Hotjar.isReady()) {
  // Hotjar is initialized
}
```

## User Identification

Tag sessions with known user identity so recordings and feedback can be associated with specific users. This does NOT create a persistent user profile like product analytics tools — it tags the current session.

**Browser:**

```javascript
// Using the global hj() function
hj('identify', 'usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  plan: 'pro',
  role: 'admin',
  account_id: 'acc_456'
});
```

```typescript
// Using @hotjar/browser
import Hotjar from '@hotjar/browser';

Hotjar.identify('usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  plan: 'pro',
  role: 'admin',
  account_id: 'acc_456'
});
```

**Constraints on identify attributes:**

| Constraint | Value |
|---|---|
| Max attributes per site | 100 |
| Attribute name max length | 50 characters |
| String attribute value max length | 255 characters <!-- UNVERIFIED: 255 not explicitly confirmed in current docs; Hotjar docs confirm the 50-char attribute name limit but do not prominently state the value length limit --> |
| User ID max length | 255 characters <!-- UNVERIFIED: not explicitly stated in current Hotjar docs --> |

Attribute values must be strings, numbers, or booleans. Nested objects and arrays are not supported.

**When to call:** On login, and on every page load where the user is known (Hotjar does not persist identity across page loads by default in all configurations).

## Custom Events / Triggers

Hotjar uses events to trigger recordings, surveys, and other behaviors. Events can be sent from JavaScript to activate Hotjar features configured in the dashboard.

```javascript
// Trigger a Hotjar event
hj('event', 'report_created');

// Using @hotjar/browser
Hotjar.event('report_created');
```

Events in Hotjar are used to:
1. **Start recordings** when specific events fire (configured in Hotjar dashboard under Recordings > Targeting)
2. **Show surveys** when events fire (configured under Surveys > Targeting > JavaScript trigger)
3. **Filter recordings** by events in the Hotjar dashboard

```javascript
// Example: trigger events for key product actions
hj('event', 'signup_completed');
hj('event', 'onboarding_finished');
hj('event', 'feature_first_used');
hj('event', 'plan_upgraded');
```

**Event naming:** Event names are case-sensitive strings. Use `snake_case` for consistency with product analytics conventions. Maximum length is 250 characters. Allowed characters: alphanumeric (a-z, A-Z, 0-9), underscores (`_`), dashes (`-`), spaces, periods (`.`), colons (`:`), pipes (`|`), and forward slashes (`/`). There is a limit of 10,000 unique events per Hotjar site, and only the first 50 unique events in a single session are searchable by filters.

### Triggering Surveys via JavaScript

Surveys configured with a JavaScript trigger can be shown programmatically:

```javascript
// In Hotjar dashboard: set survey trigger to "JavaScript trigger"
// The event name must match the trigger configured in the dashboard
hj('event', 'completed_checkout');
// If a survey is configured to trigger on 'completed_checkout', it appears
```

## Session Recording

Hotjar records sessions by default once recording is enabled in the dashboard. Recordings capture DOM mutations, mouse movements, clicks, scrolls, and form interactions.

**IMPORTANT: Session recording captures everything visible on the page by default.** This includes text content, form values, and any data rendered in the UI. Privacy controls are essential.

### How Recording Works

1. Recording is enabled in the Hotjar dashboard (Recordings section)
2. Sessions are recorded based on targeting rules (URL, device, user attributes, events)
3. Recordings are stored in Hotjar's cloud for 365 days (varies by plan)
4. Recordings can be tagged, filtered, and shared in the dashboard

### Manual Recording Control

**Legacy approach (deprecated but still functional):**

```javascript
// hj('trigger', ...) is legacy — still respected by Hotjar but triggers are
// NOT searchable in Recordings filters and cannot be used for targeting.
hj('trigger', 'record_this_session');
```

**Current approach — use the Events API instead:**

```javascript
// Use hj('event', ...) to trigger recordings via event-based targeting
hj('event', 'record_this_session');

// Using @hotjar/browser
Hotjar.event('record_this_session');
```

Configure event-based recording targeting in the Hotjar dashboard under Recordings > Targeting.

### State Tags

Add tags to recordings for later filtering:

```javascript
hj('stateChange', '/virtual/checkout/step-2');
```

This is useful in SPAs where URL changes are not detected automatically. It creates a "virtual page view" in the recording timeline.

## Privacy Controls

**Session recording has significant privacy implications.** Hotjar captures the visual state of the page, which can include sensitive data. Use these controls to prevent leakage.

### Suppress Sensitive Content (HTML Data Attributes)

Hotjar uses HTML data attributes to control what is recorded:

| Attribute | Effect | Use For |
|---|---|---|
| `data-hj-suppress` | Replaces element content with a placeholder in recordings | PII, account data, financial info |
| `data-hj-allow` | Explicitly allows content (overrides global suppression) | Non-sensitive content in a suppressed container |

```html
<!-- Suppress sensitive content in recordings -->
<div data-hj-suppress>
  <p>Account balance: $12,345.67</p>
  <p>SSN: 123-45-6789</p>
</div>

<!-- Allow specific content inside a suppressed parent -->
<div data-hj-suppress>
  <p>Sensitive info here (hidden)</p>
  <p data-hj-allow>This label is visible in recordings</p>
</div>
```

### Input Masking

By default, Hotjar masks all input field values in recordings. This can be configured:

```html
<!-- Inputs are masked by default — values show as ****** -->
<input type="text" name="email" />

<!-- Explicitly mark as unmasked (use only for non-sensitive fields) -->
<input type="text" name="search_query" data-hj-allow />

<!-- Explicitly suppress an entire form section -->
<form data-hj-suppress>
  <input type="text" name="credit_card" />
  <input type="text" name="cvv" />
</form>
```

### Exclude Specific Pages

In the Hotjar dashboard, configure URL exclusion rules to prevent recording on sensitive pages (e.g., `/settings/billing`, `/admin/users`).

### Opt-Out Users Programmatically

<!-- UNVERIFIED: hj('optOut') is not documented in current Hotjar API reference pages. Hotjar's documented opt-out mechanism is the user-facing opt-out page (https://www.hotjar.com/policies/do-not-track/) and browser Do Not Track settings. The method below may still work but is not confirmed in current docs. -->

```javascript
// Disable all Hotjar tracking for this user
hj('optOut');

// Check opt-out status (stored in cookie)
// Users can also opt out via Hotjar's opt-out page or Do Not Track browser settings
```

### GDPR / Consent

Hotjar provides a consent-aware mode. Do not load the Hotjar script until the user has consented to analytics/tracking cookies:

```javascript
// Only initialize Hotjar after user consent
if (userHasConsentedToAnalytics()) {
  initHotjar(YOUR_SITE_ID);
}
```

## What Hotjar Is NOT

Hotjar provides **qualitative** behavioral data — session recordings, heatmaps, and user surveys. It supplements product analytics but does not replace them.

**Hotjar does NOT provide:**
- Event funnels or conversion analysis (use Amplitude, Mixpanel, PostHog)
- User journey mapping across sessions (use product analytics)
- Account-level / B2B group analytics (use Accoil, Amplitude, Mixpanel)
- Persistent user profiles with traits (identify tags sessions, not profiles)
- Custom event properties (events are name-only triggers)
- Server-side tracking (browser-only)
- Quantitative product metrics (DAU, retention, feature adoption rates)

**Use Hotjar alongside product analytics** to answer "why" questions that quantitative data surfaces. Example: if funnel analysis shows a 40% drop-off at step 3, watch Hotjar recordings of that step to understand what users are struggling with.

## Forge Compatibility

**Approved domains:**
- `*.hotjar.io`
- `*.hotjar.com`

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.hotjar.com"
          category: analytics
          inScopeEUD: false
        - address: "*.hotjar.io"
          category: analytics
          inScopeEUD: false
```

**IMPORTANT: Session recording tools have significant privacy implications in Forge's sandboxed environment.** Forge Custom UI runs in a sandboxed iframe. Hotjar's recording script would need to run inside this iframe to capture the app's UI. Consider carefully:

1. Session recordings may capture Atlassian user interface elements and data
2. Recordings could inadvertently capture in-scope End User Data (issue titles, page content, user-generated text)
3. The `inScopeEUD: false` declaration requires that no in-scope EUD reaches the analytics provider — this is difficult to guarantee with session recording

**Recommendation for Forge apps:** Use Hotjar for surveys and feedback collection rather than session recording. If session recording is required, apply aggressive suppression (`data-hj-suppress`) to all elements that render Atlassian content, and use URL-based exclusion rules for sensitive pages.

## Common Pitfalls

1. **Recording captures sensitive data by default** -- Hotjar records the visual state of the page including all visible text. Without explicit suppression via `data-hj-suppress`, PII and sensitive business data will appear in recordings. Audit every page for sensitive content before enabling recording.

2. **Identify does not persist across page loads** -- Unlike product analytics SDKs, Hotjar's `identify()` tags the current session. In SPAs this is usually fine, but in multi-page apps you must call `identify()` on every page load to maintain the association.

3. **Events are triggers, not analytics data** -- Hotjar events trigger recordings or surveys. They do not accumulate as countable analytics events with properties. Do not use Hotjar events as a substitute for product analytics `track()` calls.

4. **SPA navigation is not detected automatically** -- Hotjar may not detect client-side route changes. Use `hj('stateChange', '/new/path')` to notify Hotjar of virtual page views in single-page applications.

5. **Sampling and recording limits** -- Hotjar plans have session recording quotas. Not all sessions are recorded. Do not rely on Hotjar for quantitative "every session" data — it is a sampling-based qualitative tool.

6. **Attribute value types on identify** -- Passing arrays or nested objects to `identify()` attributes silently fails. Only strings, numbers, and booleans are supported.

## Debugging

### Verify Hotjar Is Active

Open browser DevTools and check:

```javascript
// Console check
typeof hj === 'function'  // Should return true

// Check if Hotjar is initialized
window._hjSettings  // Should show { hjid: YOUR_SITE_ID, hjsv: 6 }
```

### Visual Indicator

When Hotjar is actively recording, a small red notification dot appears in the bottom-right corner of the page (visible only to the site owner when logged into Hotjar, or in debug mode).

### Network Tab

In DevTools Network tab, look for requests to:
- `static.hotjar.com` — script loading
- `*.hotjar.io` — data transmission (recordings, events, survey responses)

### Hotjar Dashboard Verification

1. **Recordings:** Go to Recordings in the Hotjar dashboard. New recordings appear within minutes.
2. **Events:** Use the event filter in Recordings to verify events are firing.
3. **Identify:** Filter recordings by User ID to verify identity tagging.

### @hotjar/browser Debug

```typescript
import Hotjar from '@hotjar/browser';

// Check initialization state
console.log('Hotjar ready:', Hotjar.isReady());
```

## Further Documentation

This reference covers the essentials for session recording and behavior tracking implementation. For advanced topics, consult Hotjar's official documentation:

- **Tracking Code Installation:** https://help.hotjar.com/hc/en-us/articles/36819972345105-How-to-Install-Your-Hotjar-Tracking-Code
- **User Attributes (Identify API):** https://help.hotjar.com/hc/en-us/articles/36820019873169-How-to-Set-Up-User-Attributes
- **Identify API Reference:** https://help.hotjar.com/hc/en-us/articles/36820006120721-Identify-API-Reference
- **Events API Reference:** https://help.hotjar.com/hc/en-us/articles/36819965075473-Events-API-Reference
- **Suppress Sensitive Content:** https://help.hotjar.com/hc/en-us/articles/36819956605329-How-to-Suppress-Text-Images-Videos-and-User-Input-from-Collected-Data
- **Privacy and Data Safety:** https://help.hotjar.com/hc/en-us/articles/36819972898193-Data-Safety-Privacy-Security
- **Privacy FAQs (GDPR):** https://help.hotjar.com/hc/en-us/articles/36820004397713-Privacy-FAQs
- **@hotjar/browser npm Package:** https://www.npmjs.com/package/@hotjar/browser
