# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Cloud & Serverless)

### Release Discipline
- Design for cold starts, retries, and at-least-once execution semantics.
- Guard IAM permissions and network exposure with least privilege.
- Treat infrastructure config drift as deployment risk.

### Merge/Release Gates
- Deployment plan validated with environment-specific config checks.
- Critical alarms/observability are in place for changed services.
- Rollback path tested or documented before release.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Orchestration: AWS Step Functions (Standard Workflows for long-running, Express for high-volume)
- IaC: AWS CDK v2 (TypeScript)
- Compute: AWS Lambda (Node.js 20) for task states
- Language: TypeScript 5.x (strict mode)
- Database: DynamoDB for workflow state and results
- Messaging: SQS for dead-letter queues, SNS for notifications
- Monitoring: CloudWatch Logs, X-Ray for distributed tracing
- Package Manager: pnpm
- Testing: Jest with CDK assertions and Step Functions Local
- Linting: ESLint with @typescript-eslint

## Project Structure

```
lib/
  stacks/
    pipeline-stack.ts   # CDK stack defining Step Functions state machine
    lambda-stack.ts     # CDK stack for Lambda functions
    shared-stack.ts     # Shared resources (DynamoDB tables, SQS queues)
  constructs/
    workflow.ts         # Custom CDK construct for the state machine
    taskLambda.ts       # Reusable construct for Lambda task functions
src/
  handlers/
    validate.ts         # Validation step Lambda handler
    process.ts          # Core processing step Lambda handler
    transform.ts        # Data transformation step Lambda handler
    notify.ts           # Notification step Lambda handler
    cleanup.ts          # Cleanup/finalization step Lambda handler
  services/
    dynamodb.ts         # DynamoDB read/write helpers
    s3.ts               # S3 read/write for large payloads
  types/
    workflow.ts         # State machine input/output type definitions
    events.ts           # Step function event payload types
  utils/
    payload.ts          # Payload size checker and S3 offloading
bin/
  app.ts                # CDK app entry point
statemachine/
  definition.asl.json   # ASL definition (if not using CDK-native)
cdk.json                # CDK configuration
```

## Architecture Rules

- Define state machines using CDK's `sfn.Chain` and typed state classes, not raw ASL JSON, unless the workflow is imported.
- Step Functions has a 256KB payload limit per state. For larger data, store in S3 and pass the S3 key through the state machine.
- Use `ResultPath` to merge task output with existing state instead of replacing it. Default `$.result` convention.
- Every state machine must have a dead-letter queue (SQS) configured on the `onFailed` callback for failed executions.
- Lambda tasks should be idempotent -- Step Functions may retry on transient failures.
- Use `Map` state for parallel iteration over arrays. Set `maxConcurrency` to control throttling.
- Standard Workflows for processes up to 1 year. Express Workflows for sub-5-minute, high-throughput use cases.
- Task timeouts: set `TimeoutSeconds` on every Task state. Default Lambda timeout to 60 seconds.

## Coding Conventions

- CDK construct pattern: each state machine is a custom Construct in `lib/constructs/`.
- Define states using CDK classes: `new tasks.LambdaInvoke(this, 'Validate', { lambdaFunction: validateFn, resultPath: '$.validation' })`.
- Use `sfn.Choice` for branching: `.when(sfn.Condition.stringEquals('$.validation.status', 'valid'), processStep)`.
- Lambda handler signature: `async (event: WorkflowEvent, context: Context): Promise<StepOutput>`.
- Each Lambda handler receives only the data it needs via `InputPath` or `Parameters` -- never pass the entire state.
- Use `sfn.Wait` with `sfn.WaitTime.duration(Duration.seconds(30))` for polling patterns.
- Error handling: use `addCatch()` on task states to route to error-handling states.

## Library Preferences

- IaC: AWS CDK v2 (never CloudFormation YAML directly)
- State machine tasks: aws-cdk-lib/aws-stepfunctions-tasks
- Lambda runtime: aws-cdk-lib/aws-lambda-nodejs (esbuild bundling)
- DynamoDB: @aws-sdk/lib-dynamodb (v3 document client)
- Observability: Powertools for AWS Lambda (logger, tracer)
- Testing: aws-cdk-lib/assertions for CDK, @aws-sdk/client-mock for Lambda handlers
- Local testing: Step Functions Local (Docker image)

## File Naming

- CDK stacks: PascalCase ending in `-stack.ts` (`pipeline-stack.ts`)
- CDK constructs: camelCase (`workflow.ts`, `taskLambda.ts`)
- Lambda handlers: camelCase by step name (`validate.ts`, `process.ts`, `notify.ts`)
- Type files: camelCase by domain (`workflow.ts`, `events.ts`)
- State machine ASL: `definition.asl.json` in `statemachine/` directory

## NEVER DO THIS

1. Never pass payloads larger than 256KB between states -- offload to S3 and pass the object key instead.
2. Never use `"ResultPath": null` unless you intentionally want to discard the task output.
3. Never omit `TimeoutSeconds` on Task states -- a stuck Lambda will cause the execution to hang until the 1-year limit.
4. Never use Express Workflows for executions longer than 5 minutes -- they will be terminated.
5. Never hardcode ARNs in state machine definitions -- use CDK references (`fn.functionArn`) for cross-stack resolution.
6. Never skip idempotency in Lambda tasks -- Step Functions retries mean a handler may execute multiple times for the same input.
7. Never use `sfn.Pass` states in production for data transformation that could fail -- use Lambda tasks with proper error handling.

## Testing

- Unit test CDK stacks using `aws-cdk-lib/assertions`: `Template.fromStack(stack).hasResourceProperties('AWS::StepFunctions::StateMachine', { ... })`.
- Verify state machine definition structure: assert that required states exist and transitions are correct.
- Unit test Lambda handlers independently by mocking DynamoDB and S3 calls with `@aws-sdk/client-mock`.
- Integration test the full state machine using Step Functions Local Docker image (`amazon/aws-stepfunctions-local`).
- Test error paths by injecting failures: verify that `Catch` states route correctly and DLQ receives failed events.
- Test Map state with various array sizes including empty arrays.
- Use CDK snapshot tests (`Template.fromStack(stack).toJSON()`) to detect unintended infrastructure changes.
