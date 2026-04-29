#!/usr/bin/env python3
"""Run a Gemma/mock baseline against an FGS-labeled validation manifest."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from PIL import Image  # noqa: E402

from cat_pain_detector.feline_grimace_scale import ActionUnitName  # noqa: E402
from cat_pain_detector.model_runner import runner_from_env  # noqa: E402
from cat_pain_detector.prompts import build_fgs_prompt  # noqa: E402
from cat_pain_detector.validation import compute_metrics, load_validation_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="CSV with image paths and FGS labels")
    parser.add_argument("--output", default="metrics/baseline_metrics.json")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    examples = load_validation_manifest(args.manifest)
    if args.limit:
        examples = examples[: args.limit]
    if not examples:
        raise SystemExit("Validation manifest is empty")

    runner = runner_from_env()
    rows = []
    failures = []
    for index, example in enumerate(examples):
        try:
            image = Image.open(example.image_path).convert("RGB")
            result = runner.analyze(
                image=image,
                prompt=build_fgs_prompt(f"Validation image {index}. Return strict JSON only."),
            )
            parsed = result.parsed
            row = {
                "image_path": str(example.image_path),
                "backend": result.backend,
                "true_total_raw": example.total_raw,
                "true_total_normalized": example.total_normalized,
                "true_rescue_threshold_positive": example.rescue_threshold_positive,
                "pred_total_raw": parsed["total_raw"],
                "pred_total_normalized": parsed["total_normalized"],
                "pred_rescue_threshold_positive": parsed["rescue_threshold_positive"],
            }
            for unit in ActionUnitName:
                row[f"true_{unit.value}"] = example.labels[unit.value]
                row[f"pred_{unit.value}"] = parsed["action_units"][unit.value]["score"]
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - record every model/data failure.
            failures.append({"image_path": str(example.image_path), "error": str(exc)})

    output = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(Path(args.manifest).resolve()),
        "result_count": len(rows),
        "failure_count": len(failures),
        "metrics": compute_metrics(rows) if rows else None,
        "rows": rows,
        "failures": failures,
    }
    out_path = PROJECT_ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2))
    print(out_path)
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())

