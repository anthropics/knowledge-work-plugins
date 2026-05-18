# Gmail: finding contract attachments

Use the Gmail MCP connector to find contract attachments in recent email.

## Search for contract emails

Use `search_threads` with a query targeting recent emails with attachments:

```
Query: "has:attachment (contract OR agreement OR NDA OR MSA OR SOW) newer_than:14d"
```

## What to do with results

1. Present a short list (subject, sender, date) if multiple candidates match.
2. Ask the user to confirm which one before downloading.
3. Use `get_thread` to fetch the full thread, then locate and read the attachment.

## Fallback

If Gmail is not connected or no matching attachment is found:

```
"I didn't find a recent contract attachment in Gmail — can you forward it or attach the file directly?"
```

## What NOT to do

- Do not read emails unrelated to the contract (no general inbox trawl).
- Do not send any reply or draft email during the review workflow.
