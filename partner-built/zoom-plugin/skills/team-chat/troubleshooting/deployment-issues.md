# Deployment Issues

## Works Locally, Fails in Prod

- DNS/HTTPS misconfiguration
- blocked outbound calls from your environment
- missing env vars / secrets
- wrong env file loaded at runtime (for split setups like `team-chat-api/.env` and `chatbot-api/.env`)

## Quick Prod Checklist

- Confirm token endpoint is `https://zoom.us/oauth/token`
- Confirm user OAuth authorize URL is `https://zoom.us/oauth/authorize`
- Confirm current UI routes are `/team-chat/user-demo` and `/team-chat/bot-demo`
- Confirm reverse proxy forwards `/team-chat/api/*` correctly

## Webhooks Time Out

- Respond fast and move long-running work to async jobs.
