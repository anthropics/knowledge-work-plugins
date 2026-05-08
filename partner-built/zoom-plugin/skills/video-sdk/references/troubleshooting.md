# Video SDK - Troubleshooting

Common issues and solutions for Video SDK.

## Overview

Troubleshooting guide for Video SDK across all platforms.

## Common Issues

### Join Session Failed

| Error | Possible Cause | Solution |
|-------|----------------|----------|
| Invalid signature | JWT malformed or expired | Regenerate signature server-side |
| Session not found | Topic mismatch | Verify topic matches exactly |
| Auth failed | Invalid SDK credentials | Check SDK Key/Secret |

**Note:** Error code 0 often means success - check the SDK enum values.

### No Video

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Black screen | Permission denied | Request camera permission |
| Video not starting | Camera in use | Close other apps using camera |
| Poor quality | Bandwidth limited | Check network connection |

### No Audio

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Can't hear others | Audio not started | Call `startAudio()` |
| Others can't hear me | Microphone permission | Request mic permission |
| Echo | Speaker feedback | Use headphones |

### Web-Specific Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| SharedArrayBuffer error | Missing headers | Add COOP/COEP headers |
| WebRTC issues | Browser incompatibility | Check browser support |
| Performance issues | Too many video streams | Reduce participants or resolution |

## Collecting Logs

See [SDK Logs & Troubleshooting](../../general/references/sdk-logs-troubleshooting.md) for log collection.

## Getting Support

1. Collect SDK logs
2. Note SDK version and platform
3. Document steps to reproduce
4. Contact [Developer Support](https://devsupport.zoom.us/)

## Resources

- **Developer forum**: https://devforum.zoom.us/
- **Support**: https://devsupport.zoom.us/
