# Version Drift

React Native wrapper, native Video SDKs, and docs may drift independently.

## Upgrade checklist

1. Compare wrapper package version and exported type signatures.
2. Re-check join config/property names and enum constants.
3. Re-test full lifecycle: init -> join -> media/helper calls -> leave -> cleanup.
4. Re-validate event types used in app listeners.
5. Re-run smoke tests on both iOS and Android.
