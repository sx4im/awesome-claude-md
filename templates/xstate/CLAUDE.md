# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- XState v5 (state machines and statecharts)
- React 18+
- TypeScript 5.x
- @xstate/react for React integration
- XState Store (lightweight alternative)

## Project Structure

```
src/
├── machines/
│   ├── index.ts                // Machine exports
│   ├── auth.machine.ts         // Auth state machine
│   ├── checkout.machine.ts     // Checkout flow
│   └── form.machine.ts         // Complex form handling
├── hooks/
│   └── useMachines.ts          // Machine hook wrappers
└── lib/
    └── machine-utils.ts        // Shared machine patterns
```

## Architecture Rules

- **Machines for complex state.** Use XState when state has multiple modes, transitions, and side effects.
- **Declarative statecharts.** Define all possible states, events, and transitions upfront in the machine config.
- **Actors for encapsulation.** Spawn child machines or actors for independent subsystems.
- **Actions for side effects.** Keep side effects in actions (entry, exit, transition), not in components.

## Coding Conventions

- Define machine: `const machine = setup({ ... }).createMachine({ ... })` in XState v5.
- Use in components: `const [state, send] = useMachine(machine)`.
- Check state: `state.matches('idle')`, `state.matches({ loading: 'fetching' })`.
- Send events: `send({ type: 'FETCH' })` or `send({ type: 'SUBMIT', data })`.
- Use context: `state.context` for data associated with the machine.

## Library Preferences

- **@xstate/react:** `useMachine`, `useActor` hooks.
- **@xstate/store:** Lightweight store for simple global state.
- **@xstate/inspect:** Visualize machines in XState Viz or Stately Studio.
- **@xstate/test:** Model-based testing utilities.

## File Naming

- Machine files: `[domain].machine.ts` → `auth.machine.ts`
- Type files: `[domain].types.ts` for machine types.
- Barrel export: `machines/index.ts`

## NEVER DO THIS

1. **Never use XState for simple toggle state.** `useState` is fine for booleans. XState shines in complex flows.
2. **Never put side effects directly in components.** Actions should be in the machine, not `useEffect` around `useMachine`.
3. **Never ignore the statechart pattern.** Model all states explicitly. Avoid "catch-all" states that hide complexity.
4. **Never forget to handle all events.** Use `always` transitions or ensure every event has a target, even if it's a no-op.
5. **Never spawn actors without cleanup.** Child actors must be stopped when the parent unmounts.
6. **Never use `send` without type safety.** XState v5 has strong typing. Define event types properly.
7. **Never visualize only in your head.** Use Stately Studio or XState Viz to draw statecharts. They catch logic errors.

## Testing

- Test machines independently of React. They're pure logic.
- Use `@xstate/test` for model-based testing.
- Test all transitions by sending events and asserting state.
- Test actions by mocking effects and verifying they're called.

