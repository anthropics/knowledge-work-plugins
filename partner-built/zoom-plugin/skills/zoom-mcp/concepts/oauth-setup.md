# OAuth Setup — Zoom MCP Server

## Overview

The documented path for Zoom MCP is a **General app** using **user-level OAuth**.
Each user authorizes with their own Zoom account, and the resulting bearer token is passed by
the bundled connector in [`.mcp.json`](../../../.mcp.json).

## Step 1: Create a General App with User-Level OAuth

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us) → **Develop** → **Build App**.
2. Create a **General app**.
3. Configure the app for **user-level OAuth** for the per-user MCP path.
4. Set a redirect URL for your client or local test environment.
5. Note the client ID and client secret.

### If You Do Not Already Have a Redirect Endpoint

For development, two pragmatic options are:

**Option 0: `localhost` and manually copy the code**

Example:

```text
http://localhost:3000/oauth/zoom/callback
```

If the local app does not actually handle the callback yet, the browser may show a failed page
load. You can still copy the `code` and `state` values from the browser URL and paste them into
Claude or your terminal flow so the token exchange can continue manually.

Pros:
- no tunnel and no third-party capture service
- fastest setup if you only need the authorization code once
- keeps the authorization code on your machine

Cons:
- manual copy/paste step every time
- no automatic code exchange or refresh flow
- less convenient if you repeat the auth flow often

**Option 1: `ngrok` in front of a local callback server**

Example:

```text
Local app: http://localhost:3000/oauth/zoom/callback
Public redirect URL: https://your-subdomain.ngrok.app/oauth/zoom/callback
```

Pros:
- best match for the real OAuth flow because your own app receives the callback directly
- easy to inspect requests locally while keeping your app logic in one place
- useful if you also need to exchange the code for tokens automatically

Cons:
- requires running a local server plus the tunnel
- slightly more setup than a capture-only endpoint
- you are exposing a local service to the internet, so keep the callback narrow and temporary

**Option 2: `webhook.site` for one-off callback capture**

Example:

```text
https://webhook.site/your-token
```

Pros:
- fastest path when you just need to capture the authorization redirect once
- no local server required
- easy to inspect the query string and copy out `code` and `state`

Cons:
- not a full OAuth app backend; you still need to exchange the code for tokens yourself
- weaker fit for repeated development flows and team usage
- the authorization code is sensitive, so only use this for short-lived development testing and
  avoid shared or long-lived capture URLs

Practical recommendation:
- use plain `localhost` if you only need a one-off auth code and are fine copying it manually
- use `ngrok` if you are building a real integration or expect to repeat the flow
- use `webhook.site` only for quick one-off testing when you do not yet have a callback handler

## Step 2: Configure Zoom MCP Scopes

Add the MCP-specific granular scopes required by the tools you want to use.

| Product Area | Scope | Zoom label | Needed for |
|--------------|-------|------------|------------|
| AI Companion | `ai_companion:read:search` | Search across Zoom Meeting, Zoom Chat, and Zoom Doc, returning the most relevant results based on the query. | semantic MCP search |
| Meeting | `meeting:read:search` | Search and view meetings | `search_meetings` |
| Meeting | `meeting:read:assets` | View a meeting's assets | `get_meeting_assets` |
| Recording | `cloud_recording:read:list_user_recordings` | Lists all cloud recordings for a user. | `recordings_list` |
| Recording | `cloud_recording:read:content` | read recording content scope | `get_recording_resource` |
| Zoom Docs | `docs:write:import` | Create new file by import | `create_file_with_content` |
| Zoom Docs | `docs:read:export` | Read file content in Markdown format | `get_file_content` |

Minimum recommendation for the main Zoom MCP connector:
- use a General app
- use user-level OAuth
- include the 7 main MCP scopes above on the same app

For the dedicated Zoom Docs MCP connector:
- add `docs:write:import` if you want Docs creation
- add `docs:read:export` if you want Docs retrieval
- export the resulting token as `ZOOM_DOCS_MCP_ACCESS_TOKEN`

Whiteboard MCP uses a separate scope set. See [../whiteboard/SKILL.md](../whiteboard/SKILL.md).

## Step 3: Authorize and Exchange for Tokens

1. Construct the authorization URL:
   ```
   https://zoom.us/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI
   ```
2. Sign in as the Zoom user who should authorize the app and approve the requested scopes.
3. Copy the `code` from the redirect URL.
4. Exchange the code for tokens:
   ```bash
   curl -X POST https://zoom.us/oauth/token \
     -u "CLIENT_ID:CLIENT_SECRET" \
     -d "grant_type=authorization_code&code=CODE&redirect_uri=REDIRECT_URI"
   ```
5. Store the returned `access_token` and `refresh_token`.

Treat the refresh token as **single-use**:
- every successful refresh can return a new refresh token
- persist the newly returned refresh token atomically with the new access token
- stop using the old refresh token after a successful refresh
- avoid concurrent refresh requests against the same stored token

If you used `webhook.site`, the callback will arrive as a captured request and the `code`
parameter will be in the query string. Exchange it immediately and do not keep using the same
capture URL longer than necessary.

## Step 4: Enable AI Companion Features

Smart Recording and Meeting Summary are feature prerequisites for useful semantic meeting
search, meeting assets, and transcript-rich recording content.

In the Zoom web portal:
1. Go to **Admin → Account Management → Account Settings → AI Companion**.
2. Enable **Smart Recording**.
3. Enable **Meeting Summary**.

Important:
- these settings do **not** replace the OAuth scopes above
- they affect whether useful recap and transcript content exists for MCP retrieval

## Step 5: Provide the Token to the Bundled MCP Connector

Export the token environment variable used by this plugin:

```bash
export ZOOM_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_DOCS_MCP_ACCESS_TOKEN="YOUR_DOCS_ACCESS_TOKEN"
```

Verification:
- restart Claude Code or re-enable the plugin so the bundled MCP server restarts with the token
- confirm the client can see `recordings_list`, `search_meetings`, `get_meeting_assets`,
  and `get_recording_resource`
- for the dedicated Docs server, confirm the client can see `create_file_with_content`
  and `get_file_content`
- if your client exposes protocol inspection, use `tools/list` as the authority for the live catalog
- run a simple tool such as `recordings_list` to verify the token has the correct MCP scopes

## Token Lifecycle

| Property | Details |
|----------|---------|
| Access token expiry | About 1 hour |
| Refresh flow | Exchange `refresh_token` for a new `access_token` and replacement `refresh_token` |
| Client update | Update `ZOOM_MCP_ACCESS_TOKEN`, then restart Claude Code or re-enable the plugin |

Refresh exchange:

```bash
curl -X POST https://zoom.us/oauth/token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN"
```

After a successful refresh:
- replace the stored access token
- replace the stored refresh token
- treat the previously used refresh token as spent
- restart Claude Code or re-enable the plugin if you are injecting tokens through env vars

## Environment Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_MCP_ACCESS_TOKEN=your_access_token
ZOOM_DOCS_MCP_ACCESS_TOKEN=your_docs_access_token
ZOOM_REFRESH_TOKEN=your_refresh_token
```

See also: [../../oauth/SKILL.md](../../oauth/SKILL.md)
