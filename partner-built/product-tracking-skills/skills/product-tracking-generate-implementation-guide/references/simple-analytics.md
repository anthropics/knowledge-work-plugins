<!-- Last verified: 2026-03-10 against Simple Analytics docs -->

# Simple Analytics Implementation Reference

## Overview

Simple Analytics is a privacy-focused, cookieless web analytics tool. It is GDPR, CCPA, and PECR compliant by default with no consent banners or cookie notices required. Simple Analytics is cloud-only and does not store any personal data -- not even anonymized IPs. The script is lightweight (~6 KB) and collects the minimum data needed for web traffic analysis.

## Integration

### Script Tag

```html
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="" referrerpolicy="no-referrer-when-downgrade" /></noscript>
```

The `<noscript>` tag provides a pixel-based fallback for visitors with JavaScript disabled. Unlike Plausible and Fathom, Simple Analytics does not require a site ID in the script tag -- it uses the page's hostname to identify the site.

**Development version:** Use `https://scripts.simpleanalyticscdn.com/latest.dev.js` for localhost testing to avoid sending data to production.

**Forge-approved domain:** `*.scripts.simpleanalyticscdn.com`

### Script Attributes

| Attribute | Value | Purpose |
|---|---|---|
| `data-hostname` | Domain string | Override auto-detected hostname (useful for localhost testing). |
| `data-collect-dnt` | `true` | Track visitors who have Do Not Track enabled. Default: does not track DNT users. Legacy attribute `data-skip-dnt` still works but is deprecated. |
| `data-mode` | `hash` | Enable hash-based routing for SPAs. |
| `data-ignore-pages` | Comma-separated paths | Exclude specific pages from tracking (e.g., `/admin,/dashboard`). Supports wildcards: `/search/*` matches all subpaths. |
| `data-auto-collect` | `true` or `false` | Enable or disable automatic page view collection. Default: `true`. When `false`, exposes `sa_pageview` for manual tracking. |
| `data-namespace` | Custom prefix string | Change the global function prefix from `sa` to a custom name. Changes all functions: `sa_event`, `sa_pageview`, `sa_metadata`, `sa_loaded`, etc. Example: `data-namespace="ba"` creates `ba_event`, `ba_pageview`, etc. |
| `data-metadata-collector` | Function name string | Name of a callback function that returns metadata for each page view or event. |

### SPA Support

**Hash-based routing:**

```html
<script async src="https://scripts.simpleanalyticscdn.com/latest.js" data-mode="hash"></script>
```

**History API routing (pushState):** Simple Analytics automatically detects `pushState` and `replaceState` calls by overwriting the native `pushState` function in the browser. For most SPAs (React Router, Vue Router, Next.js), page views are tracked automatically without additional configuration.

**Manual page view tracking:**

```javascript
// Trigger a page view manually (defaults to window.location.pathname if no path given)
sa_pageview('/custom/path');
```

This is useful when automatic detection is disabled via `data-auto-collect="false"` or does not cover all navigation patterns. Always check the function exists before calling:

```javascript
if (window.sa_pageview) {
  sa_pageview(window.location.pathname);
}
```

## Core Methods

### Page Views

Page views are tracked automatically on page load and on SPA route changes (via History API detection). The following is auto-collected:

- Page URL (protocol, hostname, pathname -- query parameters and fragments excluded by default)
- Referrer (referring domain, same URL structure)
- UTM parameters (source, medium, campaign, content -- note: `utm_term` is deprecated and not collected)
- Browser and OS (version numbers truncated for privacy)
- Screen dimensions (viewport and screen width/height)
- Country (derived from device timezone, not IP)
- Language (browser language)
- Time on page (excludes time when browser tab is hidden)
- Scroll depth (recorded in 5% increments)
- Session ID (connects pages and events within one session)
- Page ID (connects events on the same page)
- Bot detection (bots are filtered out via user agent analysis)

**Not auto-collected:** user identity, click tracking, form interactions, IP address (never collected or stored), detailed query parameters or fragments.

### Custom Events

Simple Analytics supports custom events through the `sa_event` global function.

```javascript
// Basic custom event
sa_event('signup');

// Custom event with metadata
sa_event('download', { filename: 'report.pdf', format: 'pdf' });
```

**Important:** The function is `sa_event`, not `sa.event` or `simpleanalytics.event`.

**Custom event behavior:**

- Event names may only contain alphanumeric characters and underscores
- Event names are converted to lowercase; spaces are replaced with underscores
- Event name maximum length: 200 characters (longer names are truncated)
- Events appear in the Events Explorer in the Simple Analytics dashboard
- Metadata is supported as key-value pairs (see Metadata section below)
- Events do not need to be pre-registered in the dashboard -- they appear automatically
- Events can use dynamic names via a function: `sa_event(function() { return "clicked_on_" + location.pathname; })`

