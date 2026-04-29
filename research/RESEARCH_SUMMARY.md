# Research Sprint Summary — Cat Pain Detector

## Completed Searches

- Firecrawl scraped search results saved to:
  - `research/firecrawl/fgs-validation-search.json`
  - `research/firecrawl/cat-pain-datasets-search.json`
- Tavily deep research saved to:
  - `research/tavily/cat-pain-detector-deep-research.md`
  - `research/tavily/cat-pain-detector-deep-research-clean.md`

## Downloaded Papers

- `papers/evangelista-2019-feline-grimace-scale.pdf`
- `papers/steagall-2023-automated-fgs-prediction.pdf`
- `papers/martvel-2024-video-pain-recognition-facial-landmarks.pdf`
- `papers/caregivers-2023-fgs-global-survey.pdf`
- `papers/catflw-2023-cat-facial-landmarks-in-the-wild.pdf`
- `papers/explainable-automated-pain-recognition-cats-2023.pdf`

## Key Takeaways

- The core clinical target should be Feline Grimace Scale scoring, not generic cat emotion detection.
- Validation must be central: total FGS score error, per-action-unit agreement, threshold accuracy/F1, confusion matrix, and uncertainty.
- Public FGS-labeled image/video data appears limited; the best FGS pain datasets from automated papers are likely available by author request.
- `georgemartvel/catflw` is immediately usable for cat facial landmark validation but is not a pain-label dataset.
- First model should run server-side for reliability; local/edge optimization comes after validation.

## Tavily Sources

- Facial expressions of pain in cats: the development and validation of a Feline Grimace Scale - PubMed: https://pubmed.ncbi.nlm.nih.gov/31836868/
- Clinical applicability of the Feline Grimace Scale: real-time versus image scoring and the influence of sedation and surgery - PubMed: https://pubmed.ncbi.nlm.nih.gov/32322445/
- Acute Pain Assessment in Cats using Facial Expressions: https://www.felinegrimacescale.com/publications
- Explainable automated pain recognition in cats | Scientific Reports: https://www.nature.com/articles/s41598-023-35846-6
- CatFLW: https://www.kaggle.com/datasets/georgemartvel/catflw
- Automated Detection of Cat Facial Landmarks - Springer Nature: https://link.springer.com/article/10.1007/s11263-024-02006-w
- Cat Dataset - Kaggle: https://www.kaggle.com/datasets/crawford/cat-dataset
- [2305.04232] CatFLW: Cat Facial Landmarks in the Wild Dataset: https://arxiv.org/abs/2305.04232
