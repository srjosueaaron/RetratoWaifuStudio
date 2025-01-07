# model.py
import torch
from diffusers import StableDiffusionPipeline

def get_device():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Usando dispositivo: {device}")
    return device

def load_model(device):
    pipe = StableDiffusionPipeline.from_pretrained(
        'hakurei/waifu-diffusion',
        torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
        variant="fp16" if device == 'cuda' else None
    ).to(device)
    pipe.safety_checker = None
    return pipe