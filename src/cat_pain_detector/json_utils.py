"""Utilities for extracting model JSON from fenced or noisy text."""

from __future__ import annotations

import json
import re
from typing import Any

from cat_pain_detector.feline_grimace_scale import (
    ActionUnitName,
    RESCUE_ANALGESIA_THRESHOLD,
)


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract the first JSON object from raw model text.

    Handles plain JSON and fenced ```json blocks. Raises ValueError if parsing
    fails so callers can store the raw response for debugging.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in model output")
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("Model JSON output must be an object")
    return parsed


def validate_fgs_response(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a Gemma FGS JSON response.

    Raises ValueError with actionable messages so validation scripts can store
    failure modes. Returns the original payload if valid.
    """
    required = {
        "action_units",
        "total_raw",
        "total_normalized",
        "rescue_threshold_positive",
        "uncertainty",
        "recommendation",
        "disclaimer",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"FGS response missing required keys: {sorted(missing)}")
    if payload["uncertainty"] not in {"low", "medium", "high"}:
        raise ValueError("uncertainty must be low, medium, or high")
    if not isinstance(payload["recommendation"], str):
        raise ValueError("recommendation must be a string")
    if not isinstance(payload["disclaimer"], str):
        raise ValueError("disclaimer must be a string")
    if not isinstance(payload["action_units"], dict):
        raise ValueError("action_units must be an object")

    action_units = payload["action_units"]
    scores: list[int] = []
    all_visible = True
    missing_units = {unit.value for unit in ActionUnitName} - set(action_units)
    if missing_units:
        raise ValueError(f"Missing action units: {sorted(missing_units)}")
    for unit in ActionUnitName:
        item = action_units[unit.value]
        if not isinstance(item, dict):
            raise ValueError(f"{unit.value}: action unit entry must be an object")
        for key in ("score", "visible", "evidence", "uncertainty"):
            if key not in item:
                raise ValueError(f"{unit.value}: missing required key {key}")
        score = item["score"]
        visible = item["visible"]
        if not isinstance(visible, bool):
            raise ValueError(f"{unit.value}: visible must be boolean")
        if score not in (0, 1, 2, None):
            raise ValueError(f"{unit.value}: score must be 0, 1, 2, or null")
        if not isinstance(item["evidence"], str) or not item["evidence"].strip():
            raise ValueError(f"{unit.value}: evidence must be a non-empty string")
        if item["uncertainty"] not in {"low", "medium", "high"}:
            raise ValueError(f"{unit.value}: uncertainty must be low, medium, or high")
        if not visible:
            all_visible = False
            if score is not None:
                raise ValueError(f"{unit.value}: score must be null when visible=false")
            continue
        if score is None:
            raise ValueError(f"{unit.value}: score is required when visible=true")
        scores.append(score)

    if all_visible:
        expected_total = sum(scores)
        if payload["total_raw"] != expected_total:
            raise ValueError(f"total_raw must equal sum of AU scores ({expected_total})")
        expected_normalized = round(expected_total / 10.0, 2)
        if round(float(payload["total_normalized"]), 2) != expected_normalized:
            raise ValueError(f"total_normalized must equal {expected_normalized}")
        expected_threshold = expected_normalized > RESCUE_ANALGESIA_THRESHOLD
        if payload["rescue_threshold_positive"] != expected_threshold:
            raise ValueError(f"rescue_threshold_positive must equal {expected_threshold}")
    else:
        if payload["total_raw"] is not None:
            raise ValueError("total_raw must be null when any action unit is not visible")
        if payload["total_normalized"] is not None:
            raise ValueError("total_normalized must be null when any action unit is not visible")
        if payload["rescue_threshold_positive"] is not None:
            raise ValueError("rescue_threshold_positive must be null when any action unit is not visible")

    return payload


def parse_fgs_model_output(text: str) -> dict[str, Any]:
    """Extract and validate a model response as FGS JSON."""
    return validate_fgs_response(extract_json_object(text))

