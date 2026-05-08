---
title: "Zoom Apps vs Meeting SDK (Common Confusion)"
---

# Zoom Apps vs Meeting SDK (Common Confusion)

Forum pattern: developers try to use Meeting SDK concepts inside Zoom Apps, or vice versa.

## Zoom Apps (Apps SDK)

Use when you want a **web app that runs inside the Zoom client**:

- in-meeting panel
- main client
- webinar contexts
- Layers API (immersive / camera mode)
- collaborate mode (shared state)

The app runs in Zoom’s embedded browser and interacts with the meeting via `@zoom/appssdk` capabilities.

## Meeting SDK

Use when you want to **embed the Zoom meeting experience in your own app** (outside the Zoom client):

- your website or desktop app hosts the meeting UI
- you handle signature generation server-side

## The Practical Decision

- “I want a sidebar app inside Zoom” -> Zoom Apps SDK
- “I want to embed Zoom meeting UI inside my product” -> Meeting SDK

If the question is “show contents in Zoom App via Meeting SDK”, first clarify which experience they actually want (inside Zoom vs embedded in their product).

