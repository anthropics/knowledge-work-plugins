<!-- Last verified: 2026-03-11 against Intercom docs -->
# Intercom Implementation Reference

## Overview

Intercom is a customer engagement and communications platform used for live chat, in-app messaging, product tours, and customer support. It maintains a contact model (users and leads) with company associations, and supports custom event tracking for triggering messages, building segments, and measuring engagement. Proprietary, cloud-only SaaS.

**Category:** B2B Engagement
**B2B Fit:** Full — native users, companies (accounts), and custom events with metadata properties.

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | `@intercom/messenger-js-sdk` | `npm install @intercom/messenger-js-sdk` |
| Browser (snippet) | JavaScript snippet | No install — embed in HTML |
| Node.js | `intercom-client` | `npm install intercom-client` |
| HTTP API | REST API | No SDK — raw `fetch()` calls |

Intercom provides a JavaScript Messenger SDK for browser-side identity and event tracking, a Node.js SDK (`intercom-client`) for server-side contact/company/event management, and a REST API usable from any environment. Ruby, Python, and PHP SDKs also exist but are not documented here.

## Initialization

### Browser (Messenger JS SDK)

```typescript
import Intercom from '@intercom/messenger-js-sdk';

Intercom({
  app_id: 'YOUR_APP_ID',
  user_id: 'usr_123',
  email: 'jane@example.com',
  created_at: 1705276800,
  user_hash: 'HMAC_SHA256_HASH', // required when identity verification is enabled
});
```

### Browser (Snippet)

```html
<script>
(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/YOUR_APP_ID';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
</script>
```

Then boot with user identity:

```javascript
window.Intercom('boot', {
  app_id: 'YOUR_APP_ID',
  user_id: 'usr_123',
  email: 'jane@example.com',
  created_at: 1705276800,
  user_hash: 'HMAC_SHA256_HASH',
});
```

### Node.js

```typescript
import { IntercomClient } from 'intercom-client';

const client = new IntercomClient({
  token: process.env.INTERCOM_ACCESS_TOKEN!,
});
```

### HTTP API

```
Base URL: https://api.intercom.io
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
Intercom-Version: 2.11
```

Access tokens are created in Settings > Developer Hub > Your App > Authentication. Tokens require write permissions to send events and create/update contacts and companies.

## Core Methods

### identify()

Identifies a user (contact) and sets user-level attributes. Intercom distinguishes between `user` and `lead` roles — use `role: "user"` for authenticated users.

**Browser (snippet):**
```javascript
window.Intercom('boot', {
  app_id: 'YOUR_APP_ID',
  user_id: 'usr_123',
  email: 'jane@example.com',
  name: 'Jane Doe',
  created_at: 1705276800,
  user_hash: 'HMAC_SHA256_HASH',
  company: {
    company_id: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    monthly_spend: 5000,
    created_at: 1685577600,
  },
  custom_attributes: {
    role: 'admin',
    plan: 'enterprise',
  },
});
```

To update traits after boot:

```javascript
window.Intercom('update', {
  name: 'Jane Doe',
  custom_attributes: {
    role: 'admin',
    last_active_project: 'proj_123',
  },
});
```

**Browser (Messenger JS SDK):**
```typescript
import Intercom from '@intercom/messenger-js-sdk';
import { update } from '@intercom/messenger-js-sdk';

// Initial boot
Intercom({
  app_id: 'YOUR_APP_ID',
  user_id: 'usr_123',
  email: 'jane@example.com',
  name: 'Jane Doe',
  created_at: 1705276800,
});

// Update traits later
update({
  name: 'Jane Doe',
  custom_attributes: {
    role: 'admin',
  },
});
```

