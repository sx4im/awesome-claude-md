# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Kamal (deploy tool by 37signals)
- Docker containers
- Traefik reverse proxy
- Any cloud/VPS provider
- Zero-downtime deploys

## Project Structure
```
src/
├── ...                         # Application code
config/
├── deploy.yml                  # Kamal configuration
└── deploy.staging.yml          # Staging overrides
Dockerfile
```

## Architecture Rules

- **Docker-based deployments.** Build once, run anywhere.
- **Traefik for load balancing.** Automatic SSL, routing.
- **Multiple servers supported.** Deploy to fleet of servers.
- **Accessory services.** Databases, caches as separate containers.

## Coding Conventions

- Config: `config/deploy.yml` defines servers, image, env.
- Setup: `kamal setup` prepares servers.
- Deploy: `kamal deploy` builds and deploys.
- Env: `kamal env push` updates environment variables.
- Logs: `kamal logs` tails application logs.
- Console: `kamal console` runs interactive console.
- Accessories: Define database/redis in `accessories` section.

## NEVER DO THIS

1. **Never skip `kamal setup` on new servers.** Required for Docker, Traefik, etc.
2. **Never use without Docker registry.** Kamal pushes to registry, pulls on servers.
3. **Never ignore the healthcheck.** Configure in Dockerfile or deploy.yml.
4. **Never forget to configure Traefik labels.** For routing and SSL.
5. **Never deploy without database migrations plan.** Run migrations carefully.
6. **Never use `kamal deploy` without testing locally.** `kamal build` first.
7. **Never ignore server SSH key setup.** Kamal needs SSH access to deploy.

## Testing

- Test with `kamal build` locally.
- Test on staging servers before production.
- Test rollback with `kamal rollback`.

