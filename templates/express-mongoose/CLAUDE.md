# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with Mongoose
- Mongoose 8.x
- MongoDB native driver
- Schema validation
- Middleware

## Project Structure
```
src/
├── models/
│   ├── User.ts                 // Mongoose models
│   └── index.ts                // Model exports
├── controllers/
└── routes/
```

## Architecture Rules

- **Schema-first.** Define structure, validation, middleware.
- **Models compile from schemas.** `mongoose.model()`.
- **Instance methods.** Add methods to documents.
- **Static methods.** Add methods to model.

## Coding Conventions

- Schema: `const userSchema = new Schema({ name: { type: String, required: true }, email: { type: String, required: true, unique: true }, age: Number }, { timestamps: true })`.
- Model: `const User = mongoose.model('User', userSchema)`.
- Instance method: `userSchema.methods.getFullName = function() { return this.firstName + ' ' + this.lastName }`.
- Static method: `userSchema.statics.findByEmail = function(email) { return this.findOne({ email }) }`.
- Query: `const user = await User.findByEmail('test@example.com')`.

## NEVER DO THIS

1. **Never use arrow functions in methods.** Lose `this` context.
2. **Never forget to handle unique constraint errors.** `MongoServerError` with code 11000.
3. **Never skip schema validation.** Define `required`, `min`, `max`, etc.
4. **Never use `save()` for updates without checking.** Can overwrite.
5. **Never ignore the `select` option.** `User.find().select('-password')`.
6. **Never forget `await` on Mongoose calls.** All async.
7. **Never use callbacks.** Promises/async-await preferred.

## Testing

- Test with `mongodb-memory-server`.
- Test schema validation.
- Test pre/post hooks.

