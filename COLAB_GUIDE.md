# 📘 Panduan Menggunakan di Google Colab

Panduan lengkap untuk menjalankan YouTube Viral Clipper di Google Colab.

## 🚀 Keuntungan Menggunakan Google Colab

✅ **GPU Gratis** - Akses GPU T4 gratis untuk processing yang lebih cepat  
✅ **Tidak Perlu Install** - Semua dependencies terinstall otomatis  
✅ **Cloud-based** - Tidak memakan resource komputer lokal  
✅ **Mudah Download** - Download hasil langsung dari browser  

## 📋 Langkah-langkah

### 1. Buka Google Colab
- Kunjungi: https://colab.research.google.com/
- Login dengan akun Google Anda

### 2. Upload Notebook
- Klik **File** → **Upload notebook**
- Upload file `colab_notebook.ipynb`
- Atau buka langsung dari GitHub jika sudah di-upload

### 3. Aktifkan GPU (Recommended)
- Klik **Runtime** → **Change runtime type**
- Pilih **GPU** di Hardware accelerator
- Klik **Save**

### 4. Setup Kode Aplikasi

**Opsi A: Clone dari GitHub (Recommended)**
```python
# Edit cell "Clone dari GitHub"
!git clone https://github.com/your-username/youtube-viral-clipper.git
%cd youtube-viral-clipper
```

**Opsi B: Upload File Manual**
- Jalankan cell "Create Directory Structure"
- Jalankan cell "Upload Files"
- Upload semua file:
  - `config.py`
  - `main.py`
  - Semua file di folder `services/`
  - Semua file di folder `styles/`
  - Semua file di folder `utils/`

### 5. Setup API Key
- Jalankan cell "Setup API Key"
- Masukkan Gemini API Key Anda
- Dapatkan API key di: https://makersuite.google.com/app/apikey

### 6. Jalankan Aplikasi
- Jalankan cell "Jalankan Aplikasi"
- Masukkan:
  - YouTube URL
  - Jumlah klip
  - Durasi maksimal/minimal
  - Style caption

### 7. Download Hasil
- Jalankan cell "Download Hasil"
- File akan otomatis terdownload sebagai ZIP

## ⚙️ Konfigurasi Tambahan

### Menggunakan Model Whisper Lebih Kecil (Lebih Cepat)
Edit cell "Setup API Key" dan tambahkan:
```python
f.write('WHISPER_MODEL=tiny\n')  # atau 'base', 'small'
```

### Menggunakan Model Whisper Lebih Besar (Lebih Akurat)
```python
f.write('WHISPER_MODEL=large-v2\n')
```

## 🔧 Troubleshooting

### Error: "Module not found"
- Pastikan semua file sudah terupload dengan benar
- Restart runtime: **Runtime** → **Restart runtime**

### Error: "CUDA out of memory"
- Gunakan model Whisper yang lebih kecil (`tiny` atau `base`)
- Atau restart runtime dan coba lagi

### Video download gagal
- Coba video YouTube lain
- Pastikan video tidak private atau age-restricted

### Processing terlalu lama
- Gunakan GPU (Runtime → Change runtime type → GPU)
- Gunakan model Whisper yang lebih kecil
- Pilih video yang lebih pendek

## 💡 Tips

1. **Gunakan GPU** untuk processing 3-5x lebih cepat
2. **Video pendek** (5-10 menit) akan diproses lebih cepat
3. **Model 'tiny'** untuk testing cepat, 'medium' untuk hasil terbaik
4. **Simpan notebook** ke Google Drive untuk digunakan lagi nanti

## 📝 Catatan

- Colab free tier memiliki batasan waktu runtime (12 jam)
- GPU mungkin tidak selalu tersedia (tergantung demand)
- File di Colab akan hilang setelah runtime disconnect (kecuali disimpan ke Drive)

## 🎯 Quick Start

1. Upload `colab_notebook.ipynb` ke Colab
2. Aktifkan GPU
3. Clone/upload kode
4. Setup API key
5. Jalankan aplikasi
6. Download hasil

Selamat mencoba! 🚀

