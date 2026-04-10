<!-- Last verified: 2026-03-10 against Plausible docs -->
# Plausible Implementation Reference

## Overview

Plausible is an open-source, privacy-focused web analytics tool. It is cookieless, GDPR/CCPA/PECR-compliant by default, and requires no consent banners. Available as cloud-hosted (plausible.io) or self-hosted (Community Edition). The script is under 1 KB, making it significantly lighter than traditional analytics.

## Integration

### Script Tag (Current -- v3.1+)

As of October 2025 (v3.1.0), Plausible provides a **per-site dynamic snippet**. Each site gets a unique script URL generated from the Plausible dashboard:

```html
<script async src="https://plausible.io/js/pa-SITE_SPECIFIC_ID.js"></script>
<script>
  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
  plausible.init()
</script>
```

The per-site snippet is obtained from Settings > Site Installation > "Review Installation" in the Plausible dashboard. Optional measurements (outbound links, file downloads, form submissions, etc.) are toggled in the dashboard and apply automatically -- no snippet changes needed.

**`plausible.init()` overrides** can be passed to customize behavior per page:

```javascript
plausible.init({
  hashBasedRouting: true,        // Enable hash-based routing
  autoCapturePageviews: false,   // Disable automatic page view tracking (manual mode)
  captureOnLocalhost: true,      // Track on localhost for testing
  fileDownloads: { fileExtensions: ['pdf', 'xlsx'] },  // Custom file download tracking
  endpoint: 'https://your-proxy.com/api/event'         // Custom proxy endpoint
})
```

**Forge-approved domain:** `*.plausible.io`

### Legacy Script Tag (still supported)

The legacy format continues to work for backward compatibility:

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

The `data-domain` attribute must match the site domain registered in your Plausible dashboard. The `defer` attribute is required to avoid blocking page rendering.

### Script Extensions (Legacy)

> **Note:** As of v3.1.0, filename-based extensions are superseded by dashboard-based configuration and `plausible.init()` options. Legacy extension filenames still work but are no longer the recommended approach.

The legacy approach uses filename-based extensions appended to the script filename with dots:

| Extension | Filename | Purpose | New equivalent (`plausible.init`) |
|---|---|---|---|
| Custom events | `script.tagged-events.js` | Enable CSS-class-based event tracking | Automatic in new script |
| Hash-based routing | `script.hash.js` | Track hash changes as page views | `hashBasedRouting: true` |
| Outbound links | `script.outbound-links.js` | Track clicks on external links | Dashboard toggle |
| File downloads | `script.file-downloads.js` | Track file download clicks | Dashboard toggle / `fileDownloads` |
| Form submissions | `script.form-submissions.js` | Track form submissions | Dashboard toggle / `formSubmissions` |
| Revenue tracking | `script.revenue.js` | Attach revenue to custom events | Automatic in new script |
| Manual page views | `script.manual.js` | Disable auto page views, call manually | `autoCapturePageviews: false` |

Legacy combined extensions example:

```html
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.tagged-events.hash.outbound-links.js"></script>
```

### SPA Support

By default, Plausible tracks the initial page load only. For single-page applications, there are three approaches:

**Option 1: History API routing** -- Plausible's script automatically listens to `pushState` events. If your SPA uses the History API (React Router, Vue Router, Next.js), standard page view tracking works without additional configuration.

**Option 2: Hash-based routing** -- enable in `plausible.init()`:

```javascript
plausible.init({ hashBasedRouting: true })
```

Legacy approach: use the `hash` extension (`script.hash.js`).

**Option 3: Manual mode** -- disable auto-capture and call `plausible` explicitly on route changes:

```javascript
plausible.init({ autoCapturePageviews: false })
```

```javascript
// Call on each route change
window.plausible('pageview');
```

## Core Methods

### Page Views

Page views are tracked automatically on each page load. No code is required beyond the script tag. The following is auto-collected:

- Page URL (path)
- Referrer
- Browser (parsed from User-Agent)
- Operating system
- Device type (desktop/mobile/tablet)
- Country (from IP, then IP is discarded)

