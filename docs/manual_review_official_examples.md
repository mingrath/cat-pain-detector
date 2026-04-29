# Manual Review Table — Official FGS Educational Examples

This table tracks the only currently available FGS-labeled reference examples.
They are useful for smoke testing and debugging all-zero collapse, but they are
not enough for training, fine-tuning, or clinical accuracy claims.

| Example | Expected AU Pattern | Expected Total | Current Gemma 4 Failure Mode | Use |
|---|---:|---:|---|---|
| `fgs_official_au0_no_or_mild_pain_cat_only.png` | all 0 | 0/10 | Correctly predicts all 0 | Smoke sanity only |
| `fgs_official_au1_mild_to_moderate_pain_cat_only.png` | all 1 | 5/10 | Predicts all 0, false negative | Prompt/crop debugging only |
| `fgs_official_au2_moderate_to_severe_pain_cat_only.png` | all 2 | 10/10 | Predicts all 0, false negative | Prompt/crop debugging only |

Conclusion: the current model path parses reliably but collapses to relaxed
scores on known moderate/severe educational examples. Do not show numeric scores
publicly until this failure mode is fixed on real FGS-labeled data.
