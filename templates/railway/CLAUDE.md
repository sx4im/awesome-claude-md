# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Railway (application hosting platform)
- Docker or Nixpacks builds
- PostgreSQL, Redis, MongoDB add-ons
- GitHub/GitLab integration
- Environment variables & secrets

## Project Structure
```
src/
├── ...                         # Application code
railway.json                    # Railway configuration (optional)
Dockerfile                      # Optional custom build
.nixpacks/                      # Nixpacks configuration
```

## Architecture Rules

- **Git-based deployments.** Push to branch deploys automatically.
- **Nixpacks or Docker.** Nixpacks auto-detects, Docker for custom builds.
- **Add-ons for data services.** PostgreSQL, Redis, etc. provisioned via UI/CLI.
- **Environments for stages.** Production, staging, PR environments.

## Coding Conventions

- Deploy: `railway up` or push to connected repo.
- Variables: `railway variables set KEY=value` or via dashboard.
- Database: Add PostgreSQL addon, `DATABASE_URL` auto-injected.
- Domains: Auto-generated or custom domain in settings.
- Logs: `railway logs` or dashboard streaming.

## NEVER DO THIS

1. **Never commit secrets to repo.** Use Railway environment variables.
2. **Never ignore the build logs.** Nixpacks detection can fail—check logs.
3. **Never forget to set `PORT`.** Railway sets `PORT` env var—app must listen on it.
4. **Never use SQLite in production.** Use PostgreSQL addon instead.
5. **Never ignore health checks.** Configure proper health endpoints.
6. **Never deploy without checking resource limits.** Monitor CPU/memory usage.
7. **Never forget to configure start command.** Custom `railway.json` if auto-detection fails.

## Testing

- Test deployment with `railway up` locally.
- Test in PR environment before merging.
- Test with production-like database.

