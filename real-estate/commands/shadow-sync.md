---
name: shadow-sync
description: Manually synchronize corporate CRM activity with your private Google Sheets/Tasks logs.
arguments:
  - name: source
    description: "The source system (e.g., Vault RE, NurtureCloud)."
    required: true
  - name: target
    description: "The private destination (e.g., Private Google Sheet, Google Tasks)."
    required: true
---

# /shadow-sync Command

Ensure your private mirror of intelligence is up to date with the corporate network.

## When to Use

Use this command when:
- You've just finished a prospecting session and want to export notes to your private logs.
- You're preparing for a weekend of open homes and need your private task list synced.
- Real-time webhooks have failed or are unavailable.

## Workflow

### 1. Data Aggregation

Use `~~real-estate/shadow-workflow` to:
- Collect recent activity logs from the `source`.
- Filter for high-value intelligence (e.g., specific buyer feedback).

### 2. Mirror Execution

Produce:
- **Sync Log**: List of contacts and properties updated in your private admin account.
- **Conflict Report**: (If applicable) Discrepancies between your notes and corporate records.
- **Task Pulse**: New high-priority tasks created in Google Tasks.

## Example Session

**User:** `/shadow-sync source: "Vault RE" target: "Private Google Sheet"`

**System:**
```
[~] AGGREGATING VAULT RE LOGS...
[~] UPDATING PRIVATE MIRROR...

SYNC COMPLETE:

1. Contacts Mirrored: 5 new buyer leads from Maungaraki open home.
2. Property Updates: 1 listing (123 Petone) moved to 'Unconditional'.
3. Conflict: Your note 'Buyer needs 90 day settlement' is missing in Vault RE. (Note preserved in Private Sheet).

Next Step: Run /private-brief for listing '123 Petone' to prepare for settlement.
```

## Integration Points

- **Skill**: Uses `~~real-estate/shadow-workflow`.
- **Downstream**: Feeds into `/private-brief`.
