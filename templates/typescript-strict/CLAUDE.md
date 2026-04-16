# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- TypeScript 5.4+
- Strict mode enabled
- No implicit any
- Strict null checks
- Exhaustive type checking

## Project Structure
```
src/
├── lib/
│   └── utils.ts                // Strictly typed code
tests/
└── utils.test.ts
package.json
tsconfig.json                   // Strict configuration
```

## Architecture Rules

- **Strict mode on.** All strict flags enabled in tsconfig.
- **Explicit types.** No implicit `any` anywhere.
- **Null safety.** Handle undefined/null explicitly.
- **Exhaustive checks.** Switch statements cover all cases.

## Coding Conventions

- tsconfig: `{ "compilerOptions": { "strict": true, "noImplicitAny": true, "strictNullChecks": true, "strictFunctionTypes": true, "strictBindCallApply": true, "strictPropertyInitialization": true, "noImplicitThis": true, "alwaysStrict": true, "noUnusedLocals": true, "noUnusedParameters": true, "exactOptionalPropertyTypes": true, "noImplicitReturns": true, "noFallthroughCasesInSwitch": true } }`.
- Types: `function greet(name: string): string { return `Hello ${name}` }`.
- Null checks: `if (user === undefined) throw new Error('User not found')`.
- Exhaustive: `switch (status) { case 'active': ...; case 'inactive': ...; default: const _exhaustive: never = status; throw new Error(_exhaustive) }`.

## NEVER DO THIS

1. **Never use `any` type.** Use `unknown` with type guards.
2. **Never disable strict flags for convenience.** Fix the types instead.
3. **Never use non-null assertion (`!`) carelessly.** Check for null first.
4. **Never ignore `strictFunctionTypes` errors.** Contravariance enforcement.
5. **Never use `ts-ignore` without comment.** Explain why.
6. **Never forget `exactOptionalPropertyTypes`.** Distinguish `undefined` from missing.
7. **Never skip `noFallthroughCasesInSwitch`.** All cases must be handled.

## Testing

- Test with `tsc --noEmit` passes.
- Test edge cases with strict types.
- Test null/undefined handling.

