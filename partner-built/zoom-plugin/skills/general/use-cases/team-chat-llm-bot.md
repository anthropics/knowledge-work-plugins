# Use Case: AI-Powered Team Chat Bot with LLM Integration

Build an intelligent Zoom Team Chat bot that uses Claude/GPT for natural language understanding and can be chained with other Zoom skills.

## Scenario

Create a chatbot that:
1. Responds to natural language queries
2. Can trigger Zoom Meeting creation
3. Can search and retrieve chat history
4. Provides intelligent assistance across Zoom products

## Skills Required

- **zoom-team-chat** - Primary skill for chatbot functionality
- **zoom-rest-api** - For meeting creation, user management
- **oauth** - For user authentication flows (optional)
- **zoom-meeting-sdk** - For advanced meeting integrations (optional)

## Architecture

```
User sends message → Team Chat Bot receives webhook
                            ↓
                     Call LLM (Claude/GPT)
                            ↓
                     Parse LLM response for intent
                            ↓
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    Create Meeting    Get User Info    Send Response
    (REST API)        (REST API)       (Team Chat)
```

## Implementation Steps

### 1. Setup Team Chat Bot

**Skill**: `zoom-team-chat`

```javascript
// Handle bot notification
case 'bot_notification': {
  const { toJid, cmd, accountId } = payload;
  
  // Call LLM
  const llmResponse = await callClaude(cmd);
  
  // Check for intents
  const intent = parseIntent(llmResponse);
  
  if (intent.type === 'create_meeting') {
    await handleCreateMeeting(toJid, accountId, intent);
  } else {
    await sendTextMessage(toJid, accountId, llmResponse);
  }
}
```

### 2. Create Meeting Intent

**Skills**: `zoom-team-chat` + `zoom-rest-api`

```javascript
async function handleCreateMeeting(toJid, accountId, intent) {
  // Extract meeting details from LLM response
  const { topic, start_time, duration } = intent.details;
  
  // Create meeting using REST API
  const meeting = await fetch('https://api.zoom.us/v2/users/me/meetings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${userAccessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      topic,
      type: 2, // Scheduled meeting
      start_time,
      duration
    })
  });
  
  const meetingData = await meeting.json();
  
  // Send meeting details back to Team Chat
  await sendChatbotMessage(toJid, accountId, {
    head: { text: 'Meeting Created' },
    body: [
      { type: 'message', text: `Meeting "${topic}" created successfully!` },
      {
        type: 'fields',
        items: [
          { key: 'Start Time', value: start_time },
          { key: 'Duration', value: `${duration} minutes` },
          { key: 'Join URL', value: meetingData.join_url }
        ]
      },
      {
        type: 'actions',
        items: [
          { text: 'Join Meeting', value: `join_${meetingData.id}`, style: 'Primary' },
          { text: 'Share Link', value: `share_${meetingData.id}`, style: 'Default' }
        ]
      }
    ]
  });
}
```

### 3. LLM Integration with Intent Parsing

**Skill**: `zoom-team-chat`

```javascript
const Anthropic = require('@anthropic-ai/sdk');
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function callClaude(userMessage) {
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    system: `You are a Zoom assistant bot. You can help users with:
- Creating meetings
- Finding user information
- Answering questions about Zoom
- General assistance

When a user wants to create a meeting, respond with JSON:
{
  "intent": "create_meeting",
  "details": {
    "topic": "Meeting topic",
    "start_time": "ISO 8601 format",
    "duration": 60
  }
}

Otherwise, provide a helpful text response.`,
    messages: [{ role: 'user', content: userMessage }]
  });
  
  return response.content[0].text;
}

function parseIntent(llmResponse) {
  try {
    // Check if response is JSON
    if (llmResponse.trim().startsWith('{')) {
      const intent = JSON.parse(llmResponse);
      return intent;
    }
  } catch (e) {
    // Not JSON, regular text response
  }
  
  return { type: 'text_response', message: llmResponse };
}
```

## Skill Chaining Examples

### Example 1: Create Meeting from Chat

**User**: `/bot schedule a team standup tomorrow at 10am for 30 minutes`

**Flow**:
1. **zoom-team-chat**: Receives command via webhook
2. LLM parses: "create_meeting" intent
3. **zoom-rest-api**: Creates meeting
4. **zoom-team-chat**: Sends confirmation with buttons

### Example 2: Find User and Start DM

**User**: `/bot who is John Doe?`

**Flow**:
1. **zoom-team-chat**: Receives query
2. LLM identifies: "find_user" intent
3. **zoom-rest-api**: Searches users
4. **zoom-team-chat**: Shows user info with "Send DM" button

### Example 3: Search Chat History

**User**: `/bot find messages about project alpha`

**Flow**:
1. **zoom-team-chat**: Receives search query
2. **zoom-rest-api**: Searches chat messages
3. **zoom-team-chat**: Displays results with links

## Environment Variables

```bash
# Team Chat (from zoom-team-chat skill)
ZOOM_CLIENT_ID=
ZOOM_CLIENT_SECRET=
ZOOM_BOT_JID=
ZOOM_VERIFICATION_TOKEN=
ZOOM_ACCOUNT_ID=

# LLM Integration
ANTHROPIC_API_KEY=    # or OPENAI_API_KEY

# Server
PORT=4000
```

## Advanced: Multi-Skill Integration

### With webhooks

Subscribe to meeting events and notify in Team Chat:

```javascript
// Webhook handler for meeting events
app.post('/meeting-webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.started') {
    // Notify in Team Chat
    await sendChatbotMessage(channelJid, accountId, {
      body: [
        { type: 'message', text: `Meeting "${payload.object.topic}" has started!` },
        {
          type: 'actions',
          items: [
            { text: 'Join Now', value: `join_${payload.object.id}`, style: 'Primary' }
          ]
        }
      ]
    });
  }
  
  res.status(200).send();
});
```

## Testing Checklist

- [ ] Bot responds to natural language queries
- [ ] Can create meetings from chat commands
- [ ] Meeting details sent back to Team Chat
- [ ] Buttons trigger appropriate actions
- [ ] LLM intent parsing works correctly
- [ ] Error handling for failed API calls
- [ ] Multi-turn conversation support

## Resources

- [zoom-team-chat skill](../../team-chat/SKILL.md)
- [zoom-rest-api skill](../../rest-api/SKILL.md)
- [oauth skill](../../oauth/SKILL.md)
- [Chatbot Setup Example](../../team-chat/examples/chatbot-setup.md)
- [LLM Integration Example](../../team-chat/examples/llm-integration.md)
- [Claude Chatbot Sample](https://github.com/zoom/zoom-chatbot-claude-sample)

## Next Steps

1. Build basic chatbot using [Chatbot Setup](../../team-chat/examples/chatbot-setup.md)
2. Add LLM integration
3. Implement intent parsing
4. Add REST API calls for meetings
5. Test end-to-end flow
6. Deploy to production
