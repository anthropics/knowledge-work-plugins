---
name: build-zoom-phone-integration
description: "Reference skill for Zoom Phone. Use after routing to a phone workflow when implementing OAuth, Phone APIs, webhooks, Smart Embed events, URI schemes, CRM or CTI dialers, or call handling automation."
triggers:
  - "zoom phone"
  - "phone smart embed"
  - "zoom phone api"
  - "zoom phone webhook"
  - "call history"
  - "call handling"
  - "zoomphonecall"
  - "zoomphonesms"
  - "phone crm integration"
  - "call element"
---

# /build-zoom-phone-integration

Background reference for Zoom Phone integrations across API, webhook, Smart Embed, and URI-launch workflows.

Implementation guidance for Zoom Phone integrations across API, webhook/event, Smart Embed, and URI-launch workflows.

Official docs:
- https://developers.zoom.us/docs/phone/
- CRM sample reference: https://github.com/zoom/CRM-Sample

## Routing Guardrail

- If the user needs embedded softphone behavior in a web app, use Smart Embed ([examples/smart-embed-postmessage-bridge.md](examples/smart-embed-postmessage-bridge.md)).
- If the user needs call records, analytics, or automation, use Phone REST API and webhooks ([references/deprecations-and-migrations.md](references/deprecations-and-migrations.md)).
- If the user needs click-to-dial/SMS launch from external UI, use URI schemes (`zoomphonecall://`, `zoomphonesms://`).
- If the user mixes Zoom Phone and Contact Center, chain with [../contact-center/SKILL.md](../contact-center/SKILL.md).

## Quick Links

Start here:
1. [concepts/architecture-and-lifecycle.md](concepts/architecture-and-lifecycle.md)
2. [scenarios/high-level-scenarios.md](scenarios/high-level-scenarios.md)
3. [references/deprecations-and-migrations.md](references/deprecations-and-migrations.md)
4. [references/forum-top-questions.md](references/forum-top-questions.md)
5. [references/smart-embed-event-contract.md](references/smart-embed-event-contract.md)
6. [references/call-handling-patterns.md](references/call-handling-patterns.md)
7. [references/environment-variables.md](references/environment-variables.md)
8. [references/crm-sample-validation.md](references/crm-sample-validation.md)
9. [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
10. [RUNBOOK.md](RUNBOOK.md)
11. [examples/smart-embed-postmessage-bridge.md](examples/smart-embed-postmessage-bridge.md)
12. [examples/phone-api-service-pattern.md](examples/phone-api-service-pattern.md)
13. [references/source-map.md](references/source-map.md)

## Common Lifecycle Pattern

1. Provision account prerequisites (Zoom Phone license, admin setup, SMS readiness).
2. Create OAuth app and scopes in Marketplace.
3. Choose integration surface:
- Smart Embed (iframe + postMessage)
- REST + webhooks
- URI launch (`callto`, `tel`, `zoomphonecall`, `zoomphonesms`)
4. Capture real-time events (Smart Embed events and/or webhooks).
5. Persist call identifiers and correlate records (`call_id`, `call_history_uuid`, `call_element_id`).
6. Apply migration-safe data mapping (v1 -> v2 -> v3) and handle renamed fields.
7. Harden security (origin validation, webhook signature validation, least-privilege scopes).

## High-Level Scenarios

- CRM softphone pane using Smart Embed + contact search/match callbacks.
- Click-to-call from account/contact table via `zp-make-call`.
- Call disposition workflow using `zp-save-log-event` and custom notes page.
- SMS engagement workflow with `zoomphonesms://` and `zp-sms-log-event`.
- Real-time operational board driven by `phone.*` webhook events.
- Call analytics migration from legacy call logs to call history/call elements.
- Admin automation for user/auto-receptionist/call-queue call-handling settings.

See [scenarios/high-level-scenarios.md](scenarios/high-level-scenarios.md) for details.

## Chaining

- OAuth setup/token lifecycle: [../oauth/SKILL.md](../oauth/SKILL.md)
- Phone and account resources via REST: [../rest-api/SKILL.md](../rest-api/SKILL.md)
- Event delivery and signature validation: [../webhooks/SKILL.md](../webhooks/SKILL.md)
- Contact Center blended journey: [../contact-center/SKILL.md](../contact-center/SKILL.md)

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.