**Node.js:**
```typescript
// Create a new contact
await client.contacts.create({
  role: 'user',
  externalId: 'usr_123',
  email: 'jane@example.com',
  name: 'Jane Doe',
  signedUpAt: 1705276800,
  customAttributes: {
    role: 'admin',
    plan: 'enterprise',
  },
});

// Update an existing contact (requires Intercom's internal contact ID)
await client.contacts.update({
  contactId: 'INTERCOM_CONTACT_ID',
  name: 'Jane Doe',
  customAttributes: {
    role: 'admin',
    plan: 'enterprise',
  },
});
```

**HTTP API:**
```json
POST /contacts
{
  "role": "user",
  "external_id": "usr_123",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "signed_up_at": 1705276800,
  "custom_attributes": {
    "role": "admin",
    "plan": "enterprise"
  }
}
```

To update, use PUT with the Intercom-assigned contact ID:

```json
PUT /contacts/{id}
{
  "name": "Jane Doe",
  "custom_attributes": {
    "role": "admin",
    "plan": "enterprise"
  }
}
```

**When to call:** On login, signup, or when user traits change. The `update` method (browser) is throttled to 20 calls per 30-minute window per user.

### group() / Company Tracking

Intercom uses "companies" as its account/group concept. Companies are associated with contacts and can carry their own attributes. Every user can belong to multiple companies.

**Browser (snippet):**
```javascript
window.Intercom('boot', {
  app_id: 'YOUR_APP_ID',
  user_id: 'usr_123',
  email: 'jane@example.com',
  company: {
    company_id: 'acc_456',
    name: 'Acme Corp',
    plan: 'enterprise',
    monthly_spend: 5000,
    size: 150,
    industry: 'technology',
    created_at: 1685577600,
    custom_attributes: {
      is_paying: true,
      mrr: 5000,
    },
  },
});
```

**Node.js:**
```typescript
// Create or update a company
await client.companies.createOrUpdate({
  companyId: 'acc_456',
  name: 'Acme Corp',
  plan: 'enterprise',
  size: 150,
  industry: 'technology',
  monthlySpend: 5000,
  remoteCreatedAt: 1685577600,
  customAttributes: {
    is_paying: true,
    mrr: 5000,
  },
});

// Attach a contact to a company
await client.companies.attachContact({
  contactId: 'INTERCOM_CONTACT_ID',
  id: 'INTERCOM_COMPANY_ID',
});
```

**HTTP API:**
```json
POST /companies
{
  "company_id": "acc_456",
  "name": "Acme Corp",
  "plan": "enterprise",
  "size": 150,
  "industry": "technology",
  "monthly_spend": 5000,
  "remote_created_at": 1685577600,
  "custom_attributes": {
    "is_paying": true,
    "mrr": 5000
  }
}
```

To attach a contact to a company via the REST API:

```json
POST /contacts/{contact_id}/companies
{
  "id": "INTERCOM_COMPANY_ID"
}
```

**Important:** Companies are only visible in Intercom when at least one contact is associated with them. In the browser, passing the `company` object inside `boot` or `update` automatically associates the current user with that company. Server-side requires an explicit attach call.

### track()

Records a custom event associated with a user. Events in Intercom are used for triggering messages, building user segments, and tracking engagement.

**Browser (snippet):**
```javascript
Intercom('trackEvent', 'report_created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  source: 'dashboard',
});
```

**Browser (Messenger JS SDK):**
```typescript
import { trackEvent } from '@intercom/messenger-js-sdk';

trackEvent('report_created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  source: 'dashboard',
});
```

**Node.js:**
```typescript
await client.events.create({
  eventName: 'report_created',
  userId: 'usr_123',
  createdAt: Math.floor(Date.now() / 1000),
  metadata: {
    report_id: 'rpt_789',
    report_type: 'standard',
    source: 'dashboard',
  },
});
```

**HTTP API:**
```json
POST /events
{
  "event_name": "report_created",
  "created_at": 1710100000,
  "user_id": "usr_123",
  "metadata": {
    "report_id": "rpt_789",
    "report_type": "standard",
    "source": "dashboard"
  }
}
```

