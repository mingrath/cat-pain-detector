# Kaggle + StackOverflow Research Sprint

Goal: find practical Kaggle and StackOverflow resources that can improve the Cat Pain Detector beyond the scientific-paper baseline.

## Artifacts Created

Tavily:

- `research/tavily/kaggle-gemma4-hackathon-search.json`
- `research/tavily/kaggle-gemma4-notebooks-search.json`
- `research/tavily/stackoverflow-gradio-hf-gpu-search.json`
- `research/tavily/stackoverflow-gemma-keras-search.json`
- `research/tavily/kaggle-stackoverflow-improvement-research.md`

Firecrawl:

- `research/firecrawl/kaggle-gemma4-code-search.json`
- `research/firecrawl/kaggle-cat-pain-datasets-search.json`
- `research/firecrawl/stackoverflow-gradio-hf-search.json`
- `research/firecrawl/stackoverflow-gemma-kaggle-search.json`

Kaggle CLI:

- `research/kaggle/models-gemma4.csv`
- `research/kaggle/kernels-gemma4.csv`
- `research/kaggle/kernels-gemma4-multimodal.csv`
- `research/kaggle/kernels-catflw.csv`
- `research/kaggle/datasets-cat-pain.csv`
- `research/kaggle/datasets-feline-grimace.csv`
- `research/kaggle/datasets-cat-landmarks.csv`
- `research/kaggle/pulled/gpreda-gemma4/`
- `research/kaggle/pulled/catflw-load/`

## Key Kaggle Findings

### 1. Use the official Gemma 4 model assets

Kaggle Models has:

- `google/gemma-4` — official Google Gemma 4 model collection
- `keras/gemma4` — Keras Gemma 4 model collection, described as multimodal for text, image, and video input

Action for our project:

- Build `src/model_runner.py` around a swappable backend.
- Start with server-side inference using official Kaggle/HF-compatible Gemma 4 assets.
- Do not use older Gemma 2/3 notebooks as proof of multimodal behavior unless we explicitly adapt them.

Sources:

- https://www.kaggle.com/models/google/gemma-4
- https://www.kaggle.com/models/keras/gemma4/keras/gemma4_4b/2

### 2. Pull and adapt the best Gemma 4 multimodal Kaggle notebook

Pulled locally:

- `research/kaggle/pulled/gpreda-gemma4/gemma-4-e2b-multilangual-and-multimodal.ipynb`

Important implementation pattern from the notebook:

```python
MODEL_PATH = kagglehub.model_download("google/gemma-4/transformers/gemma-4-e2b-it")

processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.bfloat16,
    device_map="auto"
)
```

Image prompt pattern:

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": "..."}
        ]
    }
]

text = processor.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True,
)
inputs = processor(text=text, images=image, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=1024)
response = processor.decode(outputs[0][input_len:], skip_special_tokens=False)
output = processor.parse_response(response)
```

Action for our project:

- Use this as the first concrete Gemma 4 baseline runner.
- Add a strict JSON parser after `processor.parse_response(response)`.
- Keep `max_new_tokens` small for demo latency, probably 512 or less for structured FGS output.
- Log raw responses for validation debugging.

Source:

- https://www.kaggle.com/code/gpreda/gemma-4-e2b-multilangual-and-multimodal

### 3. Pull and adapt the CatFLW loading notebook

Pulled locally:

- `research/kaggle/pulled/catflw-load/catflw-load.ipynb`

Important implementation pattern:

```python
imgs_list = sorted(glob.glob('/kaggle/input/catflw/CatFLW dataset/images/*.png'))

for path in imgs_list:
    name = path.split('/')[-1][:-4]
    image = cv2.imread(f'/kaggle/input/catflw/CatFLW dataset/images/{name}.png')

    with open(f'/kaggle/input/catflw/CatFLW dataset/labels/{name}.json', 'r') as f:
        data = json.load(f)
        labels.append(data['labels'])
        bboxes.append(data['bounding_boxes'])
