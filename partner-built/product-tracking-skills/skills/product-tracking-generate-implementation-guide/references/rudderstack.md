<!-- Last verified: 2026-03-10 against RudderStack docs -->
# RudderStack Implementation Guide

## Overview

RudderStack is an open-source customer data platform (CDP) that routes events to downstream destinations. Its API is Segment-compatible — the same identify/group/track model — so switching between them requires minimal code changes.

## Installation

**npm (recommended for SPAs):**
```bash
npm install @rudderstack/analytics-js
```

**CDN snippet (traditional websites):**

Add to `<head>`. Replace `WRITE_KEY` and `DATA_PLANE_URL` from your RudderStack source dashboard. The recommended approach is to copy the snippet directly from your RudderStack dashboard (Sources > JavaScript > Setup), which includes your write key and data plane URL pre-filled.

> **Note:** SDK v3 uses a new CDN URL pattern (`cdn.rudderlabs.com/v3/[modern|legacy]/rsa.min.js`) and a substantially different snippet than v1.1. The snippet below is the current v3 pattern. The SDK auto-detects browser capabilities and loads the appropriate modern or legacy bundle.

```html
<script type="text/javascript">
!function(){"use strict";
  var e,n,s,o,i,a,r,c,l,d,t="rudderanalytics";
  if(window[t]||(window[t]=[]),e=window[t],!Array.isArray(e))return;
  if(e.snippetExecuted===!0){window.console&&console.error("RudderStack JavaScript SDK snippet included more than once.");return}
  e.snippetExecuted=!0;
  window.rudderAnalyticsBuildType="legacy";
  c="https://cdn.rudderlabs.com/v3";
  l="rsa.min.js";
  i=["setDefaultInstanceKey","load","ready","page","track","identify","alias","group","reset",
     "setAnonymousId","startSession","endSession","consent"];
  for(n=0;n<i.length;n++)a=i[n],e[a]=function(n){return function(){
    if(Array.isArray(window[t]))e.push([n].concat(Array.prototype.slice.call(arguments)));
    else{var s;(s=window[t][n])===null||s===void 0||s.apply(window[t],arguments)}
  }}(a);
  try{new Function('class Test{field=()=>{};test({prop=[]}={}){return prop?(prop?.property??[...prop]):import("");}}');
    window.rudderAnalyticsBuildType="modern"}catch(x){}
  s=document.head||document.getElementsByTagName("head")[0];
  r=document.body||document.getElementsByTagName("body")[0];
  window.rudderAnalyticsAddScript=function(e,t,n){
    var i=document.createElement("script");i.src=e;i.setAttribute("data-loader","RS_JS_SDK");
    t&&n&&i.setAttribute(t,n);i.async=!0;
    s?s.insertBefore(i,s.firstChild):r.insertBefore(i,r.firstChild);
  };
  window.rudderAnalyticsMount=function(){
    window.rudderAnalyticsAddScript("".concat(c,"/").concat(window.rudderAnalyticsBuildType,"/").concat(l),"data-rsa-write-key","WRITE_KEY");
  };
  typeof Promise=="undefined"||typeof globalThis=="undefined"
    ?window.rudderAnalyticsAddScript("https://polyfill-fastly.io/v3/polyfill.min.js?version=3.111.0&features=Symbol%2CPromise&callback=rudderAnalyticsMount")
    :window.rudderAnalyticsMount();
  e.load("WRITE_KEY","DATA_PLANE_URL");
}();
</script>
```

> **Important (v3 change):** The implicit `page()` call at the end of the snippet (present in v1.1) has been removed in SDK v3. If you need automatic page tracking, either call `page()` explicitly or enable `autoTrack.pageLifecycle` in the load options.

## Initialization (npm)

```typescript
import { RudderAnalytics } from '@rudderstack/analytics-js';

const analytics = new RudderAnalytics();
analytics.load('WRITE_KEY', 'DATA_PLANE_URL');
```

## Core Flow: Identify, Group, Track

### 1. Identify the User

Call on login or signup, once the user ID is known.

```typescript
analytics.identify('usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  role: 'admin',
  plan: 'pro'
});
```

This ties all future events from this browser to the identified user.

### 2. Associate User with a Group

For B2B, always call `group()` after `identify()` to establish account context.

```typescript
analytics.group('acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise',
  employee_count: 50
});
```

