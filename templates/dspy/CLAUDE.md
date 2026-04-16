# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- DSPy v2 (framework for programming LLMs)
- Python 3.11+
- Any LLM (OpenAI, Anthropic, local)
- Optional: Weights & Biases for tracking
- Optional: Milvus/Chroma for retrieval

## Project Structure
```
src/
├── modules/
│   ├── qa_module.py            # Custom DSPy modules
│   └── summarizer.py
├── signatures/
│   └── qa_signature.py         # Input/output signatures
├── optimizers/
│   └── bootstrap.py            # Few-shot optimizers
├── teleprompters/
│   └── mipro.py                # Automatic prompt optimization
├── metrics/
│   └── answer_match.py         # Evaluation metrics
└── data/
    └── train.jsonl
```

## Architecture Rules

- **Signatures define I/O.** `question -> answer` with typed fields.
- **Modules contain logic.** Predict, ChainOfThought, ProgramOfThought for reasoning.
- **Teleprompters optimize prompts.** Automatic few-shot selection and instruction tuning.
- **Compiling for optimization.** `teleprompter.compile(program, trainset)` optimizes prompts.

## Coding Conventions

- Define signature: `class QA(Signature): question = InputField(); answer = OutputField(desc="...")`.
- Create module: `class RAG(Module): def __init__(self): self.retrieve = ..., self.generate = Predict(QA)`.
- Forward pass: `def forward(self, question): context = self.retrieve(question); return self.generate(context=context, question=question)`.
- Set LM: `dspy.settings.configure(lm=OpenAI(model="gpt-4"))`.
- Optimize: `tp = BootstrapFewShot(metric=validate); optimized = tp.compile(RAG(), trainset=trainset)`.

## NEVER DO THIS

1. **Never hand-craft prompts.** DSPy's point is optimization—let teleprompters work.
2. **Never skip the train set.** Compilation needs examples to optimize from.
3. **Never ignore the metric.** Optimization requires a quality metric to optimize toward.
4. **Never mix module types carelessly.** Predict vs ChainOfThought have different use cases.
5. **Never forget to configure the LM.** `dspy.settings.configure(lm=...)` is required.
6. **Never skip evaluation.** Measure before and after optimization.
7. **Never use without understanding signatures.** They're the contract between components.

## Testing

- Test signatures produce expected output formats.
- Test modules forward pass with sample inputs.
- Test optimized vs unoptimized performance.

