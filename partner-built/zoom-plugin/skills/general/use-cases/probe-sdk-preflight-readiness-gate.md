# Probe SDK Preflight Readiness Gate

Use Probe SDK before user join/start flows to detect device, browser, and network issues early.

## When to Use

- You want to reduce failed joins and low-quality first-minute experiences.
- You need a clear pass/warn/fail decision before launching Meeting SDK or Video SDK UX.
- You need structured diagnostics for support workflows.

## Skill Chain

- [probe-sdk](../../probe-sdk/SKILL.md)
- [zoom-meeting-sdk/web](../../meeting-sdk/web/SKILL.md) or [zoom-video-sdk/web](../../video-sdk/web/SKILL.md)
- [zoom-general](../SKILL.md)

## High-Level Flow

1. Request media permissions and enumerate devices.
2. Run targeted diagnostics for selected mic/camera/speaker.
3. Run comprehensive network probe and collect final report.
4. Apply readiness policy (`allow`, `warn`, `block`) and present next steps.
5. Launch meeting/session only when policy permits.

## Risks

- Renderer and report schema drift across versions.
- Browser support changes over time.
- Incomplete cleanup causing residual device/network usage.

## See Also

- [probe-sdk runbook](../../probe-sdk/RUNBOOK.md)
- [probe-sdk troubleshooting](../../probe-sdk/troubleshooting/common-issues.md)
