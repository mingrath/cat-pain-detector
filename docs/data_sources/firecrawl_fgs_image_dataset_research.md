# Firecrawl Deep Research — Cat Photos Matched to Pain / FGS Labels

Run date: 2026-04-29

Question: Can we find publicly accessible real cat photos matched to Feline
Grimace Scale (FGS) or pain labels, suitable for improving image-based cat pain
prediction?

## Bottom Line

I found **promising sources**, but I did **not** find a clean, immediately
usable public download that contains both raw cat photos and expert FGS labels
with clear use permissions.

The closest leads are:

1. **Feighelstein et al. 2022 — Automated recognition of pain in cats**
   - Article reports 464 cat facial images with binary `Pain` / `No Pain` labels
     and landmark annotations.
   - The article text mentions a GitLab repository for images and landmarks.
   - Current access attempt redirects to GitLab sign-in / returns 403 for git
     access, so it is not directly downloadable from this environment.
   - Label type appears binary pain/no-pain, not full FGS per-action-unit labels.

2. **Ngai et al. 2025 — Chatbot assessment using FGS**
   - Supplementary XLSX is public and contains 50 image IDs with expert
     gold-standard total FGS ratios.
   - The raw cat photos are not inside the XLSX.
   - This is useful label-only data, but cannot validate an image model until the
     matching photos are obtained.

3. **Understanding the Feline Grimace Scale, 2025**
   - Search result states 100 cat face images with FGS scores from a databank.
   - I did not find a public image download; likely request/access required.

4. **Automated FGS prediction, 2023**
   - Uses FGS-labeled images and is the most directly relevant to our goal.
   - Data availability says dataset is available from corresponding authors upon
     request, not public direct download.

## Search Artifacts

Raw Firecrawl outputs are saved under:

`research/firecrawl/deep_fgs_search/`

That directory is gitignored because it contains bulky scraped web content.

Key searches included:

- `Feline Grimace Scale dataset images labels cat pain`
- `cat pain Feline Grimace Scale images supplementary material dataset`
- `automated prediction pain Feline Grimace Scale dataset images labels GitHub`
- `"Automated recognition of pain in cats" dataset images FGS labels`
- `"Finka" "cat pain" dataset images labels`
- `"TiHo" "cat pain" dataset images labels`
- `"Understanding the Feline Grimace Scale" images FGS scores databank 100 face images`
- `"gitlab.com/is-annazam/automated-recognition-of-pain-in-cats"`

## Candidate Sources

### 1. Feighelstein et al. 2022 — Automated Recognition of Pain in Cats

URL: https://www.nature.com/articles/s41598-022-13348-1

Firecrawl finding:

- The article describes domestic shorthair cat facial images captured around
  ovariohysterectomy at pain-relevant time points.
- It reports a final balanced dataset of 464 images from 26 cats: 232 `No Pain`
  and 232 `Pain`.
- It reports 48 facial landmark annotations.
- The article text references:
  `https://gitlab.com/is-annazam/automated-recognition-of-pain-in-cats`

Access check:

- Firecrawl scrape of GitLab returned a sign-in page.
- `curl` archive checks redirected to GitLab sign-in.
- git smart HTTP returned 403.

Conclusion:

- This is the best lead for raw cat photos matched to pain labels.
- It is binary pain/no-pain, not full FGS action-unit labels.
- We need GitLab access or author contact.

Next action:

- Contact Anna Zamansky / Tech4Animals and ask for repository access or a data-use
  route for the 464 images and labels.

### 2. Ngai et al. 2025 — Chatbot FGS Study

URL: https://www.nature.com/articles/s41598-025-27404-z

Supplementary XLSX:

`https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-025-27404-z/MediaObjects/41598_2025_27404_MOESM1_ESM.xlsx`

What we extracted:

- `data/public_fgs_chatbot_2025/expert_gs_total_labels.csv`
- 50 image IDs
- expert gold-standard total FGS ratios
- rescue-threshold label computed as `GS > 0.39`

Limitation:

- Raw photos are not included in the workbook.
- Per-action-unit expert labels are not included in the `Expert rater (GS)` sheet.

Next action:

- Send `docs/dataset_requests/04-chatbot-2025-ngai-image-request.eml` asking for
  the 50 matching images.

### 3. Understanding the Feline Grimace Scale, 2025

URL found by Firecrawl:

https://www.sciencedirect.com/science/article/pii/S1090023325001522

Firecrawl search result states:

- 100 face images of cats with different pain severity.
- Images had FGS scores.
- Images were selected from a databank.

Limitation:

- No public image download was found in this pass.

Next action:

- Add author/data request if we identify corresponding author contact.

### 4. Automated FGS Prediction, 2023

URL: https://www.nature.com/articles/s41598-023-49031-2

Status:

- Highly relevant because it used FGS-labeled images.
- Still appears available only from corresponding authors on reasonable request.
- Request draft already exists in `docs/dataset_requests/02-automated-fgs-2023-steagall.eml`.

## Practical Implication for Our Model

We still cannot honestly train or validate a photo-based FGS predictor until we
obtain the matching images. However, this Firecrawl pass produced two concrete
follow-ups:

1. Request access to the Feighelstein/Zamansky 2022 GitLab dataset: 464 cat face
   images with pain/no-pain labels and landmarks.
2. Request the 50 photos matching the Ngai 2025 public expert FGS total labels.

If either request succeeds, we can build a real validation manifest and restart
model calibration.
