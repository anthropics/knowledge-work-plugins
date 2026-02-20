# OpenClaw Integration: Shadow Marketing

This document explains how to use **OpenClaw** to automate your personal branding and "Shadow Marketing" outside of corporate oversight.

## Why use OpenClaw?

As an independent contractor, your personal brand is your most valuable asset. While agency marketing focus on the corporate brand, OpenClaw allows you to:
1.  **Own your content**: Draft and post to your *personal* LinkedIn, Instagram, and TikTok profiles.
2.  **Bypass approval loops**: Publish "Coming Soon" or "Just Sold" teasers instantly.
3.  **Maintain consistency**: Keep your personal brand alive even if you switch agencies.

## Setup Instructions

1.  **Configure Connector**: In your private admin account, map `~~social media` to your OpenClaw server URL.
2.  **API Keys**: Store your personal social media API keys (LinkedIn, Twitter/X, etc.) within your OpenClaw instance.
3.  **ToV Sync**: Ensure your "Tone of Voice" profile in `marketing-suite` is synced with your OpenClaw templates.

## Workflows

### 1. The "Sneak Peek" Teaser
When a property is updated in Vault RE (via webhook), use `/draft-listing` to generate a personal teaser.
- **Goal**: Build a "Shadow Buyer List" before the corporate campaign launches.
- **Connector**: OpenClaw drafts the post and schedules it for your personal LinkedIn.

### 2. The "Community Expert" Pulse
OpenClaw can monitor local suburb hashtags (e.g., #LowerHuttRealEstate).
- **Goal**: Identify and engage with potential vendors early.
- **Workflow**: OpenClaw flags relevant posts -> Gemini Pro suggests a "shadow comment" -> You approve via your private Workspace.

### 3. "Just Sold" Proof of Concept
Immediately upon settlement milestone:
- **Action**: OpenClaw posts a "Verified Result" to your personal Instagram story.
- **Why**: Proves your individual track record to your private database.

## Connector Configuration (`.mcp.json`)

```json
{
  "mcpServers": {
    "openclaw": {
      "type": "http",
      "url": "https://your-private-openclaw-instance.com/api"
    }
  }
}
```
