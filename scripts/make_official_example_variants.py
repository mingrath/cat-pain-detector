#!/usr/bin/env python3
"""Create crop/framing variants for the three official FGS smoke examples.

These images are reference-only and not redistributable training data. Outputs go
under data/processed/ so they are ignored by git.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from PIL import Image, ImageChops  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/fgs_official_examples_manifest.csv")
    parser.add_argument("--output-dir", default="data/processed/fgs_official_variants")
    parser.add_argument("--output-manifest", default="data/processed/fgs_official_variants_manifest.csv")
    args = parser.parse_args()

    manifest_path = PROJECT_ROOT / args.manifest
    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_manifest = PROJECT_ROOT / args.output_manifest
    output_manifest.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    with manifest_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            src = PROJECT_ROOT / row["image_path"]
            img = Image.open(src).convert("RGB")
            stem = src.stem

            variants = {
                "cat_only": img,
                "tight_content": crop_non_background(img),
                "padded_square": padded_square(img),
            }
            for variant_name, variant_img in variants.items():
                out_path = output_dir / f"{stem}_{variant_name}.png"
                variant_img.save(out_path)
                out_row = dict(row)
                out_row["image_path"] = str(out_path.relative_to(PROJECT_ROOT))
                out_row["notes"] = f"{row.get('notes', '')} Variant: {variant_name}. Reference-only smoke/calibration image."
                out_row["variant"] = variant_name
                rows.append(out_row)

    fieldnames = list(rows[0].keys())
    with output_manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(output_manifest)
    return 0


def crop_non_background(img: Image.Image, padding_ratio: float = 0.08) -> Image.Image:
    """Crop away mostly-white margins, retaining padding around visible content."""
    bg = Image.new("RGB", img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg).convert("L")
    # Keep pixels that differ enough from the corner background.
    mask = diff.point(lambda value: 255 if value > 20 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return img.copy()
    x1, y1, x2, y2 = bbox
    pad_x = int((x2 - x1) * padding_ratio)
    pad_y = int((y2 - y1) * padding_ratio)
    crop = (
        max(0, x1 - pad_x),
        max(0, y1 - pad_y),
        min(img.width, x2 + pad_x),
        min(img.height, y2 + pad_y),
    )
    return img.crop(crop)


def padded_square(img: Image.Image, fill: tuple[int, int, int] = (250, 250, 250)) -> Image.Image:
    side = max(img.width, img.height)
    canvas = Image.new("RGB", (side, side), fill)
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    return canvas


if __name__ == "__main__":
    raise SystemExit(main())
