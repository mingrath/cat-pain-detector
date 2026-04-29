# Data Inventory

This project is validation-first. Do not make model accuracy claims unless the claim points to a validation split and a generated metrics file.

## Secured Locally

### Official FGS Website Educational Examples

- Source page: `https://www.felinegrimacescale.com/practice-your-skills`
- Local original images: `data/raw/fgs_official_examples/`
- Local cat-photo-only crops: `data/raw/fgs_official_examples/cat_only/`
- Local manifest: `data/fgs_official_examples_manifest.csv`
- Count: 3 images
- Labels: all five action units are scored as all-0, all-1, and all-2 according to the official page examples
- Use in this project: smoke test, prompt calibration, visual sanity check, pipeline testing
- Not valid for: public accuracy claims, clinical validation, or measuring real-world distribution performance
- License note: the website does not provide an explicit reuse license; treat images as copyrighted/reference-only and do not commit or redistribute them

Downloaded official reference PDFs:

- `papers/fgs_official/fgs-training-manual.pdf`
- `papers/fgs_official/fgs-factsheet.pdf`

### CatFLW

- Kaggle dataset: `georgemartvel/catflw`
- Local path: `data/raw/catflw/CatFLW dataset/`
- Size on disk: ~1.4 GB
- Images: 2,079 PNG files
- Labels: 2,079 JSON files
- Label fields: `labels` with 48 facial landmarks, `bounding_boxes` with face box coordinates
- License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
- Use in this project: cat face localization, facial landmark parsing, evidence overlay validation
- Not valid for: pain-label accuracy or FGS score accuracy

Demo subset:

- Local path: `data/demo_samples/catflw/`
- Manifest: `data/demo_samples/catflw_demo_manifest.csv`
- Count: 3 images copied from CatFLW under CC BY-NC 4.0
- Use: Gradio upload examples only
- Not valid for: pain-score accuracy or FGS clinical validation


### Ngai et al. 2025 Chatbot FGS Supplement

- Article DOI: `10.1038/s41598-025-27404-z`
- Local raw supplement path: `data/public_fgs_chatbot_2025/raw/` (gitignored)
- Extracted label-only CSV: `data/public_fgs_chatbot_2025/expert_gs_total_labels.csv`
- Count: 50 image IDs with expert gold-standard total FGS ratios
- What is missing: raw cat images and per-action-unit expert labels
- Use in this project: author follow-up/request matching; not directly usable as image validation until corresponding photos are obtained
- Request draft: `docs/dataset_requests/04-chatbot-2025-ngai-image-request.eml`

## FGS-Labeled Datasets To Request

### 2019 Original FGS Validation Study

- Paper: “Facial expressions of pain in cats: the development and validation of a Feline Grimace Scale”
- DOI: `10.1038/s41598-019-55693-8`
- Contact identified: Paulo V. Steagall, `paulo.steagall@umontreal.ca`
- Request draft: `docs/dataset_requests/01-original-fgs-2019-steagall.eml`
- Desired labels: five FGS action units, total FGS score, pain/control status, rescue analgesia label if available

### 2023 Automated FGS Prediction Study

- Paper: “Fully automated deep learning models with smartphone applicability for prediction of pain using the Feline Grimace Scale”
- DOI: `10.1038/s41598-023-49031-2`
- Contact identified: P. V. Steagall, `pmortens@cityu.edu.hk`
- Request draft: `docs/dataset_requests/02-automated-fgs-2023-steagall.eml`
- Desired labels: image-level FGS action-unit scores, total score, train/validation/test split if shareable

### 2024 Video-Based Pain Recognition Study

- Paper: “Automated video-based pain recognition in cats using facial landmarks”
- DOI: `10.1038/s41598-024-78406-2`
- Contact identified: Anna Zamansky, `annazam@is.haifa.ac.il`
- Request draft: `docs/dataset_requests/03-video-pain-2024-zamansky.eml`
- Desired labels: video/frame pain labels, landmarks, split protocol, aggregate baselines

## Fallback If Author Data Does Not Arrive

- Use the official FGS website educational examples only as smoke/calibration data.
- Create any additional tiny validation subset from license-compatible images only.
- Label any fallback subset manually using the FGS rubric with explicit uncertainty.
- Report fallback data as “pilot validation,” not clinical validation.
- Do not compare to published 95%+ results unless using comparable labels and split protocol.

