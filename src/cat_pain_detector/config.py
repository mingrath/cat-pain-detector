"""Project configuration constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
METRICS_DIR = PROJECT_ROOT / "metrics"
MODELS_DIR = PROJECT_ROOT / "models"

