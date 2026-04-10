<!-- Last verified: 2026-03-10 against Fathom docs -->
# Fathom Implementation Reference

## Overview

Fathom is a privacy-focused, cookieless web analytics tool. It is GDPR, CCPA, ePrivacy, and PECR compliant out of the box with no consent banners required. Fathom is cloud-only (no self-hosted option). The tracking script is lightweight (~2 KB) and designed as a simple, privacy-respecting alternative to Google Analytics.

## Integration

### Script Tag

```html
<script src="https://cdn.usefathom.com/script.js" data-site="ABCDEFGH" defer></script>
```

The `data-site` attribute is your unique Site ID, found in the Fathom dashboard under Settings > Sites. The `defer` attribute is recommended.

**Forge-approved domain:** `*.cdn.usefathom.com`

### Script Attributes

| Attribute | Value | Purpose |
|---|---|---|
| `data-site` | Site ID string | Required. Identifies your site. |
| `data-spa` | `auto`, `history`, or `hash` | Enables SPA page view tracking. `auto` detects HTML5 History API and falls back to hash changes. `history` uses only HTML5 History API. `hash` uses only hash-based routing. |
| `data-honor-dnt` | `true` or `false` | Whether to honor Do Not Track headers. Default: `false`. Note: DNT is deprecated and no longer recommended by any browser. |
| `data-canonical` | `true` or `false` | Use canonical URL instead of current URL. Default: `true`. |
| `data-auto` | `true` or `false` | Controls automatic page view tracking on page load. Default: `true`. Set to `false` to disable automatic tracking and call `fathom.trackPageview()` manually. |

> **Note on domain filtering:** Fathom does not support `data-excluded-domains` or `data-included-domains` script attributes. Domain filtering (allowed domains, blocked IPs, blocked countries, blocked referrers) is configured through the **dashboard firewall settings** under Settings > Firewall.

### SPA Support

Fathom has built-in SPA support. Add the `data-spa="auto"` attribute to automatically track route changes in single-page applications:

```html
<script src="https://cdn.usefathom.com/script.js" data-site="ABCDEFGH" data-spa="auto" defer></script>
```

This listens for History API `pushState` and `replaceState` calls, as well as `popstate` events, and falls back to `hashchange` if the History API is unavailable. Works with React Router, Vue Router, Next.js, Nuxt, SvelteKit, and similar frameworks.

## Core Methods

### Page Views

Page views are tracked automatically on page load (unless `data-auto="false"` is set). When `data-spa="auto"` is set, SPA route changes are also tracked automatically. The following is auto-collected:

- Page URL (path)
- Referrer
- UTM parameters (source, medium, campaign, term, content)
- Browser and OS (aggregated, not per-user)
- Country (from IP, then IP is discarded)
- Device type

**Not auto-collected:** scroll depth, time on page, user identity, form interactions, click tracking.

**Manual page view tracking:**

```javascript
// Track a page view manually
fathom.trackPageview();

// Track a page view for a specific URL
fathom.trackPageview({ url: '/custom/path' });

// Track a page view with a specific URL and referrer
fathom.trackPageview({ url: '/custom/path', referrer: 'https://example.com' });
```

When passing custom `url` or `referrer` parameters, the canonical URL will not be used -- your parameters become the source of truth. You do not have to send both; if you send just the referrer, the URL defaults to the canonical or current URL.

### Custom Events

Fathom supports custom events (formerly called "Goals"). Events are tracked by **event name** (a human-readable string), not by an opaque ID.

```javascript
// Track a custom event by name
fathom.trackEvent('newsletter signup');

// Track a custom event with a monetary value (in cents)
fathom.trackEvent('cart add', { _value: 2999 });
```

Events do **not** need to be pre-created in the Fathom dashboard. When you call `fathom.trackEvent('some name')`, if the event doesn't exist yet, Fathom creates it automatically.

> **Deprecated:** The old `fathom.trackGoal('GOAL_ID')` method (which used opaque goal IDs from the dashboard) was deprecated on October 25, 2023. Use `fathom.trackEvent('event name')` instead. Existing `trackGoal` calls continue to work but should be migrated.

**Custom event limitations:**

- No custom properties or dimensions on events. The only optional parameter is `_value` (monetary, in cents).
- Event names should avoid special characters and emojis.
- You cannot rename an event once it has been created and fired to the dashboard, but you can change the event name in your code (which creates a new event).
- No way to attach metadata, categories, or labels to events.
- Events count as page views against your plan's monthly pageview allowance.