**Not auto-collected:** scroll depth, user identity, session recordings. Time on page is now measured via engagement signals (changed March 2025 -- previously estimated from subsequent page views). Form interactions can be tracked via the optional form submissions measurement.

### Custom Events

Custom events in Plausible are called "Goals" and must be pre-registered in the Plausible dashboard before data appears in reports.

With the **new per-site script (v3.1+)**, custom events and revenue tracking are automatically enabled -- no script extension required. With the **legacy script**, the `tagged-events` extension is needed for CSS-class-based event tracking. The `plausible()` JavaScript function works with both script versions.

```javascript
// Basic custom event
plausible('Signup');

// Custom event with properties
plausible('Download', { props: { format: 'pdf', document: 'whitepaper' } });

// Custom event with callback
plausible('Download', {
  callback: function() { console.log('event logged'); },
  props: { method: 'HTTP' }
});
```

**CSS class method** (alternative to JavaScript, tracks clicks automatically):

```html
<a class="plausible-event-name=Download plausible-event-position=header" href="/file.pdf">
  Download PDF
</a>
```

Note: use `+` to represent spaces in CSS class values (e.g., `plausible-event-name=Button+Click` becomes "Button Click").

**Custom event options:**

| Option | Type | Description |
|---|---|---|
| `props` | Object | Custom properties (key-value pairs) |
| `revenue` | Object | Revenue data (`{ currency, amount }`) |
| `callback` | Function | Executed after event is logged |
| `interactive` | Boolean | Whether event affects bounce rate (default: `true`) |

**Custom event limitations:**

- Event names are case-sensitive
- Property values must be strings, numbers, or booleans (no nested objects, no arrays)
- Maximum 30 custom properties per event
- Each event name must be registered as a Goal in site settings before data appears
- Property names limited to 300 characters, values limited to 2,000 characters
- Custom events count toward billable monthly pageviews

### Revenue Tracking

Attach monetary values to custom events. With the new per-site script, revenue tracking is automatically available. With the legacy script, the `revenue` extension is required.

```javascript
plausible('Purchase', { revenue: { currency: 'USD', amount: 29.99 } });
```

**CSS class method:**

```html
<button class="plausible-event-name=Purchase plausible-revenue-amount=29.99 plausible-revenue-currency=USD">
  Buy Now
</button>
```

Revenue tracking requires:
1. The event must be registered as a revenue goal in the dashboard with a base currency
2. The base currency cannot be changed after creation
3. Multi-currency is supported -- Plausible converts to the goal's base currency automatically

## Events API (Server-Side)

For server-side tracking, mobile apps, or non-browser environments:

**Endpoint:** `POST https://plausible.io/api/event`

**Required headers:**
- `User-Agent` -- used for device detection and unique visitor identification
- `Content-Type` -- `application/json` or `text/plain`

**Optional headers:**
- `X-Forwarded-For` -- client IP for unique visitor counting and geolocation
- `X-Debug-Request: true` -- returns HTTP 200 with IP info instead of 202

**Request body:**

```json
{
  "domain": "yourdomain.com",
  "name": "pageview",
  "url": "https://yourdomain.com/page",
  "referrer": "https://referrer.com",
  "props": { "key": "value" },
  "revenue": { "currency": "USD", "amount": 10.29 }
}
```

**Response:** HTTP 202 Accepted with empty JSON body `{}`

## Limits

| Constraint | Value |
|---|---|
| Custom properties per event | 30 |
| Property name length | 300 characters |
| Property value length | 2,000 characters |
| URL length (excluding domain & query) | 2,000 characters |
| Goals per site | Unlimited (but each must be manually created) |
| Stats API rate limit | 600 requests per hour per API key |
| Data retention (cloud) | Unlimited |
| Sites per account (cloud) | 50 on Growth plan, unlimited on Business |

## B2B Limitation

