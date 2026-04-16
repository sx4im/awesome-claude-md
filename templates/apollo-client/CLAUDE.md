# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Apollo Client v3 (GraphQL client)
- React 18+
- TypeScript 5.x
- GraphQL
- @apollo/client

## Project Structure

```
src/
├── lib/
│   ├── apollo-client.ts        // Client configuration
│   ├── cache.ts                // InMemoryCache config
│   └── links/                  // Apollo Link chain
│       ├── http-link.ts
│       └── auth-link.ts
├── graphql/
│   ├── queries.ts              // GraphQL documents
│   ├── mutations.ts
│   └── fragments.ts
├── hooks/
│   └── useApollo.ts            // Custom Apollo hooks
└── providers/
    └── apollo-provider.tsx     // ApolloProvider setup
```

## Architecture Rules

- **Normalized caching by default.** Apollo Client normalizes GraphQL responses automatically. Understand how it works.
- **Type policies for custom fields.** Use `typePolicies` in cache config for computed fields or pagination.
- **Links for request pipeline.** Compose links for auth, error handling, logging, retry logic.
- **Fragments for colocation.** Define fragments alongside components that use them.

## Coding Conventions

- Create client: `new ApolloClient({ uri: '/graphql', cache: new InMemoryCache() })`.
- Use hook: `const { data, loading, error } = useQuery(QUERY)`.
- Mutations: `const [mutate] = useMutation(MUTATION)`.
- Refetch: `refetch()` from useQuery result or `client.refetchQueries()`.
- Update cache: `update` option in mutations or `cache.modify()`.

## Library Preferences

- **@apollo/client:** Core client with React hooks.
- **@apollo/link-error:** Error handling link.
- **@apollo/link-retry:** Retry failed requests.
- **@apollo/link-context:** Add context (auth headers) to requests.
- **@apollo/devtools:** Chrome extension for debugging.

## File Naming

- Query files: `[Name].ts` with `gql` template literals.
- Fragment files: Co-located with components using them.
- Client config: `apollo-client.ts`

## NEVER DO THIS

1. **Never disable cache without reason.** The cache is Apollo's strength. Use `fetchPolicy: 'network-only'` sparingly.
2. **Never ignore cache updates after mutations.** Without `update` or refetch, UI shows stale data.
3. **Never use `any` for GraphQL types.** Generate TypeScript types from your schema.
4. **Never create new client instances per render.** Create once, reuse. New clients lose cache state.
5. **Never forget error boundaries.** GraphQL errors should be caught by Error Boundaries.
6. **Never mix local and remote schema without understanding.** Local resolvers are powerful but complex.
7. **Never skip the `keyFields` configuration.** Apollo needs to know how to identify entities for normalization.

## Testing

- Mock Provider with `MockedProvider` from `@apollo/client/testing`.
- Define mocks with request/response pairs.
- Test loading, error, and success states.
- Test cache updates by verifying subsequent renders.

