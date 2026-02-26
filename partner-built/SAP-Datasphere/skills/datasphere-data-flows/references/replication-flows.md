# Replication Flows Reference

## Source Configuration

### S/4HANA CDS Views

**Required Annotations for Delta:**
```abap
@Analytics.dataExtraction.enabled: true
@Analytics.dataExtraction.delta.changeDataCapture: true
```

**Common CDS Views:**
| CDS View | Description | CDC Support |
|----------|-------------|-------------|
| I_ACDOCA | Universal Journal | Yes |
| I_BSEG | Accounting Line Items | Yes |
| I_PURCHASEORDER | Purchase Orders | Yes |
| I_SALESORDER | Sales Orders | Yes |

### Connection Requirements
- ABAP connection with Cloud Connector
- User with extraction authorization
- RFC destination configured

## Target Configuration

### Local Table
- Best for: In-memory analytics
- Enable "Delta Capture" for downstream Transformation Flows
- Storage: Uses Space memory quota

### Local Table (File) - Object Store
- Best for: Large volumes, warm/cold data
- Format: Parquet (default), CSV
- Storage: HANA Data Lake Files (HDLF)
- Performance: Slower than in-memory

### External Targets (POI Required)

#### Amazon S3
```
Bucket: s3://your-bucket
Path: /datasphere/exports/
Format: Parquet (recommended) or CSV
```

#### Azure Data Lake Gen2
```
Container: your-container
Path: /datasphere/exports/
Format: Parquet (recommended) or CSV
```

#### Kafka
```
Bootstrap Servers: kafka:9092
Topic: datasphere-events
Format: JSON or Avro
```

## Load Types

### Initial Load Only
- Full extraction on each run
- Use when: Source lacks CDC, one-time migration

### Initial + Delta
- First run: Full extraction
- Subsequent runs: Only changed records
- Requires: CDC-enabled source

## Monitoring

### Data Integration Monitor
Path: Left Menu → Data Integration Monitor

**Key Metrics:**
- Records transferred
- Duration
- Error count
- Delta queue status

### Troubleshooting Failed Runs
1. Check connection status
2. Verify CDC annotations
3. Review error logs in monitor
4. Check Cloud Connector (on-prem sources)
5. Verify POI block availability (external targets)
