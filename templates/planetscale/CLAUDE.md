# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- PlanetScale (serverless MySQL platform)
- Vitess-based (YouTube's scaling solution)
- Git-like branching for databases
- Deploy requests for schema changes
- Edge replication

## Project Structure
```
src/
├── db/
│   ├── connection.ts           # Connection setup (mysql2)
│   ├── schema.prisma           # ORM schema (optional)
│   └── migrations/
└── scripts/
    └── db-push.ts
```

## Architecture Rules

- **Branch-based workflows.** Create database branches like git branches for development.
- **Deploy requests for schema changes.** Review and approve schema changes before production.
- **Vitess-backed scaling.** Automatic sharding and connection pooling.
- **Edge for global distribution.** Replicate read regions globally.

## Coding Conventions

- Connection: Use `mysql2` or `planetscale` database-js driver.
- `database-js`: `import { connect } from '@planetscale/database'; const conn = connect({ host, username, password })`.
- Branching: `pscale branch create mydb dev-branch`.
- Deploy request: `pscale deploy-request create mydb dev-branch main`.
- ORM: Prisma, Drizzle work normally. Configure connection string.

## NEVER DO THIS

1. **Never connect to main branch directly for development.** Always use branches.
2. **Never make schema changes without deploy requests.** Bypassing loses audit trail.
3. **Never ignore the connection limits.** Monitor and configure connection pooling.
4. **Never use foreign key constraints.** PlanetScale recommends avoiding FKs (Vitess limitation).
5. **Never skip the edge regions if global.** Use for read replicas near users.
6. **Never commit credentials.** Use environment variables for connection strings.
7. **Never forget pscale CLI.** `pscale` CLI is essential for branch management.

## Testing

- Test branch-based development workflow.
- Test deploy request review process.
- Test connection pooling under load.

