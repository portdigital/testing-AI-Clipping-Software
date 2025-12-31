# 📤 Panduan Upload ke GitHub Repository Sendiri

Panduan untuk mengupload kode ini ke GitHub repository Anda sendiri.

## 🚀 Langkah-langkah

### 1. Buat Repository Baru di GitHub

1. Login ke GitHub: https://github.com
2. Klik tombol **"+"** di kanan atas → **"New repository"**
3. Isi informasi:
   - **Repository name**: `AI-Clipping-Software` (atau nama lain yang Anda inginkan)
   - **Description**: "YouTube Viral Clipper - AI-powered video clipping software"
   - **Visibility**: Pilih **Public** atau **Private**
   - **JANGAN** centang "Initialize with README" (karena kita sudah punya kode)
4. Klik **"Create repository"**

### 2. Ubah Remote Origin

Setelah repository dibuat, GitHub akan menampilkan URL repository Anda. Contoh:
- `https://github.com/USERNAME/AI-Clipping-Software.git`
- atau `git@github.com:USERNAME/AI-Clipping-Software.git`

**Jalankan perintah berikut di terminal:**

```bash
cd /Users/ditusigaming/Documents/developments/AI-Clipping-Software

# Hapus remote origin yang lama
git remote remove origin

# Tambahkan remote origin baru (ganti USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/USERNAME/AI-Clipping-Software.git

# Atau jika menggunakan SSH:
# git remote add origin git@github.com:USERNAME/AI-Clipping-Software.git

# Verifikasi remote sudah benar
git remote -v
```

### 3. Commit Perubahan

```bash
# Tambahkan semua file yang sudah diubah/ditambah
git add .

# Commit perubahan
git commit -m "Update: Fix MediaPipe compatibility and add Colab notebook

- Update face_tracker.py untuk kompatibel dengan MediaPipe versi baru
- Tambahkan colab_notebook.ipynb untuk Google Colab
- Tambahkan COLAB_GUIDE.md untuk panduan penggunaan"

# Atau jika ingin commit terpisah:
git add services/face_tracker.py
git commit -m "Fix: Update face_tracker.py untuk MediaPipe versi baru"

git add colab_notebook.ipynb COLAB_GUIDE.md
git commit -m "Add: Colab notebook dan panduan penggunaan"
```

### 4. Push ke Repository Baru

```bash
# Push ke branch main (atau master jika repository lama)
git push -u origin main

# Jika branch Anda bernama master:
# git push -u origin master
```

### 5. Verifikasi

1. Buka repository Anda di GitHub
2. Pastikan semua file sudah terupload
3. Pastikan `colab_notebook.ipynb` dan `COLAB_GUIDE.md` sudah ada

## 🔄 Update Repository di Masa Depan

Setelah setup pertama kali, untuk update repository:

```bash
# Tambahkan perubahan
git add .

# Commit
git commit -m "Deskripsi perubahan"

# Push
git push
```

## 📝 Catatan Penting

1. **Jangan lupa update README.md** dengan informasi repository Anda
2. **Update colab_notebook.ipynb** - ganti URL GitHub di Cell 1 dengan URL repository Anda
3. **License** - Pastikan Anda menghormati license dari repository asal (cek file LICENSE)

## 🆘 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/AI-Clipping-Software.git
```

### Error: "failed to push some refs"
```bash
# Jika repository baru sudah ada file (README, LICENSE, dll)
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: Authentication failed
- Pastikan sudah login di GitHub
- Atau gunakan Personal Access Token (Settings → Developer settings → Personal access tokens)

## ✅ Checklist

- [ ] Repository baru sudah dibuat di GitHub
- [ ] Remote origin sudah diubah ke repository baru
- [ ] Semua perubahan sudah di-commit
- [ ] Kode sudah di-push ke GitHub
- [ ] README.md sudah diupdate (opsional)
- [ ] colab_notebook.ipynb sudah diupdate dengan URL repository baru (opsional)

Selamat! Kode Anda sekarang sudah di GitHub repository sendiri! 🎉

