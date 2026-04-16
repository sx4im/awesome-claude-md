# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Tailwind Variants (TV)
- Tailwind CSS v3+
- TypeScript 5.x
- React/Vue/Svelte/Any
- Slot-based API

## Project Structure
```
src/
├── components/
│   └── Card.tsx                // Uses tv
├── lib/
│   └── tv.ts                   // TV config
└── styles/
    └── slots.ts                // Shared slot patterns
```

## Architecture Rules

- **Slots for complex components.** `base`, `header`, `body`, `footer` as separate style targets.
- **Compound slots.** Style combinations across slots.
- **Responsive variants.** Breakpoint-based styling.
- **Overrides.** Easy style overrides per instance.

## Coding Conventions

- Define: `const card = tv({ slots: { base: 'rounded-lg shadow', header: 'px-4 py-2 border-b', body: 'p-4', footer: 'px-4 py-2 border-t' }, variants: { color: { primary: { base: 'bg-blue-50', header: 'border-blue-200' } } } })`.
- Use: `const { base, header, body, footer } = card({ color: 'primary' }); <div className={base()}><div className={header()}>Title</div>...</div>`.
- Override: `<Card classNames={{ base: 'my-custom-class', header: 'custom-header' }} />`.

## NEVER DO THIS

1. **Never use slots for simple components.** Overkill for buttons.
2. **Never forget to call slot functions.** `base()` not `base`.
3. **Never ignore the `extend` feature.** Extend existing components.
4. **Never skip `createTV` for global config.** Set defaults once.
5. **Never use without `tailwind-merge`.** Required for proper merging.
6. **Never create circular slot references.** Slots can't reference each other.
7. **Never ignore the `responsiveVariants` array.** Configure breakpoints explicitly.

## Testing

- Test slot composition renders correctly.
- Test overrides merge properly.
- Test responsive variants at different breakpoints.

