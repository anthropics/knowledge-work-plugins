# SDK Upgrade Guide

Guide for upgrading Meeting SDK and Video SDK versions.

For customer upgrades from older versions to latest, use:
- [sdk-upgrade-workflow.md](sdk-upgrade-workflow.md) - changelog + RSS, version-by-version migration workflow.

## IMPORTANT: Check the Changelog First

**Before any upgrade, always check the official Zoom changelog:**

**Primary URL**: https://developers.zoom.us/changelog/

If the above URL is unavailable or has moved, search for **"zoom changelog"** or **"zoom developer changelog"** to find the current location.

The changelog contains:
- Latest SDK versions and release dates
- Breaking changes and deprecations
- New features and improvements
- Bug fixes and security patches

## Overview

Zoom releases SDK updates regularly. This guide covers version policy and upgrade procedures.

## Version Policy

- **Major versions** - May contain breaking changes
- **Minor versions** - New features, backward compatible
- **Patch versions** - Bug fixes

## Before Upgrading

1. Read changelog for target version
2. Note breaking changes and deprecations
3. Test in development environment
4. Plan migration for deprecated APIs

## Upgrade Steps

### Web SDK (npm)

```bash
# Check current version
npm list @zoom/meetingsdk

# Update to latest
npm update @zoom/meetingsdk

# Or specific version
npm install @zoom/meetingsdk@2.18.0
```

### Native SDKs

1. Download new SDK from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
2. Replace SDK files in your project
3. Update linker/framework settings if needed
4. Rebuild project

## Common Migration Tasks

### API Signature Changes

When methods change signatures between versions:

```javascript
// Old (v2.x)
client.join({
  sdkKey: key,
  sdkSecret: secret,  // REMOVED in v3.x
  meetingNumber: number
});

// New (v3.x) - signature generated server-side
client.join({
  sdkKey: key,
  signature: serverGeneratedSignature,  // NEW
  meetingNumber: number
});
```

**Action**: Update to server-side signature generation for security.

### Deprecated Method Replacements

| Old Method | New Method | Version |
|------------|------------|---------|
| `ZoomMtg.init()` | `client.init()` | Web SDK 3.x |
| `startVideo()` | `startVideo()` + `renderVideo()` | Video SDK 1.8+ |
| `getMeetingUUID()` | Use webhook payload | Meeting SDK 2.x |

### New Initialization Requirements

**Meeting SDK Web 3.x**:
```javascript
// Now requires explicit preload
import ZoomMtgEmbedded from '@zoom/meetingsdk/embedded';

const client = ZoomMtgEmbedded.createClient();

// Must init before join
await client.init({
  zoomAppRoot: document.getElementById('root'),
  language: 'en-US'
});
```

**Video SDK 1.8+**:
```javascript
// Video rendering is now two-step
await stream.startVideo();
await stream.renderVideo(
  document.querySelector('#video-canvas'),
  myUserId,
  1280, 720, 0, 0, 3  // width, height, x, y, quality
);
```

### Breaking Changes Checklist

When upgrading major versions, check:

- [ ] Initialization flow changed?
- [ ] Authentication method changed?
- [ ] Event names/signatures changed?
- [ ] Required permissions changed?
- [ ] Minimum platform version changed?
- [ ] New required headers (COOP/COEP)?

### Testing Upgrade

```bash
# Create upgrade branch
git checkout -b sdk-upgrade-v3

# Update package
npm install @zoom/meetingsdk@latest

# Run tests
npm test

# Test manually
# - Join meeting
# - Audio/video functionality
# - Screen sharing
# - Recording (if used)
# - Custom UI features
```

## Version Support Policy

- **Latest version**: Full support
- **Previous major**: Security fixes only
- **Older versions**: No support, upgrade recommended

## Resources

- **Main Changelog**: https://developers.zoom.us/changelog/ (check here first!)
- **Meeting SDK changelog**: https://developers.zoom.us/changelog/meeting-sdk/
- **Video SDK changelog**: https://developers.zoom.us/changelog/video-sdk/
- **Migration guides**: https://developers.zoom.us/docs/meeting-sdk/web/migrate/

> **Note for LLMs/Agents**: If the changelog URLs return 404 or have moved, perform a web search for "zoom developer changelog" or "zoom sdk changelog" to find the current location. Zoom occasionally restructures their documentation.
