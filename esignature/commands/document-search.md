---
description: Search across all documents — signed, pending, expired, and templates — by name, signer, or status
argument-hint: "[search query]"
---

# /document-search -- Search Documents

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Search across all e-signature documents by name, signer, or status.

## Invocation

```
/document-search [query]
```

If no query is provided, prompt the user for what they're looking for.

## Workflow

### Step 1: Understand the Query

Parse the search query to determine intent:

- **By document name**: "NDA with Acme", "Q4 contract"
- **By signer/recipient**: "documents sent to john@example.com", "what did Jane sign"
- **By status**: "all pending", "expired this month", "signed last week"
- **By time range**: "signed this week", "pending for more than 5 days"

### Step 2: Search Across Document States

Query ~~e-signature across all relevant states:

1. **Signed/completed documents** -- Search by name or signer
2. **Pending documents** -- Search pending requests and get signer details
3. **Expired documents** -- Search lapsed requests
4. **Templates** -- Search available templates
5. **Original documents** -- Search uploaded files

### Step 3: Present Results

```
## Search Results: "[query]"

### Signed Documents ([count])
| Document | Signers | Signed Date |
|----------|---------|-------------|
| [name]   | [names] | [date]      |

### Pending Documents ([count])
| Document | Waiting On | Sent Date | Days Pending |
|----------|-----------|-----------|--------------|
| [name]   | [names]   | [date]    | [count]      |

### Expired Documents ([count])
| Document | Intended Signers | Expired Date |
|----------|-----------------|--------------|
| [name]   | [names]         | [date]       |

### Templates ([count])
| Template Name |
|--------------|
| [name]       |
```

### Step 4: Offer Actions

For each result type, suggest relevant actions:
- **Signed**: View signer details
- **Pending**: Send reminder, view signer status, cancel request
- **Expired**: Resend for signature
- **Templates**: Use template to create new signature request

## Notes

- If the search returns no results, suggest broadening the search or trying alternate names
- For signer searches, match on both name and email
- Show the most recent results first