### Revenue / Value Tracking

Attach a monetary value to any event. Values are specified in the smallest currency unit (cents):

```javascript
// Track a $29.99 purchase
fathom.trackEvent('widget purchase', { _value: 2999 });
```

The currency is set per-site in the Fathom dashboard (not in code).

## Limits

| Constraint | Value |
|---|---|
| Events per site | Unlimited (events count as pageviews against plan allowance) |
| Custom properties per event | 0 (not supported) |
| Event value | Integer (cents), no fractional values |
| Sites per account | Up to 50 included on all plans |
| API rate limit (Sites & Events) | 2,000 requests per hour |
| API rate limit (Aggregations & Current Visitors) | 10 requests per minute |
| Data retention | Unlimited |

## B2B Limitation

> **Not a product analytics tool.** Fathom is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties. It tracks aggregate page views and (optionally) simple custom events with an optional monetary value. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) -- not as a replacement.

## Common Pitfalls

1. **Using the deprecated `trackGoal()` instead of `trackEvent()`** -- The old `trackGoal('GOAL_ID')` method was deprecated in October 2023. Use `fathom.trackEvent('event name')` with a human-readable event name string instead. The old method still works for existing goals but should be migrated.

2. **Forgetting `data-spa="auto"` for SPAs** -- Without this attribute, Fathom only tracks the initial page load. All subsequent client-side route changes are invisible. This is the most common issue in React, Vue, and Next.js apps.

3. **Expecting custom properties on events** -- Fathom events have no property or dimension support. If you need to track event metadata (e.g., `button_color`, `plan_type`), Fathom cannot do this. Use a product analytics tool for property-rich event tracking.

4. **Value in dollars instead of cents** -- The `_value` parameter expects the smallest currency unit (cents). Passing `29.99` instead of `2999` records the value as $0.30, not $29.99.

5. **Blocked by ad blockers** -- Fathom's CDN domain (`cdn.usefathom.com`) may be blocked by some ad blockers. <!-- UNVERIFIED: Fathom's custom domain feature (which was used to bypass ad blockers) is no longer offered as of May 2023. Existing custom domains continue to work but new ones cannot be created. Current ad-blocker bypass options should be verified with Fathom support. -->

6. **Domain filtering is dashboard-only** -- Domain allowing/blocking (allowed domains, blocked IPs, blocked countries, blocked referrers) is configured in the Fathom dashboard under firewall settings, not via script attributes. There are no `data-excluded-domains` or `data-included-domains` script attributes.

## Debugging

**Check script loaded:** Open browser DevTools > Network tab. Filter for `usefathom`. You should see a request to `cdn.usefathom.com/script.js` (status 200).

**Verify page views firing:** In the Network tab, look for requests to Fathom's collection endpoint. Each page view sends a beacon.

**Test manual tracking in console:**

```javascript
// Check the fathom object is available
console.log(typeof fathom);  // should be 'object'

// Fire a manual page view
fathom.trackPageview();

// Fire a test event
fathom.trackEvent('test event');
```

**Fathom dashboard:** Page views and events appear in the dashboard within seconds (near real-time). Check the main dashboard for page views and the Events section for custom events.

**Block your own visits:** Use `fathom.blockTrackingForMe()` in the browser console to exclude your own traffic. This is stored in localStorage and persists across sessions. Use `fathom.enableTrackingForMe()` to re-enable.

```javascript
// Exclude yourself from analytics
fathom.blockTrackingForMe();

// Re-include yourself
fathom.enableTrackingForMe();
```

## Further Documentation

This reference covers the essentials for implementation. For advanced topics, consult Fathom's official documentation:

- **Getting Started:** https://usefathom.com/docs
- **Script Installation:** https://usefathom.com/docs/script/embed
- **Script Attributes:** https://usefathom.com/docs/script/script-advanced
- **SPA Tracking:** https://usefathom.com/docs/script/script-advanced
- **Custom Events:** https://usefathom.com/docs/events/overview
- **Custom Domains:** https://usefathom.com/docs/script/custom-domains (no longer offered)
- **API Reference:** https://usefathom.com/api
- **Framework Guides:** https://usefathom.com/docs/integrations
