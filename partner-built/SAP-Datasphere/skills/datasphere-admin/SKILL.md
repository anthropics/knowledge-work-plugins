---
name: datasphere-admin
description: SAP Datasphere system administration skill for managing spaces, users, roles, security, monitoring, and transport operations. Use when performing administrative tasks including creating/managing spaces, user management, role assignment, system monitoring, capacity planning, or transport package operations.
---

# SAP Datasphere Administrator

Comprehensive administration skill for SAP Datasphere covering space management, security configuration, system monitoring, and transport operations.

## Navigation Overview

SAP Datasphere uses a left-side navigation menu. Administrative functions are located in the lower section:

| Menu Item | Submenu Items | URL Fragment |
|-----------|---------------|--------------|
| Space Management | (direct) | `#/managespaces` |
| Security | Users, Roles, Authorization Overview, Activities | `#/users`, `#/roles` |
| Transport | Packages, Export, Import, Monitor | `#/repository_packages` |
| System Monitor | System Monitor, Capacities | `#/monitoring` |
| System | Configuration, Administration, About | `#/administration` |

## Space Management

**Navigation:** Left Menu → Space Management

### View All Spaces
1. Click **Space Management** in left navigation
2. View space cards showing: Name, Status (Cold/Warm), Disk Storage, Memory Storage
3. Toggle between tile/list view using icons in top-right toolbar

### Create a New Space
1. Navigate to Space Management
2. Click **Create** button (top toolbar) OR click **+** on Spaces card from Home
3. Fill in space details:
   - Business Name (display name)
   - Technical Name (system identifier)
   - Storage allocation (Disk and Memory quotas)
4. Click **Create**

### Edit Space Properties
1. Navigate to Space Management
2. Locate the space card
3. Click **Edit** button on the card
4. Modify: Storage quotas, Members, Properties
5. Save changes

### Space Status Management
- **Lock/Unlock:** Select space → Click Lock/Unlock in toolbar
- **Monitor:** Select space → Click Monitor to view space-specific metrics
- **Delete:** Select space → Click Delete (moves to Recycle Bin)

### Recycle Bin
- Access via left panel in Space Management
- Restore or permanently delete spaces

## Security Administration

**Navigation:** Left Menu → Security → [submenu]

### User Management
**Path:** Security → Users (`#/users`)

#### View Users
1. Navigate to Security → Users
2. Use Filter By panel to filter by: Role Name, Scope Name, License Type
3. Results show: User ID, Display Name, First Name, Last Name, Email, Roles count

#### Add New User
1. Click **+** (Add) button in toolbar
2. Enter user details
3. Assign roles
4. Save

#### Edit User
1. Select user row
2. Click Edit icon
3. Modify user properties and role assignments
4. Save

### Role Management
**Path:** Security → Roles (`#/roles`)

#### Standard Roles
| Role | Description |
|------|-------------|
| Data Warehouse Cloud Space Administrator | Full space privileges |
| Data Warehouse Cloud Integrator | Full data integration privileges |
| Data Warehouse Cloud Modeler | Modeling privileges |
| Data Warehouse Cloud Viewer | View-only access |
| Data Warehouse Cloud Consumer | Data consumption privileges |
| Data Warehouse Cloud Extended Viewer | Extended viewer privileges |
| Data Catalog Administrator | Full catalog privileges |
| Data Catalog User | Read catalog privileges |

#### Scoped Roles
Scoped roles limit permissions to specific spaces. Naming pattern: `Scoped Data Warehouse Cloud [Role Type]`

#### Create Custom Role
1. Navigate to Security → Roles
2. Click **+** button
3. Define role name and description
4. Configure permissions
5. Save

### Authorization Overview
**Path:** Security → Authorization Overview

View consolidated authorization matrix across users, roles, and spaces.

### Activities Log
**Path:** Security → Activities

Monitor user activities and audit trail.

## System Monitoring

**Navigation:** Left Menu → System Monitor → [submenu]

### Dashboard
**Path:** System Monitor → System Monitor (`#/monitoring`)

**Tabs available:**
- Dashboard (default)
- Elastic Compute Nodes
- Task Logs
- Statement Logs
- Object Store

