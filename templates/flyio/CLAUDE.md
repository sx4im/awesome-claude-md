# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fly.io (global application platform)
- Firecracker microVMs
- Docker containers
- PostgreSQL (managed or LiteFS)
- Edge deployment

## Project Structure
```
src/
├── ...                         # Application code
fly.toml                        # Fly configuration
Dockerfile                      # Container definition
```

## Architecture Rules

- **fly.toml for configuration.** App name, services, environment, mounts defined here.
- **Dockerfile for builds.** Or use buildpacks for common frameworks.
- **Regions for distribution.** Deploy to multiple regions for global presence.
- **Volumes for persistent data.** Or use LiteFS for SQLite replication.

## Coding Conventions

- Launch: `fly launch` creates `fly.toml` and app.
- Deploy: `fly deploy` builds and releases.
- Scale: `fly scale count 3` for horizontal scaling.
- Regions: `fly regions add fra` for Frankfurt region.
- Secrets: `fly secrets set KEY=value` (encrypted).
- Postgres: `fly postgres create` provisions cluster.
- SSH: `fly ssh console` for debugging.

## NEVER DO THIS

1. **Never commit secrets to fly.toml.** Use `fly secrets` for sensitive data.
2. **Never use build cache incorrectly.** Sometimes need `--no-cache` for clean builds.
3. **Never ignore volume placement.** Volumes are region-specific—match with app regions.
4. **Never forget to set `internal_port` in fly.toml.** Must match app's listening port.
5. **Never deploy without health checks.** Configure `[http_service.checks]` in fly.toml.
6. **Never ignore the swap configuration.** Small VMs may need swap for memory spikes.
7. **Never use Fly Postgres as backup target.** It's for operational data, not backups.

## Testing

- Test locally with `fly deploy --build-only`.
- Test in staging region before production regions.
- Test database connections from app instances.