**When to call:** After the action succeeds. In the browser, `trackEvent` automatically associates the event with the currently logged-in user. Server-side requires explicit `user_id`, `email`, or Intercom contact `id`.

## Group Context on Track Calls

Intercom's event model does not natively support attributing events to a specific company. Events are associated with contacts (users/leads), not companies. Company attribution is inferred from the user-company association rather than being passed on each event.

**For products with hierarchical groups:** Intercom operates at a single company level. There is no native support for nested structures like account > workspace > project. Carry sub-group identifiers as event metadata:

```json
POST /events
{
  "event_name": "task_completed",
  "created_at": 1710100000,
  "user_id": "usr_123",
  "metadata": {
    "task_id": "task_456",
    "workspace_id": "ws_789",
    "project_id": "proj_123",
    "company_id": "acc_456"
  }
}
```

If you need events attributed to specific companies for filtering or segmentation, include the `company_id` in event metadata as shown above. This is a metadata-level workaround — Intercom does not filter events by company natively in the way product analytics tools do.

## Metadata Types

Intercom supports typed metadata values on events:

| Type | Format | Example |
|---|---|---|
| String | JSON string (max 255 chars) | `"source": "desktop"` |
| Number | JSON number | `"load": 3.67` |
| Date | Key ending in `_date`, value is Unix timestamp | `"contact_date": 1392036272` |
| Link | HTTP/HTTPS URL | `"article": "https://example.org/ab1de.html"` |
| Rich Link | Object with `url` and `value` keys | `"article": {"url": "https://example.org/ab1de.html", "value": "the dude abides"}` |
| Monetary Amount | Object with `amount` (cents) and `currency` | `"price": {"amount": 34999, "currency": "eur"}` |

Nested JSON structures beyond Rich Link and Monetary Amount are **not supported**.

## Account Traits That Matter

Intercom uses company attributes for segmentation, message targeting, and reporting. Keep these up to date:

| Trait | Why | Type |
|---|---|---|
| `name` | Company identification in Intercom UI | string |
| `plan` | Plan-based segmentation and targeting | string |
| `monthly_spend` | Revenue tracking (whole integers only, max 2,147,483,647) | integer |
| `size` | Employee count for size-based targeting | integer |
| `industry` | Segmentation | string |
| `remote_created_at` | Cohort analysis | Unix timestamp |
| `custom_attributes.mrr` | Revenue-weighted segmentation | number |
| `custom_attributes.is_paying` | Payment status filtering | boolean |

## Required Fields

| Method | Required Fields | Notes |
|---|---|---|
| Create contact | `role` (`user` or `lead`) | `external_id` or `email` strongly recommended |
| Update contact | Intercom `id` (path param) | Use `external_id` to look up first if needed |
| Create/update company | `company_id` | `name` strongly recommended; `company_id` cannot be changed after creation |
| Attach contact to company | Contact `id`, company `id` | Both must be Intercom-assigned IDs (not external IDs) |
| Track event | `event_name`, `created_at` | Plus one of: `user_id`, `email`, or `id` (Intercom contact ID) |

## Limits

| Constraint | Value |
|---|---|
| API rate limit (per app) | 10,000 requests/minute |
| API rate limit (per workspace) | 25,000 requests/minute (cumulative across apps) |
| Rate limit window | Distributed in 10-second intervals |
| Event metadata keys | 10 per event (first 10 by send order) |
| Event metadata string values | 255 characters max |
| Custom attributes per contact/company | 250 active (soft limit; archive unused to free space) |
| Custom attribute key length | 190 characters max |
| Custom attribute value (string) | 255 characters max |
| `monthly_spend` max | 2,147,483,647 (signed 32-bit integer) |
| Browser `update` calls | 20 per user per 30-minute window |
| Event metadata keys once set | Cannot be changed; create new event instead |

## Common Pitfalls

1. **Metadata keys are locked after first send** — Once an event is sent with specific metadata keys, those keys cannot be changed for that event name. If you need different keys, you must create a new event with a new name and archive the old one. Plan your metadata schema carefully before sending events to production.

