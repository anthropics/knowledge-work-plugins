# Exploration Workflows — Detailed Reference

## Connection Troubleshooting Checklist

If `test_connection` fails, walk through these steps:

1. **OAuth credentials**: Verify the client ID and secret are correct and haven't expired
2. **Token URL**: Must match the tenant's authentication endpoint (format: `https://<tenant>.authentication.<region>.hana.ondemand.com/oauth/token`)
3. **Base URL**: Must include the tenant name and region (format: `https://<tenant>.<region>.hcs.cloud.sap`)
4. **Network access**: The MCP server must be able to reach SAP BTP endpoints (check firewall/proxy)
5. **Scopes**: The OAuth client needs appropriate scopes for the APIs being called
6. **User permissions**: The technical user must have space-level read access at minimum

Common error patterns:
- `401 Unauthorized` → credentials are wrong or expired
- `403 Forbidden` → user lacks required permissions/scopes
- `Connection refused` → network/firewall issue
- `404 Not Found` → wrong base URL or tenant name

## Tool Reference by Workflow

### Foundation Tools

#### test_connection
Verifies OAuth connectivity to the Datasphere tenant.
- **Use when**: Starting a session, or when other tools fail
- **Returns**: Connection status, tenant info, authenticated user

#### get_current_user
Returns the authenticated user's details.
- **Use when**: Need to check who is connected and their permissions
- **Returns**: Username, display name, assigned roles

#### get_tenant_info
Returns tenant configuration and capacity.
- **Use when**: Understanding the environment's size and setup
- **Returns**: Tenant name, region, storage capacity, feature flags

#### get_available_scopes
Lists OAuth2 scopes the current credentials have access to.
- **Use when**: Debugging permission issues
- **Returns**: List of granted scopes

### Catalog & Discovery Tools

#### list_spaces
Lists all spaces the authenticated user can access.
- **Use when**: Getting a landscape overview
- **Returns**: Space names, descriptions, storage used, member counts

#### get_space_info
Returns detailed information about a specific space.
- **Parameters**: `space_id` (required)
- **Use when**: Drilling into a specific space
- **Returns**: Storage quotas, members, settings, status

#### search_catalog
Full-text search across the entire data catalog.
- **Parameters**: `query` (required), filters (optional)
- **Use when**: User is looking for data about a topic
- **Returns**: Matching assets with name, description, type, space

#### list_catalog_assets
Browse catalog assets with filters.
- **Parameters**: Various filters (space, type, etc.)
- **Use when**: Browsing available assets
- **Returns**: Asset list with metadata

#### get_asset_details
Returns rich metadata for a specific catalog asset.
- **Parameters**: Asset identifier
- **Use when**: Understanding a specific asset's purpose and structure
- **Returns**: Description, tags, lineage info, quality metrics

#### get_asset_by_compound_key
Looks up an asset by its compound key (space + technical name).
- **Parameters**: `space_id`, `technical_name`
- **Use when**: You know the exact asset identifier
- **Returns**: Full asset details

#### get_space_assets
Lists all assets within a specific space.
- **Parameters**: `space_id` (required)
- **Use when**: Exploring everything in a space
- **Returns**: All assets grouped by type

#### search_tables
Searches for tables across spaces.
- **Parameters**: Search terms, space filter
- **Use when**: Looking for specific tables
- **Returns**: Matching tables with schema summaries

#### browse_marketplace
Browse available data marketplace packages.
- **Use when**: Looking for external/shared data
- **Returns**: Available packages with descriptions

### Schema & Metadata Tools

#### get_table_schema
Returns column definitions for a relational table or view.
- **Parameters**: `space_id`, `table_name`
- **Use when**: Understanding table structure
- **Returns**: Column names, types, keys, nullability, descriptions

#### get_relational_metadata
Returns CSDL metadata for relational entities in a space.
- **Parameters**: `space_id`
- **Use when**: Need OData-level schema details
- **Returns**: Entity types, properties, navigation properties

#### get_analytical_metadata
Returns CSDL metadata for analytical models.
- **Parameters**: `space_id`
- **Use when**: Understanding analytical model structure (measures, dimensions)
- **Returns**: Measures, dimensions, attributes, hierarchies

#### get_relational_entity_metadata
Returns detailed column metadata for a specific entity.
- **Parameters**: `space_id`, `entity_name`
- **Use when**: Need per-column OData details
- **Returns**: Property names, types, annotations

