---
description: Get a dashboard view of all signature activity — pending, signed, expired, and documents awaiting your action
---

# /signature-status -- Signature Dashboard

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Get a real-time overview of your e-signature pipeline across all document states.

## Invocation

```
/signature-status
```

## Workflow

### Step 1: Gather Data

Query ~~e-signature for all document states:

1. **Pending for me** -- Documents that need your signature
2. **Pending for others** -- Documents you sent that are waiting on others
3. **Recently signed** -- Documents completed in the past 7 days
4. **Expired/lapsed** -- Signature requests that expired without completion
5. **Account summary** -- Overall document counts and recent activity

### Step 2: Generate Dashboard

Output a structured dashboard:

```
## Signature Dashboard -- [Date]

### Action Required
- **Pending Your Signature**: [count]
  [List each document with name, sender, and date received]

### Awaiting Others
- **Sent & Waiting**: [count]
  [List each document with name, recipients, and days pending]

### Recently Completed
- **Signed This Week**: [count]
  [List each document with name, signers, and completion date]

### Needs Attention
- **Expired/Lapsed**: [count]
  [List each document with name, intended signers, and expiry date]

### Account Overview
- **Total Documents**: [count]
- **Templates Available**: [count]
- **Subscription Status**: [status]
```

### Step 3: Highlight Urgent Items

Flag any items that need immediate attention:
- Documents pending your signature for more than 2 days
- Documents sent to others that have been pending for more than 5 days
- Recently expired documents that may need to be resent

### Step 4: Suggest Actions

Based on the current state, suggest next steps:
- Remind signers on stale pending documents
- Resend expired documents
- Follow up on documents awaiting others

## Notes

- If ~~e-signature is not connected, inform the user and provide instructions for connecting
- Sort pending documents by date received (oldest first) to prioritize
- For documents with multiple signers, show individual signer status
