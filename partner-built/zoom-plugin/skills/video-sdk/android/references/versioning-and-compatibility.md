# Android Versioning and Compatibility

## Package evidence

- SDK package: `zoom-video-sdk-android-2.5.0.zip`
- Internal version: `v2.5.0 (37500)`
- Package includes `mobilertc.aar` and sample modules.

## Compatibility notes

- Keep app and backend token logic aligned with the same Video SDK release family.
- Expect method additions/renames across releases; pin SDK version per release train.
- Revalidate proguard/R8 rules and permissions whenever upgrading.

## Contradictions or drift to watch

- Changelog points to external support portal pages, not in-package detailed notes.
- Crawl of docs subpages may miss dynamic pages; confirm against official docs at build time.
