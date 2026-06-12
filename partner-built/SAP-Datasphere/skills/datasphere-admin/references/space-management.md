# Space Management Reference

## Table of Contents
1. [Space Concepts](#space-concepts)
2. [Creating Spaces](#creating-spaces)
3. [Space Configuration](#space-configuration)
4. [Member Management](#member-management)
5. [Storage Management](#storage-management)
6. [Elastic Compute Nodes](#elastic-compute-nodes)

## Space Concepts

Spaces are isolated virtual environments that contain data models, objects, and user assignments. Each space has:
- **Technical Name:** System identifier (cannot be changed after creation)
- **Business Name:** Human-readable display name
- **Status:** Cold (inactive) or Warm (active with loaded data)
- **Storage Quotas:** Disk and Memory limits

## Creating Spaces

### Step-by-Step Process
1. Navigate: Left Menu → Space Management
2. Click **Create** button in top toolbar
3. Complete the form:

| Field | Description | Example |
|-------|-------------|---------|
| Business Name | Display name | "Finance Analytics" |
| Technical Name | System ID (uppercase, underscores) | "FINANCE_ANALYTICS" |
| Disk Storage | Maximum disk quota | 2 GB |
| Memory Storage | Maximum memory quota | 1 GB |

4. Click **Create** to provision the space

### Best Practices
- Use meaningful technical names that reflect purpose
- Start with conservative storage quotas and expand as needed
- Document space purpose in the description field

## Space Configuration

### General Properties
Access via: Space card → Edit → General tab

- Business Name (editable)
- Description
- Priority (1-5, affects resource allocation)
- Time Data settings

### Database Users
Configure Open SQL schema access:
1. Space → Edit → Database Users tab
2. Add database user with credentials
3. Configure schema access permissions

### Connections
Associate data connections with the space:
1. Space → Edit → Connections tab
2. Assign existing connections or create new ones

## Member Management

### Adding Members
1. Space card → Edit → Members tab
2. Click **Add**
3. Search for user by ID or name
4. Select role for this space:
   - Space Administrator
   - Integrator
   - Modeler
   - Viewer

### Role Permissions in Space Context
| Space Role | Create/Edit Models | Run Data Flows | View Data | Manage Space |
|------------|-------------------|----------------|-----------|--------------|
| Administrator | Yes | Yes | Yes | Yes |
| Integrator | Yes | Yes | Yes | No |
| Modeler | Yes | Limited | Yes | No |
| Viewer | No | No | Yes | No |

### Removing Members
1. Space → Edit → Members tab
2. Select member row
3. Click **Remove**
4. Confirm action

## Storage Management

### Monitoring Storage Usage
View from Space Management:
- Disk for Storage: Used/Allocated
- Memory for Storage: Used/Allocated
- Progress bars indicate utilization

### Adjusting Quotas
1. Space → Edit → General tab
2. Modify Disk Storage or Memory Storage values
3. Save changes

Note: Cannot reduce below current usage.

### Storage Best Practices
- Monitor usage regularly via System Monitor
- Set alerts for high utilization
- Plan for growth in data volumes

## Elastic Compute Nodes

### Overview
Elastic Compute Nodes provide additional compute capacity on-demand.

### Viewing ECN Status
Location: Space Management → Left panel → "Elastic Compute Nodes"

Shows:
- Block-Hour Remaining
- View Logs link
- Create option

### Creating ECN
1. Click **Create** in Elastic Compute Nodes section
2. Configure:
   - Node size
   - Duration
   - Associated space
3. Confirm creation

### Monitoring ECN Usage
- View Logs shows consumption history
- Block-hours are consumed during active usage
