# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Stencil (Web Components compiler)
- TypeScript
- JSX support
- Lazy loading
- Framework-agnostic output

## Project Structure
```
src/
├── components/
│   ├── my-button/
│   │   ├── my-button.tsx       // Stencil component
│   │   ├── my-button.css
│   │   └── my-button.e2e.ts    // E2E tests
│   └── my-card/
├── utils/
│   └── helpers.ts
└── index.html
```

## Architecture Rules

- **Compiler-based.** Generates optimized Web Components.
- **Decorators for metadata.** `@Component`, `@Prop`, `@State`, `@Event`.
- **JSX templating.** React-like JSX syntax.
- **Framework bindings.** Generates React, Vue, Angular wrappers.

## Coding Conventions

- Component: `@Component({ tag: 'my-button', styleUrl: 'my-button.css', shadow: true }) export class MyButton { @Prop() label: string; @State() count = 0; render() { return <button>{this.label}</button>; } }`.
- Props: `@Prop() label: string;` (immutable from outside).
- State: `@State() count = 0;` (internal mutable).
- Events: `@Event() myClick: EventEmitter; this.myClick.emit(data)`.

## NEVER DO THIS

1. **Never mutate @Prop directly.** Props are immutable.
2. **Never forget the @Component decorator.** Required metadata.
3. **Never use without understanding shadow vs scoped.** `shadow: true/false`.
4. **Never skip the `dist-custom-elements` output.** For tree-shaking.
5. **Never ignore the `hydrated` flag.** Check before DOM operations.
6. **Never mix mutable patterns with @State.** Mutate state object, trigger re-render.
7. **Never forget to build before testing in other frameworks.** Generates wrappers.

## Testing

- Test with Jest and Puppeteer.
- Test component methods directly.
- Test in consuming frameworks (React, Vue, Angular).

