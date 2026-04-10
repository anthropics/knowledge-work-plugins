# Client Connection Examples for TLS

This reference provides TLS connection strings and configuration for common database clients connecting to CockroachDB.

## Connection String Format

The standard PostgreSQL connection string format with TLS parameters:

```
postgresql://<username>:<password>@<host>:26257/<database>?sslmode=verify-full&sslrootcert=<ca-cert-path>
```

**SSL modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| `verify-full` | Verify server cert + hostname | **Production (recommended)** |
| `verify-ca` | Verify server cert only | When hostname mismatch is expected |
| `require` | Encrypt but don't verify cert | Development only |
| `disable` | No TLS | Never use with CockroachDB Cloud |

## CLI Clients

### cockroach sql

```bash
# Password authentication
cockroach sql \
  --url "postgresql://<user>:<password>@<host>:26257/defaultdb?sslmode=verify-full&sslrootcert=<ca.crt>"

# Client certificate authentication
cockroach sql \
  --url "postgresql://<user>@<host>:26257/defaultdb?sslmode=verify-full&sslrootcert=<ca.crt>&sslcert=client.<user>.crt&sslkey=client.<user>.key"

# Using individual flags
cockroach sql \
  --certs-dir=certs \
  --host=<host> \
  --port=26257 \
  --user=<user>
```

### psql

```bash
# Password authentication
psql "postgresql://<user>:<password>@<host>:26257/defaultdb?sslmode=verify-full&sslrootcert=<ca.crt>"

# Client certificate authentication
psql "sslmode=verify-full sslrootcert=<ca.crt> sslcert=client.<user>.crt sslkey=client.<user>.key host=<host> port=26257 dbname=defaultdb user=<user>"
```

### DBeaver

1. Create a new CockroachDB connection
2. In **SSL** tab:
   - Check **Use SSL**
   - **Root certificate:** Path to CA certificate
   - **SSL mode:** `verify-full`
3. For client certificate auth:
   - **Client certificate:** Path to `client.<user>.crt`
   - **Client key:** Path to `client.<user>.key`

**Common DBeaver issue:** DBeaver may need the CA cert in Java KeyStore format. Convert with:
```bash
keytool -import -alias cockroachdb -file ca.crt \
  -keystore truststore.jks -storepass changeit -noprompt
```

## Application Drivers

### Go (pgx)

```go
// Password authentication
connStr := "postgresql://user:password@host:26257/defaultdb?sslmode=verify-full&sslrootcert=ca.crt"
conn, err := pgx.Connect(context.Background(), connStr)

// Client certificate authentication
connStr := "postgresql://user@host:26257/defaultdb?sslmode=verify-full&sslrootcert=ca.crt&sslcert=client.user.crt&sslkey=client.user.key"
conn, err := pgx.Connect(context.Background(), connStr)
```

### Python (psycopg2)

```python
import psycopg2

# Password authentication
conn = psycopg2.connect(
    host="<host>",
    port=26257,
    database="defaultdb",
    user="<user>",
    password="<password>",
    sslmode="verify-full",
    sslrootcert="ca.crt"
)

# Client certificate authentication
conn = psycopg2.connect(
    host="<host>",
    port=26257,
    database="defaultdb",
    user="<user>",
    sslmode="verify-full",
    sslrootcert="ca.crt",
    sslcert="client.<user>.crt",
    sslkey="client.<user>.key"
)
```

### Java (JDBC)

```java
// Password authentication
String url = "jdbc:postgresql://<host>:26257/defaultdb?sslmode=verify-full&sslrootcert=ca.crt";
Connection conn = DriverManager.getConnection(url, "<user>", "<password>");

// Client certificate authentication
String url = "jdbc:postgresql://<host>:26257/defaultdb"
    + "?sslmode=verify-full"
    + "&sslrootcert=ca.crt"
    + "&sslcert=client.<user>.crt"
    + "&sslkey=client.<user>.key.pk8";
Connection conn = DriverManager.getConnection(url, "<user>", "");
```

**Java key format:** JDBC requires the client key in PKCS#8 DER format:
```bash
openssl pkcs8 -topk8 -inform PEM -outform DER \
  -in client.<user>.key -out client.<user>.key.pk8 -nocrypt
```

### Node.js (node-postgres / pg)

```javascript
const { Pool } = require('pg');
const fs = require('fs');

// Password authentication
const pool = new Pool({
  host: '<host>',
  port: 26257,
  database: 'defaultdb',
  user: '<user>',
  password: '<password>',
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('ca.crt').toString(),
  },
});

// Client certificate authentication
const pool = new Pool({
  host: '<host>',
  port: 26257,
  database: 'defaultdb',
  user: '<user>',
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('ca.crt').toString(),
    cert: fs.readFileSync('client.<user>.crt').toString(),
    key: fs.readFileSync('client.<user>.key').toString(),
  },
});
```

### TypeORM

```typescript
// ormconfig.ts
{
  type: "cockroachdb",
  host: "<host>",
  port: 26257,
  username: "<user>",
  password: "<password>",
  database: "defaultdb",
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync("ca.crt").toString(),
  },
}
```

**Common TypeORM issue:** `DEPTH_ZERO_SELF_SIGNED_CERT` error means the CA cert is not being loaded. Verify the path to `ca.crt` is correct.

## Notes

- CockroachDB Cloud always requires TLS — `sslmode=disable` will fail
- The default port for CockroachDB is 26257 (not 5432 like standard PostgreSQL)
- Client certificate key files must have restrictive permissions: `chmod 0600 client.*.key`
- When using connection pools, ensure all pool connections use the same TLS configuration
- For CockroachDB Cloud, download the CA cert from the Cloud Console or via `ccloud cluster cert`
