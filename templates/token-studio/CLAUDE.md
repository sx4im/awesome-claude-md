# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Tokens Studio for Figma
- Figma plugin
- JSON token format
- Style Dictionary integration
- Multi-theme support

## Project Structure
```
tokens/
├── $metadata.json               // Token metadata
├── $themes.json                // Theme definitions
├── global.json                 // Global tokens
├── light.json                  // Light theme
└── dark.json                   // Dark theme
figma/
└── tokens.json                 // Exported from Figma
```

## Architecture Rules

- **Figma-native workflow.** Design in Figma, export tokens.
- **Token sets.** Organize by theme, platform, or category.
- **References.** Link tokens to create relationships.
- **Multi-theme.** Light, dark, brand variants.

## Coding Conventions

- Structure: Organize in Figma with groups (color, typography, spacing).
- References: In Figma, use `{color.base.blue}` to reference another token.
- Themes: Create separate token sets for light/dark, enable per theme.
- Export: `tokens.json` exported from plugin.
- Transform: Use Style Dictionary to convert to CSS, SCSS, etc.

## NEVER DO THIS

1. **Never edit exported JSON directly.** Edit in Figma, re-export.
2. **Never skip backing up tokens.** Figma file or repo sync.
3. **Never use without naming conventions.** Consistent token names.
4. **Never forget about token types.** Color, dimension, fontFamily, etc.
5. **Never ignore the `resolveReferences` option.** When exporting.
6. **Never mix design and code tokens without sync.** Regular export/import.
7. **Never skip the Style Dictionary step.** Transform for code usage.

## Testing

- Test tokens export correctly.
- Test references resolve in Figma.
- Test theme switching in Figma.

