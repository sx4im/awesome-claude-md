# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with Sequelize
- Sequelize 6.x
- Model definition
- Migrations
- Associations

## Project Structure
```
src/
├── models/
│   ├── index.ts                // Sequelize setup
│   └── user.ts                 // Model definitions
├── migrations/
├── seeders/
└── routes/
```

## Architecture Rules

- **Model definitions.** Define tables and relationships.
- **Sequelize CLI.** For migrations and seeders.
- **Associations.** HasMany, BelongsTo, etc.
- **Scopes.** Predefined query filters.

## Coding Conventions

- Model: `User.init({ id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true }, name: DataTypes.STRING }, { sequelize, modelName: 'user' })`.
- Association: `User.hasMany(Post); Post.belongsTo(User)`.
- Query: `const users = await User.findAll({ where: { age: { [Op.gt]: 18 } }, include: Post })`.
- Migration: `npx sequelize-cli migration:generate --name create-user`.

## NEVER DO THIS

1. **Never use `sync({ force: true })` in production.** Drops tables!
2. **Never skip migrations.** Database version control essential.
3. **Never ignore the `underscored` option.** For snake_case columns.
4. **Never forget to handle associations properly.** Define both directions.
5. **Never use raw queries without replacements.** `{ replacements: { id } }`.
6. **Never ignore the `paranoid` option.** Soft deletes with `deletedAt`.
7. **Never mix async and sync methods.** Sequelize methods are async.

## Testing

- Test with `sqlite-memory` for unit tests.
- Test migrations up/down.
- Test associations eager loading.

