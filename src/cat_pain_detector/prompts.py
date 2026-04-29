"""Prompt scaffolds for Gemma 4 multimodal FGS analysis."""

from __future__ import annotations

import json
from typing import Any

from cat_pain_detector.feline_grimace_scale import (
    ACTION_UNIT_RUBRIC,
    FGS_OUTPUT_JSON_SCHEMA,
    RESCUE_ANALGESIA_THRESHOLD,
)

STANDARD_DISCLAIMER = (
    "This prototype is triage support only and is not a veterinary diagnosis. "
    "If the cat appears distressed, injured, unusually quiet, not eating, hiding, "
    "limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly."
)

FGS_JSON_INSTRUCTION = f"""
You are assisting with feline acute pain triage from an image.
Return only JSON. Do not diagnose. Score visible Feline Grimace Scale action units.
If an action unit is not visible, mark visible=false and use score=null.
Use these action units exactly: ear_position, orbital_tightening, muzzle_tension,
whiskers_change, head_position.
Scores are 0 absent, 1 moderate/uncertain, 2 obvious.
Compute total_raw as the sum only if all five action units are visible.
Compute total_normalized as total_raw / 10.
Use rescue_threshold_positive=true only if total_normalized > {RESCUE_ANALGESIA_THRESHOLD}.
Every action unit must include visible, score, evidence, and uncertainty.
""".strip()


FGS_RUBRIC_TEXT = "\n".join(
    f"- {name.value}: 0={levels[0]} 1={levels[1]} 2={levels[2]}"
    for name, levels in ACTION_UNIT_RUBRIC.items()
)


FGS_CALIBRATION_TEXT = """
Calibration guidance for avoiding all-zero under-calling:
- Score 0 only when the visible cue clearly looks relaxed/absent.
- Score 1 when the cue is partly changed, mildly tense, or ambiguous but not fully relaxed.
- Score 2 when the cue is clearly changed in the pain/grimace direction.
- If a visible cue is uncertain between 0 and 1, choose 1 and mark uncertainty=medium instead of defaulting to 0.
- If several facial cues are ambiguous in the pain direction, avoid an all-zero total unless the image strongly supports relaxed cues across the whole face.
- Do not require dramatic illness, injury, vocalization, or body posture to score facial action units.
- Before returning all five scores as 0, verify that the ears, eyelids, muzzle, whiskers, and head position each independently support a relaxed score.
- If the cat face is visible but the cue is genuinely hard to assess, use visible=false and score=null rather than defaulting to 0.
""".strip()


FGS_RESPONSE_TEMPLATE: dict[str, Any] = {
    "action_units": {
        "ear_position": {
            "score": 0,
            "visible": True,
            "evidence": "Ears appear forward and relaxed.",
            "uncertainty": "low",
        },
        "orbital_tightening": {
            "score": 0,
            "visible": True,
            "evidence": "Eyes appear open with relaxed eyelids.",
            "uncertainty": "low",
        },
        "muzzle_tension": {
            "score": 1,
            "visible": True,
            "evidence": "Muzzle shape is partially tense, but the image angle limits confidence.",
            "uncertainty": "medium",
        },
        "whiskers_change": {
            "score": None,
            "visible": False,
            "evidence": "Whisker position is not clearly visible in this image.",
            "uncertainty": "high",
        },
        "head_position": {
            "score": 0,
            "visible": True,
            "evidence": "Head appears upright relative to the visible shoulders.",
            "uncertainty": "medium",
        },
    },
    "total_raw": None,
    "total_normalized": None,
    "rescue_threshold_positive": None,
    "uncertainty": "high",
    "recommendation": "Cannot compute a full score because one or more action units are not visible. Recheck with a clear, awake, front-facing image; contact a veterinarian if concerning behavior persists.",
    "disclaimer": STANDARD_DISCLAIMER,
}


def build_fgs_prompt(extra_context: str | None = None) -> str:
    """Build the strict text prompt sent alongside the cat image."""
    context = f"\nAdditional context from user: {extra_context.strip()}\n" if extra_context else ""
    return f"""
{FGS_JSON_INSTRUCTION}

Rubric:
{FGS_RUBRIC_TEXT}

{FGS_CALIBRATION_TEXT}

Output contract:
- Return exactly one JSON object and no markdown.
- Use the JSON keys shown in the template exactly.
- Evidence must describe visible image details, not assumptions about disease.
- If the image is not a cat, no cat face is visible, the cat is asleep/grooming, or key regions are occluded, set visible=false for affected action units and use high uncertainty.
- `total_raw`, `total_normalized`, and `rescue_threshold_positive` must be null unless all five action units are visible and scored.
- If all five scores are visible, `total_raw` must equal their sum and `total_normalized` must equal `total_raw / 10` rounded to two decimals.
- `recommendation` must be one of: low visible concern, monitor closely, contact a veterinarian, cannot assess.
- Always include this disclaimer verbatim: {STANDARD_DISCLAIMER!r}
{context}
JSON schema:
{json.dumps(FGS_OUTPUT_JSON_SCHEMA, indent=2)}

Example shape only, not an answer for the current image:
{json.dumps(FGS_RESPONSE_TEMPLATE, indent=2)}
""".strip()


def build_gemma4_messages(image: Any, extra_context: str | None = None) -> list[dict[str, Any]]:
    """Build Gemma 4 multimodal chat messages for Transformers processors.

    The pulled Kaggle notebook uses messages where image content is a PIL image
    and the same image is passed to `processor(..., images=image)`.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": build_fgs_prompt(extra_context)},
            ],
        }
    ]

