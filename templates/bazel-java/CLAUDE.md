# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Bazel 7.x with bzlmod for external dependency management
- Java 21 LTS with rules_java for compilation and packaging
- Kotlin 1.9+ with rules_kotlin for mixed Java/Kotlin projects
- rules_jvm_external (maven_install) for Maven dependency resolution
- Remote caching via bazel-remote or Google Cloud Storage
- Remote execution via BuildBuddy or Buildbarn
- JUnit 5 for unit testing, Testcontainers for integration tests
- Google Java Format and ktlint for code formatting

## Project Structure

```
.
├── MODULE.bazel
├── MODULE.bazel.lock
├── .bazelrc
├── .bazelversion
├── BUILD.bazel
├── tools/
│   ├── BUILD.bazel
│   └── format/
│       └── BUILD.bazel
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── app/
│   │   │       │   └── BUILD.bazel
│   │   │       ├── domain/
│   │   │       │   └── BUILD.bazel
│   │   │       └── infra/
│   │   │           └── BUILD.bazel
│   │   └── kotlin/
│   │       └── com/example/
│   │           └── BUILD.bazel
│   └── test/
│       ├── java/
│       │   └── com/example/
│       │       └── BUILD.bazel
│       └── kotlin/
│           └── com/example/
│               └── BUILD.bazel
├── libs/
│   ├── common/
│   │   └── BUILD.bazel
│   └── proto/
│       └── BUILD.bazel
└── deploy/
    └── BUILD.bazel
```

## Architecture Rules

- Use bzlmod (MODULE.bazel) for all external dependencies; WORKSPACE is deprecated and must not be used
- Every directory containing source files must have its own BUILD.bazel with fine-grained targets
- Library targets must have visibility restricted to the packages that depend on them; never use //visibility:public for internal libraries
- One java_library per logical module; avoid monolithic targets that compile the entire source tree
- Remote caching must be enabled in .bazelrc with --remote_cache for all CI builds
- All third-party Maven dependencies must be pinned with exact versions in MODULE.bazel using maven.install
- Use java_binary for application entry points and java_library for shared code
- Proto files must use rules_proto with java_proto_library for generated code

## Coding Conventions

- BUILD.bazel target names match the directory name or the primary class for single-purpose targets
- Dependencies must be listed explicitly; never use glob() for srcs in production code, only in test targets
- Use exports sparingly and only for re-exporting transitive APIs that are part of the public contract
- Tags for test targets: small (< 1min, no I/O), medium (< 5min, localhost only), large (< 15min, external services)
- All java_library targets must specify a deps list; implicit deps via the classpath are not allowed
- Use Label() for all cross-package references; never use relative paths across package boundaries
- Runtime deps (JDBC drivers, SPI implementations) go in runtime_deps, not deps

## Library Preferences

- Use rules_jvm_external with maven.install for Maven Central dependencies
- Use Dagger (the DI framework) for dependency injection; configure with java_plugin for annotation processing
- Use jOOQ for SQL, Jackson for JSON serialization, Guava for utilities
- Use rules_oci for container image building instead of rules_docker (deprecated)
- Use rules_pkg for creating deployment archives (tar, deb, rpm)
- Use aspect-build/rules_lint for enforcing Checkstyle, Error Prone, and ktlint

## File Naming

- Build files: BUILD.bazel (never BUILD without extension)
- Module file: MODULE.bazel at repository root
- Bazel config: .bazelrc at repository root, .bazelrc.user for local overrides (gitignored)
- Version pinning: .bazelversion containing the exact Bazel version
- Macro files: {purpose}.bzl in the tools/ directory
- Extension files: extensions.bzl for custom module extensions

## NEVER DO THIS

1. Never use glob(["**/*.java"]) for production srcs; it breaks remote caching and makes targets non-hermetic
2. Never add deps that are only needed at test time to a java_library target; put them in the test target's deps
3. Never set --jobs to unlimited on CI; use a fixed value matching available cores to prevent OOM
4. Never use local_repository for dependencies that should come from a registry; it breaks reproducibility
5. Never skip the build --remote_upload_local_results flag in CI; local results must be shared to the cache
6. Never put generated code in version control; let Bazel generate it from proto files or annotation processors

## Testing

- Run bazel test //... to execute all tests; CI must pass this command with zero failures
- Unit tests use JUnit 5 with java_test targets tagged as size = "small"
- Integration tests use Testcontainers and are tagged as size = "medium" with requires-docker
- Use bazel coverage //... --combined_report=lcov to generate coverage reports
- Test caching correctness: modify a file and verify only affected tests re-run with --test_output=summary
- Use bazel query to validate dependency graphs: bazel query 'deps(//src/main/java/...)' for dependency auditing
- Run buildifier to format all BUILD and .bzl files; fail CI on formatting violations
