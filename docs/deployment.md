# Deployment Notes

Preferred public deployment: Hugging Face Spaces with GPU or a CPU Space that
calls a separate GPU-backed `CAT_PAIN_RUNNER=http` endpoint.

## Required secrets / environment

- `CAT_PAIN_RUNNER=mock|http|transformers`
- `GEMMA_SERVER_URL` if using `CAT_PAIN_RUNNER=http`
- `GEMMA_MODEL_PATH` or `GEMMA_MODEL_ID` if using `CAT_PAIN_RUNNER=transformers`
- `GEMMA_MAX_NEW_TOKENS=512`
- `GEMMA_ENABLE_THINKING=false`

## Local public share smoke test

```bash
CAT_PAIN_RUNNER=mock \
GRADIO_SHARE=true \
.venv-gemma4/bin/python app.py
```

This creates a temporary Gradio share link only. It is useful for demo smoke
testing, but it is not a stable hackathon deployment.

## Hugging Face Space plan

1. Create a Space under the project/user account.
2. Push this repository's `app.py`, `src/`, `requirements.txt`, `README.md`, and
   `data/demo_samples/`.
3. Set the Space environment variables above.
4. If GPU-backed Gemma 4 cannot fit in the Space budget, run the Space in HTTP
   mode and point it to a GPU inference endpoint.

Current blocker: no Hugging Face token is configured in this environment, so the
public Space cannot be created automatically from here.

## Kaggle fallback

A private Kaggle kernel was pushed for Gemma 4 baseline execution:

`https://www.kaggle.com/code/mingrathmekavichai/cat-pain-gemma4-official-examples-baseline`

It failed on the assigned P100 because the installed PyTorch build did not
support that GPU architecture. Local Apple Silicon Python 3.12 + Transformers
5.7 succeeded for the smoke baseline.
