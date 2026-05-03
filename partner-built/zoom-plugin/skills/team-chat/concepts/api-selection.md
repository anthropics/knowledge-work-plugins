# API Selection Guide

Zoom Team Chat offers **two distinct APIs** for different use cases. Choose the right one before you start building.

## Critical First Decision

Pick one of these integration types before writing code:

- **User type** -> Team Chat API -> User OAuth -> `/v2/chat/users/...`
- **Bot type** -> Chatbot API -> Client Credentials -> `/v2/im/chat/messages`

Most implementation issues come from mixing user-type auth with bot-type endpoints (or the opposite).

## Quick Decision Matrix

| Use Case | API to Use | Messages Appear As |
|----------|------------|-------------------|
| Send notifications from scripts/CI/CD | **Team Chat API** | Authenticated user |
| Automate messages as a user | **Team Chat API** | Authenticated user |
| Build an interactive chatbot | **Chatbot API** | Your bot |
| Respond to slash commands | **Chatbot API** | Your bot |
| Create messages with buttons/forms | **Chatbot API** | Your bot |
| Handle user interactions | **Chatbot API** | Your bot |

## Team Chat API (User-Level Messaging)

### What It Is

The Team Chat API allows your application to send messages **as an authenticated user**. Messages appear in Team Chat as if the user sent them manually.

### When to Use

✅ **Use Team Chat API when:**
- You want to send simple text messages programmatically
- Messages should appear as sent by a specific user
- You're building CI/CD notifications
- You're automating user-level messaging
- You don't need interactive components (buttons, forms)

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Authentication** | User OAuth (authorization_code flow) |
| **Endpoint** | `POST https://api.zoom.us/v2/chat/users/me/messages` |
| **Message Format** | Plain text or markdown |
| **Scopes** | `chat_message:write`, `chat_channel:read` |
| **User Experience** | Messages appear from the authenticated user |

### Example Use Cases

1. **CI/CD Notifications**
   ```
   User: "Build #123 completed successfully"
   ```

2. **Automated Reporting**
   ```
   User: "Daily sales report: $10,000"
   ```

3. **Task Reminders**
   ```
   User: "Reminder: Team meeting in 15 minutes"
   ```

## Chatbot API (Bot-Level Interactions)

### What It Is

The Chatbot API allows your application to send messages **as a bot**. Bots can send rich, interactive messages with buttons, forms, images, and handle user interactions via webhooks.

### When to Use

✅ **Use Chatbot API when:**
- You want to build an interactive chatbot
- You need rich message formatting (cards, buttons, forms)
- You want to handle slash commands (e.g., `/weather`)
- You need to respond to button clicks or form submissions
- You're integrating LLMs (Claude, GPT, etc.)
- You want scheduled notifications

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Authentication** | Client Credentials grant |
| **Endpoint** | `POST https://api.zoom.us/v2/im/chat/messages` |
| **Message Format** | Rich cards with components |
| **Scopes** | `imchat:bot` (auto-added) |
| **User Experience** | Messages appear from your bot |
| **Interactivity** | Buttons, forms, dropdowns, webhooks |

### Example Use Cases

1. **Support Bot**
   ```
   Bot: "How can I help you?"
   [Help Center] [Contact Support] [Report Bug]
   ```

2. **Approval Workflow**
   ```
   Bot: "Expense Report: $500"
   Branch: main
   Requester: John
   [Approve] [Reject]
   ```

3. **AI Assistant**
   ```
   User: "/ask What's the weather?"
   Bot: "The weather in San Francisco is 72°F and sunny."
   ```

## Feature Comparison

| Feature | Team Chat API | Chatbot API |
|---------|---------------|-------------|
| **Plain Text Messages** | ✅ | ✅ |
| **Markdown** | ✅ | ✅ |
| **Rich Cards** | ❌ | ✅ |
| **Buttons** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Dropdowns** | ❌ | ✅ |
| **Images** | ✅ (basic) | ✅ (rich) |
| **Slash Commands** | ❌ | ✅ |
| **Webhooks** | ❌ | ✅ |
| **Button Click Handling** | ❌ | ✅ |
| **Form Submissions** | ❌ | ✅ |

## Authentication Comparison

### Team Chat API (User OAuth)

**Flow**: authorization_code  
**Requires**: User login and consent  
**Token Scope**: User's data only

```javascript
// Step 1: Redirect user to OAuth consent page
const authUrl = `https://zoom.us/oauth/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;

// Step 2: Exchange auth code for access token
const tokens = await exchangeCodeForToken(code);

// Step 3: Use access token to send messages
fetch('https://api.zoom.us/v2/chat/users/me/messages', {
  headers: { 'Authorization': `Bearer ${tokens.access_token}` }
});
```

### Chatbot API (Client Credentials)

**Flow**: client_credentials  
**Requires**: No user login  
**Token Scope**: Bot actions only

```javascript
// Step 1: Get bot token (no user interaction)
const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
const response = await fetch('https://zoom.us/oauth/token', {
  method: 'POST',
  headers: { 'Authorization': `Basic ${credentials}` },
  body: 'grant_type=client_credentials'
});

const { access_token } = await response.json();

// Step 2: Use access token to send bot messages
fetch('https://api.zoom.us/v2/im/chat/messages', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## Can I Use Both?

**Yes!** You can use both APIs in the same application.

**Example**: Task management app
- **Team Chat API**: User creates a task → message appears as "User created task #123"
- **Chatbot API**: Bot sends reminders → "Task #123 is due today [View] [Snooze]"

## Decision Tree

```
Need rich interactive messages?
├─ Yes → Chatbot API
└─ No
   └─ Need webhooks (slash commands, button clicks)?
      ├─ Yes → Chatbot API
      └─ No
         └─ Messages should appear as user?
            ├─ Yes → Team Chat API
            └─ No → Chatbot API
```

## Common Misconceptions

### ❌ "I need to use Server-to-Server OAuth for bots"
**Reality**: Chatbots require **General App (OAuth)**, not Server-to-Server OAuth. S2S apps don't support the Chatbot feature.

### ❌ "Team Chat API can send buttons"
**Reality**: Only Chatbot API supports interactive components (buttons, forms, dropdowns).

### ❌ "Chatbot API requires user login"
**Reality**: Chatbot API uses client_credentials flow (no user login needed).

### ❌ "OAuth token endpoint is `/oauth/token`"
**Reality**: Use `https://zoom.us/oauth/token` for token exchange. Keep `https://zoom.us/oauth/authorize` for the user consent step.

### ❌ "I can only use one API per app"
**Reality**: You can use both APIs in the same application.

## Next Steps

### If you chose **Team Chat API**:
1. [Environment Setup](environment-setup.md) - Get credentials
2. [OAuth Setup](../examples/oauth-setup.md) - Implement OAuth flow
3. [Send Message](../examples/send-message.md) - Send your first message

### If you chose **Chatbot API**:
1. [Environment Setup](environment-setup.md) - Get credentials (including Bot JID)
2. [Chatbot Setup](../examples/chatbot-setup.md) - Build your first bot
3. [Webhook Architecture](webhooks.md) - Understand webhook events

## Resources

- [Official Team Chat API Docs](https://developers.zoom.us/docs/api/rest/reference/chat/)
- [Official Chatbot API Docs](https://developers.zoom.us/docs/api/rest/reference/chatbot/)
- [Chatbot Quickstart Sample](https://github.com/zoom/chatbot-nodejs-quickstart)
