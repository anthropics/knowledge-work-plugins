<!-- Last verified: 2026-03-10 against Google Tag Manager docs -->
# Google Tag Manager Implementation Reference

## Overview

Google Tag Manager (GTM) is a tag management system that loads and configures other analytics tools. It is not an analytics destination itself — it is a routing layer that sits between your application and one or more analytics providers. GTM uses a DataLayer to receive events from your application code and then fires configured tags (GA4, Amplitude, Mixpanel, etc.) based on trigger rules.

**Category:** Tag Management
**B2B Fit:** None — GTM does not store, analyze, or group data. It routes events to tools that do.
**Forge-approved domain:** `*.googletagmanager.com`

## When GTM Makes Sense vs Direct SDK Integration

**Use GTM when:**
- Marketing teams need to add, remove, or reconfigure analytics tags without code deployments
- Multiple non-engineering stakeholders manage tag configurations
- You need to rapidly test new analytics destinations without engineering effort
- Your site runs many third-party marketing/advertising tags that change frequently

**Use direct SDK integration when:**
- Engineering owns the analytics implementation end-to-end
- You need precise control over event timing, batching, and error handling
- You want type-safe, compile-time validated tracking calls
- You are building a B2B SaaS product where identify/group/track ordering matters
- You are on a platform like Forge where external script loading is restricted

**Key trade-off:** GTM adds a layer of indirection. Events go from your code into the DataLayer, then GTM evaluates trigger rules and fires tags. This indirection makes debugging harder and introduces subtle timing issues. For engineering-led product analytics, direct SDK integration is simpler and more predictable.

## How GTM Works

```
Your Application Code
  │
  │  window.dataLayer.push({ event: 'report_created', ... })
  ▼
DataLayer (in-page JavaScript array)
  │
  │  GTM evaluates trigger rules
  ▼
GTM Container (loaded from googletagmanager.com)
  │
  │  Fires matching tags
  ▼
Analytics Destinations (GA4, Amplitude, Mixpanel, etc.)
```

1. Your code pushes structured objects into `window.dataLayer`
2. GTM's container script monitors the DataLayer for changes
3. When a push matches a configured trigger (e.g., `event` equals `report_created`), GTM fires the associated tag(s)
4. Tags execute destination-specific code (e.g., `gtag('event', ...)` for GA4, `amplitude.track(...)` for Amplitude)

## Installation

### Browser (Container Snippet)

Add the GTM container snippet to every page. Replace `GTM-XXXXXXX` with your container ID (found in GTM > Admin > Container Settings).

Place this as high in the `<head>` as possible:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

Place this immediately after the opening `<body>` tag:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

### npm / SPA Integration

There is no official GTM npm package. For SPAs, initialize the DataLayer before the GTM snippet loads:

```javascript
// Initialize DataLayer before GTM loads
window.dataLayer = window.dataLayer || [];
```

For React/Vue/Angular SPAs, community packages exist (e.g., `react-gtm-module`) but the core mechanism is the same: push objects to `window.dataLayer`.

## The DataLayer

The DataLayer is a plain JavaScript array (`window.dataLayer`) that acts as the communication channel between your application and GTM. GTM monitors this array and reacts to pushes.

### Basic Push

```javascript
window.dataLayer = window.dataLayer || [];

window.dataLayer.push({
  event: 'report_created',
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});
```

### Structure of a DataLayer Push

Every push is a plain object. The `event` key is special — it triggers GTM's tag evaluation. Other keys become DataLayer variables available in GTM triggers and tags.

```javascript
// This push triggers GTM evaluation (has 'event' key)
window.dataLayer.push({
  event: 'report_created',
  report_id: 'rpt_789'
});

// This push updates variables but does NOT trigger evaluation (no 'event' key)
window.dataLayer.push({
  user_id: 'usr_123',
  user_role: 'admin'
});
```

### Setting User Context

Push user identity into the DataLayer so downstream tags can access it. Do this on login, before tracking events.

```javascript
window.dataLayer.push({
  event: 'user_identified',
  user_id: 'usr_123',
  user_email: 'jane@example.com',
  user_role: 'admin',
  user_plan: 'enterprise'
});
```

### Setting Account Context

Push account/group information. Downstream tags use these variables to set group context in their respective SDKs.

```javascript
window.dataLayer.push({
  event: 'account_context_set',
  account_id: 'acc_456',
  account_name: 'Acme Corp',
  account_plan: 'enterprise',
  workspace_id: 'ws_789',
  workspace_name: 'Engineering'
});
```

### Tracking Events

```javascript
// Feature usage
window.dataLayer.push({
  event: 'report_created',
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});

// Navigation (SPA route change)
window.dataLayer.push({
  event: 'virtual_page_view',
  page_title: 'Report Detail',
  page_path: '/reports/rpt_789'
});

// Form interaction
window.dataLayer.push({
  event: 'form_submitted',
  form_name: 'contact',
  form_location: 'sidebar'
});
```

### Clearing Stale Variables

DataLayer variables persist across pushes. If a previous push set `report_id: 'rpt_789'` and a subsequent event does not set `report_id`, the old value is still available. To prevent stale data, explicitly clear variables:

