# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- Django 5.x with Django REST Framework
- PostgreSQL 15+
- Celery + Redis for background tasks
- django-allauth for authentication
- Django ORM (no raw SQL unless profiled and justified)

## Project Structure

```
project/
├── config/                  # Project-level settings
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── local.py         # Dev overrides (DEBUG=True)
│   │   └── production.py    # Prod overrides (security, logging)
│   ├── urls.py              # Root URL conf
│   ├── celery.py            # Celery app setup
│   └── wsgi.py
├── apps/
│   ├── users/               # Custom user model and auth
│   ├── orders/              # Business domain app
│   └── notifications/       # Cross-cutting: email, push, in-app
├── common/                  # Shared base classes, mixins, utils
│   ├── models.py            # TimestampedModel base class
│   ├── permissions.py       # Shared DRF permissions
│   └── pagination.py        # Standard pagination classes
├── templates/               # Django HTML templates (if serving HTML)
├── static/
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
└── manage.py
```

## Architecture Rules

- **One app per business domain.** `apps/users/`, `apps/orders/`, `apps/billing/`. Never create an app called `utils` or `helpers` — those go in `common/`.
- **Fat models, thin views.** Business logic lives on model methods and managers, not in views or serializers. Views are glue code: validate input, call model/service, return response.
- **Custom User model from day one.** Always subclass `AbstractUser` in `apps/users/models.py`. Migrating away from Django's default User later is painful enough to justify this even for toy projects.
- **Settings are split by environment.** `base.py` has everything shared. `local.py` imports from base and sets `DEBUG=True`. `production.py` imports from base and enforces `SECURE_SSL_REDIRECT`, `HSTS`, etc. Never use a single `settings.py` with `if DEBUG:` conditionals.
- **Celery for anything that takes more than 500ms.** Email sending, PDF generation, external API calls, image processing — all go in Celery tasks. Never block a request/response cycle with slow I/O.

## Coding Conventions

- **Model field ordering:** primary key → foreign keys → required fields → optional fields → timestamps. Every model inherits from `TimestampedModel` in `common/models.py` which adds `created_at` and `updated_at`.
- **Serializer naming:** `{Model}ListSerializer`, `{Model}DetailSerializer`, `{Model}CreateSerializer`. Never use one serializer for both list and detail — list serializers should be lean.
- **URL naming:** `{app}:{action}-{resource}` → `users:detail-user`, `orders:list-orders`, `orders:create-order`.
- **Manager methods over QuerySet filters in views.** `Order.objects.pending()` is better than `Order.objects.filter(status='pending')` scattered across views.
- **Use `select_related` and `prefetch_related` in every queryset that touches foreign keys.** N+1 queries are the #1 performance killer. Add `django-debug-toolbar` in development and check the SQL panel.

## DRF Conventions

- Viewsets for CRUD resources: `ModelViewSet` or `ReadOnlyModelViewSet`. For custom endpoints, use `@action` decorators — never create standalone API views for resource sub-actions.
- Permissions live in `common/permissions.py` and are composed per view: `permission_classes = [IsAuthenticated, IsOwnerOrAdmin]`.
- Pagination is standardized in `common/pagination.py`. Use `PageNumberPagination` with `page_size=25`. Never return unbounded querysets.
- Filters use `django-filter` with explicit `FilterSet` classes. Never use `SearchFilter` alone — it's too loose for production.

## Library Preferences

- **Auth:** `django-allauth` — handles email verification, social login, and account management. Not `djoser` (less polished) and not `django-rest-auth` (abandoned).
- **Tasks:** Celery + Redis — not Django-Q (smaller community, fewer production deployments). Not `huey` (fine for small projects but lacks Celery's monitoring).
- **Admin:** Django's built-in admin with `django-unfold` for a modern UI. Not Jet (abandoned). Not building a custom admin from scratch.
- **Environment config:** `django-environ` to load `.env` files. Not `python-decouple` (django-environ integrates with Django settings patterns better).
- **Testing:** `pytest-django` — not Django's built-in `TestCase` (pytest is more composable, fixtures are better than setUp/tearDown).

## File Naming

- Apps: `snake_case` → `apps/user_profiles/`, `apps/order_management/`
- Models: one file per app `models.py`, split into `models/` package with `__init__.py` if a single file exceeds 300 lines
- Serializers: `serializers.py` per app
- Views: `views.py` per app, or `views/` package for complex apps
- URLs: `urls.py` per app, included in `config/urls.py`
- Tasks: `tasks.py` per app (Celery auto-discovers these)
- Tests: `tests/` directory per app with `test_models.py`, `test_views.py`, `test_serializers.py`

## NEVER DO THIS

1. **Never use the default `User` model.** Always create a custom user model in `apps/users/` that extends `AbstractUser`. Swapping the user model after migrations exist requires nuking the database.
2. **Never put business logic in serializers.** Serializers validate and transform data. Business rules (pricing calculations, permission checks, state transitions) belong in model methods or a service layer.
3. **Never write raw SQL unless you've profiled the ORM query first.** Django's ORM handles 99% of cases. If you need raw SQL, wrap it in a manager method with a comment explaining why the ORM wasn't sufficient.
4. **Never return unbounded querysets from API endpoints.** Always paginate. An endpoint that returns 50,000 rows will crash the server and the client. Set pagination globally in DRF settings.
5. **Never use `ForeignKey(on_delete=models.CASCADE)` without thinking.** CASCADE deletes are dangerous on user-facing data. Use `PROTECT` or `SET_NULL` for most foreign keys and handle deletions explicitly.
6. **Never send email synchronously in a view.** Use Celery: `send_welcome_email.delay(user.id)`. Synchronous email blocks the response and fails silently if the SMTP server is slow.
7. **Never store secrets in `settings.py`.** Use environment variables loaded via `django-environ`. `SECRET_KEY`, `DATABASE_URL`, and API keys come from `.env` (gitignored).

## Testing

- Use `pytest-django` with `pytest-factoryboy` for model factories. Never construct test data with `Model.objects.create()` inline — use factories.
- Test views via DRF's `APIClient`. Assert status codes and response structure, not implementation details.
- Test model methods and managers directly — these contain business logic.
- Use `@pytest.mark.django_db` on tests that hit the database. Tests without this marker run faster.
- Celery tasks: test the task function directly (it's just a function). Test the `.delay()` path separately with `CELERY_ALWAYS_EAGER=True` in test settings.
