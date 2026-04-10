# Connectors

This plugin works best with access to your development environment.

## ~~code — Source Control

| Tool | Purpose |
|------|---------|
| GitHub | Codebase scanning, PR context |
| GitLab | Same as GitHub |
| Bitbucket | Same as GitHub |

Used by: the **product-tracking-audit-current-tracking** skill for codebase scanning, the **product-tracking-model-product** skill for product shape inference.

## ~~docs — Product Specs

| Tool | Purpose |
|------|---------|
| Notion | Feature specs, product docs |
| Confluence | Enterprise documentation |
| Linear | Issue context, feature specs |
| Jira | Same as Linear |

Used by: the **product-tracking-model-product** skill for product context, the **product-tracking-instrument-new-feature** skill for feature specs.

## Analytics SDKs

Code generation supports these platforms:

| Platform | Browser | Node.js | Notes |
|----------|---------|---------|-------|
| Segment | `@segment/analytics-next` | `@segment/analytics-node` | Multi-destination routing |
| Amplitude | `@amplitude/analytics-browser` | `@amplitude/analytics-node` | Behavioral analytics |
| Mixpanel | `mixpanel-browser` | `mixpanel` | Funnel/cohort analysis |
| PostHog | `posthog-js` | `posthog-node` | Open-source, feature flags |
| Accoil | `tracker.js` (CDN) | Direct API (`in.accoil.com`) | B2B engagement scoring; also via Segment |
| Intercom | `@intercom/messenger-js-sdk` | `intercom-client` | Customer engagement, messaging, event tracking |
| RudderStack | `@rudderstack/analytics-js` | `@rudderstack/rudder-sdk-node` | Open-source CDP |

Used by: the **product-tracking-implement-tracking** skill for code generation, the **product-tracking-audit-current-tracking** skill for SDK detection.

## Common Case

Most users work within a code repository. The plugin presumes this context — it scans routes, models, and tracking calls directly from the filesystem. No API keys or OAuth required.

## No External Data Dependencies

This plugin does not connect to analytics platforms to read events. It works entirely from tracking plans and codebase analysis. It plans and implements telemetry — it does not analyze it.
