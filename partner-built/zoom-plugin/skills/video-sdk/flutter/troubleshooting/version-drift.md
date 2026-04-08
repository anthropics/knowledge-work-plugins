# Version Drift

Flutter wrapper, native SDKs, and docs can drift independently.

## Upgrade checklist

1. Compare wrapper version metadata and changelog with actual package content.
2. Re-validate API enum names and helper method signatures.
3. Re-test lifecycle: init -> join -> media -> leave -> cleanup.
4. Re-check event constants and error handling mappings.
5. Re-run smoke tests for chat/share/recording/transcription if used.
