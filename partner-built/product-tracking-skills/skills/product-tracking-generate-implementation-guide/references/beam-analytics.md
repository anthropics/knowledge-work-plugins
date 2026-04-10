<!-- Last verified: 2026-03-10 against Beam Analytics docs -->

# Beam Analytics Implementation Reference

> **END-OF-LIFE NOTICE:** Beam Analytics is shutting down on **September 1, 2026**. The service will continue running until that date to allow users to export data and migrate. Consider migrating to Plausible, Fathom, Umami, or Pirsch. Export your data from the Beam dashboard settings before the shutdown date.

## Overview

Beam Analytics is a privacy-focused, cookieless web analytics tool. It provides aggregate traffic metrics (page views, referrers, devices, locations) without collecting personal data or requiring cookie consent banners. GDPR, CCPA, and PECR compliant. Cloud-only, proprietary SaaS. Registered in the United Kingdom.

## Integration

### Script Tag

```html
<script
  src="https://beamanalytics.b-cdn.net/beam.min.js"
  data-token="YOUR_TOKEN"
  async
></script>
```

The `data-token` attribute is your site-specific token, found in your Beam Analytics dashboard under site settings.

#### Dynamic Script Injection (alternative)

When using Google Tag Manager or when the standard script tag is not suitable, you can inject the script dynamically:

```html
<script>
  var script = document.createElement('script');
  script.defer = true;
  script.dataset.token = "YOUR_BEAM_TOKEN";
  script.dataset.api = "https://api.beamanalytics.io/api/log";
  script.src = "https://beamanalytics.b-cdn.net/beam.min.js";
  document.getElementsByTagName('head')[0].appendChild(script);
</script>
```

The `data-api` attribute specifies the API endpoint for logging events (`https://api.beamanalytics.io/api/log`). When using the standard script tag, this endpoint is used implicitly.

### Forge Manifest

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.beamanalytics.b-cdn.net"
          category: analytics
          inScopeEUD: false
        - address: "api.beamanalytics.io"
          category: analytics
          inScopeEUD: false
```

### SPA Support

Beam Analytics does not natively detect client-side route changes in single-page applications. It tracks the initial page load only. For SPAs built with React Router, Next.js, or similar, page views after the initial load will not be recorded automatically.

However, you can use the custom events API (`window.beam()`) as a workaround to track client-side navigation. Beam's documentation provides a hash-change listener pattern:

```javascript
function onHashChange() {
  const hash = window.location.hash;
  window.beam(`/custom-events/hashchange/${hash}`);
}
window.addEventListener('hashchange', onHashChange, false);
```

This approach logs route changes as custom events (not true page views), so they appear in custom event reports and can be included in conversion funnels. For full native SPA page-view tracking, consider Plausible or Fathom instead.

## Core Methods

### Page Views

Page views are tracked automatically on script load. There is no manual `pageview()` function exposed.

### Custom Events

Beam Analytics supports custom events via a global function. Events are modeled as path-style strings and treated internally as dedicated page views:

```javascript
// Track a named event (no properties supported)
window.beam('/custom-event-name');
```

Custom events in Beam are limited to an event name string in URL-path format. There is no support for event properties, numeric values, or structured metadata.

**Best practice:** Use a consistent prefix (e.g., `/custom-events/`) to separate custom events from actual page views in your analytics reports.

#### Custom Event Examples

```javascript
// Time-on-page milestone (user stayed 5 seconds on homepage)
setTimeout(() => {
  window.beam("/custom-events/homepage_5_seconds");
}, 5000);

// Button click tracking
document.getElementById('signup-btn').addEventListener('click', () => {
  window.beam("/custom-events/signup-click");
});

// Hash-change tracking for SPA-like navigation
window.addEventListener('hashchange', () => {
  window.beam(`/custom-events/hashchange/${window.location.hash}`);
}, false);
```

### Conversion Funnels

Custom events can be used as steps in Beam's conversion funnel builder. Funnels support transitions from page views to custom events (and vice versa). There are no limits on how many conversion funnels you can build on a paid account.

## Limits

| Constraint | Value |
|---|---|
| Custom event properties | Not supported |
| User identification | Not supported |
| Account/group grouping | Not supported |
| SPA auto-detection | Not supported (workaround via custom events) |
| Data retention | Varies by plan |
| Event name format | URL-path style (e.g., `/signup-click`) |
| Free tier page views | Up to 100,000 per month |
| Conversion funnels | Unlimited (paid plans) |

## B2B Limitation

> **Not a product analytics tool.** Beam Analytics is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) — not as a replacement.

## Common Pitfalls

1. **Assuming SPA page views are tracked** — Beam only fires on full page loads. Client-side navigation in React, Vue, Angular, or Next.js apps will not trigger additional page views. You can use `window.beam()` to log custom events on route changes as a workaround, but these are tracked as custom events, not page views.

2. **Expecting event properties or metadata** — Custom events accept only a name string. You cannot attach properties like `report_type: 'standard'` or `plan: 'pro'`. If you need event properties, use a product analytics tool.

3. **Using Beam as a product analytics replacement** — Beam provides aggregate traffic data (total page views, top pages, referrer breakdown). It cannot answer questions like "how many users completed onboarding" or "which accounts used feature X this week." It is a complement to product analytics, not a substitute.

4. **Ad-blocker interference** — The `beamanalytics.b-cdn.net` CDN domain may be blocked by some ad blockers and privacy extensions (notably Firefox, Brave, and Safari may block if loaded via GTM). There is no documented self-hosted or proxy option to mitigate this. Direct script embedding (not via GTM) may improve reach.

5. **Confusing the token with an API key** — The `data-token` in the script tag is a site identifier, not a secret. It is safe to include in client-side code. However, there is no server-side API for sending events programmatically.

6. **Not planning for shutdown** — Beam Analytics shuts down on September 1, 2026. Any new integration should account for migration to an alternative analytics provider before that date.

## Debugging

1. **Check script loading** — Open browser DevTools, go to the Network tab, and filter for `beam.min.js`. Confirm it loads with a 200 status.
2. **Check beacon requests** — After the script loads, look for outgoing requests to `api.beamanalytics.io` in the Network tab. A successful page view will generate a request shortly after page load.
3. **Dashboard verification** — Log into your Beam Analytics dashboard and check the real-time or recent activity view. Page views should appear within a few minutes.
4. **Ad-blocker check** — If no requests appear, disable ad blockers and privacy extensions temporarily to rule out script blocking.
5. **GTM interference** — If using Google Tag Manager, note that GTM itself is blocked by Firefox, Brave, Safari, and many browser extensions. Consider direct script embedding for better coverage.

## Further Documentation

This reference covers the essentials for implementation. Beam Analytics has limited public documentation. Consult:

- **Official site:** https://beamanalytics.io
- **Custom Events:** https://beamanalytics.io/blog/custom-events-on-beam
- **Conversion Funnels:** https://beamanalytics.io/blog/conversion_funnels_with_beam
- **GTM Integration:** https://beamanalytics.io/blog/beam-and-google-tag-manager
- **FAQs:** https://beamanalytics.io/blog/faqs

**End-of-life note:** Beam Analytics shuts down September 1, 2026. This reference remains useful for existing integrations that need maintenance before migration, but new projects should consider alternatives such as Plausible, Fathom, Umami, or Pirsch.
