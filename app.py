"""Gradio entrypoint for Cat Pain Detector."""

from __future__ import annotations

import sys
import os
from html import escape
from functools import lru_cache
from pathlib import Path
from typing import Any

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cat_pain_detector.feline_grimace_scale import ACTION_UNIT_LABELS, ActionUnitName  # noqa: E402
from cat_pain_detector.model_runner import runner_from_env  # noqa: E402
from cat_pain_detector.prompts import STANDARD_DISCLAIMER, build_fgs_prompt  # noqa: E402


BASELINE_NOTE = (
    "Measured smoke baseline: Gemma 4 ran on 3 official FGS educational examples "
    "with 3/3 parse success, but under-called pain (normalized MAE 0.50; "
    "rescue-threshold accuracy 0.333). This is not a clinical accuracy claim."
)
SCORING_DISABLED_NOTE = (
    "Numeric FGS scoring is currently under recalibration after live testing showed "
    "the first Gemma 4 scores were not close enough. Use this screen as an FGS cue "
    "checklist only; do not use it for pain decisions."
)
SHOW_NUMERIC_SCORE = os.environ.get("CAT_PAIN_SHOW_NUMERIC_SCORE", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

DEMO_SAMPLE_PATHS = [
    str(path)
    for path in sorted((PROJECT_ROOT / "data" / "demo_samples" / "catflw").glob("*.png"))
]

APP_CSS = """
body { background: #FAFAFA; color: #0A0A0A; }
.gradio-container { max-width: 1280px !important; }
.hero-card, .safety-card, .validation-card, .report-shell {
  border: 1px solid #E8E8EC;
  border-radius: 12px;
  background: #FFFFFF;
  padding: 20px;
}
.hero-eyebrow { color: #6366F1; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.hero-title { font-size: 40px; line-height: 1.05; letter-spacing: -0.04em; margin: 8px 0; }
.hero-copy { color: #6B6B6B; font-size: 15px; max-width: 780px; }
.metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 14px 0; }
.metric-card { border: 1px solid #E8E8EC; border-radius: 12px; padding: 14px; background: #FAFAFA; }
.metric-label { color: #6B6B6B; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }
.metric-value { color: #0A0A0A; font-size: 24px; font-weight: 700; margin-top: 4px; }
.evidence-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 12px; }
.evidence-card { border: 1px solid #E8E8EC; border-radius: 12px; padding: 14px; background: #FFFFFF; }
.evidence-title { font-weight: 700; margin-bottom: 8px; }
.score-pill, .uncertainty-pill { display: inline-block; border-radius: 999px; padding: 3px 10px; font-size: 12px; font-weight: 700; margin-right: 6px; }
.score-pill { background: #EEF2FF; color: #4F46E5; }
.uncertainty-low { background: #D1FAE5; color: #065F46; }
.uncertainty-medium { background: #FEF3C7; color: #92400E; }
.uncertainty-high { background: #FEE2E2; color: #991B1B; }
.vet-next { border-left: 4px solid #6366F1; padding: 12px 14px; background: #F8FAFC; border-radius: 8px; }
"""


@lru_cache(maxsize=1)
def get_runner():
    """Cache the runner so the model is not reloaded on every click."""
    return runner_from_env()


def _format_score(value: Any) -> str:
    if value is None:
        return "not computed"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _recommendation_badge(recommendation: str) -> str:
    normalized = recommendation.lower().strip()
    if normalized == "contact a veterinarian":
        return "🔴 Contact a veterinarian"
    if normalized == "monitor closely":
        return "🟠 Monitor closely"
    if normalized == "low visible concern":
        return "🟢 Low visible concern"
    return "⚪ Cannot assess"


def _uncertainty_class(value: Any) -> str:
    normalized = str(value or "high").lower()
    if normalized not in {"low", "medium", "high"}:
        normalized = "high"
    return f"uncertainty-{normalized}"


def build_human_report(parsed: dict[str, Any], backend: str) -> str:
    total_normalized = parsed.get("total_normalized")
    rescue_positive = parsed.get("rescue_threshold_positive")
    recommendation = str(parsed.get("recommendation", "cannot assess"))

    lines = [
        '<div class="report-shell">',
        "<h2>Cat Pain Detector Report</h2>",
        f"<p><strong>Recommendation:</strong> {escape(_recommendation_badge(recommendation))}</p>",
        f'<div class="vet-next"><strong>Scoring status:</strong> {escape(SCORING_DISABLED_NOTE if not SHOW_NUMERIC_SCORE else "Numeric score display is enabled for internal validation.")}</div>',
        '<div class="metric-grid">',
        f'<div class="metric-card"><div class="metric-label">FGS total</div><div class="metric-value">{escape(_format_score(parsed.get("total_raw")) + " / 10" if SHOW_NUMERIC_SCORE else "hidden")}</div></div>',
        f'<div class="metric-card"><div class="metric-label">Normalized</div><div class="metric-value">{escape(_format_score(total_normalized) if SHOW_NUMERIC_SCORE else "hidden")}</div></div>',
        f'<div class="metric-card"><div class="metric-label">Threshold &gt; 0.39</div><div class="metric-value">{escape(_format_score(rescue_positive) if SHOW_NUMERIC_SCORE else "hidden")}</div></div>',
        f'<div class="metric-card"><div class="metric-label">Uncertainty</div><div class="metric-value">{escape(str(parsed.get("uncertainty", "unknown")))}</div></div>',
        "</div>",
        f"<p><strong>Model backend:</strong> <code>{escape(backend)}</code></p>",
        "<h3>Evidence by Feline Grimace Scale cue</h3>",
        '<div class="evidence-grid">',
    ]

    action_units = parsed.get("action_units", {})
    for unit in ActionUnitName:
        item = action_units.get(unit.value, {})
        label = ACTION_UNIT_LABELS[unit]
        uncertainty = item.get("uncertainty", "unknown")
        lines.append(
            '<div class="evidence-card">'
            f'<div class="evidence-title">{escape(label)}</div>'
            f'<span class="score-pill">Score {escape(_format_score(item.get("score")))}</span>'
            f'<span class="uncertainty-pill {_uncertainty_class(uncertainty)}">{escape(str(uncertainty))}</span>'
            f'<p><strong>Visible:</strong> {escape(str(item.get("visible")))}</p>'
            f'<p>{escape(str(item.get("evidence", "No evidence returned.")))}</p>'
            '</div>'
        )

    lines.extend(
        [
            "</div>",
            "<h3>Vet-safe next steps</h3>",
            '<div class="vet-next">Use this as a prompt to look more carefully, not as a diagnosis. '
            "If behavior, appetite, breathing, mobility, or comfort is concerning, contact a veterinarian.</div>",
            f"<p><strong>Safety note:</strong> {escape(str(parsed.get('disclaimer') or STANDARD_DISCLAIMER))}</p>",
            f"<p><strong>Validation note:</strong> {escape(BASELINE_NOTE)}</p>",
            "</div>",
        ]
    )
    return "\n".join(lines)


def analyze_image(image):
    if image is None:
        error = {
            "status": "error",
            "message": "Please upload a clear image of an awake cat face.",
            "disclaimer": STANDARD_DISCLAIMER,
        }
        return "Please upload a clear image of an awake cat face.", error

    try:
        runner = get_runner()
        result = runner.analyze(
            image=image,
            prompt=build_fgs_prompt("Demo upload. Return strict JSON only. Do not include markdown."),
        )
        parsed = result.parsed
        structured = {
            "status": "ok",
            "backend": result.backend,
            "assessment": parsed,
            "metadata": result.metadata,
            "raw_text": result.raw_text,
            "validation_note": BASELINE_NOTE,
            "scoring_disabled_note": None if SHOW_NUMERIC_SCORE else SCORING_DISABLED_NOTE,
        }
        return build_human_report(parsed, result.backend), structured
    except Exception as exc:  # noqa: BLE001 - show safe UI error without hiding debug context.
        error = {
            "status": "error",
            "message": str(exc),
            "disclaimer": STANDARD_DISCLAIMER,
            "validation_note": BASELINE_NOTE,
            "scoring_disabled_note": SCORING_DISABLED_NOTE,
        }
        return (
            "The analysis could not be completed. Try a clearer front-facing image, "
            "or check the configured Gemma runner.\n\n"
            f"**Error:** `{exc}`\n\n"
            f"**Safety note:** {STANDARD_DISCLAIMER}",
            error,
        )


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Cat Pain Detector") as demo:
        gr.Markdown(
            """
            <div class="hero-card">
              <div class="hero-eyebrow">Gemma 4 Good Hackathon · Health & Sciences</div>
              <div class="hero-title">Cat Pain Detector</div>
              <div class="hero-copy">
                Upload a cat face image to estimate visible Feline Grimace Scale cues: ears,
                eyes, muzzle, whiskers, and head position. The report emphasizes evidence,
                uncertainty, and safe next steps — not diagnosis.
              </div>
            </div>
            """
        )
        with gr.Row():
            with gr.Column(scale=1):
                image = gr.Image(type="pil", label="Cat image", height=420)
                gr.Markdown(
                    f"""
                    <div class="safety-card">
                      <strong>How to use safely</strong><br/>
                      This is triage support only. If the cat seems distressed, injured,
                      unusually quiet, not eating, hiding, limping, struggling to breathe,
                      or suddenly changed in behavior, contact a veterinarian promptly.
                      <br/><br/><strong>Scoring disabled:</strong> {SCORING_DISABLED_NOTE}
                    </div>
                    <br/>
                    <div class="validation-card">
                      <strong>Validation snapshot</strong><br/>
                      {BASELINE_NOTE}
                    </div>
                    """
                )
            with gr.Column(scale=2):
                report = gr.Markdown(label="Human-readable report")
                output = gr.JSON(label="Structured model output", open=False)
        if DEMO_SAMPLE_PATHS:
            gr.Examples(
                examples=DEMO_SAMPLE_PATHS,
                inputs=image,
                label="Licensed CatFLW demo images (not pain-labeled)",
            )
        button = gr.Button("Analyze image", variant="primary")
        button.click(analyze_image, inputs=image, outputs=[report, output])
        gr.Markdown(f"**Safety note:** {STANDARD_DISCLAIMER}\n\n**Validation note:** {BASELINE_NOTE}")
    return demo


if __name__ == "__main__":
    build_app().launch(
        css=APP_CSS,
        share=os.environ.get("GRADIO_SHARE", "false").lower() in {"1", "true", "yes", "on"},
        server_name=os.environ.get("GRADIO_SERVER_NAME"),
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
        allowed_paths=[str(PROJECT_ROOT / "data" / "demo_samples")],
    )

