# Validation Protocol

## Goal

Validate whether the Cat Pain Detector can reproduce Feline Grimace Scale-style assessments from cat face images with measurable accuracy and calibrated uncertainty.

The key deliverable is not the UI. The key deliverable is a repeatable validation report that explains what the model gets right, what it gets wrong, and when users should not trust it.

## Label Schema

Each FGS-labeled image should have five action-unit labels scored as integers:

- `ear_position`: 0 absent, 1 moderate/uncertain, 2 obvious
- `orbital_tightening`: 0 absent, 1 moderate/uncertain, 2 obvious
- `muzzle_tension`: 0 absent, 1 moderate/uncertain, 2 obvious
- `whiskers_change`: 0 absent, 1 moderate/uncertain, 2 obvious
- `head_position`: 0 absent, 1 moderate/uncertain, 2 obvious

Derived labels:

- `total_raw`: sum of five AU scores, range 0–10
- `total_normalized`: `total_raw / 10`, range 0–1
- `rescue_threshold_positive`: `total_normalized > 0.39`, following the original FGS validation cutoff for rescue analgesia
- `visibility_mask`: per-AU boolean when an action unit cannot be assessed due to crop, occlusion, sleeping, grooming, motion blur, or pose

## Model Output Schema

The model must return structured JSON with:

```json
{
  "action_units": {
    "ear_position": {"score": 0, "evidence": "", "visible": true},
    "orbital_tightening": {"score": 0, "evidence": "", "visible": true},
    "muzzle_tension": {"score": 0, "evidence": "", "visible": true},
    "whiskers_change": {"score": 0, "evidence": "", "visible": true},
    "head_position": {"score": 0, "evidence": "", "visible": true}
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low|medium|high",
  "recommendation": "",
  "disclaimer": ""
}
```

## Primary Metrics

### Total Score Error

- MAE on `total_normalized`
- RMSE on `total_normalized`
- MAE on `total_raw`

Use this for the main technical claim: “mean FGS score error on validation set.”

### Rescue-Threshold Classification

Convert predicted and true normalized scores to binary labels using `> 0.39`.

Report:

- Accuracy
- Precision
- Recall/sensitivity
- Specificity
- F1 score
- Confusion matrix: true negative, false positive, false negative, true positive

False negatives are the highest-risk error because the app may miss a cat with pain indicators.

### Per-Action-Unit Agreement

For each visible AU:

- Exact-match accuracy on scores 0/1/2
- Mean absolute error
- Weighted Cohen’s kappa if enough labels exist

Also report which AUs are weakest. Expect whiskers and muzzle tension to be harder than ears or eyes on low-resolution images.

## Secondary Metrics

### Calibration / Uncertainty

For each model output, bucket by `uncertainty`:

- low
- medium
- high

Report error rate and MAE per bucket. Good behavior means high-uncertainty examples have higher error than low-uncertainty examples.

### Coverage

Report:

- number of images processed
- number rejected as non-cat / no face
- number with each AU visible
- number with all five AUs visible

### Robustness Slices

If metadata exists, slice metrics by:

- painful vs control
- image vs video frame
- pose: frontal vs non-frontal
- lighting quality
- breed/face-shape notes where available
- occlusion / cone / cage bars / human hands

## CatFLW Landmark Validation

CatFLW does not validate pain scoring, but it validates the data loader and visual-evidence pipeline.

For CatFLW:

- Load image, face box, and 48 landmarks.
- Verify one JSON label exists for each image.
- Draw landmarks and boxes for a random sample.
- Compute simple data-quality stats: image sizes, bbox dimensions, missing/invalid landmarks.

If we add a landmark detector later, report normalized mean error against CatFLW labels.

## Baseline Order

1. Data-only sanity report on CatFLW.
2. Prompt-only Gemma 4 baseline on FGS-labeled data when available.
3. Prompt + stricter JSON schema and examples.
4. Prompt + CatFLW/face crop preprocessing.
5. Fine-tuning/LoRA only if baseline is weak and data license permits training.

## Minimum Report For Kaggle Writeup

The writeup should include:

- dataset source and license/permission status
- number of validation examples
- total FGS MAE/RMSE
- rescue-threshold F1 and confusion matrix
- one short failure-mode table
- explicit safety disclaimer: triage support, not diagnosis

## Acceptance Bar For Demo Claims

- If no FGS-labeled validation data is available: demo may say “research prototype” only; no accuracy claim.
- If fewer than 30 labeled images: report metrics as exploratory only.
- If 30+ labeled images: report measured metrics but include confidence caveat.
- If 100+ labeled images: use metrics in the main demo story, still framed as validation on a limited dataset.

