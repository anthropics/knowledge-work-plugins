---
title: "Video SDK Session Lifecycle (Join, Stream, Render, Leave)"
---

# Video SDK Session Lifecycle (Join, Stream, Render, Leave)

Many “video not showing” and “audio not starting” threads are caused by calling APIs out of order.

## Canonical Order

1. Create client
2. `init`
3. `join`
4. Get stream (`getMediaStream`) after join
5. Start audio/video and render based on events
6. Leave session and cleanup

## Common Gotcha: `getMediaStream()` Timing

On Web, `client.getMediaStream()` is only valid after `join`.

## Rendering Is Event-Driven

Make sure you:

- listen for join/leave events
- listen for peer video state changes
- attach/detach video elements when peers start/stop video

## UI Toolkit Notes

If using UI Toolkit:

- let Toolkit manage most lifecycle/rendering
- when you need something “custom” (e.g., snapshot, screen-share detection), confirm whether Toolkit exposes that or whether you must use underlying SDK APIs

