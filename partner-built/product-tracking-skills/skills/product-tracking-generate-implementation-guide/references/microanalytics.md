<!-- Last verified: 2026-03-10 against Microanalytics docs -->
# Microanalytics Implementation Reference

## Overview

Microanalytics is a privacy-focused, cookieless web analytics tool hosted in the EU (OVH data center in France). It is GDPR, PECR, and CCPA compliant by design, does not use cookies or fingerprinting, and does not collect personal data. It provides page view counts, referrers, browser/device breakdowns, geographic data (country and city level), and custom event tracking. The tracking script is less than 1KB. Cloud-only, proprietary SaaS.

## Integration

### Script Tag

```html
<script
  data-host="https://microanalytics.io"
  data-dnt="false"
  src="https://microanalytics.io/js/script.js"
  id="ZwSg9rf6GA"
  async
  defer
></script>
```

The `id` attribute is your site-specific tracking ID, found in your Microanalytics dashboard. Replace `ZwSg9rf6GA` with your actual ID.

The optional `data-dnt` attribute controls Do Not Track header compliance. When set to `"true"`, the script will not send tracking requests for visitors whose browsers have DNT enabled. Defaults to `"false"`.

### Forge Manifest

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.microanalytics.io"
          category: analytics
          inScopeEUD: false
```

### SPA Support

Microanalytics automatically detects `history.pushState()` calls and `popstate` events for single-page application routing. The script overrides `history.pushState()` to intercept client-side navigation, capturing the previous URL as the referrer and sending a tracking request on each route change. Back/forward button navigation is tracked via the `onpopstate` event handler. This means SPAs using React Router, Vue Router, Next.js, or similar client-side routers should have page views tracked without additional configuration.

If automatic detection does not work in your setup, you can manually trigger a page view by calling `window.pa.track()` with no arguments after a route change.

## Core Methods

### Page Views

Page views are tracked automatically on page load and on SPA route changes (via History API detection). No manual call is needed.

### Custom Events

Microanalytics supports custom event tracking via the `window.pa.track()` method:

```javascript
// Track a named event
window.pa.track('signup-button-clicked');

// Or equivalently
pa.track('signup-button-clicked');
```

Custom events are limited to a name string. There is no support for event properties or structured metadata. Events are sent as POST requests to the `/api/event` endpoint on the Microanalytics host.

Custom events can be queried via the Stats API using the `event` stat type (see REST API section below).

## REST API

Microanalytics provides a read-only REST API for retrieving analytics data. API access is included in all pricing tiers.

### Authentication

API keys are obtained from the account settings page at `https://app.microanalytics.io/account/api`. Send the key as a Bearer token:

```
Authorization: Bearer {api_key}
```

### Stats API

```bash
curl --location --request GET \
  'https://app.microanalytics.io/api/v1/stats/{site_id}?name={stat_type}&from={YYYY-MM-DD}&to={YYYY-MM-DD}' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {api_key}'
```

**Required parameters:**

| Parameter | Type | Description |
|---|---|---|
| `name` | string | Stat type: `browser`, `campaign`, `city`, `continent`, `country`, `device`, `event`, `landing_page`, `language`, `os`, `page`, `pageviews`, `pageviews_hours`, `referrer`, `resolution`, `visitors`, `visitors_hours` |
| `from` | string | Start date (`YYYY-MM-DD`) |
| `to` | string | End date (`YYYY-MM-DD`) |

**Optional parameters:** `search`, `search_by` (default: `url`), `sort_by` (`count` or `value`, default: `count`), `sort` (`asc` or `desc`, default: `desc`), `per_page` (`10`, `25`, `50`, `100`, default: `25`).

### Websites API

- **List:** `GET https://app.microanalytics.io/api/v1/websites`
- **Get:** `GET https://app.microanalytics.io/api/v1/websites/{id}`
- **Create:** `POST https://app.microanalytics.io/api/v1/websites` (required: `domain`)
- **Update:** `PUT/PATCH https://app.microanalytics.io/api/v1/websites/{id}`
- **Delete:** `DELETE https://app.microanalytics.io/api/v1/websites/{id}`

### Account API

- **Get:** `GET https://app.microanalytics.io/api/v1/account`

## Limits

| Constraint | Value |
|---|---|
| Custom event properties | Not supported (name string only) |
| User identification | Not supported (aggregate metrics only) |
| Account/group grouping | Not supported |
| Data hosting | EU — OVH data center, France |
| Cookie usage | None |
| Fingerprinting | None |
| Tracking script size | < 1KB |
| Free plan limit | 1,000 pageviews/month, 1 website |
| Data retention | Varies by plan |
| Server-side tracking | Not supported (client-side only) |
| REST API | Read-only, included in all plans |

## B2B Limitation

> **Not a product analytics tool.** Microanalytics is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) — not as a replacement.

## Common Pitfalls

1. **Assuming custom events support properties** — Custom events accept only a name string. You cannot attach structured data like `{ report_id: 'rpt_789', type: 'standard' }`. For rich event tracking, use a product analytics tool alongside Microanalytics.

2. **Expecting user-level analytics** — Microanalytics provides aggregate metrics only. You cannot see individual user journeys, session recordings, or per-user event streams. It answers "how many page views did /pricing get?" not "which users visited /pricing?"

3. **Relying on Microanalytics for funnel analysis** — Without user identity or event properties, funnel analysis (e.g., signup > onboarding > first use) is not possible. Use Microanalytics for traffic overview and a product analytics tool for behavioral analysis.

4. **Script blocked by ad blockers** — The `microanalytics.io` domain may be blocked by some browser extensions. Unlike Plausible, Microanalytics does not offer a documented proxy or custom domain option to bypass this.

5. **Assuming server-side tracking is available** — Microanalytics is a client-side-only tool. There is no documented server-side API or Node.js SDK for sending events from a backend.

## Debugging

1. **Check script loading** — Open browser DevTools Network tab and filter for `microanalytics.io`. Verify the script loads with a 200 status code.
2. **Check outgoing beacons** — After page load, look for POST requests to `/api/event` on `microanalytics.io` in the Network tab. A successful page view generates a tracking request via XMLHttpRequest POST.
3. **Dashboard verification** — Log into your Microanalytics dashboard. Page views typically appear within minutes. Check the real-time view if available.
4. **SPA route tracking** — Navigate between routes in your SPA and verify each navigation generates a new network request to `microanalytics.io`.
5. **Ad-blocker check** — If no tracking requests appear, temporarily disable ad blockers and privacy extensions to rule out script blocking.

## Further Documentation

This reference covers the essentials for implementation. Consult:

- **Official site:** https://microanalytics.io
- **Developer API portal:** https://app.microanalytics.io/developers
- **Stats API docs:** https://app.microanalytics.io/developers/stats
- **Websites API docs:** https://app.microanalytics.io/developers/websites
- **Account API docs:** https://app.microanalytics.io/developers/account
- **API key management:** https://app.microanalytics.io/account/api
- **Articles / blog:** https://microanalytics.io/articles/index.html

**Documentation note:** The custom event API (`window.pa.track()`) and SPA behavior documented here were verified by inspecting the tracking script source (`microanalytics.io/js/script.js`) and the REST API developer pages. The REST API documentation is available behind the app subdomain at the links above.
