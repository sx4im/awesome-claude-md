# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: R 4.3+ with tidyverse ecosystem
- Framework: Shiny 1.8+ with golem package structure for production apps
- UI: bslib 0.6+ for Bootstrap 5 theming, shiny.semantic or shinydashboard for layouts
- Build: golem framework with dev scripts, renv for dependency lockfiles
- Testing: testthat 3.x with shinytest2 for end-to-end UI tests
- Database: DBI with pool for connection pooling, dbplyr for dplyr-to-SQL translation
- Deployment: Posit Connect, ShinyProxy with Docker, or shinyapps.io

## Project Structure

```
R/
  app_config.R              # golem config, get_golem_config()
  app_server.R              # Main server function, calls module servers
  app_ui.R                  # Main UI function, assembles module UIs
  mod_data_upload.R         # Module: file upload with validation
  mod_data_table.R          # Module: interactive DT table display
  mod_visualization.R       # Module: plot output with parameter controls
  mod_export.R              # Module: report generation and download
  fct_data_processing.R     # Business logic: data cleaning pipelines
  fct_plotting.R            # Plot builders returning ggplot objects
  fct_validation.R          # Input validation helpers
  utils_helpers.R           # Small utility functions, formatters
  utils_db.R                # Database connection and query functions
inst/
  app/
    www/
      custom.css            # Custom CSS overrides for bslib theme
      logo.png              # App branding assets
  golem-config.yml          # App configuration per environment
dev/
  01_start.R                # golem project setup script
  02_dev.R                  # Development helpers, add modules
  03_deploy.R               # Deployment checklist and scripts
  run_dev.R                 # Quick launcher for local development
tests/
  testthat/
    test-fct_data_processing.R  # Unit tests for data functions
    test-mod_visualization.R    # shinytest2 module tests
    test-app.R                  # Full app integration test
  testthat.R                # Test runner configuration
DESCRIPTION                 # Package metadata, dependencies
NAMESPACE                   # Exported functions via roxygen2
renv.lock                   # Locked dependency versions
```

## Architecture Rules

- Every feature is a Shiny module with `mod_<name>_ui` and `mod_<name>_server` functions in one file.
- Business logic lives in `fct_*.R` files as pure functions that take data and return data. No Shiny reactivity in fct files.
- Modules communicate via returned reactive values, never by accessing parent session inputs directly.
- Use `reactiveVal()` for single values and `reactiveValues()` for related state within a module.
- Wrap expensive computations in `bindCache()` with appropriate cache keys to avoid redundant recalculation.
- All database queries go through `utils_db.R`. Modules never construct SQL or manage connections directly.

## Coding Conventions

- Function names: snake_case. Module functions: `mod_<name>_ui()`, `mod_<name>_server()`.
- Use roxygen2 `#'` comments on all exported functions with `@param`, `@return`, `@examples`.
- Pipe with `|>` (base R pipe, R 4.1+). Avoid magrittr `%>%` in new code.
- Use tidyverse verbs for data manipulation: `dplyr::mutate()`, `tidyr::pivot_longer()`, `purrr::map()`.
- Prefix external package functions with `pkg::fn()` instead of `library()` calls in package code.
- Reactive expressions: name them descriptively like `filtered_data <- reactive({...})`, not `r1`.

## Library Preferences

- Data manipulation: dplyr, tidyr, purrr, stringr, lubridate, forcats
- Plotting: ggplot2 with custom theme function, plotly for interactive via `ggplotly()`
- Tables: DT package for interactive DataTables, gt for static publication tables
- UI components: bslib for theming, bsicons for icons, shinyWidgets for enhanced inputs
- File handling: readr for CSV, readxl for Excel, arrow for Parquet
- Reporting: rmarkdown and quarto for parameterized report generation
- Validation: shinyvalidate for form input validation in modules

## File Naming

- Module files: `mod_<feature_name>.R` with both UI and server in one file.
- Business logic: `fct_<domain>.R` for functions that implement features.
- Utilities: `utils_<purpose>.R` for small reusable helpers.
- Tests: `test-<matching_source_file>.R` in `tests/testthat/`.

## NEVER DO THIS

1. Never use `<<-` (global assignment) to pass data between modules; return reactives and pass them as arguments.
2. Never put `library()` calls in R package code; use `@importFrom` or `pkg::fn()` namespacing.
3. Never use `observe()` when `observeEvent()` with an explicit trigger is appropriate; unscoped observers cause hard-to-debug reactivity loops.
4. Never read files with hardcoded absolute paths; use `system.file()` for package data or `golem::app_sys()` for app resources.
5. Never store large datasets in `reactiveValues`; use database queries with pagination or server-side filtering.
6. Never use `req(FALSE)` to silently stop execution without user feedback; show a notification or validation message.

## Testing

- Run tests: `devtools::test()` or `testthat::test_local()` from project root.
- Unit test `fct_*.R` functions with regular testthat: `expect_equal()`, `expect_s3_class()`, `expect_error()`.
- Module tests use `shiny::testServer(mod_name_server, {session$setInputs(x = 1); expect_equal(output$plot, ...)})`.
- End-to-end tests with shinytest2: `AppDriver$new()`, set inputs, expect screenshots or output values.
- Snapshot tests for ggplot outputs: `vdiffr::expect_doppelganger("plot name", my_plot)`.
- CI pipeline: `R CMD check --as-cran` plus `devtools::test()` with code coverage via covr.