**Dashboard Metrics:**
- Disk Storage Used (pie chart breakdown)
- Disk Used by Spaces for Storage
- Memory Used by Spaces for Storage
- Failed Tasks (Last 24 Hours)
- Out-of-Memory Errors
- Top 5 Out-of-Memory Errors by Space
- Admission Control Events

### Capacities
**Path:** System Monitor → Capacities

View and manage compute capacity allocation.

### Task Logs
1. Navigate to System Monitor → System Monitor
2. Click **Task Logs** tab
3. Filter by: Space, Task Type, Status, Date Range
4. View execution details and errors

### Statement Logs
1. Navigate to System Monitor → System Monitor
2. Click **Statement Logs** tab
3. Analyze SQL statement execution

## Transport Operations

**Navigation:** Left Menu → Transport → [submenu]

### Packages
**Path:** Transport → Packages (`#/repository_packages`)

#### View Packages
1. Navigate to Transport → Packages
2. Filter by Space using dropdown
3. View: Business Name, Technical Name, Space, Created On, Result

#### Create Package
1. Click **+** button
2. Select space and objects to include
3. Define package name
4. Save

### Export
**Path:** Transport → Export

Export packages for deployment to other systems.

### Import
**Path:** Transport → Import

Import packages from other Datasphere instances.

### Transport Monitor
**Path:** Transport → Monitor

Track transport operation status and history.

## System Administration

**Navigation:** Left Menu → System → Administration (`#/administration`)

### Configuration Tabs
| Tab | Purpose |
|-----|---------|
| System Configuration | Session timeout, SAP support access |
| Tenant Links | External system links |
| Data Source Configuration | Data source settings |
| Security | Security policies |
| App Integration | Third-party integrations |
| Notifications | Alert and notification settings |

### System Configuration
1. Navigate to System → Administration
2. On System Configuration tab:
   - Set **Session Timeout** (default: 3600 seconds)
   - Toggle **Allow SAP support user creation**
3. Click Edit to modify, Save to confirm

## Common Administrative Workflows

### Onboard New Team Member
1. Security → Users → Add user
2. Assign appropriate roles (e.g., Data Warehouse Cloud Modeler)
3. Space Management → Edit space → Add member to relevant space(s)
4. Configure scoped roles if needed

### Capacity Planning
1. System Monitor → Dashboard → Review storage metrics
2. System Monitor → Capacities → Assess compute allocation
3. Space Management → Edit spaces to adjust quotas as needed

### Troubleshoot Failed Tasks
1. System Monitor → Task Logs → Filter by Failed status
2. Review error details
3. Check Statement Logs for SQL-level issues
4. Review Out-of-Memory metrics if relevant

## MCP Tools Integration

When the SAP Datasphere MCP Server is connected (via Claude Desktop), the following tools are available for programmatic administration:

### Foundation Tools
| Tool | Description |
|------|-------------|
| `test_connection` | Verify connectivity to Datasphere tenant |
| `get_current_user` | Get current authenticated user info |
| `get_tenant_info` | Get tenant configuration details |
| `list_spaces` | List all available spaces |

### Catalog & Discovery Tools
| Tool | Description |
|------|-------------|
| `list_catalog_assets` | Browse catalog assets |
| `get_asset_details` | Get detailed asset metadata |
| `search_catalog` | Search for assets by criteria |
| `find_assets_by_column` | Find assets containing specific columns |

### Data Quality & Analysis Tools
| Tool | Description |
|------|-------------|
| `smart_query` | Intelligent data querying |
| `query_analytical_data` | Query analytical models |
| `query_relational_entity` | Query relational tables/views |
| `analyze_column_distribution` | Analyze data distribution |

### Database User Management Tools
| Tool | Description |
|------|-------------|
| `list_database_users` | List database users in a space |
| `create_database_user` | Create new database user |
| `get_database_user_details` | Get user configuration |
| `update_database_user` | Modify user settings |
| `delete_database_user` | Remove database user |

### MCP Server Setup
To use MCP tools, configure Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "sap-datasphere": {
      "command": "/path/to/start_sap_datasphere_mcp.sh",
      "args": []
    }
  }
}
```

## Resources

See reference files for detailed procedures:
- `references/space-management.md` - Detailed space operations
- `references/security-governance.md` - Security configuration details
- `references/system-monitoring.md` - Monitoring and troubleshooting
- `references/transport.md` - Transport lifecycle management
