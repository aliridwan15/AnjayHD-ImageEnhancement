from PIL import Image
import numpy as np
from skimage import color
import torch
import torch.nn.functional as F
import cv2


def load_img(img_path):
    out_np = np.asarray(Image.open(img_path))
    if out_np.ndim == 2:
        out_np = np.tile(out_np[:, :, None], 3)
    elif out_np.ndim == 3 and out_np.shape[2] == 4:
        out_np = out_np[:, :, :3]
    return out_np


def resize_img(img, HW, resample=Image.BICUBIC):
    return np.array(Image.fromarray(img).resize((HW[1], HW[0]), resample=resample))


def adjust_saturation(img_rgb, saturation_factor=1.3):
    """
    Increase saturation of the colorized image.
    saturation_factor: 1.0 = no change, >1.0 = more saturated
    """
    # Convert to HSV
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    
    # Increase saturation
    hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    
    # Convert back to RGB
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    
    return result


def preprocess_img(img_rgb_orig, HW=(256, 256), resample=Image.BICUBIC):
    """
    Preprocess for ECCV16 model.
    Returns original size L and resized L as torch Tensors.
    """
    img_rgb_rs = resize_img(img_rgb_orig, HW=HW, resample=resample)
    
    img_lab_orig = color.rgb2lab(img_rgb_orig)
    img_lab_rs = color.rgb2lab(img_rgb_rs)

    img_l_orig = img_lab_orig[:, :, 0]
    img_l_rs = img_lab_rs[:, :, 0]

    tens_orig_l = torch.Tensor(img_l_orig)[None, None, :, :]
    tens_rs_l = torch.Tensor(img_l_rs)[None, None, :, :]

    return tens_orig_l, tens_rs_l


def postprocess_tens(tens_orig_l, out_ab, mode='bilinear', saturation_boost=1.3):
    """
    Postprocess the output.
    tens_orig_l: 1 x 1 x H_orig x W_orig (L channel from original image)
    out_ab: 1 x 2 x H x W (ab channels from model output)
    saturation_boost: factor to boost color saturation (1.0 = no change)
    """
    HW_orig = tens_orig_l.shape[2:]
    HW = out_ab.shape[2:]

    if HW_orig[0] != HW[0] or HW_orig[1] != HW[1]:
        out_ab_orig = F.interpolate(out_ab, size=HW_orig, mode=mode)
    else:
        out_ab_orig = out_ab

    out_lab_orig = torch.cat((tens_orig_l, out_ab_orig), dim=1)
    
    out_rgb = color.lab2rgb(out_lab_orig.data.cpu().numpy()[0, ...].transpose((1, 2, 0)))
    
    # Boost saturation
    if saturation_boost > 1.0:
        out_rgb = adjust_saturation((out_rgb * 255).astype(np.uint8), saturation_boost)
        out_rgb = out_rgb.astype(np.float32) / 255.0
    
    return out_rgb


def colorize_eccv16(img_rgb, saturation_boost=1.3):
    """
    Colorize using ECCV16 model.
    img_rgb: numpy array (H x W x 3) in RGB format
    saturation_boost: factor to boost color saturation
    Returns: numpy array (H x W x 3) in RGB format
    """
    from .eccv16 import eccv16
    
    model = eccv16(pretrained=True).eval()
    
    (tens_l_orig, tens_l_rs) = preprocess_img(img_rgb, HW=(256, 256))
    
    with torch.no_grad():
        out_ab = model(tens_l_rs)
    
    out_img = postprocess_tens(tens_l_orig, out_ab, saturation_boost=saturation_boost)
    out_img = np.clip(out_img * 255, 0, 255).astype(np.uint8)
    
    return out_img


def colorize_siggraph17(img_rgb, saturation_boost=1.3):
    """
    Colorize using SIGGRAPH17 model.
    img_rgb: numpy array (H x W x 3) in RGB format
    saturation_boost: factor to boost color saturation
    Returns: numpy array (H x W x 3) in RGB format
    """
    from .siggraph17 import siggraph17
    
    model = siggraph17(pretrained=True).eval()
    
    (tens_l_orig, tens_l_rs) = preprocess_img(img_rgb, HW=(256, 256))
    
    with torch.no_grad():
        out_ab = model(tens_l_rs)
    
    out_img = postprocess_tens(tens_l_orig, out_ab, saturation_boost=saturation_boost)
    out_img = np.clip(out_img * 255, 0, 255).astype(np.uint8)
    
    return out_img
