# 1. Core Feline Grimace Scale (FGS) papers  

| Study | Focus | Key Findings |
|-------|-------|--------------|
| Evangelista et al., 2019 – *Scientific Reports* | Development & validation of the original FGS (5 action units: ear position, orbital tightening, muzzle tension, whisker change, head position) | Strong inter‑rater reliability (ICC = 0.89), excellent intra‑rater reliability (ICC > 0.91), high internal consistency (Cronbach α = 0.89), cut‑off > 0.39 for rescue analgesia [1] |
| Evangelista et al., 2020 – *PeerJ* | Real‑time vs. image scoring; effect of sedation & ovariohysterectomy | Real‑time scores slightly higher but clinically negligible; sedation (acepromazine‑buprenorphine) did **not** alter total FGS [2] |
| Steagall et al., 2024 – *Journal of Feline Medicine & Surgery* | Effect of training on FGS scoring | Brief training markedly improved inter‑rater agreement among seven veterinarians [3] |
| Watanabe et al., 2020 – *Frontiers in Veterinary Science* | Inter‑rater reliability in cats undergoing dental extractions | ICC ≈ 0.90; caregiver presence had minimal impact [3] |
| Marangoni et al., 2025 – *Journal of Feline Medicine & Surgery* | Application to brachycephalic cats with ocular pain | FGS remained reliable and responsive despite facial‑shape differences [3] |
| Steagall et al., 2023 – *Scientific Reports* | Construct validity & responsiveness in kittens | Moderate‑to‑good inter‑rater reliability; scores rose post‑surgery and fell after analgesia [4] |
| Robinson & Steagall, 2024 – *Journal of Feline Medicine & Surgery* | Training impact on acute‑pain assessment | Training reduced variance and increased ICC [3] |

# 2. Publicly available validation datasets  

| Dataset | Modality | Size* | Annotation format | Licensing / notes |
|---------|----------|------|-------------------|-------------------|
| Original FGS image set (Evangelista et al.) | Still images (110 scored frames) | 110 images (35 painful + 20 controls, multiple frames per cat) | Each image scored 0‑2 on 5 AUs; total ratio calculated | Not explicitly released; used under research‑only agreement (flexible) [1] |
| Cat Pain Dataset used for deep‑learning (Steagall et al., 2023) | Images & video clips | 1 188 annotated images (derived from multiple studies) | FGS total ratio + per‑AU scores | Available via request from FGS website; no formal license stated [3] |
| CatFLW – “Cat Facial Landmarks in the Wild” | Images | 2 079 images (≈2 000) | 48 facial landmarks (ears, eyes, nose, muzzle, whiskers, head pose) | CC‑BY‑NC 4.0 [3][5] |
| Zhang et al. 2008 cat head detection dataset | Images | ~10 000 images | 9 facial landmarks (2 eyes, nose, 6 ear points) | Academic‑use only; distributed via Springer link [6] |
| Kaggle “Cat Dataset” | Images | 9 000+ images | 9 points (2 eyes, mouth, 6 ear points) | CC0 public domain [7] |
| “Cat Facial Landmarks in the Wild” (ArXiv) | Images | 2 079 (same as above) | 48 landmarks, bounding box | CC‑BY‑NC 4.0 [8] |

\*Sizes are approximate as reported in the source material.

# 3. Open‑source cat facial‑landmark resources  

| Resource | # of landmarks | Annotation conventions | Access |
|----------|----------------|------------------------|--------|
| CatFLW (Martvel et al., 2023) | 48 landmarks covering ears, eyes, nose, muzzle, whisker base, head contour | Defined according to cat‑specific Facial Action Coding System (CatFACS); coordinates normalized to [0,1] | Downloadable from the project page / Kaggle; CC‑BY‑NC 4.0 [3][5] |
| Zhang et al. 2008 cat head detection | 9 landmarks (eye corners, nose tip, three points per ear) | Simple geometric points for head pose estimation | Provided with the original CVPR/ECCV supplemental material; academic‑use license [6] |
| Kaggle “Cat Dataset” | 9 landmarks (same as above) | Same as Zhang et al.; stored in per‑image text files | Public domain CC0 [7] |

# 4. Recommended evaluation metrics for a Gemma‑4‑based detector  

| Metric | Why it matters for a hackathon‑scale pain detector |
|--------|---------------------------------------------------|
| **Intraclass Correlation Coefficient (ICC)** | Quantifies agreement between automated scores and human raters; essential because FGS is an observer‑based scale (used in original validation) [1] |
| **Cronbach’s α** | Measures internal consistency of the five AUs when the model outputs them separately; high α indicates coherent composite score (original paper reported α = 0.89) |
| **Pearson / Spearman correlation (ρ)** | Simple indicator of linear relationship with a gold‑standard composite pain score (e.g., Glasgow CMPS‑F) [1] |
| **Accuracy** | Overall proportion of correct pain/no‑pain classifications; easy to compute and communicate in a hackathon demo |
| **Area Under the ROC Curve (AUROC)** | Captures trade‑off between sensitivity and specificity across thresholds; robust to class imbalance common in pain datasets |
| **F1‑score** | Harmonic mean of precision and recall; useful when the “pain” class is rarer than “no‑pain” |
| **Sensitivity & Specificity** | Directly reflect clinical usefulness – sensitivity ensures painful cats are not missed, specificity avoids overtreatment |
| **Mean Absolute Error (MAE) / Normalized Root Mean Square Error (NRMSE)** | For regression‑style outputs (e.g., total FGS ratio), MAE gives an interpretable error magnitude; NRMSE is used in landmark‑prediction studies [4] |
| **Bland‑Altman bias & limits of agreement** | Shows systematic over‑/under‑estimation of real‑time vs. image scores, as reported for FGS‑RT vs. FGS‑IMG [2] |

*In a hackathon, reporting **ICC**, **AUROC**, **F1‑score**, and **MAE** together provides a balanced view of reliability (agreement with humans), discriminative ability (binary classification), and quantitative error (continuous score).*

---

### Sources
- [1] https://pubmed.ncbi.nlm.nih.gov/31836868/
- [2] https://pubmed.ncbi.nlm.nih.gov/32322445/
- [3] https://www.felinegrimacescale.com/publications
- [4] https://www.nature.com/articles/s41598-023-35846-6
- [5] https://www.kaggle.com/datasets/georgemartvel/catflw
- [6] https://link.springer.com/article/10.1007/s11263-024-02006-w
- [7] https://www.kaggle.com/datasets/crawford/cat-dataset
- [8] https://arxiv.org/abs/2305.04232

