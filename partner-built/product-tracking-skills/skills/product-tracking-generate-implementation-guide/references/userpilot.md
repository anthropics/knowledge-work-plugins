<!-- Last verified: 2026-03-10 against UserPilot docs -->
# Userpilot Implementation Reference

## Overview

Userpilot is a user onboarding and product adoption platform. It provides in-app guides, checklists, tooltips, surveys (NPS/CSAT), and resource centers to drive feature adoption. Userpilot also includes a lightweight event tracking API for product analytics. It is proprietary and cloud-only.

**Category: Session / Behavior Tool.** Userpilot supplements product analytics with in-app engagement experiences. Its event tracking is secondary to its core purpose of delivering contextual guidance. It is not a replacement for full product analytics.

## Integration

### Script Tag

Add the Userpilot snippet to the `<head>` of your application. The App Token is found in Userpilot under Settings > Environment.

```html
<script>window.userpilotSettings = {token: "YOUR_APP_TOKEN"};</script>
<script src="https://js.userpilot.io/sdk/latest.js"></script>
```

Replace `YOUR_APP_TOKEN` with your Userpilot App Token (found in Settings > Environment).

### npm Package

```bash
npm install userpilot
```

```typescript
import { Userpilot } from 'userpilot';

Userpilot.initialize('YOUR_APP_TOKEN');
```

## Initialization

After loading the script or npm package, Userpilot must be initialized with user identification before any experiences (guides, checklists) can be triggered. Userpilot does NOT display experiences until `identify()` or `anonymous()` is called.

```typescript
// Userpilot is loaded but inactive until identify() or anonymous() is called
```

## User Identification

User identification is the core requirement for Userpilot. Every feature — guides, checklists, NPS surveys, resource centers — depends on knowing who the user is so experiences can be targeted and tracked.

**Browser:**

```javascript
userpilot.identify('usr_123', {
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'admin',
  plan: 'pro',
  created_at: '2024-01-15T00:00:00Z',
  company: {
    id: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    created_at: '2023-06-01T00:00:00Z',
    monthly_spend: 5000
  }
});
```

```typescript
// Using the npm package
import { Userpilot } from 'userpilot';

Userpilot.identify('usr_123', {
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'admin',
  plan: 'pro',
  created_at: '2024-01-15T00:00:00Z',
  company: {
    id: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    created_at: '2023-06-01T00:00:00Z',
    monthly_spend: 5000
  }
});
```

**Key points about identify:**

| Aspect | Detail |
|---|---|
| First argument | Unique user ID (string, required) |
| Second argument | Object with user properties and optional `company` object |
| Company nesting | Pass `company: { id, name, ... }` inside the identify properties |
| created_at | ISO 8601 string. Used for cohort-based targeting of experiences. |
| Persistence | Userpilot stores identification in the browser session |

**When to call:** In multi-page apps, call on every page load. In SPAs, call `identify()` once after successful authentication, then call `userpilot.reload()` on each route change to re-evaluate targeting rules for the current page.

### SPA Route Change Handling

```typescript
// Call on every route change in your SPA
// This re-evaluates which experiences should show on the new page
userpilot.reload();

// Optionally pass a URL to override the detected page URL
userpilot.reload({ url: 'https://app.example.com/dashboard' });
```

For React Router:

```typescript
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();

  useEffect(() => {
    userpilot.reload();
  }, [location]);

  return <Routes>...</Routes>;
}
```

### Anonymous Users

Userpilot supports anonymous users via the `anonymous()` method. This automatically generates a session-based unique ID, enabling targeted content on public pages without requiring user-specific data.

```javascript
// For public/pre-login pages — no parameters needed
userpilot.anonymous();
```

Anonymous users are counted toward your MAU. To target content specifically at anonymous users, set audience conditions in the dashboard to "User Data" => "user id" => doesn't exist. Content marked for "All users" will also display to anonymous visitors.

## Group / Company Identification

Company data is passed as a nested object inside `identify()`. The JavaScript SDK does not have a separate `group()` method.

```javascript
userpilot.identify('usr_123', {
  name: 'Jane Smith',
  email: 'jane@example.com',
  company: {
    id: 'acc_456',           // Required for company identification
    name: 'Acme Corp',
    plan: 'enterprise',
    created_at: '2023-06-01T00:00:00Z',
    employee_count: 50,
    monthly_spend: 5000
  }
});
```

For server-side company updates, use the HTTP API endpoint `POST https://analytex.userpilot.io/v1/companies/identify` with `company_id` (required) and `metadata` object. A company without associated users will not appear in the companies dashboard.

