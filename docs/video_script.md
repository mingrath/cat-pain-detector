# 3-Minute Video Script — Cat Pain Detector

Target length: ~3 minutes. Tone: emotional, careful, validation-first.

## 0:00–0:20 — Hook

Visual: quiet cat hiding under a chair; cut to owner looking worried.

Narration: “Cats are experts at hiding pain. By the time we notice something is wrong, the signs can be subtle: a different face, a lower head, eyes a little tighter. For owners, shelters, and foster homes, the hard question is: should I monitor, or should I call a vet now?”

## 0:20–0:45 — Clinical Language

Visual: simple overlay of the five Feline Grimace Scale cues.

Narration: “Veterinary researchers created the Feline Grimace Scale: ears, eyes, muzzle, whiskers, and head position. Cat Pain Detector uses that validated language as a structured checklist. It is not trying to diagnose disease. It helps a human look more carefully.”

## 0:45–1:25 — Working Demo

Visual: open Gradio app, upload a cat face image, click Analyze.

Narration: “The user uploads a cat image. Gemma 4 receives the image and a strict multimodal prompt. The model must return JSON: one score for each visible action unit, evidence from the image, uncertainty, a normalized total, and safe next steps.”

Visual: report cards appear.

Narration: “The report is intentionally transparent: evidence cards, uncertainty, a recommendation badge, and a reminder to contact a veterinarian if the cat’s behavior or comfort is concerning.”

## 1:25–2:05 — Technical Proof

Visual: architecture diagram.

Narration: “Under the hood, the app has a stable runner abstraction. We can use a mock runner for UI work, a Transformers runner for `google/gemma-4/transformers/gemma-4-e2b-it`, or an HTTP runner for a GPU endpoint. Every response goes through JSON extraction and schema validation before the UI shows it.”

Visual: terminal running validation command, metrics JSON.

Narration: “The project is validation-first. Before making any accuracy claim, we run a repeatable metrics script: total FGS error, rescue-threshold confusion matrix, per-cue agreement, and coverage.”

## 2:05–2:40 — Measured Honesty

Visual: metrics summary table.

Narration: “The first Gemma 4 smoke baseline ran on three official educational FGS examples. It parsed all three responses, but it under-called pain: normalized MAE 0.50, rescue-threshold accuracy 0.333, and zero recall on the two higher-pain examples. A prompt calibration pass did not improve that tiny smoke set.”

Visual: warning/limitations panel.

Narration: “That is exactly why this project matters as a responsible AI pattern. The demo works, but we do not claim clinical accuracy. We are requesting FGS-labeled datasets from the research authors and will only report clinical claims against real labeled validation data.”

## 2:40–3:00 — Impact Close

Visual: owner calling a vet; shelter volunteer using app as checklist.

Narration: “Cat Pain Detector is for earlier attention, not automated diagnosis. It turns a cat photo into an explainable checklist, shows uncertainty, and nudges people toward veterinary care when risk is present. The vision is simple: help humans notice hidden feline pain sooner — safely, transparently, and with measured evidence.”
