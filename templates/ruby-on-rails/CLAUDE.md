# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Ruby 3.2+
- Ruby on Rails 7.1+
- Hotwire (Turbo & Stimulus)
- PostgreSQL
- Tailwind CSS
- Redis & Sidekiq (for background jobs)
- RSpec (for testing)

## Project Structure

```
app/
├── models/                  # ActiveRecord models, validations, associations
├── controllers/             # ActionController classes
├── views/                   # ERB templates and Turbo Stream templates
│   ├── layouts/
│   └── users/
├── helpers/                 # View helpers
├── javascript/              # Importmap / esbuild roots
│   ├── controllers/         # Stimulus controllers
│   └── application.js       # JS entry point
├── jobs/                    # ActiveJob classes (Sidekiq)
├── mailers/                 # ActionMailer classes
├── components/              # ViewComponent classes and templates
└── services/                # Plain Old Ruby Objects (POROs) for business logic
config/
├── routes.rb                # Routing
├── database.yml             # DB configuration
└── environments/            # Dev, Test, Prod settings
db/
├── migrate/                 # Schema migrations
└── schema.rb                # Auto-generated schema definition
spec/                        # RSpec tests (or test/ for Minitest)
```

## Architecture Rules

- **Fat Models, Skinny Controllers (mostly).** Controllers should do three things: grab params, call the model/service, and render a response. All business logic and validations belong in the Model or dedicated Service objects.
- **Service Objects for complex logic.** If a Model starts doing too much (sending emails, calling external APIs, multi-model orchestrations), extract a Service Object (`app/services/create_user_service.rb`).
- **Use Hotwire for reactivity, not SPAs.** Use Turbo Drive for fast navigation, Turbo Frames for isolated component updates, and Turbo Streams for real-time WebSocket updates. Resort to Stimulus.js only when you need client-side interactivity (like toggling a modal or copying text).
- **Keep views logicless.** Use Helpers or ViewComponents. Do not write complex `if/else` logic or database queries inside ERB templates.
- **Background Jobs for slow tasks.** Anything that takes longer than 200ms (sending emails, webhook processing, report generation) must go to a background job (`ActiveJob` + Sidekiq).

## Coding Conventions

- **Follow standard Rails naming conventions.** Models are singular (`User`), Controllers are plural (`UsersController`), DB tables are plural (`users`). Foreign keys are `model_id` (`user_id`). Don't fight Rails naming.
- **Use standard RESTful routes.** Stick to `index, show, new, create, edit, update, destroy`. If you need more actions, you probably need a new controller (`Users::PasswordsController` instead of `UsersController#update_password`).
- **Use the hash rocket (`=>`) only for string keys.** Otherwise, use the standard Ruby 1.9+ syntax `key: value`.
- **Prefer `ActiveRecord` query methods over raw SQL.** Use `where`, `joins`, and `includes`.
- **Use `!` methods correctly.** `save!` and `create!` raise exceptions on validation failure. Use them in background jobs or when a failure means a critical system error. Use `save` and `create` in controllers where you handle the `false` return to render errors to the user.

## Library Preferences

- **Testing:** RSpec with FactoryBot (instead of Minitest and Fixtures).
- **Frontend reactivity:** Hotwire (Turbo + Stimulus) — not Vue, React, or custom JS, unless building a strict API for a mobile app.
- **CSS:** Tailwind CSS via `tailwindcss-rails`.
- **Background Jobs:** Sidekiq (requires Redis) — faster and more robust than DelayedJob or Solid Queue for high volume.
- **Pagination:** Pagy — significantly faster and uses less memory than Kaminari or WillPaginate.

## NEVER DO THIS

1. **Never write `N+1` database queries.** If you are looping through `@users` and rendering `@user.posts.count`, you will trigger a query per user. Use `includes(:posts)` in the controller to eager-load associations.
2. **Never query the database in the view.** All data required by the view must be instantiated as instance variables (`@post`) in the controller.
3. **Never skip CSRF protection.** Rails protects form submissions by default. Do not disable `protect_from_forgery` unless building a strictly stateless API endpoint.
4. **Never put secrets in code.** Use `Rails.application.credentials` or `.env` via the `dotenv` gem. Never commit API keys or Stripe secrets.
5. **Never use `default_scope` in models.** It applies to *every* query by default and is notoriously difficult to override cleanly later. Prefer explicitly called class methods or standard scopes (`scope :active, -> { where(active: true) }`).
6. **Never leave controllers unpaginated if a collection can grow.** A simple `User.all` will crash your server when you hit 10,000 users.
7. **Never perform I/O in migrations.** Migrations change database structure. Don't call external APIs, send emails, or do complex data processing inside `db/migrate/`. Use rake tasks or background scripts for data backfills.

## Testing

- **RSpec is the standard.** Write model specs for validations and business logic.
- **System tests over controller tests.** Use Capybara + Selenium/Cuprite to test the full user flow (login, click button, see result). Controller tests are structurally deprecated for UI testing.
- **FactoryBot for mock data.** Use factories instead of raw fixtures. Let FactoryBot handle associations.
- Run tests regularly: `bundle exec rspec`.
