# Hardware and Infrastructure

Cloud instance recommendations, topology patterns, and infrastructure configuration for CockroachDB Self-Hosted deployments.

## Cloud Instance Recommendations

### AWS

| Workload | Instance Type | vCPUs | RAM | Notes |
|----------|--------------|-------|-----|-------|
| Production (general) | m6i.2xlarge | 8 | 32 GB | Best price/performance |
| Production (large) | m6i.4xlarge | 16 | 64 GB | Higher throughput |
| Write-heavy | c6i.4xlarge | 16 | 32 GB | More CPU for write amplification |
| Development | m6i.xlarge | 4 | 16 GB | Minimum viable |

**Storage:** gp3 (3000+ IOPS, 125+ MB/s throughput) or io2 for write-heavy workloads.

**Avoid:** t-series (burstable), gp2 below 1TB (insufficient baseline IOPS), st1/sc1 (HDD).

### GCP

| Workload | Machine Type | vCPUs | RAM | Notes |
|----------|-------------|-------|-----|-------|
| Production (general) | n2-standard-8 | 8 | 32 GB | Best price/performance |
| Production (large) | n2-standard-16 | 16 | 64 GB | Higher throughput |
| Write-heavy | n2-highcpu-16 | 16 | 16 GB | Use with caution (low RAM) |
| Development | n2-standard-4 | 4 | 16 GB | Minimum viable |

**Storage:** pd-ssd (minimum). pd-balanced acceptable for dev/test.

**Avoid:** e2-micro/small/medium (shared CPU), pd-standard (HDD-backed).

### Azure

| Workload | VM Size | vCPUs | RAM | Notes |
|----------|---------|-------|-----|-------|
| Production (general) | Standard_D8s_v5 | 8 | 32 GB | Best price/performance |
| Production (large) | Standard_D16s_v5 | 16 | 64 GB | Higher throughput |
| Development | Standard_D4s_v5 | 4 | 16 GB | Minimum viable |

**Storage:** Premium SSD v2 or Ultra Disk. Premium SSD (P30+) acceptable.

**Avoid:** Standard HDD, Standard SSD, B-series (burstable).

## Topology Patterns

### Single-Region (3 nodes, 3 zones)

```
Region: us-east-1
├── Zone a: Node 1  --locality=region=us-east-1,zone=us-east-1a
├── Zone b: Node 2  --locality=region=us-east-1,zone=us-east-1b
└── Zone c: Node 3  --locality=region=us-east-1,zone=us-east-1c
```

- Survives 1 zone failure
- Lowest latency (single-digit ms)
- Minimum production topology

### Multi-Region (9 nodes, 3 regions)

```
Region: us-east-1
├── Zone a: Node 1  --locality=region=us-east-1,zone=us-east-1a
├── Zone b: Node 2  --locality=region=us-east-1,zone=us-east-1b
└── Zone c: Node 3  --locality=region=us-east-1,zone=us-east-1c

Region: us-west-2
├── Zone a: Node 4  --locality=region=us-west-2,zone=us-west-2a
├── Zone b: Node 5  --locality=region=us-west-2,zone=us-west-2b
└── Zone c: Node 6  --locality=region=us-west-2,zone=us-west-2c

Region: eu-west-1
├── Zone a: Node 7  --locality=region=eu-west-1,zone=eu-west-1a
├── Zone b: Node 8  --locality=region=eu-west-1,zone=eu-west-1b
└── Zone c: Node 9  --locality=region=eu-west-1,zone=eu-west-1c
```

- Survives 1 region failure
- Higher write latency (cross-region consensus)
- Use with survival goal configuration for region-level survival

## systemd Service Template

```ini
[Unit]
Description=CockroachDB
Requires=network.target
After=network.target

[Service]
Type=notify
User=cockroach
Group=cockroach
ExecStart=/usr/local/bin/cockroach start \
  --certs-dir=/var/lib/cockroach/certs \
  --store=/var/lib/cockroach/data \
  --listen-addr=<node-address>:26257 \
  --http-addr=<node-address>:8080 \
  --join=<node1>,<node2>,<node3> \
  --locality=region=<region>,zone=<zone> \
  --cache=.25 \
  --max-sql-memory=.25
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=cockroach
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Clock Synchronization

CockroachDB requires clocks within `--max-offset` (default 500ms). Nodes that exceed this offset will self-terminate.

### NTP Configuration

```bash
# Install and enable chrony (preferred over ntpd)
sudo apt install chrony  # Debian/Ubuntu
sudo yum install chrony  # RHEL/CentOS

# Configure low-latency sync
echo "server time.google.com iburst" >> /etc/chrony/chrony.conf
echo "makestep 0.1 3" >> /etc/chrony/chrony.conf
sudo systemctl restart chronyd

# Verify
chronyc tracking
```

### Cloud Provider Time Sync

- **AWS:** Use Amazon Time Sync Service (169.254.169.123)
- **GCP:** Google NTP is pre-configured
- **Azure:** Use Azure NTP (time.windows.com or Hyper-V)

## Load Balancer Configuration

### Health Check Endpoint

CockroachDB exposes `/health?ready=1` on the HTTP port (default 8080):
- Returns 200 when the node is live and ready to accept connections
- Returns 503 when draining or not ready

### HAProxy Example

```
frontend cockroachdb
    bind *:26257
    mode tcp
    default_backend cockroachdb_nodes

backend cockroachdb_nodes
    mode tcp
    balance roundrobin
    option httpchk GET /health?ready=1
    http-check expect status 200
    server node1 <node1>:26257 check port 8080
    server node2 <node2>:26257 check port 8080
    server node3 <node3>:26257 check port 8080
```

### Cloud Load Balancers

- **AWS NLB:** TCP listener on 26257, HTTP health check on 8080 path `/health?ready=1`
- **GCP TCP LB:** TCP forwarding on 26257, HTTP health check on 8080 path `/health?ready=1`
- **Azure LB:** TCP rule on 26257, HTTP probe on 8080 path `/health?ready=1`

## Firewall / Security Group Rules

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 26257 | TCP | Inbound | SQL client connections |
| 26257 | TCP | Inter-node | Node-to-node communication |
| 8080 | TCP | Inbound (restricted) | DB Console and health checks |

Restrict DB Console (8080) to admin networks. SQL port (26257) should be accessible from application servers and inter-node communication.
