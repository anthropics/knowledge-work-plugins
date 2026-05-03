# Zoom Mail Integration

Integrate with Zoom Mail via REST API and Zoom Apps SDK for mail plugins.

## Overview

**Important**: There is no standalone "ZMail JS SDK". Zoom Mail integration uses:
1. **Zoom Mail REST API** - Server-side email operations
2. **Zoom Apps SDK** - Build mail plugins that run inside Zoom client

## Prerequisites

- Zoom Workplace Pro, Standard Pro, Business, or Enterprise account
- Zoom Mail enabled (Pro accounts have it by default; Business/Enterprise must enable)
- OAuth app with mail scopes

## Zoom Mail REST API

### Base URL

```
https://api.zoom.us/v2/emails
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/emails/mailboxes/{email}/messages/send` | Send a message |
| POST | `/emails/mailboxes/{email}/messages` | Create/add message to mailbox |
| POST | `/emails/mailboxes/{email}/drafts` | Create draft |
| POST | `/emails/mailboxes/{email}/labels` | Create label |
| GET | `/emails/mailboxes/me/profile` | Get mailbox profile |

### Send Email Example

Emails must be in RFC 2822 format, base64 encoded:

```javascript
// Generate RFC 2822 compliant message
function generateEmailMessage(from, to, subject, body) {
  const message = `From: ${from}\nTo: ${to}\nSubject: ${subject}\n\n${body}`;
  return btoa(message);  // Base64 encode
}

// Send email via API
async function sendEmail(mailbox, toEmail, subject, body) {
  const encodedMessage = generateEmailMessage(mailbox, toEmail, subject, body);
  
  const response = await fetch(
    `https://api.zoom.us/v2/emails/mailboxes/${mailbox}/messages/send`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        raw: encodedMessage
      })
    }
  );
  
  return response.json();
}

// Usage
await sendEmail(
  'sender@company.zmail.com',
  'recipient@example.com',
  'Meeting Follow-up',
  'Thank you for attending today\'s meeting.'
);
```

### Create Draft

```javascript
async function createDraft(mailbox, to, subject, body) {
  const encodedMessage = generateEmailMessage(mailbox, to, subject, body);
  
  await fetch(
    `https://api.zoom.us/v2/emails/mailboxes/${mailbox}/drafts`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        raw: encodedMessage
      })
    }
  );
}
```

### Get Mailbox Profile

```javascript
const profile = await fetch(
  'https://api.zoom.us/v2/emails/mailboxes/me/profile',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
).then(r => r.json());

console.log('Email:', profile.email);
```

## Zoom Apps SDK - Mail Plugins

Build apps that run inside Zoom Mail tab using Zoom Apps SDK.

### Installation

```bash
npm install @zoom/appssdk
```

Or via CDN:
```html
<script src="https://appssdk.zoom.us/sdk.js"></script>
```

### Initialize for Mail Context

```javascript
// IMPORTANT: Do NOT declare "let zoomSdk" - causes redeclaration error
// The SDK defines window.zoomSdk globally
let sdk = window.zoomSdk;

async function init() {
  try {
    const configResponse = await sdk.config({
      popout: true,
      capabilities: ['insertContentToMailActiveEditor'],
      version: '0.16'
    });
    
    console.log('Running in context:', configResponse.runningContext);
    // Will be "mailTab" when running in Zoom Mail
  } catch (error) {
    console.error('Not running inside Zoom client:', error);
  }
}
```

### Insert Content to Mail Editor

Insert HTML content into the active mail composer:

```javascript
// Insert content into mail editor (must comply with Tiptap HTML specs)
await sdk.insertContentToMailActiveEditor({
  html: '<p>This content will be inserted into the email body.</p>'
});
```

### Mail Plugin Use Cases

| Use Case | Description |
|----------|-------------|
| **Email Templates** | Insert pre-built email templates |
| **Signature Manager** | Dynamic email signatures |
| **Meeting Links** | Auto-insert Zoom meeting links |
| **CRM Integration** | Pull contact info into emails |
| **Translation** | Translate email content |

## Authentication

### Server-to-Server OAuth (for REST API)

```javascript
async function getAccessToken() {
  const response = await fetch('https://zoom.us/oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + btoa(`${clientId}:${clientSecret}`),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  });
  
  const data = await response.json();
  return data.access_token;  // Valid for 1 hour
}
```

## Required Scopes

| Scope | Description |
|-------|-------------|
| `mail:read` | Read mailbox data |
| `mail:write` | Send emails, create drafts |
| `mail:read:admin` | Admin read access |
| `mail:write:admin` | Admin write access |

## Limitations

| Limitation | Notes |
|------------|-------|
| Account requirement | Zoom Workplace Pro+ with Zoom Mail |
| Email format | Must be RFC 2822 compliant, base64 encoded |
| Plugin context | Zoom Apps SDK mail features only work in Mail tab |
| HTML in editor | Must comply with Tiptap specifications |

## Resources

- **Zoom Mail API Docs**: https://developers.zoom.us/docs/api/rest/zoom-mail/
- **Zoom Mail Overview**: https://developers.zoom.us/docs/mail/
- **Zoom Apps SDK**: https://github.com/zoom/appssdk
- **NPM Package**: https://www.npmjs.com/package/@zoom/appssdk
- **Sample Implementation**: https://github.com/Wrightlab1/ZoomMailAPI
