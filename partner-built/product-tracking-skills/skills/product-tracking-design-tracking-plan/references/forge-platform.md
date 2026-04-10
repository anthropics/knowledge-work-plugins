# Forge Platform Constraints

Design-time constraints for products running on Atlassian Forge. These supplement — not replace — the standard naming conventions and schema design rules. Everything in `naming-conventions.md`, `event-categories.md`, and `anti-patterns.md` still applies.

## Architecture Awareness for Tracking Plan Design

Forge apps use a **queue-based, privacy-first architecture** where all analytics flow through the backend:

```
Frontend Events --> invoke() --> Backend Resolver --> Queue --> Consumer --> Analytics Provider
                                                       ^
                                   Backend Events -----+
```

**Key constraint:** Forge Custom UI frontends run in a sandboxed iframe and **cannot make direct network calls** to external services. Every analytics event — whether triggered by a UI interaction or backend business logic — must route through backend resolvers using `invoke()` from `@forge/bridge`. This is not a design choice; it is a hard platform constraint.

This affects tracking plan design in three ways:

1. **Event origin matters.** When designing events, consider whether each event will be triggered from the frontend (UI interaction) or backend (business logic). Backend-triggered events are simpler — they call tracking functions directly from resolvers. Frontend-triggered events require the `invoke()` bridge, so only design frontend events for UI-only actions that don't already route through a backend resolver.

2. **Zero properties from the frontend.** The frontend sends only the event name. All properties, identity, and group context are added server-side from the Forge context object. Design event properties assuming they will be populated from backend data, not from the UI layer.

3. **Scheduled events for snapshot metrics.** Instance-level metrics (license status, usage counts, domain) are collected by a daily scheduled trigger, not attached to individual events. Design group traits knowing they will be refreshed on a daily cadence via a separate scheduled call.

## cloudId Is the Top-Level Group ID

Non-negotiable. The Forge `cloudId` (Atlassian instance identifier) must be used as the top-level group ID in every `group()` call.

Why: cloudId is the key that enables matching analytics data against Atlassian Marketplace billing and revenue data. Without it, you cannot connect product usage to commercial outcomes.

```yaml
groups:
  - type: instance
    id_source: context.cloudId
    is_top_level: true
    traits: [domain, license_type, license_status]
```

## Group Traits Must Include Domain

The `domain` trait (e.g., `acme.atlassian.net`) serves as the human-readable instance name alongside the opaque cloudId. Always include it in group traits.

Additional high-value group traits from Forge context:
- `license_type` — active, inactive, evaluation
- `license_status` — `context.license.isActive`, `context.license.isEvaluation`
- `last_daily_sync` — timestamp from scheduled analytics

### Atlassian Marketplace Traits

Group calls should include company name, site hostname, and license type so free-license installs are trackable before the Marketplace connector kicks in. When a user upgrades, the Marketplace connector sends updated values for the same keys — the data lines up automatically.

**When the destination is Accoil**, use the `am.*` prefixed trait names. These align with the Atlassian Marketplace connector built into Accoil:

| Trait | Source | Example |
|---|---|---|
| `am.contactdetails.company` | Subdomain from `context.siteUrl` | `acme` |
| `am.cloudsitehostname` | `context.siteUrl` | `acme.atlassian.net` |
| `am.licensetype` | Derived from `context.license` | `FREE`, `evaluation`, `paid` |

**When the destination is not Accoil**, use standard trait names instead (`company`, `domain`, `license_type`). The `am.*` prefix is Accoil-specific and has no meaning in other providers.

## Event Origin: Frontend vs Backend

When designing events for a Forge app, classify each event by its trigger origin. This determines how it will be implemented.

**Backend-triggered events** (preferred when possible):
- Events that correspond to business logic already handled by a resolver (create, update, delete operations)
- The resolver already has the Forge context, so tracking is a direct function call
- Example: `form.created`, `todo.deleted`, `settings.updated`

**Frontend-triggered events** (only when necessary):
- UI-only interactions that do not already have a resolver: search, filter, navigation, tab switches, expand/collapse
- These require the `invoke()` bridge and a dedicated `track-event` resolver
- The frontend sends **only the event name** — no properties, no context, no user data
- Example: `search.performed`, `filter.applied`, `export.generated`

**Scheduled events** (for snapshot metrics):
- Instance-level state captured on a daily cadence: license status, usage counts, domain info
- These are group trait updates, not track events
- Example: daily group call with `domain`, `license_type`, `total_form_count`

If a UI action already calls a backend resolver for its primary purpose (e.g., clicking "Create" calls a `create` resolver), the tracking should happen in that resolver — do not add a separate frontend event for it.

## No End User Data in Analytics

Forge apps must declare `inScopeEUD: false` on all analytics egress permissions to maintain "Runs on Atlassian" eligibility. This means analytics payloads must not contain **any** in-scope End User Data — user-generated content, personally identifiable information, or customer business data.

This is stricter than the general "no PII" rule.

**Prohibited (in-scope End User Data):**
- Issue titles, summaries, descriptions
- Page names, space names
- Form content, comments, labels
- Search queries containing user text
- Custom field values
- Any content a human typed

