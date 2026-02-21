import subprocess
import os
import argparse


def cari_exe():
    """Cari executable di folder saat ini atau folder tambahan."""
    nama_exe = "realesrgan-ncnn-vulkan.exe"
    
    lokasi = [
        nama_exe,
        os.path.join(os.getcwd(), nama_exe),
        os.path.join(os.path.dirname(__file__), nama_exe),
        os.path.join(os.path.dirname(__file__), "bin", nama_exe),
        r"D:\Open Code\ImageHD\realesrgan-ncnn-vulkan.exe",
        r"D:\Open Code\realesrgan-ncnn-vulkan.exe",
    ]
    
    for path in lokasi:
        if os.path.exists(path):
            return path
    
    return nama_exe


def proses_hd_ncnn(input_path: str, output_path: str, exe_path: str | None = None, scale: int = 4) -> None:
    """Restorasi gambar HD menggunakan Real-ESRGAN NCNN Vulkan executable."""
    if exe_path is None:
        exe_path = cari_exe()
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File input tidak ditemukan: {input_path}")
    
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"Executable tidak ditemukan: {exe_path}")
    
    print(f"[INFO] Memproses: {input_path}")
    print(f"[INFO] Menggunakan: {exe_path}")
    
    result = subprocess.run(
        [exe_path, "-i", input_path, "-o", output_path, "-s", str(scale)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Error menjalankan Real-ESRGAN: {result.stderr}")
    
    print(f"[INFO] Selesai! Hasil disimpan ke: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image HD Enhancement dengan Real-ESRGAN NCNN')
    parser.add_argument('input', help='Path gambar input')
    parser.add_argument('output', help='Path gambar output')
    parser.add_argument('--scale', type=int, default=4, help='Faktor pembesaran (default: 4)')
    parser.add_argument('--exe', type=str, default=None, help='Path ke realesrgan-ncnn-vulkan.exe (opsional)')
    
    args = parser.parse_args()
    
    try:
        proses_hd_ncnn(args.input, args.output, exe_path=args.exe, scale=args.scale)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except RuntimeError as e:
        print(f"[ERROR] {e}")
