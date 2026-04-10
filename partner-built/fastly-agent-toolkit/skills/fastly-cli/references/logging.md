# Fastly Logging Configuration

Configure real-time log streaming from Fastly edge to various destinations.

## Supported Logging Providers

| Provider             | Command                                   |
| -------------------- | ----------------------------------------- |
| Amazon S3            | `fastly service logging s3`               |
| Google Cloud Storage | `fastly service logging gcs`              |
| Google BigQuery      | `fastly service logging bigquery`         |
| Google Pub/Sub       | `fastly service logging googlepubsub`     |
| Azure Blob Storage   | `fastly service logging azureblob`        |
| Datadog              | `fastly service logging datadog`          |
| Splunk               | `fastly service logging splunk`           |
| Elasticsearch        | `fastly service logging elasticsearch`    |
| New Relic            | `fastly service logging newrelic`         |
| New Relic OTLP       | `fastly service logging newrelicotlp`     |
| Honeycomb            | `fastly service logging honeycomb`        |
| Grafana Cloud Logs   | `fastly service logging grafanacloudlogs` |
| Kafka                | `fastly service logging kafka`            |
| Kinesis              | `fastly service logging kinesis`          |
| Syslog               | `fastly service logging syslog`           |
| HTTPS                | `fastly service logging https`            |
| FTP                  | `fastly service logging ftp`              |
| SFTP                 | `fastly service logging sftp`             |
| Heroku               | `fastly service logging heroku`           |
| Loggly               | `fastly service logging loggly`           |
| Logshuttle           | `fastly service logging logshuttle`       |
| Papertrail           | `fastly service logging papertrail`       |
| Scalyr               | `fastly service logging scalyr`           |
| Sumologic            | `fastly service logging sumologic`        |
| DigitalOcean Spaces  | `fastly service logging digitalocean`     |
| OpenStack            | `fastly service logging openstack`        |
| Cloudfiles           | `fastly service logging cloudfiles`       |

## Common Operations

All logging providers support these operations:

```bash
fastly service logging <provider> list --service-id SERVICE_ID --version 1
fastly service logging <provider> describe --service-id SERVICE_ID --version 1 --name NAME
fastly service logging <provider> create --service-id SERVICE_ID --version 1 ...
fastly service logging <provider> update --service-id SERVICE_ID --version 1 --name NAME ...
fastly service logging <provider> delete --service-id SERVICE_ID --version 1 --name NAME
```

## Popular Provider Examples

### Amazon S3

```bash
fastly service logging s3 create \
  --service-id SERVICE_ID \
  --version 1 \
  --name s3-logs \
  --bucket-name my-fastly-logs \
  --access-key YOUR_AWS_ACCESS_KEY \
  --secret-key YOUR_AWS_SECRET_KEY \
  --path "/logs/%Y/%m/%d/" \
  --period 3600 \
  --gzip-level 9 \
  --format '%h %l %u %t "%r" %>s %b'
```

### Google Cloud Storage

```bash
fastly service logging gcs create \
  --service-id SERVICE_ID \
  --version 1 \
  --name gcs-logs \
  --bucket-name my-fastly-logs \
  --user service-account@project.iam.gserviceaccount.com \
  --secret-key "$(cat service-account.json)" \
  --path "/logs/%Y/%m/%d/" \
  --period 3600
```

### BigQuery

```bash
fastly service logging bigquery create \
  --service-id SERVICE_ID \
  --version 1 \
  --name bq-logs \
  --project-id my-gcp-project \
  --dataset fastly_logs \
  --table cdn_requests \
  --user service-account@project.iam.gserviceaccount.com \
  --secret-key "$(cat service-account.json)" \
  --format '{"timestamp":"%{begin:%Y-%m-%dT%H:%M:%S}t","client_ip":"%h","request":"%r","status":%>s}'
```

### Datadog

```bash
fastly service logging datadog create \
  --service-id SERVICE_ID \
  --version 1 \
  --name datadog-logs \
  --token YOUR_DATADOG_API_KEY \
  --region US \
  --format '{"ddsource":"fastly","service":"%{req.service_id}V","host":"%{Fastly-Orig-Host}i"}'
```

### Splunk

```bash
fastly service logging splunk create \
  --service-id SERVICE_ID \
  --version 1 \
  --name splunk-logs \
  --url https://http-inputs-yourdomain.splunkcloud.com/services/collector \
  --token YOUR_HEC_TOKEN \
  --format '{"time":%{begin:%s}t,"host":"%h","event":{"request":"%r","status":%>s}}'
```

