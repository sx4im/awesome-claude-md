# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Nx Plugin development
- Custom generators
- Custom executors
- Workspace tools
- Devkit

## Project Structure
```
tools/
├── my-plugin/
│   ├── generators/
│   │   └── my-generator/
│   │       ├── schema.json
│   │       └── index.ts
│   ├── executors/
│   │   └── my-executor/
│   │       ├── schema.json
│   │       └── index.ts
│   └── plugin.ts
└── tsconfig.tools.json
```

## Architecture Rules

- **Generators scaffold code.** Create files, modify existing.
- **Executors run tasks.** Build, test, deploy custom steps.
- **Schema defines inputs.** JSON schema for validation.
- **Composable.** Generators can call other generators.

## Coding Conventions

- Generator: `export default async function (tree: Tree, schema: any) { generateFiles(tree, join(__dirname, 'files'), schema.projectRoot, schema); addProjectConfiguration(tree, schema.name, { ... }) }`.
- Executor: `export default async function (options: any, context: ExecutorContext) { console.log(options.myOption); return { success: true } }`.
- Schema: `{ "$schema": "http://json-schema.org/schema", "type": "object", "properties": { "name": { "type": "string" }, "directory": { "type": "string" } }, "required": ["name"] }`.
- Register: `const plugin: NxPlugin = { name: '@scope/my-plugin', ... }`.

## NEVER DO THIS

1. **Never forget `schema.json` for generators/executors.** Required for CLI.
2. **Never skip input validation.** Schema validates, but double-check in code.
3. **Never use sync file operations in generators.** Use `tree` async methods.
4. **Never ignore the `context` in executors.** Workspace, project info.
5. **Never forget to test generators.** Run with `nx generate` and verify.
6. **Never skip caching hints.** `cacheableOperations` in `nx.json`.
7. **Never publish plugin without testing locally.** `nx generate` from dist.

## Testing

- Test generators with temporary workspaces.
- Test executors with `nx run`.
- Test with `e2e` target in plugin.

