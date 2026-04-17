# Environment Setup

Complete guide to configuring your Zoom Team Chat development environment, obtaining credentials, and setting up your app.

## Prerequisites

- Zoom account
- Account owner, admin, or **Zoom for developers** role enabled

### Enable "Zoom for developers" Role

If you don't have owner/admin privileges:

1. Ask your admin to enable the **Zoom for developers** role
2. Navigate to: **User Management** → **Roles** → **Role Settings** → **Advanced features**
3. Enable **View** and **Edit** checkboxes for **Zoom for developers**

![Zoom for developers role](https://developers.zoom.us/img/nextImageExportOptimizer/UBF-role-prerequisite-opt-1080.WEBP)

## Step 1: Create Zoom App

### 1.1 Access App Marketplace

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**

### 1.2 Select App Type

**Select**: **General App** (OAuth)

> ⚠️ **CRITICAL**: Do NOT select "Server-to-Server OAuth"
> 
> **Why**: Server-to-Server OAuth apps do NOT support the Team Chat/Chatbot features. Only General App (OAuth) supports chatbots and team chat integrations.

## Step 2: Basic Information

On the **Basic Info** page, configure your app:

### 2.1 App Name

Update the auto-generated app name:
- Click the edit icon (pencil)
- Enter your app name (e.g., "My Team Chat Bot")
- Click outside the field to save

### 2.2 App Management Type

Choose how your app is managed:

| Type | Use Case | Token Flow |
|------|----------|------------|
| **Admin-managed** | Company-wide bots, notifications, helpdesk | Recommended for chatbots |
| **User-managed** | Personal bots, individual user tools | For user-specific apps |

**For most chatbots**: Choose **Admin-managed**

**Important**: App management type affects available features and scopes. If you change it later, reconfirm your selected features and scopes.

### 2.3 App Credentials (Auto-generated)

The build flow automatically generates:

| Credential | Environment |
|------------|-------------|
| **Client ID** | Development & Production |
| **Client Secret** | Development & Production |

**Note**: Development and production credentials are different.

### 2.4 OAuth Information

#### OAuth Redirect URL (Required)

Enter your OAuth callback endpoint:

**Local development**:
```
http://YOUR_DEV_HOST:4000/auth/callback
```

**Production**:
```
https://yourdomain.com/auth/callback
```

#### OAuth Allow Lists (Required)

Add all URLs that Zoom should allow as valid OAuth redirects:

**Examples**:
- Complete URL: `https://subdomain.domain.tld/path/oauth/callback`
- Base URL: `https://subdomain.domain.tld`

## Step 3: Enable Team Chat (Chatbot API Only)

> **Skip this step** if you're only using Team Chat API (user-level messaging)

### 3.1 Navigate to Features Page

Go to **Features** page → **Surface** tab

### 3.2 Select Team Chat Product

In **Select where to use your app**, check **Team Chat**

### 3.3 Configure App URLs

| Field | Value | Example |
|-------|-------|---------|
| **Home URL** | Your app's home page | `https://yourdomain.com` |
| **Domain Allow List** | URLs Zoom client should accept | `https://yourdomain.com` |

### 3.4 Enable Team Chat Subscription

Configure webhook settings:

| Field | Value | Example |
|-------|-------|---------|
| **Slash Command** | Command to invoke bot | `/mybot` |
| **Bot Endpoint URL** | Webhook endpoint | `https://yourdomain.com/webhook` |

> **Critical**: Your bot will NOT appear in Team Chat unless you enable Team Chat Subscription!

## Step 4: Get Credentials

### 4.1 App Credentials (Both APIs)

Navigate to **App Credentials** → **Development**:

| Credential | Where to Find |
|------------|---------------|
| **Client ID** | App Credentials → Development |
| **Client Secret** | App Credentials → Development (Click "View") |
| **Account ID** | App Credentials → Development |

### 4.2 Bot JID (Chatbot API Only)

> **Note**: Bot JID only appears AFTER enabling Chatbot in Features tab

**To find Bot JID**:

1. Go to **Features** tab in left sidebar
2. Ensure **Chatbot** toggle is **ON**
3. Click **Chatbot** section to expand
4. Scroll to **Bot Credentials** section
5. You'll see two JIDs:
   - **Bot JID (Development)**: Use for testing
   - **Bot JID (Production)**: Use for live apps

**Format**: `v1abc123xyz@xmpp.zoom.us`

### 4.3 Webhook Secret Token (Chatbot API Only)

Navigate to **Features** → **Team Chat Subscriptions** → **Secret Token**

This token is used to verify webhook signatures.

### 4.4 Credentials Summary

| Credential | Team Chat API | Chatbot API | Location |
|------------|---------------|-------------|----------|
| Client ID | ✅ Required | ✅ Required | App Credentials → Development |
| Client Secret | ✅ Required | ✅ Required | App Credentials → Development |
| Account ID | ❌ | ✅ Required | App Credentials → Development |
| Bot JID | ❌ | ✅ Required | Features → Chatbot → Bot Credentials |
| Secret Token | ❌ | ✅ Required | Features → Team Chat Subscriptions |

## Step 5: Configure Scopes

Navigate to **Scopes** page in your app.

### Team Chat API Scopes

Manually add these scopes:

- `chat_message:write` - Send messages
- `chat_message:read` - Read messages
- `chat_channel:read` - List channels
- `chat_channel:write` - Create/manage channels

### Chatbot API Scopes

When you enable Team Chat Subscription, these scopes are **automatically added**:

- `imchat:bot` - Basic chatbot functionality
- `team_chat:read:list_user_channels:admin` - List channels
- `team_chat:read:list_members:admin` - List members

## Step 6: Create .env File

### For Team Chat API (User-Level)

```bash
# .env file
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_REDIRECT_URI=http://YOUR_DEV_HOST:4000/auth/callback

PORT=4000
```

### For Chatbot API (Bot-Level)

```bash
# .env file
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_BOT_JID=v1abc123xyz@xmpp.zoom.us
ZOOM_VERIFICATION_TOKEN=your_webhook_secret_token
ZOOM_ACCOUNT_ID=your_account_id

PORT=4000
```

### .env.example Template

Create this file in your project root:

```bash
# Zoom App Credentials (Required for both APIs)
ZOOM_CLIENT_ID=
ZOOM_CLIENT_SECRET=
ZOOM_REDIRECT_URI=http://YOUR_DEV_HOST:4000/auth/callback

# Chatbot Credentials (Required for Chatbot API only)
ZOOM_BOT_JID=
ZOOM_VERIFICATION_TOKEN=
ZOOM_ACCOUNT_ID=

# Server Configuration
PORT=4000
```

## Step 7: Test Your App

On the **Local Test** page:

### 7.1 Add App to Your Account

1. Click **Add App Now**
2. Click **Allow** to authorize the app
3. You'll be redirected to your OAuth redirect URL

### 7.2 Preview App Listing

Click **Preview Your App Listing Page** to see how your app appears in the marketplace.

### 7.3 Share with Team Members

To share your app with other users on your account:

1. Go to **Authorization URL** section
2. Click **Generate**
3. Click **Copy**
4. Share the URL with your team members

> **Note**: Beta apps can only be installed by members of the developer's Zoom account (security restriction).

## Common Setup Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Bot JID not visible | Chatbot feature not enabled | Go to Features tab, toggle Chatbot ON |
| Can't find Secret Token | Team Chat Subscription not enabled | Enable Team Chat Subscription in Features → Surface |
| OAuth redirect error | Redirect URL not in allow list | Add full redirect URL to OAuth allow lists |
| Scopes not appearing | Wrong app type | Verify you created General App (OAuth), not S2S |
| App can't be added | Missing required configuration | Complete all steps in Basic Info and Features |

## Verification Checklist

Before proceeding to development, verify:

- [ ] Created **General App (OAuth)** (not Server-to-Server)
- [ ] Selected appropriate App Management Type
- [ ] Configured OAuth redirect URL
- [ ] Added URLs to OAuth allow lists
- [ ] Enabled Team Chat in Surface tab (for chatbots)
- [ ] Configured Team Chat Subscription (for chatbots)
- [ ] Added all required scopes
- [ ] Obtained all required credentials
- [ ] Created .env file with credentials
- [ ] Successfully added app to your account

## Next Steps

### For Team Chat API:
1. [Authentication Flows](authentication.md) - Understand OAuth
2. [OAuth Setup Example](../examples/oauth-setup.md) - Implement OAuth
3. [Send Message Example](../examples/send-message.md) - Send first message

### For Chatbot API:
1. [Webhook Architecture](webhooks.md) - Understand webhooks
2. [Chatbot Setup Example](../examples/chatbot-setup.md) - Build your bot
3. [Message Cards Reference](../references/message-cards.md) - Create rich messages

## Resources

- [Zoom App Marketplace](https://marketplace.zoom.us/)
- [OAuth Documentation](https://developers.zoom.us/docs/integrations/oauth/)
- [Chatbot Documentation](https://developers.zoom.us/docs/team-chat/chatbot/extend/)
- [Using Role Management](https://support.zoom.us/hc/en-us/articles/115001078646)
