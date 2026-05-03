# App Types

Choose the right Zoom app type for your integration.

## Overview

Zoom Marketplace has 3 app types:

| App Type | Use Case |
|----------|----------|
| **General App** | Flexible - configure surfaces, embeds, OAuth, webhooks |
| **Server-to-Server OAuth** | Backend automation, no user authorization |
| **Webhook Only** | Receive events only, no API access |

## General App

The modular app type. Pick what you need:

### OAuth Type (choose one)

| Type | Scopes | Authorization |
|------|--------|---------------|
| **Admin** | Admin scopes (`*:admin`) | Entire account OR specific users |
| **User** | User scopes | Only themselves (self-service) |

### Surfaces (product contexts)

Your app can interact with these Zoom products:

- Meetings
- Webinars
- Rooms
- Phone
- Team Chat
- Contact Center
- Whiteboard
- Virtual Agent
- Events
- Mail
- Workflows

### Embeds (SDKs)

Embed Zoom functionality in your app:

| Embed | Description |
|-------|-------------|
| **Meeting SDK** | Embed Zoom meetings |
| **Contact Center SDK** | Embed Contact Center |
| **Phone SDK** | Embed Phone functionality |

### Access

Configure in the Access tab:

- **Secret Token** - Verify webhook notifications
- **Event Subscription** - Webhooks
- **WebSockets** - Real-time event connections

### Scopes

Define which API methods the app can call. Scopes are:
- Restricted to specific resources
- Reviewed by Zoom during app submission

### Features in General App

General App can also include:
- **Zoom Apps** - Apps that run inside Zoom client

## Server-to-Server OAuth

Backend automation without user authorization.

- No user interaction required
- Access your account's data
- Can include webhooks and zoom-websockets
- Best for: automation, reporting, integrations

## Webhook Only

Event notifications only.

- Receive events, no API calls
- No OAuth tokens needed
- Best for: event logging, triggering external workflows

Use this when you ONLY need events. Otherwise, add webhooks to General App or S2S.

## Decision Guide

| Need | App Type |
|------|----------|
| Call APIs for your account (backend) | Server-to-Server OAuth |
| Call APIs on behalf of users | General App (Admin or User OAuth) |
| Embed Zoom meetings | General App + Meeting SDK embed |
| Embed Contact Center | General App + Contact Center SDK embed |
| Embed Phone | General App + Phone SDK embed |
| Build in-client app | General App + Zoom Apps |
| Receive events only | Webhook Only |
| Receive events + call APIs | General App or S2S (with webhooks) |

## Resources

- **App types docs**: https://developers.zoom.us/docs/integrations/
- **Marketplace**: https://marketplace.zoom.us/
