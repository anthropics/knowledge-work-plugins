# Unity Versioning and Compatibility

## Package evidence

- Wrapper package: `unity-zoom-video-sdk-0.0.2-beta.zip`
- Contains `ZoomVideoSDK.unitypackage` wrapper bundle.

## Compatibility notes

- Unity wrapper versioning is independent from native Android/iOS/macOS SDK streams.
- Validate each API/event used in wrapper reference docs before implementation.
- Treat wrapper as potentially partial feature surface versus native SDKs.

## Contradictions or drift to watch

- Wrapper release (`0.0.2-beta`) is substantially behind native 2.5.0 package family.
- Some docs and feature names may differ between wrapper and native platform references.
