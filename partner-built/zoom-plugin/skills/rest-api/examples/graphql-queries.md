# GraphQL Queries (Zoom)

Use this when a forum question is really about "how do I fetch X without calling 10 REST endpoints".

## Practical Guidance

- Treat GraphQL as an alternative query surface. Not all REST resources are available.
- Auth is still OAuth; the most common failure mode is missing scopes.

## Pitfalls Seen In Forum Threads

- Confusing GraphQL "cursor" pagination with REST `next_page_token`.
- Assuming GraphQL replaces webhooks. It does not.

