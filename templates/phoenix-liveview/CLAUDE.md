# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Phoenix LiveView (real-time server-rendered UI)
- Elixir 1.16+
- Phoenix 1.7+
- Tailwind CSS
- WebSocket communication

## Project Structure
```
lib/
├── my_app/
│   ├── live/
│   │   ├── user_live/
│   │   │   ├── index.ex        # LiveView module
│   │   │   └── index.html.heex # Template
│   │   └── home_live.ex
│   └── web/
│       ├── components/
│       │   └── core_components.ex
│       └── router.ex
```

## Architecture Rules

- **Server-rendered, stateful.** UI state on server, updates via WebSocket.
- **Mount, render, handle_event.** Core lifecycle functions.
- **HEEx templates.** HTML+EEx for templates with change tracking.
- **No JavaScript required.** Interactivity without writing JS (mostly).

## Coding Conventions

- LiveView: `defmodule MyApp.UserLive.Index do use MyApp, :live_view`.
- Mount: `def mount(_params, _session, socket) do { :ok, assign(socket, users: list_users()) } end`.
- Handle event: `def handle_event("delete", %{"id" => id}, socket) do ... {:noreply, socket} end`.
- Template: `<button phx-click="delete" phx-value-id={user.id}>Delete</button>`.
- JS commands: `JS.push("validate") |> JS.add_class(...)` for client-side effects.

## NEVER DO THIS

1. **Never store large state in socket.** Memory usage grows per connection.
2. **Never ignore the connected? check.** `mount` runs twice—once static, once connected.
3. **Never block the LiveView process.** Long operations should be async Tasks.
4. **Never forget CSRF tokens.** LiveView includes them—don't disable.
5. **Never ignore JavaScript interoperability.** Sometimes `Phoenix.LiveView.JS` isn't enough.
6. **Never use LiveView for static pages.** Regular controllers are better for mostly-static content.
7. **Never forget to test connected and disconnected mounts.** Both paths matter.

## Testing

- Test with `Phoenix.LiveViewTest`.
- Test `mount` assigns correctly.
- Test `handle_event` updates state.

