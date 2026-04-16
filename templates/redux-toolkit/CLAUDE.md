# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Redux Toolkit (RTK) v2
- React Redux v9
- React 18+
- TypeScript 5.x
- Redux DevTools Extension

## Project Structure

```
src/
├── store/
│   ├── index.ts                # Store configuration
│   ├── root-reducer.ts         # Combined reducers
│   └── middleware.ts           // Custom middleware
├── features/
│   ├── auth/
│   │   ├── authSlice.ts        // Redux slice
│   │   ├── authSelectors.ts    // Memoized selectors
│   │   └── authThunks.ts       // Async thunks
│   └── posts/
│       ├── postsSlice.ts
│       └── postsThunks.ts
├── hooks/
│   └── redux.ts                // Typed useDispatch, useSelector
└── ...
```

## Architecture Rules

- **Feature-based slices.** Each domain (auth, posts, users) has its own slice with reducer, actions, and selectors.
- **RTK Query for API calls.** Use RTK Query for server state instead of manual thunks where applicable.
- **Selectors in slices.** Define selectors alongside slices using `createSelector` for memoization.
- **Thunks for async logic.** Use `createAsyncThunk` for API calls and side effects.

## Coding Conventions

- Create slice: `createSlice({ name: 'auth', initialState, reducers: { ... } })`.
- Export actions: `export const { login, logout } = authSlice.actions`.
- Export reducer: `export default authSlice.reducer`.
- Use selectors: `const user = useSelector(selectCurrentUser)` with memoized selectors.
- Dispatch: `const dispatch = useAppDispatch()` (typed version).
- Thunks: `createAsyncThunk('auth/login', async (credentials) => { ... })`.

## Library Preferences

- **RTK Query:** For API endpoints. Replaces manual fetch + caching logic.
- **Immer:** Built into RTK. Mutative updates in reducers are fine.
- **Reselect:** Built into RTK via `createSelector` for memoized selectors.
- **DevTools:** Redux DevTools Extension integration built-in.

## File Naming

- Slice files: `[feature]Slice.ts` → `authSlice.ts`
- Thunk files: `[feature]Thunks.ts` or co-located in slice.
- Selector files: `[feature]Selectors.ts` or in slice.

## NEVER DO THIS

1. **Never use plain Redux without Toolkit.** RTK eliminates boilerplate and prevents common mistakes. Always use RTK.
2. **Never define action types as strings manually.** RTK generates these. Don't use `const LOGIN = 'LOGIN'` pattern.
3. **Never mutate state in non-RTK reducers.** Outside `createSlice`, immutability rules apply. Spread operators only.
4. **Never ignore selector memoization.** Inline selectors like `state => state.auth.user` cause re-renders. Use `createSelector`.
5. **Never use `connect` HOC.** Use hooks: `useSelector`, `useDispatch`. `connect` is legacy API.
6. **Never store derived data in Redux.** Compute in selectors, not reducers.
7. **Never put non-serializable data in Redux.** No Dates (use timestamps), no functions, no class instances.

## Testing

- Test slices by calling reducers directly with actions.
- Test thunks by dispatching and checking state changes.
- Test selectors with mock state.
- Use `configureStore` in tests with preloaded state.

