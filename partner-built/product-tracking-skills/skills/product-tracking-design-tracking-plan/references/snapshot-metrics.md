# Snapshot Metrics

Tracking what exists, not just what happened.

## Events vs Snapshots

**Events** track actions — what users *did*.
- `todo.created`
- `report.exported`
- `user.invited`

**Snapshots** track state — what *exists* right now.
- Total todos in account
- Number of active users
- Current subscription status

Both are essential. Events alone can't reliably answer "How many X does this account have?"

## Why You Can't Derive Counts from Events

In theory: `todos_created - todos_deleted = current_todo_count`

In practice:
- Events can be dropped or duplicated
- Historical events may predate your tracking
- Edge cases accumulate drift over time
- Migrations and imports bypass event tracking

**Snapshot metrics are the source of truth for counts.**

## What to Snapshot

Common account-level snapshots:

| Metric | Description |
|--------|-------------|
| `total_todo_count` | Objects in the account |
| `active_user_count` | Users active in last 30 days |
| `project_count` | Projects/workspaces created |
| `integration_count` | Connected integrations |
| `storage_used_mb` | Storage consumption |

Common status snapshots:

| Metric | Description |
|--------|-------------|
| `is_active` | Account is in good standing |
| `is_trial` | Account is in trial period |
| `last_sync_at` | When snapshot was last updated |

## Implementation Pattern

Snapshots are sent as **group traits**, not events:

```javascript
// Scheduled job (daily)
async function sendDailySnapshot(accountId) {
  const traits = {
    total_todo_count: await getTodoCount(accountId),
    active_user_count: await getActiveUserCount(accountId),
    is_active: await isAccountActive(accountId),
    last_daily_sync: new Date().toISOString()
  };
  
  group(accountId, traits);
}
```

### Key Points

1. **Scheduled, not event-triggered** — Run on a cadence (daily, hourly)
2. **Sent via group()** — These are account traits, not events
3. **Calculate from source of truth** — Query your database, not event logs
4. **Include timestamp** — `last_sync_at` tracks freshness

## When to Use Snapshots

| Use Case | Why Snapshots |
|----------|---------------|
| Plan limit tracking | "Account has 95/100 projects" needs current count |
| Health scoring | Account health depends on current state |
| Growth analysis | Track object counts over time |
| License status | Trial vs paid vs expired |
| Usage-based billing | Current usage determines cost |

## Snapshots vs Events: Which to Use?

| Question | Answer With |
|----------|-------------|
| "How many todos were created yesterday?" | Events |
| "How many todos does this account have?" | Snapshots |
| "What features did users use?" | Events |
| "How many users are on this account?" | Snapshots |
| "Did the user export a report?" | Events |
| "What's the account's MRR?" | Snapshots |

## Best Practices

1. **Run on a schedule** — Daily for most metrics, hourly for critical ones
2. **Don't infer from events** — Always calculate from your database
3. **Use consistent types** — Some analytics platforms prefer strings for numbers
4. **Track the sync timestamp** — Know when data was last updated
5. **Include license/subscription status** — Critical for B2B segmentation

## Example: Account Health Traits

```javascript
// Daily snapshot job
group(accountId, {
  // Object counts
  total_projects: 42,
  total_users: 8,
  total_integrations: 3,
  
  // Status
  plan: 'pro',
  status: 'paid',
  mrr: 9900,  // $99 in cents
  
  // Activity
  is_active: true,
  active_users_30d: 6,
  
  // Metadata
  last_daily_sync: '2024-02-07T00:00:00Z'
});
```

These traits become available for segmentation, alerting, and analysis in downstream tools.
