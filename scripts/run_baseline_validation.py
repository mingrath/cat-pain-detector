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
    parser.add_argument("--review-output", default=None, help="Optional Markdown error-review report path")
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
                "source": example.source,
                "license": example.license,
                "notes": example.notes,
                "true_total_raw": example.total_raw,
                "true_total_normalized": example.total_normalized,
                "true_rescue_threshold_positive": example.rescue_threshold_positive,
                "pred_total_raw": parsed["total_raw"],
                "pred_total_normalized": parsed["total_normalized"],
                "pred_rescue_threshold_positive": parsed["rescue_threshold_positive"],
                "pred_uncertainty": parsed.get("uncertainty"),
                "pred_recommendation": parsed.get("recommendation"),
                "raw_text": result.raw_text,
            }
            for unit in ActionUnitName:
                row[f"true_{unit.value}"] = example.labels[unit.value]
                row[f"pred_{unit.value}"] = parsed["action_units"][unit.value]["score"]
                row[f"pred_{unit.value}_visible"] = parsed["action_units"][unit.value]["visible"]
                row[f"pred_{unit.value}_uncertainty"] = parsed["action_units"][unit.value]["uncertainty"]
                row[f"pred_{unit.value}_evidence"] = parsed["action_units"][unit.value]["evidence"]
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
    review_path = PROJECT_ROOT / args.review_output if args.review_output else out_path.with_suffix(".review.md")
    review_path.write_text(_build_review_markdown(output))
    print(out_path)
    print(review_path)
    return 0 if rows else 1


def _build_review_markdown(output: dict) -> str:
    lines = [
        "# Baseline Error Review",
        "",
        f"Created: {output['created_at']}",
        f"Manifest: `{output['manifest']}`",
        f"Rows: {output['result_count']} successful, {output['failure_count']} failed",
        "",
        "This report is for manual debugging. It is not a clinical validation claim.",
        "",
    ]
    metrics = output.get("metrics")
    if metrics:
        lines.extend([
            "## Metric Snapshot",
            "",
            f"- Total normalized MAE: {metrics['total_score'].get('mae_normalized')}",
            f"- Rescue threshold accuracy: {metrics['rescue_threshold'].get('accuracy')}",
            f"- Rescue threshold recall: {metrics['rescue_threshold'].get('recall_sensitivity')}",
            f"- Confusion matrix: `{metrics['rescue_threshold'].get('confusion_matrix')}`",
            "",
        ])
    if output.get("failures"):
        lines.extend(["## Failures", ""])
        for failure in output["failures"]:
            lines.extend([f"- `{failure['image_path']}`: {failure['error']}", ""])
    lines.extend(["## Row Review", ""])
    for i, row in enumerate(output.get("rows", []), start=1):
        pred_scores = [row.get(f"pred_{unit.value}") for unit in ActionUnitName]
        true_scores = [row.get(f"true_{unit.value}") for unit in ActionUnitName]
        all_zero_collapse = any(int(v) > 0 for v in true_scores) and all(v == 0 for v in pred_scores)
        lines.extend([
            f"### {i}. `{Path(row['image_path']).name}`",
            "",
            f"Image: `{row['image_path']}`",
            f"True total: `{row['true_total_raw']}` / normalized `{row['true_total_normalized']}` / threshold `{row['true_rescue_threshold_positive']}`",
            f"Pred total: `{row['pred_total_raw']}` / normalized `{row['pred_total_normalized']}` / threshold `{row['pred_rescue_threshold_positive']}`",
            f"Prediction uncertainty: `{row.get('pred_uncertainty')}`",
            f"Recommendation: `{row.get('pred_recommendation')}`",
            f"Failure flags: `all_zero_collapse={all_zero_collapse}`",
            "",
            "| Action unit | True | Pred | Visible | Uncertainty | Evidence |",
            "|---|---:|---:|---|---|---|",
        ])
        for unit in ActionUnitName:
            evidence = str(row.get(f"pred_{unit.value}_evidence", "")).replace("|", "\\|")
            lines.append(
                f"| {unit.value} | {row.get(f'true_{unit.value}')} | {row.get(f'pred_{unit.value}')} | "
                f"{row.get(f'pred_{unit.value}_visible')} | {row.get(f'pred_{unit.value}_uncertainty')} | {evidence} |"
            )
        lines.extend(["", "<details><summary>Raw model text</summary>", "", "```json", str(row.get("raw_text", "")), "```", "", "</details>", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

