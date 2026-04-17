---
title: "Forum-Derived Top Questions (Video SDK)"
---

# Forum-Derived Top Questions (Video SDK)

Use this as a checklist of what developers repeatedly ask about the **Zoom Video SDK**.

## Fast Routing Questions (Ask First)

- Platform: **Web** vs **React Native** vs **Flutter** vs **Linux**
- UI style: **UI Toolkit** vs **Custom UI**
- What you are building: 1:1 call, group session, audio-only room, screen share, recording, etc.
- Inputs you have: `sdkKey`, `sdkSecret` (server only), `topic`, `userName`, `password`, signature

## Signatures (Common Failure Point)

- Signatures must be generated server-side (do not ship `sdkSecret` to clients).
- Confirm signature expiry and clock skew if joins fail.

## Lifecycle Ordering (Very Common Bug)

Developers frequently call APIs out of order.

Required order:
1. `client = ZoomVideo.createClient()`
2. `await client.init(...)`
3. `await client.join(...)`
4. `stream = client.getMediaStream()` (only after join)
5. `await stream.startVideo()` / `await stream.startAudio()`

## Rendering and Events

Common asks:
- “Why is remote video not showing?”
- “How do I render self-view / peer video?”

Answer pattern:
- Emphasize event-driven rendering (listen for `user-added`, `peer-video-state-change`, etc.)
- Prefer `attachVideo()` / `detachVideo()` where supported (Web)

## UI Toolkit Questions

Common asks:
- retrieving errors/logs from UI Toolkit
- capturing images/snapshots in Toolkit
- detecting screen sharing when using Toolkit

Answer pattern:
- Confirm the UI Toolkit version + SDK version
- Clarify which surfaces the Toolkit abstracts vs what requires underlying SDK APIs

## React Native / Flutter

Common asks:
- permissions (camera/mic)
- native build issues
- background/foreground behavior
- audio routing and device disconnects

Answer pattern:
- Ask for platform version + SDK wrapper version
- Ask for minimal reproduction steps and logs

