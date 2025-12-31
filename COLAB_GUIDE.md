# 📘 Panduan Menggunakan di Google Colab

Panduan lengkap untuk menjalankan YouTube Viral Clipper di Google Colab.

## 🚀 Keuntungan Menggunakan Google Colab

✅ **GPU Gratis** - Akses GPU T4 gratis untuk processing yang lebih cepat (tested & compatible!)  
✅ **Tidak Perlu Install** - Semua dependencies terinstall otomatis  
✅ **Cloud-based** - Tidak memakan resource komputer lokal  
✅ **Mudah Download** - Download hasil langsung dari browser  
✅ **No Errors** - Menggunakan MediaPipe 0.8.10 (stable version, no AttributeError!)

## 📋 Langkah-langkah (Super Simple!)

### 1. Buka Notebook di Google Colab

**Opsi A: Via GitHub (Recommended)**
- Kunjungi link ini: `https://colab.research.google.com/github/portdigital/testing-AI-Clipping-Software/blob/main/colab_notebook.ipynb`
- Atau ganti `portdigital/testing-AI-Clipping-Software` dengan repository Anda

**Opsi B: Upload Manual**
- Buka: https://colab.research.google.com/
- Login dengan akun Google Anda
- Klik **File** → **Upload notebook**
- Upload file `colab_notebook.ipynb`

### 2. Aktifkan GPU (PENTING!)

- Klik **Runtime** → **Change runtime type**
- Pilih **Hardware accelerator: T4 GPU**
- Klik **Save**

### 3. Jalankan CELL 1: Setup & Instalasi

**Jalankan cell ini SEKALI saja** (hanya pertama kali atau setelah restart runtime)

1. Klik tombol **Play** (▶️) di Cell 1 atau tekan `Shift + Enter`
2. Proses akan berjalan 2-3 menit dan melakukan:
   - ✅ Install semua dependencies dengan smart check
   - ✅ Install MediaPipe 0.8.10 (stable version - no errors!)
   - ✅ Clone repository dari GitHub
   - ✅ Setup Gemini API key (Anda akan diminta input API key)
   - ✅ Test semua imports
   - ✅ Check GPU availability
   
3. **Masukkan Gemini API Key**:
   - Dapatkan API key gratis di: https://aistudio.google.com/app/apikey
   - Copy-paste API key Anda saat diminta
   
4. Tunggu sampai muncul: **"✅ SETUP COMPLETE! Ready to generate viral clips!"**

**💡 Catatan:**
- Jika ada warning tentang protobuf conflicts, **abaikan saja**. Itu normal dan tidak mengganggu.
- Jika MediaPipe gagal, restart runtime dan jalankan Cell 1 lagi.
- Setelah setup berhasil, Anda **tidak perlu** menjalankan Cell 1 lagi.

### 4. Jalankan CELL 2: Generate Video Clips

**Jalankan cell ini untuk membuat klip viral** (bisa diulang berkali-kali dengan video berbeda!)

1. Klik tombol **Play** (▶️) di Cell 2
2. Masukkan informasi yang diminta:
   - **🔗 YouTube URL**: Link video YouTube
   - **🎯 Number of clips**: Berapa klip yang ingin dibuat (default: 3)
   - **⏱️ Min duration**: Durasi minimum klip (detik, default: 30)
   - **⏱️ Max duration**: Durasi maximum klip (detik, default: 60)
   - **🎨 Caption style**: Pilih style 1-5 (default: 1 = MrBeast style)

3. Proses akan berjalan otomatis:
   ```
   🎬 Downloading video from YouTube...
   ✂️ Transcribing audio with Whisper AI...
   🤖 AI selecting best viral clips with Gemini...
   🎯 Smart face tracking and cropping to 9:16...
   📝 Adding word-by-word captions...
   💾 Exporting final clips...
   ```

4. Setelah selesai:
   - File ZIP akan otomatis terdownload ke komputer Anda
   - Isinya: Semua video clips yang sudah jadi
   - Siap diupload ke TikTok, Instagram, YouTube Shorts!

