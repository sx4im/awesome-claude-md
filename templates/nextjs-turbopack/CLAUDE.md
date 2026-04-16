# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Next.js 14+ with Turbopack
- React 18+
- Turbopack (Rust-based bundler)
- App Router
- Fast HMR

## Project Structure
```
app/
├── page.tsx
├── layout.tsx
└── api/
    └── route.ts
components/
└── *.tsx
next.config.js
turbo.json                      // Turborepo config (optional)
```

## Architecture Rules

- **Turbopack dev server.** `next dev --turbo` for faster builds.
- **Webpack still production.** Turbopack only for dev currently.
- **Native imports.** No need for special loaders.
- **Fast HMR.** Sub-second updates.

## Coding Conventions

- Start: `next dev --turbo` to use Turbopack.
- Config: `next.config.js` with standard Next.js options.
- Caveats: Some webpack plugins don't work—check compatibility.
- Same patterns as standard Next.js.

## NEVER DO THIS

1. **Never use `--turbo` in production.** Development only currently.
2. **Never expect all webpack plugins to work.** Check compatibility list.
3. **Never ignore the `experimental` flags.** Some features need enabling.
4. **Never mix Turbopack with custom webpack config.** Use one or other.
5. **Never forget to test production build.** Turbopack dev, webpack build.
6. **Never use for production deployments yet.** Until Turbopack stable.
7. **Never skip `next.config.js` validation.** Different from webpack config.

## Testing

- Test dev server starts with `--turbo`.
- Test HMR updates quickly.
- Test production build (webpack) works.

