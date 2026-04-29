# Public FGS-Labeled Data Search — 2026-04-29

Goal: find real Feline Grimace Scale (FGS) labels that are publicly accessible,
preferably with raw cat photos.

## Found: Ngai et al. 2025 chatbot FGS study supplement

Source:

- Article: “Chatbot assessment of acute pain in cats using the Feline Grimace Scale: comparative study”
- DOI: `10.1038/s41598-025-27404-z`
- Supplementary material 1 URL: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-025-27404-z/MediaObjects/41598_2025_27404_MOESM1_ESM.xlsx`
- Supplementary material 2 URL: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-025-27404-z/MediaObjects/41598_2025_27404_MOESM2_ESM.pdf`

What is useful:

- The article used 50 images.
- Supplementary material 1 contains an `Expert rater (GS)` sheet with 50 image IDs
  and expert gold-standard total FGS ratios.
- Extracted local label-only CSV: `data/public_fgs_chatbot_2025/expert_gs_total_labels.csv`
- Extraction script: `scripts/extract_chatbot_2025_labels.py`

What is missing:

- The XLSX does **not** include the raw cat photos.
- It does not provide per-action-unit expert labels in the `Expert rater (GS)` sheet;
  it provides total normalized/gold-standard score only.
- Therefore it is not directly usable as a vision validation manifest unless we
  obtain the 50 images or can map the image IDs to permissioned image files.

Use in this project:

- Request matching / author follow-up: ask for the 50 images corresponding to the
  public image IDs and GS labels.
- Possible threshold-label validation if the images are obtained.
- Not training data yet.

## Still not found

As of this search, I did not find a publicly downloadable package containing both:

1. raw cat photos, and
2. expert FGS labels for those exact photos,

with license terms allowing use in this project.

The best fully usable FGS datasets still appear to require author permission.
