# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Verdaccio (private npm registry)
- Node.js 20+
- NPM/Yarn/PNPM compatible
- Auth plugins
- Uplinks to npmjs

## Project Structure
```
config.yaml                   // Verdaccio configuration
storage/                      // Local package storage
htpasswd                      // User credentials
packages/
```

## Architecture Rules

- **Proxy to npm.** Cache public packages locally.
- **Private packages.** Publish internal packages.
- **Authentication.** HTpasswd, GitHub, GitLab, etc.
- **Access control.** Who can publish/access packages.

## Coding Conventions

- Config: `storage: ./storage; uplinks: { npmjs: { url: https://registry.npmjs.org/ } }; packages: { '@mycompany/*': { access: $authenticated, publish: $authenticated, proxy: npmjs } }`.
- Auth: `auth: { htpasswd: { file: ./htpasswd } }`.
- Middleware: Custom plugins for logging, notifications.
- Publish: `npm publish --registry http://localhost:4873`.

## NEVER DO THIS

1. **Never expose Verdaccio publicly without auth.** Private packages at risk.
2. **Never forget to configure HTTPS in production.** Use reverse proxy.
3. **Never skip backup for local storage.** `storage/` directory.
4. **Never use `allow_publish: '*'` blindly.** Restrict publishing rights.
5. **Never ignore the `max_body_size`.** For large packages.
6. **Never forget uplink timeout settings.** Prevent hanging.
7. **Never use default config in production.** Customize auth, access, storage.

## Testing

- Test publishing and installing packages.
- Test auth with different providers.
- Test uplink fallback when npmjs down.
- Test with scoped packages.
- Test with scoped packages.
