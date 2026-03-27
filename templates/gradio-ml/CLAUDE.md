# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- Gradio 4.x as the demo interface framework
- Hugging Face Transformers 4.x for model loading and inference
- Hugging Face Hub for model and space deployment
- torch 2.x as the deep learning backend
- Pillow and OpenCV for image preprocessing
- soundfile and librosa for audio preprocessing
- uvicorn behind Gradio for production serving

## Project Structure

```
app/
├── app.py                    # Main Gradio Blocks application
├── models/
│   ├── loader.py             # Model loading with caching
│   ├── text.py               # Text generation/classification inference
│   ├── vision.py             # Image classification/detection inference
│   └── audio.py              # Speech/audio model inference
├── components/
│   ├── inputs.py             # Custom input component builders
│   ├── outputs.py            # Custom output formatters
│   ├── examples.py           # Example inputs per model type
│   └── theme.py              # Custom Gradio theme definition
├── preprocessing/
│   ├── images.py             # Image resize, normalize, augment
│   ├── text.py               # Tokenization helpers, prompt templates
│   └── audio.py              # Audio resampling, chunking
├── utils/
│   ├── device.py             # CUDA/MPS/CPU device selection
│   ├── config.py             # Model IDs, max lengths, defaults
│   └── rate_limit.py         # Request rate limiting logic
├── assets/
│   └── examples/             # Sample images, text files, audio clips
├── Dockerfile
├── requirements.txt
└── tests/
    ├── test_preprocessing.py
    └── test_inference.py
```

## Architecture Rules

- All model loading must go through `models/loader.py` which caches models at module level; never load a model inside a Gradio event handler.
- Use `gr.Blocks` for layout, not `gr.Interface`, to allow tabbed multi-model demos.
- Every inference function must accept and return Python-native types (str, PIL.Image, numpy array); never pass Gradio component objects between functions.
- Preprocessing functions must be pure and testable without Gradio or model dependencies.
- Device selection happens once at startup in `utils/device.py` and is passed to all model loaders.
- All model IDs and hyperparameter defaults live in `utils/config.py` as module-level constants.

## Coding Conventions

- Gradio event handlers must be async functions when doing I/O-bound work; use sync for CPU-bound inference.
- Use `gr.State()` for per-session conversation history, never module-level variables.
- Wrap all inference calls in `torch.no_grad()` context manager.
- Use `gr.Progress()` tracker for any operation taking longer than 2 seconds.
- Set explicit `elem_id` on all interactive components for CSS targeting and testing.
- Type-hint every function; inference functions must annotate input/output types matching Gradio components.

## Library Preferences

- Hugging Face `pipeline()` for standard tasks; raw model + tokenizer only when pipeline lacks needed control.
- Pillow for image I/O; OpenCV only for operations Pillow cannot do (video frames, complex transforms).
- numpy arrays as the interchange format between preprocessing and model input.
- Gradio native components over custom HTML; use `gr.HTML` only for result visualization.

## File Naming

- Model wrapper files named by modality: `text.py`, `vision.py`, `audio.py`.
- Preprocessing files mirror model files by modality name.
- Test files: `test_` prefix matching source module name.

## NEVER DO THIS

1. Never load a model inside a Gradio callback; models must be loaded once at startup and reused.
2. Never use `gr.Interface` for multi-model apps; always use `gr.Blocks` with `gr.Tab`.
3. Never store user uploads or inference results on disk without cleanup; use tempfile with context managers.
4. Never expose raw model error tracebacks to users; catch exceptions and return friendly `gr.Warning` or `gr.Error` messages.
5. Never skip `torch.no_grad()` during inference; it wastes GPU memory and slows execution.
6. Never hardcode model IDs in inference functions; centralize them in `utils/config.py`.

## Testing

- Test all preprocessing functions with small fixture inputs (tiny images, short text strings).
- Test inference wrappers with a small model variant (e.g., `distilbert-base-uncased` instead of full BERT).
- Use `pytest` with `tmp_path` fixture for any test that writes files.
- Mock `torch.cuda.is_available()` in tests to ensure CPU fallback works.
- Integration test: call `gr.Blocks.launch(prevent_thread_lock=True)` and hit the API endpoint with `gradio_client.Client`.
- Run `python app.py` in CI to verify the app initializes without import errors.
