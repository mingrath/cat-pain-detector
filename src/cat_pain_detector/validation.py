"""Validation utilities for FGS-labeled baseline runs."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cat_pain_detector.feline_grimace_scale import ActionUnitName, RESCUE_ANALGESIA_THRESHOLD


@dataclass(frozen=True)
class ValidationExample:
    image_path: Path
    labels: dict[str, int]
    total_raw: int
    total_normalized: float
    rescue_threshold_positive: bool
    source: str = "unknown"
    license: str = "unknown"
    notes: str = ""


def load_validation_manifest(path: str | Path) -> list[ValidationExample]:
    manifest_path = Path(path)
    examples: list[ValidationExample] = []
    with manifest_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            labels = {unit.value: int(row[unit.value]) for unit in ActionUnitName}
            total_raw = int(row.get("total_raw") or sum(labels.values()))
            total_normalized = float(row.get("total_normalized") or (total_raw / 10.0))
            rescue = _parse_bool(row.get("rescue_threshold_positive"))
            image_path = Path(row["image_path"])
            if not image_path.is_absolute():
                parent_relative = manifest_path.parent / image_path
                image_path = parent_relative if parent_relative.exists() else Path.cwd() / image_path
            examples.append(
                ValidationExample(
                    image_path=image_path.resolve(),
                    labels=labels,
                    total_raw=total_raw,
                    total_normalized=total_normalized,
                    rescue_threshold_positive=rescue,
                    source=row.get("source", "unknown"),
                    license=row.get("license", "unknown"),
                    notes=row.get("notes", ""),
                )
            )
    return examples


def _parse_bool(value: str | None) -> bool:
    if value is None:
        raise ValueError("Missing boolean value")
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute total-score, threshold, and per-action-unit metrics."""
    if not rows:
        raise ValueError("Cannot compute metrics for empty validation results")

    true_norm = [float(row["true_total_normalized"]) for row in rows]
    pred_norm = [float(row["pred_total_normalized"]) for row in rows if row["pred_total_normalized"] is not None]
    comparable_rows = [row for row in rows if row["pred_total_normalized"] is not None]

    if comparable_rows:
        abs_errors = [
            abs(float(row["pred_total_normalized"]) - float(row["true_total_normalized"]))
            for row in comparable_rows
        ]
        sq_errors = [err * err for err in abs_errors]
        total_score_metrics: dict[str, Any] = {
            "count": len(comparable_rows),
            "coverage": len(comparable_rows) / len(rows),
            "mae_normalized": sum(abs_errors) / len(abs_errors),
            "rmse_normalized": math.sqrt(sum(sq_errors) / len(sq_errors)),
        }
    else:
        total_score_metrics = {
            "count": 0,
            "coverage": 0.0,
            "mae_normalized": None,
            "rmse_normalized": None,
        }

    threshold_metrics = compute_binary_metrics(
        [bool(row["true_rescue_threshold_positive"]) for row in comparable_rows],
        [bool(row["pred_rescue_threshold_positive"]) for row in comparable_rows],
    ) if comparable_rows else compute_binary_metrics([], [])

    per_au: dict[str, Any] = {}
    for unit in ActionUnitName:
        unit_rows = [row for row in rows if row.get(f"pred_{unit.value}") is not None]
        if not unit_rows:
            per_au[unit.value] = {"count": 0, "coverage": 0.0, "accuracy": None, "mae": None}
            continue
        exact = [int(row[f"pred_{unit.value}"]) == int(row[f"true_{unit.value}"]) for row in unit_rows]
        errors = [abs(int(row[f"pred_{unit.value}"]) - int(row[f"true_{unit.value}"])) for row in unit_rows]
        per_au[unit.value] = {
            "count": len(unit_rows),
            "coverage": len(unit_rows) / len(rows),
            "accuracy": sum(exact) / len(exact),
            "mae": sum(errors) / len(errors),
        }

    return {
        "n_examples": len(rows),
        "threshold": RESCUE_ANALGESIA_THRESHOLD,
        "total_score": total_score_metrics,
        "rescue_threshold": threshold_metrics,
        "per_action_unit": per_au,
        "notes": [
            "Metrics are valid only for the stated validation manifest.",
            "Rows where the model could not compute a total score count against coverage.",
        ],
    }


def compute_binary_metrics(y_true: list[bool], y_pred: list[bool]) -> dict[str, Any]:
    if not y_true:
        return {
            "count": 0,
            "accuracy": None,
            "precision": None,
            "recall_sensitivity": None,
            "specificity": None,
            "f1": None,
            "confusion_matrix": {"tn": 0, "fp": 0, "fn": 0, "tp": 0},
        }
    tp = sum(t and p for t, p in zip(y_true, y_pred))
    tn = sum((not t) and (not p) for t, p in zip(y_true, y_pred))
    fp = sum((not t) and p for t, p in zip(y_true, y_pred))
    fn = sum(t and (not p) for t, p in zip(y_true, y_pred))
    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    specificity = _safe_div(tn, tn + fp)
    f1 = _safe_div(2 * precision * recall, precision + recall) if precision is not None and recall is not None else None
    return {
        "count": len(y_true),
        "accuracy": (tp + tn) / len(y_true),
        "precision": precision,
        "recall_sensitivity": recall,
        "specificity": specificity,
        "f1": f1,
        "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    }


def _safe_div(num: float, den: float) -> float | None:
    return None if den == 0 else num / den

