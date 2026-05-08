# Zoom Phone Source Map

Crawled docs source:
- `https://developers.zoom.us/docs/phone/`
- Crawl config used: depth `10`, concurrency `10`, Android excluded.

## Processed pages

- `call-data.md`
- `call-handling.md`
- `create-app.md`
- `first-app.md`
- `integrate-with-zoom-phone.md`
- `migrate.md`
- `outbound-call.md`
- `outbound-sms.md`
- `smart-embed-guide.md`
- `smart-embed.md`
- `start.md`
- `webhook-migrate.md`

## Mapping to skill docs

- App setup + OAuth -> [../SKILL.md](../SKILL.md), [environment-variables.md](environment-variables.md)
- Smart Embed lifecycle/events -> `examples/smart-embed-postmessage-bridge.md`, `references/smart-embed-event-contract.md`
- Call handling admin API -> `references/call-handling-patterns.md`
- API/webhook migration timeline -> `references/deprecations-and-migrations.md`
- CRM sample validation -> `references/crm-sample-validation.md`
