# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- AWS Cloud Development Kit (AWS CDK) v2
- TypeScript (Strict mode)
- AWS Services deployed via CloudFormation
- Jest (Snapshot and Assertion testing)
- Esbuild (for fast bundling of Lambda functions)

## Project Structure

```
.
├── bin/
│   └── app.ts                   # Entry point, instantiates the App and Stacks
├── lib/
│   ├── stacks/                  # Top-level Stack definitions
│   │   ├── network-stack.ts     # VPC, Subnets, Security Groups
│   │   ├── database-stack.ts    # RDS, DynamoDB
│   │   └── compute-stack.ts     # ECS, Lambda, API Gateway
│   └── constructs/              # Reusable L3 constructs
│       ├── secure-bucket.ts     # Standardized S3 with explicit block public access
│       └── api-gateway-lambda.ts# Standardized REST endpoint
├── src/                         # Application runtime code (Lambda, etc.)
│   └── functions/
│       ├── process-sqs/
│       │   └── index.ts
│       └── api-handler/
│           └── index.ts
├── test/
│   ├── snapshot.test.ts         # Generates CloudFormation assertion snapshot
│   └── constructs/              # Unit tests for specific L3 constructs
├── cdk.json                     # CDK configurations and feature flags
├── tsconfig.json
└── package.json
```

## Architecture Rules

- **Use L3 Constructs.** Group L2 constructs (like `s3.Bucket`, `lambda.Function`) into modular, reusable L3 constructs that enforce organizational opinions (encryption, logging, retention). Never drop naked L1/L2 constructs in a main Stack file.
- **Separate Stacks by lifecycle.** Deployments should group resources by change velocity. Put VPCs and Databases in a `StatefulStack` (rarely changes). Put API Gateways and Lambdas in a `StatelessStack` (frequently changes).
- **Pass resources via Props, not exports.** If the Compute Stack needs the VPC ID, pass the `IVpc` reference into the `ComputeStackProps` from `bin/app.ts`. Never use CloudFormation `CfnOutput` / `ExportValue` cross-stack references, as they rigidly lock stacks together and make deletion painfully difficult.
- **Bundle code with NodejsFunction.** Use `aws-lambda-nodejs.NodejsFunction`. It utilizes `esbuild` locally (or via Docker) to seamlessly compile your TypeScript Lambda handlers alongside infrastructure synthesis without external webpack pipelines.
- **Least Privilege IAM.** explicitly `grant` permissions between constructs. `myBucket.grantReadWrite(myLambda)` automatically scopes the exact IAM policy required. Never manually write wildcard `iam.PolicyStatement` JSON unless integrating custom non-CDK boundaries.

## Coding Conventions

- **Typescript Strictness.** Use Strict Typescript. Define interfaces explicitly for your custom Construct props (`interface SecureBucketProps extends s3.BucketProps`).
- **Resource Naming.** Do not hardcode `bucketName` or `functionName` attributes. Let CloudFormation auto-generate physical IDs based on the logical construct tree. Hardcoding names prohibits deploying the same stack twice in one account.
- **Token resolution awareness.** Values like `vpc.vpcId` are Tokens (e.g. `${Token[TOKEN.123]}`) at synthesis time, not actual strings. Do not try to run string manipulation, regex, or `if (vpcId == "vpc-123")` on CDK properties during synthesis.
- **Tagging.** Apply tags at the Stack level or App level so they cascade down to all resources. `Tags.of(app).add('Environment', 'Production')`.

## Library Preferences

- **Testing:** `aws-cdk-lib/assertions` (Built into v2). Use it for `Template.fromStack(stack).hasResourceProperties(...)`.
- **Lambda compute:** `aws-lambda-nodejs`.
- **Formatting/Linting:** Prettier + ESLint to keep synthesis code uniform.
- **CI/CD:** Use CDK Pipelines for cross-account deployments, or standard GitHub Actions synthesizing and calling `cdk deploy`.

## NEVER DO THIS

1. **Never hardcode ARNs or IDs across environments.** Do not write `import { Bucket } from 'aws-cdk-lib/aws-s3'; Bucket.fromBucketArn(this, 'Bucket', 'arn:aws:s3:::my-prod-bucket')`. Look them up via SSM Parameter Store, or pass them in dynamically using CDK contexts (`cdk.json`).
2. **Never commit raw credentials to synthesis.** The CDK CLI utilizes standard AWS profiles (`~/.aws/credentials`). The synthesis code should NEVER read explicit `process.env.AWS_SECRET_ACCESS_KEY`.
3. **Never apply generic RemovalPolicies to stateful logic.** Amazon natively retains databases on stack deletion to prevent catastrophic data loss. Do not carelessly set `removalPolicy: RemovalPolicy.DESTROY` on DynamoDB arrays unless explicitly designing temporary test environments.
4. **Never create cross-stack `CfnOutput` exports randomly.** If an API Stack references a Database Stack via strong Cfn linkages, you cannot tear down or drastically modify the Database stack without tearing down the API stack first. Dependency inversions are preferred.
5. **Never write fat Stacks.** A 3,000 line `InfrastructureStack.ts` is unmaintainable. Break architecture down into logical boundaries.
6. **Never use the default `cdk.json` parameters in production without review.** Review the feature flags in `cdk.json`. They dictate critical behaviors like default bucket encryption and IAM structural changes.
7. **Never assume Lambda environments have node_modules.** Using `NodejsFunction` utilizes esbuild to bundle code. If you rely on native binaries (Prisma, sharp), you must configure `bundling.nodeModules` appropriately or use layer Docker bundling.

## Testing

- **Fine-Grained Assertions.** Write tests verifying that specific resources are created with exact parameters. (e.g., Assert the S3 bucket has `BucketEncryption.S3_MANAGED`).
- **Snapshot Testing.** `expect(Template.fromStack(stack).toJSON()).toMatchSnapshot()`. This captures the exact CloudFormation JSON output and fails CI if any construct change accidentally modified the underlying infrastructure graph. It forces you to manually approve the snapshot update if changes are intentional.
