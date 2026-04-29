# Baseline Error Review

Created: 2026-04-29T08:09:48.631150+00:00
Manifest: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants_manifest.csv`
Rows: 9 successful, 0 failed

This report is for manual debugging. It is not a clinical validation claim.

## Metric Snapshot

- Total normalized MAE: 0.47777777777777775
- Rescue threshold accuracy: 0.3333333333333333
- Rescue threshold recall: 0.0
- Confusion matrix: `{'tn': 3, 'fp': 0, 'fn': 6, 'tp': 0}`

## Row Review

### 1. `fgs_official_au0_no_or_mild_pain_cat_only_cat_only.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au0_no_or_mild_pain_cat_only_cat_only.png`
True total: `0` / normalized `0.0` / threshold `False`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=False`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 0 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 0 | 0 | True | low | Eyes are wide open with relaxed eyelids. |
| muzzle_tension | 0 | 0 | True | low | Muzzle appears relaxed and rounded. |
| whiskers_change | 0 | 0 | True | low | Whiskers appear naturally curved and relaxed. |
| head_position | 0 | 0 | True | low | Head is held in a normal alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are wide open with relaxed eyelids.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears relaxed and rounded.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers appear naturally curved and relaxed.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 2. `fgs_official_au0_no_or_mild_pain_cat_only_tight_content.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au0_no_or_mild_pain_cat_only_tight_content.png`
True total: `0` / normalized `0.0` / threshold `False`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=False`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 0 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 0 | 0 | True | low | Eyes are wide open with relaxed eyelids. |
| muzzle_tension | 0 | 0 | True | low | Muzzle appears relaxed and rounded. |
| whiskers_change | 0 | 0 | True | low | Whiskers are relaxed and naturally curved. |
| head_position | 0 | 0 | True | low | Head is held in a normal alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are wide open with relaxed eyelids.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears relaxed and rounded.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers are relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 3. `fgs_official_au0_no_or_mild_pain_cat_only_padded_square.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au0_no_or_mild_pain_cat_only_padded_square.png`
True total: `0` / normalized `0.0` / threshold `False`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=False`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 0 | 0 | True | low | Ears are held in a normal, relaxed position. |
| orbital_tightening | 0 | 0 | True | low | Eyes are wide open with relaxed eyelids. |
| muzzle_tension | 0 | 0 | True | low | Muzzle appears relaxed and rounded. |
| whiskers_change | 0 | 0 | True | low | Whiskers appear relaxed and naturally curved. |
| head_position | 0 | 0 | True | low | Head is held in a normal, alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held in a normal, relaxed position.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are wide open with relaxed eyelids.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears relaxed and rounded.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers appear relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal, alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 4. `fgs_official_au1_mild_to_moderate_pain_cat_only_cat_only.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au1_mild_to_moderate_pain_cat_only_cat_only.png`
True total: `5` / normalized `0.5` / threshold `True`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=True`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 1 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 1 | 0 | True | low | Eyes are open with relaxed eyelids. |
| muzzle_tension | 1 | 0 | True | low | Muzzle appears rounded and relaxed. |
| whiskers_change | 1 | 0 | True | low | Whiskers are relaxed and naturally curved. |
| head_position | 1 | 0 | True | low | Head is held in a normal alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are open with relaxed eyelids.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears rounded and relaxed.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers are relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 5. `fgs_official_au1_mild_to_moderate_pain_cat_only_tight_content.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au1_mild_to_moderate_pain_cat_only_tight_content.png`
True total: `5` / normalized `0.5` / threshold `True`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=True`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 1 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 1 | 0 | True | low | Eyes are open without any visible squinting or tightening. |
| muzzle_tension | 1 | 0 | True | low | Muzzle appears rounded and relaxed. |
| whiskers_change | 1 | 0 | True | low | Whiskers are visible and appear relaxed and naturally curved. |
| head_position | 1 | 0 | True | low | Head is held in a normal alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are open without any visible squinting or tightening.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears rounded and relaxed.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers are visible and appear relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 6. `fgs_official_au1_mild_to_moderate_pain_cat_only_padded_square.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au1_mild_to_moderate_pain_cat_only_padded_square.png`
True total: `5` / normalized `0.5` / threshold `True`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=True`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 1 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 1 | 0 | True | low | Eyes are open with relaxed eyelids. |
| muzzle_tension | 1 | 0 | True | low | Muzzle appears relaxed and rounded. |
| whiskers_change | 1 | 0 | True | low | Whiskers appear relaxed and naturally curved. |
| head_position | 1 | 0 | True | low | Head is held in a normal alert posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are open with relaxed eyelids.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears relaxed and rounded.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers appear relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a normal alert posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 7. `fgs_official_au2_moderate_to_severe_pain_cat_only_cat_only.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au2_moderate_to_severe_pain_cat_only_cat_only.png`
True total: `10` / normalized `1.0` / threshold `True`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=True`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 2 | 0 | True | low | Ears are positioned upright and appear relaxed. |
| orbital_tightening | 2 | 0 | True | low | Eyes are open and appear relaxed. |
| muzzle_tension | 2 | 0 | True | low | Muzzle appears rounded and relaxed. |
| whiskers_change | 2 | 0 | True | low | Whiskers are visible and appear naturally curved. |
| head_position | 2 | 0 | True | low | Head is held in a posture that appears neutral. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are positioned upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are open and appear relaxed.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears rounded and relaxed.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers are visible and appear naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is held in a posture that appears neutral.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 8. `fgs_official_au2_moderate_to_severe_pain_cat_only_tight_content.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au2_moderate_to_severe_pain_cat_only_tight_content.png`
True total: `10` / normalized `1.0` / threshold `True`
Pred total: `2` / normalized `0.2` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=False`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 2 | 0 | True | low | Ears are visible and appear to be in a relaxed, forward position. |
| orbital_tightening | 2 | 1 | True | medium | Eyes are partially closed or squinted, suggesting some degree of narrowing. |
| muzzle_tension | 2 | 1 | True | low | The muzzle shape shows some subtle tension or rounding consistent with a relaxed, resting expression. |
| whiskers_change | 2 | 0 | True | low | Whiskers are visible and appear naturally curved, not stiff or pulled. |
| head_position | 2 | 0 | True | low | The head is held in a resting position, aligned with the body. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are visible and appear to be in a relaxed, forward position.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 1,
      "visible": true,
      "evidence": "Eyes are partially closed or squinted, suggesting some degree of narrowing.",
      "uncertainty": "medium"
    },
    "muzzle_tension": {
      "score": 1,
      "visible": true,
      "evidence": "The muzzle shape shows some subtle tension or rounding consistent with a relaxed, resting expression.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers are visible and appear naturally curved, not stiff or pulled.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "The head is held in a resting position, aligned with the body.",
      "uncertainty": "low"
    }
  },
  "total_raw": 2,
  "total_normalized": 0.20,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>

### 9. `fgs_official_au2_moderate_to_severe_pain_cat_only_padded_square.png`

Image: `/Users/mingrath/projects/cat-pain-detector/data/processed/fgs_official_variants/fgs_official_au2_moderate_to_severe_pain_cat_only_padded_square.png`
True total: `10` / normalized `1.0` / threshold `True`
Pred total: `0` / normalized `0.0` / threshold `False`
Prediction uncertainty: `low`
Recommendation: `low visible concern`
Failure flags: `all_zero_collapse=True`

| Action unit | True | Pred | Visible | Uncertainty | Evidence |
|---|---:|---:|---|---|---|
| ear_position | 2 | 0 | True | low | Ears are held upright and appear relaxed. |
| orbital_tightening | 2 | 0 | True | low | Eyes are open and appear relaxed. |
| muzzle_tension | 2 | 0 | True | low | Muzzle appears rounded and relaxed. |
| whiskers_change | 2 | 0 | True | low | Whiskers appear relaxed and naturally curved. |
| head_position | 2 | 0 | True | low | Head is positioned normally relative to the visible posture. |

<details><summary>Raw model text</summary>

```json
{
  "action_units": {
    "ear_position": {
      "score": 0,
      "visible": true,
      "evidence": "Ears are held upright and appear relaxed.",
      "uncertainty": "low"
    },
    "orbital_tightening": {
      "score": 0,
      "visible": true,
      "evidence": "Eyes are open and appear relaxed.",
      "uncertainty": "low"
    },
    "muzzle_tension": {
      "score": 0,
      "visible": true,
      "evidence": "Muzzle appears rounded and relaxed.",
      "uncertainty": "low"
    },
    "whiskers_change": {
      "score": 0,
      "visible": true,
      "evidence": "Whiskers appear relaxed and naturally curved.",
      "uncertainty": "low"
    },
    "head_position": {
      "score": 0,
      "visible": true,
      "evidence": "Head is positioned normally relative to the visible posture.",
      "uncertainty": "low"
    }
  },
  "total_raw": 0,
  "total_normalized": 0.0,
  "rescue_threshold_positive": false,
  "uncertainty": "low",
  "recommendation": "low visible concern",
  "disclaimer": "This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
}
```

</details>