Company properties enable targeting experiences by account attributes (e.g., show an enterprise onboarding flow only to accounts on the `enterprise` plan).

## Custom Events / Triggers

Userpilot supports custom events that serve two purposes:
1. **Trigger experiences** — show a guide, checklist, or survey when an event fires
2. **Track product usage** — Userpilot records events for its own analytics (feature adoption, user activity)

### Track Events

```javascript
// Track a product event
userpilot.track('report_created', {
  report_id: 'rpt_789',
  report_type: 'standard'
});

// Track without properties
userpilot.track('onboarding_completed');

// Track feature usage
userpilot.track('export_generated', {
  format: 'csv',
  row_count: 1500
});
```

Unlike Hotjar, Userpilot events do accept properties. Property values must be primitive types: string, number, boolean, or null. Arrays and objects as property values are not supported. These properties can be used for:
- Filtering in Userpilot's analytics
- Targeting experiences (e.g., show a guide when `report_type` equals `template`)

### Trigger Experiences Programmatically

You can trigger specific Userpilot experiences (guides, checklists) via their content ID:

```javascript
// Trigger a specific experience by its content ID
userpilot.trigger('CONTENT_ID');
```

The Content ID is found in the Userpilot dashboard under the experience settings. This bypasses normal targeting rules and forces the experience to display.

## Guides and Checklists

Guides, checklists, tooltips, and resource centers are configured in the Userpilot dashboard — not in code. The JavaScript SDK's role is to:

1. **Identify the user** so targeting rules can be evaluated
2. **Track events** that trigger experiences
3. **Reload on navigation** so page-based targeting works
4. **Programmatically trigger** specific experiences when needed

### Checklist Example (Dashboard-Configured, Code-Triggered)

A typical onboarding checklist flow:

```javascript
// 1. User logs in — identify them
userpilot.identify('usr_123', {
  name: 'Jane Smith',
  email: 'jane@example.com',
  created_at: '2024-01-15T00:00:00Z',
  company: { id: 'acc_456', name: 'Acme Corp' }
});

// 2. User completes onboarding steps — track events
// Userpilot checklist items can be marked complete based on these events
userpilot.track('profile_completed');
userpilot.track('first_report_created');
userpilot.track('team_member_invited');

// 3. On route change — reload to show context-appropriate guides
userpilot.reload();
```

### Listening to Experience Events

```javascript
// Listen for experience events
// Supported events: 'started', 'completed', 'dismissed', 'step'
userpilot.on('completed', (data) => {
  console.log('User completed experience:', data);
});

userpilot.on('dismissed', (data) => {
  console.log('User dismissed experience:', data);
});

// One-time listener (fires once then auto-removes)
userpilot.once('started', (data) => {
  console.log('First experience started:', data);
});

// Remove a listener
userpilot.off('completed');
```

## Privacy Controls

### Opt Out Users

```javascript
// Do not initialize Userpilot for users who have not consented
if (userHasConsentedToAnalytics()) {
  userpilot.identify('usr_123', { ... });
} else {
  // Do not call identify — Userpilot remains inactive
}
```

### Clear User Data / Session Management

```javascript
// Clear Userpilot storage and session data
userpilot.clean();

// Remove all Userpilot data and active content from the page
userpilot.destroy();

// Temporarily halt all SDK operations (e.g., for consent withdrawal)
userpilot.suppress();

// Resume SDK operations
userpilot.unsuppress();

// End the currently running flow
userpilot.end();
```

### Exclude Specific Pages

Page-based targeting is configured in the Userpilot dashboard. To prevent experiences from appearing on specific pages, configure URL exclusion rules in the experience targeting settings.

### Data Sent to Userpilot

Userpilot receives:
- User ID and properties passed to `identify()`
- Company ID and properties
- Events passed to `track()`
- Current page URL (for page-based targeting)
- Browser metadata (user agent, screen size)

Userpilot does NOT record sessions or capture screenshots. It operates on the DOM level to inject guides and tooltips, not to capture visual recordings.

## What Userpilot Is NOT

Userpilot provides **in-app guidance and lightweight event tracking** to drive product adoption. It supplements product analytics but does not replace them.

**Userpilot does NOT provide:**
- Full product analytics (funnels, retention, cohort analysis — use Amplitude, Mixpanel, PostHog)
- Session recording or heatmaps (use Hotjar, PostHog)
- Account-level engagement scoring (use Accoil)
- Server-side experience triggering (experiences are browser-only; however, a server-side HTTP API exists for identify and track)
- A/B testing for code changes (use LaunchDarkly, PostHog, Statsig)
- Deep behavioral analytics or SQL-based querying

