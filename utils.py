import torch
from torch.cuda.amp import autocast
from translations import CATEGORIES, TRANSLATIONS

def build_prompt(**kwargs):
    default_params = ["masterpiece", "best quality", "1girl", "watercolor", "portrait", "upper body", "looking at viewer", "cute", "highres"]

    for key, values in kwargs.items():
        if values:
            english_values = [CATEGORIES[key][TRANSLATIONS[key].index(v)] for v in values if v in TRANSLATIONS[key]]
            default_params.append(", ".join(english_values))

    return ', '.join(default_params)

def generate_image(prompt, pipe, device):
    height = 512
    width = 512
    guidance_scale = 15
    num_inference_steps = 50
    pipe.enable_attention_slicing()

    with torch.autocast('cuda') if device == 'cuda' else torch.inference_mode():
        image = pipe(
            prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            height=height,
            width=width
        ).images[0]
    return image
