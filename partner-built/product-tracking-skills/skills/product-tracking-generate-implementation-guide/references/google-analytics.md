<!-- Last verified: 2026-03-10 against Google Analytics docs -->
# Google Analytics (GA4) Implementation Reference

## Overview

Google Analytics 4 (GA4) is a full-stack analytics platform for tracking user behavior across web and app surfaces. It supports user identification via `user_id` (set through `gtag('config', ...)` or the Measurement Protocol), custom events with parameters, and automatic page tracking. GA4 does not have a native account/group concept, making it a partial fit for B2B SaaS products.

**Category:** Full-Stack Analytics
**B2B Fit:** Partial — user identity supported, no account-level grouping
**Forge-approved domain:** `*.google-analytics.com`

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | gtag.js (Global Site Tag) | CDN snippet in `<head>` |
| Browser (GTM) | Via Google Tag Manager container | GTM snippet in `<head>` |
| Server / HTTP API | Measurement Protocol (GA4) | No SDK — raw `fetch()` calls |

There is no official GA4 Node.js SDK. Server-side tracking uses the Measurement Protocol HTTP API directly.

## Initialization

### Browser (gtag.js)

Add the gtag.js snippet to `<head>`. Replace `G-XXXXXXXXXX` with your GA4 Measurement ID (found in GA4 Admin > Data Streams > Web).

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

For SPAs, disable automatic page views and fire them manually on route change:

```html
<script>
  gtag('config', 'G-XXXXXXXXXX', {
    send_page_view: false
  });
</script>
```

### Server-Side (Measurement Protocol)

No initialization step. Each request to the Measurement Protocol is stateless. You need:

- **Measurement ID** (`G-XXXXXXXXXX`) — from GA4 Admin > Data Streams > Web
- **API Secret** — from GA4 Admin > Data Streams > [your stream] > Measurement Protocol API secrets

```
Endpoint: https://www.google-analytics.com/mp/collect
EU Endpoint: https://region1.google-analytics.com/mp/collect
Method: POST
Query params: ?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET
Content-Type: application/json
```

Use the EU endpoint if your data should be collected in the EU (routes through European servers).

## Core Methods

GA4 uses `gtag()` as a single function with different command names. The identify/group/track/page model maps as follows.

### identify()

GA4 uses `config` with a `user_id` parameter to associate events with a known user. There is no standalone identify call — user identity is set as a configuration property.

**Browser:**
```javascript
gtag('config', 'G-XXXXXXXXXX', {
  user_id: 'usr_123'
});
```

User properties (traits) are set separately via `set`:

```javascript
gtag('set', 'user_properties', {
  role: 'admin',
  plan: 'enterprise',
  account_id: 'acc_456'
});
```

**HTTP API (Measurement Protocol):**
```javascript
await fetch(
  'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: 'server_generated_client_id',
      user_id: 'usr_123',
      user_properties: {
        role: { value: 'admin' },
        plan: { value: 'enterprise' },
        account_id: { value: 'acc_456' }
      },
      events: [{
        name: 'login',
        params: {}
      }]
    })
  }
);
```

**When to call:**
- On login or signup, once the user ID is known
- On sign-out, set `user_id` to `null` to clear the association (do not use an empty string or placeholder)
- When user properties change (call `gtag('set', 'user_properties', {...})` again)

**Important:**
- GA4 user properties are limited to 25 custom user-scoped dimensions per property. Plan your user properties carefully.
- User property names must be 24 characters or fewer; values must be 36 characters or fewer.
- `user_id` values must be 256 characters or fewer and must not contain PII (e.g., email addresses).
- Reserved user property name prefixes (`google_`, `ga_`, `firebase_`) and reserved names (`first_open_time`, `first_visit_time`, `last_deep_link_referrer`, `user_id`, `first_open_after_install`) cannot be used for custom user properties.

### group()

**GA4 does not support account-level grouping.** There is no `group()` equivalent, no account entity, and no way to natively aggregate events by account/organization.

**Workaround for B2B:** Set `account_id`, `account_name`, and `account_plan` as user properties. This allows filtering events by account in GA4 reports, but does not provide true account-level analytics (e.g., account-level funnels, retention, or engagement scores).

