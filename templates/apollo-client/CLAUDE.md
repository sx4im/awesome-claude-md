# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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
