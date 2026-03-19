# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Elixir 1.15+ / Erlang/OTP 26+
- Phoenix Framework 1.7+ (LiveView, HEEx)
- PostgreSQL + Ecto (Database mapping)
- Tailwind CSS
- Phoenix PubSub (Realtime)

## Project Structure

```
├── lib/
│   ├── my_app/              # Core business logic (Contexts & Schemas)
│   │   ├── accounts/
│   │   │   ├── user.ex      # Ecto schema
│   │   │   └── accounts.ex  # Context module (public API boundary)
│   │   ├── mailer.ex        # Swoosh mailer configuration
│   │   └── repo.ex          # Ecto generic database repo
│   └── my_app_web/          # Web frontend (LiveView, controllers, views)
│       ├── controllers/     # API or standard HTML controllers
│       ├── live/            # Phoenix LiveView modules
│       │   ├── user_live/
│       │   │   ├── index.ex # LiveView module
│       │   │   └── index.html.heex  # Co-located template
│       ├── components/      # Functional HEEx components
│       │   ├── core_components.ex  # Reusable UI (Button, Modal, Input)
│       │   └── layouts/     # Root & App layouts
│       ├── router.ex        # Web routes
│       └── endpoint.ex      # Phoenix endpoint config
├── priv/
│   └── repo/
│       ├── migrations/      # Ecto migrations
│       └── seeds.exs        # Database seed script
├── test/                    # ExUnit tests
├── mix.exs                  # Project dependencies
└── config/                  # Configuration (dev, test, prod)
```

## Architecture Rules

- **Contexts are the Public API.** The web layer (`my_app_web`) only calls functions in Context modules (`MyApp.Accounts.get_user!(id)`). The web layer never references Ecto schemas (`MyApp.Accounts.User`) directly in `Repo` queries.
- **Schemas are data structures, not active records.** Ecto schemas describe data shape and map changesets. They do not have `save()` or `update()` methods. All database operations happen through `MyApp.Repo` in Context functions.
- **LiveView for dynamic UI.** Use LiveView (`use MyAppWeb, :live_view`) for reactive, stateful UIs without writing JavaScript. State is held on the server, and diffs are pushed over WebSockets.
- **Function Components.** Write reusable UI using HEEx function components in `my_app_web/components/`. Call them like `<.button phx-click="save">Save</.button>`.
- **OTP for background processes.** Use GenServers, Tasks, or robust background job libraries (Oban) for concurrent or scheduled work. Don't use standard OS cron if it can live in the BEAM.

## Coding Conventions

- **Pipe operator `|>` everywhere.** Chain functional transformations instead of nesting calls or assigning multiple intermediate variables.
- **Pattern matching and guards.** Use pattern matching in function heads to handle different cases instead of large `if/else` or `cond` blocks.
- **`with` statements for sequential operations.** Use `with` to chain operations that might fail, rather than deep nesting of `case` statements.
- **Bang vs Non-Bang functions.** `get_user!` raises an exception if not found. `get_user` returns `{:ok, user}` or `{:error, reason}`. Handlers in LiveView and Controllers should pattern match on the ok/error tuple.
- **Documentation.** Use `@moduledoc` and `@doc` to document modules and public functions. Use ExDoc conventions.

## Library Preferences

- **Database:** Ecto — Standard for all Phoenix apps.
- **Realtime:** Phoenix PubSub and Phoenix Channels — Built-in, extremely scalable.
- **Background Jobs:** Oban — PostgreSQL-backed job queues, robust and transactional.
- **Auth:** `mix phx.gen.auth` — Built-in generators for battle-tested authentication. Not a third-party dependency.
- **Email:** Swoosh — Built-in local mailer and production adapters.

## NEVER DO THIS

1. **Never write raw SQL for standard queries.** Use Ecto.Query. It's safe, composable, and compiled. Only use `Ecto.Adapters.SQL.query` for complex specialized queries that Ecto can't express.
2. **Never block the LiveView process.** A LiveView process handles UI interactions. Heavy computations or slow API calls inside `handle_event` freeze the UI for that user. Delegate to `Task.async` or a background job.
3. **Never bypass the Context layer.** Don't query `MyApp.Repo.all(User)` from controllers or LiveViews. This leaks database structure into the web layer and breaks architectural isolation.
4. **Never ignore `{:error, changeset}` returns.** Form submissions must handle both the success case and the error case, passing the errored Ecto changeset back to the LiveView to display field errors.
5. **Never put business logic in LiveViews.** LiveViews orchestrate state and handle user events but should delegate data mutation to Contexts.
6. **Never leave `config/prod.secret.exs` in git.** Use standard Elixir `runtime.exs` or ENV parameters to configure production secrets safely.
7. **Never use `throw` or `catch`.** Elixir uses Exceptions (`raise`/`rescue`) strictly for exceptional events, and `{:ok, val}`/`{:error, val}` tuples for expected control flow.

## Testing

- Use **ExUnit** (built-in).
- **Context tests:** Test the business logic directly using `DataCase`. Verify changesets and database inserts.
- **LiveView tests:** Use `Phoenix.LiveViewTest` to mount LiveViews, simulate clicks/forms (`render_click`, `render_change`), and assert on the rendered HTML diffs.
- Isolate database tests using `Ecto.Adapters.SQL.Sandbox`, which wraps every test in a transaction that is rolled back, enabling async, fast, parallel testing.
