# Message Card Components Reference

Complete reference for building rich interactive messages in Zoom Team Chat chatbots.

## Card Structure

Every chatbot message has this structure:

```javascript
{
  "content": {
    "head": {          // Optional header
      "text": "Title",
      "sub_head": { "text": "Subtitle" }
    },
    "body": [          // Array of components
      { "type": "message", "text": "Content" },
      { "type": "actions", "items": [...] }
      // ... more components
    ]
  }
}
```

## Components Catalog

### Text Components

#### message
Plain text content.

```javascript
{
  "type": "message",
  "text": "Hello, this is plain text"
}
```

#### header  
Title text with optional styling.

```javascript
{
  "type": "header",
  "text": "Main Heading",
  "style": {
    "bold": true,
    "italic": false
  }
}
```

#### styled_text
Text with markdown-like styling.

```javascript
{
  "type": "styled_text",
  "text": "**Bold** *italic* `code`"
}
```

### Interactive Components

#### actions (Buttons)
Clickable buttons that trigger webhooks.

```javascript
{
  "type": "actions",
  "items": [
    {
      "text": "Approve",
      "value": "approve",
      "style": "Primary"      // Primary, Danger, Default
    },
    {
      "text": "Reject",
      "value": "reject",
      "style": "Danger"
    }
  ]
}
```

**Styles**:
- `Primary` - Blue button
- `Danger` - Red button
- `Default` - Gray button

#### dropdown
Select menu with options.

```javascript
{
  "type": "dropdown",
  "select_items": [
    { "text": "Option 1", "value": "opt1" },
    { "text": "Option 2", "value": "opt2" }
  ]
}
```

#### form_field
Text input field.

```javascript
{
  "type": "form_field",
  "editable": true,
  "text": "Enter your name"
}
```

### Layout Components

#### section
Group components with optional colored sidebar.

```javascript
{
  "type": "section",
  "sidebar_color": "#3b82f6",      // Hex color
  "sections": [
    { "type": "message", "text": "Grouped content" }
  ]
}
```

**Common colors**:
- Success: `#10b981` (green)
- Error: `#ef4444` (red)
- Warning: `#f59e0b` (orange)
- Info: `#3b82f6` (blue)

#### fields
Key-value pairs displayed in columns.

```javascript
{
  "type": "fields",
  "items": [
    { "key": "Status", "value": "Active" },
    { "key": "Priority", "value": "High" },
    { "key": "Assignee", "value": "John Doe" }
  ]
}
```

#### divider
Horizontal line separator.

```javascript
{
  "type": "divider"
}
```

### Media Components

#### attachments
Image with optional link.

```javascript
{
  "type": "attachments",
  "img_url": "https://example.com/image.jpg",
  "resource_url": "https://example.com/full-page",
  "information": {
    "title": { "text": "Image Title" },
    "description": { "text": "Click to view" }
  }
}
```

## Complete Examples

### Build Notification

```javascript
{
  "content": {
    "head": {
      "text": "Build #123 Complete",
      "sub_head": { "text": "main branch" }
    },
    "body": [
      {
        "type": "section",
        "sidebar_color": "#10b981",
        "sections": [
          { "type": "message", "text": "✅ Build completed successfully" }
        ]
      },
      {
        "type": "fields",
        "items": [
          { "key": "Branch", "value": "main" },
          { "key": "Commit", "value": "abc123" },
          { "key": "Duration", "value": "2m 34s" }
        ]
      },
      {
        "type": "actions",
        "items": [
          { "text": "View Logs", "value": "view_logs", "style": "Primary" },
          { "text": "Deploy", "value": "deploy", "style": "Default" }
        ]
      }
    ]
  }
}
```

### Approval Request

```javascript
{
  "content": {
    "head": {
      "text": "Expense Approval Required"
    },
    "body": [
      { "type": "message", "text": "John Doe submitted an expense report" },
      {
        "type": "fields",
        "items": [
          { "key": "Amount", "value": "$500.00" },
          { "key": "Category", "value": "Travel" },
          { "key": "Date", "value": "Feb 9, 2026" }
        ]
      },
      { "type": "divider" },
      {
        "type": "actions",
        "items": [
          { "text": "Approve", "value": "approve_500", "style": "Primary" },
          { "text": "Reject", "value": "reject_500", "style": "Danger" },
          { "text": "View Details", "value": "details_500", "style": "Default" }
        ]
      }
    ]
  }
}
```

### Error Notification

```javascript
{
  "content": {
    "head": {
      "text": "⚠️ Service Alert"
    },
    "body": [
      {
        "type": "section",
        "sidebar_color": "#ef4444",
        "sections": [
          { "type": "message", "text": "Database connection failed" }
        ]
      },
      {
        "type": "fields",
        "items": [
          { "key": "Service", "value": "api-prod" },
          { "key": "Error", "value": "Connection timeout" },
          { "key": "Time", "value": "2026-02-09 18:30:00 UTC" }
        ]
      },
      {
        "type": "actions",
        "items": [
          { "text": "View Logs", "value": "logs", "style": "Primary" },
          { "text": "Acknowledge", "value": "ack", "style": "Default" }
        ]
      }
    ]
  }
}
```

## Limitations

| Component | Limit |
|-----------|-------|
| Message text | 4,096 characters |
| Button text | 40 characters |
| Field key/value | 256 characters each |
| Dropdown options | 100 options |
| Buttons per message | 5 buttons |

## Best Practices

### Button Design
✅ **DO**: Use clear, action-oriented labels
- "Approve Request"
- "View Details"
- "Cancel Order"

❌ **DON'T**: Use vague labels
- "OK"
- "Click Here"
- "Button"

### Color Usage
✅ **DO**: Use semantic colors
- Green (`#10b981`) for success
- Red (`#ef4444`) for errors/destructive actions
- Blue (`#3b82f6`) for info
- Orange (`#f59e0b`) for warnings

❌ **DON'T**: Use random colors without meaning

### Field Formatting
✅ **DO**: Keep keys concise, values informative
```javascript
{ "key": "Status", "value": "Active" }
```

❌ **DON'T**: Make keys too long
```javascript
{ "key": "The current status of the request", "value": "Active" }
```

## Testing Cards

Use the [Team Chat App Card Builder](https://appssdk.zoom.us/cardbuilder/) to:
- Preview card designs
- Test layouts
- Generate JSON

## Next Steps

- [Chatbot Setup](../examples/chatbot-setup.md) - Build your first bot
- [Button Actions](../examples/button-actions.md) - Handle button clicks
- [Webhook Events](webhook-events.md) - Understand webhook payloads

## Resources

- [Official Card Components](https://developers.zoom.us/docs/team-chat/customizing-messages/)
- [App Card Builder](https://appssdk.zoom.us/cardbuilder/)
- [Sample Chatbots](https://github.com/zoom?q=chatbot)
