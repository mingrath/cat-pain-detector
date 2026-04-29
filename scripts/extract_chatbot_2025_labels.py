#!/usr/bin/env python3
"""Extract public expert FGS total-ratio labels from Ngai et al. 2025 supplement.

The supplementary workbook contains image IDs and expert gold-standard total FGS
ratios, but not the underlying cat images. This creates a label-only CSV for data
inventory and request matching; it is not directly usable as a vision validation
manifest until images are obtained with permission.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", default="data/public_fgs_chatbot_2025/raw/supplementary_material_1.xlsx")
    parser.add_argument("--output", default="data/public_fgs_chatbot_2025/expert_gs_total_labels.csv")
    args = parser.parse_args()

    xlsx = PROJECT_ROOT / args.xlsx
    output = PROJECT_ROOT / args.output
    df = pd.read_excel(xlsx, sheet_name="Expert rater (GS)")
    df = df.rename(columns={"Image ID": "image_id", "GS": "expert_total_normalized"})
    df["expert_total_raw_estimated"] = df["expert_total_normalized"] * 10.0
    df["rescue_threshold_positive"] = df["expert_total_normalized"] > 0.39
    df["source"] = "Ngai et al. 2025 Scientific Reports supplementary material 1"
    df["doi"] = "10.1038/s41598-025-27404-z"
    df["image_available_locally"] = False
    df["notes"] = "Label-only public supplement; underlying raw cat images are not in the XLSX."
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(output)
    print(df.head().to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