> **Not a product analytics tool.** Plausible is a privacy-focused web analytics tool. It does not support user identification, account grouping, or event properties beyond simple custom dimensions. It tracks aggregate page views and (optionally) simple custom events. For B2B user/account tracking, use it alongside a product analytics tool (Amplitude, Mixpanel, PostHog, or Accoil) -- not as a replacement.

## Common Pitfalls

1. **Forgetting to register Goals** -- Custom events silently drop if the event name is not registered as a Goal in the Plausible dashboard. No error is thrown in the browser. Always create the Goal in Settings > Goals before deploying event tracking code.

2. **Using the legacy script without required extensions** -- With the legacy `script.js`, CSS-class-based custom event tracking requires the `tagged-events` extension. Events via CSS classes are silently ignored without it. Note: the `plausible()` JavaScript function works with the base legacy script for programmatic event tracking. With the new per-site script (v3.1+), all features are automatically enabled.

3. **Mismatched domain** -- The domain in your snippet must exactly match the domain registered in Plausible. A mismatch (e.g., `www.example.com` vs `example.com`) causes all tracking to fail silently.

4. **Ad blockers blocking the script** -- Plausible's default CDN domain (`plausible.io`) is blocked by many ad blockers (6-26% of visitors, up to 60% for tech-savvy audiences). For higher accuracy, use a custom domain proxy (managed on Enterprise plans or self-configured via Cloudflare, Vercel, Nginx, etc.) or self-host.

5. **SPA route changes not tracked** -- If page views only show the initial load, verify you are using the latest script (which auto-detects History API navigation) or enable `hashBasedRouting` for hash-based routing.

6. **Expecting real-time property filtering** -- Custom properties are only available in the dashboard after the Goal is created and data is received. There is no retroactive property attachment.

7. **Mixing legacy and new script configuration** -- Legacy `data-*` attributes (like `data-exclude`, `data-include`, `data-api`) do not work with the new per-site script. Use `plausible.init()` options instead.

## Debugging

**Check script loaded:** Open browser DevTools > Network tab. Filter for `plausible`. You should see a request to the script URL (status 200) and subsequent requests to `plausible.io/api/event` (or your proxy endpoint) on page load.

**Verify events firing:** In the Network tab, filter for `/api/event`. Each page view and custom event sends a POST request. Inspect the request body to see the event name, URL, and properties.

**Test custom events in console:**

```javascript
// Fire a test event
plausible('Test Event', { props: { test: 'true' } });
```

**Debug via Events API header:** Add `X-Debug-Request: true` header to server-side requests to receive an HTTP 200 response with the IP address used for visitor counting.

**Plausible dashboard:** Events appear in the dashboard within 1-2 minutes. Check the "Goal Conversions" section for custom events.

**Self-hosted debug:** Check server logs for incoming events if running self-hosted Plausible Community Edition.

## Further Documentation

This reference covers the essentials for implementation. For advanced topics, consult Plausible's official documentation:

- **Getting Started:** https://plausible.io/docs
- **Add Snippet to Site:** https://plausible.io/docs/plausible-script
- **Script Update Guide (legacy to new):** https://plausible.io/docs/script-update-guide
- **Optional Measurements (Extensions):** https://plausible.io/docs/script-extensions
- **Custom Events (Goals):** https://plausible.io/docs/custom-event-goals
- **Custom Properties:** https://plausible.io/docs/custom-props/introduction
- **Custom Properties for Events:** https://plausible.io/docs/custom-props/for-custom-events
- **SPA / Hash-Based Routing:** https://plausible.io/docs/hash-based-routing
- **Revenue Tracking:** https://plausible.io/docs/ecommerce-revenue-tracking
- **Events API (Server-Side):** https://plausible.io/docs/events-api
- **Stats API (v2):** https://plausible.io/docs/stats-api
- **Stats API v1 (Legacy):** https://plausible.io/docs/stats-api-v1
- **Proxy Setup (Ad Blocker Bypass):** https://plausible.io/docs/proxy/introduction
- **Self-Hosting (Community Edition):** https://plausible.io/docs/self-hosting