### Elasticsearch

```bash
fastly service logging elasticsearch create \
  --service-id SERVICE_ID \
  --version 1 \
  --name es-logs \
  --url https://your-cluster.es.amazonaws.com \
  --index fastly-logs \
  --user elastic \
  --password YOUR_PASSWORD \
  --format '{"@timestamp":"%{begin:%Y-%m-%dT%H:%M:%SZ}t","client_ip":"%h"}'
```

### HTTPS (Generic Webhook)

```bash
fastly service logging https create \
  --service-id SERVICE_ID \
  --version 1 \
  --name webhook-logs \
  --url https://your-endpoint.example.com/logs \
  --method POST \
  --content-type application/json \
  --format '{"timestamp":"%{begin:%s}t","request":"%r","status":%>s}'
```

### Syslog

```bash
fastly service logging syslog create \
  --service-id SERVICE_ID \
  --version 1 \
  --name syslog-logs \
  --address logs.example.com \
  --port 514 \
  --use-tls \
  --tls-ca-cert "$(cat ca.crt)" \
  --format '%h %l %u %t "%r" %>s %b'
```

### Kafka

```bash
fastly service logging kafka create \
  --service-id SERVICE_ID \
  --version 1 \
  --name kafka-logs \
  --brokers broker1.example.com:9092,broker2.example.com:9092 \
  --topic fastly-logs \
  --required-acks 1 \
  --format '{"timestamp":%{begin:%s}t,"request":"%r"}'
```

## Log Format Variables

Common log format variables:

| Variable             | Description                  |
| -------------------- | ---------------------------- |
| `%h`                 | Client IP address            |
| `%l`                 | Remote logname               |
| `%u`                 | Remote user                  |
| `%t`                 | Time (CLF format)            |
| `%r`                 | Request line                 |
| `%>s`                | Response status              |
| `%b`                 | Response bytes               |
| `%{Header}i`         | Request header               |
| `%{Header}o`         | Response header              |
| `%D`                 | Time to serve (microseconds) |
| `%{begin:%Y-%m-%d}t` | Custom time format           |
| `%{req.service_id}V` | Service ID                   |

## Compute Logs (Real-time Streaming)

For Compute services, use `logtail` for real-time log streaming:

```bash
# Stream logs from Compute service
fastly log-tail --service-id SERVICE_ID

```

## Common Patterns

### JSON Log Format for Analytics

```json
{
  "timestamp": "%{begin:%Y-%m-%dT%H:%M:%SZ}t",
  "client_ip": "%h",
  "request_method": "%m",
  "request_uri": "%U",
  "request_protocol": "%H",
  "status": %{>s},
  "bytes_sent": %B,
  "response_time_ms": %{time.elapsed.msec}V,
  "cache_status": "%{Fastly-Cache-Status}o",
  "pop": "%{server.datacenter}V",
  "service_id": "%{req.service_id}V"
}
```

### Conditional Logging

Use placement to log only on specific conditions:

```bash
fastly service logging s3 create \
  --service-id SERVICE_ID \
  --version 1 \
  --name error-logs \
  --placement waf_debug \
  --response-condition "resp.status >= 500"
  # ... other options
```

### Multiple Log Endpoints

You can create multiple logging endpoints for the same service:

```bash
# All logs to S3 for archival
fastly service logging s3 create --name archive-logs ...

# Error logs to Datadog for alerting
fastly service logging datadog create --name error-alerts --response-condition "resp.status >= 500" ...

# Real-time to Kafka for processing
fastly service logging kafka create --name realtime-logs ...
```

## Updating Logging Configuration

```bash
# List current logging endpoints
fastly service logging s3 list --service-id SERVICE_ID --version active

# Clone version before making changes
fastly service version clone --service-id SERVICE_ID --version active

# Update endpoint on new version
fastly service logging s3 update \
  --service-id SERVICE_ID \
  --version 2 \
  --name s3-logs \
  --period 1800

# Activate new version
fastly service version activate --service-id SERVICE_ID --version 2
```

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- `fastly service logging <provider> delete` - Removes a logging endpoint, stopping log delivery

Deleting logging endpoints may cause compliance issues or loss of observability.

## Propagation Delays

Logging configuration changes require version activation and can take up to 10 minutes to propagate globally. After activating a new version with updated logging endpoints, allow time for propagation before verifying logs appear at the destination. Initial log delivery to new endpoints may take additional time as connections are established.
