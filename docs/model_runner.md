# Model Runner Abstraction

Implemented in `src/cat_pain_detector/model_runner.py`.

## Why This Exists

Gemma 4 should run server-side first on a GPU-backed environment. The local app, validation scripts, and demo should call a stable runner interface instead of directly coupling to a specific Kaggle, Hugging Face, or local model setup.

Local/edge optimization is intentionally deferred until validation is measurable.

## Backends

### Mock

Default backend for UI development and parser tests.

```bash
CAT_PAIN_RUNNER=mock PYTHONPATH=src python scripts/smoke_test_model_runner.py
```

### HTTP

Server-side backend for hosted GPU inference.

```bash
CAT_PAIN_RUNNER=http \
GEMMA_SERVER_URL=https://your-endpoint.example/analyze \
PYTHONPATH=src python scripts/smoke_test_model_runner.py path/to/cat.jpg
```

Request contract:

```json
{
  "image": "data:image/jpeg;base64,...",
  "prompt": "...",
  "max_new_tokens": 512
}
```

Response contract can be one of:

- final FGS JSON object
- `{ "raw_text": "..." }`
- `{ "content": "..." }`
- `{ "parsed": {...}, "raw_text": "..." }`

### Transformers

GPU/server Python backend adapted from the pulled Kaggle notebook:

`research/kaggle/pulled/gpreda-gemma4/gemma-4-e2b-multilangual-and-multimodal.ipynb`

```bash
CAT_PAIN_RUNNER=transformers \
GEMMA_MODEL_ID=google/gemma-4/transformers/gemma-4-e2b-it \
GEMMA_MAX_NEW_TOKENS=512 \
PYTHONPATH=src python scripts/smoke_test_model_runner.py path/to/cat.jpg
```

For strict JSON scoring, thinking is disabled by default. Leaving Gemma 4 thinking
enabled caused the first local smoke run to spend the token budget on a
`<|channel>thought` trace before emitting JSON. Re-enable only for diagnostics:

```bash
GEMMA_ENABLE_THINKING=true
```

Defaults:

- `device_map="auto"`
- bfloat16/float16 dtype where supported
- batch size 1 via single-image inference
- strict JSON validation after model generation

## Environment Variables

- `CAT_PAIN_RUNNER=mock|http|transformers`
- `GEMMA_SERVER_URL` for HTTP backend
- `GEMMA_MODEL_ID` for Transformers/KaggleHub backend
- `GEMMA_MODEL_PATH` for already-downloaded local/server model path
- `GEMMA_MAX_NEW_TOKENS`, default `512`
- `GEMMA_ENABLE_THINKING=true|false`, default `false`

Local Apple Silicon smoke run note: use a Python 3.12+ environment with current
Gemma 4 Transformers support. Example:

```bash
uv venv .venv-gemma4 --python 3.12
uv pip install --python .venv-gemma4/bin/python -r requirements.txt
```

## Next Use

The validation runner should call:

1. `build_fgs_prompt()`
2. `runner_from_env()`
3. `runner.analyze(image, prompt)`
4. write `ModelResult.raw_text`, `ModelResult.parsed`, and metrics to disk