For hierarchical products, issue a `group()` call for **every level** in the hierarchy, with `parent_group_id` to establish relationships:

```typescript
// Account (top level)
analytics.group('acc_456', {
  name: 'Acme Corp',
  group_type: 'account',
  plan: 'enterprise'
});

// Workspace (child of account)
analytics.group('ws_789', {
  name: 'Engineering',
  group_type: 'workspace',
  parent_group_id: 'acc_456'
});

// Project (child of workspace)
analytics.group('proj_123', {
  name: 'Q1 Release',
  group_type: 'project',
  parent_group_id: 'ws_789'
});
```

### 3. Track Events

```typescript
analytics.track('report.created', {
  report_id: 'rpt_789',
  report_type: 'standard'
});
```

The SDK automatically attaches the identified user. You do not need to pass `userId` in the browser.

### 4. Reset on Logout

```typescript
analytics.reset();  // Clears userId, traits, and group associations
```

## Group Context on Track Calls

<!-- UNVERIFIED: The exact auto-attachment behavior of groupId to track calls after a group() call varies across SDK versions and is not fully documented. The JS SDK may include group traits in context automatically, but explicit groupId on track calls is the most reliable approach for downstream attribution. -->

After calling `group()`, the JavaScript SDK persists group traits and may include them in the `context` of subsequent calls. However, for **explicit and reliable group attribution** on track events -- especially when working with multiple groups or hierarchies -- include `groupId` directly in the track call's `context` object:

```typescript
// Project-level event
analytics.track('task.completed', {
  task_id: 'task_456'
}, {
  context: { groupId: 'proj_123' }
});

// Account-level event
analytics.track('plan.upgraded', {
  from_plan: 'free',
  to_plan: 'pro'
}, {
  context: { groupId: 'acc_456' }
});
```

**Critical limitation:** RudderStack has no native group hierarchy support. The `context.groupId` is what downstream tools (Accoil, Amplitude, Mixpanel) use for event-level group attribution. Hierarchical rollups depend on the downstream tool supporting `parent_group_id` traits on group calls.

## Node.js (Server-Side)

```typescript
import Analytics from '@rudderstack/rudder-sdk-node';

const analytics = new Analytics('WRITE_KEY', {
  dataPlaneUrl: 'DATA_PLANE_URL'
});

// Server-side requires userId on every call
analytics.identify({
  userId: 'usr_123',
  traits: {
    email: 'jane@example.com',
    plan: 'pro'
  }
});

analytics.group({
  userId: 'usr_123',
  groupId: 'acc_456',
  traits: {
    name: 'Acme Corp',
    plan: 'enterprise'
  }
});

analytics.track({
  userId: 'usr_123',
  event: 'report.created',
  properties: {
    report_id: 'rpt_789',
    report_type: 'standard'
  },
  context: { groupId: 'acc_456' }
});
```

## Verifying Events

1. Go to your Source in the RudderStack dashboard
2. Open the **Live Events** debugger
3. Trigger actions in your app and confirm `identify`, `group`, and `track` events appear with correct payloads

## Common Pitfalls

1. **Calling track before identify** -- Events are anonymous until identify is called
2. **Forgetting reset on logout** -- Previous user context persists for the next user
3. **Missing group() calls** -- Downstream B2B tools lose account-level attribution
4. **Server-side without userId** -- Unlike the browser SDK, there is no implicit user context
5. **Assuming group context carries to track** -- For reliable attribution, always pass `context.groupId` explicitly on each track call

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult RudderStack's official documentation:

- **Getting Started:** https://www.rudderstack.com/docs/get-started/
- **JavaScript SDK:** https://www.rudderstack.com/docs/sources/event-streams/sdks/rudderstack-javascript-sdk/
- **Node.js SDK:** https://www.rudderstack.com/docs/sources/event-streams/sdks/rudderstack-node-sdk/
- **Identify:** https://www.rudderstack.com/docs/event-spec/standard-events/identify/
- **Group:** https://www.rudderstack.com/docs/event-spec/standard-events/group/
- **Track:** https://www.rudderstack.com/docs/event-spec/standard-events/track/
- **Destinations:** https://www.rudderstack.com/docs/destinations/
- **HTTP API:** https://www.rudderstack.com/docs/api/http-api/
- **Transformations:** https://www.rudderstack.com/docs/transformations/overview/
