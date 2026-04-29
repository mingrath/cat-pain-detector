"""Feline Grimace Scale schema and scoring helpers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


RESCUE_ANALGESIA_THRESHOLD = 0.39


class ActionUnitName(str, Enum):
    EAR_POSITION = "ear_position"
    ORBITAL_TIGHTENING = "orbital_tightening"
    MUZZLE_TENSION = "muzzle_tension"
    WHISKERS_CHANGE = "whiskers_change"
    HEAD_POSITION = "head_position"


ACTION_UNIT_LABELS: dict[ActionUnitName, str] = {
    ActionUnitName.EAR_POSITION: "Ear position",
    ActionUnitName.ORBITAL_TIGHTENING: "Orbital tightening",
    ActionUnitName.MUZZLE_TENSION: "Muzzle tension",
    ActionUnitName.WHISKERS_CHANGE: "Whiskers change",
    ActionUnitName.HEAD_POSITION: "Head position",
}


ACTION_UNIT_RUBRIC: dict[ActionUnitName, dict[int, str]] = {
    ActionUnitName.EAR_POSITION: {
        0: "Ears forward and relaxed.",
        1: "Ears slightly pulled apart or mildly rotated outward.",
        2: "Ears flattened, rotated outward, or held far apart.",
    },
    ActionUnitName.ORBITAL_TIGHTENING: {
        0: "Eyes open with relaxed eyelids.",
        1: "Partial eyelid narrowing or mild squinting.",
        2: "Marked orbital tightening, squinting, or eyes nearly closed while awake.",
    },
    ActionUnitName.MUZZLE_TENSION: {
        0: "Muzzle appears relaxed and rounded.",
        1: "Mild muzzle tension or shape change.",
        2: "Marked muzzle tension, flattening, or pronounced angular shape.",
    },
    ActionUnitName.WHISKERS_CHANGE: {
        0: "Whiskers relaxed and naturally curved.",
        1: "Whiskers mildly straightened or shifted.",
        2: "Whiskers straight, stiff, bunched, or visibly pulled forward/back.",
    },
    ActionUnitName.HEAD_POSITION: {
        0: "Head held above shoulder line in a normal alert posture.",
        1: "Head approximately aligned with shoulder line or mildly lowered.",
        2: "Head clearly below shoulder line or tucked downward while awake.",
    },
}


@dataclass(frozen=True)
class ActionUnitScore:
    name: ActionUnitName
    score: int | None
    visible: bool
    evidence: str
    uncertainty: str = "medium"

    def validate(self) -> None:
        if self.score is not None and self.score not in (0, 1, 2):
            raise ValueError(f"{self.name.value} score must be 0, 1, 2, or None")
        if not self.visible and self.score is not None:
            raise ValueError(f"{self.name.value} score must be None when visible=false")


@dataclass(frozen=True)
class FGSAssessment:
    action_units: dict[ActionUnitName, ActionUnitScore]
    uncertainty: str
    recommendation: str
    disclaimer: str

    @property
    def visible_scores(self) -> list[int]:
        return [au.score for au in self.action_units.values() if au.visible and au.score is not None]

    @property
    def total_raw(self) -> int | None:
        if len(self.visible_scores) != len(ActionUnitName):
            return None
        return sum(self.visible_scores)

    @property
    def total_normalized(self) -> float | None:
        if self.total_raw is None:
            return None
        return self.total_raw / 10.0

    @property
    def rescue_threshold_positive(self) -> bool | None:
        if self.total_normalized is None:
            return None
        return self.total_normalized > RESCUE_ANALGESIA_THRESHOLD

    def validate(self) -> None:
        missing = set(ActionUnitName) - set(self.action_units)
        if missing:
            raise ValueError(f"Missing action units: {sorted(m.value for m in missing)}")
        for score in self.action_units.values():
            score.validate()

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "action_units": {
                name.value: {
                    "score": score.score,
                    "visible": score.visible,
                    "evidence": score.evidence,
                    "uncertainty": score.uncertainty,
                    "rubric": ACTION_UNIT_RUBRIC[name].get(score.score)
                    if score.score is not None
                    else None,
                }
                for name, score in self.action_units.items()
            },
            "total_raw": self.total_raw,
            "total_normalized": self.total_normalized,
            "rescue_threshold_positive": self.rescue_threshold_positive,
            "uncertainty": self.uncertainty,
            "recommendation": self.recommendation,
            "disclaimer": self.disclaimer,
        }


def normalize_score(total_raw: int) -> float:
    if not 0 <= total_raw <= 10:
        raise ValueError("total_raw must be in range 0..10")
    return total_raw / 10.0


def exceeds_rescue_threshold(total_normalized: float) -> bool:
    if not 0.0 <= total_normalized <= 1.0:
        raise ValueError("total_normalized must be in range 0..1")
    return total_normalized > RESCUE_ANALGESIA_THRESHOLD


FGS_OUTPUT_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "action_units",
        "total_raw",
        "total_normalized",
        "rescue_threshold_positive",
        "uncertainty",
        "recommendation",
        "disclaimer",
    ],
    "properties": {
        "action_units": {
            "type": "object",
            "required": [unit.value for unit in ActionUnitName],
            "additionalProperties": False,
            "properties": {
                unit.value: {
                    "type": "object",
                    "required": ["score", "visible", "evidence", "uncertainty"],
                    "additionalProperties": False,
                    "properties": {
                        "score": {"type": ["integer", "null"], "enum": [0, 1, 2, None]},
                        "visible": {"type": "boolean"},
                        "evidence": {"type": "string"},
                        "uncertainty": {"type": "string", "enum": ["low", "medium", "high"]},
                    },
                }
                for unit in ActionUnitName
            },
        },
        "total_raw": {"type": ["integer", "null"], "minimum": 0, "maximum": 10},
        "total_normalized": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "rescue_threshold_positive": {"type": ["boolean", "null"]},
        "uncertainty": {"type": "string", "enum": ["low", "medium", "high"]},
        "recommendation": {"type": "string"},
        "disclaimer": {"type": "string"},
    },
}

