# Chatbot Setup - Complete Working Example

Build your first interactive Zoom chatbot from scratch. This guide provides complete, production-ready code.

## Prerequisites

- Completed [Environment Setup](../concepts/environment-setup.md)
- Obtained Bot JID, Client ID, Client Secret, Account ID, Secret Token
- Created .env file with credentials

## Project Structure

```
my-zoom-chatbot/
├── .env
├── .env.example
├── package.json
├── server.js
├── routes/
│   └── webhook.js
└── utils/
    ├── auth.js
    ├── chatbot.js
    └── validation.js
```

## Step 1: Initialize Project

```bash
mkdir my-zoom-chatbot
cd my-zoom-chatbot
npm init -y
```

## Step 2: Install Dependencies

```bash
npm install express dotenv node-fetch
```

## Step 3: Create .env File

```bash
# .env
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_BOT_JID=v1abc123xyz@xmpp.zoom.us
ZOOM_VERIFICATION_TOKEN=your_webhook_secret_token
ZOOM_ACCOUNT_ID=your_account_id

PORT=4000
```

## Step 4: Create Utility Files

### utils/auth.js

```javascript
// utils/auth.js
const fetch = require('node-fetch');

/**
 * Get chatbot access token using client_credentials flow
 */
async function getChatbotToken() {
  const credentials = Buffer.from(
    `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
  ).toString('base64');

  const response = await fetch('https://zoom.us/oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'grant_type=client_credentials'
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Token error: ${error.error_description || error.error}`);
  }

  const data = await response.json();
  return data.access_token;
}

module.exports = { getChatbotToken };
```

### utils/validation.js

```javascript
// utils/validation.js
const crypto = require('crypto');

/**
 * Verify Zoom webhook signature
 */
function verifyZoomWebhookSignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];

  if (!signature || !timestamp) {
    throw new Error('Missing signature headers');
  }

  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const hash = crypto
    .createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
    .update(message)
    .digest('hex');

  if (signature !== `v0=${hash}`) {
    throw new Error('Invalid webhook signature');
  }

  return true;
}

/**
 * Sanitize message (4096 char limit)
 */
function sanitizeMessage(message) {
  if (typeof message !== 'string') return '';
  return message
    .trim()
    .replace(/[\x00-\x1F\x7F]/g, '')
    .substring(0, 4096);
}

/**
 * Validate JID format
 */
function isValidJID(jid) {
  if (typeof jid !== 'string' || !jid.trim()) return false;
  return /^[^@\s]+@[^@\s]+$/.test(jid);
}

module.exports = {
  verifyZoomWebhookSignature,
  sanitizeMessage,
  isValidJID
};
```

### utils/chatbot.js

```javascript
// utils/chatbot.js
const fetch = require('node-fetch');
const { getChatbotToken } = require('./auth');
const { sanitizeMessage } = require('./validation');

/**
 * Send chatbot message
 */
async function sendChatbotMessage(toJid, accountId, content) {
  const accessToken = await getChatbotToken();

  const body = {
    robot_jid: process.env.ZOOM_BOT_JID,
    to_jid: toJid,
    account_id: accountId,
    content: content
  };

  const response = await fetch('https://api.zoom.us/v2/im/chat/messages', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Send message error: ${JSON.stringify(error)}`);
  }

  return response.json();
}

/**
 * Send simple text message
 */
async function sendTextMessage(toJid, accountId, text) {
  return sendChatbotMessage(toJid, accountId, {
    body: [
      { type: 'message', text: sanitizeMessage(text) }
    ]
  });
}

/**
 * Send message with buttons
 */
async function sendMessageWithButtons(toJid, accountId, options) {
  const { title, message, buttons } = options;

  return sendChatbotMessage(toJid, accountId, {
    head: {
      text: title
    },
    body: [
      { type: 'message', text: sanitizeMessage(message) },
      {
        type: 'actions',
        items: buttons.map(btn => ({
          text: btn.text,
          value: btn.value,
          style: btn.style || 'Default'
        }))
      }
    ]
  });
}

