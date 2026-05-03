# Rivet High-Level Scenarios

## 1) Team Chat Standup Bot with Channel Intelligence

- Modules: `ChatbotClient` + `TeamChatClient`
- Auth: Client Credentials (chatbot) + User OAuth or S2S for Team Chat APIs
- Flow:
1. Slash command enters chatbot webhook.
2. Bot queries channel and member lists via Team Chat endpoints.
3. Bot posts/updates interactive message cards.
- Risks:
- Misaligned scopes cause endpoint failures.
- Wrong port in Marketplace event subscription prevents callbacks.

## 2) ISV Admin Automation Service

- Modules: `UsersS2SAuthClient`, `MeetingsS2SAuthClient`, optionally `AccountsS2SAuthClient`
- Auth: S2S OAuth
- Flow:
1. Backend receives internal request to create/update Zoom resources.
2. Rivet endpoints wrap REST calls.
3. Webhooks confirm completion state.
- Risks:
- Missing `accountId` or stale S2S credentials.
- Event and API schema mismatch across versions.

## 3) Video SDK API Operations and Recording Workflow

- Module: `VideoSdkClient`
- Auth: Video SDK JWT
- Flow:
1. Create/list/manage sessions.
2. Manage recording/BYOS/report endpoints.
3. React to session/recording webhooks.
- Risks:
- Wrong credential type (OAuth client vs Video SDK key/secret).
- Ignoring recording and BYOS endpoint field changes after upgrades.

## 4) AWS Lambda Event Receiver Deployment

- Module: product-specific client + `AwsLambdaReceiver`
- Flow:
1. Instantiate client with `receiver: new AwsLambdaReceiver(...)`.
2. Export Lambda handler that delegates to `await client.start()` handler.
3. Use API Gateway/serverless-offline for local parity.
- Risks:
- User OAuth expectations with unsupported receiver flow.
- Secret token mismatch across Lambda environments.

## 5) Multi-Tenant Event Router

- Modules: one or more, with external token/state stores
- Flow:
1. Receive webhook.
2. Resolve tenant and token context.
3. Execute routed API action.
4. Persist audit and retry state.
- Risks:
- In-memory token store only (tokens lost on restart).
- Missing idempotency for retried webhook events.
