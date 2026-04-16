# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- pnpm workspace versioning
- pnpm publish
- Workspace protocol
- Granular version control

## Project Structure

```
packages/
├── pkg-a/
│   └── package.json
└── pkg-b/
    └── package.json
pnpm-workspace.yaml
package.json
```

## Architecture Rules

- **Independent or fixed versioning.** Choose between all packages same version or independent.
- **Workspace protocol links.** `"dep": "workspace:^"` links to local package.
- **pnpm version updates.** `pnpm version` bumps and updates dependents.
- **pnpm publish from-git.** Publish only packages with version changes.

## Coding Conventions

- Version package: `pnpm version patch --filter @scope/pkg`.
- Version recursively: `pnpm -r version patch`.
- Publish: `pnpm publish -r`.
- Publish from git: `pnpm publish -r --filter "...[HEAD~1]"`.
- Update workspace ranges: `pnpm -r update --latest`.

## NEVER DO THIS

1. **Never manually edit version in workspace packages.** Use `pnpm version`.
2. **Never forget `workspace:` protocol.** Without it, published package may have wrong dependency ranges.
3. **Never publish without building.** `prepublishOnly` script should build.
4. **Never ignore the `publishConfig`.** Set `access: public` for scoped packages.
5. **Never mix registry and workspace references.** Be consistent.
6. **Never forget to commit version bumps.** They must be in git before publishing.
7. **Never publish in CI without npm token.** Configure `NPM_TOKEN` secret.

## Testing

- Test with `pnpm publish --dry-run`.
- Verify workspace links with `pnpm list`.
- Test in CI with Verdaccio or similar local registry.

