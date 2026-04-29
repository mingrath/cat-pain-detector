# Cat Pain Detector — Gemma 4 Good Hackathon Plan

## Context

Build a hackathon submission for Kaggle's **The Gemma 4 Good Hackathon** using Gemma 4 to solve a real-world health/science problem: helping cat owners, shelters, and veterinary teams detect possible feline pain earlier from cat images and short observations.

Confirmed competition details:

- Competition: `gemma-4-good-hackathon`
- Deadline: **May 18, 2026 at 23:59 UTC**
- Submission format: Kaggle Writeup with video, public code repo, live demo, and media gallery
- Dataset: no official dataset is provided; we must bring or curate our own
- Judging: 40 points impact/vision, 30 points video/storytelling, 30 points technical depth/execution

Recommended positioning:

- Primary track: **Impact Track — Health & Sciences**
- Technical angle: Gemma 4 multimodal reasoning plus structured, explainable Feline Grimace Scale scoring
- Core story: “Cats hide pain. This tool helps humans notice earlier, explain why, and decide when to seek veterinary care.”

## Approach

Create a working proof-of-concept called **Cat Pain Detector** with three layers:

1. **Vision input**
   - User uploads a cat face image or short clip frame.
   - The app analyzes visible facial cues aligned with the Feline Grimace Scale: ears, eyes/orbital tightening, muzzle, whiskers, and head position.

2. **Gemma 4 reasoning layer**
   - Gemma 4 receives the image plus a structured prompt.
   - It returns a pain-likelihood assessment, visible evidence, uncertainty, and practical next steps.
   - Output must be safety-framed: not a veterinary diagnosis, but a triage/support signal.

3. **Demo application**
   - Fast hackathon UI with upload, sample cases, score explanation, and exportable report.
   - Prefer Gradio or Streamlit for speed, with an optional polished landing page if time allows.

Avoid overclaiming. The product should say “possible pain indicators detected” rather than “your cat is in pain.”

## Files to Modify

Initial scaffold should create:

- `README.md` — project overview, setup, demo instructions, safety disclaimer
- `DESIGN.md` — visual design system created with the designmd CLI/API; initial kit downloaded: `chef/genesis`, to be adapted for a trustworthy pet-health demo
- `app.py` — Gradio or Streamlit live demo
- `src/` — reusable app logic
- `src/gemma_client.py` — Gemma 4 inference wrapper
- `src/prompts.py` — structured multimodal prompts
- `src/feline_grimace_scale.py` — scoring schema and explanation helpers
- `data/` — local-only dataset staging, not committed unless licensing allows
- `notebooks/` — experiments and optional fine-tuning notebooks
- `docs/writeup.md` — draft Kaggle writeup under 1,500 words
- `docs/video_script.md` — 3-minute demo/story video script
- `docs/model_card.md` — limitations, safety, data, bias, and intended use
- `requirements.txt` or `pyproject.toml` — dependencies
- `.gitignore` — exclude datasets, model weights, secrets, caches

## Deep Research Findings

Firecrawl research has already identified the first scientific resources and dataset targets. Tavily deep research should also be run before implementation once `tvly` or `TAVILY_API_KEY` is available; currently the local environment has no `tvly` CLI and no `TAVILY_API_KEY`, so this is a short setup blocker rather than a product decision.

Papers to download/read first:

- **Facial expressions of pain in cats: the development and validation of a Feline Grimace Scale** — Evangelista et al., Scientific Reports, 2019. This is the core FGS validation paper. Firecrawl summary: 55 cats, five action units, rescue-analgesia cutoff >0.39 on the 0–1 normalized score, AUC 0.94, strong correlation with rCMPS-F, good/excellent reliability.
- **Fully automated deep learning models with smartphone applicability for prediction of pain using the Feline Grimace Scale** — Scientific Reports, 2023. This is the closest automated baseline. Firecrawl summary: 3,447 cat facial images, 37 landmarks, FGS labels, XGBoost reported 95.5% accuracy and MSE 0.0096 for FGS score prediction; dataset is not public but available from corresponding author on reasonable request.
- **Automated video-based pain recognition in cats using facial landmarks** — Scientific Reports, 2024. Firecrawl summary: uses Finka et al. and TiHo Cat Pain datasets, 48 facial landmarks, temporal video features, AutoEncoder + XGBoost, accuracy/F1 metrics; data available from corresponding authors on reasonable request and code/API appears partially available through a Colab link.
- **CatFLW: Cat Facial Landmarks in the Wild Dataset** — arXiv, 2023. Useful for landmark validation, not pain-label validation. Kaggle has `georgemartvel/catflw` with cat face images and 48 landmarks; use it to evaluate cat face/landmark extraction robustness.
- **Can cat caregivers reliably assess acute pain in cats using the Feline Grimace Scale? A large bilingual global survey** — useful for the owner-facing story and reliability claims.

Dataset acquisition priority:

- First priority: obtain or request FGS-labeled pain images/video from the 2023 and 2024 automated FGS papers.
- Second priority: use `georgemartvel/catflw` for landmark/localization validation while waiting for pain labels.
- Third priority: build a small hand-labeled validation set using FGS rubric and clearly document labeling limitations.

Kaggle and StackOverflow research addendum:

- Pull and adapt the Kaggle notebook `gpreda/gemma-4-e2b-multilangual-and-multimodal` as the concrete Gemma 4 multimodal runner reference.
- Pull and adapt the Kaggle notebook `georgemartvel/catflw-load` for CatFLW image, bounding-box, and landmark loading.
- Add an image smoke test to ensure Gemma 4 is genuinely receiving image inputs, not only text prompts.
- Add strict JSON extraction/repair because model outputs may use fenced JSON or malformed JSON.
- Add GPU safety defaults: `device_map="auto"`, bfloat16/float16 where possible, batch size 1 for validation, and short generation lengths.
- Keep all accuracy claims gated behind generated validation metrics files, not UI impressions.

