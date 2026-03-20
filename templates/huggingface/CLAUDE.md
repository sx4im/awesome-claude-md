# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- HuggingFace Transformers 4.40+
- HuggingFace Datasets for data loading and processing
- PEFT (Parameter-Efficient Fine-Tuning) with LoRA/QLoRA
- Accelerate for distributed training
- bitsandbytes for quantization (4-bit / 8-bit)
- Weights & Biases or MLflow for experiment tracking
- PyTorch 2.x (not TensorFlow, not JAX unless specified)

## Project Structure

```
.
├── configs/
│   ├── training/
│   │   ├── base.yaml            # Base training args (lr, epochs, batch_size)
│   │   ├── lora.yaml            # LoRA-specific: rank, alpha, target_modules
│   │   └── qlora.yaml           # QLoRA: quantization + LoRA config
│   └── model/
│       └── {model-name}.yaml    # Model-specific settings (max_length, tokenizer)
├── src/
│   ├── data/
│   │   ├── dataset.py           # Dataset loading, splits, preprocessing
│   │   ├── collator.py          # Custom data collators (padding, masking)
│   │   └── templates.py         # Chat/instruction templates per model family
│   ├── model/
│   │   ├── loader.py            # Model + tokenizer loading with quantization
│   │   ├── peft_config.py       # LoRA/QLoRA config factory
│   │   └── merging.py           # Merge LoRA adapters back to base model
│   ├── training/
│   │   ├── trainer.py           # Custom Trainer subclass or training loop
│   │   └── metrics.py           # Evaluation metrics (perplexity, ROUGE, accuracy)
│   ├── inference/
│   │   └── pipeline.py          # HF pipeline wrapper + FastAPI serving
│   └── utils/
│       ├── config.py            # Typed config loading from YAML
│       └── reproducibility.py   # Seed setting, GPU memory, dtype selection
├── scripts/
│   ├── train.py                 # Entry point: parse args → load → train → save
│   ├── evaluate.py              # Run evaluation on test set
│   └── merge_adapter.py         # Merge LoRA weights into base model
├── data/                        # Local data cache (gitignored)
├── outputs/                     # Training outputs, checkpoints (gitignored)
├── notebooks/
│   └── exploration.ipynb        # Data exploration and quick experiments
└── pyproject.toml
```

## Architecture Rules

- **Config files drive everything.** Training hyperparameters, LoRA rank, model name, dataset path—all in YAML configs. The training script reads a config path and nothing else. No hyperparameters in Python code.
- **Model loading is centralized in `model/loader.py`.** One function handles: model name resolution, quantization config (4-bit/8-bit/none), dtype selection (bf16/fp16/fp32), device mapping, and tokenizer loading with proper padding configuration. Never load models ad-hoc in training scripts.
- **Data preprocessing is deterministic and cached.** Use `dataset.map()` with `batched=True` and `num_proc>1`. HF Datasets caches processed data via Arrow files. Never reprocess data on every training run.
- **LoRA targets are explicit.** Define `target_modules` in config, not by guessing. For LLaMA: `["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`. For GPT-NeoX: `["query_key_value"]`. Wrong targets = wasted training.
- **Training outputs are organized.** Save to `outputs/{model_name}/{run_id}/` with: adapter weights, tokenizer, training config, metrics, and a `README.md` model card. Never save to the project root.

## Coding Conventions

- **Tokenizer padding side matters.** For causal LM (GPT-style): `tokenizer.padding_side = "left"`. For seq2seq (T5-style): `tokenizer.padding_side = "right"`. Getting this wrong silently produces garbage during batched generation.
- **Always set `pad_token`.** Many models (LLaMA, Mistral) don't have a pad token. Set `tokenizer.pad_token = tokenizer.eos_token` and `model.config.pad_token_id = tokenizer.pad_token_id`. Missing pad token causes crashes during batched training.
- **Use `bf16` when available, `fp16` as fallback.** Check with `torch.cuda.is_bf16_supported()`. bf16 has better numerical stability than fp16 for training. fp32 is wasteful for fine-tuning. Set in config, not hardcoded.
- **Chat templates for instruction tuning.** Use the model's built-in chat template: `tokenizer.apply_chat_template(messages, tokenize=True)`. Never manually format `<s>` instruction markers or `<|im_start|>` tokens—each model family has different special tokens.
- **Gradient checkpointing for memory efficiency.** Enable with `model.gradient_checkpointing_enable()` when fine-tuning models > 7B. Trades compute for memory. Reduces VRAM usage by ~40% with ~20% speed penalty.

