# Getting Started Pattern (Single Module)

This pattern shows a minimal Rivet bootstrap for Team Chat with OAuth installation support.

```javascript
import { TeamChatClient } from "@zoom/rivet/teamchat";

(async () => {
  const teamchatClient = new TeamChatClient({
    clientId: process.env.RIVET_CLIENT_ID,
    clientSecret: process.env.RIVET_CLIENT_SECRET,
    webhooksSecretToken: process.env.RIVET_WEBHOOK_SECRET_TOKEN,
    installerOptions: {
      redirectUri: process.env.RIVET_REDIRECT_URI,
      stateStore: process.env.RIVET_STATE_STORE_SECRET,
    },
    port: Number(process.env.RIVET_PORT || 8080),
  });

  teamchatClient.webEventConsumer.event("chat_message.sent", ({ payload }) => {
    console.log("event", payload);
  });

  const server = await teamchatClient.start();
  console.log("rivet server", server.address());
})();
```

## Required Marketplace Wiring

- Add endpoint URL to event subscription with `/zoom/events` suffix.
- Ensure OAuth redirect URI exactly matches `installerOptions.redirectUri` + callback path behavior.
- Include all scopes needed by `endpoints.*` calls.

## Common Extension

Add API calls with typed wrappers:

```javascript
const channels = await teamchatClient.endpoints.chatChannels.listUsersChannels({
  path: { userId: "me" },
});
```
