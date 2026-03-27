# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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
