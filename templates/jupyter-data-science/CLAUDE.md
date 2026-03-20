# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+ with Jupyter notebooks (.ipynb)
- pandas 2.x / polars for data manipulation
- scikit-learn for ML modeling, XGBoost/LightGBM for gradient boosting
- matplotlib + seaborn for static plots, plotly for interactive
- NumPy for numerical computation
- DVC for data versioning, MLflow for experiment tracking

## Project Structure

```
{project-root}/
├── notebooks/
│   ├── 01_data_exploration.ipynb    # EDA and profiling
│   ├── 02_feature_engineering.ipynb # Feature creation and selection
│   ├── 03_modeling.ipynb            # Model training and evaluation
│   └── 04_analysis.ipynb            # Final analysis and reporting
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── loaders.py               # Data loading functions
│   │   └── validators.py            # Schema validation (pandera)
│   ├── features/
│   │   └── transformers.py          # sklearn-compatible transformers
│   ├── models/
│   │   └── pipelines.py             # Full sklearn Pipeline definitions
│   └── visualization/
│       └── plots.py                 # Reusable plotting functions
├── data/
│   ├── raw/                         # Immutable original data (gitignored)
│   ├── processed/                   # Cleaned datasets (gitignored)
│   └── external/                    # Third-party reference data
├── models/                          # Serialized models (gitignored)
├── reports/
│   └── figures/                     # Exported plots for sharing
├── tests/
│   └── test_transformers.py
├── pyproject.toml
└── dvc.yaml                         # DVC pipeline definitions
```

## Architecture Rules

- **Notebooks are for narrative, not logic.** Notebooks call functions from `src/`. If a cell exceeds 15 lines of non-plotting code, extract it to a module. Notebooks are presentation layers, not engineering artifacts.
- **Data is immutable.** Never modify files in `data/raw/`. All transformations produce new files in `data/processed/`. This guarantees reproducibility from raw source to final result.
- **Pipelines over loose steps.** Use `sklearn.pipeline.Pipeline` and `ColumnTransformer` for all preprocessing + modeling. Never manually call `.fit()` then `.transform()` in separate cells that depend on execution order.
- **Parameterize everything.** Hardcoded file paths, column names, and hyperparameters go in a config dict or YAML at the top of the notebook. Never scatter `df["customer_id"]` string literals across 40 cells.
- **One notebook, one purpose.** Numbered prefix indicates execution order. Each notebook reads an artifact from the previous step and writes one for the next. Never have a 200-cell mega-notebook.

## Coding Conventions

- **Imports at the top.** Every notebook starts with a single cell containing all imports. Never `import pandas as pd` halfway through a notebook.
- **Use polars for large datasets.** If data exceeds 1GB or operations are slow, use polars with lazy evaluation (`pl.scan_csv().filter().collect()`). Convert to pandas only at the visualization boundary.
- **Type-annotated functions.** All functions in `src/` have type hints. Use `pd.DataFrame` for pandas, `pl.DataFrame` for polars, `npt.NDArray[np.float64]` for numpy.
- **Consistent column naming.** All column names are `snake_case`. Rename on load: `df.columns = [c.lower().replace(" ", "_") for c in df.columns]`.
- **Reproducible randomness.** Every function accepting randomness takes a `random_state` parameter. Set `np.random.seed()` once at notebook top, pass `random_state=42` to sklearn estimators.

## Library Preferences

- **DataFrames:** polars for ETL and large data, pandas for sklearn integration and plotting. Not PySpark unless data physically cannot fit in memory.
- **Validation:** pandera for DataFrame schema validation. Not manual assert statements scattered through code.
- **Plotting:** matplotlib/seaborn for publication-quality static plots, plotly for interactive exploration. Not bokeh (ecosystem fragmentation).
- **Experiment tracking:** MLflow for logging params, metrics, and artifacts. Not manual spreadsheets or print statements.
- **Environment:** pip with pyproject.toml and pip-compile for pinned lockfile. Not conda unless you need compiled C dependencies that pip cannot install.

## File Naming

- Notebooks: `XX_descriptive_name.ipynb` (numbered, snake_case)
- Source modules: `snake_case.py`
- Data files: `descriptive_name_YYYYMMDD.parquet` (date-stamped, parquet over CSV)
- Models: `model_name_vX.Y.joblib` (versioned, joblib over pickle)

## NEVER DO THIS

1. **Never commit data files to git.** Use `.gitignore` for `data/raw/`, `data/processed/`, and `models/`. Track data with DVC or store in S3/GCS. Git repos with 500MB CSVs are unusable.
2. **Never use `df.inplace=True`.** It is deprecated behavior, causes subtle bugs with chained operations, and prevents method chaining. Always reassign: `df = df.dropna()`.
3. **Never use global mutable state between cells.** If cell 15 depends on a variable set in cell 3 and modified in cell 9, the notebook is broken for anyone who runs cells out of order. Pass data through function arguments.
4. **Never train and evaluate on the same data.** Always split first: `X_train, X_test = train_test_split(X, test_size=0.2, random_state=42, stratify=y)`. Never report training accuracy as model performance.
5. **Never pickle sklearn models without versioning.** Pickle files are Python-version-specific and break silently. Use `joblib.dump()` with sklearn version in the filename. Log the exact `sklearn.__version__` in MLflow.
6. **Never suppress warnings globally.** `warnings.filterwarnings("ignore")` hides convergence failures, deprecation notices, and data type coercions that indicate real bugs.
7. **Never use `pd.read_csv()` without specifying `dtype` for key columns.** Pandas will silently convert your ID column to float64 if it contains NaN, turning `"12345"` into `12345.0`. Specify `dtype={"id": str}`.

## Testing

- Test all functions in `src/` with pytest. Create small fixture DataFrames that exercise edge cases (empty frames, NaN values, single-row frames).
- Validate DataFrame schemas at pipeline boundaries using pandera: assert expected columns, types, and value ranges before modeling.
- Use `nbval` or `nbmake` to execute notebooks end-to-end in CI with a small sample dataset. A notebook that cannot run top-to-bottom without errors is broken.
- Test custom sklearn transformers by verifying `.fit().transform()` output shapes and that `.get_feature_names_out()` returns correct names.