**Use Userpilot alongside product analytics.** Product analytics tells you which features have low adoption. Userpilot helps you fix it by showing targeted guides to the right users at the right time.

## Forge Compatibility

**Approved domains:**
- `*.userpilot.io`

```yaml
permissions:
  external:
    fetch:
      backend:
        - address: "*.userpilot.io"
          category: analytics
          inScopeEUD: false
```

**Considerations for Forge apps:** Userpilot runs in the browser and injects DOM elements (tooltips, modals, guides) into the page. In Forge Custom UI (sandboxed iframe), the Userpilot script would need to run inside the iframe. This means:

1. Userpilot guides will appear inside the Forge app iframe, not in the parent Atlassian page
2. The current page URL visible to Userpilot is the iframe URL, not the Atlassian page URL — configure targeting rules accordingly
3. Ensure no in-scope End User Data (issue titles, page content) is passed to Userpilot via `identify()` or `track()` properties

## Common Pitfalls

1. **Not calling identify before anything else** -- Userpilot does nothing until `identify()` is called. Experiences will not display, events will not track, and checklists will not appear. This is the most common integration issue.

2. **Forgetting to call reload() on SPA route changes** -- Userpilot evaluates targeting rules based on the current page URL. In single-page applications, route changes do not trigger a page load. Call `userpilot.reload()` on every route change or the wrong experiences will appear (or none at all).

3. **Passing company data outside the company object** -- Company properties must be nested inside `company: { id, name, ... }` in the identify call. Flat properties like `company_name: 'Acme'` at the top level are treated as user properties, not company properties. The JavaScript SDK does not have a separate `group()` method.

4. **Using Userpilot events as primary product analytics** -- Userpilot's `track()` API is useful for triggering experiences and lightweight analytics. It is not a substitute for a dedicated product analytics platform. Event properties and querying capabilities are limited compared to Amplitude, Mixpanel, or PostHog.

5. **Not sending created_at on identify** -- Without `created_at`, Userpilot cannot target experiences by user age (e.g., "show onboarding guide only to users created in the last 7 days"). This is critical for time-based onboarding flows.

6. **Expecting server-side experience triggering** -- Userpilot experiences (guides, checklists, tooltips) are browser-only and cannot be triggered from the server. However, Userpilot does provide a server-side HTTP REST API (`POST https://analytex.userpilot.io/v1/identify` and `/v1/track`) for sending identify and track data. This API uses an API Key (not App Token) and requires the `X-API-Version: 2020-09-22` header.

## Debugging

### Verify Userpilot Is Loaded

```javascript
// Console check
typeof userpilot !== 'undefined'  // Should be true
```

<!-- UNVERIFIED: isIdentified() was previously documented here but is not listed in current SDK docs. It may still work but is not in the official API reference. -->

### Network Tab

In DevTools Network tab, look for requests to:
- `js.userpilot.io` — SDK script loading
- `analytex.userpilot.io` — event, identification, and analytics data transmission

### Userpilot Chrome Extension

Userpilot provides a Chrome extension for debugging:
- See which experiences are loaded on the current page
- View targeting rule evaluation results
- Preview experiences in draft mode

### Dashboard Verification

1. **Users:** In the Userpilot dashboard, go to Users to verify identification data is arriving.
2. **Events:** Check the Events section to see tracked events and their properties.
3. **Experience Preview:** Use the preview mode in the experience editor to test targeting rules.

### Debug Mode

```javascript
// Enable verbose console logging
// Add ?userpilot_debug=true to your page URL
// Or set in initialization:
userpilot.identify('usr_123', {
  name: 'Jane Smith'
});
// Then check browser console for Userpilot debug output
```

## Further Documentation

This reference covers the essentials for user onboarding and behavior tracking implementation. For advanced topics, consult Userpilot's official documentation:

- **Getting Started:** https://docs.userpilot.com/
- **Web Installation:** https://docs.userpilot.com/developer/installation/web
- **JavaScript SDK API:** https://docs.userpilot.com/developer/installation/SDK-APIs
- **User Identification:** https://docs.userpilot.com/api-references/real-time/identify-user
- **Bulk User Updates:** https://docs.userpilot.com/api-references/bulk-updates/users
- **Anonymous Users:** https://docs.userpilot.com/developer/installation/anonymous-user
- **Real-Time API Overview:** https://docs.userpilot.com/api-references/real-time/overview
- **HTTP REST API (Identify/Track):** https://docs.userpilot.com/article/195-identify-users-and-track-api
- **Identify Company API:** https://docs.userpilot.com/api-references/real-time/identify-company
- **SPA Frameworks:** https://docs.userpilot.com/article/22-install-userpilot-on-single-page-application-frameworks
