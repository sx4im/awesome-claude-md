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

## Production Delivery Playbook (Category: AI & ML)

### Release Discipline
- Never expose raw secrets, prompts, or proprietary training data.
- Validate model outputs before side effects (tool calls, writes, automations).
- Track model/version/config used in each production-impacting change.

### Merge/Release Gates
- Evaluation set checks pass on quality, safety, and regression thresholds.
- Hallucination-sensitive flows have deterministic fallback behavior.
- Prompt/template changes include before/after examples.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Python 3.11+
- MLflow 2.x for experiment tracking, model registry, and serving
- scikit-learn, XGBoost, or LightGBM for model training
- PyTorch or TensorFlow for deep learning models (via MLflow flavors)
- pandas for feature engineering and data manipulation
- Optuna for hyperparameter optimization with MLflow callback
- Docker for containerized model serving
- PostgreSQL + S3 as the MLflow tracking server backend

## Project Structure

```
project/
├── train.py                        # Main training entry point
├── serve.py                        # Model serving entry point
├── pipelines/
│   ├── feature_engineering.py      # Feature computation and selection
│   ├── training.py                 # Model training with MLflow tracking
│   ├── evaluation.py              # Model evaluation and comparison
│   ├── registration.py            # Model registry promotion logic
│   └── inference.py               # Batch and online inference logic
├── models/
│   ├── baseline.py                 # Baseline model (logistic regression)
│   ├── xgboost_model.py           # XGBoost model wrapper
│   ├── lightgbm_model.py          # LightGBM model wrapper
│   └── custom_model.py            # Custom MLflow pyfunc model
├── data/
│   ├── loader.py                   # Data loading and train/test split
│   ├── validation.py              # Data schema and drift checks
│   └── preprocessing.py           # Scaling, encoding, imputation
├── evaluation/
│   ├── metrics.py                  # Custom metric computation
│   ├── plots.py                   # Confusion matrix, ROC, SHAP plots
│   └── comparison.py             # Multi-run comparison utilities
├── config/
│   ├── experiment.yaml             # Experiment name, tags, defaults
│   ├── hyperparams.yaml           # Hyperparameter search spaces
│   └── serving.yaml               # Serving endpoint configuration
├── utils/
│   ├── mlflow_helpers.py          # MLflow convenience wrappers
│   ├── reproducibility.py        # Seed setting, determinism helpers
│   └── environment.py            # Tracking URI and artifact config
└── tests/
    ├── test_feature_engineering.py
    ├── test_training.py
    └── test_custom_model.py
```

## Architecture Rules

- Every training run must be wrapped in `mlflow.start_run()` context manager; never log metrics or artifacts outside an active run.
- Log all hyperparameters with `mlflow.log_params()` at the start of the run, before training begins.
- Log metrics at each training epoch/iteration with `mlflow.log_metric(key, value, step=epoch)` for loss curves.
- Log the trained model with the appropriate flavor (`mlflow.sklearn.log_model`, `mlflow.xgboost.log_model`) including an `input_example` and `signature`.
- Register production-ready models in the MLflow Model Registry with stage transitions: None -> Staging -> Production.
- All experiment names must follow the format `<project>/<model_type>/<task>` (e.g., `churn/xgboost/classification`).

## Coding Conventions

- Set the tracking URI in `utils/environment.py` from the `MLFLOW_TRACKING_URI` environment variable; never hardcode URIs.
- Use `mlflow.autolog()` for supported frameworks (sklearn, xgboost, lightgbm) as a baseline, then add custom logging on top.
- Log evaluation plots as artifacts: `mlflow.log_figure(fig, "confusion_matrix.png")`.
- Tag every run with `mlflow.set_tag("developer", os.getenv("USER"))` and `mlflow.set_tag("git_sha", git_sha)`.
- Use `mlflow.log_input()` to record the training dataset as a logged dataset for lineage.
- Model versions in the registry must have a description explaining what changed from the previous version.
- Use `mlflow.pyfunc.PythonModel` for custom models that need preprocessing bundled with prediction.

## Library Preferences

- MLflow native model flavors (`mlflow.sklearn`, `mlflow.xgboost`) over generic `mlflow.pyfunc` when a flavor exists.
- Optuna with `MLflowCallback` for hyperparameter search; log each trial as a nested MLflow run.
- SHAP for model explainability; log SHAP summary plots as MLflow artifacts.
- scikit-learn pipelines (`Pipeline`, `ColumnTransformer`) for preprocessing to ensure the full pipeline is serialized with the model.
- YAML config files for experiment parameters; do not use argparse for hyperparameters.

## File Naming

- Pipeline step files: verb describing the ML lifecycle step (`training.py`, `evaluation.py`, `registration.py`).
- Model files: model algorithm name in snake_case (`xgboost_model.py`, `lightgbm_model.py`).
- Config files: purpose-based naming (`experiment.yaml`, `hyperparams.yaml`).

## NEVER DO THIS

1. Never train a model without an active MLflow run context; orphaned metrics and artifacts are impossible to trace.
2. Never log a model without `mlflow.models.signature.infer_signature()` and `input_example`; models without signatures cannot be validated at serving time.
3. Never promote a model to Production stage without comparing its metrics against the current Production model programmatically.
4. Never hardcode the MLflow tracking URI; always read from environment variables for portability across dev/staging/prod.
5. Never use `pickle` or `joblib` directly for model serialization; always use MLflow model flavors which handle environment capture and reproducibility.
6. Never skip logging the git commit SHA and training data hash; without these, runs are not reproducible.
7. Never log large raw datasets as artifacts; log dataset fingerprints (hash, row count, schema) and store data in the data warehouse.

## Testing

- Test feature engineering functions with small pandas DataFrames (10-20 rows) and assert output column names, types, and value ranges.
- Test custom `PythonModel` classes by instantiating them, calling `predict()` with fixture data, and asserting output shape and type.
- Test model registration logic with a local MLflow tracking server (`mlflow server --backend-store-uri sqlite:///test.db`).
- Use `mlflow.start_run()` in tests with a temporary experiment to avoid polluting real experiment namespaces.
- Assert that every training pipeline call results in logged params, metrics, and a model artifact by querying the MLflow client API.
- Test serving by loading a logged model with `mlflow.pyfunc.load_model()` and calling `.predict()` on fixture data.
