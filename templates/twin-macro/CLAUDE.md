# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Twin.macro (Tailwind + CSS-in-JS)
- Emotion or styled-components
- TypeScript 5.x
- Babel macro
- Gatsby/Next.js/Cra

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses tw macro
├── styles/
│   └── globalStyles.ts         // Global styles with tw
├── twin.d.ts                   // TypeScript declarations
└── babel-plugin-macros.config.js
```

## Architecture Rules

- **Babel macro at build time.** No runtime overhead.
- **Tailwind classes as objects.** `tw`div`bg-red-500`` becomes CSS object.
- **Composition with `tw`.** Merge classes conditionally.
- **Full Tailwind config support.** Custom theme, plugins work.

## Coding Conventions

- Import: `import tw from 'twin.macro'`.
- Basic: `const Button = tw.button`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded``.
- Composition: `const PrimaryButton = tw(Button)`bg-blue-600``.
- Conditional: `tw.div`[${condition && `bg-red-500`}]``.
- Arbitrary: `tw.div`w-[100px]``.
- Global: `const GlobalStyles = tw`@import ...`` or `tw`@apply ...``.

## NEVER DO THIS

1. **Never use without Babel macro setup.** Requires babel-plugin-macros.
2. **Never forget twin.d.ts.** TypeScript needs declarations.
3. **Never use runtime composition.** Do at build time with template literals.
4. **Never mix `tw` with `styled` carelessly.** Pick primary approach.
5. **Never ignore the `preset` option.** Choose emotion or styled-components.
6. **Never use for dynamic values.** No runtime interpolation—use CSS vars.
7. **Never skip the config path.** Twin needs to find tailwind.config.js.

## Testing

- Test macro transforms at build time.
- Test composed styles merge correctly.
- Test TypeScript recognizes tw prop types.

