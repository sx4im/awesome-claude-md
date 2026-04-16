# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Relay (Facebook's GraphQL client)
- React 18+
- TypeScript 5.x
- GraphQL
- Babel/Relay Compiler

## Project Structure

```
src/
├── __generated__/              // Relay generated files (gitignored)
├── components/
│   ├── User.tsx                // Component with fragment
│   └── UserQuery.tsx           // Query component
├── mutations/
│   └── CreateUserMutation.ts   // Mutation definitions
├── subscriptions/
│   └── UserSubscription.ts     // Subscription definitions
├── relay/
│   ├── environment.ts          // Relay Environment
│   └── network.ts              // Network layer
└── schema.graphql              // GraphQL schema
```

## Architecture Rules

- **Fragments for data masking.** Components declare their data needs with fragments. Parent components compose fragments.
- **Compiler enforces correctness.** Relay Compiler validates queries against schema and generates types.
- **Normalization and garbage collection.** Relay normalizes data and removes unused records automatically.
- **Entry points for data fetching.** Top-level queries fetch data, child components use fragments.

## Coding Conventions

- Define fragment: `graphql` template literal with `fragment User_user on User { name email }`.
- Use fragment: `const user = useFragment(graphql`...`, props.user)`.
- Fetch query: `const data = usePreloadedQuery(query, props.queryReference)`.
- Mutations: `commitMutation(environment, { mutation, variables })`.
- Subscriptions: `requestSubscription(environment, { subscription })`.

## Library Preferences

- **relay-compiler:** Must run to generate types and validate queries.
- **react-relay:** React hooks and components.
- **babel-plugin-relay:** Transform GraphQL literals at build time.
- **relay-config.json:** Compiler configuration.

## File Naming

- Fragment files: Co-located with component: `User.tsx` has `User_user` fragment.
- Mutation files: `[Name]Mutation.ts`.
- Generated files: `__generated__/[Name].graphql.ts`.

## NEVER DO THIS

1. **Never use inline queries without the compiler.** Relay requires the compiler to run. Without it, no types, no validation.
2. **Never bypass fragment data masking.** Accessing fields not in your fragment breaks encapsulation.
3. **Never forget `@relay(plural: true)` for arrays.** Without it, Relay doesn't track array items correctly.
4. **Never use fragments without spreading them in a parent query.** Orphan fragments never fetch data.
5. **Never ignore the garbage collector.** Keep references to records you need with `retain()`.
6. **Never skip pagination helpers.** Use `usePaginationFragment` or `useBlockingPaginationFragment` for lists.
7. **Never mix Relay with another GraphQL client.** Relay owns the cache. Other clients cause conflicts.

## Testing

- Test with `createMockEnvironment` from `relay-test-utils`.
- Mock network responses with `mock.resolve()`.
- Test fragments by providing mock data that matches fragment types.
- Test mutations by verifying optimistic updates and commit payloads.