## Reuse

There is **no reusable application code yet**. This is a new project folder and should be treated as a clean scaffold.

Existing local project state to preserve:

- `NOTE.md` — official competition note confirming there is no provided dataset.

Reference inputs to incorporate during implementation, not existing code to reuse:

- Feline Grimace Scale literature and scoring rubric.
- Publicly licensed cat face/pain datasets if available and license-compatible.
- Kaggle Models: `google/gemma-4` or `keras/gemma4` for Gemma 4 inference.
- Kaggle Writeups format for final submission.

Implementation should start simple and auditable instead of assuming an existing ML pipeline. If fine-tuning is too slow, use Gemma 4 multimodal prompting plus curated examples and structured evaluation.

## Steps

- [x] Finish research sprint before coding: run Firecrawl searches/scrapes, run Tavily deep research after `TAVILY_API_KEY` is provided, and download the papers listed above.
- [x] Secure validation data before building a polished UI: identify FGS-labeled datasets, request non-public datasets from paper authors, and download `georgemartvel/catflw` for landmark validation.
- [x] Define the validation protocol as the core technical deliverable: total FGS score error, per-action-unit agreement, rescue-analgesia threshold accuracy/F1, confusion matrix, and calibration/uncertainty notes.
- [x] Create repository scaffold with README, app entrypoint, docs, source package, ignored data/model folders, and the already-created `DESIGN.md` design system from designmd.
- [x] Define product scope and safety language: triage support, not diagnosis.
- [x] Build Feline Grimace Scale schema with five visible action units and evidence explanations.
- [x] Implement Gemma 4 multimodal prompt that returns structured JSON: per-AU scores, total normalized score, evidence, uncertainty, recommendation, and disclaimer.
- [x] Implement a model runner abstraction so Gemma can run server-side first, with local/edge optimization only after the validation loop works.
- [x] Run the first Gemma 4 baseline on the available tiny official FGS educational validation/smoke set and record metrics before any fine-tuning. Real clinical FGS-labeled validation remains blocked on dataset access.
- [x] Build first Gradio demo with upload image, run analysis, and show a human-readable report only after baseline validation is measurable.
- [x] Add licensed sample images from validation/demo sources; avoid generated placeholders for accuracy claims.
- [x] If baseline accuracy is weak, improve with prompt examples, landmark preprocessing, or lightweight fine-tuning/LoRA. First prompt-calibration iteration was implemented and measured; it did not improve the tiny official-example smoke metric, so further gains require real FGS-labeled examples or landmark preprocessing.
- [x] Improve UI for hackathon storytelling using `DESIGN.md`: trustworthy health feel, evidence cards, uncertainty display, and vet-safe next steps.
- [x] Draft Kaggle writeup with architecture diagram, Gemma 4 usage, dataset/validation method, metrics, limitations, and impact story.
- [x] Draft 3-minute video script focused on emotional story + measured validation + working demo + technical proof.
- [ ] Deploy live demo publicly, likely Hugging Face Spaces or another GPU-backed endpoint, and keep Kaggle Notebook as a reproducible fallback. Deployment notes are drafted in `docs/deployment.md`; automatic HF Space creation is blocked until a Hugging Face token/account is configured.
- [ ] Publish public GitHub repo and attach it to Kaggle Writeup.
- [ ] Submit Kaggle Writeup before **May 18, 2026 at 23:59 UTC**.

## Verification

Technical checks:

- Validation set is defined before demo claims are made.
- Report total FGS score MAE/RMSE or MSE against labels.
- Report binary pain/no-pain or rescue-threshold accuracy, precision, recall, F1, and confusion matrix.
- Report per-action-unit agreement where labels exist.
- Compare Gemma 4 baseline against a simple non-LLM baseline if the dataset supports it.
- App starts locally from clean setup instructions.
- Uploading a cat image produces a structured assessment without crashing.
- Gemma 4 response is parsed reliably, including malformed-response fallback.
- App handles non-cat or low-quality images gracefully.
- Safety disclaimer appears in the UI and generated report.
- No API keys, private datasets, or large model weights are committed.

Hackathon checks:

- Video is 3 minutes or less and publicly viewable without login.
- Public repository clearly shows Gemma 4 implementation.
- Live demo URL is public and does not require login.
- Kaggle Writeup is under 1,500 words.
- Writeup includes project links, media gallery cover image, video, repo, and live demo.

## Open Decisions

- Choose demo framework: Gradio for fastest build, Streamlit for slightly more app-like layout.
- Gemma runtime decision: run Gemma 4 **server-side first** on a GPU-backed service or Kaggle/Hugging Face environment. Do not assume local Mac inference for the hackathon demo. Keep the UI local-light and call a model runner/backend. Explore local/edge/quantized inference only after validation works.
- Decide whether to fine-tune or use prompt-based multimodal reasoning after the first measured baseline.
- Confirm which public cat pain datasets are license-safe for demo/training.
- Get Tavily access: install/enable `tvly` or provide `TAVILY_API_KEY` so the requested Tavily deep-research pass can run alongside Firecrawl.

## Recommended MVP

For the first working milestone, build a **validation-first** Gemma 4 multimodal baseline before the polished demo. It should take labeled cat images, output FGS action-unit scores, compare predictions to labels, and produce an accuracy report.

Then wrap the validated baseline in a Gradio demo that analyzes one uploaded image, scores visible FGS cues, explains uncertainty, and recommends whether the owner should monitor or contact a veterinarian. This is more credible for judging than a UI-only demo.
