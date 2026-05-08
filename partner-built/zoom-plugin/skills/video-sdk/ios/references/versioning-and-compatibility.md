# iOS Versioning and Compatibility

## Package evidence

- SDK package: `zoom-video-sdk-iOS-2.5.0.zip`
- Internal version file: `v2.5.0(33006)`
- Changelog is externally hosted via developer support portal.

## Compatibility notes

- Keep iOS SDK and backend token claims aligned to same release train.
- Recheck Swift/ObjC bridge and framework embedding settings on upgrade.
- Audit deprecated APIs from the iOS reference when moving minor/major versions.

## Contradictions or drift to watch

- Changelog content is not bundled in package; release details are external.
- Copyright footer differs across packages (iOS bundle includes 2025).