/**
 * Send message with fields
 */
async function sendMessageWithFields(toJid, accountId, options) {
  const { title, fields } = options;

  return sendChatbotMessage(toJid, accountId, {
    head: {
      text: title
    },
    body: [
      {
        type: 'fields',
        items: fields.map(field => ({
          key: field.key,
          value: field.value
        }))
      }
    ]
  });
}

module.exports = {
  sendChatbotMessage,
  sendTextMessage,
  sendMessageWithButtons,
  sendMessageWithFields
};
```

## Step 5: Create Webhook Handler

### routes/webhook.js

```javascript
// routes/webhook.js
const crypto = require('crypto');
const { verifyZoomWebhookSignature } = require('../utils/validation');
const { sendTextMessage, sendMessageWithButtons } = require('../utils/chatbot');

async function handleWebhook(req, res) {
  try {
    // Verify signature
    verifyZoomWebhookSignature(req);

    const { event, payload } = req.body;

    switch (event) {
      case 'endpoint.url_validation':
        return handleUrlValidation(req, res);

      case 'bot_installed':
        console.log('Bot installed for account:', payload.accountId);
        return res.status(200).json({ success: true });

      case 'bot_notification':
        return handleBotNotification(payload, res);

      case 'interactive_message_actions':
        return handleButtonClick(payload, res);

      case 'app_deauthorized':
        console.log('Bot uninstalled for account:', payload.accountId);
        return res.status(200).json({ success: true });

      default:
        console.log('Unsupported event:', event);
        return res.status(200).json({ success: true });
    }
  } catch (error) {
    console.error('Webhook error:', error);
    
    if (error.message.includes('signature')) {
      return res.status(401).json({ error: 'Invalid webhook signature' });
    }
    
    return res.status(500).json({ error: error.message });
  }
}

/**
 * Handle URL validation
 */
function handleUrlValidation(req, res) {
  const { plainToken } = req.body.payload;

  const encryptedToken = crypto
    .createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
    .update(plainToken)
    .digest('hex');

  return res.status(200).json({
    plainToken,
    encryptedToken
  });
}

/**
 * Handle bot notification (slash command or direct message)
 */
async function handleBotNotification(payload, res) {
  const { toJid, cmd, accountId, userName } = payload;

  console.log(`${userName} sent: ${cmd}`);

  // Respond immediately
  res.status(200).json({ success: true });

  // Process command asynchronously
  try {
    // Simple command router
    if (cmd.toLowerCase().includes('help')) {
      await sendTextMessage(toJid, accountId, 
        'Available commands:\n- help: Show this message\n- ping: Test bot\n- demo: Show demo buttons'
      );
    } 
    else if (cmd.toLowerCase().includes('ping')) {
      await sendTextMessage(toJid, accountId, 'Pong! 🏓');
    } 
    else if (cmd.toLowerCase().includes('demo')) {
      await sendMessageWithButtons(toJid, accountId, {
        title: 'Demo Buttons',
        message: 'Click a button below:',
        buttons: [
          { text: 'Option A', value: 'option_a', style: 'Primary' },
          { text: 'Option B', value: 'option_b', style: 'Default' },
          { text: 'Cancel', value: 'cancel', style: 'Danger' }
        ]
      });
    } 
    else {
      await sendTextMessage(toJid, accountId, 
        `You said: "${cmd}"\n\nType "help" to see available commands.`
      );
    }
  } catch (error) {
    console.error('Error processing command:', error);
  }
}

/**
 * Handle button click
 */
