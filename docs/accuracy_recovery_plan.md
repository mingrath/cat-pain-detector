# Accuracy Recovery Plan — Cat Pain Detector

Status: created after live-demo testing showed pain scores were not close enough
to trust. This plan supersedes polish/deployment work until scoring improves.

## Top-Level Decision

Do **not** present the current Gemma 4 output as a pain score. The live demo can
remain useful only as an explainable FGS cue checklist after the scoring pipeline
is recalibrated and measured.

The temporary Gradio share should stay offline or clearly disabled until the
minimum gates below pass.

## Target Outcome

Build a validation-first scoring pipeline that can answer three questions:

1. Is a usable awake cat face visible?
2. Which FGS action units are visible and what evidence supports each cue?
3. Given validated labels, how close are the predicted FGS scores to ground truth?

Only after those are measurable should the app show a pain score.

## Minimum Acceptance Gates Before Public Demo

- JSON parse success: >= 95% on the selected validation set.
- Coverage: all five action units scored on >= 80% of clear frontal awake cat-face images.
- Rescue-threshold recall: must be non-zero and reviewed manually; false negatives are highest risk.
- Per-action-unit sanity: model must not collapse to all-zero scores on known moderate/severe examples.
- UI language: score must be labeled “FGS cue estimate,” never diagnosis.
- Every result must include uncertainty and “contact a veterinarian” safety language.

## Phase 0 — Immediate Safety Fix

Goal: prevent misleading users while debugging.

- Take down the temporary Gradio share or switch it to mock/checklist mode.
- Add a UI banner: “Scoring is under recalibration; do not use for pain decisions.”
- Hide or de-emphasize the numeric total until validation gates pass.
- Keep evidence cards visible because they are useful for debugging model perception.

Deliverable: demo cannot imply working pain-score accuracy.

## Phase 1 — Build a Better Error Report

Goal: understand exactly why the score is wrong.

For every validation/demo run, save:

- input image path and thumbnail/crop metadata,
- raw model text,
- parsed JSON,
- per-AU true vs predicted labels when labels exist,
- image quality flags: frontal/side, awake/asleep, occlusion, face crop quality,
- failure class: all-zero collapse, over-score, not-cat, occlusion, parse failure, wrong visibility.

Add a compact HTML/Markdown review report with image + prediction + expected label.

Deliverable: `metrics/error_review_*.md` or `metrics/error_review_*.html`.

## Phase 2 — Fix Input Framing Before Prompt Tuning

Goal: ensure Gemma receives the right visual evidence.

Current official examples may include limited/cropped visual context, and the
model may be defaulting to “healthy-looking cat” instead of FGS calibration.

Actions:

- Add face-crop variants: original image, tight face crop, padded face crop.
- Use CatFLW landmarks to validate face-box and landmark parsing.
- Add a simple image-quality classifier/checklist: cat visible, face visible,
  awake, frontal enough, ears/eyes/muzzle/whiskers/head visible.
- If key cues are missing, force `cannot assess` rather than low score.

Deliverable: preprocessing script that outputs standardized model inputs and a
quality/visibility report.

## Phase 3 — Add True FGS Calibration Examples

Goal: stop all-zero collapse by anchoring the model to the FGS rubric.

Current data reality: we **do not** have raw FGS-labeled training data yet. The
local CatFLW dataset has landmarks only, not pain/FGS labels. The three official
FGS educational examples are too few and have unclear reuse rights, so they are
only suitable for smoke testing and prompt sanity checks — not training,
fine-tuning, or publishable validation.

Priority order:

1. Use author-provided FGS-labeled images if permission is granted.
2. Use any license-safe FGS-labeled public images if found.
3. As a fallback, create a tiny pilot set with manual labels and clear caveats.
   This can support UI/debugging only; it cannot support strong accuracy claims.

Prompt changes:

- Add few-shot examples with expected JSON outputs, but only from license-safe or
  permissioned data.
- Test per-AU prompting separately before asking for total score.
- Ask for visibility first, then score only visible cues.
- Add explicit “do not default uncertain visible cues to 0” instruction.

Deliverable: prompt variants compared by metrics, not by visual impression.

Blocked until one of these is true:

- author-provided FGS-labeled images arrive,
- a license-safe public FGS-labeled dataset is found,
- or we explicitly downgrade the project to an FGS education/checklist demo.

## Phase 4 — Split Detection From Scoring

Goal: reduce one-shot multimodal reasoning errors.

Pipeline should become:

1. Cat/face/quality gate.
2. Landmark or region localization for ears, eyes, muzzle, whiskers, head line.
3. Per-AU scorer with evidence.
4. Score validator that checks total/threshold consistency.
5. Safety recommendation layer.

Gemma can still be the reasoning layer, but it should not be asked to solve all
tasks in one unconstrained pass.

Deliverable: modular pipeline and ablation metrics: raw image vs crop vs
crop+quality gate vs crop+few-shot.

## Phase 5 — Consider Lightweight Fine-Tuning Only After Data Exists

Goal: improve scoring if prompt/crop calibration is still weak.

Training status: blocked. We cannot train or fine-tune on CatFLW for pain
scoring because it has no FGS labels, and we cannot train on the official FGS
website examples because there are only three and reuse rights are unclear.

Only proceed if dataset license/permission explicitly allows training.

Options:

- LoRA or adapter tuning on labeled FGS examples.
- Train a small landmark/FGS baseline model as a sanity comparator.
- Use Gemma for explanation/reporting while a supervised model predicts scores.

Deliverable: baseline comparison table showing whether fine-tuning beats
prompt-only Gemma 4.

## Phase 6 — Re-launch Demo With Guardrails

Goal: publish only after the measured gates pass.

The relaunched demo should show:

- image quality status,
- per-AU visibility,
- per-AU evidence and score,
- total score only when all cues are visible,
- confidence/uncertainty,
- validation snapshot with dataset size,
- explicit “not diagnosis” disclaimer.

If gates do not pass, launch as an “FGS learning/checklist demo” rather than a
“pain detector.”

## Immediate Next Implementation Tasks

1. Disable numeric scoring in the public demo by default.
2. Add error-review report generation to `scripts/run_baseline_validation.py`.
3. Add CatFLW face-box/landmark sanity script and standardized crop generator.
4. Build a small manual review table for the three official examples plus any
   permissioned examples received.
5. Re-run Gemma 4 on original, tight crop, and padded crop variants.
6. Choose the best preprocessing/prompt variant using metrics.

## Non-Negotiable Rule

No Kaggle writeup, video, or live demo may claim the model “detects pain” until
metrics from a real FGS-labeled validation set support that statement.
