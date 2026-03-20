# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Meteor 3+ (full-stack JavaScript/TypeScript platform)
- React 18+ (UI layer)
- MongoDB (primary database via Meteor Collections)
- TypeScript (strict mode)
- DDP (Distributed Data Protocol) for real-time pub/sub
- Meteor Methods for RPC
- Vitest or Meteor's built-in test driver

## Project Structure

```
imports/
├── api/                       # Server + shared data layer
│   ├── [feature]/
│   │   ├── collection.ts      # Mongo collection definition + schema
│   │   ├── methods.ts         # Meteor Methods (RPC endpoints)
│   │   ├── publications.ts    # DDP publications (server only)
│   │   └── types.ts           # TypeScript interfaces
├── ui/
│   ├── components/            # Reusable React components
│   ├── pages/                 # Route-level page components
│   ├── layouts/               # Layout wrappers
│   └── hooks/                 # Custom React hooks
├── startup/
│   ├── client/                # Client-specific initialization
│   │   └── index.ts
│   └── server/                # Server-specific initialization
│       ├── index.ts
│       ├── fixtures.ts        # Seed data
│       └── migrations.ts      # Data migrations
client/
├── main.tsx                   # Client entry point (imports startup/client)
server/
├── main.ts                    # Server entry point (imports startup/server)
```

## Architecture Rules

- **Everything lives in `imports/`.** Meteor 3 uses lazy evaluation. Code in `imports/` only runs when explicitly imported. The `client/main.tsx` and `server/main.ts` files are the only eager entry points that import everything else.
- **Publications for reads, Methods for writes.** Use `Meteor.publish` to reactively stream data to clients via DDP. Use `Meteor.methods` for validated write operations. Never write to collections directly from the client.
- **Collections are defined once, used everywhere.** Define each MongoDB collection in `imports/api/[feature]/collection.ts`. Import the same collection on both client (MiniMongo) and server (real Mongo). Never create separate client/server collection instances.
- **Schema validation on collections.** Attach a schema using `collection2` or custom validation in Methods. MongoDB is schemaless, but your app should not be. Validate every insert and update.
- **Methods must validate with `check()`.** Every Meteor Method validates its arguments using `check(arg, Match.pattern)` or Zod. Never trust client-submitted arguments.

## Coding Conventions

- **Use `useTracker` for reactive data.** In React components, wrap Meteor reactive data sources (subscriptions, collection queries) in `useTracker(() => { ... })`. Never call `Collection.find()` outside a reactive context.
- **Use `useSubscribe` for subscriptions.** The `useSubscribe('publicationName', ...args)` hook handles subscription lifecycle. Check loading state with the returned `isLoading`. Never call `Meteor.subscribe` directly in components.
- **Async Methods in Meteor 3.** Meteor 3 Methods are async by default. Use `async/await` in Method definitions. On the client, `Meteor.callAsync('methodName', args)` returns a Promise. Never use the old callback pattern.
- **Organize by feature in `imports/api/`.** Each feature gets its own directory with collection, methods, publications, and types. Never dump all methods in a single `methods.ts` file.
- **Use `this.userId` in Methods and Publications.** Access the authenticated user's ID via `this.userId`. Never pass userId as a Method argument from the client.

## Library Preferences

- **Routing:** [React Router 6+] or `ostrio:flow-router-extra`. Defined in `imports/startup/client/`.
- **Schema validation:** [simpl-schema] with `collection2` or Zod for Method argument validation.
- **Accounts:** `accounts-password`, `accounts-google`, `accounts-github` (Meteor packages). Never implement custom auth.
- **Styling:** [Tailwind CSS] or [styled-components]. Configure in `client/`.
- **Rate limiting:** `ddp-rate-limiter` (built-in). Apply to Methods and subscriptions. Never skip rate limiting on public Methods.

## File Naming

- Collections: `imports/api/[feature]/collection.ts`
- Methods: `imports/api/[feature]/methods.ts`
- Publications: `imports/api/[feature]/publications.ts`
- Pages: `imports/ui/pages/[Feature]Page.tsx`
- Components: `imports/ui/components/[ComponentName].tsx`
- Hooks: `imports/ui/hooks/use[Hook].ts`

## NEVER DO THIS

1. **Never use `allow`/`deny` rules on collections.** This is Meteor's legacy client-side write system. It is inherently insecure. All writes must go through validated Methods. Remove any `Collection.allow()` calls.
2. **Never publish entire collections without filters.** Always limit publications with `{ fields: {}, limit: N }`. Publishing all documents or all fields leaks data and kills performance.
3. **Never put code outside `imports/` (except entry points).** Files in `client/`, `server/`, `lib/` outside `imports/` are eagerly loaded and cannot be tree-shaken. This is a legacy pattern that bloats bundles.
4. **Never use `Meteor.call` with callbacks in Meteor 3.** Use `Meteor.callAsync` with `await`. The callback pattern is deprecated and doesn't work with Meteor 3's async Method handlers.
5. **Never store files in MongoDB directly.** Use `ostrio:files` or an external service (S3, Cloudflare R2) for file storage. MongoDB documents have a 16MB limit and GridFS adds unnecessary complexity.
6. **Never skip `check()` in Methods.** Unvalidated Methods are the most common Meteor security vulnerability. The `audit-argument-checks` package will throw if any Method skips validation.
7. **Never subscribe in a loop or without cleanup.** Subscriptions inside `useEffect` without cleanup cause memory leaks. Always use `useSubscribe` or return the subscription's `stop()` in the cleanup function.

## Testing

- **Method tests:** Import Method definitions and invoke with `call` against a test MongoDB instance. Use `meteor/test-helpers` for `userId` stubbing.
- **Publication tests:** Use `publication-collector` package to capture published documents without a DDP connection. Assert correct filtering and field projection.
- **Component tests:** Use `@testing-library/react`. Mock `useTracker` and `useSubscribe` to provide deterministic data. Never depend on a running Meteor server in unit tests.
- **Integration tests:** Run `meteor test --full-app --driver-package=meteortesting:mocha` for full-app integration tests with a real MongoDB.
- Run tests: `meteor test --driver-package=meteortesting:mocha` or `npx vitest` for pure unit tests.
