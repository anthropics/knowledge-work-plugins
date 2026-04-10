<!-- Last verified: 2026-03-10 against Cabin docs -->
# Cabin (WithCabin) Implementation Reference

## Overview

Cabin is a privacy-focused, cookieless web analytics tool. It tracks page views, referrers, and basic visitor metrics without collecting personal data or requiring cookie consent. Cabin positions itself as a simple, lightweight, carbon-conscious alternative to Google Analytics (its script is 77x smaller than GA). Cloud-only, proprietary SaaS. Runs on 100% renewable energy.

## Integration

### Script Tag

```html
<script
  async
  defer
  src="https://scripts.withcabin.com/hello.js"
></script>
```

Cabin uses a single script tag with no site-specific token in the tag itself. Site identification is handled by the domain the script is loaded on, matched against sites configured in your Cabin dashboard. Place the script before the closing `</body>` tag. Before installation, add your domain in the [Domains settings page](https://withcabin.com/settings/domains).

### Forge Manifest

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.scripts.withcabin.com"
          category: analytics
          inScopeEUD: false
```

### SPA Support

Cabin automatically tracks client-side route changes using the History API (`pushState`/`replaceState`). SPAs built with React Router, Next.js, Vue Router, and similar frameworks should have page views tracked without additional configuration.

If the automatic History API detection does not work in your specific setup, there is no documented manual `pageview()` function to call explicitly.

## Core Methods

### Page Views

Page views are tracked automatically on initial page load and on SPA route changes. No manual API call is needed or available.

### Custom Events

Event tracking requires a **PRO account**.

Cabin supports basic custom event tracking via two methods:

#### JavaScript API

```javascript
// Track a named event
cabin.event('button clicked');
```

#### HTML Data Attributes

Add `data-cabin-event` to any HTML element. Cabin automatically converts these to click events when the element is clicked:

```html
<a href="menu.pdf" data-cabin-event="Download Menu">Download Menu</a>
```

Custom events accept only an event name string. There is no support for event properties, numeric values, or structured metadata. Cabin automatically records which page triggered each event.

**Important:** The `cabin` global object is created by the script. Ensure the script has loaded before calling `cabin.event()`. There is no documented ready callback or promise.

## Limits

| Constraint | Value |
|---|---|
| Custom event properties | Not supported |
| Event tracking | PRO account required |
| User identification | Not supported |
| Account/group grouping | Not supported |
| Server-side API | Read-only analytics API (PRO only) |
| Cookie usage | None |
| Data retention | Varies by plan |
| API rate limit | 20 requests per minute |

## B2B Limitation

> **Not a product analytics tool.** Cabin is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) — not as a replacement.

## Common Pitfalls

1. **No site token in the script tag** — Unlike most analytics tools, Cabin does not use a `data-token` or `data-site-id` attribute. Site matching is based on the domain where the script loads. If you add a new domain or subdomain, you must register it in the Cabin dashboard first, or page views will not appear.

2. **Calling `cabin.event()` before the script loads** — The `cabin` global is not available until `hello.js` finishes loading. If you call `cabin.event()` immediately on page load (before the async script completes), you will get a `ReferenceError`. Wrap calls in a check: `if (typeof cabin !== 'undefined') cabin.event('...');`

3. **Expecting event properties or user identity** — Custom events are name-only. You cannot attach properties, user IDs, or account context. Cabin tells you "button clicked happened 47 times today" but not "which users clicked" or "from which accounts."

4. **Assuming server-side event tracking exists** — Event tracking is client-side only via the browser script. Cabin does offer a read-only analytics API (`api.withcabin.com/v1/`) for retrieving aggregated data (PRO accounts only), but there is no server-side event ingestion API, Node.js SDK, or backend tracking integration.

5. **Subdomain mismatch** — If your app runs on `app.example.com` but you registered `example.com` in Cabin, page views may not be recorded. Verify the exact domain/subdomain configuration in your Cabin dashboard.

6. **Event tracking requires PRO** — Custom events (both `cabin.event()` and `data-cabin-event` attributes) require a PRO account. On free plans, event calls will not record data.

## Debugging

1. **Check script loading** — Open browser DevTools Network tab, filter for `scripts.withcabin.com`. Verify `hello.js` loads with a 200 status.
2. **Check the global object** — In the browser console, type `cabin`. If the script loaded correctly, you should see the Cabin object with available methods.
3. **Check outgoing beacons** — After page load, look for outgoing requests to Cabin's endpoint in the Network tab. A successful page view generates a tracking beacon.
4. **Dashboard verification** — Log into your Cabin dashboard at https://withcabin.com. Page views should appear within a few minutes.
5. **Custom event test** — Run `cabin.event('test-event')` in the browser console and verify it appears in the Cabin dashboard.

## Further Documentation

This reference covers the essentials for implementation. Consult:

- **Official site:** https://withcabin.com
- **Documentation:** https://docs.withcabin.com/
- **Installation:** https://docs.withcabin.com/install
- **Event Tracking:** https://docs.withcabin.com/events
- **API:** https://docs.withcabin.com/api
- **Bypass Ad-blockers:** https://docs.withcabin.com/bypass-ad-blockers
- **Campaigns & UTMs:** https://docs.withcabin.com/campaigns-and-utms
- **Public Dashboards:** https://docs.withcabin.com/public-dashboards
- **GitHub (hello.js source):** https://github.com/withcabin/hello.js

**Documentation note:** Cabin's public developer documentation is focused but covers installation, events, and the analytics API. The custom event API, SPA behavior, and domain-based site matching described here are verified against current documentation as of March 2026.
