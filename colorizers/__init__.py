from .base_color import *
from .eccv16 import eccv16
from .siggraph17 import siggraph17
from .util import *

import torch
import numpy as np
from PIL import Image


_colorizer_cache = {}


def get_colorizer(model_type='eccv16', device='cpu'):
    """Get or create cached colorizer model."""
    cache_key = f"{model_type}_{device}"
    
    if cache_key not in _colorizer_cache:
        if model_type == 'eccv16':
            model = eccv16(pretrained=True)
        elif model_type == 'siggraph17':
            model = siggraph17(pretrained=True)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model.eval()
        model.to(device)
        _colorizer_cache[cache_key] = model
    
    return _colorizer_cache[cache_key]


def colorize_image(img_path, model_type='siggraph17', device='cpu', saturation_boost=1.3):
    """
    Colorize a grayscale image using the specified model.
    
    Args:
        img_path: Path to the input image or numpy array
        model_type: 'eccv16' or 'siggraph17'
        device: 'cpu' or 'cuda'
        saturation_boost: factor to boost color saturation (1.0-2.0 recommended)
    
    Returns:
        PIL Image of the colorized image
    """
    if isinstance(img_path, str):
        img_rgb = load_img(img_path)
    elif isinstance(img_path, np.ndarray):
        img_rgb = img_path
    else:
        raise ValueError("img_path must be string path or numpy array")
    
    if img_rgb.ndim == 2:
        img_rgb = np.tile(img_rgb[:, :, None], 3)
    
    model = get_colorizer(model_type, device)
    
    tens_orig_l, tens_rs_l = preprocess_img(img_rgb, HW=(256, 256))
    tens_orig_l = tens_orig_l.to(device)
    tens_rs_l = tens_rs_l.to(device)
    
    with torch.no_grad():
        out_ab = model(tens_rs_l)
    
    result = postprocess_tens(tens_orig_l, out_ab, saturation_boost=saturation_boost)
    result = np.clip(result * 255, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result)


def colorize_image_siggraph(img_path, device='cpu', saturation_boost=1.3):
    """Colorize using SIGGRAPH17 model (better quality + saturation boost)."""
    return colorize_image(img_path, model_type='siggraph17', device=device, saturation_boost=saturation_boost)
