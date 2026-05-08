# SDK Upgrade Workflow (Changelog + RSS)

Reusable process for upgrading Zoom SDK integrations from an older customer version to latest with low regression risk.

## Use This When

- Customer is multiple versions behind.
- Breaking changes may exist between current and latest.
- You need a defensible, version-by-version upgrade plan.

## Inputs Required

1. Product and platform
- Example: `Meeting SDK Android`, `Video SDK iOS`, `Contact Center Web`.

2. Current version in production
- Example: `6.3.1`, `2.1.0`.

3. Target version
- Usually latest stable from changelog.

4. Critical features in use
- Example: custom UI, raw data, recording, chat, live transcription, token flow.

## Canonical Source

- Changelog entry point: https://developers.zoom.us/changelog/

## Workflow

### 1) Scope the upgrade lane

- Confirm exact product + platform lane before collecting releases.
- Do not mix lanes (for example, Meeting SDK Web and Meeting SDK iOS must be treated separately).

### 2) Locate the platform-specific RSS feed

From `https://developers.zoom.us/changelog/`:
- Filter by product/platform.
- Find the RSS link for that filtered lane.
- Use only that feed for release collection.

If feed discovery is unclear:
- Open the filtered changelog page and locate the RSS icon/link.
- Confirm feed entries match the same product/platform lane.

### 3) Build the release ledger

Collect all releases from:
- `current_version` (exclusive) up to `target_version` (inclusive), then latest if target is `latest`.

For each release entry capture:
- Version
- Release date
- Release URL
- Breaking/deprecated notes
- Required migration actions

Sort upgrade steps in ascending version order.

### 4) Plan upgrade hops

Default strategy:
- Patch/minor jumps can often be grouped.
- Major changes should be isolated into dedicated hops.

Recommended hop pattern:
1. `current -> next safe checkpoint`
2. `checkpoint -> next major boundary`
3. Repeat until latest

### 5) Extract required actions per hop

For each hop, classify actions under:
- Auth/token contract changes
- API renames/signature changes
- Initialization/lifecycle changes
- Event payload/callback changes
- Build/dependency/runtime requirements
- Feature removals/deprecations

### 6) Apply compatibility guards

- Wrap renamed/deprecated calls behind adapters.
- Keep temporary compatibility mappings for payload changes.
- Add feature flags for behavior toggles when needed.

### 7) Validate each hop before continuing

Minimum validation set:
- SDK init/auth
- Join/start/session entry flow
- Core media flows (audio/video/share) if applicable
- Critical product-specific features used by customer
- Cleanup/leave/disconnect behavior

Do not skip to next hop if the current hop is unstable.

### 8) Produce final upgrade package

Deliver:
- Step-by-step upgrade matrix
- Per-hop code/config change list
- Deprecated-to-replacement map
- Risks and rollback notes
- Final target-state checklist

## Output Template

```markdown
## Upgrade Plan: <product/platform>

- Current: <x.y.z>
- Target: <a.b.c or latest>
- Source feed: <rss_url>

### Hop 1: <x.y.z -> x.y+1.z>
- Release notes:
  - <url>
- Breaking/deprecations:
  - <item>
- Required changes:
  - <item>
- Validation:
  - <item>

### Hop 2: <...>
...

## Deprecated -> Replacement Map
- <old> -> <new>

## Risks
- <risk>

## Rollback
- <rollback step>
```

## Operating Rules

- Never assume only latest release notes are sufficient.
- Always process intermediate releases between customer version and target.
- Prefer smallest-risk path over fastest path for production upgrades.
