# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Symfony 7 (PHP framework)
- PHP 8.3+
- Doctrine ORM
- Twig templates
- Flex for project management

## Project Structure
```
├── config/
├── src/
│   ├── Controller/
│   │   └── UserController.php
│   ├── Entity/
│   │   └── User.php
│   ├── Repository/
│   └── Form/
│       └── UserType.php
├── templates/
│   └── user/
│       └── index.html.twig
└── tests/
```

## Architecture Rules

- **Bundle-based organization.** Controllers, entities, templates grouped by domain.
- **Dependency injection container.** Services configured in `services.yaml`.
- **Doctrine for ORM.** Entities, repositories, migrations.
- **Twig for templates.** Template inheritance and components.

## Coding Conventions

- Controller: `class UserController extends AbstractController { public function index(UserRepository $repo): Response { ... } }`.
- Route: `#[Route('/users', name: 'user_index')]` attribute.
- Entity: `#[ORM\Entity] class User { #[ORM\Id, ORM\GeneratedValue, ORM\Column] private ?int $id = null; }`.
- Form: `class UserType extends AbstractType { public function buildForm(FormBuilderInterface $builder, array $options): void { $builder->add('name', TextType::class); } }`.
- Template: `{{ user.name }}`, `{% for user in users %}`, `{% extends 'base.html.twig' %}`.

## NEVER DO THIS

1. **Never put business logic in controllers.** Use services.
2. **Never ignore dependency injection.** Don't use `new Service()`, use injection.
3. **Never skip form validation.** Symfony forms handle validation—use it.
4. **Never forget to clear cache after config changes.** `php bin/console cache:clear`.
5. **Never use raw SQL without parameter binding.** SQL injection risk.
6. **Never ignore security.yaml configuration.** Firewalls, access control matter.
7. **Never commit `.env.local` with secrets.** Use `.env.local` for local secrets—gitignore it.

## Testing

- Test with PHPUnit.
- Test controllers with `WebTestCase`.
- Test forms with `FormTestCase`.

