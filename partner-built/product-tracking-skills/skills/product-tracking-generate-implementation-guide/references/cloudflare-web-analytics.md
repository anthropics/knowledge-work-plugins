<!-- Last verified: 2026-03-10 against Cloudflare Web Analytics docs -->

# Cloudflare Web Analytics Implementation Reference

## Overview

Cloudflare Web Analytics is a free, privacy-focused web analytics tool provided by Cloudflare. It is cookieless, does not track individual users, and is GDPR-compliant by default. It can be used in two modes: automatically via Cloudflare's DNS/CDN proxy (zero-config for sites already on Cloudflare), or standalone via a JavaScript beacon for sites not using Cloudflare's network. Proprietary, free tier with no paid plans.

## Integration

### Mode 1: Cloudflare-Proxied Sites (Automatic)

If your site already uses Cloudflare as its DNS/CDN provider (orange-cloud enabled), Web Analytics can be activated directly from the Cloudflare dashboard with no code changes. Cloudflare injects the beacon script automatically into HTML responses served through its edge network.

**Setup:**
1. Log into the Cloudflare dashboard
2. Navigate to **Web Analytics**
3. Select **Add a site** and choose your hostname from the dropdown
4. Automatic setup is enabled by default

No script tag is needed. Cloudflare injects the beacon at the edge.

> **Note:** Automatic injection will fail if your site sets a `Cache-Control` header with `public, no-transform`, because Cloudflare's proxy cannot modify the original response payload. In that case, use the standalone beacon (Mode 2).

**For Cloudflare Pages:** Go to **Workers & Pages**, select your project, navigate to **Metrics**, and select **Enable** under Web Analytics. Cloudflare will automatically add the JavaScript snippet on the next deployment.

### Mode 2: JavaScript Beacon (Standalone)

For sites not proxied through Cloudflare, or when you need explicit control, add the beacon script manually:

```html
<script
  defer
  src="https://static.cloudflareinsights.com/beacon.min.js"
  data-cf-beacon='{"token": "YOUR_SITE_TOKEN"}'
></script>
```

The `token` is a site-specific identifier found in your Cloudflare dashboard under **Web Analytics > Manage site**. It is not a secret — it is safe to include in client-side code. Place the snippet before the closing `</body>` tag.

### Forge Manifest

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "static.cloudflareinsights.com"
          category: analytics
          inScopeEUD: false
```

### SPA Support

Cloudflare Web Analytics automatically tracks SPA route changes. The beacon detects History API calls (`pushState`, `replaceState`) and records page views for each client-side navigation. This works with React Router, Next.js, Vue Router, and similar frameworks.

For the automatic Cloudflare-proxied mode, SPA support is also handled by the injected beacon.

## Core Methods

### Page Views

Page views are tracked automatically on page load and on SPA route changes. There is no manual `pageview()` API.

The beacon collects:
- Page URL and path
- Referrer
- Browser and device type
- Country (from IP, not stored)
- Performance metrics (Core Web Vitals: LCP, INP, CLS)
- Additional performance metrics: TTFB, FCP, First Paint
- Resource metrics: `transferSize`, `decodedBodySize`
- Navigation metadata: `deliveryType`, `navigationType`
- Server-Timing headers
- `navigator.webdriver` (bot detection)

> **Note:** INP (Interaction to Next Paint) replaced FID (First Input Delay) as a Core Web Vital in March 2024. Cloudflare's beacon already collects INP.

### Custom Events

**Cloudflare Web Analytics does not support custom events.** There is no `track()`, `event()`, or equivalent API. It is a page-view-only analytics tool with performance metrics. The FAQ states: "Not yet, but we may add support for this in the future."

If you need custom event tracking, use a separate product analytics tool. (Cloudflare's separate product, Zaraz, does support custom event tracking via `zaraz.track()`, but that is a different tool.)

## Limits

| Constraint | Value |
|---|---|
| Custom events | Not supported |
| Custom event properties | Not supported |
| User identification | Not supported |
| Account/group grouping | Not supported |
| Server-side API | Not available (but GraphQL Analytics API can query RUM data — see below) |
| Cookie usage | None |
| Cost | Free |
| Data retention | 6 months |
| Sites per account | 10 (soft limit, adjustable via support) |
| Sampling | May apply on high-traffic sites (Adaptive Bit Rate) |

## Cloudflare-Specific Setup Notes

Cloudflare Web Analytics is tightly coupled with the Cloudflare platform. Key differences from standalone analytics tools:

1. **Two integration modes** — Automatic (for Cloudflare-proxied sites) requires zero code. Standalone (JavaScript beacon) works on any site but requires the script tag. These are the same product with different deployment methods.

2. **DNS/CDN dependency for automatic mode** — The zero-config automatic injection only works if your site's traffic flows through Cloudflare's edge network (DNS proxy enabled, orange cloud icon). If your site uses Cloudflare for DNS-only (grey cloud), you must use the standalone beacon.

3. **Performance metrics built in** — Unlike most privacy-focused analytics tools, Cloudflare Web Analytics collects Core Web Vitals (Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout Shift) automatically, plus supplementary metrics (TTFB, FCP, First Paint). This data appears in the dashboard alongside page view metrics.

4. **No separate account needed for proxied sites** — If you already have a Cloudflare account managing your domain, Web Analytics is available at no additional cost and no separate signup.

5. **Beacon domain is fixed** — The standalone beacon always loads from `static.cloudflareinsights.com`. There is no option to self-host the script or use a custom domain for the beacon.

6. **GraphQL Analytics API access** — Although there is no dedicated Web Analytics REST API, Cloudflare's GraphQL Analytics API exposes RUM datasets (`rumPageloadEventsAdaptiveGroups`, `rumPerformanceEventsAdaptiveGroups`) at the account level. You can query page view and performance data programmatically. Requires an API token with "Account Analytics: Read" permission. Data can be exported to CSV. Endpoint: `https://api.cloudflare.com/client/v4/graphql`.

