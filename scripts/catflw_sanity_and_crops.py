#!/usr/bin/env python3
"""Create a CatFLW landmark sanity report and standardized face crops.

CatFLW is not pain-labeled. This script validates only image/landmark/bbox
loading and prepares crops for later visual-quality and region-localization work.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from PIL import Image  # noqa: E402


@dataclass
class CatFLWRow:
    image_path: Path
    label_path: Path
    crop_path: Path
    width: int
    height: int
    bbox_x1: float
    bbox_y1: float
    bbox_x2: float
    bbox_y2: float
    bbox_width: float
    bbox_height: float
    landmark_count: int
    valid: bool
    error: str = ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catflw-root", default="data/raw/catflw/CatFLW dataset")
    parser.add_argument("--output-dir", default="data/processed/catflw_face_crops")
    parser.add_argument("--manifest-output", default="data/processed/catflw_face_crops_manifest.csv")
    parser.add_argument("--report-output", default="metrics/catflw_sanity_report.md")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--padding", type=float, default=0.20)
    args = parser.parse_args()

    root = PROJECT_ROOT / args.catflw_root
    image_dir = root / "images"
    label_dir = root / "labels"
    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[CatFLWRow] = []
    for label_path in sorted(label_dir.glob("*.json"))[: args.limit]:
        image_path = image_dir / f"{label_path.stem}.png"
        crop_path = output_dir / f"{label_path.stem}_face_padded.png"
        try:
            row = process_one(image_path, label_path, crop_path, args.padding)
        except Exception as exc:  # noqa: BLE001 - this is a data-quality report.
            row = CatFLWRow(image_path, label_path, crop_path, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, str(exc))
        rows.append(row)

    manifest_path = PROJECT_ROOT / args.manifest_output
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    write_manifest(rows, manifest_path)

    report_path = PROJECT_ROOT / args.report_output
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(rows, manifest_path, output_dir))
    print(report_path)
    print(manifest_path)
    return 0 if any(row.valid for row in rows) else 1


def process_one(image_path: Path, label_path: Path, crop_path: Path, padding: float) -> CatFLWRow:
    if not image_path.exists():
        raise FileNotFoundError(f"Missing image for label: {image_path}")
    label = json.loads(label_path.read_text())
    landmarks = label.get("labels")
    bbox = label.get("bounding_boxes")
    if not isinstance(landmarks, list):
        raise ValueError("labels must be a list")
    if len(landmarks) != 48:
        raise ValueError(f"expected 48 landmarks, found {len(landmarks)}")
    if not isinstance(bbox, list) or len(bbox) != 4:
        raise ValueError("bounding_boxes must be [x1, y1, x2, y2]")
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size
        x1, y1, x2, y2 = [float(v) for v in bbox]
        bw, bh = x2 - x1, y2 - y1
        if bw <= 1 or bh <= 1:
            raise ValueError(f"invalid bbox size {bw}x{bh}")
        pad_x, pad_y = bw * padding, bh * padding
        crop_box = (
            max(0, int(round(x1 - pad_x))),
            max(0, int(round(y1 - pad_y))),
            min(width, int(round(x2 + pad_x))),
            min(height, int(round(y2 + pad_y))),
        )
        img.crop(crop_box).save(crop_path)
    return CatFLWRow(image_path, label_path, crop_path, width, height, x1, y1, x2, y2, bw, bh, len(landmarks), True)


def write_manifest(rows: list[CatFLWRow], path: Path) -> None:
    fieldnames = list(CatFLWRow.__dataclass_fields__.keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(getattr(row, key)) for key in fieldnames})


def build_report(rows: list[CatFLWRow], manifest_path: Path, output_dir: Path) -> str:
    valid = [row for row in rows if row.valid]
    invalid = [row for row in rows if not row.valid]
    manifest_display = manifest_path.relative_to(PROJECT_ROOT) if manifest_path.is_relative_to(PROJECT_ROOT) else manifest_path
    output_display = output_dir.relative_to(PROJECT_ROOT) if output_dir.is_relative_to(PROJECT_ROOT) else output_dir
    lines = [
        "# CatFLW Landmark Sanity and Crop Report",
        "",
        "CatFLW has landmarks only; this does not validate pain scoring.",
        "",
        f"Rows checked: {len(rows)}",
        f"Valid rows: {len(valid)}",
        f"Invalid rows: {len(invalid)}",
        f"Crop output dir: `{output_display}`",
        f"Manifest: `{manifest_display}`",
        "",
    ]
    if valid:
        lines.extend([
            "## BBox Summary",
            "",
            f"- Mean bbox width: {mean(row.bbox_width for row in valid):.1f}px",
            f"- Mean bbox height: {mean(row.bbox_height for row in valid):.1f}px",
            f"- Landmark count: {sorted(set(row.landmark_count for row in valid))}",
            "",
        ])
    if invalid:
        lines.extend(["## Invalid Rows", ""])
        for row in invalid[:20]:
            lines.append(f"- `{row.label_path}`: {row.error}")
        lines.append("")
    lines.extend(["## Sample Crops", ""])
    for row in valid[:10]:
        rel = row.crop_path.relative_to(PROJECT_ROOT) if row.crop_path.is_relative_to(PROJECT_ROOT) else row.crop_path
        lines.append(f"- `{rel}` from `{row.image_path.name}` bbox=({row.bbox_x1:.0f},{row.bbox_y1:.0f},{row.bbox_x2:.0f},{row.bbox_y2:.0f})")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
