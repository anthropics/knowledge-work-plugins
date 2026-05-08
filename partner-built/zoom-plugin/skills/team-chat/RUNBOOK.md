# Team Chat 5-Minute Preflight Runbook

Use this before deep debugging. It catches the most common Team Chat failures fast.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm Integration Type

- User type (Team Chat API): user OAuth + `/v2/chat/users/...`
- Bot type (Chatbot API): client credentials + `/v2/im/chat/messages`

If this is wrong, everything else will fail.

## 2) Confirm OAuth Endpoints

- Authorize URL: `https://zoom.us/oauth/authorize`
- Token URL: `https://zoom.us/oauth/token`

If token requests hit `/oauth/token`, expect 404/HTML.

## 3) Confirm Runtime Env Loading

If credentials are split by mode, verify your server loads the actual files at runtime:

- `project/team-chat-api/.env`
- `project/chatbot-api/.env`

Do not assume root `.env` is enough.

## 4) Confirm App Routes + Reverse Proxy

- Current demo pages:
  - `/team-chat/user-demo`
  - `/team-chat/bot-demo`
- API path should resolve: `/team-chat/api/*`

If browser calls old routes (`/api/channel/*`) and gets 404, either update frontend or keep compatibility routes.

## 5) Run Curl Probes

Use backend probes before browser debugging.

```bash
TEAM_CHAT_BASE_URL="http://YOUR_HOST:YOUR_PORT"

curl -sS "$TEAM_CHAT_BASE_URL/team-chat/api/config"
curl -sS -i "$TEAM_CHAT_BASE_URL/team-chat/api/bot/token"
curl -sS -i "$TEAM_CHAT_BASE_URL/team-chat/api/channel/list"
```

Expected:
- `api/config` shows required flags as configured.
- `api/bot/token` should return JSON (200 or actionable 4xx), never HTML 404 page.
- `api/channel/list` returns validation errors or data, not generic 404.

## 6) Browser-Specific Reality Check

`ERR_BLOCKED_BY_CLIENT` usually means extension/adblock/privacy filter interference.

- Re-test in Incognito.
- Temporarily disable blockers for host.
- Validate with curl first.

## 7) User OAuth Callback Flow (In-App)

For user-demo, avoid manual copy/paste flow:

1. UI button triggers backend authorize URL generation with `state`.
2. Browser redirects to Zoom consent page.
3. Callback validates `state` and exchanges `code` server-side.
4. Token is stored where UI expects (session/db/local storage for demo).
5. Redirect back to user-demo.

If callback returns but token is missing, focus on `state` validation and persistence path.

## 8) Fast Decision Tree

- **404 on bot token** -> check token URL (`/oauth/token`), then proxy path.
- **All channel APIs 404** -> route mismatch (old UI vs new backend routes).
- **OAuth works but sends fail** -> wrong scopes or app type mismatch.
- **Works by curl but fails in browser** -> blocked client/cached old JS.
