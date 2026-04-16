# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Coolify (self-hosted PaaS)
- Docker-based deployments
- Git integration
- Let's Encrypt SSL
- Server management

## Project Structure
```
src/
├── ...                         # Application code
coolify.json                    # Coolify configuration
docker-compose.yml              # Multi-service apps
Dockerfile
```

## Architecture Rules

- **Self-hosted alternative to Heroku/Railway.** Run on your own servers.
- **Docker Compose or Dockerfile.** Define services and builds.
- **Git-based deployments.** Connect repo for auto-deploy on push.
- **Resource isolation.** Each app runs in Docker containers.

## Coding Conventions

- Connect repo: Add GitHub/GitLab repository in Coolify UI.
- Configure build: Select Dockerfile or Docker Compose.
- Environment: Set env vars in Coolify UI or via `.env` file.
- Domains: Configure custom domains with auto SSL.
- Databases: Deploy PostgreSQL, MySQL, Redis as separate services.
- Health checks: Configure in Coolify for auto-restart.

## NEVER DO THIS

1. **Never expose Coolify dashboard publicly without auth.** It controls your servers.
2. **Never forget to configure firewall.** Only expose necessary ports.
3. **Never ignore backup configuration.** Coolify can backup databases—enable it.
4. **Never use without server monitoring.** Install monitoring alongside Coolify.
5. **Never skip SSL configuration.** Let's Encrypt is automatic—use it.
6. **Never deploy without resource limits.** Set CPU/memory limits per service.
7. **Never forget to update Coolify.** Security updates are important.

## Testing

- Test deployment on staging server first.
- Test Git webhooks trigger deployments.
- Test SSL certificate renewal.