2. **Events do not attach to companies** — Unlike product analytics tools where `group()` context flows to subsequent `track()` calls, Intercom events belong to contacts only. Company attribution is inferred through the user-company association. If you need to filter events by company, include `company_id` in metadata as a workaround.

3. **`company_id` is immutable** — The `company_id` field cannot be updated after a company is created. Use a stable, unique identifier (like a database primary key) from the start. If you set it to a temporary value, you'll need to delete and recreate the company.

4. **Companies are invisible without contacts** — A company created via the REST API will not appear in Intercom's UI until at least one contact is associated with it. Always attach contacts to companies after creating them server-side.

5. **Browser `update` throttling** — The `Intercom('update')` method is limited to 20 calls per user per 30-minute window. Excessive calls are silently dropped. Batch attribute changes into fewer `update` calls rather than calling it on every state change.

6. **No nested JSON in event metadata** — Intercom does not support nested JSON structures in metadata (except the specific Rich Link and Monetary Amount formats). Flatten nested objects into top-level keys or stringify them before sending.

7. **`created_at` is critical for de-duplication** — Events are de-duplicated by workspace + contact + event name + `created_at` timestamp. Always send a second-granularity Unix timestamp. Omitting or reusing timestamps causes events to be silently dropped as duplicates.

8. **API events do not trigger Banners or Carousels** — Events sent via the REST API cannot trigger Banner or Carousel message types. Only events from the JavaScript Messenger SDK or mobile SDKs can trigger these. Use the browser SDK for events that should trigger in-app messages.

## Debugging

**Browser:** The Intercom Messenger exposes events in the browser console. Open DevTools Network tab and filter for requests to `api-iam.intercom.io` or `widget.intercom.io`. Inspect outgoing POST payloads to verify user IDs and event metadata.

**HTTP response codes:**
- `202` — Event accepted (empty body)
- `200` — Contact/company created or updated successfully
- `400` — Bad request (check payload format)
- `401` — Invalid or missing access token
- `403` — Token lacks required permissions
- `404` — Contact/user not found (for events sent to non-existent users)
- `429` — Rate limited (check `X-RateLimit-Remaining` header)
- `500` — Server error

**Rate limit headers:** Every API response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers. Monitor `X-RateLimit-Remaining` to avoid 429 errors.

**Node.js error handling:**
```typescript
try {
  await client.events.create({
    eventName: 'report_created',
    userId: 'usr_123',
    createdAt: Math.floor(Date.now() / 1000),
    metadata: { report_id: 'rpt_789' },
  });
} catch (error) {
  if (error instanceof IntercomError) {
    console.error('[Intercom] Event failed:', error.statusCode, error.message);
  }
}
```

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Intercom's official documentation:

- **REST API Reference:** https://developers.intercom.com/docs/references/rest-api/api.intercom.io
- **Data Events API:** https://developers.intercom.com/docs/references/rest-api/api.intercom.io/data-events/createdataevent
- **Contacts API:** https://developers.intercom.com/docs/references/rest-api/api.intercom.io/contacts
- **Companies API:** https://developers.intercom.com/docs/references/rest-api/api.intercom.io/companies
- **JavaScript API Installation:** https://www.intercom.com/help/en/articles/170-install-intercom-in-your-product
- **Event Tracking Setup:** https://www.intercom.com/help/en/articles/175-set-up-event-tracking-in-intercom
- **Custom Data Attributes:** https://www.intercom.com/help/en/articles/179-send-custom-user-attributes-to-intercom
- **Messenger JS SDK (npm):** https://www.npmjs.com/package/@intercom/messenger-js-sdk
- **Node.js SDK (npm):** https://www.npmjs.com/package/intercom-client
- **Node.js SDK (GitHub):** https://github.com/intercom/intercom-node
- **Identity Verification:** https://www.intercom.com/help/en/articles/183-set-up-identity-verification-for-web-and-mobile