7. **Cache-Control caveat** — Automatic beacon injection (Mode 1) fails if your origin sets `Cache-Control: public, no-transform`, because Cloudflare's proxy is unable to modify the response. Use the standalone beacon in that case.

## B2B Limitation

> **Not a product analytics tool.** Cloudflare Web Analytics is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties. It does not support custom events of any kind. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) — not as a replacement.

## Common Pitfalls

1. **Expecting custom event support** — Cloudflare Web Analytics has no event tracking API whatsoever. Unlike Plausible, Fathom, or even Cabin, there is no way to track custom events. It is strictly a page view and performance metrics tool. If your tracking plan includes any custom events, you need a second analytics tool.

2. **Confusing automatic and standalone modes** — If your site is proxied through Cloudflare AND you also add the beacon script manually, you may get duplicate page view counts. Use one mode or the other, not both.

3. **Grey-cloud DNS expecting automatic injection** — Automatic beacon injection only works when the Cloudflare proxy is active (orange cloud in DNS settings). DNS-only mode (grey cloud) does not inject the beacon. You must add the script tag manually.

4. **Assuming real-time data** — Cloudflare Web Analytics data can be delayed. Page views may take several minutes to appear in the dashboard. Do not assume the dashboard is real-time when debugging.

5. **Data sampling on high-traffic sites** — Cloudflare uses Adaptive Bit Rate (ABR) sampling on high-traffic sites. The dashboard numbers may be estimates rather than exact counts. This is generally not an issue for low-to-medium traffic sites.

6. **Ad blockers block the beacon** — Ad blockers (e.g., Adblock Plus, uBlock Origin, Brave browser) block the `beacon.min.js` script from `static.cloudflareinsights.com`. This means some visitors will not be counted. Edge analytics (available on Pro, Business, and Enterprise plans) are not affected by ad blockers since they measure at Cloudflare's edge.

7. **Query strings and UTM parameters not logged** — Cloudflare Web Analytics does not log query strings, which means UTM parameters are not tracked. This is by design to avoid capturing sensitive data in URLs. If UTM tracking is required, use a separate analytics tool.

8. **GraphQL API is available for programmatic access** — Contrary to common assumption, Web Analytics data *can* be queried programmatically via the GraphQL Analytics API using the `rumPageloadEventsAdaptiveGroups` and `rumPerformanceEventsAdaptiveGroups` datasets. However, this is an account-level API, not a dedicated Web Analytics API, and requires an API token with "Account Analytics: Read" permission.

## Debugging

1. **Check beacon loading (standalone mode)** — Open browser DevTools Network tab, filter for `cloudflareinsights.com`. Verify `beacon.min.js` loads with a 200 status.
2. **Check outgoing beacons** — After the page loads, look for POST requests to `cloudflareinsights.com` in the Network tab. The beacon sends page view and performance data.
3. **Verify token** — In the script tag, confirm the `data-cf-beacon` JSON contains the correct token from your Cloudflare dashboard.
4. **Dashboard verification** — In the Cloudflare dashboard, navigate to **Web Analytics**. Page views should appear within a few minutes.
5. **Automatic mode check** — If using Cloudflare proxy, view the page source in the browser and search for `cloudflareinsights`. The beacon script should be injected automatically near the closing `</body>` tag.
6. **SPA navigation check** — Navigate between routes in your SPA and verify each navigation generates a new beacon request in the Network tab.

## Further Documentation

This reference covers the essentials for implementation. For advanced topics, consult Cloudflare's official documentation:

- **Web Analytics overview:** https://developers.cloudflare.com/web-analytics/
- **Getting started:** https://developers.cloudflare.com/web-analytics/get-started/
- **About Web Analytics:** https://developers.cloudflare.com/web-analytics/about/
- **Core Web Vitals:** https://developers.cloudflare.com/web-analytics/data-metrics/core-web-vitals/
- **FAQs:** https://developers.cloudflare.com/web-analytics/faq/
- **Beacon changelog:** https://developers.cloudflare.com/web-analytics/changelog/
- **GraphQL Analytics API:** https://developers.cloudflare.com/analytics/graphql-api/
- **Cloudflare dashboard:** https://dash.cloudflare.com/
