# Transport Operations Reference

## Table of Contents
1. [Transport Concepts](#transport-concepts)
2. [Package Management](#package-management)
3. [Export Operations](#export-operations)
4. [Import Operations](#import-operations)
5. [Transport Monitoring](#transport-monitoring)
6. [Best Practices](#best-practices)

## Transport Concepts

### Purpose
Transport enables moving Datasphere objects between environments:
- Development → Test → Production
- Tenant to tenant migration
- Backup and recovery

### Transportable Objects
- Tables (local and remote)
- Views (graphical and SQL)
- Analytic Models
- Data Flows
- Replication Flows
- Transformation Flows
- Task Chains
- Connections (metadata only)

### Transport Lifecycle
1. Create Package (group objects)
2. Export Package (generate archive)
3. Transfer Archive (download/upload)
4. Import Package (deploy to target)
5. Monitor Results

## Package Management

### Accessing Packages
Path: Left Menu → Transport → Packages

### Package Properties
| Field | Description |
|-------|-------------|
| Business Name | Display name |
| Technical Name | System identifier |
| Space | Source space |
| Created On | Creation timestamp |
| Result | Status (Success/Failed) |

### Creating a Package
1. Navigate to Transport → Packages
2. Click **+** (Add) button
3. Configure package:
   - Select source space
   - Enter business name
   - Enter technical name
4. Add objects:
   - Browse space objects
   - Select objects to include
   - Dependencies auto-included
5. Save package

### Editing a Package
1. Select package row
2. Click Edit icon
3. Add/remove objects
4. Save changes

### Deleting a Package
1. Select package row
2. Click Delete icon
3. Confirm deletion

Note: Deleting a package does not affect source objects.

## Export Operations

### Accessing Export
Path: Left Menu → Transport → Export

### Export Process
1. Navigate to Transport → Export
2. Select package(s) to export
3. Configure export options:
   - Include data (optional)
   - Compression settings
4. Execute export
5. Download archive file (.zip)

### Export Considerations
- **With Data:** Includes actual data records (larger file)
- **Without Data:** Structure only (smaller file)
- Export validates object dependencies

### Export Troubleshooting
| Issue | Resolution |
|-------|------------|
| Missing dependencies | Add required objects to package |
| Permission denied | Verify export privileges |
| Large file timeout | Split into smaller packages |

## Import Operations

### Accessing Import
Path: Left Menu → Transport → Import

### Import Process
1. Navigate to Transport → Import
2. Upload archive file
3. Select target space
4. Configure import options:
   - Overwrite existing (yes/no)
   - Data handling
5. Preview changes
6. Execute import
7. Review results

### Import Modes
| Mode | Behavior |
|------|----------|
| Create Only | Fails if object exists |
| Overwrite | Replaces existing objects |
| Merge | Updates without losing custom changes |

### Import Validation
Pre-import checks:
- Object name conflicts
- Dependency availability
- Connection references
- Space capacity

### Post-Import Tasks
- Verify object functionality
- Update connection credentials
- Test data flows
- Validate security settings

## Transport Monitoring

### Accessing Monitor
Path: Left Menu → Transport → Monitor

### Monitored Information
- Transport execution history
- Status per object
- Error details
- Timing information

### Status Values
| Status | Meaning |
|--------|---------|
| Running | In progress |
| Completed | Successful |
| Completed with Warnings | Success with issues |
| Failed | Error occurred |

### Viewing Details
Click on transport record to see:
- Object-level status
- Error messages
- Execution timestamps

## Best Practices

### Package Organization
- Group related objects together
- Use meaningful names
- Document package contents
- Version packages (v1, v2, etc.)

### Development Workflow
1. Develop in DEV space
2. Create package
3. Export without data
4. Import to TEST
5. Validate functionality
6. Export for PROD
7. Import to PROD with approval

### Dependency Management
- Include all dependencies
- Test complete package
- Document external dependencies

### Security Considerations
- Remove sensitive data before transport
- Update credentials in target
- Verify role assignments post-import

### Troubleshooting Transport Failures
1. Check Transport Monitor for errors
2. Common issues:
   - Missing dependencies → Add to package
   - Name conflicts → Rename or use overwrite
   - Connection errors → Verify target connections
   - Capacity limits → Free space or increase quota
3. Retry after resolution
