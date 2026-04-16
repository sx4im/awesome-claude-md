# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify with Mongoose
- Mongoose 8.x
- MongoDB 7+
- Schema-based models
- Validation hooks

## Project Structure
```
src/
├── models/
│   └── User.ts                 // Mongoose schemas
├── routes/
│   └── users.ts
├── plugins/
│   └── db.ts                   // Database connection
└── app.ts
```

## Architecture Rules

- **Schema definition.** Define structure, validation, hooks.
- **Model creation.** `mongoose.model()` creates queryable models.
- **Plugin pattern.** Fastify plugin for database connection.
- **TypeScript integration.** `@typegoose/typegoose` or interfaces.

## Coding Conventions

- Schema: `const userSchema = new mongoose.Schema({ name: { type: String, required: true }, email: { type: String, unique: true } }, { timestamps: true })`.
- Model: `const User = mongoose.model('User', userSchema)`.
- Plugin: `export default fp(async (fastify) => { await mongoose.connect(process.env.MONGO_URI); fastify.addHook('onClose', async () => { await mongoose.disconnect() }) })`.
- Query: `const users = await User.find().select('name email').lean()`.

## NEVER DO THIS

1. **Never skip schema validation.** Define `required`, `minlength`, etc.
2. **Never use callbacks.** Mongoose supports promises—use async/await.
3. **Never forget connection error handling.** `mongoose.connect().catch()`.
4. **Never use `.exec()` without need.** Only for query building.
5. **Never ignore the `lean()` option.** Use for read-only performance.
6. **Never skip index creation.** `schema.index({ email: 1 })` for queries.
7. **Never use `new ObjectId()` directly.** Use `new mongoose.Types.ObjectId()`.

## Testing

- Test with `mongodb-memory-server`.
- Test schema validation.
- Test hooks (pre/post save).