```javascript
gtag('set', 'user_properties', {
  account_id: 'acc_456',
  account_name: 'Acme Corp',
  account_plan: 'enterprise'
});
```

**B2B Limitation:** GA4 does not support account-level grouping. For B2B SaaS products that need account-level engagement analytics, GA4 should be supplemented with a tool that supports group() calls (Amplitude, Mixpanel, PostHog, or Accoil).

### track()

GA4 uses `event` as the command name. Events have a name and optional parameters.

**Browser:**
```javascript
gtag('event', 'report_created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});
```

**HTTP API (Measurement Protocol):**
```javascript
await fetch(
  'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: 'server_generated_client_id',
      user_id: 'usr_123',
      events: [{
        name: 'report_created',
        params: {
          report_id: 'rpt_789',
          report_type: 'standard',
          template_used: 'false'
        }
      }]
    })
  }
);
```

**Event naming rules:**
- Names must be 1-40 characters
- Must start with a letter
- Only letters, numbers, and underscores allowed
- GA4 uses `snake_case` by convention (e.g., `report_created`, not `report.created`)
- Do not use reserved prefixes: `firebase_`, `ga_`, `google_`

**Parameter rules:**
- Up to 25 custom event parameters per event
- Parameter names: up to 40 characters
- Parameter string values: up to 100 characters
- Up to 50 custom event-scoped dimensions and 50 custom metrics per GA4 property

### page()

GA4 tracks page views automatically when `gtag('config', ...)` is called (unless `send_page_view: false`). For SPAs, fire page views manually on route change.

**Browser (automatic):**
```javascript
// Fires automatically on config — no manual call needed for traditional sites
gtag('config', 'G-XXXXXXXXXX');
```

**Browser (SPA manual page view):**
```javascript
gtag('event', 'page_view', {
  page_title: 'Report Detail',
  page_location: 'https://app.example.com/reports/rpt_789'
});
```

**Note:** Only `page_title` and `page_location` are documented parameters for manual `page_view` events. `page_path` is not a standard GA4 parameter. The `page_location` value must include the protocol (e.g., `https://`). If you send manual page views without disabling automatic page view measurement, you may get duplicate page views.

**HTTP API (Measurement Protocol):**
```javascript
await fetch(
  'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: 'server_generated_client_id',
      user_id: 'usr_123',
      events: [{
        name: 'page_view',
        params: {
          page_title: 'Report Detail',
          page_location: 'https://app.example.com/reports/rpt_789'
        }
      }]
    })
  }
);
```

## Required Fields

| Method | Required Fields | Notes |
|---|---|---|
| `gtag('config', ...)` | Measurement ID (`G-XXXXXXXXXX`) | Initializes tracking |
| `gtag('event', ...)` | Event name (string) | Parameters optional but recommended |
| Measurement Protocol | `client_id`, `events[]` (with `name`) | `user_id` optional but recommended; `api_secret` + `measurement_id` in query string |

**client_id:** Required on every Measurement Protocol request (for web streams). For browser events, gtag.js manages this automatically. For server-side, generate a UUID and persist it per user/session. This is NOT the same as `user_id` — `client_id` identifies a device/session, `user_id` identifies a person.

**Recommended Measurement Protocol event parameters:** Include `session_id` and `engagement_time_msec` in event `params` for events to appear in real-time reports. Without these, events are still collected but may not surface in the Realtime view.

## Limits

| Constraint | Value |
|---|---|
| Custom event parameters per event | 25 |
| Custom user properties per GA4 property | 25 |
| Custom event-scoped dimensions per property | 50 |
| Custom metrics per property | 50 |
| Event name length | 1-40 characters |
| Parameter name length | up to 40 characters |
| Parameter string value length | up to 100 characters (500 for GA4 360) |
| User property name length | up to 24 characters |
| User property value length | up to 36 characters |
| User ID (`user_id`) length | up to 256 characters |
| Measurement Protocol events per request | 25 |
| Measurement Protocol request size | 130 KB |
| Measurement Protocol timestamp backdating | up to 72 hours via `timestamp_micros` |
| Measurement Protocol requests per day | No documented hard limit; subject to quota |
| Data freshness | Events appear in reports within 24-48 hours (real-time view available for recent events) |