**Event queue for early loading:**

If events fire before the script loads, add this placeholder in the `<head>`:

```html
<script>window.sa_event=window.sa_event||function(){var a=[].slice.call(arguments);window.sa_event.q?window.sa_event.q.push(a):window.sa_event.q=[a]};</script>
```

This queues events and replays them once the main script loads.

### Metadata

Metadata can be attached to both events and page views. Simple Analytics supports four data types:

| Type | Notes |
|---|---|
| Text | Maximum 1,000 characters (truncated if exceeded) |
| Boolean | `true` or `false` |
| Number | Must be finite; range approximately -2x10^36 to 2x10^36 |
| Date | Use `new Date()` constructor; stored as ISO 8601 format |

**Restrictions:** No nested objects, arrays, or functions. No falsy values except booleans. Non-alphanumeric characters in keys are replaced with underscores; leading/trailing underscores are trimmed. Do not include personal data (email addresses, identifiers) -- accounts may be suspended.

**Three ways to send metadata:**

1. **Event function parameter** (most common):
```javascript
sa_event('click_download', { filename: 'document.pdf' });
```

2. **Window object assignment** (applies to subsequent page views):
```javascript
sa_metadata = { theme_color: 'green' };
```

3. **Metadata collector callback** (via script attribute):
```html
<script data-metadata-collector="myAddMetadataFunction">
  function myAddMetadataFunction(data) {
    if (data.type === 'pageview') return { page_id: 123 };
    if (data.type === 'event') return { event_id: 124 };
    return {};
  }
</script>
```

When multiple methods are used, values merge with later values overwriting earlier ones.

### Auto Events Script

The `auto-events.js` script adds automatic tracking of outbound link clicks, email link clicks, and file download clicks:

```html
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<script async
  data-collect="outbound,emails,downloads"
  data-extensions="pdf,csv,docx,xlsx,zip,doc,xls"
  data-use-title="true"
  data-full-urls="false"
  src="https://scripts.simpleanalyticscdn.com/auto-events.js"></script>
```

| Attribute | Default | Purpose |
|---|---|---|
| `data-collect` | `outbound,emails,downloads` | Types of interactions to auto-track. |
| `data-extensions` | `pdf,csv,docx,xlsx,zip,doc,xls` | File extensions to track as downloads. |
| `data-use-title` | `true` | Include link title text in event names. |
| `data-full-urls` | `false` | Track complete URLs vs. shortened versions. |

```html
<!-- Auto-tracked by auto-events.js -->
<a href="https://external.com">External Link</a>
<a href="mailto:hello@example.com">Email</a>
<a href="/files/report.pdf" download>Download</a>
```

### Inline Events Script

The `inline-events.js` script provides HTML-attribute-based event tracking without custom JavaScript:

```html
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<script async src="https://scripts.simpleanalyticscdn.com/inline-events.js"></script>
```

**Button/link clicks:**
```html
<a href="/pricing" data-simple-event="visit_pricing_page">See pricing</a>
```

**Form submissions:**
```html
<form action="/signup" data-simple-event="signup_form">
  <input name="email" type="email" />
  <button type="submit">Sign up</button>
</form>
```

**Metadata via HTML attributes** (prefix with `data-simple-event-`, dashes become underscores):
```html
<button
  data-simple-event="select_plan"
  data-simple-event-plan="enterprise"
  data-simple-event-referrer="homepage">
  Choose Enterprise
</button>
```

The inline events script also auto-detects 404 errors, sending a `page_404` event with URL and status. Note: this feature is in beta.

### Programmatic Event Tracking

```javascript
// Check if Simple Analytics is loaded
if (typeof sa_event === 'function') {
  sa_event('form_submitted', { form_name: 'contact', source: 'footer' });
}

// Use a callback for navigation after event fires
sa_event('outbound_link_to_affiliate', function() {
  window.location.href = 'https://example.com/?affiliate=123';
});
```

### Server-Side Event Tracking

Events can be submitted from server-side or mobile applications via a JSON POST:

**Endpoint:** `https://queue.simpleanalyticscdn.com/events`

This supports both event and page view submissions with metadata. See the server-side documentation for payload format.

## Limits

| Constraint | Value |
|---|---|
| Event name length | Maximum 200 characters (truncated beyond) |
| Event name characters | Alphanumeric and underscores only (auto-sanitized) |
| Metadata value length (text) | Maximum 1,000 characters |
| Metadata data types | Text, Boolean, Number, Date (no objects, arrays, or functions) |
| API rate limit | Reasonable use; no published per-second limit |
| Data retention | Unlimited on paid plans |
| Sites per account | Varies by plan |

