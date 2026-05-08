# Deployment Guide (Team Chat / Chatbot)

## Basic Requirements

- Your webhook endpoint must be reachable by Zoom (public HTTPS).
- Keep secrets out of the repo:
  - `ZOOM_CLIENT_ID`
  - `ZOOM_CLIENT_SECRET`
  - `ZOOM_BOT_JID` (chatbot)
  - `ZOOM_SECRET_TOKEN` (chatbot verification)

## Recommended Production Setup

- Run behind a reverse proxy (TLS termination).
- Use a persistent store for:
  - OAuth tokens (Team Chat API)
  - installation state (Chatbot API)
  - idempotency keys for webhooks (avoid double-processing)

## Local Testing

- Use a tunneling tool to expose your local development host over HTTPS for webhook testing.
- Keep a "dev" app and "prod" app to avoid breaking production while iterating.
