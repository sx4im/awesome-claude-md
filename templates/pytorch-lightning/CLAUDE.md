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
- PyTorch 2.x as the tensor and autograd engine
- PyTorch Lightning 2.x as the training framework
- torchmetrics for metric computation
- torchvision / torchaudio / torchtext for domain-specific transforms
- Hydra 1.3 for configuration management
- Weights & Biases for experiment tracking
- Lightning CLI for command-line training entry points

## Project Structure

```
src/
├── train.py                     # Entry point: instantiates Trainer and calls fit
├── predict.py                   # Batch prediction script
├── models/
│   ├── base.py                  # Base LightningModule with shared logic
│   ├── classifier.py            # Classification LightningModule
│   └── components/
│       ├── encoder.py           # nn.Module encoder backbone
│       ├── decoder.py           # nn.Module decoder head
│       └── losses.py            # Custom loss functions
├── data/
│   ├── datamodule.py            # LightningDataModule implementation
│   ├── dataset.py               # torch Dataset classes
│   └── transforms.py            # Data augmentation pipelines
├── callbacks/
│   ├── logging.py               # Custom logging callbacks
│   └── early_stop.py            # Custom early stopping logic
├── configs/
│   ├── config.yaml              # Root Hydra config
│   ├── model/
│   │   ├── small.yaml           # Small model variant
│   │   └── large.yaml           # Large model variant
│   ├── data/
│   │   └── default.yaml         # Dataset paths and loader params
│   └── trainer/
│       ├── gpu.yaml             # GPU trainer settings
│       └── cpu.yaml             # CPU debug settings
├── utils/
│   ├── metrics.py               # torchmetrics wrappers
│   └── checkpoint.py            # Checkpoint loading helpers
└── tests/
    ├── test_model.py
    ├── test_datamodule.py
    └── test_transforms.py
```

## Architecture Rules

- Every model must subclass `lightning.LightningModule` and implement `training_step`, `validation_step`, and `configure_optimizers`.
- All data loading must go through a `LightningDataModule` subclass; never create DataLoaders manually in training scripts.
- Neural network building blocks (encoders, decoders, attention) must be plain `nn.Module` classes in `models/components/`; LightningModule classes compose them.
- Hyperparameters must be passed via `__init__` and saved with `self.save_hyperparameters()`.
- Configuration is managed by Hydra YAML files; never hardcode hyperparameters in Python code.
- Use `torchmetrics` objects attached to the module via `self.train_acc = torchmetrics.Accuracy(...)`, never compute metrics with raw Python.

## Coding Conventions

- Log metrics with `self.log("val/loss", loss, prog_bar=True, on_epoch=True)` using the `split/metric_name` format.
- Use `self.trainer.is_global_zero` guard before any print or file-write in distributed training.
- Set `torch.set_float32_matmul_precision("medium")` in `train.py` for Ampere+ GPU performance.
- Prefer `torch.compile(model)` for PyTorch 2.x speed gains; keep a config flag to disable it for debugging.
- Always set `num_workers` and `persistent_workers=True` in DataLoader kwargs via the DataModule.
- Use Lightning's built-in `ModelCheckpoint` callback; configure `monitor="val/loss"` and `mode="min"`.

## Library Preferences

- Weights & Biases (`WandbLogger`) as the primary experiment tracker; TensorBoard as offline fallback.
- Hydra for all config; do not use argparse or click for hyperparameter arguments.
- torchmetrics for accuracy, F1, AUROC; do not use sklearn metrics inside training loops.
- Lightning Fabric only if you need granular control without full Trainer overhead.

## File Naming

- LightningModule files: descriptive model name in snake_case (`classifier.py`, `segmenter.py`).
- Config files: variant name matching the Python module (`small.yaml`, `large.yaml`).
- Test files: `test_` prefix mirroring source path.

## NEVER DO THIS

1. Never call `loss.backward()` or `optimizer.step()` manually in a LightningModule; Lightning handles the training loop.
2. Never create DataLoaders outside of a LightningDataModule; it breaks distributed training and reproducibility.
3. Never hardcode `device` strings like `"cuda:0"`; use `self.device` inside LightningModule methods.
4. Never use `model.eval()` or `torch.no_grad()` in validation_step; Lightning sets these automatically.
5. Never store large tensors in `self` attributes during steps; detach and delete to avoid GPU memory leaks.
6. Never skip `self.save_hyperparameters()`; it is required for checkpoint loading and experiment reproducibility.
7. Never use Python `random` for data augmentation; use `torch.Generator` with seed for reproducibility.

## Testing

- Test every LightningModule with `Trainer(fast_dev_run=True)` to verify the full train/val loop runs without error.
- Test the LightningDataModule by calling `setup("fit")` and checking the first batch shape from `train_dataloader()`.
- Test custom loss functions with small hand-crafted tensors where expected output is known.
- Use `pytest-timeout` with a 60-second limit to catch infinite loops in data loading.
- Run a 2-epoch overfit test on a single batch in CI to verify the model can memorize a trivial dataset.
