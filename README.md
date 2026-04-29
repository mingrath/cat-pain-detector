# Cat Pain Detector

Validation-first Gemma 4 Good Hackathon prototype for explainable feline acute pain triage from cat face images.

The project uses the Feline Grimace Scale (FGS) as the clinical reasoning frame: ear position, orbital tightening, muzzle tension, whisker change, and head position.

## Safety Scope

This is **triage support, not veterinary diagnosis**. The app should help owners and care teams notice possible pain indicators earlier, explain visible evidence, and decide when to contact a veterinarian.

Do not use this tool to delay urgent veterinary care.

Full safety language: `docs/product_scope_and_safety.md`.

## Current Status

- Competition research complete.
- Scientific papers downloaded into `papers/`.
- CatFLW downloaded locally for landmark validation.
- FGS-labeled pain datasets are pending author request.
- Validation protocol is defined in `docs/validation_protocol.md`.
- First Gemma 4 smoke baseline ran on 3 official FGS educational examples. It parsed 3/3 outputs, but under-called pain, so it is calibration evidence only — not a clinical accuracy claim.
- Gradio demo is wired to `runner_from_env()` and defaults to the mock backend unless configured for Gemma 4.
- Licensed CatFLW demo images are available in `data/demo_samples/` for UI examples; they are not pain-labeled.

Temporary public demo: `https://0aa7a9e29bfaf3de84.gradio.live`

This Gradio share link is temporary and depends on a local machine staying online;
replace it with a stable hosted URL before final Kaggle submission.

## Quick Start

Mock UI development:

```bash
uv venv .venv-gemma4 --python 3.12
uv pip install --python .venv-gemma4/bin/python -r requirements.txt
CAT_PAIN_RUNNER=mock .venv-gemma4/bin/python app.py
```

Gemma 4 local/server smoke run, after the Kaggle model is downloaded:

```bash
CAT_PAIN_RUNNER=transformers \
GEMMA_MODEL_PATH=/path/to/gemma-4-e2b-it/1 \
GEMMA_MAX_NEW_TOKENS=512 \
.venv-gemma4/bin/python app.py
```

For strict JSON scoring, `GEMMA_ENABLE_THINKING` defaults to `false`.

## Project Structure

```text
app.py                         # Gradio demo entrypoint
src/cat_pain_detector/         # reusable package code
docs/                          # validation, writeup, safety docs
research/                      # Firecrawl/Tavily/Kaggle research artifacts
papers/                        # local research PDFs
data/                          # local/private datasets, gitignored except README
models/                        # local model weights/checkpoints, gitignored
metrics/                       # generated validation reports
DESIGN.md                      # design system from designmd
```

## Validation First

The app is not considered credible until it reports:

- total FGS score error
- rescue-threshold accuracy/F1
- confusion matrix
- per-action-unit agreement when labels are available
- uncertainty/failure-mode analysis

See `docs/validation_protocol.md`.

Current tiny smoke metrics are recorded at
`metrics/gemma4_official_examples_smoke_metrics_py312.json` and summarized in
`docs/baseline_validation_status.md`.

## Key References

- Evangelista et al. 2019, original FGS validation: `10.1038/s41598-019-55693-8`
- Automated FGS prediction paper: `10.1038/s41598-023-49031-2`
- Video-based pain recognition paper: `10.1038/s41598-024-78406-2`
- CatFLW paper: `https://arxiv.org/abs/2305.04232`

