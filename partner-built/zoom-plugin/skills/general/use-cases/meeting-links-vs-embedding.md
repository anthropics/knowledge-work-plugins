# Meeting Links vs Embedding (REST `join_url` vs Meeting SDK)

This is a high-frequency confusion cluster:

- "Generate Zoom Meeting URLs server-side"
- "Join meeting via API"
- "Can I use the `join_url` inside Meeting SDK?"

## The Decision

### Use `join_url` (Meeting Link) When

- You are sending a user to the Zoom client or Zoom web client.
- You do not need embedded UI inside your application.

### Use Meeting SDK When

- You must embed a meeting inside your app.
- You need SDK-level control over the experience.

## Common Mistakes

- Treating REST `join_url` as a way to join via SDK.
- Expecting an API endpoint to "join a user to a meeting".

## Skills Needed

| Order | Skill | Purpose |
|------:|------|---------|
| 1 | **zoom-rest-api** | Create meetings and understand what `join_url` is |
| 2 | **zoom-meeting-sdk** | Embed meetings correctly |

## Links

- `../../rest-api/concepts/meeting-urls-and-sdk-joining.md`
- `../../meeting-sdk/SKILL.md`
- `embed-meetings.md`

