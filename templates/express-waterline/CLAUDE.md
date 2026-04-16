# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with Waterline
- Waterline ORM (Sails.js)
- Adapter-based
- NoSQL and SQL support
- Bluebird promises

## Project Structure
```
api/
├── models/
│   └── User.js                 // Waterline models
├── controllers/
└── policies/
config/
└── connections.js              // Database connections
```

## Architecture Rules

- **Adapter-based.** Connect to any database via adapters.
- **Model attributes.** Define schema in models.
- **Lifecycle callbacks.** `beforeCreate`, `afterUpdate`, etc.
- **Associations.** Built-in relation support.

## Coding Conventions

- Model: `module.exports = { attributes: { name: { type: 'string', required: true }, email: { type: 'string', unique: true }, age: { type: 'number' } } }`.
- Query: `const users = await User.find({ age: { '>': 18 } }).populate('pets')`.
- Create: `const user = await User.create({ name: 'John', email: 'john@test.com' }).fetch()`.
- Association: `// User model pets: { collection: 'pet', via: 'owner' } // Pet model owner: { model: 'user' }`.

## NEVER DO THIS

1. **Never use without adapter installation.** `sails-disk`, `sails-mysql`, etc.
2. **Never skip connection configuration.** `config/connections.js`.
3. **Never ignore lifecycle callbacks.** Use for validation, transformation.
4. **Never mix Waterline with raw queries.** Use `.query()` carefully.
5. **Never forget `.fetch()` on creates/updates.** Returns record.
6. **Never use `.exec()` without callback.** Use async/await.
7. **Never skip `migrate` setting.** `alter`, `drop`, `safe`.

## Testing

- Test with `sails-disk` for unit tests.
- Test lifecycle callbacks.
- Test associations populate correctly.