```javascript
window.dataLayer.push({
  event: 'report_created',
  report_id: 'rpt_789',
  report_type: 'standard'
});

// Later, a different event — clear report-specific variables
window.dataLayer.push({
  event: 'dashboard_viewed',
  report_id: undefined,
  report_type: undefined
});
```

## Core Methods Mapping

GTM is a routing layer. It does not have its own identify/group/track/page methods. Instead, you push data into the DataLayer and configure GTM tags to map that data to destination-specific SDK calls.

### identify()

GTM does not identify users itself. Push user context to the DataLayer, then configure each destination tag to read the `user_id` variable.

**Your code:**
```javascript
window.dataLayer.push({
  event: 'user_identified',
  user_id: 'usr_123',
  user_role: 'admin',
  user_plan: 'enterprise'
});
```

**GTM configuration (per destination):**
- Create a DataLayer Variable for `user_id`
- In the Google tag: set User ID to `{{DL - user_id}}`
- In the Amplitude tag: map `user_id` to Amplitude's `setUserId()`
- Each destination requires its own tag configuration

### group()

GTM has no group concept. Push account context to the DataLayer and configure destination tags to use it.

**Your code:**
```javascript
window.dataLayer.push({
  event: 'account_context_set',
  account_id: 'acc_456',
  account_name: 'Acme Corp',
  account_plan: 'enterprise'
});
```

**GTM configuration:**
- Create DataLayer Variables for `account_id`, `account_name`, `account_plan`
- In destination tags that support groups (Amplitude, Mixpanel, PostHog): configure group calls using these variables
- Destinations without group support (GA4): set as user properties or event parameters

### track()

Push events to the DataLayer. GTM fires matching tags.

**Your code:**
```javascript
window.dataLayer.push({
  event: 'report_created',
  report_id: 'rpt_789',
  report_type: 'standard'
});
```

**GTM configuration:**
- Create a Custom Event trigger matching `report_created`
- Create tags for each destination (GA4 Event tag, Amplitude Event tag, etc.)
- Map DataLayer variables to destination-specific parameters

### page()

For traditional sites, GTM auto-fires a Page View trigger on load. For SPAs, push a virtual page view event on route change.

**Your code (SPA):**
```javascript
window.dataLayer.push({
  event: 'virtual_page_view',
  page_title: document.title,
  page_path: window.location.pathname
});
```

**GTM configuration:**
- Create a Custom Event trigger matching `virtual_page_view`
- Fire GA4 page_view event tag with `page_title` and `page_path` from DataLayer

## GTM Container Configuration

### Variables

Create DataLayer Variables in GTM for every piece of data your tags need:

| Variable Name | DataLayer Key | Type |
|---|---|---|
| DL - user_id | `user_id` | Data Layer Variable |
| DL - account_id | `account_id` | Data Layer Variable |
| DL - report_id | `report_id` | Data Layer Variable |
| DL - report_type | `report_type` | Data Layer Variable |

### Triggers

Create Custom Event triggers for each DataLayer event:

| Trigger Name | Trigger Type | Event Name |
|---|---|---|
| CE - report_created | Custom Event | `report_created` |
| CE - user_identified | Custom Event | `user_identified` |
| CE - virtual_page_view | Custom Event | `virtual_page_view` |
| Page View - All Pages | Page View | (built-in) |

### Tags

Create tags for each destination + event combination:

| Tag Name | Tag Type | Trigger | Purpose |
|---|---|---|---|
| Google Tag - Config | Google tag | All Pages | Initialize Google tag with Measurement ID |
| GA4 - report_created | GA4 Event | CE - report_created | Send event to GA4 |
| Amplitude - report_created | Custom HTML | CE - report_created | Send event to Amplitude |

## Required Fields

| Element | Required Fields | Notes |
|---|---|---|
| DataLayer push (event) | `event` (string) | Without `event` key, GTM does not evaluate triggers |
| DataLayer push (data) | No required fields | Any key-value pairs; become DataLayer variables |
| GTM Container | Container ID (`GTM-XXXXXXX`) | In the snippet URL |

## Limits

| Constraint | Value |
|---|---|
| Container size limit | 200 KB (compressed) |
| Maximum tags per container | No hard limit; performance degrades with many tags |
| DataLayer push size | No hard limit; keep payloads small for performance |
| Tag firing timeout | Configurable per tag (default: no timeout) |
| GTM snippet load time | Adds 50-150ms to page load (varies by container size and network) |

## Common Pitfalls

1. **Pushing to DataLayer before GTM loads** — If your code pushes events before the GTM container script initializes, those events are queued in the array and processed when GTM loads. This works, but only if `window.dataLayer = window.dataLayer || [];` is declared before the first push. Without this initialization, pushes are lost.

2. **Stale DataLayer variables** — Variables set in previous pushes persist. If you push `{event: 'report_created', report_id: 'rpt_789'}` and then push `{event: 'dashboard_viewed'}`, the `report_id` variable still holds `'rpt_789'`. Tags triggered by `dashboard_viewed` may accidentally include stale `report_id` values. Explicitly set variables to `undefined` when they do not apply.

