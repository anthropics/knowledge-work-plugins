# Fastly Logging

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/logging

## Key Concepts

**Versioned resources.** Logging endpoints are tied to service versions. Creating, updating, or deleting a logging endpoint requires a draft (inactive) service version. You must activate the version for changes to take effect.

**Format version 2 is the modern format.** Version `2` supports all VCL variables and JSON-style format strings using `%{variable}V` syntax. Version `1` is the legacy Apache-style format (`%h`, `%t`, etc.). Version `2` is the default.

**Log format string.** Uses VCL variable interpolation. Common patterns: `%h` (client IP), `%t` (timestamp), `%r` (request line), `%>s` (status code), `%b` (body bytes). For JSON logging, use `%{req.url}V` for VCL variables and wrap strings in `json.escape()` to avoid broken JSON.

**Placement.** Controls where in the generated VCL the logging call is placed. If not set (or `null`), endpoints with `format_version` of `2` are placed in `vcl_log` and those with `format_version` of `1` are placed in `vcl_deliver`. `none` disables automatic log statement rendering in VCL (use when writing log statements manually). Most users should leave this as default.

**Batch vs streaming delivery.** Object storage providers (S3, GCS, Azure Blob, FTP, SFTP, DigitalOcean, OpenStack, Cloud Files) batch log lines into files uploaded at intervals controlled by `period` (seconds). Streaming providers (HTTPS, Datadog, Splunk, Syslog, Kafka, etc.) deliver log batches controlled by `request_max_entries` and `request_max_bytes`.

**Response conditions.** Attach a named condition to selectively log. The condition name must reference a condition object already created on the same service version.

## Common Endpoint Pattern

All logging providers follow the same CRUD pattern. Replace `{provider}` with the API path from the provider catalog below.

| Action          | Method   | Endpoint                                                               |
| --------------- | -------- | ---------------------------------------------------------------------- |
| List endpoints  | `GET`    | `/service/{service_id}/version/{version_id}/logging/{provider}`        |
| Create endpoint | `POST`   | `/service/{service_id}/version/{version_id}/logging/{provider}`        |
| Get endpoint    | `GET`    | `/service/{service_id}/version/{version_id}/logging/{provider}/{name}` |
| Update endpoint | `PUT`    | `/service/{service_id}/version/{version_id}/logging/{provider}/{name}` |
| Delete endpoint | `DELETE` | `/service/{service_id}/version/{version_id}/logging/{provider}/{name}` |

Request body encoding: `application/x-www-form-urlencoded` for POST and PUT.

```bash
# Create an S3 logging endpoint
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-s3-logs&bucket_name=my-log-bucket&access_key=YOUR_AWS_ACCESS_KEY&secret_key=YOUR_AWS_SECRET_KEY&format_version=2" \
  "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/logging/s3"

# Create an HTTPS logging endpoint
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-https-logs&url=https://logs.example.com/ingest&method=POST&format_version=2&json_format=2" \
  "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/logging/https"

# List all S3 logging endpoints for a version
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/logging/s3"
```

## Provider Catalog

All providers use the common endpoint pattern above. The `{provider}` path segment and provider-specific config fields are listed below.

| Provider                | API path           | Key config fields                                                             |
| ----------------------- | ------------------ | ----------------------------------------------------------------------------- |
| AWS S3                  | `s3`               | `bucket_name`, `access_key`, `secret_key`, `iam_role`, `domain`, `path`       |
| Azure Blob Storage      | `azureblob`        | `account_name`, `container`, `sas_token`, `path`                              |
| BigQuery                | `bigquery`         | `project_id`, `dataset`, `table`, `user`, `secret_key`                        |
| Cloud Files (Rackspace) | `cloudfiles`       | `bucket_name`, `access_key`, `region`                                         |
| Datadog                 | `datadog`          | `token`, `region` (US/US3/US5/EU/EU1/AP1)                                     |
| DigitalOcean Spaces     | `digitalocean`     | `bucket_name`, `access_key`, `secret_key`, `domain`                           |
| Elasticsearch           | `elasticsearch`    | `url`, `index`, `pipeline`, `user`, `password`                                |
| FTP                     | `ftp`              | `address`, `user`, `password`, `path`, `port`                                 |
| Google Cloud Pub/Sub    | `pubsub`           | `topic`, `project_id`, `user`, `secret_key`                                   |
| Google Cloud Storage    | `gcs`              | `bucket_name`, `project_id`, `user`, `secret_key`, `path`                     |
| Grafana Cloud Logs      | `grafanacloudlogs` | `url`, `user`, `token`, `index`                                               |
| Heroku                  | `heroku`           | `token`, `url`                                                                |
| Honeycomb               | `honeycomb`        | `token`, `dataset`                                                            |
| HTTPS                   | `https`            | `url`, `method`, `content_type`, `json_format`, `header_name`, `header_value` |
| Kafka                   | `kafka`            | `topic`, `brokers`, `compression_codec`, `required_acks`                      |
| Kinesis (AWS)           | `kinesis`          | `topic`, `region`, `access_key`, `secret_key`, `iam_role`                     |
| Log Shuttle             | `logshuttle`       | `token`, `url`                                                                |
| Logentries              | `logentries`       | `token`, `port`, `region`, `use_tls`                                          |
| Loggly                  | `loggly`           | `token`                                                                       |
| New Relic Logs          | `newrelic`         | `token`, `region` (US/EU)                                                     |
| New Relic OTLP          | `newrelicotlp`     | `token`, `region` (US/EU), `url`                                              |
| OpenStack               | `openstack`        | `url`, `access_key`, `bucket_name`, `user`                                    |
| Papertrail              | `papertrail`       | `address`, `port`                                                             |
| Scalyr                  | `scalyr`           | `token`, `region` (US/EU), `project_id`                                       |
| SFTP                    | `sftp`             | `address`, `user`, `password`, `ssh_known_hosts`, `path`, `port`              |
| Splunk                  | `splunk`           | `url`, `token`, `use_tls`                                                     |
| Sumo Logic              | `sumologic`        | `url`, `message_type`                                                         |
| Syslog                  | `syslog`           | `hostname`, `port`, `token`, `use_tls`                                        |

## Common Fields

These fields are shared across all or most logging providers:

| Field                | Description                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`               | Unique name for the endpoint (primary key for GET/PUT/DELETE by name)                                                                         |
| `format`             | VCL log format string with variable interpolation (e.g., `%h %l %u %t "%r" %>s %b`)                                                           |
| `format_version`     | `1` (legacy classic format) or `2` (modern, supports JSON-style format strings)                                                               |
| `placement`          | Where in the generated VCL the logging call is placed: `none` (disable automatic rendering) or `null` (use default based on `format_version`) |
| `response_condition` | Name of a condition object; only matching requests produce log lines                                                                          |

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                | URL                                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| Logging API reference                 | `https://www.fastly.com/documentation/reference/api/logging`                          |
| Logging integrations guide            | `https://www.fastly.com/documentation/guides/integrations/logging`                    |
| Log format reference                  | `https://www.fastly.com/documentation/guides/integrations/logging/custom-log-formats` |
| Logging endpoint setup by provider    | `https://www.fastly.com/documentation/guides/integrations/logging-endpoints`          |
| Real-time log streaming configuration | `https://www.fastly.com/documentation/guides/integrations/streaming-logs`             |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.
