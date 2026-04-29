import json, re, time, subprocess, sys
from pathlib import Path
from urllib.request import Request, urlopen

# Match the public Gemma 4 Kaggle notebook setup as closely as possible.
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'transformers', 'kagglehub', '-q'])

import kagglehub
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

OUT = Path('/kaggle/working')
IMG_DIR = OUT / 'fgs_official_examples'
IMG_DIR.mkdir(exist_ok=True)

EXAMPLES = [
    {
        'name': 'fgs_official_au0_no_or_mild_pain.png',
        'url': 'https://static.wixstatic.com/media/d1b6de_7b457746a6d94be1a5c19f7552b34402~mv2.png/v1/fill/w_246,h_353,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Frame%2032.png',
        'labels': {'ear_position':0,'orbital_tightening':0,'muzzle_tension':0,'whiskers_change':0,'head_position':0},
    },
    {
        'name': 'fgs_official_au1_mild_to_moderate_pain.png',
        'url': 'https://static.wixstatic.com/media/d1b6de_9384c0cfb19b44b3bbf7c1834bcf8168~mv2.png/v1/fill/w_246,h_353,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Frame%2033.png',
        'labels': {'ear_position':1,'orbital_tightening':1,'muzzle_tension':1,'whiskers_change':1,'head_position':1},
    },
    {
        'name': 'fgs_official_au2_moderate_to_severe_pain.png',
        'url': 'https://static.wixstatic.com/media/d1b6de_028a2ee8159741a28c5b4b623b5d19b2~mv2.png/v1/fill/w_246,h_353,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Frame%2034.png',
        'labels': {'ear_position':2,'orbital_tightening':2,'muzzle_tension':2,'whiskers_change':2,'head_position':2},
    },
]

DISCLAIMER = 'This prototype is triage support only and is not a veterinary diagnosis. If the cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly.'

PROMPT = f'''
You are assisting with feline acute pain triage from an image.
Return exactly one JSON object and no markdown. Do not diagnose.
Score visible Feline Grimace Scale action units.
Use these action units exactly: ear_position, orbital_tightening, muzzle_tension, whiskers_change, head_position.
Scores are 0 absent, 1 moderate/uncertain, 2 obvious.
Every action unit must include score, visible, evidence, and uncertainty.
If all five action units are visible, total_raw is their sum and total_normalized is total_raw / 10.
rescue_threshold_positive is true only if total_normalized > 0.39.
If any action unit is not visible, total_raw, total_normalized, and rescue_threshold_positive must be null.
Recommendation must be one of: low visible concern, monitor closely, contact a veterinarian, cannot assess.
Always include this disclaimer verbatim: {DISCLAIMER!r}
JSON keys required: action_units, total_raw, total_normalized, rescue_threshold_positive, uncertainty, recommendation, disclaimer.
'''.strip()


def extract_json(text):
    text = text.strip()
    text = re.sub(r'^```(?:json)?\\s*', '', text, flags=re.I)
    text = re.sub(r'\\s*```$', '', text)
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r'\{.*\}', text, flags=re.S)
        if not m: raise
        return json.loads(m.group(0))


def load_crop(ex):
    raw = urlopen(Request(ex['url'], headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
    p = IMG_DIR / ex['name']
    p.write_bytes(raw)
    img = Image.open(p).convert('RGB')
    crop = img.crop((0, 0, img.width, 205))
    crop_path = IMG_DIR / ex['name'].replace('.png', '_cat_only.png')
    crop.save(crop_path)
    return crop, str(crop_path)


def true_row(ex):
    total = sum(ex['labels'].values())
    return total, total/10, total/10 > 0.39

start = time.time()
model_path = kagglehub.model_download('google/gemma-4/transformers/gemma-4-e2b-it')
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.bfloat16, device_map='auto')
model.eval()

rows, failures = [], []
for i, ex in enumerate(EXAMPLES):
    try:
        image, image_path = load_crop(ex)
        messages = [{'role':'user', 'content':[{'type':'image', 'image': image}, {'type':'text', 'text': PROMPT}]}]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
        inputs = processor(text=text, images=image, return_tensors='pt').to(model.device)
        input_len = inputs['input_ids'].shape[-1]
        with torch.inference_mode():
            outputs = model.generate(**inputs, max_new_tokens=512)
        response = processor.decode(outputs[0][input_len:], skip_special_tokens=False)
        parsed_response = processor.parse_response(response)
        raw = parsed_response.get('content', str(parsed_response)) if isinstance(parsed_response, dict) else str(parsed_response)
        pred = extract_json(raw)
        t_raw, t_norm, t_rescue = true_row(ex)
        rows.append({'image_path': image_path, 'true_total_raw': t_raw, 'true_total_normalized': t_norm, 'true_rescue_threshold_positive': t_rescue, 'prediction': pred, 'raw_text': raw})
    except Exception as e:
        failures.append({'name': ex['name'], 'error': repr(e)})

# Minimal metrics, only for smoke/calibration examples.
comparable = [r for r in rows if isinstance(r.get('prediction'), dict) and r['prediction'].get('total_normalized') is not None]
if comparable:
    abs_err = [abs(float(r['prediction']['total_normalized']) - float(r['true_total_normalized'])) for r in comparable]
    mae = sum(abs_err)/len(abs_err)
else:
    mae = None

out = {
    'status': 'completed' if rows else 'failed',
    'runtime_seconds': time.time() - start,
    'result_count': len(rows),
    'failure_count': len(failures),
    'caution': 'Only 3 official FGS educational examples; smoke/calibration only, not clinical validation.',
    'metrics': {'mae_normalized_on_comparable_rows': mae, 'comparable_count': len(comparable)},
    'rows': rows,
    'failures': failures,
}
(OUT / 'gemma4_official_examples_smoke_metrics.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2)[:4000])
