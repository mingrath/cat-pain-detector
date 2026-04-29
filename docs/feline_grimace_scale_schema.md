# Feline Grimace Scale Schema

The app uses five visible action units from the Feline Grimace Scale.

Each action unit is scored:

- `0`: absent / normal appearance
- `1`: moderate or uncertain presence
- `2`: obvious presence
- `null`: cannot assess because the cue is not visible

## Action Units

| Key | Label | 0 | 1 | 2 |
|---|---|---|---|---|
| `ear_position` | Ear position | Ears forward/relaxed | Slightly pulled apart/rotated | Flattened, rotated outward, far apart |
| `orbital_tightening` | Orbital tightening | Eyes open/relaxed | Mild narrowing/squinting | Marked tightening or near-closed eyes while awake |
| `muzzle_tension` | Muzzle tension | Relaxed, rounded muzzle | Mild tension/shape change | Marked tension, flattening, angular shape |
| `whiskers_change` | Whiskers change | Relaxed natural curve | Mildly shifted/straightened | Straight, stiff, bunched, or pulled |
| `head_position` | Head position | Above shoulder line | Near shoulder line/mildly lowered | Below shoulder line or tucked downward |

## Derived Score

- `total_raw = sum(action unit scores)`, range 0–10
- `total_normalized = total_raw / 10`, range 0–1
- `rescue_threshold_positive = total_normalized > 0.39`

If any action unit is not visible, the total score should be `null` and the result should emphasize uncertainty.

## Evidence Requirement

Every action unit must include one short evidence sentence grounded in visible image details. If not visible, evidence should explain why the cue cannot be assessed.

