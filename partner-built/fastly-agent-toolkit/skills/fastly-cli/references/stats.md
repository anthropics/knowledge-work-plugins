# Fastly Statistics and Analytics

Access historical, real-time, and aggregated metrics for Fastly services.

## Command Overview

| Command                  | Description                    |
| ------------------------ | ------------------------------ |
| `stats aggregate`        | Aggregated historical stats    |
| `stats domain-inspector` | Domain inspector stats         |
| `stats historical`       | Historical stats for a service |
| `stats origin-inspector` | Origin inspector stats         |
| `stats realtime`         | Real-time stats for a service  |
| `stats regions`          | List stats regions             |
| `stats usage`            | Usage stats                    |

## Aggregate Statistics

Query aggregated historical stats across services.

```bash
# Aggregated stats
fastly stats aggregate

# Specific time range
fastly stats aggregate \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-02T00:00:00Z"

# JSON output
fastly stats aggregate --json
```

## Historical Statistics

Query aggregated metrics over time periods.

```bash
# Basic historical stats
fastly stats historical --service-id SERVICE_ID

# Specific time range
fastly stats historical \
  --service-id SERVICE_ID \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-02T00:00:00Z"

# Filter by region
fastly stats historical --service-id SERVICE_ID --region europe

# Filter to a single stats field
fastly stats historical --service-id SERVICE_ID --field bandwidth

# Aggregation period: minute, hour, or day (no "month")
fastly stats historical --service-id SERVICE_ID --by day

# JSON output for processing
fastly stats historical --service-id SERVICE_ID --json
```

### Available Fields

| Field        | Description               |
| ------------ | ------------------------- |
| `requests`   | Total requests            |
| `hits`       | Cache hits                |
| `miss`       | Cache misses              |
| `pass`       | Requests passed to origin |
| `bandwidth`  | Total bandwidth (bytes)   |
| `status_1xx` | 1xx responses             |
| `status_2xx` | 2xx responses             |
| `status_3xx` | 3xx responses             |
| `status_4xx` | 4xx responses             |
| `status_5xx` | 5xx responses             |
| `hit_ratio`  | Cache hit ratio           |
| `errors`     | Error count               |

## Domain Inspector Statistics

Inspect domain-level metrics for your service. Useful for understanding traffic patterns and performance on a per-domain basis.

```bash
# Domain inspector stats
fastly stats domain-inspector --service-id SERVICE_ID

# Specific time range
fastly stats domain-inspector --service-id SERVICE_ID \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-02T00:00:00Z"

# JSON output
fastly stats domain-inspector --service-id SERVICE_ID --json
```

## Origin Inspector Statistics

Inspect origin-level metrics for your service. Helps identify origin health issues, latency, and request volume per origin.

```bash
# Origin inspector stats
fastly stats origin-inspector --service-id SERVICE_ID

# Specific time range
fastly stats origin-inspector --service-id SERVICE_ID \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-02T00:00:00Z"

# JSON output
fastly stats origin-inspector --service-id SERVICE_ID --json
```

## Real-time Statistics

Stream live metrics from your service.

```bash
# Real-time stats (updates every second)
fastly stats realtime --service-id SERVICE_ID

# JSON output
fastly stats realtime --service-id SERVICE_ID --json
```

Real-time stats show:
- Requests per second
- Bandwidth
- Cache hit ratio
- Error rates
- Response times

## Usage Statistics

View usage stats across your account, including bandwidth and request totals.

```bash
# Usage stats
fastly stats usage

# Specific time range
fastly stats usage \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-02T00:00:00Z"

# Break down usage by service
fastly stats usage --by-service

# JSON output
fastly stats usage --json
```

## Regional Statistics

Filter metrics by geographic region using `--region`.

```bash
# List available regions
fastly stats regions

# Filter stats to a specific region
fastly stats historical --service-id SERVICE_ID --region europe --json --by day
```

### Regions

| Region             | Description           |
| ------------------ | --------------------- |
| `usa`              | United States         |
| `europe`           | Europe                |
| `asia`             | Asia Pacific          |
| `asia_india`       | India                 |
| `asia_southkorea`  | South Korea           |
| `anzac`            | Australia/New Zealand |
| `africa_std`       | Africa                |
| `latam`            | Latin America         |
| `mexico`           | Mexico                |
| `southamerica_std` | South America         |

## Infrastructure Information

```bash
# List Fastly datacenter POPs
fastly pops

# List Fastly public IP ranges
fastly ip-list
```

Use IP ranges for:
- Firewall allowlists at origin
- Identifying Fastly traffic
- Security group configuration

## Common Use Cases

### Check Cache Performance

```bash
# Get hit ratio over last day
fastly stats historical \
  --service-id SERVICE_ID \
  --from "24 hours ago" \
```

### Monitor Error Rates

```bash
# Check 5xx errors over the last day
fastly stats historical --service-id SERVICE_ID --json --by hour \
  | jq -s '[.[].status_5xx] | add'

# Real-time error monitoring
fastly stats realtime --service-id SERVICE_ID
```

### Bandwidth Analysis

```bash
# Total bandwidth over last 7 days
fastly stats historical --service-id SERVICE_ID --json --by day \
  --from "7 days ago" | jq -s '[.[].bandwidth] | add'
```

### Regional Traffic Analysis

```bash
# Bandwidth from Europe
fastly stats historical --service-id SERVICE_ID --json --by day \
  --region europe | jq -s '[.[].bandwidth] | add'
```

## JSON Output Format

With `--json`, each line is a separate JSON object (one per aggregation period). Lines are **not** wrapped in an array or envelope. Use `jq -s` (slurp) to collect them into an array for aggregation:

```bash
# Human-readable (default)
fastly stats historical --service-id SERVICE_ID

# JSON output — one JSON object per line
fastly stats historical --service-id SERVICE_ID --json --by day

# Sum bandwidth across all days
fastly stats historical --service-id SERVICE_ID --json --by day \
  --from "2026-02-01" --to "2026-03-01" \
  | jq -s '[.[].bandwidth] | add'

# Extract per-day request counts
fastly stats historical --service-id SERVICE_ID --json --by day \
  | jq -s '.[] | {start_time, requests}'
```

## Cross-Service Aggregation

The CLI has no built-in cross-service stats. Loop over services to compare:

```bash
fastly service list --json | jq -r '.[] | "\(.ServiceID)|\(.Name)"' | while IFS='|' read -r id name; do
  bw=$(fastly stats historical -s "$id" --json --by day \
    --from "2026-02-01" --to "2026-03-01" \
    | jq -s '[.[].bandwidth] | add // 0')
  echo "${bw} ${name}"
done | sort -rn
```

## Integration Examples

### Export to CSV

```bash
fastly stats historical \
  --service-id SERVICE_ID \
  --json --by day | jq -rs '
  .[] | [.start_time, .requests, .hits, .miss, .bandwidth] | @csv
' > stats.csv
```

### Monitor with Watch

```bash
# Update stats every 5 seconds
watch -n 5 'fastly stats realtime --service-id SERVICE_ID'
```

### Alert on High Error Rate

```bash
#!/bin/bash
errors=$(fastly stats historical --service-id SERVICE_ID --json --by hour \
  | jq -s '.[-1].status_5xx')
if [ "$errors" -gt 100 ]; then
  echo "High error rate: $errors"
fi
```
