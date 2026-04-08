# Native Video SDK Multi-Platform Delivery

## Goal

Ship one product experience across Android, iOS, macOS, and Unity while keeping token auth, session behavior, and upgrade policies aligned.

## Skills to chain

- [zoom-video-sdk](../../video-sdk/SKILL.md)
- [zoom-video-sdk-android](../../video-sdk/android/SKILL.md)
- [zoom-video-sdk-ios](../../video-sdk/ios/SKILL.md)
- [zoom-video-sdk-macos](../../video-sdk/macos/SKILL.md)
- [zoom-video-sdk-unity](../../video-sdk/unity/SKILL.md)
- [zoom-oauth](../../oauth/SKILL.md)

## Recommended delivery model

1. Standardize backend token service contract (`sessionName`, `userName`, role/claims).
2. Keep platform session state machines consistent (init -> join -> media -> leave).
3. Version-lock each platform release and run compatibility checks before rollout.
4. Maintain per-platform fallback plans for renamed/deprecated APIs.

## Failure modes to pre-plan

- Wrapper/native feature mismatch (especially Unity).
- Event naming drift across SDK versions.
- Token claim changes that break only one platform.
- Permission/regression differences per OS release.

## Output checklist

- Shared auth/token contract spec
- Platform-specific session lifecycle docs
- Upgrade runbook with rollback plan
- Known incompatibility matrix
