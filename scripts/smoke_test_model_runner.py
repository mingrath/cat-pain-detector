#!/usr/bin/env python3
"""Smoke-test the configured model runner.

Default mode uses the mock runner so this can run on any machine. With
`CAT_PAIN_RUNNER=transformers` or `http`, it exercises the real backend.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from PIL import Image, ImageDraw  # noqa: E402

from cat_pain_detector.model_runner import runner_from_env  # noqa: E402
from cat_pain_detector.prompts import build_fgs_prompt  # noqa: E402


def load_image(path: str | None) -> Image.Image:
    if path:
        return Image.open(path).convert("RGB")
    image = Image.new("RGB", (256, 256), color=(245, 245, 245))
    draw = ImageDraw.Draw(image)
    draw.ellipse((72, 72, 184, 184), fill=(180, 140, 100), outline=(80, 60, 40), width=3)
    draw.polygon([(92, 86), (112, 42), (128, 92)], fill=(180, 140, 100), outline=(80, 60, 40))
    draw.polygon([(128, 92), (144, 42), (164, 86)], fill=(180, 140, 100), outline=(80, 60, 40))
    draw.ellipse((105, 115, 120, 128), fill=(20, 20, 20))
    draw.ellipse((136, 115, 151, 128), fill=(20, 20, 20))
    draw.polygon([(128, 136), (120, 148), (136, 148)], fill=(70, 40, 40))
    return image


def main() -> int:
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    image = load_image(image_path)
    runner = runner_from_env()
    result = runner.analyze(
        image=image,
        prompt=build_fgs_prompt("Smoke test image. Return strict JSON only."),
    )
    print(json.dumps({"backend": result.backend, "parsed": result.parsed, "metadata": result.metadata}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