## B2B Limitation

> **Not a product analytics tool.** Simple Analytics is a privacy-focused web analytics tool. It does not support user identification, account grouping, or rich event properties beyond simple metadata. It tracks aggregate page views and (optionally) custom events with metadata. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) -- not as a replacement.

## Common Pitfalls

1. **Using the wrong function name** -- The global function is `sa_event`, not `sa.event`, `simpleAnalytics.event`, or `sa.track`. Using the wrong name throws a `ReferenceError`. If you changed the prefix via `data-namespace`, use that prefix instead (e.g., `ba_event`).

2. **DNT visitors not tracked by default** -- Unlike most analytics tools, Simple Analytics respects Do Not Track headers by default. This can cause undercounting. If you want to track all visitors, add `data-collect-dnt="true"` to the script tag. Note: Apple discontinued DNT support, and the W3C disbanded its DNT working group in 2018, so the practical impact has diminished.

3. **No site ID in the script tag** -- Simple Analytics identifies your site by the page hostname. If you test on `localhost` or a staging domain, data goes to the wrong site (or nowhere). Use `data-hostname="yourdomain.com"` to override when testing locally. Alternatively, use the dev script: `latest.dev.js`.

4. **Expecting user-level analytics** -- Simple Analytics provides aggregate metrics with session-level grouping. You cannot filter events by user, see individual user journeys, or identify users. If you need user-level data, use a product analytics tool.

5. **Hash routing not enabled** -- For apps using hash-based routing (e.g., `/#/page`), you must add `data-mode="hash"` to the script tag. Without it, all hash route changes are invisible.

6. **Event names are auto-sanitized** -- Event names are lowercased, spaces are replaced with underscores, and only alphanumeric characters and underscores are kept. `Signup Form` becomes `signup_form`. Names over 200 characters are truncated. Plan for this in your dashboard and any automations that reference event names.

7. **Metadata type mismatches** -- Metadata values must be Text (string), Boolean, Number, or Date. Passing objects, arrays, or functions as metadata values will fail silently. Ensure all values are primitive types.

8. **Events firing before script loads** -- If custom events fire before `latest.js` loads, they are lost. Use the event queue placeholder script in `<head>` to buffer events until the main script is ready.

## Debugging

**Check script loaded:** Open browser DevTools > Network tab. Filter for `simpleanalyticscdn`. You should see a request to `scripts.simpleanalyticscdn.com/latest.js` (status 200).

**Verify page views firing:** In the Network tab, look for requests to `queue.simpleanalyticscdn.com`. Each page view sends a request to this endpoint.

**Test events in console:**

```javascript
// Verify the function exists
console.log(typeof sa_event);  // should be 'function'

// Check if script is loaded
console.log(window.sa_loaded);  // should be true

// Fire a test event
sa_event('test_event', { test: 'true' });
```

**Dashboard verification:** Page views appear in the Simple Analytics dashboard within minutes. Check the main dashboard for page views and the Events Explorer for custom events.

**Localhost testing:** To test locally, add the hostname override:

```html
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"
  data-hostname="yourdomain.com"></script>
```

This routes local development data to your production site in Simple Analytics. Remove the override before deploying to production.

**Bypass ad blockers during development:** If the script is blocked, check if a browser extension is interfering. Simple Analytics has generally low ad-blocker interference compared to Google Analytics, but some privacy-focused blockers may still block it.

## Further Documentation

This reference covers the essentials for implementation. For advanced topics, consult Simple Analytics' official documentation:

- **Script Installation:** https://docs.simpleanalytics.com/script
- **Overwrite Domain Name:** https://docs.simpleanalytics.com/overwrite-domain-name
- **Custom Events:** https://docs.simpleanalytics.com/events
- **Inline Events:** https://docs.simpleanalytics.com/events/inline
- **Server-Side Events:** https://docs.simpleanalytics.com/events/server-side
- **Event Metadata:** https://docs.simpleanalytics.com/metadata
- **SPA / Hash Mode:** https://docs.simpleanalytics.com/hash-mode
- **Trigger Custom Page Views:** https://docs.simpleanalytics.com/trigger-custom-page-views
- **Auto Events (Links, Downloads):** https://docs.simpleanalytics.com/automated-events
- **Do Not Track:** https://docs.simpleanalytics.com/dnt
- **Ignore Pages:** https://docs.simpleanalytics.com/ignore-pages
- **What We Collect:** https://docs.simpleanalytics.com/what-we-collect
- **API Reference:** https://docs.simpleanalytics.com/api
- **Framework Guides (React):** https://docs.simpleanalytics.com/install-simple-analytics-with-react