5. **Ingin process video lain?** Jalankan Cell 2 lagi dengan URL baru!

## ⚙️ Struktur Notebook (2 Cell Saja!)

Notebook ini dirancang **super simple** dengan hanya **2 cell**:

### 📦 Cell 1: Setup & Instalasi
- Jalankan **SEKALI** saja (atau setelah restart runtime)
- Install semua dependencies
- MediaPipe 0.8.10 (stable, no errors!)
- Setup API key & repository
- ~2-3 menit

### 🎬 Cell 2: Generate Video
- Jalankan **BERKALI-KALI** untuk video berbeda
- Input video URL & preferences
- Process & download otomatis
- ~3-10 menit (tergantung panjang video)

## 🎨 Caption Styles yang Tersedia

1. **MrBeast** - Bold, kuning, stroke hitam tebal
2. **Alex Hormozi** - Modern, besar, font sans-serif
3. **Minimalist** - Simple, elegan, tidak ramai
4. **Energetic** - Warna-warni, fun, eye-catching
5. **Professional** - Clean, corporate, subtle

## 🔧 Troubleshooting

### ❌ Error: "No module named 'services'"
**Solusi**: Jalankan ulang Cell 1. Pastikan clone repository berhasil.

### ❌ Error: "GEMINI_API_KEY not found"
**Solusi**: 
1. Jalankan Cell 1 lagi dan masukkan API key yang benar
2. Get free API key: https://aistudio.google.com/app/apikey

### ❌ Error: MediaPipe AttributeError
**Solusi**: Notebook baru sudah menggunakan MediaPipe 0.8.10 (stable). Error ini TIDAK akan muncul lagi.

Jika masih error:
1. **Runtime → Restart runtime**
2. Jalankan Cell 1 lagi
3. Seharusnya langsung work!

### ❌ Video Download Gagal
**Solusi**:
1. Cek apakah video YouTube bisa diakses (tidak private/restricted)
2. Coba video lain
3. Pastikan video tidak terlalu panjang (max 2 jam)

### ⚠️ GPU Tidak Terdeteksi
**Solusi**:
1. **Runtime → Change runtime type**
2. Pilih **Hardware accelerator: T4 GPU**
3. Klik **Save**
4. Jalankan Cell 1 lagi

### ⏱️ Process Terlalu Lama?
**Tips untuk processing lebih cepat**:
- Gunakan video yang lebih pendek (5-20 menit ideal)
- Kurangi jumlah clips (misal: 2-3 clips)
- Kurangi max_duration clips (misal: 45-50 detik)
- Pastikan GPU sudah aktif (T4 GPU)

### ⚠️ Warning tentang protobuf conflicts
**Solusi**: **Abaikan saja!** Warning ini normal dan tidak mengganggu. MediaPipe akan tetap bekerja dengan baik.

## 💡 Tips & Best Practices

1. **Gunakan GPU T4** - Processing jadi 3-5x lebih cepat
2. **Video pendek lebih baik** - 5-20 menit ideal untuk hasil cepat
3. **Test dulu dengan 1-2 clips** - Sebelum generate banyak clips
4. **Pilih video dengan speaker jelas** - Face tracking akan lebih akurat
5. **Simpan API key** - Agar tidak perlu input ulang setiap kali
6. **Restart runtime jika error** - Selesaikan kebanyakan masalah

## 📝 Catatan Penting

- **Free tier Colab**: Limit 12 jam runtime, GPU terbatas
- **File akan hilang**: Setelah runtime disconnect (kecuali saved to Drive)
- **API key Gemini**: Gratis dengan quota generous
- **GPU availability**: Tergantung demand, kadang harus tunggu

## 🎯 Quick Start (TL;DR)

1. Buka notebook di Colab
2. Aktifkan GPU T4
3. Jalankan Cell 1 (setup, input API key)
4. Jalankan Cell 2 (input YouTube URL, generate!)
5. Download ZIP file hasil
6. Upload ke social media, go viral! 🚀

Selamat mencoba! 🎉