3. **Assuming GTM handles identify/group ordering** — GTM fires tags based on trigger rules, not call order. If your B2B product requires identify before group before track (as most product analytics tools do), you must either: (a) configure tag sequencing in GTM (Tag > Advanced Settings > Tag Sequencing), or (b) handle ordering in your application code by pushing events in the correct sequence with sufficient delays.

4. **Debugging in production** — GTM's Preview mode only works when you access the site through GTM's debug panel URL. Production users never see debug mode. Use GTM's built-in Preview (Container > Preview) and the Tag Assistant Chrome extension during development. Note: the former "Tag Assistant Legacy" and "Tag Assistant Companion" extensions have been consolidated into a single "Tag Assistant" extension.

5. **Container bloat from marketing tags** — GTM containers often accumulate tags added by marketing teams (Facebook Pixel, Google Ads, HotJar, etc.). Each tag adds JavaScript to the page, increasing load time. Audit containers regularly and remove unused tags. For product analytics, consider whether GTM's overhead is justified versus direct SDK integration.

6. **SPA page view tracking gaps** — GTM's built-in Page View trigger fires only on full page loads. For SPAs (React, Vue, Angular), you must push `virtual_page_view` events on every route change. Missing this means GTM-configured page view tags only fire on initial load.

7. **Auto-loading Google tag (April 2025+)** — Starting April 10, 2025, containers with Google Ads and Floodlight tags automatically load a Google tag first, before sending events. If a Google tag is also hard-coded on the page (or installed via a CMS plugin), duplicate tags may inflate conversion counts and slow down page performance. Audit for duplicates after this change.

8. **Consent Mode** — In 2025/2026, privacy regulations require consent-aware tag firing. GTM supports Consent Mode, which adjusts tag behavior based on user consent state. Push consent state into the dataLayer (e.g., `{event: 'consent_update', analytics_storage: 'granted'}`) and configure tags to respect consent signals. Without this, tags may fire before consent is obtained, creating compliance risk.

## Debugging

### GTM Preview Mode

1. In GTM, click **Preview** (top right of the container workspace)
2. Enter your site URL
3. Your site opens in a new tab with the GTM debug panel attached
4. The debug panel shows: which tags fired, which triggers matched, and DataLayer state at each push

### Tag Assistant (Chrome Extension)

Install the "Tag Assistant" Chrome extension (formerly "Tag Assistant Legacy" and "Tag Assistant Companion", now consolidated into a single extension). It shows GTM container loading status and tag firing in real-time. Available at https://tagassistant.google.com/.

### Console Logging

Inspect the DataLayer directly in the browser console:

```javascript
// View all DataLayer pushes
console.log(window.dataLayer);

// Monitor new pushes
const originalPush = window.dataLayer.push.bind(window.dataLayer);
window.dataLayer.push = function() {
  console.log('[DataLayer Push]', arguments[0]);
  return originalPush.apply(this, arguments);
};
```

### Common Issues

- **Tag not firing:** Check that the trigger's event name exactly matches the `event` value in the DataLayer push (case-sensitive)
- **Variables showing `undefined`:** Verify the DataLayer Variable name in GTM matches the exact key used in the push
- **Tags firing multiple times:** Check for duplicate triggers or the same event being pushed multiple times

## Forge Compatibility

GTM's primary use case (loading external scripts in the browser) is incompatible with Forge Custom UI. Forge runs frontend code in a sandboxed iframe that cannot load external scripts from `googletagmanager.com`.

**For Forge apps:** Do not use GTM. Instead, integrate directly with analytics providers via the Measurement Protocol or HTTP APIs from the Forge backend using `@forge/api` fetch. See the `forge-platform.md` reference for the complete architecture.

The Forge-approved domain `*.googletagmanager.com` exists because the gtag.js snippet is served from `googletagmanager.com`, but in practice, Forge apps should use server-side Measurement Protocol calls to `*.google-analytics.com` rather than client-side GTM.

## Further Documentation

This reference covers the essentials for understanding GTM's role in product tracking. For advanced topics, consult Google's official documentation:

- **GTM Overview:** https://developers.google.com/tag-platform/tag-manager
- **GTM Web Installation:** https://support.google.com/tagmanager/answer/14842164
- **DataLayer Reference:** https://developers.google.com/tag-platform/tag-manager/datalayer
- **About Tags:** https://support.google.com/tagmanager/answer/3281060
- **Google Tag Setup:** https://support.google.com/tagmanager/answer/12002338
- **GTM Trigger Types:** https://support.google.com/tagmanager/answer/7679316
- **GTM Variable Types:** https://support.google.com/tagmanager/answer/7683362
- **Tag Sequencing:** https://support.google.com/tagmanager/answer/6238868
- **GTM Preview and Debug:** https://support.google.com/tagmanager/answer/6107056
- **Consent Mode:** https://support.google.com/tagmanager/answer/10718549
- **Server-Side GTM:** https://developers.google.com/tag-platform/tag-manager/server-side
- **Release Notes:** https://support.google.com/tagmanager/answer/4620708
