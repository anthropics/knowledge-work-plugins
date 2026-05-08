# Enterprise App Deployment (Account-Wide Install / Approval)

High-frequency questions in the forum clusters:

- "How do I deploy an app to an entire company?"
- "How do I allow other users to use my app?"
- "Why can only the admin use it?"

## Skills Needed

| Order | Skill | Purpose |
|------:|------|---------|
| 1 | **zoom-general** | Understand Marketplace deployment/approval concepts |
| 2 | **zoom-rest-api** (optional) | Automate admin tasks (where supported) |

## What To Clarify Upfront

- Is this an internal app (single account) or public Marketplace app?
- Does the customer want:
  - admin pre-approval + user install?
  - account-level installation?
  - restricting installs to specific users/groups?

## Common Fix Patterns

- Ensure the app is configured for the right audience and install flow.
- Ensure required scopes are approved and users re-consented if scopes changed.
- If users are blocked, check account admin Marketplace policies.

## Links

- `marketplace-publishing.md`
- `../references/marketplace.md`

