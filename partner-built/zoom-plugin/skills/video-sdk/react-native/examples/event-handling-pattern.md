# Event Handling Pattern

Attach listener(s) early and route all event types through a centralized state handler.

## Prioritized events

- session join/leave and error events
- user/video/audio/share status changes
- chat + command channel events
- recording/transcription status events

## Pattern

1. Register listeners once near app/session root.
2. Map event payloads to typed state updates.
3. Keep cleanup to remove listeners on unmount/leave.

## Practical custom UI baseline

For a production-like test surface, implement a single custom session screen with:

- Join / leave actions
- Local controls: mute-unmute, video on-off
- Device controls: camera switch, speaker toggle
- Remote participant video tiles
- Timestamped event log panel

This minimal UI gives fast validation of core media and event paths without relying on sample navigation complexity.
