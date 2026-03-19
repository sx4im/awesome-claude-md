# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Docker + Docker Compose v2
- Multi-service architecture (API, database, cache, worker, proxy)
- Environment-specific overrides
- Health checks on all services
- Bind mounts for development, volumes for production

## Project Structure

```
.
├── docker/
│   ├── api/
│   │   ├── Dockerfile       # Multi-stage build for API
│   │   └── .dockerignore
│   ├── worker/
│   │   └── Dockerfile       # Worker process Dockerfile
│   └── nginx/
│       └── nginx.conf       # Reverse proxy configuration
├── docker-compose.yml       # Base compose (shared config)
├── docker-compose.dev.yml   # Dev overrides (volumes, debug ports, hot reload)
├── docker-compose.prod.yml  # Prod overrides (resource limits, restart policies)
├── .env.example             # Template for environment variables
└── scripts/
    ├── seed.sh              # Database seeding script
    └── backup.sh            # Database backup script
```

## Architecture Rules

- **Base + override compose files.** `docker-compose.yml` defines services, networks, and dependencies shared across environments. `docker-compose.dev.yml` adds hot reload, debug ports, and bind mounts. `docker-compose.prod.yml` adds resource limits, restart policies, and production images. Run with: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`.
- **One process per container.** The API runs in one container, the database in another, the worker in another. Never run multiple processes in a single container with supervisord or a shell script.
- **Named volumes for persistent data.** Database data goes in a named volume (`postgres_data:`), not a bind mount. Named volumes persist across `docker compose down` and have better performance on macOS/Windows.
- **Health checks on every service.** Every service defines a `healthcheck` in compose. `depends_on` uses `condition: service_healthy` — not just `service_started`. Without health checks, the API starts before the database is ready.
- **Networks isolate communication.** Define a `backend` network for API ↔ database ↔ cache. A `frontend` network for proxy ↔ API. The database should not be reachable from the proxy.

## Coding Conventions

- **Multi-stage Dockerfiles.** Stage 1: install dependencies. Stage 2: build. Stage 3: production image with only the built artifact and runtime deps. The final image should not contain `node_modules/devDependencies`, build tools, or source code.
- **`.dockerignore` is mandatory.** Every Dockerfile directory has a `.dockerignore` that excludes `node_modules`, `.git`, `*.md`, test files, and local env files. Without it, `docker build` copies gigabytes of unnecessary files.
- **Environment variables via `.env` files.** `docker-compose.yml` uses `env_file: .env`. Never hardcode database passwords or API keys in compose files. Distribute `.env.example` with placeholder values.
- **Pin image versions.** `FROM node:20.11-alpine` — not `FROM node:latest`. `image: postgres:16.2` — not `image: postgres`. Unpinned versions cause "works on my machine" bugs when upstream images update.
- **Use non-root users.** Every Dockerfile creates a non-root user and switches to it: `RUN adduser -D appuser` then `USER appuser`. Running as root inside containers is a security vulnerability.

## Service Naming

```yaml
services:
  api:          # Application server
  db:           # PostgreSQL, MySQL, etc.
  cache:        # Redis
  worker:       # Background job processor
  proxy:        # Nginx reverse proxy
  mailpit:      # Dev-only email catcher
```

Use short, descriptive names. All lowercase. The service name is the hostname on the Docker network: `api` connects to `db:5432`.

## NEVER DO THIS

1. **Never use `latest` tags for base images.** `node:latest` today is not `node:latest` tomorrow. Pin exact versions: `node:20.11-alpine`. This prevents builds from breaking when upstream publishes a new major version.
2. **Never store secrets in `docker-compose.yml`.** Use `.env` files (gitignored) or Docker secrets for production. Compose files are committed to git — secrets in them are secrets in your repo history forever.
3. **Never use `depends_on` without `condition: service_healthy`.** `depends_on: db` only waits for the container to start — not for PostgreSQL to be ready to accept connections. Your API will crash with "connection refused" on startup.
4. **Never run containers as root in production.** Create a non-root user in the Dockerfile and use `USER appuser`. Root in a container is root on the host if the container escapes.
5. **Never use bind mounts for database data.** Bind mounts have performance issues on macOS/Windows and don't persist cleanly. Use named volumes: `volumes: postgres_data:`.
6. **Never put everything in one Dockerfile.** Use multi-stage builds. A single-stage Dockerfile includes compilers, dev dependencies, and source code in the final image — bloating it from 100MB to 2GB.
7. **Never skip `.dockerignore`.** Without it, `COPY . .` copies `node_modules` (hundreds of MB), `.git` (entire history), and test files into the build context. Builds become slow and images become enormous.

## Development Workflow

```bash
# Start all services in dev mode
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Rebuild after Dockerfile changes
docker compose build --no-cache api

# View logs for a specific service
docker compose logs -f api

# Run a one-off command in the API container
docker compose exec api npm run migrate

# Tear down everything including volumes
docker compose down -v
```

## Testing

- Use Docker Compose to spin up test dependencies (database, cache) for integration tests.
- CI runs `docker compose build` to verify all Dockerfiles build successfully.
- Test health checks by starting services and asserting `docker compose ps` shows "healthy" for all services.
- Load test the production compose configuration to verify resource limits are adequate.
