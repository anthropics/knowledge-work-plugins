# Additional SQL Audit Queries for Cluster Settings

## Settings by Category with Modification Count

Summarize how many settings exist per variable-name prefix and how many have been modified from defaults:

```sql
SELECT
  split_part(variable, '.', 1) AS category,
  count(*) AS total_settings,
  count(*) FILTER (WHERE value != default_value) AS modified_count
FROM [SHOW ALL CLUSTER SETTINGS]
GROUP BY split_part(variable, '.', 1)
ORDER BY modified_count DESC, total_settings DESC;
```

## SQL Defaults and Their Session Variable Equivalents

Many `sql.defaults.*` cluster settings establish the default for a corresponding session variable. This query lists them alongside their current cluster-level value:

```sql
SELECT
  variable,
  value,
  default_value,
  description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE 'sql.defaults.%'
ORDER BY variable;
```

**Common mappings:**

| Cluster Setting | Session Variable | SET Command |
|---|---|---|
| `sql.defaults.distsql` | `distsql` | `SET distsql = 'auto';` |
| `sql.defaults.idle_in_transaction_session_timeout` | `idle_in_transaction_session_timeout` | `SET idle_in_transaction_session_timeout = '300s';` |
| `sql.defaults.statement_timeout` | `statement_timeout` | `SET statement_timeout = '30s';` |
| `sql.defaults.default_int_size` | `default_int_size` | `SET default_int_size = 8;` |
| `sql.defaults.serial_normalization` | `serial_normalization` | `SET serial_normalization = 'virtual_sequence';` |
| `sql.defaults.vectorize` | `vectorize` | `SET vectorize = 'on';` |
| `sql.defaults.results_buffer.size` | `results_buffer_size` | `SET results_buffer_size = '16384';` |
| `sql.defaults.use_declarative_schema_changer` | `use_declarative_schema_changer` | `SET use_declarative_schema_changer = 'on';` |

## Sensitive Settings Check

Verify whether sensitive setting values are being redacted from logs and diagnostic reports:

```sql
-- Check if redaction is enabled
SHOW CLUSTER SETTING server.redact_sensitive_settings.enabled;

-- Enable redaction (recommended for production)
SET CLUSTER SETTING server.redact_sensitive_settings.enabled = true;

-- List settings that are marked as sensitive
SELECT variable, value, setting_type
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE public = false;
```

When `server.redact_sensitive_settings.enabled` is `true`, the values of sensitive settings are replaced with `<redacted>` in:
- `SHOW CLUSTER SETTINGS` output for non-admin users
- Diagnostic bundles
- Telemetry reports

## Full Production Readiness Audit

Comprehensive query that evaluates key cluster settings and flags potential issues:

```sql
SELECT
  variable,
  value,
  default_value,
  CASE
    -- Critical settings that should be enabled
    WHEN variable = 'kv.rangefeed.enabled' AND value = 'false'
      THEN 'WARNING: Changefeeds will not work. Enable if CDC is planned.'
    WHEN variable = 'sql.stats.automatic_collection.enabled' AND value = 'false'
      THEN 'CRITICAL: Optimizer will use heuristics. Enable immediately.'
    WHEN variable = 'admission.kv.enabled' AND value = 'false'
      THEN 'CRITICAL: No overload protection. Enable immediately.'

    -- Timeout settings that should be non-zero
    WHEN variable = 'sql.defaults.idle_in_transaction_session_timeout' AND value = '0s'
      THEN 'WARNING: Idle transactions can hold locks indefinitely. Set to 300s or appropriate value.'
    WHEN variable = 'sql.defaults.statement_timeout' AND value = '0s'
      THEN 'INFO: No statement timeout. Consider setting based on workload SLA.'

    -- Upgrade safety
    WHEN variable = 'cluster.preserve_downgrade_option' AND value != ''
      THEN 'INFO: Downgrade option is set to ' || value || '. Finalization is blocked. Clear after confirming upgrade health.'

    -- Dead node detection
    WHEN variable = 'server.time_until_store_dead'
      AND value::INTERVAL < '3m'::INTERVAL
      THEN 'WARNING: Store dead threshold is very low (' || value || '). Risk of false positives.'
    WHEN variable = 'server.time_until_store_dead'
      AND value::INTERVAL > '10m'::INTERVAL
      THEN 'INFO: Store dead threshold is high (' || value || '). Recovery will be delayed.'

    -- Diagnostics
    WHEN variable = 'diagnostics.reporting.enabled' AND value = 'false'
      THEN 'INFO: Telemetry disabled. Cockroach Labs cannot provide proactive support insights.'

    ELSE 'OK'
  END AS assessment
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled',
  'sql.stats.automatic_collection.enabled',
  'admission.kv.enabled',
  'sql.defaults.idle_in_transaction_session_timeout',
  'sql.defaults.statement_timeout',
  'server.time_until_store_dead',
  'cluster.preserve_downgrade_option',
  'diagnostics.reporting.enabled',
  'kv.snapshot_rebalance.max_rate',
  'kv.snapshot_recovery.max_rate',
  'server.redact_sensitive_settings.enabled'
)
ORDER BY
  CASE
    WHEN value != default_value THEN 0
    ELSE 1
  END,
  variable;
```

## Recently Modified Settings

Identify settings that differ from their defaults to understand what has been customized:

```sql
SELECT
  variable,
  value,
  default_value,
  description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE value != default_value
ORDER BY variable;
```

## Settings Search

Find settings by keyword when you are unsure of the exact setting name:

```sql
SELECT variable, value, description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE
  variable LIKE '%keyword%'
  OR description LIKE '%keyword%'
ORDER BY variable;
```

Replace `%keyword%` with the relevant term (e.g., `%timeout%`, `%admission%`, `%snapshot%`).

## Zone Configuration Audit

Zone configurations (including `gc.ttlseconds`) are not cluster settings. Query them separately:

```sql
-- Cluster-wide default zone config
SHOW ZONE CONFIGURATION FOR RANGE default;

-- All zone configurations
SELECT
  target,
  raw_config_sql
FROM [SHOW ALL ZONE CONFIGURATIONS]
ORDER BY target;

-- Check gc.ttlseconds specifically
SELECT
  target,
  config ->> 'gc' AS gc_config
FROM [SHOW ALL ZONE CONFIGURATIONS]
ORDER BY target;
```