```

Action for our project:

- Create `src/data/catflw.py` to load local CatFLW from `data/raw/catflw/CatFLW dataset/`.
- Use CatFLW to validate face localization and landmark/evidence overlays.
- Do not treat CatFLW as pain data.

Sources:

- https://www.kaggle.com/datasets/georgemartvel/catflw
- https://www.kaggle.com/code/georgemartvel/catflw-load
- https://github.com/martvelge/CatFLW

### 4. Kaggle search confirms no obvious public FGS pain dataset

Kaggle CLI searches:

- `feline grimace` returned no useful dataset rows.
- `cat pain` returned no FGS-labeled pain dataset.
- `cat landmarks` returned CatFLW as the relevant dataset.

Action for our project:

- Keep author-request path as the primary validation-data path.
- If no response, create a small transparent validation set and label it as limited / exploratory.
- Avoid making accuracy claims from generic cat-face datasets.

## StackOverflow / Implementation Pitfall Findings

The StackOverflow results were less domain-specific than Kaggle, but they highlighted practical failure modes.

### 1. Make sure the model is truly receiving the image

A common multimodal failure mode is accidentally using a text-only Gemma variant or passing image data in a format the model runner ignores.

Action:

- Add a smoke test image in `tests/` or `scripts/smoke_test_gemma_image.py`.
- Ask a simple visual question and assert the answer changes when the image changes.
- In the runner, accept a PIL image and pass it through the processor `images=` argument, not as plain JSON text.

Relevant result:

- https://stackoverflow.com/questions/79015047/ollama-multimodal-gemma-not-seeing-image

### 2. Plan for GPU memory failure

Relevant StackOverflow results surfaced CUDA out-of-memory issues and GPU loading concerns.

Action:

- Use `device_map="auto"` first.
- Use `torch.bfloat16` or `torch.float16` where supported.
- Keep validation batch size at 1 initially.
- Build a CLI flag for `--max-new-tokens` and default it low.
- Catch OOM and return a useful error message.

Relevant results:

- https://stackoverflow.com/questions/59129812/how-to-avoid-cuda-out-of-memory-in-pytorch
- https://stackoverflow.com/questions/59789059/gpu-out-of-memory-error-message-on-google-colab
- https://stackoverflow.com/questions/77237818/how-to-load-a-huggingface-pretrained-transformer-model-directly-to-gpu

### 3. Do not rely on raw JSON upload for images

StackOverflow surfaced recurring confusion about putting images directly inside JSON. For our app, Gradio should pass image data as a file/PIL object. For any API route, use multipart upload or base64 with explicit decoding.

Action:

- Gradio app: `gr.Image(type="pil")`.
- API wrapper: accept multipart image upload first; use base64 only for external service compatibility.
- Model prompt output can be JSON, but image input should not be conflated with JSON payload design.

Relevant results:

- https://stackoverflow.com/questions/68643893/upload-an-image-file-with-json-format
- https://stackoverflow.com/questions/73082927/how-to-store-html-input-type-file-as-json-object

## Recommendations To Add To The Build Plan

1. Add `src/model_runner.py` with `Gemma4TransformersRunner` based on the pulled Kaggle notebook.
2. Add `src/data/catflw.py` and `scripts/inspect_catflw.py` based on the CatFLW notebook.
3. Add `scripts/smoke_test_gemma_image.py` to verify image input actually changes the model response.
4. Add `src/json_repair.py` or robust parser logic for fenced JSON, malformed JSON, and fallback outputs.
5. Add validation modes:
   - `catflw-landmarks`: image + landmark/bbox sanity checks.
   - `fgs-labeled`: true FGS metrics once labels are available.
6. Add explicit deployment notes for Hugging Face Spaces / Kaggle Notebook fallback.
7. Keep all accuracy language gated behind `metrics/*.json` generated by the validation script.

## Bottom Line

The most useful external improvement is not another generic model: it is adapting the existing Kaggle Gemma 4 multimodal notebook plus CatFLW loader into our repo, then wrapping them with validation-first scripts and strict JSON parsing.
