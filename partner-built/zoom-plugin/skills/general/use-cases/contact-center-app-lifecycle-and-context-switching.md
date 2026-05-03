# Contact Center App Lifecycle and Context Switching

Build a Contact Center app that survives engagement switching without losing in-progress work.

## Skills Needed

- `contact-center`
- `zoom-apps-sdk`
- `zoom-oauth` (if backend identity mapping is required)

## Problem

Agents can switch between active engagements. Your app instance may remain alive while visible context changes. If state is global rather than engagement-scoped, data corruption and agent frustration follow.

## Recommended Pattern

1. Configure SDK with engagement capabilities.
2. Query initial context and status.
3. Subscribe to engagement context and status change events.
4. Store drafts and workflow state by `engagementId`.
5. On context switch, load the target engagement state.
6. On end state, finalize or clear that engagement data.

## Failure Modes To Avoid

- Single shared draft object for all engagements.
- Late event subscription after user interaction starts.
- Hard cleanup on tab switch instead of engagement end.
- Assuming visibility equals process lifetime.

## Implementation References

- `../../contact-center/web/examples/app-context-and-state.md`
- `../../contact-center/concepts/architecture-and-lifecycle.md`
- `../../contact-center/RUNBOOK.md`