async function handleButtonClick(payload, res) {
  const { actionItem, toJid, accountId, userName } = payload;

  console.log(`${userName} clicked: ${actionItem.value}`);

  // Respond immediately
  res.status(200).json({ success: true });

  // Process button click asynchronously
  try {
    switch (actionItem.value) {
      case 'option_a':
        await sendTextMessage(toJid, accountId, '✅ You selected Option A');
        break;

      case 'option_b':
        await sendTextMessage(toJid, accountId, '✅ You selected Option B');
        break;

      case 'cancel':
        await sendTextMessage(toJid, accountId, '❌ Cancelled');
        break;

      default:
        await sendTextMessage(toJid, accountId, `Unknown action: ${actionItem.value}`);
    }
  } catch (error) {
    console.error('Error processing button click:', error);
  }
}

module.exports = { handleWebhook };
```

## Step 6: Create Main Server

### server.js

```javascript
// server.js
require('dotenv').config();
const express = require('express');
const { handleWebhook } = require('./routes/webhook');

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Zoom Team Chat Bot is running!' });
});

app.post('/webhook', handleWebhook);

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Webhook endpoint: ${process.env.PUBLIC_BASE_URL || 'https://YOUR_PUBLIC_BASE_URL'}/webhook`);
});
```

## Step 7: Test Locally with ngrok

```bash
# Install ngrok
npm install -g ngrok

# Start your server
node server.js

# In a new terminal, expose with ngrok
ngrok http 4000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

## Step 8: Configure Zoom Marketplace

1. Go to your app in [Zoom Marketplace](https://marketplace.zoom.us/)
2. Navigate to **Features** → **Team Chat Subscription**
3. Set **Bot Endpoint URL**: `https://abc123.ngrok.io/webhook`
4. Set **Slash Command**: `/mybot`
5. Click **Save**

Zoom will send a `endpoint.url_validation` request. If successful, you'll see a green checkmark.

## Step 9: Install and Test

1. Go to **Local Test** page in Zoom Marketplace
2. Click **Add App Now**
3. Click **Allow**
4. Open Zoom Team Chat
5. In any channel, type: `/mybot help`

You should see the bot respond with the help message!

## Testing Checklist

- [ ] `/mybot help` - Shows help message
- [ ] `/mybot ping` - Responds with "Pong! 🏓"
- [ ] `/mybot demo` - Shows buttons
- [ ] Click button - Sends confirmation message

## Production Deployment

### Environment Variables

```bash
# Production .env
ZOOM_CLIENT_ID=your_production_client_id
ZOOM_CLIENT_SECRET=your_production_client_secret
ZOOM_BOT_JID=v1abc123xyz@xmpp.zoom.us  # Production Bot JID
ZOOM_VERIFICATION_TOKEN=your_production_token
ZOOM_ACCOUNT_ID=your_account_id

PORT=4000
NODE_ENV=production
```

### Deploy to Cloud

**Options**:
- Heroku
- AWS Lambda
- Google Cloud Run
- Digital Ocean App Platform
- Vercel (with serverless functions)

**Requirements**:
- HTTPS endpoint (required for production)
- Publicly accessible URL
- Update Bot Endpoint URL in Zoom Marketplace to production URL

## Next Steps

- [Button Actions](button-actions.md) - Advanced button handling
- [LLM Integration](llm-integration.md) - Add Claude/GPT
- [Message Cards Reference](../references/message-cards.md) - Rich message components
- [Webhook Events Reference](../references/webhook-events.md) - All webhook events

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid signature" | Verify ZOOM_VERIFICATION_TOKEN matches Zoom Marketplace |
| Bot doesn't respond | Check ngrok is running and URL is correct |
| URL validation fails | Ensure endpoint returns plainToken + encryptedToken |
| Messages not sending | Verify Bot JID and Account ID are correct |

## Resources

- [Chatbot Quickstart (Official)](https://github.com/zoom/chatbot-nodejs-quickstart)
- [Claude Chatbot Sample](https://github.com/zoom/zoom-chatbot-claude-sample)
- [Unsplash Chatbot Sample](https://github.com/zoom/unsplash-chatbot)
