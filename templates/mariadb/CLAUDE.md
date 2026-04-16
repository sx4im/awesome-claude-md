# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- MariaDB 11.x (MySQL fork)
- Python (aiomysql, mysql-connector-python)
- Node.js (mysql2)
- JSON support, ColumnStore
- Galera Cluster for HA

## Project Structure
```
src/
├── db/
│   ├── connection.py           # Connection pooling
│   ├── migrations/
│   └── models.py               # ORM models (SQLAlchemy)
├── queries/
│   └── *.sql
└── config/
    └── database.py
```

## Architecture Rules

- **Drop-in MySQL replacement.** Compatible with MySQL clients and protocols.
- **JSON data type.** Native JSON support with indexing via virtual columns.
- **ColumnStore for analytics.** Columnar storage engine for OLAP workloads.
- **Galera Cluster for HA.** True multi-master synchronous replication.

## Coding Conventions

- Connection pool: Use connection pooling in all environments.
- JSON columns: `CREATE TABLE users (id INT PRIMARY KEY, data JSON)`.
- JSON indexing: `CREATE INDEX idx_name ON users ((JSON_VALUE(data, '$.name')))`.
- Async Python: `aiomysql.create_pool(...)` for async applications.
- Transactions: Explicit `BEGIN`, `COMMIT`, `ROLLBACK` or context managers.

## NEVER DO THIS

1. **Never assume MariaDB = MySQL behavior.** Small differences in optimizer, features.
2. **Never skip connection pooling.** Creating connections per request is expensive.
3. **Never use MyISAM.** Use InnoDB for ACID compliance and row-level locking.
4. **Never store JSON without considering query patterns.** Index frequently queried paths.
5. **Never ignore character set configuration.** Use utf8mb4 for full Unicode support.
6. **Never run production without backups.** mysqldump, MariaDB Backup, or replication.
7. **Never use root user for application connections.** Create dedicated users with limited privileges.

## Testing

- Test query performance with `EXPLAIN`.
- Test Galera cluster behavior with node failures.
- Test JSON indexing effectiveness.

