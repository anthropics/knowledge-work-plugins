# Smart Embed Event Contract

## Core initialization and command messages

- `zp-init-config`
- `zp-make-call`
- `zp-input-sms`
- `zp-contact-search-response`
- `zp-contact-match-response`

## Core emitted event types

- `zp-call-ringing-event`
- `zp-call-connected-event`
- `zp-call-ended-event`
- `zp-call-log-completed-event`
- `zp-call-recording-completed-event`
- `zp-call-voicemail-received-event`
- `zp-ai-call-summary-event`
- `zp-sms-log-event`
- `zp-save-log-event`
- `zp-contact-search-event`
- `zp-contact-match-event`
- `zp-notes-save-event`

## Field-level reliability notes

- `callId` appears early in lifecycle.
- `callLogId` appears in completion-oriented events.
- `event.id` can be used for deduplication/idempotency.
- Additional flags can appear (for example `enableAutoLog` behavior fields).

## Security and resilience

- Validate `event.origin === https://applications.zoom.us`.
- Keep a permissive parser for new optional fields.
- Route unknown event types into structured logs, not hard failures.
