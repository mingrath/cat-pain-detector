# Baseline Validation Status

Step 9 now has a Gemma 4 smoke/calibration baseline on the tiny official FGS
educational examples. Scientific accuracy claims remain blocked until a real
FGS-labeled validation set is available.

## Completed Smoke Baseline

Run date: 2026-04-29 UTC

Command:

```bash
CAT_PAIN_RUNNER=transformers \
GEMMA_MAX_NEW_TOKENS=512 \
GEMMA_MODEL_PATH=/Users/mingrath/.cache/kagglehub/models/google/gemma-4/transformers/gemma-4-e2b-it/1 \
PYTHONPATH=src \
.venv-gemma4/bin/python scripts/run_baseline_validation.py \
  --manifest data/fgs_official_examples_manifest.csv \
  --output metrics/gemma4_official_examples_smoke_metrics_py312.json
```

Local setup note: this required Python 3.12 with `transformers==5.7.0`, because
the system Python 3.9 install did not include Gemma 4 classes. Thinking was
disabled (`GEMMA_ENABLE_THINKING=false`, the new default) because the first run
used its generation budget on a `<|channel>thought` trace and emitted no JSON.

Results on 3 official educational examples only:

- Rows: 3 successful, 0 failed
- Total normalized MAE: 0.50
- Rescue-threshold accuracy: 0.333
- Rescue-threshold recall/sensitivity: 0.0
- Confusion matrix: TN=1, FP=0, FN=2, TP=0
- Per-action-unit accuracy: 0.333 for all five action units

Interpretation: the first prompt-only Gemma 4 baseline parsed reliably but
under-called pain on these official examples, predicting all action units as 0.
This is useful evidence for Step 12 prompt/example/landmark improvement, but it
is not a publishable clinical validation benchmark.

## Prompt Iteration 1

Because the smoke baseline was weak, the prompt now includes calibration guardrails
to reduce all-zero under-calling: score 0 only when a cue is clearly relaxed,
use score 1 for visible cues uncertain between 0 and 1, and avoid all-zero totals
unless every visible cue independently supports relaxed status.

Re-run output:

- Metrics file: `metrics/gemma4_official_examples_prompt_v3_metrics_py312.json`
- Rows: 3 successful, 0 failed
- Total normalized MAE: 0.50
- Rescue-threshold accuracy: 0.333
- Confusion matrix: TN=1, FP=0, FN=2, TP=0

Result: no measurable improvement on the three official educational examples;
Gemma 4 still predicted all action units as 0. Next credible improvements should
use either true FGS-labeled examples in-context/fine-tuning or a landmark/crop
pipeline validated on CatFLW. Do not tune further against these 3 examples as if
they were a real validation distribution.

## Why It Is Blocked

We have CatFLW locally, but CatFLW contains cat facial landmarks, not pain labels or FGS scores. It can validate face/landmark handling, but it cannot validate pain-score accuracy.

We also now have three official FGS website educational examples locally in `data/raw/fgs_official_examples/` with a manifest at `data/fgs_official_examples_manifest.csv`. These are useful for smoke tests and prompt calibration, but they are not a real validation set because there are only three examples, they come from an educational page, and the reuse license is not explicit.

The scientific papers indicate the best FGS-labeled datasets are available from corresponding authors on reasonable request. Draft emails are in `docs/dataset_requests/`.

## What Is Ready

Baseline runner script:

```bash
CAT_PAIN_RUNNER=transformers \
PYTHONPATH=src \
python scripts/run_baseline_validation.py \
  --manifest data/private/fgs_validation_manifest.csv \
  --output metrics/gemma4_baseline_metrics.json
```

HTTP backend version:

```bash
CAT_PAIN_RUNNER=http \
GEMMA_SERVER_URL=https://your-gpu-endpoint/analyze \
PYTHONPATH=src \
python scripts/run_baseline_validation.py \
  --manifest data/private/fgs_validation_manifest.csv \
  --output metrics/gemma4_baseline_metrics.json
```

Manifest columns are shown in `docs/validation_manifest_example.csv`.

Tiny official-example smoke test manifest:

```bash
CAT_PAIN_RUNNER=transformers \
PYTHONPATH=src \
python scripts/run_baseline_validation.py \
  --manifest data/fgs_official_examples_manifest.csv \
  --output metrics/gemma4_official_examples_smoke_metrics.json
```

This command is only a smoke/calibration run, not a publishable accuracy benchmark.

## Metrics It Will Produce

- total FGS normalized MAE/RMSE
- rescue threshold accuracy/precision/recall/specificity/F1
- confusion matrix
- per-action-unit accuracy and MAE
- coverage, including rows where the model cannot compute a total score

## Rule

Until `metrics/gemma4_baseline_metrics.json` exists from real FGS-labeled images, the demo and writeup must not claim model accuracy.

