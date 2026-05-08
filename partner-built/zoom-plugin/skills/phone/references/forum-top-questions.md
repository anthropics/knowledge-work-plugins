---
title: "Forum-Derived Top Questions (Phone)"
---

# Forum-Derived Top Questions (Phone)

Use this as a checklist of the most common recent Developer Forum asks for Zoom Phone integrations.

## Fast Routing Questions (Ask First)

- Integration surface: Smart Embed, Phone REST API, webhooks, or URI launch (`zoomphonecall://`, `zoomphonesms://`).
- App/auth type: Server-to-Server OAuth vs user OAuth, and who the token is acting as.
- Account posture: Zoom Phone license assigned, user enabled, admin permissions, site/queue scope.
- Exact failure: HTTP status + Zoom `code`/`message` + endpoint/event name + sample payload.
- Correlation IDs available: `call_id`, `call_history_uuid`, `call_element_id`, recording ID.

## Smart Embed Sign-In or Calling Fails

Common asks:
- Smart Embed shows login but never completes.
- Widget loads, but outbound/inbound calling does not work.
- `zp-make-call`/search-and-match behaviors are inconsistent.

Answer pattern:
- Confirm approved Smart Embed domain matches the real runtime origin exactly.
- Confirm `origin` parameter is domain-level where required and not path-mismatched.
- Verify Zoom client sign-in state and account licensing prerequisites.
- Add strict `postMessage` origin handling and validate event init sequence.

## `call_logs` to `call_history` Migration Gaps

Common asks:
- Missing fields after migrating to `call_history`.
- Existing call analytics pipelines break after deprecation migration.

Answer pattern:
- Treat migration as a schema migration, not a drop-in endpoint swap.
- Build a mapping layer from legacy fields to current call history/call element fields.
- Persist both legacy and new IDs during transition for reconciliation.
- Update downstream reports that assumed removed fields.

## Recording and Download URL Auth Errors

Common asks:
- `download_url` returns 401/403.
- `Invalid access token, does not contain scopes` on recordings/transcripts.

Answer pattern:
- Generate a fresh token from the app that owns the needed scopes.
- Re-authorize after scope changes; verify token scope set, not just app config.
- Handle redirects while preserving auth headers where needed.
- Keep a fallback retry path for temporary scope/permission regressions.

## "Zoom Phone Has Not Been Enabled" (`2013`/`2031`)

Common asks:
- Token works for some APIs/users but Phone endpoints return not enabled.

Answer pattern:
- Verify `account_id` is present in S2S token request and token is from expected account.
- Verify target users actually have Zoom Phone entitlement.
- Verify caller/admin context has permission for account-level Phone resources.
- Re-test with one known-good licensed admin and one known-good licensed user.

## Webhooks: Missing Events or Duplicates

Common asks:
- Expected call events not received.
- Missed-call events delivered more than once.

Answer pattern:
- Acknowledge webhooks quickly with `200`/`204` and process asynchronously.
- Implement idempotency keyed by event ID/call identifiers.
- Expect retries and occasional ordering variance.
- Validate event subscription scope and verify webhook logs before blaming delivery.

## Correlating Calls Across APIs and Events

Common asks:
- Hard to tie recordings, call path/history, and webhook events to one interaction.

Answer pattern:
- Persist all call identifiers emitted at each lifecycle phase.
- Build a correlation table keyed by your internal interaction ID.
- Do not rely on a single identifier across all endpoints.

## Pagination and Incomplete Result Sets

Common asks:
- `/phone/users` or call list endpoints appear to miss records.

Answer pattern:
- Always iterate `next_page_token` until exhausted.
- Keep query filters stable between page requests.
- Add dedupe + page-audit logging to detect loops or repeated pages.
