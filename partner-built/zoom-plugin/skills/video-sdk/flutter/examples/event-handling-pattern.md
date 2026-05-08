# Event Handling Pattern

Bind the SDK event listener early and route events through one reducer/state manager.

## Pattern

1. Register listener before or immediately after join.
2. Map `EventType` values to handlers.
3. Keep handler side-effects minimal and predictable.

## Typical events to prioritize

- session join/leave
- user join/leave/video/audio status
- share status
- error and subscribe-fail events
- chat/command channel events

## Minimum realtime media UX checklist

For practical 2-device validation, include these controls and views:

- join / leave session
- local mic mute-unmute
- local video on-off
- camera switch
- speaker toggle
- remote participant video tiles
- event log panel (timestamped)

## Remote media rendering pattern

- On session join, fetch current users and render local preview + remote tiles.
- On `onUserJoin` and `onUserLeave`, refresh participant list and rerender.
- On `onUserVideoStatusChanged` and `onUserAudioStatusChanged`, update UI state from events (avoid optimistic-only state).
- Keep one code path for participant list refresh to avoid state drift.
