# Common Issues and Solutions

Quick diagnostics and solutions for Zoom Team Chat development.

## Authentication Issues

### "Invalid client_id or client_secret"

**Cause**: Incorrect credentials or using wrong environment (dev vs production)

**Solution**:
1. Verify credentials in `.env` match Zoom Marketplace
2. Check you're using Development credentials (not Production)
3. Regenerate Client Secret if needed

### "Get Bot Token" returns 404 or HTML page

**Cause**: Using wrong token endpoint.

**Fix**:
- Use `https://zoom.us/oauth/token` for token exchange.
- Do not use `https://zoom.us/oauth/token` for chatbot token requests.

Quick check:
```bash
curl -X POST https://zoom.us/oauth/token \
  -H "Authorization: Basic <base64(client_id:client_secret)>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials"
```

### "Token expired"

**Cause**: Access token has expired (1 hour for user tokens)

**Solution**:
```javascript
// Implement token refresh
if (error.message.includes('token expired')) {
  const newToken = await refreshAccessToken(refreshToken);
  // Retry request with new token
}
```

### "Scope not authorized"

**Cause**: Missing required scope in app configuration

**Solution**:
1. Go to Zoom Marketplace → Your App → Scopes
2. Add missing scope (e.g., `chat_message:write`)
3. Users must re-authorize the app

## Webhook Issues

### "Cannot GET /webhook" (Browser)

**Expected Behavior**: This is NORMAL

**Explanation**: Webhooks are POST-only. Browsers send GET requests.

**Test properly**:
```bash
WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:4000"

# Use POST instead
curl -X POST "$WEBHOOK_BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{"event":"test"}'
```

### "Invalid webhook signature"

**Cause**: Mismatch between your Secret Token and Zoom's

**Solution**:
1. Verify `ZOOM_VERIFICATION_TOKEN` in `.env`
2. Check Secret Token in Zoom Marketplace → Features → Team Chat Subscriptions
3. Ensure no extra spaces/characters in token

**Debug**:
```javascript
console.log('Expected token:', process.env.ZOOM_VERIFICATION_TOKEN);
console.log('Signature from Zoom:', req.headers['x-zm-signature']);
```

### URL Validation Fails

**Cause**: Incorrect response format

**Correct response**:
```javascript
{
  "plainToken": "xyz123",
  "encryptedToken": "hmac_sha256_hash"
}
```

**Incorrect**:
```javascript
{ "success": true }  // Wrong!
```

### No Webhooks Received

**Checklist**:
- [ ] ngrok is running: `ngrok http 4000`
- [ ] Bot Endpoint URL in Zoom Marketplace matches ngrok URL
- [ ] Server is running: `node server.js`
- [ ] Slash command configured in Zoom Marketplace
- [ ] Bot installed in your account

**Test**:
```bash
# In Zoom Team Chat, type:
/yourbot test

# Should see webhook in server logs
```

## Bot JID Issues

### "Bot JID not found"

**Cause**: Chatbot feature not enabled

**Solution**:
1. Go to Zoom Marketplace → Your App → Features
2. Toggle **Chatbot** ON
3. Bot JID will appear in **Bot Credentials** section

### "Bot JID appears but messages not sending"

**Cause**: Wrong Bot JID format or environment mismatch

**Solution**:
1. Verify format: `v1abc123xyz@xmpp.zoom.us`
2. Use Development Bot JID for testing
3. Check Account ID matches the bot's account

## Message Sending Issues

### "Messages not appearing in Team Chat"

**Common causes**:

1. **Wrong `to_jid`**
   ```javascript
   // Use toJid from webhook payload
   await sendMessage(payload.toJid, accountId, content);
   ```

2. **Missing `account_id`**
   ```javascript
   // Required for chatbot messages
   {
     "account_id": process.env.ZOOM_ACCOUNT_ID,  // Don't forget!
     "robot_jid": process.env.ZOOM_BOT_JID,
     "to_jid": toJid
   }
   ```

3. **Incorrect content format**
   ```javascript
   // ❌ Wrong
   { "text": "Hello" }
   
   // ✅ Correct
   {
     "content": {
       "body": [
         { "type": "message", "text": "Hello" }
       ]
     }
   }
   ```

### "Message truncated or garbled"

**Cause**: Special characters or exceeding 4096 char limit

**Solution**:
```javascript
function sanitizeMessage(message) {
  return message
    .trim()
    .replace(/[\x00-\x1F\x7F]/g, '')  // Remove control chars
    .substring(0, 4096);                // Enforce limit
}
```

## Button/Form Issues

### "Buttons not clickable"

**Cause**: Missing `value` field

**Incorrect**:
```javascript
{
  "type": "actions",
  "items": [
    { "text": "Click Me" }  // Missing value!
  ]
}
```

**Correct**:
```javascript
{
  "type": "actions",
  "items": [
    { "text": "Click Me", "value": "clicked" }
  ]
}
```

### "Button clicks not triggering webhooks"

**Checklist**:
- [ ] Webhook handler has `interactive_message_actions` case
- [ ] Bot Endpoint URL configured correctly
- [ ] Server responding with 200 status
- [ ] Webhook signature verification passing

