# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- ReScript (type-safe JavaScript)
- React 18+ bindings
- Vite/Webpack integration
- Pattern matching, pipe operator
- Zero runtime overhead

## Project Structure
```
src/
├── components/
│   └── Button.res               // ReScript component
├── bindings/
│   └── External.res             // External bindings
├── lib/
│   └── Utils.res                // Pure functions
└── bsconfig.json
```

## Architecture Rules

- **Sound type system.** No runtime type errors possible.
- **JavaScript output.** Compiles to readable JS.
- **React first-class.** `@rescript/react` for components.
- **Pattern matching exhaustive.** Compiler ensures all cases handled.

## Coding Conventions

- Component: `@react.component let make = (~name: string) => { <div> {React.string(name)} </div> }`.
- Hooks: `let (count, setCount) = React.useState(() => 0)`.
- Pattern match: `switch user { | Admin => ... | Guest => ... }`.
- Pipe: `data -> Array.map(fn) -> Array.filter(pred)`.
- Records: `type user = {name: string, age: int}; let user = {name: "John", age: 30}`.

## NEVER DO THIS

1. **Never ignore compiler warnings.** Treat as errors.
2. **Never use `Obj.magic`.** Unsafe escape hatch—avoid.
3. **Never skip `bsconfig.json` setup.** Proper configuration critical.
4. **Never mix ReScript with TS carelessly.** Keep boundaries clear.
5. **Never forget `rescript` npm script.** `rescript build`, `rescript dev`.
6. **Never ignore the generated JS.** Review occasionally for sanity.
7. **Never use without understanding the module system.** Different from JS.

## Testing

- Test with `rescript-test` or Jest.
- Test bindings work correctly.
- Test compiled JS runs without errors.

