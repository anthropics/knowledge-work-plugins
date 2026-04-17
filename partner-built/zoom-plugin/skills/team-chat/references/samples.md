# Sample Applications Analysis

Analysis of 10 official Zoom Team Chat sample applications, extracted patterns, and best practices.

## Sample Overview

| Sample | Language | Complexity | Best For |
|--------|----------|------------|----------|
| [chatbot-nodejs-quickstart](https://github.com/zoom/chatbot-nodejs-quickstart) | Node.js | ⭐ Beginner | **Start here** - Tutorial series |
| [zoom-chatbot-claude-sample](https://github.com/zoom/zoom-chatbot-claude-sample) | Node.js | ⭐⭐ Intermediate | LLM integration pattern |
| [unsplash-chatbot](https://github.com/zoom/unsplash-chatbot) | Node.js | ⭐⭐ Intermediate | API integration + database |
| [zoom-erp-chatbot-sample](https://github.com/zoom/zoom-erp-chatbot-sample) | Node.js | ⭐⭐⭐ Advanced | Enterprise integration |
| [task-manager-sample](https://github.com/zoom/task-manager-sample) | Node.js | ⭐⭐⭐ Advanced | Full CRUD application |
| [zoom-cohere-chatbot-sample](https://github.com/zoom/zoom-cohere-chatbot-sample) | Node.js | ⭐⭐ Intermediate | Cohere LLM integration |
| [zoom-cerebras-chatbot-sample](https://github.com/zoom/zoom-cerebras-chatbot-sample) | Node.js | ⭐⭐ Intermediate | Cerebras LLM integration |
| [zoom-team-chat-shortcut-sample](https://github.com/zoom/zoom-team-chat-shortcut-sample) | Node.js | ⭐⭐ Intermediate | Shortcuts and UI elements |
| [zoom-teams-chat-snowflake-sample](https://github.com/zoom/zoom-teams-chat-snowflake-sample) | Node.js | ⭐⭐⭐ Advanced | Snowflake data integration |
| [rivet-javascript-sample](https://github.com/zoom/rivet-javascript-sample) | Node.js | ⭐⭐ Intermediate | Rivet SDK usage |

## 1. chatbot-nodejs-quickstart

**Repository**: https://github.com/zoom/chatbot-nodejs-quickstart

**Description**: Official tutorial series covering 9 episodes from setup to advanced features.

**Key Features**:
- Setup & Send Messages
- Handle Events
- Slash Commands
- Markdown & Emojis
- Reactions & Interactive Messages
- Threaded Replies
- Search Messages via API
- Scheduling Messages
- Zoom Workplace App Integration

**Project Structure**:
```
chatbot-nodejs-quickstart/
├── routes/
│   ├── zoom-webhookHandler.js     # Webhook event handling
│   └── oauth-routes.js             # OAuth flow
├── utils/
│   ├── zoom-api.js                 # API helper functions
│   ├── zoom-chatbot-auth.js        # Token generation
│   └── validation.js               # Webhook signature verification
├── views/                          # EJS templates
├── server.js                       # Express app
└── .env.example                    # Environment variables
```

**Key Patterns**:

### Webhook Handler Pattern
```javascript
async function handleZoomWebhook(req, res) {
  verifyZoomWebhookSignature(req);
  
  const { event, payload } = req.body;
  
  switch (event) {
    case 'bot_notification':
      return handleBotNotification(payload, res);
    case 'interactive_message_actions':
      return handleButtonClick(payload, res);
    // ... more cases
  }
}
```

### Token Generation
```javascript
async function getChatbotToken() {
  const credentials = Buffer.from(
    `${CLIENT_ID}:${CLIENT_SECRET}`
  ).toString('base64');
  
  const response = await fetch('https://zoom.us/oauth/token', {
    method: 'POST',
    headers: { 'Authorization': `Basic ${credentials}` },
    body: 'grant_type=client_credentials'
  });
  
  return (await response.json()).access_token;
}
```

**Best Practices**:
- ✅ Signature verification on all webhooks
- ✅ Environment variables for credentials
- ✅ Modular route structure
- ✅ Error handling with try/catch
- ✅ Immediate webhook response (200 status)

**Recommended For**: First-time chatbot developers

## 2. zoom-chatbot-claude-sample

**Repository**: https://github.com/zoom/zoom-chatbot-claude-sample

**Description**: AI-powered chatbot using Anthropic Claude for natural language responses.

**Key Features**:
- Claude API integration
- Conversation history tracking
- Streaming responses (optional)
- Context management

**LLM Integration Pattern**:
```javascript
case 'bot_notification': {
  const { toJid, cmd, accountId } = payload;
  
  // Call Claude API
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: cmd }]
  });
  
  const llmResponse = response.content[0].text;
  
  // Send back to Zoom
  await sendChatbotMessage(toJid, accountId, {
    body: [{ type: 'message', text: llmResponse }]
  });
}
```

**Conversation History Pattern**:
```javascript
const conversationHistory = new Map();

function addToHistory(userId, role, content) {
  if (!conversationHistory.has(userId)) {
    conversationHistory.set(userId, []);
  }
  conversationHistory.get(userId).push({ role, content });
}

// In bot_notification handler
const history = conversationHistory.get(userId) || [];
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  messages: history
});
```

**Environment Variables**:
```bash
ANTHROPIC_API_KEY=your_api_key_here
ZOOM_CLIENT_ID=...
ZOOM_CLIENT_SECRET=...
ZOOM_BOT_JID=...
```

**Recommended For**: Building AI assistants

## 3. unsplash-chatbot

**Repository**: https://github.com/zoom/unsplash-chatbot

**Description**: Image search bot integrating Unsplash API with database storage.

**Key Features**:
- Third-party API integration (Unsplash)
- Database persistence (SQLite/PostgreSQL)
- Image search and display
- User preference storage

**Database Schema**:
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  zoom_user_id TEXT UNIQUE,
  preferences TEXT
);

CREATE TABLE searches (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  query TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Image Display Pattern**:
```javascript
{
  "content": {
    "head": { "text": "Image Results" },
    "body": [
      {
        "type": "attachments",
        "img_url": imageData.urls.regular,
        "resource_url": imageData.links.html,
        "information": {
          "title": { "text": imageData.description },
          "description": { "text": `Photo by ${imageData.user.name}` }
        }
      }
    ]
  }
}
```

**Best Practices**:
- ✅ API rate limiting handling
- ✅ Error handling for external APIs
- ✅ Database connection pooling
- ✅ User data privacy

**Recommended For**: External API integration patterns

## 4. zoom-erp-chatbot-sample

**Repository**: https://github.com/zoom/zoom-erp-chatbot-sample

**Description**: Enterprise Resource Planning integration with scheduled alerts.

**Key Features**:
- Oracle ERP API integration
- Scheduled notifications (cron)
- Approval workflows
- Threaded conversations

**Scheduled Alerts Pattern**:
```javascript
const cron = require('node-cron');

// Daily report at 9 AM
cron.schedule('0 9 * * *', async () => {
  const report = await getERPReport();
  
  await sendChatbotMessage(channelJid, accountId, {
    head: { "text": "Daily ERP Report" },
    body: [
      { "type": "fields", "items": report.fields },
      {
        "type": "actions",
        "items": [
          { "text": "View Details", "value": "view_report" }
        ]
      }
    ]
  });
});
```

**Approval Workflow Pattern**:
```javascript
// Send approval request
{
  "head": { "text": "Expense Approval Required" },
  "body": [
    { "type": "fields", "items": expenseFields },
    {
      "type": "actions",
      "items": [
        { "text": "Approve", "value": `approve_${expenseId}`, "style": "Primary" },
        { "text": "Reject", "value": `reject_${expenseId}`, "style": "Danger" }
      ]
    }
  ]
}

// Handle button click
case 'interactive_message_actions': {
  const action = payload.actionItem.value;
  const [decision, expenseId] = action.split('_');
  
  await updateERPStatus(expenseId, decision);
  await sendConfirmation(payload.toJid, decision);
}
```

**Recommended For**: Enterprise integrations, workflows

## 5. task-manager-sample

**Repository**: https://github.com/zoom/task-manager-sample

**Description**: Full-featured task management application with CRUD operations.

**Key Features**:
- Create, read, update, delete tasks
- Task assignment
- Due date tracking
- Status management
- Persistent storage

**CRUD Pattern**:
```javascript
// CREATE
case 'bot_notification': {
  if (cmd.startsWith('create task')) {
    const taskData = parseTaskCommand(cmd);
    const task = await db.createTask(taskData);
    await sendTaskCreatedMessage(toJid, accountId, task);
  }
}

// READ
case 'interactive_message_actions': {
  if (actionItem.value.startsWith('view_task')) {
    const taskId = actionItem.value.split('_')[2];
    const task = await db.getTask(taskId);
    await sendTaskDetails(toJid, accountId, task);
  }
}

// UPDATE
case 'interactive_message_actions': {
  if (actionItem.value.startsWith('complete_task')) {
    const taskId = actionItem.value.split('_')[2];
    await db.updateTaskStatus(taskId, 'completed');
    await sendStatusUpdate(toJid, accountId, taskId);
  }
}

// DELETE
case 'interactive_message_actions': {
  if (actionItem.value.startsWith('delete_task')) {
    const taskId = actionItem.value.split('_')[2];
    await db.deleteTask(taskId);
    await sendDeletionConfirmation(toJid, accountId, taskId);
  }
}
```

**Recommended For**: Full application architecture

## Common Patterns Across Samples

### 1. Environment Variable Management

All samples use `.env` files with similar structure:

```bash
# Authentication
ZOOM_CLIENT_ID=
ZOOM_CLIENT_SECRET=
ZOOM_BOT_JID=
ZOOM_VERIFICATION_TOKEN=
ZOOM_ACCOUNT_ID=

# Third-party APIs (if applicable)
ANTHROPIC_API_KEY=
UNSPLASH_ACCESS_KEY=

# Server
PORT=4000
NODE_ENV=development
```

### 2. Project Structure

Common folder organization:

```
sample-app/
├── routes/
│   ├── webhook.js           # Webhook handlers
│   └── oauth.js             # OAuth flows (if needed)
├── utils/
│   ├── zoom-api.js          # Zoom API wrappers
│   ├── auth.js              # Token management
│   └── validation.js        # Input validation
├── models/                  # Database models (if applicable)
├── views/                   # Frontend templates (if applicable)
├── server.js                # Express app
├── .env.example
└── package.json
```

### 3. Webhook Verification

All samples verify webhook signatures:

```javascript
function verifyWebhook(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  
  const hash = crypto.createHmac('sha256', SECRET_TOKEN)
    .update(message)
    .digest('hex');
  
  return signature === `v0=${hash}`;
}
```

### 4. Error Handling

Consistent error handling pattern:

```javascript
app.post('/webhook', async (req, res) => {
  try {
    verifyWebhook(req);
    await handleWebhook(req.body);
    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);
    
    if (error.message.includes('signature')) {
      return res.status(401).json({ error: 'Invalid signature' });
    }
    
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### 5. Async Webhook Processing

Respond immediately, process async:

```javascript
app.post('/webhook', (req, res) => {
  // Respond immediately
  res.status(200).json({ success: true });
  
  // Process asynchronously
  processWebhookAsync(req.body).catch(error => {
    console.error('Async processing error:', error);
  });
});
```

## Architecture Lessons

### Chatbot Lifecycle

Common lifecycle across all samples:

```
1. User Action (slash command, button click, message)
   ↓
2. Zoom sends webhook to Bot Endpoint URL
   ↓
3. Server verifies signature
   ↓
4. Server responds 200 (immediately)
   ↓
5. Server processes request (async)
   ↓
6. Server calls external APIs if needed
   ↓
7. Server sends chatbot message back to Zoom
```

### State Management

**Simple bots**: In-memory state (Map/Object)
**Production bots**: Database (PostgreSQL, MongoDB, Redis)

```javascript
// Simple (development)
const userState = new Map();

// Production
const userState = {
  async get(userId) {
    return await db.query('SELECT * FROM user_state WHERE user_id = $1', [userId]);
  },
  async set(userId, state) {
    return await db.query('INSERT INTO user_state (user_id, state) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET state = $2', [userId, state]);
  }
};
```

## Deprecation Notes

Some samples may use deprecated patterns:

### ❌ Old Pattern (Don't Use)
```javascript
// Hardcoded credentials
const CLIENT_ID = 'abc123';
```

### ✅ New Pattern (Use This)
```javascript
// Environment variables
const CLIENT_ID = process.env.ZOOM_CLIENT_ID;
```

### ❌ Old Pattern (Don't Use)
```javascript
// Synchronous webhook processing (may timeout)
app.post('/webhook', async (req, res) => {
  await longRunningProcess();
  res.status(200).json({ success: true });
});
```

### ✅ New Pattern (Use This)
```javascript
// Async processing
app.post('/webhook', (req, res) => {
  res.status(200).json({ success: true });
  longRunningProcess().catch(console.error);
});
```

## Sample Selection Guide

### Choose chatbot-nodejs-quickstart if:
- You're new to Zoom chatbots
- You want a tutorial series
- You need step-by-step guidance

### Choose zoom-chatbot-claude-sample if:
- You want to integrate an LLM
- You need conversational AI
- You want to see LLM integration patterns

### Choose unsplash-chatbot if:
- You need to integrate external APIs
- You want database patterns
- You need user preference storage

### Choose zoom-erp-chatbot-sample if:
- You're building enterprise integrations
- You need scheduled notifications
- You want approval workflows

### Choose task-manager-sample if:
- You want a full CRUD application
- You need complex state management
- You want to see production architecture

## Next Steps

- [Chatbot Setup Example](../examples/chatbot-setup.md) - Build your own using these patterns
- [LLM Integration Example](../examples/llm-integration.md) - Integrate Claude/GPT
- [Button Actions Example](../examples/button-actions.md) - Handle interactive components
- [Sample Comparison](sample-comparison.md) - Compare common sample shapes before choosing a baseline

## Resources

- [Official Samples GitHub Org](https://github.com/zoom?q=chatbot)
- [Chatbot Documentation](https://developers.zoom.us/docs/team-chat/chatbot/extend/)
- [Developer Forum](https://devforum.zoom.us/)
