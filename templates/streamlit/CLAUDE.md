# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- Streamlit 1.38+ as the app framework
- pandas 2.x for data manipulation
- Plotly Express and Plotly Graph Objects for interactive charts
- st-aggrid for advanced data tables
- streamlit-option-menu for sidebar navigation
- SQLAlchemy 2.x for database connections
- Poetry for dependency management

## Project Structure

```
app/
├── Home.py                  # Main entry point (multipage root)
├── pages/
│   ├── 1_Dashboard.py       # Primary dashboard view
│   ├── 2_Explorer.py        # Data exploration page
│   ├── 3_Settings.py        # User settings page
│   └── 4_About.py           # About and documentation
├── components/
│   ├── charts.py            # Reusable Plotly chart builders
│   ├── filters.py           # Sidebar filter widgets
│   ├── tables.py            # AgGrid table configurations
│   └── metrics.py           # KPI metric card builders
├── data/
│   ├── loader.py            # Data loading with @st.cache_data
│   ├── processor.py         # Data transformations (pure pandas)
│   └── queries.py           # SQL query strings and builders
├── utils/
│   ├── state.py             # Session state helpers and defaults
│   ├── auth.py              # Authentication wrapper
│   └── config.py            # App configuration constants
├── .streamlit/
│   └── config.toml          # Streamlit theme and server config
├── pyproject.toml
└── tests/
    ├── test_processor.py
    └── test_charts.py
```

## Architecture Rules

- Every page file must call `st.set_page_config()` as its very first Streamlit command.
- All expensive data loading must use `@st.cache_data` with explicit `ttl` parameter in seconds.
- Use `@st.cache_resource` only for database connections and ML models, never for DataFrames.
- Session state keys must be defined as constants in `utils/state.py` and initialized in a single `init_state()` function called at app start.
- All Plotly figures must be created through helper functions in `components/charts.py` that return `go.Figure` objects, never built inline in page files.
- Page files should contain only layout logic: columns, containers, and calls to component functions.

## Coding Conventions

- Use `st.columns()` for horizontal layouts; never nest more than two levels of columns.
- Always set `use_container_width=True` on `st.plotly_chart()` and `st.dataframe()`.
- Prefix session state keys with the page name: `dashboard_date_range`, `explorer_selected_cols`.
- Use `st.fragment` decorator for components that need independent rerun behavior.
- Format all numbers with `st.metric()` using `delta` and `delta_color` parameters.
- DataFrames displayed to users must have human-readable column names via `.rename(columns={})`.

## Library Preferences

- Plotly Express for simple charts; Plotly Graph Objects only when Express cannot achieve the layout.
- pandas for all tabular data; do not introduce polars or dask.
- st-aggrid for tables needing sorting, filtering, or row selection; plain `st.dataframe` otherwise.
- Use `st.query_params` for shareable URL state, not hidden session state.

## File Naming

- Page files: number prefix for ordering, snake_case name: `1_Dashboard.py`.
- Component files: lowercase snake_case noun describing the widget group.
- Test files mirror source: `components/charts.py` -> `tests/test_charts.py`.

## NEVER DO THIS

1. Never call `st.write()` with raw DataFrames in production pages; use `st.dataframe()` or `st.table()` with explicit column configuration.
2. Never mutate session state inside a callback and also outside it in the same rerun cycle; pick one location.
3. Never use `@st.cache_data` without a `ttl` parameter; stale data causes silent bugs.
4. Never put business logic inside page files; extract it into `data/processor.py` as pure functions.
5. Never use `time.sleep()` for loading animations; use `st.spinner()` or `st.status()`.
6. Never hardcode database credentials; use `st.secrets` or environment variables via `config.py`.
7. Never create global mutable state outside of `st.session_state`; Streamlit reruns the entire script on each interaction.

## Testing

- Test all functions in `data/processor.py` and `components/` with pytest.
- Use small fixture DataFrames (5-10 rows) defined in `conftest.py`.
- Chart builder tests assert the returned object is a `plotly.graph_objects.Figure` with expected trace count and axis labels.
- Do not test Streamlit page files directly; keep them thin so component tests provide coverage.
- Run `streamlit run Home.py --server.headless true` in CI to verify the app starts without import errors.
