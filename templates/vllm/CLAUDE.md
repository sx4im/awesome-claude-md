# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- vLLM (high-throughput LLM serving)
- Python 3.11+
- PagedAttention for efficiency
- OpenAI-compatible API server
- GPU required (CUDA or ROCm)

## Project Structure
```
src/
├── serving/
│   ├── config.py               # Server configuration
│   ├── engine.py               # LLMEngine setup
│   └── api.py                  # API routes
├── models/
│   └── registry.py             # Model management
├── batch/
│   └── processing.py             # Batch inference
└── monitoring/
    └── metrics.py
```

## Architecture Rules

- **PagedAttention for throughput.** vLLM's key innovation: efficient KV cache management.
- **Continuous batching.** Process requests as they arrive, not batch-by-batch.
- **OpenAI-compatible API.** Drop-in replacement for OpenAI API.
- **Quantization support.** AWQ, GPTQ, SqueezeLLM for memory efficiency.

## Coding Conventions

- Serve: `python -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3-8b`.
- Chat completions: `curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "...", "messages": [...]}'`.
- Python API: `from vllm import LLM, SamplingParams; llm = LLM(model="..."); outputs = llm.generate(prompts, SamplingParams(temperature=0.8))`.
- Tensor parallel: `--tensor-parallel-size 2` for multi-GPU.

## NEVER DO THIS

1. **Never run without GPU.** vLLM requires CUDA/ROCm capable GPU.
2. **Never ignore memory limits.** Calculate KV cache requirements—OOM kills the server.
3. **Never skip quantization for large models.** 70B models need 4-bit quantization on consumer GPUs.
4. **Never use batch size 1.** Continuous batching benefits from concurrent requests.
5. **Never forget the system prompt limits.** They're part of the context window.
6. **Never ignore the scheduling policy.** Default FCFS, consider priority scheduling.
7. **Never deploy without monitoring.** Track GPU utilization, queue depth, latency.

## Testing

- Test throughput with concurrent requests.
- Test different quantization methods for quality.
- Test API compatibility with OpenAI client.

