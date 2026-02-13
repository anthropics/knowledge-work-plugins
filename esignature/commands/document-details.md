---
description: Get detailed information about a specific document — signer status, timeline, and available actions
argument-hint: "[document name or ID]"
---

# /document-details -- Document Details

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Get comprehensive details about a specific e-signature document, including signer-by-signer status, timeline, and available actions.

## Invocation

```
/document-details [document name or ID]
```

If no argument is provided, prompt the user for what document they want details on.

## Workflow

### Step 1: Find the Document

Query ~~e-signature to locate the document:

1. If an **ID** is provided (numeric), fetch details directly using the pending details or signer info tools
2. If a **name** is provided, search across all document states (pending, signed, expired) and match by name
3. If **multiple matches** are found, present the list and ask the user to select one

### Step 2: Fetch Full Details

Once the document is identified, gather all available information:

- **Pending documents**: Get pending envelope details AND signer information
- **Signed documents**: Get signer information with completion timestamps
- **Any document**: Get the document signers for recipient-level detail

### Step 3: Present Comprehensive Details

```
## [Document Name]

**ID**: [id]
**Status**: [Pending / Signed / Expired / Cancelled]
**Created**: [date]
**Signing Order**: [Sequential / Parallel]

### Timeline
- **Sent**: [date]
- **Last Activity**: [date or N/A]
- **Expires**: [date or N/A]
- **Completed**: [date or N/A]

### Signers ([signed_count]/[total] signed)

| # | Signer | Email | Status | Signed At |
|---|--------|-------|--------|-----------|
| 1 | [name] | [email] | Signed | [date] |
| 2 | [name] | [email] | Pending | -- |
| 3 | [name] | [email] | Declined | -- |
```

### Step 4: Show Available Actions

Based on the document state, present relevant actions:

**If Pending:**
- Send reminder to unsigned signers
- Cancel the signature request
- View which signer is currently blocking progress (for sequential signing)

**If Signed/Completed:**
- No further actions needed
- Note completion date and all signer details

**If Expired:**
- Suggest resending the document
- Note which signers had not yet signed

**If Cancelled/Voided:**
- Suggest resending if still needed
- Note the cancellation context

## Notes

- For documents with sequential signing order, highlight which signer is "next up"
- If a document has been pending for an unusually long time, proactively suggest sending a reminder
- Show both the document-level status and individual signer statuses — they can differ
- If the document is not found in any state, suggest the user check the name/ID and try again
