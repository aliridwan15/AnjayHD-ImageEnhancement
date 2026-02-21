"""
Script Pewarnaan Foto Hitam Putih Menggunakan Deep Learning (OpenCV DNN)
Menggunakan model Colorization dari Zhang et al. (ECCV 2016)

Usage:
    python warnai_foto.py
"""

import cv2
import numpy as np
from pathlib import Path
import argparse


def warnai_foto(image_path, output_path):
    """
    Mewarnai foto hitam putih menjadi berwarna menggunakan Deep Learning (OpenCV DNN).
    
    Args:
        image_path: Path ke gambar input (hitam putih)
        output_path: Path untuk menyimpan hasil gambar berwarna
    """
    print(f"[INFO] Membaca gambar: {image_path}")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Tidak dapat membaca gambar: {image_path}")
    
    h, w = img.shape[:2]
    print(f"[INFO] Resolusi gambar: {w}x{h}")
    
    model_base = Path(__file__).parent
    proto_path = model_base / "colorization_deploy_v2.prototxt"
    model_path = model_base / "colorization_release_v2.caffemodel"
    
    if not proto_path.exists():
        proto_path = model_base / "models" / "colorization_deploy_v2.prototxt"
    if not model_path.exists():
        model_path = model_base / "models" / "colorization_release_v2.caffemodel"
    
    if not proto_path.exists():
        raise FileNotFoundError(f"File prototxt tidak ditemukan: {proto_path}")
    if not model_path.exists():
        print("[WARN] File caffemodel tidak ditemukan, menggunakan metode alternatif (PyTorch)...")
        return warnai_foto_pytorch(image_path, output_path)
    
    print("[INFO] Memuat model DNN OpenCV...")
    net = cv2.dnn.readNetFromCaffe(str(proto_path), str(model_path))
    
    print("[STEP 1/6] Mengubah ke ruang warna LAB...")
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel = img_lab[:, :, 0]
    
    print("[STEP 2/6] Mengubah ukuran L channel ke 224x224...")
    l_channel_resized = cv2.resize(l_channel, (224, 224))
    
    print("[STEP 3/6] Normalisasi L channel...")
    l_channel_normalized = l_channel_resized.astype(np.float32) / 255.0
    l_channel_normalized = l_channel_normalized.reshape(1, 1, 224, 224)
    
    print("[STEP 4/6] Memasukkan ke model DNN untuk prediksi...")
    net.setInput(l_channel_normalized)
    ab_output = net.forward()
    
    print("[STEP 5/6] Mengubah ukuran output ke resolusi asli...")
    ab_output = ab_output[0, :, :, :].transpose(1, 2, 0)
    ab_output = cv2.resize(ab_output, (w, h))
    
    a_channel = np.clip(ab_output[:, :, 0], 0, 255).astype(np.uint8)
    b_channel = np.clip(ab_output[:, :, 1], 0, 255).astype(np.uint8)
    
    l_channel_resized = cv2.resize(l_channel, (w, h))
    
    result_lab = cv2.merge([l_channel_resized, a_channel, b_channel])
    result = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)
    
    print(f"[STEP 6/6] Menyimpan hasil ke: {output_path}")
    cv2.imwrite(output_path, result)
    
    print(f"[SUCCESS] Pewarnaan selesai! Hasil disimpan ke: {output_path}")
    print(f"[INFO] Resolusi hasil: {result.shape[1]}x{result.shape[0]}")
    
    return result


def warnai_foto_pytorch(image_path, output_path):
    """Fallback menggunakan PyTorch ECCV16 jika model Caffe tidak tersedia."""
    print("[INFO] Menggunakan metode alternatif: PyTorch ECCV16")
    
    from colorizers import colorize_image
    colorized = colorize_image(image_path, model_type='eccv16', device='cpu')
    result = cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR)
    
    cv2.imwrite(output_path, result)
    print(f"[SUCCESS] Pewarnaan selesai! Hasil disimpan ke: {output_path}")
    
    return result


def download_models():
    """Download model colorization dari GitHub."""
    import urllib.request
    
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    urls_to_try = [
        ("colorization_release_v2.caffemodel", 
         "https://github.com/richzhang/colorization/raw/refs/heads/caffe/colorization/models/colorization_release_v2.caffemodel"),
        ("colorization_release_v2.caffemodel",
         "https://github.com/AsadiAhmad/Colorize-Grayscale-Images/raw/main/Code/colorization_release_v2.caffemodel"),
        ("colorization_deploy_v2.prototxt",
         "https://raw.githubusercontent.com/richzhang/colorization/caffe/colorization/models/colorization_deploy_v2.prototxt"),
    ]
    
    for name, url in urls_to_try:
        path = models_dir / name
        if not path.exists():
            print(f"[INFO] Downloading {name}...")
            try:
                ctx = __import__('ssl').create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = __import__('ssl').CERT_NONE
                opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, path)
                print(f"[OK] {name} downloaded")
            except Exception as e:
                print(f"[ERROR] Gagal download {name}: {e}")
    
    proto_path = models_dir / "colorization_deploy_v2.prototxt"
    if not proto_path.exists():
        print(f"[INFO] Silakan download manual dari: https://github.com/richzhang/colorization")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pewarnaan Foto Hitam Putih dengan Deep Learning')
    parser.add_argument('input', nargs='?', help='Path gambar input')
    parser.add_argument('output', nargs='?', help='Path gambar output')
    parser.add_argument('--download', action='store_true', help='Download model terlebih dahulu')
    
    args = parser.parse_args()
    
    if args.download:
        download_models()
    elif args.input and args.output:
        try:
            warnai_foto(args.input, args.output)
        except Exception as e:
            print(f"[ERROR] {e}")
    else:
        input_path = "foto_bw.jpg"
        output_path = "foto_berwarna.jpg"
        
        print("=" * 50)
        print("Pewarnaan Foto Hitam Putih dengan Deep Learning")
        print("=" * 50)
        
        if not Path(input_path).exists():
            print(f"[ERROR] File '{input_path}' tidak ditemukan!")
            print("Silakan menyediakan file foto hitam putih atau gunakan argumen:")
            print("  python warnai_foto.py <input_path> <output_path>")
            print("")
            print("Untuk download model:")
            print("  python warnai_foto.py --download")
            exit(1)
        
        warnai_foto(input_path, output_path)
