# Multi-Client Pattern (Two Modules, Two Ports)

Use this when combining chatbot command handling with Team Chat API lookups.

```javascript
import { ChatbotClient } from "@zoom/rivet/chatbot";
import { TeamChatClient } from "@zoom/rivet/teamchat";

const CHATBOT_PORT = Number(process.env.RIVET_CHATBOT_PORT || 4001);
const TEAMCHAT_PORT = Number(process.env.RIVET_TEAMCHAT_PORT || 4002);

(async () => {
  const chatbotClient = new ChatbotClient({
    clientId: process.env.RIVET_CLIENT_ID,
    clientSecret: process.env.RIVET_CLIENT_SECRET,
    webhooksSecretToken: process.env.RIVET_WEBHOOK_SECRET_TOKEN,
    port: CHATBOT_PORT,
  });

  const teamchatClient = new TeamChatClient({
    clientId: process.env.RIVET_CLIENT_ID,
    clientSecret: process.env.RIVET_CLIENT_SECRET,
    webhooksSecretToken: process.env.RIVET_WEBHOOK_SECRET_TOKEN,
    installerOptions: {
      redirectUri: process.env.RIVET_REDIRECT_URI,
      stateStore: process.env.RIVET_STATE_STORE_SECRET,
    },
    port: TEAMCHAT_PORT,
  });

  chatbotClient.webEventConsumer.onSlashCommand("help", async ({ say }) => {
    await say("Rivet bot ready.");
  });

  chatbotClient.webEventConsumer.onSlashCommand("channels", async ({ say, payload }) => {
    const result = await teamchatClient.endpoints.chatChannels.listUsersChannels({
      path: { userId: payload.userId },
    });

    const names = (result.data?.channels || []).map((x) => x.name).join(", ");
    await say(`Channels: ${names || "none"}`);
  });

  await teamchatClient.start();
  await chatbotClient.start();
})();
```

## Operational Notes

- Subscribe chatbot events to `CHATBOT_PORT` endpoint.
- Complete Team Chat OAuth install flow against `TEAMCHAT_PORT`.
- Keep ports unique and explicit in documentation and deployment configs.
