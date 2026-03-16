# Authentication Guide

## User Name and Password

### When to Use
- Simple authentication requirements
- Service accounts with static credentials
- Development/test environments

### Configuration
1. Enter username
2. Enter password
3. Optionally save credentials

### Security Considerations
- Use dedicated service accounts
- Avoid personal user credentials
- Implement password rotation policy

---

## X.509 Client Certificate

### When to Use
- High-security requirements
- Mutual TLS authentication
- SAP Cloud Platform services

### Prerequisites
- Valid X.509 certificate (PEM format)
- Corresponding private key
- Certificate must be trusted by target system

### Configuration Steps
1. Select "X.509 Client Certificate" as authentication type
2. Upload or paste certificate content
3. Upload or paste private key
4. Validate connection

### Certificate Requirements
- RSA 2048-bit or higher
- Valid date range
- Proper chain of trust

---

## OAuth 2.0

### When to Use
- Cloud services (S/4HANA Cloud, SuccessFactors)
- Token-based authentication
- SSO integration scenarios

### OAuth Grant Types

#### Client Credentials
Best for service-to-service communication:
1. Obtain Client ID and Secret from service key
2. Configure Token URL
3. System automatically refreshes tokens

#### Authorization Code
For user-delegated access:
1. Configure authorization endpoint
2. User authenticates via browser
3. System stores refresh token

### Configuration Properties
| Property | Description |
|----------|-------------|
| Client ID | OAuth application identifier |
| Client Secret | Application secret |
| Token URL | Endpoint for token exchange |
| Scope | Optional: requested permissions |

---

## SAP Cloud Connector

### When to Use
- On-premise system access
- Firewall traversal
- Secure tunnel to cloud

### Setup Overview
1. Install Cloud Connector on-premise
2. Configure subaccount connection
3. Add virtual host mapping
4. Test connectivity from Datasphere

### Connection Configuration
- Use virtual host name (not real hostname)
- Virtual port mapped by Cloud Connector
- Datasphere connects to Cloud Connector endpoint

---

## Troubleshooting Authentication

### Common Issues

#### Invalid Credentials
- Verify username/password
- Check account lock status
- Confirm service account permissions

#### Certificate Errors
- Validate certificate expiration
- Check certificate format (PEM required)
- Verify trust chain

#### OAuth Token Failures
- Confirm client credentials
- Check token URL accessibility
- Verify scope permissions

#### Network Issues
- Test connectivity to host/port
- Check Cloud Connector status (on-prem)
- Verify firewall rules
