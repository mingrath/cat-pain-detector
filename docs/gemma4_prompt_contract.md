# Gemma 4 Prompt Contract

The model prompt is implemented in `src/cat_pain_detector/prompts.py`.

## Goals

- Accept one uploaded cat image.
- Score five Feline Grimace Scale action units.
- Return strict JSON only.
- Include visible evidence, uncertainty, recommendation, and safety disclaimer.
- Avoid diagnosis or medication advice.

## Required Output

The model must return:

- `action_units.ear_position`
- `action_units.orbital_tightening`
- `action_units.muzzle_tension`
- `action_units.whiskers_change`
- `action_units.head_position`
- `total_raw`
- `total_normalized`
- `rescue_threshold_positive`
- `uncertainty`
- `recommendation`
- `disclaimer`

Each action unit must include:

- `score`: `0`, `1`, `2`, or `null`
- `visible`: boolean
- `evidence`: short grounded sentence
- `uncertainty`: `low`, `medium`, or `high`

## Score Rules

- Scores: 0 absent, 1 moderate/uncertain, 2 obvious.
- If an action unit is not visible, set `visible=false` and `score=null`.
- Only compute `total_raw`, `total_normalized`, and `rescue_threshold_positive` if all five action units are visible.
- Rescue threshold is `total_normalized > 0.39`.

## Parser

`src/cat_pain_detector/json_utils.py` handles:

- fenced JSON extraction
- first-object extraction from noisy text
- JSON schema validation
- FGS-specific consistency validation