## Common Pitfalls

1. **Using dot-separated event names** — GA4 requires `snake_case` event names. `report.created` is invalid; use `report_created`. This differs from Segment/Amplitude conventions where dot notation is common.

2. **Exceeding the 25 custom parameter limit** — GA4 allows only 25 custom event parameters per event and 25 custom user properties per property. Plan your schema carefully. High-cardinality data (IDs, timestamps) should not be registered as custom dimensions unless you need them in reports.

3. **Confusing client_id and user_id** — `client_id` is a device/browser identifier (managed automatically by gtag.js, required manually for Measurement Protocol). `user_id` is your application's user identifier. Both can be set. Omitting `user_id` on Measurement Protocol calls means events cannot be tied to known users.

4. **Expecting real-time data in reports** — GA4 standard reports have a 24-48 hour processing delay. Use the Realtime report or DebugView for immediate verification, but do not rely on standard reports for testing.

5. **Not registering custom dimensions** — Custom event parameters and user properties must be registered as custom dimensions in GA4 Admin (Custom Definitions) before they appear in reports. Sending data without registration means it is collected but invisible in the GA4 UI.

6. **Assuming GA4 supports B2B account analytics** — GA4 has no native group/account entity. Setting `account_id` as a user property enables basic filtering but does not provide account-level funnels, retention, or engagement analysis. Supplement with a B2B-capable tool.

## Debugging

### DebugView (GA4 Dashboard)

Enable debug mode in the browser to send events to GA4 DebugView:

```javascript
gtag('config', 'G-XXXXXXXXXX', {
  debug_mode: true
});
```

Events appear in GA4 Admin > DebugView within seconds. This is the primary tool for verifying event names, parameters, and user properties.

### Browser DevTools

Check the Network tab for requests to `www.google-analytics.com/g/collect` (gtag.js) or `www.google-analytics.com/mp/collect` (Measurement Protocol).

### Google Analytics Debugger (Chrome Extension)

Install the "Google Analytics Debugger" Chrome extension. It logs all GA4 events and parameters to the browser console.

### Measurement Protocol Validation

Use the validation endpoint to test payloads without sending data to GA4:

```javascript
// Validation endpoint — returns errors but does not record events
await fetch(
  'https://www.google-analytics.com/_debug_/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: 'test_client_id',
      user_id: 'usr_123',
      events: [{
        name: 'report_created',
        params: {
          report_id: 'rpt_789'
        }
      }]
    })
  }
);
// Response includes validationMessages array with any errors
```

### Measurement Protocol HTTP Responses

- `2xx` — Accepted (does not guarantee processing; payload may still be invalid)
- `4xx` — Malformed request (check required fields)
- Use the `/_debug_/mp/collect` endpoint for detailed validation errors
- The validation server does **not** validate `api_secret` or `measurement_id` — verify these credentials separately
- Response includes a `validationMessages` array; an empty array means the payload is valid

## Forge Compatibility

GA4 is on the Atlassian Forge approved analytics domain list. Manifest configuration:

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.google-analytics.com"
          category: analytics
          inScopeEUD: false
```

For Forge apps, use the Measurement Protocol from the backend. Do not use gtag.js in the frontend — Forge Custom UI runs in a sandboxed iframe that cannot load external scripts. Route all tracking through backend resolvers using `@forge/api` fetch.

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Google's official documentation:

- **GA4 Getting Started:** https://developers.google.com/analytics/devguides/collection/ga4
- **gtag.js Reference:** https://developers.google.com/tag-platform/gtagjs/reference
- **GA4 Event Reference:** https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- **Measurement Protocol (GA4):** https://developers.google.com/analytics/devguides/collection/protocol/ga4
- **Measurement Protocol Validation:** https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events
- **Custom Dimensions and Metrics:** https://support.google.com/analytics/answer/10075209
- **User Properties:** https://developers.google.com/analytics/devguides/collection/ga4/user-properties
- **DebugView:** https://support.google.com/analytics/answer/7201382
