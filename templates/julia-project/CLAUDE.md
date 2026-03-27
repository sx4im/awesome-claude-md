# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Julia 1.10+ with multi-threading and precompilation
- Package Manager: Pkg with Project.toml and Manifest.toml for reproducibility
- Build: No separate build step; Pkg.instantiate() and using for module loading
- Testing: Test stdlib with @testset and @test macros
- Documentation: Documenter.jl for generating HTML docs from docstrings
- Notebook: Pluto.jl for reactive notebooks, Jupyter via IJulia for exploratory work

## Project Structure

```
src/
  ProjectName.jl            # Main module definition, exports, includes
  types.jl                   # Struct definitions with parametric types
  core.jl                    # Primary algorithms and dispatch methods
  io.jl                      # File I/O, data loading/saving functions
  preprocessing.jl           # Data cleaning, normalization pipelines
  analysis.jl                # Statistical analysis, model fitting
  plotting.jl                # Recipes and plot functions using Makie
  utils.jl                   # Helper functions, unit conversions
test/
  runtests.jl                # Test runner, includes all test files
  test_core.jl               # Unit tests for core algorithms
  test_io.jl                 # I/O round-trip tests with temp files
  test_analysis.jl           # Numerical accuracy tests with tolerances
notebooks/
  exploration.jl             # Pluto notebook for interactive analysis
docs/
  make.jl                    # Documenter.jl build script
  src/
    index.md                 # Documentation landing page
Project.toml                 # Package metadata and direct dependencies
Manifest.toml                # Locked dependency versions (committed)
```

## Architecture Rules

- Define abstract type hierarchies for domain concepts: `abstract type AbstractModel end` with concrete subtypes.
- Use multiple dispatch as the primary extension mechanism. Define methods on abstract types for shared behavior.
- All structs should be immutable by default. Use `mutable struct` only when in-place mutation provides measurable performance benefit.
- Separate pure computation from I/O: functions in `core.jl` and `analysis.jl` must not read files or print output.
- Use `@kwdef` for structs with many fields to enable keyword construction with defaults.
- Performance-critical inner loops must be type-stable. Run `@code_warntype` on hot paths during development.

## Coding Conventions

- Module names: PascalCase. Function names: snake_case. Type names: PascalCase. Constants: UPPER_SNAKE_CASE.
- Functions that modify arguments in-place must end with `!`: `normalize!(data)`, `fit!(model, X, y)`.
- First argument of mutating functions is the modified object. Non-mutating variant returns a new value.
- Use docstrings on all exported functions with the triple-quote format, including argument descriptions and examples.
- Prefer `eachindex(A)` and `axes(A, d)` over `1:length(A)` for array iteration to support OffsetArrays.
- Use `@views` macro on slicing operations in performance-critical code to avoid allocations.

## Library Preferences

- Linear algebra: LinearAlgebra stdlib for BLAS/LAPACK operations
- Data frames: DataFrames.jl with CSV.jl for tabular data
- Plotting: Makie.jl (CairoMakie for static, GLMakie for interactive, WGLMakie for web)
- Optimization: Optim.jl for nonlinear optimization, JuMP.jl for mathematical programming
- Statistics: StatsBase.jl for descriptive stats, Distributions.jl for probability distributions
- Serialization: JLD2.jl for Julia objects, Arrow.jl for interop with Python/R
- HTTP: HTTP.jl for web requests, Genie.jl if building a web application

## File Naming

- Source files: snake_case matching their conceptual content: `data_loader.jl`, `model_fitting.jl`.
- Main module file: PascalCase matching module name: `ProjectName.jl`.
- Test files: `test_<module>.jl` prefix in `test/` directory.
- Include files in module definition in dependency order.

## NEVER DO THIS

1. Never use untyped global variables in computation; annotate with `const` or pass as function arguments for type stability.
2. Never use `eval` or `@eval` in runtime code paths; it defeats compilation and causes world-age issues.
3. Never write `for i in 1:length(A)` when `eachindex(A)` works; it breaks for non-1-indexed arrays.
4. Never use `try/catch` for control flow; check conditions explicitly and return `nothing` or use `Maybe` patterns.
5. Never commit Manifest.toml changes from a different Julia version without testing all dependent packages.
6. Never define a method on a type you do not own for a function you do not own (type piracy). Wrap in a newtype.
7. Never use `Any` typed containers in hot loops; parameterize with concrete types or use function barriers.

## Testing

- Run tests: `julia --project=. -e 'using Pkg; Pkg.test()'` or `] test` in the REPL.
- Use `@testset` blocks to group related tests with descriptive labels.
- Use `@test a ≈ b atol=1e-8` for floating-point comparisons, never `==` on floats.
- Test type stability with `@inferred f(args...)` in test suites for critical functions.
- Use `mktempdir()` for filesystem tests; it auto-cleans on scope exit.
- Benchmark regressions: use BenchmarkTools.jl `@benchmark` and track results in CI with PkgBenchmark.jl.
