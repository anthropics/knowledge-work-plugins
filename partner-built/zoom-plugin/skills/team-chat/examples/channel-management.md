# Channel Management (Team Chat API)

Typical use cases:

- List channels a user can see (to let them pick a destination).
- Create channels (where supported by the API and account policy).

## Pitfalls

- Many "can't list channels" issues are missing `chat_channel:read`.
- Admin policies may prevent channel creation.

