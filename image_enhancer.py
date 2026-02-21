"""
Image HD Enhancement Script
Menjernihkan foto dari galeri menjadi High Definition (HD)

Fitur:
1. Restorasi HD dengan Real-ESRGAN NCNN Vulkan
2. Pewarnaan foto BW dengan PyTorch ECCV16

Usage:
    python image_enhancer.py input.jpg output.jpg --mode enhance    # HD saja
    python image_enhancer.py input.jpg output.jpg --mode colorize   # Warnai saja
    python image_enhancer.py input.jpg output.jpg --mode both       # Warnai + HD
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
import sys
import subprocess
import os
import tempfile


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def cek_gambar_hitam_putih(image: np.ndarray) -> bool:
    """Mengecek apakah gambar adalah hitam putih (grayscale) atau berwarna."""
    if len(image.shape) == 2:
        return True
    
    b, g, r = cv2.split(image.astype(np.float32))
    diff_rg = np.abs(r - g)
    diff_gb = np.abs(g - b)
    diff_rb = np.abs(r - b)
    total_diff = float(np.mean(diff_rg) + np.mean(diff_gb) + np.mean(diff_rb))
    threshold = 10.0
    return total_diff < threshold


def restorasi_hd(input_path: str, output_path: str, scale: int = 4) -> None:
    """Restorasi gambar HD menggunakan Real-ESRGAN NCNN Vulkan."""
    exe_name = "realesrgan-ncnn-vulkan.exe"
    
    exe_dir = None
    for search_dir in [os.getcwd(), os.path.dirname(__file__), r"D:\Open Code\ImageHD\models"]:
        exe_path = os.path.join(search_dir, exe_name)
        if os.path.exists(exe_path):
            exe_dir = search_dir
            exe_path = os.path.abspath(exe_path)
            break
    
    if exe_dir is None:
        raise FileNotFoundError(f"Executable tidak ditemukan: {exe_name}")
    
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File input tidak ditemukan: {input_path}")
    
    print(f"[INFO] Memproses: {input_path}")
    img = cv2.imread(input_path)
    print(f"[INFO] Resolusi awal: {img.shape[1]}x{img.shape[0]}")
    print(f"[INFO] Menggunakan Real-ESRGAN NCNN Vulkan...")
    
    try:
        subprocess.run(
            [exe_path, "-i", input_path, "-o", output_path, "-s", str(scale)],
            capture_output=True,
            text=True,
            cwd=exe_dir,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error menjalankan Real-ESRGAN: {e.stderr}")
    
    if not os.path.exists(output_path):
        raise RuntimeError("Gagal memproses gambar HD")
    
    result_img = cv2.imread(output_path)
    if result_img is None:
        raise RuntimeError("Gagal memproses gambar HD")
    
    print(f"[INFO] Selesai! Hasil disimpan ke: {output_path}")
    print(f"[INFO] Resolusi akhir: {result_img.shape[1]}x{result_img.shape[0]}")


def warnai_foto(input_path: str, output_path: str, model_type: str = 'siggraph17') -> None:
    """Pewarnaan foto BW menggunakan PyTorch ECCV16 atau SIGGRAPH17."""
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Tidak dapat membaca gambar: {input_path}")
    
    print(f"[INFO] Memproses: {input_path}")
    
    if not cek_gambar_hitam_putih(img):
        print("[WARN] Gambar sudah berwarna, tidak perlu diwarnai")
        cv2.imwrite(output_path, img)
        print(f"[INFO] Selesai! Hasil disimpan ke: {output_path}")
        return
    
    model_name = "SIGGRAPH17 (Realistis)" if model_type == 'siggraph17' else "ECCV16"
    print(f"[INFO] Mewarnai foto dengan AI Deep Learning ({model_name})...")
    
    try:
        from colorizers import colorize_image
        colorized_pil = colorize_image(input_path, model_type=model_type, device='cpu')
        colorized_np = np.array(colorized_pil)
        result = cv2.cvtColor(colorized_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"[WARN] PyTorch colorizer error: {e}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    cv2.imwrite(output_path, result)
    print(f"[INFO] Selesai! Hasil disimpan ke: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image HD Enhancement & Colorization')
    parser.add_argument('input', help='Path gambar input (opsional, gunakan nama file saja)')
    parser.add_argument('output', help='Path gambar output (opsional, gunakan nama file saja)')
    parser.add_argument('--mode', type=str, default='enhance', 
                        choices=['enhance', 'colorize', 'both'],
                        help='Mode: enhance (HD saja), colorize (warnai saja), both (warnai + HD)')
    parser.add_argument('--scale', type=int, default=4, choices=[2, 4],
                        help='Faktor pembesaran (default: 4)')
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    if not os.path.isabs(input_path):
        input_path = os.path.join(INPUT_DIR, input_path)
    
    if not os.path.isabs(output_path):
        output_path = os.path.join(OUTPUT_DIR, output_path)
    
    try:
        if args.mode == 'enhance':
            restorasi_hd(input_path, output_path, scale=args.scale)
            
        elif args.mode == 'colorize':
            warnai_foto(input_path, output_path)
            
        elif args.mode == 'both':
            print("[INFO] Mode: Warnai foto BW + Restorasi HD")
            
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                temp_path = tmp.name
            
            warnai_foto(input_path, temp_path)
            restorasi_hd(temp_path, output_path, scale=args.scale)
            os.remove(temp_path)
            
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except ValueError as e:
        print(f"[ERROR] {e}")
    except RuntimeError as e:
        print(f"[ERROR] {e}")
