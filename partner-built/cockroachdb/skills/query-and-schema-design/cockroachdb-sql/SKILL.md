---
name: cockroachdb-sql
description: Use when writing, generating, or optimizing SQL for CockroachDB, designing CockroachDB schemas, or when the user asks about CockroachDB-specific SQL patterns, type mappings, and distributed database best practices. Also use when encountering CockroachDB anti-patterns like missing primary keys, sequential ID hotspots, or incorrect type usage.
compatibility: Can work with or without connection to a database. Without connection it generates the SQL and gives instruction for connection.With connection it requires appropriate privilege on target database and tables (SELECT, INSERT, UPDATE, DELETE, or admin).
metadata:
  author: cockroachdb
  version: "1.0"
---

## CockroachDB SQL Skill  

Converts natural language questions into CockroachDB-compliant SQL queries, following CockroachDB best practices. Use it for schema design, writing queries and optimizing query.

## When to Use This Skill

Activate this skill when:
- User asks for SQL query generation for CockroachDB
- User provides natural language descriptions of database operations
- User asks questions like:
  - "How do I query recent orders in CockroachDB?"
  - "Generate a CockroachDB table for user management"
  - "Convert this to CockroachDB SQL: [description]"
  - "What's the CockroachDB way to [operation]?"
- When you encounter:
  - CREATE TABLE statements
  - ALTER TABLE modifications
  - DML Operations (INSERT, UPDATE, DELETE)
  - SELECT queries
  - Performance optimization requests
  - Backup/restore operations

## How to Apply this Skill

1. **Connection Detection** — already performed on skill invocation; reuse active connection.

2. **Parse Natural Language Intent**
   - Identify the operation type (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, etc.)

3. **Context Gathering**
   - Check for existing schema context in conversation
   - If connected to DB, query existing schema:
     - `SHOW TABLES;` to see existing tables
     - `SHOW CREATE TABLE table_name;` for existing structure
   - Ask clarifying questions if needed:
     - Table structure if not provided
     - Data types for columns
     - Index requirements
     - Multi-region needs
     - Performance characteristics

4. **Apply CockroachDB Rules**
   - Reference rules in `references/cockroachdb-rules/` 
   - Ensure compliance with CockroachDB best practices
   - **Determine rule category based on operation and apply the relavant rules**:
     * `00-fundamental-principles.md` - Always apply these first
     * `01-schema-design.md` - Table creation and structure
     * `02-dml-operations.md` - Data modification
     * `03-query-patterns.md` - Query construction
     * `04-optimization.md` - Performance, Optimization and anti-patterns
     * `05-operational.md` - Admin and maintenance
   - Validate against anti-patterns in 04-optimization.md 

5. **Validate against DB(MANDATORY)**
   - ALWAYS run EXPLAIN on every generated SQL query when connected to DB.
   - If EXPLAIN returns a parsing/syntax error, fix the query and re-run EXPLAIN until it passes.
   - Include the EXPLAIN output in the response.

## Response Behavior

### Initial Response

When skill is invoked, ALWAYS:
1. **Immediately detect connection** before any other action or response:
   - Check if connection string is provided in the prompt (postgresql://...).
     - If provided, use `cockroach sql --url "<provided-url>" -e "SQL"` to run queries. Do not use psql.
   - Else check COCKROACH_URL environment variable (`echo $COCKROACH_URL`). 
     - If set, use `cockroach sql --url $COCKROACH_URL -e "SQL"` to run queries. Do not use psql.
   - Else check for cockroach-cloud MCP server availability

2. Focus exclusively on CockroachDB
3. Emphasize "natural language to CockroachDB SQL" not "database conversion"
4. Keep user-facing content CockroachDB-specific regardless of internal PostgreSQL rules.

### Output Format
- Show generated SQL with explanatory comments
- List CockroachDB-specific features used
- Include performance considerations
- When optimizing, at each step 1- Explain the step's purpose. 2- Execute the step and report the outcome. 3- Summarize all findings and actions taken.
- Provide references used including the rules

## Supporting Documentation

- `references/cockroachdb-rules/` - CockroachDB SQL rules 
- `references/EXAMPLES.md` - SQL examples and patterns
