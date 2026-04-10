# FUNDAMENTAL PRINCIPLES

## Core CockroachDB Rules
These principles apply to ALL CockroachDB SQL operations and override everything else:

### Essential Requirements
1. **Always include PRIMARY KEY** in table definitions
2. **Prefer UUID** for primary keys in distributed scenarios
3. **Use UPSERT** for blind writes, INSERT ON CONFLICT for conditional logic
4. **Add STORING** to indexes for covering queries
5. **Use AS OF SYSTEM TIME** for historical queries
6. **Use RETURNING NOTHING** for write-only operations when results aren't needed
7. **Consider multi-region** patterns for global applications

## Core Compatibility
- CockroachDB uses PostgreSQL wire protocol and syntax as its base
- Default transaction isolation level is SERIALIZABLE (highest level)
- All tables are distributed by default using range partitioning (512MB ranges)
- Every table MUST have a PRIMARY KEY (creates hidden `rowid` if not specified)
- Prefers explicit over implicit - always specify PRIMARY KEY, data types, etc.

## Type System Philosophy
- Types are normalized to their canonical forms
- INT8 (64-bit) is the default integer type
- JSONB is the only JSON storage format

## Distribution Best Practices
- Design for distributed execution from the start
- Use UUID primary keys for better distribution
- Avoid sequential IDs that cause hotspots
- Consider data locality for multi-region deployments
- Batch operations to reduce round trips

## Performance Principles
- Write operations return immediately after consensus
- Reads are consistent by default (can use follower reads for stale data)
- Indexes are globally distributed
- STORING columns prevent additional lookups
- Prepared statements reduce parsing overhead

These rules ensure generated SQL is not only syntactically correct but also follows CockroachDB best practices for performance, scalability, and correctness.
