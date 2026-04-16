# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- URQL v4 (GraphQL client)
- React 18+
- TypeScript 5.x
- GraphQL
- Next.js 15+ or Vite

## Project Structure

```
src/
├── lib/
│   ├── urql-client.ts          // Client configuration
│   └── exchanges/              // Custom exchanges
├── graphql/
│   ├── queries/
│   │   └── GetUsers.graphql
│   ├── mutations/
│   │   └── CreateUser.graphql
│   └── fragments/
│       └── UserFields.graphql
├── hooks/
│   └── useGraphQL.ts           // Custom URQL hooks
└── providers/
    └── urql-provider.tsx       // Provider wrapper
```

## Architecture Rules

- **Exchanges for customization.** URQL's power is in its exchange system. Use built-ins and create custom exchanges.
- **CacheExchange for caching.** The default cache exchange handles GraphQL caching intelligently.
- **Document caching for static data.** Operation caching for dynamic data.
- **Custom exchanges for cross-cutting concerns.** Auth, logging, error handling go in exchanges.

## Coding Conventions

- Create client: `createClient({ url: '/graphql', exchanges: [cacheExchange, fetchExchange] })`.
- Use hook: `const [result] = useQuery({ query: GET_USERS_QUERY })`.
- Handle states: `result.fetching`, `result.error`, `result.data`.
- Mutations: `const [, execute] = useMutation(CREATE_USER_MUTATION)`.
- Refetch: `client.query(QUERY, vars).toPromise()` or `result.reexecute()`.

## Library Preferences

- **@urql/exchange-graphcache:** Normalized caching for complex apps.
- **@urql/exchange-auth:** Authentication exchange for tokens.
- **@urql/exchange-retry:** Automatic retry for failed requests.
- **@urql/devtools:** DevTools exchange for debugging.

## File Naming

- Query files: `[OperationName].graphql` → `GetUsers.graphql`
- Client config: `urql-client.ts`
- Exchange files: `[name]-exchange.ts`

## NEVER DO THIS

1. **Never skip the cacheExchange.** Without it, every query hits the network. Always include it.
2. **Never ignore requestPolicy.** `cache-first` vs `network-only` matter. Choose based on data freshness needs.
3. **Never use URQL without understanding exchanges.** Exchanges are middleware. Know what each one does.
4. **Never forget to normalize GraphCache config.** Without proper keys, cache updates after mutations fail.
5. **Never use string queries without type generation.** Generate TypeScript types from GraphQL schema.
6. **Never mix multiple GraphQL clients.** Pick URQL or Apollo, not both.
7. **Never ignore the suspense integration.** URQL works with React Suspense. Use it for better UX.

## Testing

- Mock URQL client in tests with `mockClient` from `@urql/core`.
- Test exchanges by wrapping them around mock operations.
- Test components with `Provider` wrapping with mock client.
- Test cache behavior by executing multiple operations.

