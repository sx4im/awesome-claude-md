# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Docker Compose**: Container orchestration (v2.24+)
- **Docker Engine**: Container runtime
- **YAML**: Service definition language
- **Networks**: Container communication
- **Volumes**: Persistent storage
- **Healthchecks**: Service readiness probes

## Project Structure

```
docker-compose/
├── docker-compose.yml          # Main compose file
├── docker-compose.override.yml # Local overrides
├── docker-compose.prod.yml     # Production config
├── .env                        # Environment variables
├── .env.example                # Example env vars
├── Dockerfile                  # App container
└── scripts/
    ├── init-db.sh              # Initialization
    └── wait-for-it.sh          # Dependency waiting
```

## Architecture Rules

- **Override pattern.** Base `docker-compose.yml` + `docker-compose.override.yml` for local. Separate prod config.
- **Service dependencies.** Use `depends_on` with `condition: service_healthy`. Wait for readiness, not just start.
- **Volume management.** Named volumes for persistence. Bind mounts for development hot-reload.
- **Environment files.** `.env` for local secrets. Never commit. `.env.example` with dummy values.
- **Health checks.** Define for all services. `healthcheck` with proper intervals and retries.

## Coding Conventions

- **Service definition.** `service_name: image: ... ports: ... environment: ... volumes: ...`.
- **Network aliases.** Use service name as DNS. `db` resolves to database container on same network.
- **Build context.** `build: context: . dockerfile: Dockerfile`. Separate build and runtime.
- **Secrets.** Use `secrets` for sensitive data. Mounted as files, not env vars. More secure.
- **Profiles.** Use `profiles: ["dev"]` for optional services. `docker compose --profile dev up`.

## NEVER DO THIS

1. **Never commit .env with secrets.** Add to `.gitignore`. Use `.env.example` as template.
2. **Never use latest tags.** Pin to specific versions. Reproducible builds require version pinning.
3. **Never run production on Compose.** Use Kubernetes or Swarm for production. Compose is for dev/test.
4. **Never ignore resource limits.** Set `deploy.resources` for memory/CPU. Prevents local machine slowdown.
5. **Never use container_name carelessly.** Fixed names prevent scaling. Let Compose generate names.
6. **Never forget about volumes pruning.** `docker compose down -v` removes volumes. Data loss warning.
7. **Never skip health checks.** Services start before ready causes connection failures. Health checks prevent this.

## Testing

- **Compose build.** `docker compose build` succeeds. No Dockerfile errors.
- **Service startup.** All services reach healthy state. `docker compose ps` shows healthy.
- **Connectivity testing.** Services can communicate. Database reachable from app container.
- **Volume persistence.** Data persists across restarts. Stop, start, data still there.
- **Override testing.** `docker-compose.override.yml` applies correctly. Local dev config works.

## Claude Code Integration

- Use `@docker-compose*.yml` for orchestration patterns
- Reference `@scripts/` for initialization and waiting scripts
- Apply container development from architecture rules
- Validate against Docker Compose best practices in NEVER DO THIS
