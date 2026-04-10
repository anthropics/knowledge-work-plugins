# Glossary

Common terms used in product telemetry.

## Core Concepts

### Event
A record of something that happened. Has a name, timestamp, and properties.

**Example:** `report.created` at 2024-02-07T10:30:00Z with `{ report_id: "rpt_123" }`

### Property
A key-value pair attached to an event. Provides context.

**Types:**
- **Event properties:** Specific to this event
- **User properties:** Persist across events for a user
- **Account/Group properties:** Persist for an account

### Trait
A stable, enduring attribute of a user or account that persists across events and sessions. Unlike events and properties, which capture moment-to-moment actions and context, traits represent more static characteristics that build a comprehensive entity profile over time. Set via `identify()` or `group()`.

Traits are critical for segmentation, personalization, and targeted communication. They change infrequently compared to event data.

**User trait examples:** `email`, `name`, `role`, `subscription_level`, `preferred_language`, `signup_date`
**Account trait examples:** `name`, `plan`, `industry`, `employee_count`, `billing_cycle`, `support_level`

**Example:** `{ plan: "pro", industry: "technology" }`

### Tracking Plan
The canonical document defining all events, properties, and entities. Source of truth.

### Instrumentation
The code that captures and sends events. Implementation of the tracking plan.

## User Identity

### User ID
A unique, persistent identifier for a user. Should be stable across sessions.

**Good:** `usr_abc123`, database ID
**Bad:** email (can change), session ID (not persistent)

### Anonymous ID
A temporary identifier for users before they're identified. Usually a random UUID.

### Identify
The act of associating an anonymous ID with a known user ID. Usually happens on signup or login.

```javascript
analytics.identify('usr_123', { email: 'jane@example.com' });
```

### Group / Account
In B2B, the organization a user belongs to. Set via `group()`.

```javascript
analytics.group('acc_456', { name: 'Acme Corp' });
```

## Event Categories

### Lifecycle Events
Events tracking user/account journey: signup, activation, churn.

### Core Value Events
Events representing your product's primary value delivery.

### Collaboration Events
Events involving multiple users: invites, shares, comments.

### Configuration Events
Events about setup and settings: integrations, preferences.

### Billing Events
Events with commercial signals: trials, upgrades, limits.

### Navigation Events
Events about product navigation: page views, feature access.

## Platforms

### CDP (Customer Data Platform)
A platform that collects, unifies, and routes customer data. Examples: Segment, RudderStack.

### Analytics Platform
A platform for analyzing user behavior. Examples: Amplitude, Mixpanel, Accoil.

### Data Warehouse
A database optimized for analytical queries. Examples: BigQuery, Snowflake.

## SDK Methods

### track()
Records an event.

```javascript
analytics.track('report.created', { report_id: 'rpt_123' });
```

### identify()
Associates a user with traits.

```javascript
analytics.identify('usr_123', { email: 'jane@example.com' });
```

### group()
Associates a user with an account/organization.

```javascript
analytics.group('acc_456', { name: 'Acme Corp' });
```

### page()
Records a page view (web).

```javascript
analytics.page('Dashboard');
```

### screen()
Records a screen view (mobile).

```javascript
analytics.screen('Dashboard');
```

### alias()
Links two user identities (rare, for advanced identity resolution).

## Quality Terms

### PII (Personally Identifiable Information)
Data that can identify an individual: email, name, phone, IP address.

**Rule:** PII goes in user traits, not event properties.

### Orphan Event
An event in code that isn't in the tracking plan.

### Missing Event
An event in the tracking plan that isn't implemented in code.

### Malformed Event
An event with incorrect properties, types, or naming.

## Metrics (Derived from Events)

### Activation Rate
Percentage of users who complete activation event.

### Retention
Users who return after a time period.

### DAU/WAU/MAU
Daily/Weekly/Monthly Active Users.

### Feature Adoption
Percentage of users who use a specific feature.

**Note:** These are metrics derived from events. We track events, not metrics.
