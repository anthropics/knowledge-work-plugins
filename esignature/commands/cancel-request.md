---
description: Cancel a pending signature request — individually or after reviewing all pending documents
argument-hint: "[document name or ID]"
---

# /cancel-request -- Cancel Signature Request

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Cancel/void a pending signature request so it can no longer be signed.

## Invocation

```
/cancel-request [document name]    # Cancel a specific document's signature request
/cancel-request                    # Show all pending documents and choose which to cancel
```

## Workflow

### Step 1: Identify the Document

Query ~~e-signature for pending documents.

If a specific document name or ID is provided:
- Search for the document by name or ID
- If multiple matches, present the list and ask the user to confirm which one

If no argument:
- List all documents pending for others
- Ask the user which document(s) to cancel

### Step 2: Show Document Details

For the selected document, show full details before cancellation:

```
## [Document Name] (ID: [id])
**Sent**: [date]
**Days Pending**: [count]
**Status**: [signed_count]/[total] signed

| Signer | Email | Status |
|--------|-------|--------|
| [name] | [email] | Pending / Signed |
```

### Step 3: Confirm Cancellation

**This action is irreversible.** Always confirm before cancelling:

```
WARNING: You are about to cancel the signature request for:
  - [Document Name] → [pending signer names]

This will void the document and signers will no longer be able to sign it.
Any signatures already collected will be discarded.

Proceed with cancellation? [yes/no]
```

### Step 4: Cancel and Report

Cancel the request via ~~e-signature, then confirm:

```
## Cancellation Complete

- [Document Name] (ID: [id]): Signature request cancelled

The document has been voided. Signers have been notified.
```

### Step 5: Suggest Next Steps

Based on the cancellation, suggest what to do next:
- If the document needs changes: "You can update the document and resend it for signature"
- If it was sent to the wrong person: "You can resend to the correct recipient"
- If it's no longer needed: "No further action required"

## Notes

- Only the document owner/sender can cancel a signature request
- Cancellation is **irreversible** — always confirm with the user first
- If the document has already been fully signed (completed), it cannot be cancelled
- If some signers have already signed, warn the user that those signatures will be lost
- Suggest alternatives to cancellation when appropriate (e.g., sending a reminder instead)
