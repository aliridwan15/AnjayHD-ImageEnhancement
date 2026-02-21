# ✨ AnjayHD - Image Enhancement

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0+-white?style=flat&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat">
  <img src="https://img.shields.io/github/stars/aliridwan/anjayhd?style=flat" alt="Stars">
</p>

<p align="center">
  <img src=".github/images/hero-preview.png" alt="AnjayHD Preview" width="800">
</p>

---

## 🌸 Tentang AnjayHD

AnjayHD adalah aplikasi web berbasis AI untuk meningkatkan kualitas foto dengan teknologi modern. Ubah foto lama yang buram, pecah, atau hitam putih menjadi gambar HD profesional dengan mudah.

---

## 🚀 Fitur Utama

### 1. 🔍 Super Resolution
Perjelas foto yang pecah atau buram menjadi gambar HD yang tajam menggunakan teknologi AI upscaling.

| Sebelum | Sesudah |
|:-------:|:-------:|
| <img src=".github/images/before-enhance.jpg" width="300"> | <img src=".github/images/after-enhance.jpg" width="300"> |

**Hasil:** Foto buram menjadi tajam dengan detail yang terjaga hingga 4x skala pembesaran.

---

### 2. 🎨 Pewarnaan Foto (Colorize)
Warna foto hitam putih jadul jadi hidup kembali dengan teknologi AI colorization.

| Sebelum (BW) | Sesudah (Warna) |
|:------------:|:---------------:|
| <img src=".github/images/before-colorize.jpg" width="300"> | <img src=".github/images/after-colorize.jpg" width="300"> |

**Hasil:** Foto hitam putih otomatis diwarnai dengan akurat.

---

### 3. ✨ Kombinasi (Both)
Warnai & HD-kan sekaligus dalam satu proses untuk hasil maksimal.

| Sebelum | Sesudah |
|:-------:|:-------:|
| <img src=".github/images/before-both.jpg" width="300"> | <img src=".github/images/after-both.jpg" width="300"> |

**Hasil:** Foto lama hitam putih menjadi HD berwarna.

---

## 📊 Perbandingan Skala

| Skala 2x | Skala 4x |
|:--------:|:--------:|
| Cepat, hasil baik | HD Max, detail penuh |
| Cocok untuk preview | Cocok untuk hasil akhir |

---

## 🛠️ Instalasi

### Prerequisites
- Python 3.8+
- Windows/Linux dengan GPU (opsional untuk kecepatan)

### Steps

```bash
# Clone repository
git clone https://github.com/aliridwan/anjayhd.git
cd anjayhd

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

Buka browser: **http://localhost:5000**

---

## 💻 Penggunaan

### Melalui Web Interface

1. **Buka** http://localhost:5000
2. **Drag & Drop** foto kamu ke zona upload
3. **Pilih Mode:**
   - 📸 `Foto HD` - Super Resolution
   - 🎨 `Coloring Foto` - Pewarnaan BW
   - ✨ `Kombinasi` - Keduanya sekaligus
4. **Pilih Skala:** 2x (Cepat) atau 4x (HD Max)
5. **Klik** "Proses Gambar"
6. **Download** hasil

### Melalui CLI

```bash
# HD Enhancement saja
python image_enhancer.py input.jpg output.jpg --mode enhance --scale 4

# Pewarnaan saja
python image_enhancer.py input.jpg output.jpg --mode colorize

# Keduanya
python image_enhancer.py input.jpg output.jpg --mode both --scale 4
```

---

## 📁 Struktur Project

```
anjayhd/
├── app.py                     # Flask web server
├── image_enhancer.py          # CLI image processing
├── proses_hd_ncnn.py          # NCNN processing
├── warnai_foto.py             # Colorization
├── templates/
│   └── index.html             # Frontend UI
├── models/                    # AI models
│   └── models/                # Real-ESRGAN models
├── input/                     # Input images
├── output/                    # Output images
└── penggunaan.txt             # Usage guide (ID)
```

---

## 🧰 Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Frontend | HTML, CSS, Tailwind, JavaScript |
| Backend | Python, Flask |
| AI/ML | Real-ESRGAN, OpenCV, NumPy |
| Image Processing | PIL, ncnn Vulkan |

---

## 📸 Screenshot

<p align="center">
  <img src=".github/images/screenshot-ui.png" alt="UI Screenshot" width="800">
</p>

---

## 🤝 Kontribusi

Contributions are welcome! Silakan fork repository ini dan buat pull request.

---

## 📝 Lisensi

MIT License - lihat [LICENSE](LICENSE) untuk detail.

---

## 🙏 Credits

- **Made by** Ali Ridwan Nurhasan
- Dilakukan ketika gabut 😴

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=aliridwan&repo=anjayhd&label=Views&color=ff6b81&style=flat" alt="Profile views">
</p>

<p align="center">
  <sub>Dibuat dengan ❤️ dan 🌸</sub>
</p>
