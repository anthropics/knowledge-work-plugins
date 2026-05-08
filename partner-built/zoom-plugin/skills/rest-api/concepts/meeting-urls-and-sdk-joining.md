---
title: "Meeting URLs vs Meeting SDK Joining"
---

# Meeting URLs vs Meeting SDK Joining

Forum confusion pattern:

- “How do I generate a Zoom meeting URL server-side?”
- “How do I join a meeting via API?”
- “Can I use `join_url` with Meeting SDK?”

## REST API: What You Get

When you create a meeting via REST API, you typically get:

- `join_url`: for participants to join using Zoom clients/web join links
- `start_url`: for the host (often time-limited, and tied to the host context)
- `id` / meeting number: the meeting identifier

## Meeting SDK: What It Uses

Meeting SDK integrations generally use:

- `meetingNumber` (meeting id)
- Meeting SDK **signature** (generated server-side)
- `role` (0 join, 1 start)
- passcode (if required)

So: you usually do **not** “feed join_url into Meeting SDK”. You use the meeting number + SDK signature.

## “Join via API” Clarification

The REST API does not “join” a meeting as a client. If the goal is to build an embedded or automated participant, you’re typically looking at:

- Meeting SDK (embed/join/start flows)
- or bot-style patterns (Linux Meeting SDK, or RTMS for media access), depending on the end goal

