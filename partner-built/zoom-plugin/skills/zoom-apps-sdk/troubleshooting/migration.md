# SDK Version Migration

Notes on upgrading @zoom/appssdk versions and handling deprecations.

## Current Version

**Recommended:** `@zoom/appssdk` v0.16.26+ (latest stable)

```json
{
  "dependencies": {
    "@zoom/appssdk": "^0.16.26"
  }
}
```

## Version Pinning Strategy

| Strategy | package.json | Risk | Use When |
|----------|-------------|------|----------|
| **Exact** | `"0.16.26"` | Lowest | Production apps, critical stability |
| **Patch** | `"~0.16.26"` | Low | Most apps |
| **Minor** | `"^0.16.26"` | Medium | Active development |

## Checking API Availability at Runtime

Not all APIs are available in all Zoom client versions. Always check:

```javascript
const { supportedApis } = await zoomSdk.getSupportedJsApis();

// Check before using an API
if (supportedApis.includes('authorize')) {
  // Safe to use In-Client OAuth
  await zoomSdk.authorize({...});
} else {
  // Fall back to web redirect OAuth
  window.location.href = '/install';
}
```

Also check `unsupportedApis` after `config()`:

```javascript
const config = await zoomSdk.config({
  capabilities: ['authorize', 'getMeetingContext', 'newFeature'],
  version: '0.16'
});

if (config.unsupportedApis.includes('newFeature')) {
  console.log('newFeature not available in this client version');
  // Graceful degradation
}
```

## Config Version Parameter

The `version` parameter in `config()` indicates which SDK API version you expect:

```javascript
await zoomSdk.config({
  capabilities: [...],
  version: '0.16'  // API version, not NPM package version
});
```

This helps Zoom maintain backward compatibility. Use the latest supported version.

## Sample App SDK Versions

Status of official sample repositories:

| Repository | SDK Version | Status | Notes |
|-----------|-------------|--------|-------|
| zoomapps-sample-js | ^0.16.26 | Current | Best reference |
| zoomapps-advancedsample-react | 0.16.0 | Outdated | Works but update recommended |
| zoomapps-customlayout-js | ^0.16.8 | Outdated | Layers API may differ |
| zoomapps-texteditor-vuejs | ^0.16.7 | Outdated | Y.js pattern still valid |
| zoomapps-serverless-vuejs | ^0.16.21 | Slightly outdated | Firebase pattern still valid |

## Deprecation Pattern

Zoom typically deprecates APIs gradually:
1. API marked deprecated in docs
2. `unsupportedApis` starts returning it in newer clients
3. API stops working in future client versions

**Best practice:** Check `getSupportedJsApis()` at startup and implement fallbacks.

## Migration Checklist

When upgrading SDK version:

- [ ] Update `@zoom/appssdk` in package.json
- [ ] Run `npm install`
- [ ] Check changelog for breaking changes
- [ ] Test all capabilities in Zoom client
- [ ] Verify `getSupportedJsApis()` includes your APIs
- [ ] Test in both meeting and main client contexts
- [ ] Test browser preview fallback still works
- [ ] Update `version` parameter in `config()` if needed

## Resources

- **NPM package**: https://www.npmjs.com/package/@zoom/appssdk
- **Changelog**: https://github.com/zoom/appssdk/releases
