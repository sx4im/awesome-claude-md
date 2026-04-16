# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- UnoCSS with Attributify preset
- Vue/React/Svelte
- Semantic attributes for styling
- Clean component markup

## Project Structure
```
src/
├── components/
│   └── Button.vue              // Uses attributify attributes
├── uno.config.ts               // Attributify preset enabled
└── App.vue
```

## Architecture Rules

- **Attributes instead of classes.** `m-4` becomes `m="4"`.
- **Grouped utilities.** `flex="~ col gap-4"` groups flex-related classes.
- **Cleaner templates.** Separates styling from logic in markup.
- **Same power as classes.** All UnoCSS features available.

## Coding Conventions

- Enable: `presets: [presetAttributify(), presetWind()]`.
- Basic: `<div m="4" p="4" bg="blue-500" />`.
- Grouped: `<div flex="~ col gap-4 items-center" />`.
- Complex: `<div text="sm white dark:gray-400" font="bold" />`.
- Breakpoints: `<div md:p="8" sm:p="4" />`.

## NEVER DO THIS

1. **Never use without presetAttributify.** Won't work out of the box.
2. **Never mix class and attribute styles carelessly.** Pick one approach per component.
3. **Never forget quotes.** Attribute values with special chars need quotes.
4. **Never use for very dynamic values.** Classes better for computed styles.
5. **Never ignore the `type` declaration.** TS projects need attributify types.
6. **Never skip the `prefix` option.** Use `uno-` prefix to avoid conflicts.
7. **Never forget about CSS specificity.** Same specificity as classes.

## Testing

- Test all attributify patterns compile.
- Test responsive attributify works.
- Test TypeScript recognizes attributes.
- Test with Vue templates.
- Test with Vue templates.
