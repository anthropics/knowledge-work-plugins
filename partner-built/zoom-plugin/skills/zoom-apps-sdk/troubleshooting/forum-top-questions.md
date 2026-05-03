---
title: "Forum-Derived Top Questions (Zoom Apps)"
---

# Forum-Derived Top Questions (Zoom Apps)

This is a checklist of the most common forum questions for **Zoom Apps SDK**.

## Fast Routing Questions (Ask First)

- Running context: `inMeeting` vs `inMainClient` vs `inWebinar` vs `inImmersive` etc.
- SDK loading style: **NPM import** vs **CDN** (`window.zoomSdk`)
- Marketplace config: domain allowlist, scopes, and required capabilities

## “App won’t load / blank panel”

Most common causes:
- domain not in Marketplace allowlist
- trying to run the app in a normal browser (needs preview/demo mode)
- blocked mixed-content or missing HTTPS in dev tunnel

## “zoomSdk redeclaration” (CDN)

Common failure:
- redeclaring `let zoomSdk = ...` when CDN already defines `window.zoomSdk`

Answer pattern:
- use `const sdk = window.zoomSdk` or NPM import

## Auth Confusion

Common asks:
- “Do I use OAuth redirects?”
- “How does In-Client OAuth work?”

Answer pattern:
- explain In-Client OAuth (PKCE) and required scopes
- differentiate from REST API OAuth flows

