# Zoom App Marketplace

Navigate the Zoom Marketplace developer portal.

## Overview

The [Zoom App Marketplace](https://marketplace.zoom.us/) is where you create, configure, and publish Zoom apps.

## Getting Started

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/)
2. Sign in with your Zoom account
3. Click **Develop** → **Build App**
4. Choose app type
5. Configure app settings

## Portal Sections

### Develop

- **Build App** - Create new apps
- **Manage** - Edit existing apps
- **Logs** - View API and webhook logs

### App Configuration

| Section | Purpose |
|---------|---------|
| **App Credentials** | SDK Key/Secret, Client ID/Secret |
| **Scopes** | Configure OAuth permissions |
| **Feature** | Enable Meeting SDK, Video SDK, Webhooks |
| **Activation** | Make app installable |

## SDK Downloads

**Important:** Meeting SDK and Video SDK must be downloaded from Marketplace after signing in. They are not available on public package managers (except Web SDKs via npm).

1. Go to your app's **Download** section
2. Select platform (iOS, Android, Windows, macOS, Linux)
3. Download SDK package

## Credentials

### OAuth Apps

- **Client ID** - Public identifier
- **Client Secret** - Keep secret, server-side only

### SDK Apps

- **SDK Key** - Used in JWT payload
- **SDK Secret** - Used to sign JWT, keep secret

## Publishing

To publish to Marketplace:

1. Complete app configuration
2. Submit for review
3. Address feedback
4. Get approved
5. Go live

## Resources

- **Marketplace**: https://marketplace.zoom.us/
- **Developer docs**: https://developers.zoom.us/
