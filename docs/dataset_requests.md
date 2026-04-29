# Dataset Request Packets

We need FGS-labeled validation data before making accuracy claims. Public CatFLW is downloaded for facial landmark validation, but it is not pain-labeled.

## Request 1 — Original FGS / 2019 Validation Data

Paper: "Facial expressions of pain in cats: the development and validation of a Feline Grimace Scale"

Corresponding author identified by Firecrawl: Paulo V. Steagall, paulo.steagall@umontreal.ca

Data availability statement: datasets generated/analyzed are available from the corresponding author on reasonable request.

Suggested email:

Subject: Research request: FGS-labeled cat image/video data for validation-only AI pain assessment project

Dear Prof. Steagall,

I am building a non-commercial research prototype for the Kaggle Gemma 4 Good Hackathon focused on explainable, safety-framed feline acute pain triage using the Feline Grimace Scale. I would like to validate the prototype against expert FGS labels rather than make unsupported accuracy claims.

Would it be possible to access the FGS-labeled images/video frames or a validation subset from your 2019 Scientific Reports FGS validation study for validation-only use? We would cite the paper, follow any license/ethics constraints, avoid redistributing the data unless permitted, and report aggregate metrics only.

The planned validation metrics are total FGS score MAE/RMSE, rescue-analgesia threshold classification accuracy/F1, per-action-unit agreement where labels are available, and uncertainty/failure-mode analysis.

Thank you for considering this request.

Best regards,
[Your name]

## Request 2 — 2023 Automated FGS Prediction Dataset

Paper: "Fully automated deep learning models with smartphone applicability for prediction of pain using the Feline Grimace Scale"

Corresponding author identified by Firecrawl: P. V. Steagall, pmortens@cityu.edu.hk

Data availability statement: datasets are not publicly available due to mobile app development, but are available from the corresponding author on reasonable request.

Suggested email:

Subject: Request for validation access to FGS-labeled cat facial image data

Dear Prof. Steagall,

I am developing a non-commercial hackathon prototype that uses Gemma 4 multimodal reasoning to estimate Feline Grimace Scale action-unit scores from cat facial images. The project is intended as triage support only, not diagnosis.

I read your Scientific Reports paper on automated FGS prediction with smartphone applicability. Would you consider sharing a validation subset of the FGS-labeled image data, or aggregate benchmark split details, so we can evaluate our model responsibly against expert labels?

We can keep the data private, cite your work, avoid redistribution, and report only aggregate validation metrics such as FGS score error, rescue-threshold F1, AUROC, and per-AU agreement.

Thank you,
[Your name]

## Request 3 — 2024 Video-Based Pain Recognition Data

Paper: "Automated video-based pain recognition in cats using facial landmarks"

Corresponding author identified by Firecrawl: Anna Zamansky, annazam@is.haifa.ac.il

Data availability statement: datasets used in the paper are available from the corresponding author upon reasonable request.

Suggested email:

Subject: Request for validation subset: cat pain recognition video/landmark data

Dear Prof. Zamansky,

I am building a non-commercial Kaggle Gemma 4 Good Hackathon prototype for explainable cat pain triage using Feline Grimace Scale concepts. I found your Scientific Reports paper on automated video-based pain recognition using cat facial landmarks highly relevant.

Would it be possible to access a validation subset, derived features, labels, or split protocol from the Finka/TiHo Cat Pain datasets for validation-only use? We can follow any restrictions, not redistribute data, cite the paper, and report only aggregate metrics.

Our goal is to avoid unsupported demo claims by measuring total score error, binary pain classification F1, and failure modes.

Thank you,
[Your name]

## Public Dataset Secured

- Dataset: `georgemartvel/catflw`
- Local path: `data/raw/catflw/`
- License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
- Use: landmark/localization validation only, not pain-score validation.
