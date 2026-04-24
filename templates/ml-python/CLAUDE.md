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
- PyTorch 2.x or scikit-learn (depending on task)
- Jupyter notebooks for exploration
- MLflow for experiment tracking
- FastAPI for model serving
- DVC or S3 for data versioning
- UV or pip for dependency management

## Project Structure

```
.
├── data/
│   ├── raw/               # Original, immutable data (never committed to git)
│   ├── processed/         # Cleaned, transformed data (gitignored, reproducible)
│   └── external/          # Third-party datasets (gitignored, documented in README)
├── notebooks/             # Exploration and analysis notebooks
│   ├── 2024-01-15-eda-user-churn.ipynb
│   └── 2024-01-20-feature-engineering.ipynb
├── src/
│   ├── data/              # Data loading and preprocessing
│   │   ├── dataset.py     # PyTorch Dataset classes or data loaders
│   │   └── preprocessing.py
│   ├── models/            # Model architecture definitions
│   │   ├── baseline.py
│   │   └── transformer.py
│   ├── training/          # Training loops, loss functions, schedulers
│   │   ├── train.py       # Main training script
│   │   └── evaluate.py    # Evaluation and metrics
│   ├── serving/           # FastAPI app for model inference
│   │   ├── app.py
│   │   └── schemas.py
│   └── utils/             # Shared utilities (logging, config, seeds)
│       ├── config.py      # Experiment configuration
│       ├── logger.py      # Structured logging setup
│       └── reproducibility.py  # Seed setting, deterministic flags
├── models/                # Saved model checkpoints (gitignored)
│   └── .gitkeep
├── configs/               # Experiment configs (YAML or JSON)
│   ├── baseline.yaml
│   └── experiment_v2.yaml
├── tests/
└── pyproject.toml
```

## Architecture Rules

- **Notebooks are for exploration only.** Any code that works gets refactored into `src/` within the same PR. Notebooks are documentation of the thought process, not production code.
- **Training scripts are deterministic.** Every training run must be reproducible. Set random seeds for Python, NumPy, PyTorch, and CUDA at the top of every training script. Pin every dependency version in `pyproject.toml`.
- **Data never lives in git.** Raw data stays in S3/GCS/DVC. Only `data/.gitkeep` files and a `data/README.md` describing the data sources are committed.
- **Models are saved with metadata.** Every saved model file includes: training config, metrics, git commit hash, and dataset version. Use MLflow's artifact logging or save a `metadata.json` alongside the checkpoint.
- **Experiment configs drive training.** Training scripts read parameters from YAML config files in `configs/`, not from command-line arguments scattered across scripts.

## Coding Conventions

- **Notebook naming:** `YYYY-MM-DD-description.ipynb` → `2024-01-15-eda-user-churn.ipynb`. Date-prefix ensures chronological ordering. Description uses kebab-case.
- **Experiment tracking:** Log every run to MLflow. At minimum log: all hyperparameters, training/validation metrics per epoch, final test metrics, and the model artifact. No exceptions, even for "quick tests."
- **Config files:** Use YAML with typed validation via Pydantic. Each config has `model`, `training`, and `data` sections with explicit types.
- **Imports:** `pathlib.Path` for all file paths. never string concatenation or `os.path.join()`. Define path constants in `src/utils/config.py`.
- **Type hints on all function signatures.** Use `torch.Tensor` not `Any` for tensor arguments. Use `np.ndarray` not `Any` for array arguments.

## Library Preferences

- **Experiment tracking:** MLflow. not Weights & Biases (MLflow is self-hosted, no vendor lock-in) and not TensorBoard (MLflow tracks artifacts, params, and metrics in one place).
- **Data manipulation:** `polars` for dataframes. not `pandas` (polars is 10-50x faster for large datasets) unless a downstream library requires pandas.
- **Config management:** Pydantic with YAML loading. not Hydra (too much magic) and not argparse (not composable, not typed).
- **Serving:** FastAPI. async, auto-generates OpenAPI docs, works with the Pydantic models you already have.
- **Logging:** Python's `logging` module with `structlog` for structured output. not `print()`.

## Reproducibility Rules

Every training script must call this at startup:

```python
def set_seeds(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

Pin `seed` in the experiment config. Log it to MLflow. Never run an experiment without a fixed seed.

## File Naming

- Source modules: `snake_case.py` → `train.py`, `dataset.py`, `preprocessing.py`
- Notebooks: `YYYY-MM-DD-kebab-case.ipynb` → `2024-01-15-eda-user-churn.ipynb`
- Configs: `snake_case.yaml` → `baseline.yaml`, `experiment_v2.yaml`
- Model checkpoints: `{model_name}_{epoch}_{metric}.pt` → `transformer_epoch10_val0.85.pt`
- Test files: `test_` prefix → `test_dataset.py`, `test_preprocessing.py`

## NEVER DO THIS

1. **Never train on test data.** Keep train/validation/test splits in separate files or directories. The test set is loaded only in `evaluate.py`, never imported in `train.py`. If you need a validation set, split it from training data explicitly.
2. **Never hardcode file paths.** Use `pathlib.Path` with a base `DATA_DIR` and `MODELS_DIR` defined in `src/utils/config.py`. Paths must be composable: `DATA_DIR / "raw" / "users.parquet"`.
3. **Never save a model without metadata.** Every checkpoint must be accompanied by training config, metrics, and the git commit hash. A model file alone is useless 2 weeks later when you can't remember what hyperparameters produced it.
4. **Never use `print()` for logging.** Use the `logging` module with levels: `logger.info()` for progress, `logger.warning()` for recoverable issues, `logger.error()` for failures. `print()` output disappears, structured logs are searchable.
5. **Never commit raw data to git.** Data stays in object storage with versioning (DVC, S3 versioning, or git-lfs for small files). Only data documentation and `.gitkeep` files are committed.
6. **Never skip MLflow logging for "quick experiments."** Every run gets logged. Quick experiments that produce surprising results are the ones you most need to reproduce.
7. **Never leave GPU memory unmanaged.** Use `torch.cuda.empty_cache()` between experiments, delete unused tensors explicitly, and use `with torch.no_grad():` for all inference code. OOM errors at 3 AM with no context are the worst debugging experience.

## Testing

- Use `pytest` for all tests. Test data preprocessing pipelines with small fixture datasets.
- Test model forward passes with fixed seeds and known inputs → assert expected output shapes.
- Test serving endpoints with `httpx.AsyncClient` against the FastAPI app.
- Never test against real model weights in CI. use randomly initialized models with fixed seeds.