#### get_consumption_metadata
Returns consumption layer schema information.
- **Parameters**: `space_id`
- **Use when**: Understanding what's exposed for consumption
- **Returns**: Consumption-ready entities and their structure

### Data Query Tools

#### smart_query
Intelligent SQL query with auto-aggregation.
- **Parameters**: `space_id`, `table_name`, `query_description` or `sql`
- **Use when**: User describes what data they want in natural language
- **Returns**: Query results with column headers

Best practice: Start with natural language descriptions. The tool will construct appropriate SQL
including aggregations, filters, and limits.

#### execute_query
Runs a direct SQL query against Datasphere.
- **Parameters**: `space_id`, `sql` (required)
- **Use when**: Need precise SQL control (complex joins, window functions, specific formatting)
- **Returns**: Query results
- **Limits**: Max 10,000 characters query length; results capped

Safety: The SQL sanitizer blocks destructive operations (DROP, DELETE, TRUNCATE, ALTER).
Only SELECT queries are permitted.

#### query_relational_entity
OData query on relational entities.
- **Parameters**: `space_id`, `entity_name`, OData query options ($filter, $select, $top, etc.)
- **Use when**: Querying relational data through OData protocol
- **Returns**: Entity data in structured format

#### query_analytical_data
OData query on analytical models.
- **Parameters**: `space_id`, `model_name`, OData query options
- **Use when**: Querying analytical models with proper aggregation
- **Returns**: Aggregated analytical data

### Data Profiling Tools

#### analyze_column_distribution
Profiles a column's value distribution.
- **Parameters**: `space_id`, `table_name`, `column_name`
- **Use when**: Understanding data quality, cardinality, value ranges
- **Returns**: Distinct count, null rate, min/max, top values, distribution

#### find_assets_by_column
Searches for assets containing a specific column name.
- **Parameters**: `column_name`
- **Use when**: Finding which tables/views contain a particular field
- **Returns**: List of assets with the matching column

### Repository & Lineage Tools

#### search_repository
Searches for objects with lineage information.
- **Parameters**: Search terms, space filter
- **Use when**: Understanding data flow and dependencies
- **Returns**: Objects with upstream/downstream relationships

#### list_repository_objects
Lists objects in the repository.
- **Parameters**: Space and type filters
- **Use when**: Enumerating all objects in a space
- **Returns**: Object list with types and status

#### get_deployed_objects
Lists actively deployed objects.
- **Parameters**: Space filter
- **Use when**: Understanding what's live in production
- **Returns**: Deployed objects with deployment status

#### get_object_definition
Returns the full definition/specification of an object.
- **Parameters**: Object identifier
- **Use when**: Understanding transformation logic, view definitions, or flow configurations
- **Returns**: Object specification (columns, transformations, SQL, mappings)

#### get_task_status
Checks the execution status of data flows and tasks.
- **Parameters**: Task identifier
- **Use when**: Monitoring running or recently completed jobs
- **Returns**: Status, start/end times, record counts, error messages

### Database User Management

#### list_database_users
Lists database users in a space.
- **Parameters**: `space_id`

#### create_database_user / get_database_user_details / update_database_user / delete_database_user / reset_database_user_password
Full CRUD operations on database users.

## Error Resolution Guide

### Common Query Errors

| Error | Likely Cause | Resolution |
|-------|-------------|------------|
| `Entity not found` | Wrong table/view name | Use `search_tables` or `get_space_assets` to find correct name |
| `Column not found` | Wrong column name | Use `get_table_schema` to verify column names |
| `Insufficient privileges` | Missing space access | Check user roles with `get_current_user` |
| `Query too complex` | SQL exceeds limits | Simplify the query, reduce joins, or use smaller result sets |
| `Timeout` | Large dataset without filters | Add WHERE clauses, use TOP/LIMIT, or aggregate first |

### OData-Specific Errors

| Error | Likely Cause | Resolution |
|-------|-------------|------------|
| `400 Bad Request` | Malformed $filter | Check OData syntax — strings need single quotes |
| `404 Not Found` | Entity not exposed | Verify the entity is exposed for consumption |
| `501 Not Implemented` | Unsupported operation | Try a different query approach (SQL vs OData) |

### Analytical Model Errors

Analytical models require proper aggregation. If you get unexpected results:
1. Check that you're using `query_analytical_data` (not relational queries) for analytical models
2. Ensure measures are being aggregated (SUM, AVG, etc.)
3. Verify dimension combinations exist in the data
