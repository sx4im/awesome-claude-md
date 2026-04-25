# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Brigade**: Kubernetes-native CI/CD (v2.x)
- **JavaScript/TypeScript**: Scripting language
- **Kubernetes**: Container orchestration
- **Docker**: Container images
- **Helm**: Brigade installation
- **GitHub/GitLab**: SCM integration

## Project Structure

```
brigade-project/
├── brigade.js                  # Brigade script
├── brigade.json                # Project config
├── .brigade/                   # Additional scripts
│   └── helpers.js
├── Dockerfile                  # Custom worker image
└── scripts/                    # Helper scripts
    └── test.sh
```

## Architecture Rules

- **Event-driven.** Trigger on GitHub webhooks, cron, manual. Event handlers in `brigade.js`.
- **Job-based.** Jobs run in pods. `Job` object with containers, tasks.
- **Shared storage.** Cache and scratch volumes for data between jobs.
- **Secret management.** Project-level secrets. Encrypted in Kubernetes.
- **Custom images.** Use custom worker images for specific toolchains.

## Coding Conventions

- **Event handling.** `events.on("push", async (e, p) => { ... })`. Git push triggers.
- **Job definition.** `let job = new Job("test", "node:20")`. Name and image.
- **Task specification.** `job.tasks = ["npm install", "npm test"]`. Commands to run.
- **Secret access.** `job.env = { MY_SECRET: p.secrets.MY_SECRET }`. Project secrets.
- **Concurrent jobs.** `Group` for parallel jobs. `ConcurrentGroup` for fan-out.
- **Storage.** `job.cache = { enabled: true }`. Persistent between builds.

## NEVER DO THIS

1. **Never hardcode secrets.** Use Brigade secrets. Kubernetes secret backend.
2. **Never use :latest images.** Pin to specific tags. Reproducible builds.
3. **Never skip resource limits.** Jobs without limits can exhaust cluster.
4. **Never ignore job logs.** `brigade logs` for debugging. Check failures.
5. **Never use privileged containers.** Breaks security. Rootless where possible.
6. **Never forget about storage cleanup.** Cache grows indefinitely. TTL or manual cleanup.
7. **Never skip event filtering.** Filter events carefully. Don't trigger on every commit if not needed.

## Testing

- **Event testing.** Trigger events manually. Verify handlers execute.
- **Job testing.** Individual jobs in isolation. Container commands work.
- **Integration testing.** Full pipeline on test repo. End-to-end flow.
- **Secret testing.** Secrets available in jobs. Not exposed in logs.
- **Concurrent testing.** Parallel jobs don't conflict. Race conditions handled.

## Claude Code Integration

- Use `@brigade.js` for Brigade script patterns
- Reference `@.brigade/` for helper script patterns
- Apply Brigade CI from architecture rules
- Validate against Brigade best practices in NEVER DO THIS
