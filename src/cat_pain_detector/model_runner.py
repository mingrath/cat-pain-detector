"""Model runner abstraction.

Design choice: run Gemma 4 server-side first, then optimize for local/edge only
after the validation loop works. This file gives the rest of the project one
stable interface while allowing several backends:

- HTTP server/endpoint runner for GPU-backed services and deployed demos.
- Transformers runner adapted from the pulled Kaggle Gemma 4 notebook.
- Mock runner for UI development and parser tests without GPU/model access.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, Literal, Protocol

from cat_pain_detector.json_utils import extract_json_object, parse_fgs_model_output
from cat_pain_detector.prompts import FGS_RESPONSE_TEMPLATE


@dataclass
class ModelResult:
    raw_text: str
    parsed: dict[str, Any]
    backend: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunnerConfig:
    backend: Literal["mock", "http", "transformers"] = "mock"
    endpoint_url: str | None = None
    model_id: str = "google/gemma-4/transformers/gemma-4-e2b-it"
    model_path: str | None = None
    max_new_tokens: int = 512
    timeout_seconds: int = 120
    enable_thinking: bool = False


class VisionLanguageRunner(Protocol):
    def analyze(self, image: Any, prompt: str) -> ModelResult:
        """Analyze an image with a text prompt and return raw + parsed output."""


class NotConfiguredRunner:
    def analyze(self, image: Any, prompt: str) -> ModelResult:
        raise RuntimeError("Gemma 4 runner is not configured yet.")


class MockFGSRunner:
    """Deterministic runner for UI and parser development without model access."""

    def analyze(self, image: Any, prompt: str) -> ModelResult:
        raw_text = json.dumps(FGS_RESPONSE_TEMPLATE)
        return ModelResult(
            raw_text=raw_text,
            parsed=parse_fgs_model_output(raw_text),
            backend="mock",
            metadata={"note": "Mock response; not a model prediction."},
        )


def _image_to_data_url(image: Any) -> str:
    """Encode a PIL-like image as a JPEG data URL for HTTP backends."""
    if not hasattr(image, "save"):
        raise TypeError("HTTP runner expects a PIL-like image with .save()")
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=92)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


class HTTPGemmaRunner:
    """Call a server-side Gemma endpoint.

    Expected request JSON:

    ```json
    {"image": "data:image/jpeg;base64,...", "prompt": "...", "max_new_tokens": 512}
    ```

    Expected response can be one of:

    - the final FGS JSON object
    - `{ "raw_text": "..." }`
    - `{ "content": "..." }`
    - `{ "parsed": {...}, "raw_text": "..." }`
    """

    def __init__(self, endpoint_url: str, timeout_seconds: int = 120, max_new_tokens: int = 512) -> None:
        self.endpoint_url = endpoint_url
        self.timeout_seconds = timeout_seconds
        self.max_new_tokens = max_new_tokens

    def analyze(self, image: Any, prompt: str) -> ModelResult:
        body = json.dumps(
            {
                "image": _image_to_data_url(image),
                "prompt": prompt,
                "max_new_tokens": self.max_new_tokens,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint_url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Gemma HTTP endpoint failed: {exc}") from exc

        envelope = extract_json_object(response_body)
        if "parsed" in envelope and isinstance(envelope["parsed"], dict):
            raw_text = envelope.get("raw_text", json.dumps(envelope["parsed"]))
            parsed = parse_fgs_model_output(json.dumps(envelope["parsed"]))
        elif "raw_text" in envelope:
            raw_text = str(envelope["raw_text"])
            parsed = parse_fgs_model_output(raw_text)
        elif "content" in envelope:
            raw_text = str(envelope["content"])
            parsed = parse_fgs_model_output(raw_text)
        else:
            raw_text = response_body
            parsed = parse_fgs_model_output(json.dumps(envelope))

        return ModelResult(raw_text=raw_text, parsed=parsed, backend="http", metadata={"url": self.endpoint_url})


class Gemma4TransformersRunner:
    """Local/server Python runner adapted from the Kaggle Gemma 4 notebook.

    This is intended for GPU-backed Kaggle/Hugging Face/server use, not as the
    default Mac-local development path. Dependencies are imported lazily so the
    repository can still run docs/tests without installing torch/transformers.
    """

    def __init__(
        self,
        model_id: str = "google/gemma-4/transformers/gemma-4-e2b-it",
        model_path: str | None = None,
        max_new_tokens: int = 512,
        enable_thinking: bool = False,
    ) -> None:
        self.model_id = model_id
        self.model_path = model_path
        self.max_new_tokens = max_new_tokens
        self.enable_thinking = enable_thinking
        self._processor: Any | None = None
        self._model: Any | None = None

    def _resolve_model_path(self) -> str:
        if self.model_path:
            return self.model_path
        try:
            import kagglehub  # type: ignore
        except ImportError as exc:
            raise RuntimeError("kagglehub is required to download Kaggle Gemma 4 models") from exc
        return str(kagglehub.model_download(self.model_id))

    def _load(self) -> tuple[Any, Any]:
        if self._processor is not None and self._model is not None:
            return self._processor, self._model

        try:
            import torch  # type: ignore
            from transformers import AutoModelForCausalLM, AutoProcessor  # type: ignore
        except ImportError as exc:
            raise RuntimeError("torch and transformers are required for Gemma4TransformersRunner") from exc

        path = self._resolve_model_path()
        self._processor = AutoProcessor.from_pretrained(path)

        common_kwargs = {"device_map": "auto"}
        dtype = torch.bfloat16 if hasattr(torch, "bfloat16") else torch.float16
        try:
            self._model = AutoModelForCausalLM.from_pretrained(path, dtype=dtype, **common_kwargs)
        except TypeError:
            self._model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=dtype, **common_kwargs)
        self._model.eval()
        return self._processor, self._model

    def analyze(self, image: Any, prompt: str) -> ModelResult:
        processor, model = self._load()
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        text = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=self.enable_thinking,
        )
        inputs = processor(text=text, images=image, return_tensors="pt").to(model.device)
        input_len = inputs["input_ids"].shape[-1]

        try:
            import torch  # type: ignore
            context = torch.inference_mode()
        except ImportError:  # pragma: no cover; _load already checks torch.
            context = _NullContext()

        with context:
            outputs = model.generate(**inputs, max_new_tokens=self.max_new_tokens)

        response = processor.decode(outputs[0][input_len:], skip_special_tokens=False)
        parsed_response = processor.parse_response(response)
        if isinstance(parsed_response, dict) and "content" in parsed_response:
            raw_text = str(parsed_response["content"])
        else:
            raw_text = json.dumps(parsed_response) if isinstance(parsed_response, dict) else str(parsed_response)

        return ModelResult(
            raw_text=raw_text,
            parsed=parse_fgs_model_output(raw_text),
            backend="transformers",
            metadata={"model_id": self.model_id, "model_path": str(self.model_path or "kagglehub")},
        )


class _NullContext:
    def __enter__(self) -> None:
        return None

    def __exit__(self, *_: object) -> None:
        return None


def runner_from_env() -> VisionLanguageRunner:
    """Create a runner from environment variables.

    Environment:

    - `CAT_PAIN_RUNNER=mock|http|transformers`
    - `GEMMA_SERVER_URL=https://...` for HTTP mode
    - `GEMMA_MODEL_ID=google/gemma-4/transformers/gemma-4-e2b-it`
    - `GEMMA_MODEL_PATH=/path/to/downloaded/model`
    - `GEMMA_MAX_NEW_TOKENS=512`
    - `GEMMA_ENABLE_THINKING=true|false`, default `false` for strict JSON tasks
    """
    backend = os.environ.get("CAT_PAIN_RUNNER", "mock").lower()
    max_new_tokens = int(os.environ.get("GEMMA_MAX_NEW_TOKENS", "512"))
    enable_thinking = os.environ.get("GEMMA_ENABLE_THINKING", "false").lower() in {"1", "true", "yes", "on"}

    if backend == "mock":
        return MockFGSRunner()
    if backend == "http":
        endpoint = os.environ.get("GEMMA_SERVER_URL")
        if not endpoint:
            raise RuntimeError("CAT_PAIN_RUNNER=http requires GEMMA_SERVER_URL")
        return HTTPGemmaRunner(endpoint_url=endpoint, max_new_tokens=max_new_tokens)
    if backend == "transformers":
        return Gemma4TransformersRunner(
            model_id=os.environ.get("GEMMA_MODEL_ID", "google/gemma-4/transformers/gemma-4-e2b-it"),
            model_path=os.environ.get("GEMMA_MODEL_PATH"),
            max_new_tokens=max_new_tokens,
            enable_thinking=enable_thinking,
        )
    raise RuntimeError(f"Unknown CAT_PAIN_RUNNER backend: {backend}")