**Allowed (not in-scope EUD):**
- System identifiers (cloudId, accountId, project IDs)
- Site hostname / domain (e.g., `acme.atlassian.net`) — this is instance context, not end user data
- Enumerated values (status, type, category)
- Counts and aggregates (item_count, member_count)
- Boolean states (is_active, has_custom_fields)
- License type and status
- Timestamps

The test: if a human typed it, it cannot leave as analytics data. System-generated identifiers and instance context (site domain, license info) are acceptable.

## Approved Analytics Destinations

Forge enforces an allowlist of pre-approved analytics domains. Only these domains may be used with the `category: analytics` egress permission. Apps declaring unlisted domains will be **blocked from deployment**.

**Requirements for analytics tools:**
- Must be **cloud-only** — self-hosted tools are prohibited (Atlassian cannot verify self-hosted URLs aren't used for functional egress)
- Must have a public website, documentation, and privacy policy
- Must use a recognized fixed domain

**Pre-approved domains (as of August 2025):**

| Provider | Allowed Domains |
|---|---|
| **Accoil** | `in.accoil.com` |
| **Amplitude** | `*.amplitude.com` |
| **Google Analytics** | `*.google-analytics.com` |
| **Google Tag Manager** | `*.googletagmanager.com` |
| **Mixpanel** | `cdn.mxpnl.com`, `*.cdn.mxpnl.com`, `*.mixpanel.com` |
| **PostHog** | `*.posthog.com` |
| **Segment** | `*.cdn.segment.com`, `cdn.segment.com`, `*.api.segment.io` |
| **Sentry** | `*.ingest.sentry.io`, `*.ingest.us.sentry.io`, `*.sentry-cdn.com` |
| **HotJar** | `*.hotjar.io`, `*.hotjar.com` |
| **LaunchDarkly** | `*.launchdarkly.com` |
| **New Relic** | `*.newrelic.com` |
| **Plausible** | `*.plausible.io` |
| **Azure** | `*.applicationinsights.azure.com`, `*.monitor.azure.com` |
| **Cloudflare** | `static.cloudflareinsights.com` |
| **Fathom** | `*.cdn.usefathom.com` |
| **Statsig** | `*.statsigapi.net`, `statsigapi.net`, `*.featureassets.org`, `featureassets.org`, `*.prodregistryv2.org`, `prodregistryv2.org` |
| **UserPilot** | `*.userpilot.io` |
| **Usermaven** | `*.events.usermaven.com`, `*.um.contentstudio.io` |
| **Beam Analytics** | `*.beamanalytics.b-cdn.net` |
| **Microanalytics** | `*.microanalytics.io` |
| **WithCabin** | `*.scripts.withcabin.com` |
| **Simple Analytics** | `*.scripts.simpleanalyticscdn.com` |
| **Journy** | `*.journy.io` |

To request approval for an unlisted tool, raise a support request with Atlassian. RudderStack is **not** on the approved list — if the tracking plan specifies RudderStack as destination for a Forge app, flag this as a constraint and recommend an approved alternative.

## Sub-Level Group Context

When events occur at a level below the instance (project, space, board, form), include the context group ID so analytics can attribute to the correct sub-group.

```yaml
groups:
  - type: instance
    id_source: context.cloudId
    is_top_level: true
  - type: project
    id_source: context.extension.project.id
    parent_type: instance
```

Events at project level should include the project group ID in context. This enables per-project usage analysis without losing the instance-level rollup.

## Public-Facing Apps

For apps with public/portal users (JSM service desks, public forms, customer portals):

- **Do not** track individual anonymous users — this causes MTU explosion
- **Do** group all public users under a composite identifier: `{cloudId}-public-user`
- Keep public traffic analytically separate from licensed user analytics
- Track aggregate metrics (submission_count) rather than individual sessions

```yaml
groups:
  - type: instance
    id_source: context.cloudId
    is_top_level: true
  - type: public_users
    id_source: "{cloudId}-public-user"
    parent_type: instance
```

## Tracking Plan Meta

Add `platform: forge` to the tracking plan meta block so the implementation phase knows to use Forge-specific architecture:

```yaml
meta:
  product: "My Forge App"
  platform: forge
  destinations: [accoil]
```

## Privacy by Design

The Forge analytics architecture guarantees that the analytics provider never sees:
- User IP addresses (only Forge server IPs are visible)
- Internal Jira/Confluence URLs or referrer data
- Browser user agent strings or session data
- Any end user data (issue titles, form inputs, search queries, display names)

When designing a tracking plan, apply the test: **if a human typed it, it cannot leave as analytics data.** Site hostname/domain (e.g., `acme.atlassian.net`) is acceptable as instance context — it is not classified as in-scope End User Data. Design properties around system identifiers, instance context, enumerated values, counts, booleans, and timestamps — never around free-text user input.

## What Stays the Same

Everything else follows standard conventions:
- Event naming: `object.action` in snake_case
- Property naming: snake_case with standard suffixes (`_id`, `_type`, `_count`, `is_*`)
- Category taxonomy: lifecycle, core_value, collaboration, configuration, billing, navigation
- Anti-patterns: all standard anti-patterns apply
- Minimalism: fewer events, richer properties