## ngrok Issues

### "ngrok session expired"

**Cause**: Free ngrok URLs expire after 2 hours

**Solutions**:
1. **Short-term**: Restart ngrok, update Bot Endpoint URL
2. **Long-term**: Use ngrok paid plan or deploy to production

### "ngrok URL changes every restart"

**Free plan behavior**: URL changes each time

**Solutions**:
1. Use ngrok auth token for persistent URLs (paid)
2. Use environment variable for flexibility:
   ```javascript
   const WEBHOOK_URL = process.env.WEBHOOK_URL || 'https://YOUR_PUBLIC_WEBHOOK_URL/webhook';
   ```

## Deployment Issues

### "Works locally but not in production"

**Common causes**:

1. **Environment variables not set**
   ```bash
   # Verify all vars exist
   echo $ZOOM_CLIENT_ID
   echo $ZOOM_CLIENT_SECRET
   echo $ZOOM_BOT_JID
   ```

2. **HTTP instead of HTTPS**
   - Production MUST use HTTPS
   - Zoom rejects HTTP endpoints

3. **Port binding issues**
   ```javascript
   // Use PORT from environment
    const PORT = process.env.PORT || 4000;
    ```

4. **Credentials exist, but wrong `.env` file is loaded**
   - If your app keeps per-mode env files (for example `project/team-chat-api/.env` and `project/chatbot-api/.env`), make sure runtime loads those files explicitly.
   - Verify loaded config via a health/config endpoint before debugging OAuth logic.

### `404` on `/team-chat/api/channel/*`

**Cause**: Route mismatch between old and new demo structure.

**Fix**:
- New pages should use:
  - `/team-chat/user-demo`
  - `/team-chat/bot-demo`
- Keep compatibility routes in backend if older UI still calls:
  - `/api/channel/list`
  - `/api/channel/messages`
  - `/api/channel/message`

### Browser shows `ERR_BLOCKED_BY_CLIENT`

**Cause**: Browser extension/adblock/privacy filter blocked a request.

**What to do**:
- Test in Incognito or with extensions disabled for your host.
- Confirm backend route with `curl` before treating this as server failure.

## Rate Limiting

### "Rate limit exceeded"

**Zoom Limits**:
- 10 requests/second per user
- 100 requests/second per app

**Solution**:
```javascript
// Implement exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429) {
        const delay = Math.pow(2, i) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

## General App Issues

### "App not appearing in Team Chat"

**Cause**: Team Chat surface not enabled

**Solution**:
1. Go to Zoom Marketplace → Your App → Features → Surface
2. Check **Team Chat**
3. Configure Home URL and Domain Allow List
4. Save changes

### "Users can't install the app"

**Cause**: App not in Local Test or not published

**Solutions**:
1. **For testing**: Go to Local Test → Generate Authorization URL → Share with team
2. **For production**: Submit app for Zoom review and publish

## Debugging Tools

### Log All Webhooks

```javascript
app.post('/webhook', (req, res) => {
  console.log('=== Webhook Received ===');
  console.log('Event:', req.body.event);
  console.log('Payload:', JSON.stringify(req.body.payload, null, 2));
  console.log('Headers:', req.headers);
  // ... handle webhook
});
```

### Test Token Generation

```javascript
// Test script: test-token.js
require('dotenv').config();
const { getChatbotToken } = require('./utils/auth');

(async () => {
  try {
    const token = await getChatbotToken();
    console.log('✅ Token generated successfully');
    console.log('Token:', token.substring(0, 20) + '...');
  } catch (error) {
    console.error('❌ Token error:', error.message);
  }
})();
```

### Verify Credentials

```javascript
// verify-setup.js
require('dotenv').config();

const required = [
  'ZOOM_CLIENT_ID',
  'ZOOM_CLIENT_SECRET',
  'ZOOM_BOT_JID',
  'ZOOM_VERIFICATION_TOKEN',
  'ZOOM_ACCOUNT_ID'
];

console.log('=== Credential Check ===');
required.forEach(key => {
  const value = process.env[key];
  if (!value) {
    console.error(`❌ Missing: ${key}`);
  } else {
    console.log(`✅ ${key}: ${value.substring(0, 10)}...`);
  }
});
```

## Getting Help

### Before Asking for Help

1. Check error messages in console/logs
2. Verify all credentials are correct
3. Test with curl or Postman
4. Review [official samples](https://github.com/zoom?q=chatbot)

### Where to Get Help

- [Zoom Developer Forum](https://devforum.zoom.us/)
- [GitHub Issues](https://github.com/zoom/chatbot-nodejs-quickstart/issues)
- [Developer Support](https://devsupport.zoom.us)

### Include in Support Requests

1. Zoom app type (General App OAuth)
2. Error message (full text)
3. Code snippet (sanitized - no credentials!)
4. Steps to reproduce
5. Expected vs actual behavior

## Next Steps

- [Webhook Architecture](../concepts/webhooks.md) - Deep dive into webhooks
- [Chatbot Setup](../examples/chatbot-setup.md) - Complete working example
- [API Reference](../references/api-reference.md) - Endpoint documentation
