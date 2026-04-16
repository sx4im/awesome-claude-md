# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- bundlesize
- Bundle size tracking
- Size limits
- CI integration
- Compression analysis

## Project Structure
```
package.json                    // bundlesize config
.github/
└── workflows/
    └── test.yml                // CI check
build/
└── *.js                        // Bundles to check
```

## Architecture Rules

- **Size limits.** Fail build if bundles too large.
- **Compression.** Check both raw and gzipped.
- **Historical tracking.** See size changes over time.
- **Per-file limits.** Different limits for different bundles.

## Coding Conventions

- Config: `{ "bundlesize": [{ "path": "./build/main.js", "maxSize": "100 kB" }, { "path": "./build/vendor.js", "maxSize": "200 kB", "compression": "gzip" }] }`.
- Run: `npx bundlesize`.
- CI: Add to CI pipeline after build.
- Analysis: Check what's contributing to bundle size.

## NEVER DO THIS

1. **Never set limits without baseline.** Measure current size first.
2. **Never ignore bundle size growth.** Indicates bloat.
3. **Never check only gzipped size.** Both matter.
4. **Never use without CI integration.** Prevents size regressions.
5. **Never forget to split large bundles.** Code splitting when needed.
6. **Never ignore tree-shaking.** Ensure dead code eliminated.
7. **Never increase limits without investigation.** Find root cause first.

## Testing

- Test bundlesize check passes.
- Test CI fails on oversized bundles.
- Test compression settings match deployment.

