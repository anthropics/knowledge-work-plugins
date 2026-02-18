---
description: Send signature reminders for pending documents — individually or in bulk
argument-hint: "[document name or 'all']"
---

# /send-reminder -- Signature Reminders

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Send reminders to signers for pending signature requests.

## Invocation

```
/send-reminder [document name]    # Remind signers for a specific document
/send-reminder all                # Remind signers for all pending documents
```

If no argument is provided, show all pending documents and let the user choose.

## Workflow

### Step 1: Identify Pending Documents

Query ~~e-signature for documents pending for others.

If a specific document name is provided:
- Search for the document by name
- If multiple matches, present the list and ask the user to confirm

If `all` is specified:
- List all documents pending for others

If no argument:
- List all pending documents with their signer status
- Ask the user which documents to send reminders for

### Step 2: Show Signer Details

For each selected document, show:

```
## [Document Name]
**Sent**: [date]
**Days Pending**: [count]

| Signer | Email | Status |
|--------|-------|--------|
| [name] | [email] | Pending / Signed |
```

### Step 3: Confirm and Send

Ask the user to confirm before sending reminders:

```
Ready to send reminders for:
- [Document 1] → [pending signer names]
- [Document 2] → [pending signer names]

Proceed? [yes/no]
```

Send the reminder via ~~e-signature.

### Step 4: Report Results

```
## Reminders Sent

- [Document 1]: Reminder sent to [signer names]
- [Document 2]: Reminder sent to [signer names]

[count] reminders sent successfully.
```

## Notes

- Only send reminders to signers who have not yet signed
- If a document has been pending for less than 24 hours, suggest the user wait before sending a reminder
- Show the number of previous reminders sent if available, to avoid over-reminding
