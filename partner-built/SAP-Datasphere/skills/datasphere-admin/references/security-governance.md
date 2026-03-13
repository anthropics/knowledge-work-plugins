# Security & Governance Reference

## Table of Contents
1. [User Management](#user-management)
2. [Role Architecture](#role-architecture)
3. [Scoped Roles](#scoped-roles)
4. [Data Access Controls](#data-access-controls)
5. [Authorization Overview](#authorization-overview)
6. [Activity Monitoring](#activity-monitoring)

## User Management

### User Lifecycle
1. **Provisioning:** Users created via SAP BTP cockpit or SCIM
2. **Assignment:** Add to Datasphere and assign roles
3. **Space Access:** Grant space membership
4. **Deprovisioning:** Remove roles and space access

### User Properties
| Property | Description |
|----------|-------------|
| User ID | Unique identifier (typically email) |
| Display Name | Full name shown in UI |
| First Name | Given name |
| Last Name | Family name |
| Email | Contact email |
| License Type | SAP Datasphere license assignment |

### Filtering Users
Filter panel options:
- **Role Name:** Filter by assigned role
- **Scope Name:** Filter by space assignment
- **License Type:** Filter by license tier

## Role Architecture

### Standard Roles (Global)

| Role | Privileges |
|------|-----------|
| **DW Cloud Space Administrator** | Full administrative access to assigned spaces |
| **DW Cloud Integrator** | Create and manage data flows, replication, connections |
| **DW Cloud Modeler** | Create and modify data models, views, tables |
| **DW Cloud Viewer** | Read-only access to data and models |
| **DW Cloud Consumer** | Consume data for analytics (SAC integration) |
| **DW Cloud Extended Viewer** | Enhanced viewer with additional read permissions |
| **DW Cloud AI Consumer** | Access AI/ML features |
| **Data Catalog Administrator** | Full catalog management |
| **Data Catalog User** | Browse and search catalog |

### Assigning Roles
1. Security → Users → Select user
2. Click Edit
3. Navigate to Roles section
4. Add/remove role assignments
5. Save

## Scoped Roles

### Concept
Scoped roles restrict permissions to specific spaces rather than global access.

### Naming Convention
`Scoped Data Warehouse Cloud [Role Type]`

Examples:
- Scoped Data Warehouse Cloud Viewer
- Scoped Data Warehouse Cloud Modeler
- Scoped Data Warehouse Cloud Space Administrator

### Creating Scoped Role Assignment
1. Security → Roles
2. Select scoped role template
3. Configure scope (select spaces)
4. Assign to users

### When to Use Scoped Roles
- Multi-tenant environments with isolated teams
- Project-based access control
- Principle of least privilege implementation

## Data Access Controls

### Row-Level Security
Implement DAC to restrict data visibility:

1. Define criteria (e.g., region, department)
2. Map criteria to user attributes
3. Apply to views/tables

### Column-Level Security
Restrict access to sensitive columns:
- Mask sensitive data
- Hide columns from unauthorized users

### Implementation Path
1. Data Builder → Create Data Access Control
2. Define criteria structure
3. Map to business semantics
4. Assign to protected entities

## Authorization Overview

### Accessing Authorization Matrix
Path: Security → Authorization Overview

### Matrix Views
- User vs. Role assignments
- Role vs. Permission mappings
- Space vs. User access

### Use Cases
- Audit compliance checks
- Access review campaigns
- Permission troubleshooting

## Activity Monitoring

### Activity Log Location
Path: Security → Activities

### Logged Events
- User logins/logouts
- Object modifications
- Data access events
- Administrative changes

### Filtering Activities
- By user
- By action type
- By date range
- By object/space

### Audit Best Practices
- Regular activity review
- Export logs for compliance
- Set up alerting for sensitive operations
