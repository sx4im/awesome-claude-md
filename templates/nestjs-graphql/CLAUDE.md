# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- NestJS GraphQL
- @nestjs/graphql
- Apollo Server
- Code-first schema
- TypeScript

## Project Structure
```
src/
├── app.module.ts
├── users/
│   ├── users.module.ts
│   ├── users.resolver.ts       // GraphQL resolver
│   ├── users.service.ts
│   └── dto/
│       ├── create-user.input.ts
│       └── user.entity.ts
└── main.ts
```

## Architecture Rules

- **Code-first.** Generate schema from TypeScript decorators.
- **Resolvers.** Handle GraphQL operations.
- **Services.** Business logic, data fetching.
- **DTOs/Entities.** Define GraphQL types.

## Coding Conventions

- Resolver: `@Resolver(() => User) export class UsersResolver { constructor(private usersService: UsersService) {} @Query(() => [User]) async users(): Promise<User[]> { return this.usersService.findAll(); } }`.
- Mutation: `@Mutation(() => User) async createUser(@Args('createUserInput') createUserInput: CreateUserInput) { ... }`.
- Type: `@ObjectType() export class User { @Field(() => Int) id: number; @Field() name: string; }`.
- Input: `@InputType() export class CreateUserInput { @Field() name: string; }`.

## NEVER DO THIS

1. **Never mix REST and GraphQL carelessly.** Separate concerns.
2. **Never forget the `@Field()` decorator.** Required for schema generation.
3. **Never skip resolver authorization.** Use guards for protected queries.
4. **Never ignore DataLoader.** Essential for N+1 problem.
5. **Never use `@Resolver()` without type.** `@Resolver(() => User)` for relations.
6. **Never forget `playground` config.** Disable in production.
7. **Never skip introspection config.** Control in production.

## Testing

- Test resolvers with `graphql` helper.
- Test schema generation.
- Test with Apollo Studio.

