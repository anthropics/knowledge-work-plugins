# Connection Types Reference

## SAP ABAP Connection

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| Category | Yes | Cloud or On-Premise |
| Host | Yes | Application server hostname |
| Port | Yes | Service port (typically 443 for Cloud) |
| Client | Yes | SAP client number |
| Language | No | Login language (EN, DE, etc.) |

### Authentication Options
- User Name and Password
- X.509 Client Certificate

### Supported Features
- Remote Tables
- Replication Flows
- Data Flows

---

## SAP S/4HANA Cloud

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| Host | Yes | S/4HANA Cloud tenant URL |
| Authentication Type | Yes | OAuth 2.0 (recommended) |
| OAuth Client ID | Yes | Service key client ID |
| OAuth Client Secret | Yes | Service key secret |
| Token URL | Yes | OAuth token endpoint |

### Supported Features
- Remote Tables (CDS Views)
- Replication Flows (ODP extraction)
- Data Flows

---

## SAP HANA

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| Category | Yes | Cloud or On-Premise |
| Host | Yes | HANA server hostname |
| Port | Yes | SQL port (e.g., 443 for Cloud, 30015 for on-prem) |

### Authentication Options
- User Name and Password
- X.509 Client Certificate

### Features Configuration
| Feature | Options |
|---------|---------|
| Remote Tables | Enabled (default) |
| Data Provisioning | Direct |
| Data Access | Remote and Replication |

---

## Google BigQuery

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| Project ID | Yes | GCP project identifier |
| Dataset | No | Default dataset |

### Authentication
- Service Account JSON key

### Supported Features
- Remote Tables
- Data Flows

---

## Amazon Redshift

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| Host | Yes | Redshift cluster endpoint |
| Port | Yes | Database port (default: 5439) |
| Database | Yes | Database name |

### Authentication
- User Name and Password
- IAM Authentication

---

## Generic JDBC

### Configuration Properties
| Property | Required | Description |
|----------|----------|-------------|
| JDBC URL | Yes | Full JDBC connection string |
| Driver Class | Yes | JDBC driver class name |

### Notes
- Requires JDBC driver upload to Data Provisioning Agent
- For on-premise sources only
