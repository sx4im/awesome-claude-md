# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Oxc (JavaScript toolchain)
- Rust-based
- Parser, linter, formatter
- Resolver
- TypeScript checker (planned)

## Project Structure
```
.oxc.json                       // Oxc configuration
package.json
src/
└── ...                         // Code processed by Oxc
```

## Architecture Rules

- **Next-gen toolchain.** Replaces Babel, ESLint parts.
- **Ultra-fast.** Rust performance for JS tooling.
- **Modular.** Use only needed components.
- **Parser first.** Foundation for other tools.

## Coding Conventions

- Parser: `oxc_parser` for parsing JS/TS to AST.
- Linter: `oxlint` for linting (ESLint-compatible rules).
- Resolver: `oxc_resolver` for Node.js module resolution.
- Transformer: Future Babel replacement.
- Formatter: Future Prettier alternative.

## NEVER DO THIS

1. **Never use Oxc for production yet.** Early development stage.
2. **Never expect full ESLint compatibility.** Subset of rules.
3. **Never skip reading Oxc architecture.** Different from Babel.
4. **Never use without testing output.** Verify AST transformations.
5. **Never mix Oxc parser with Babel transforms yet.** Compatibility evolving.
6. **Never ignore the performance gains.** Benchmark vs existing tools.
7. **Never forget to follow Oxc development.** Rapid changes expected.

## Testing

- Test parser output matches ESTree spec.
- Test linter rules catch issues.
- Test performance vs existing tools.