## Library Preferences

- **Training:** HuggingFace `Trainer` or `SFTTrainer` from `trl`. Not raw training loops (Trainer handles gradient accumulation, mixed precision, distributed training, and checkpointing).
- **PEFT:** `peft` library with `LoraConfig`. Not full fine-tuning unless you have 8+ GPUs. QLoRA for single-GPU fine-tuning of large models.
- **Quantization:** bitsandbytes for training (4-bit QLoRA). GPTQ or AWQ for inference-only. Not GGUF/GGML (those are for llama.cpp).
- **Data:** HuggingFace `datasets`. Not manual CSV/JSON loading (Datasets handles caching, streaming, and Arrow format).
- **Evaluation:** `evaluate` library for standard metrics. `lm-evaluation-harness` for benchmarks.

## File Naming

- Source files: `snake_case.py` → `peft_config.py`, `collator.py`
- Config files: `snake_case.yaml` → `lora.yaml`, `qlora.yaml`
- Scripts: `snake_case.py` in `scripts/` → `train.py`, `merge_adapter.py`
- Model outputs: `outputs/{model_name}/{run_id}/` → `outputs/llama-3-8b/run_20240115_143022/`

## NEVER DO THIS

1. **Never fine-tune without setting `pad_token`.** LLaMA, Mistral, and many models have `pad_token = None`. Training crashes or produces NaN losses. Always set it: `tokenizer.pad_token = tokenizer.eos_token` before any training.
2. **Never use `fp16` on Ampere+ GPUs when `bf16` is available.** fp16 underflows during loss computation for large models, causing NaN losses that waste hours of training. bf16 has the same speed with better numerical range.
3. **Never hardcode `target_modules` across model families.** LLaMA uses `q_proj, v_proj`. Falcon uses `query_key_value`. Phi uses `q_proj, k_proj`. Always check the model's named modules: `[name for name, _ in model.named_modules() if isinstance(_, torch.nn.Linear)]`.
4. **Never manually format chat tokens.** `<s>` with instruction tags is LLaMA 2 format. `<|im_start|>` is ChatML. `<|user|>` is Phi. Use `tokenizer.apply_chat_template()` which reads the model's `tokenizer_config.json`. Manual formatting breaks silently when you switch models.
5. **Never load a full-precision model for LoRA training.** Use 4-bit quantization (`load_in_4bit=True` with `BitsAndBytesConfig`) for QLoRA. Loading a 70B model in fp16 requires 140GB VRAM. QLoRA fits it in ~40GB.
6. **Never ignore the loss curve.** If training loss plateaus after 1 epoch on a small dataset, you're overfitting. If loss is NaN, check dtype, learning rate, and pad_token. If loss doesn't decrease, check learning rate (typical: 1e-4 to 2e-5 for LoRA).
7. **Never push a model to HuggingFace Hub without a model card.** Include: base model, training data description, intended use, limitations, training hyperparameters, and evaluation results. A model without a card is unusable by anyone else.

## Testing

- Test data preprocessing: load a small subset, run `dataset.map()`, assert output format matches expected schema (input_ids, attention_mask, labels).
- Test model loading: load the model with quantization config, verify dtype (`model.dtype`), verify LoRA modules are attached (`model.print_trainable_parameters()`).
- Test inference: load a trained adapter, run `model.generate()` with a known prompt, assert output is valid text (not garbage tokens or empty).
- Test merging: merge LoRA adapter into base, save, reload, compare outputs against adapter-loaded model. Assert outputs match within tolerance.
- Run `ruff check` and `ruff format --check` in CI. Type-check with `pyright` or `mypy` on `src/` (not on notebooks).
