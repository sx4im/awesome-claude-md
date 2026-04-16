# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Style Dictionary
- Design tokens
- Multi-platform output
- Transform groups
- Token transforms

## Project Structure
```
tokens/
├── color/
│   └── base.json               // Color tokens
├── size/
│   └── font.json               // Size tokens
└── index.js                    // Token definitions
config.json                     // Style Dictionary config
build/                          // Generated outputs
```

## Architecture Rules

- **Design tokens as source of truth.** Single definition, multiple outputs.
- **Multi-platform.** CSS, SCSS, iOS, Android, JS outputs.
- **Transforms.** Convert values between formats.
- **Build pipeline.** Generate platform-specific files.

## Coding Conventions

- Tokens: `{ "color": { "base": { "gray": { "light": { "value": "#CCCCCC" } } } } }`.
- References: `{ "value": "{color.base.gray.light.value}" }`.
- Config: `{ "source": ["tokens/**/*.json"], "platforms": { "scss": { "transformGroup": "scss", "buildPath": "build/scss/", "files": [{ "destination": "_variables.scss", "format": "scss/variables" }] } } }`.
- Build: `npx style-dictionary build`.

## NEVER DO THIS

1. **Never edit generated files.** Always edit source tokens.
2. **Never forget to run build after token changes.** Generated files are artifacts.
3. **Never hardcode token values outside build.** Reference generated files.
4. **Never skip the transform group.** Handles unit conversions, etc.
5. **Never use without version controlling source tokens.** Generated files can be gitignored.
6. **Never forget about themes.** Separate files or token sets for themes.
7. **Never ignore the `filter` option.** Exclude tokens from specific platforms.

## Testing

- Test build generates all platform files.
- Test token references resolve correctly.
- Test transforms apply correctly.

