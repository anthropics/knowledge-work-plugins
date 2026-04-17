# Rivet Versioning and Compatibility

## Upgrade Strategy

Use the standard upgrade workflow:
- [../../general/references/sdk-upgrade-workflow.md](../../general/references/sdk-upgrade-workflow.md)

For Rivet, treat upgrades as three parallel checks:
1. `@zoom/rivet` package release changes
2. Underlying Zoom API/event payload changes
3. Marketplace app config and scope changes

## Compatibility Risks

- Module/auth behavior drift across versions.
- Type alias or endpoint wrapper signature changes.
- Event payload shape differences for webhook types.
- Receiver behavior changes in Node runtime/Lambda environments.

## Version Signals

- `@zoom/rivet` package version in `package.json`.
- TypeDoc module/classes/type aliases under `zoom.github.io/rivet-javascript`.
- Changelog updates under https://developers.zoom.us/changelog/.

## Safe Upgrade Checklist

- Pin current and target `@zoom/rivet` versions.
- Compare TypeDoc module pages for changed constructor options and endpoints.
- Validate event names and payload fields used by your handlers.
- Revalidate OAuth install/callback flow and token persistence.
- Revalidate per-module port and `/zoom/events` mapping.
