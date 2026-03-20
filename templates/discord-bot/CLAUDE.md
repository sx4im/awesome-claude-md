# [PROJECT NAME] - Discord Bot

## Tech Stack

- discord.js v14 with TypeScript (strict mode)
- Node.js 20+ runtime
- Slash commands (application commands) exclusively
- [PRISMA/DRIZZLE] for persistent data storage
- [REDIS] for caching and rate limiting (if applicable)
- `discord-api-types` for raw API types
- `tsup` or `esbuild` for building

## Project Structure

```
src/
├── index.ts                   # Client initialization, login, event loader
├── deploy-commands.ts         # Script to register slash commands with Discord API
├── commands/                  # Slash command definitions and handlers
│   ├── ping.ts                # /ping command
│   ├── moderate/              # /moderate ban, /moderate kick, /moderate warn
│   │   ├── ban.ts
│   │   ├── kick.ts
│   │   └── index.ts           # Subcommand group registration
│   └── utility/
│       └── serverinfo.ts      # /serverinfo command
├── events/                    # Discord event handlers
│   ├── ready.ts               # Bot startup, status setting
│   ├── interactionCreate.ts   # Command routing + button/modal handling
│   ├── guildMemberAdd.ts      # Welcome messages, auto-roles
│   └── messageCreate.ts       # Message-based features (automod, logging)
├── components/                # Message component handlers
│   ├── buttons/               # Button click handlers (confirmBan.ts)
│   ├── selects/               # Select menu handlers (roleSelect.ts)
│   └── modals/                # Modal submit handlers (reportModal.ts)
├── embeds/                    # Embed builder factories (errorEmbed, successEmbed)
├── services/                  # Business logic and database operations
│   ├── moderation.service.ts
│   └── leveling.service.ts
├── guards/                    # Permission and precondition checks
│   ├── requirePermission.ts
│   └── requireRole.ts
├── types/                     # Extended types, augmented Client, command interfaces
│   └── index.ts
└── utils/
    ├── logger.ts              # Structured logging
    └── constants.ts           # Guild IDs, channel IDs, color hex codes
```

## Architecture Rules

- **Slash commands only.** No message-based command parsing (`!command`). Discord's API requires application commands for bots in 100+ guilds. Define commands with `SlashCommandBuilder`, register them with `deploy-commands.ts`, handle them in `interactionCreate`.
- **Command files export a standard interface.** Each command exports `{ data: SlashCommandBuilder, execute: (interaction: ChatInputCommandInteraction) => Promise<void> }`. The event handler in `interactionCreate.ts` loads commands into a `Collection<string, Command>` and routes by `interaction.commandName`.
- **Interactions must be acknowledged within 3 seconds.** Call `interaction.reply()` or `interaction.deferReply()` immediately. If your command does async work (DB query, API call), defer first, then `interaction.editReply()` with results. Unacknowledged interactions fail silently after 3 seconds.
- **Embeds over plain text.** Use `EmbedBuilder` for all structured responses. Set color, title, description, fields, footer, and timestamp consistently. Create factory functions in `embeds/` so every embed follows the same visual style.
- **Component handlers are separate from commands.** When a command creates a button, the button click is handled by a separate handler in `components/buttons/`. Use `customId` prefixes for routing: `customId: 'ban-confirm-${userId}'`. Parse the ID in the handler to extract context.

## Coding Conventions

- All interactions are typed: `ChatInputCommandInteraction` for slash commands, `ButtonInteraction` for buttons, `ModalSubmitInteraction` for modals. Never use the base `Interaction` type and cast -- use type guards: `interaction.isChatInputCommand()`.
- Guild-specific data (settings, levels, warnings) is always scoped by `interaction.guildId`. Never assume a single-guild deployment. Always include `guildId` in database queries.
- Permissions are checked with guards: `if (!interaction.memberPermissions?.has(PermissionFlagsBits.BanMembers))`. Create reusable guard functions in `guards/` that reply with a permission error and return `false`.
- Use `codeBlock()`, `bold()`, `italic()`, `userMention()` from `discord.js` formatters. Never write raw Markdown manually -- the formatters handle edge cases and escaping.
- Ephemeral replies for sensitive actions: `interaction.reply({ content: '...', ephemeral: true })`. Ban confirmations, error messages, and admin-only data should not be visible to the whole channel.

## Library Preferences

- **Framework:** discord.js v14. Not Eris (less maintained, smaller ecosystem). Not discord-api-types directly (too low-level, no client utilities).
- **Command registration:** discord.js `REST` + `Routes.applicationCommands()`. Not the old `client.application.commands.set()` -- the REST approach is explicit and works in deploy scripts without running the full bot.
- **Database:** Prisma. Not raw SQL. Not Sequelize (weaker TypeScript support). Models for guilds, users, warnings, config.
- **Logging:** pino. Not `console.log`. Structured JSON logs are searchable in production. Include `guildId`, `userId`, `commandName` in every log entry.
- **Hosting:** Process manager: `pm2` or Docker. Not `node index.js` in a screen session. The bot must auto-restart on crashes.

## File Naming

- Commands: `kebab-case.ts` -> `server-info.ts`, `role-assign.ts`
- Events: `camelCase.ts` matching the Discord event -> `interactionCreate.ts`, `guildMemberAdd.ts`
- Components: `camelCase.ts` -> `confirmBan.ts`, `roleSelect.ts`
- Embeds: `camelCase.ts` -> `errorEmbed.ts`, `userInfoEmbed.ts`
- Services: `kebab-case.service.ts` -> `moderation.service.ts`

## NEVER DO THIS

1. **Never use message content for commands.** The `MESSAGE_CONTENT` intent is privileged and deprecated for command parsing. Use slash commands exclusively. Message content intent is only for features that genuinely need to read messages (automod, logging).
2. **Never ignore interaction acknowledgment deadlines.** If you don't `reply()` or `deferReply()` within 3 seconds, the interaction token expires. The user sees "This interaction failed" and you cannot respond. Always defer before any async work.
3. **Never hardcode guild/channel/role IDs in command logic.** Store them in configuration (database or env vars). Hardcoded IDs break when the bot joins other servers. The only exception is a single-guild private bot.
4. **Never use `client.on('message')` for commands.** This is the v12/v13 pattern. v14 uses `client.on(Events.InteractionCreate)`. Message-based commands don't support autocomplete, permissions, or argument validation.
5. **Never send unescaped user input in embeds.** User-provided text in embed fields can contain `@everyone`, `@here`, or role mentions. Use `escapeMarkdown()` from discord.js or `allowedMentions: { parse: [] }` to prevent mention injection.
6. **Never register commands on every bot startup.** Command registration is a one-time or deploy-time operation. The `deploy-commands.ts` script runs separately. Registering on startup hits rate limits when the bot restarts frequently.
7. **Never store the bot token in source code.** Use environment variables: `process.env.DISCORD_TOKEN`. The token grants full control of the bot account. If it leaks, regenerate it immediately in the Discord Developer Portal.

## Testing

- Unit test command `execute` functions by mocking `ChatInputCommandInteraction`. Mock `interaction.reply`, `interaction.deferReply`, `interaction.editReply`, and assert they were called with expected embeds.
- Test guards by passing interactions with various permission sets and verifying they allow or deny correctly.
- Test embeds by calling factory functions and asserting on `EmbedBuilder.toJSON()`: check title, color, field count.
- Test services (database logic) independently with a test database. These tests should not import discord.js.
- Integration test with a dedicated test guild and test bot token. Guild-specific command registration is instant, unlike global which takes up to an hour.
- Never run tests against a production bot token or production guild.
