# LangkahKampus - Hackathon Submission Guide

Panduan lengkap step-by-step untuk submission AMD Hackathon ACT II - Unicorn Track di platform lablab.ai.

---

## Table of Contents

1. [Registrasi AMD AI Developer Program & lablab.ai](#1-registrasi)
2. [Konfigurasi Fireworks AI API Key](#2-konfigurasi-fireworks-ai-api-key)
3. [Merekam Demo Video](#3-merekam-demo-video)
4. [Mengisi Form Submission lablab.ai](#4-mengisi-form-submission-lablabai)
5. [Pre-Submit Checklist](#5-pre-submit-checklist)

---

## 1. Registrasi

### AMD AI Developer Program

1. Buka [AMD Developer](https://developer.amd.com/)
2. Klik "Join" atau "Sign Up"
3. Isi formulir registrasi dengan informasi yang valid
4. Verifikasi email
5. Setelah login, eksplorasi AMD Developer Cloud untuk akses GPU instances (MI210/MI250X)
6. Request access ke GPU instances jika belum tersedia di akun

### lablab.ai

1. Buka [lablab.ai](https://lablab.ai/)
2. Klik "Sign Up" dan buat akun (bisa menggunakan Google, GitHub, atau email)
3. Setelah login, cari "AMD Hackathon ACT II" di daftar hackathon
4. Klik "Join Hackathon" untuk mendaftar sebagai peserta
5. Buat atau join tim (sesuai aturan hackathon)
6. Pastikan profil tim lengkap (nama, foto, deskripsi)

---

## 2. Konfigurasi Fireworks AI API Key

### Mendapatkan API Key

1. Buka [Fireworks AI](https://fireworks.ai/)
2. Buat akun atau login
3. Navigate ke Dashboard > API Keys
4. Klik "Create API Key"
5. Salin API key yang dihasilkan (simpan dengan aman, tidak akan ditampilkan lagi)

### Mengkonfigurasi di Proyek

1. Copy file template environment:
   ```bash
   cp .env.example .env
   ```

2. Edit file `.env` dan masukkan API key:
   ```
   FIREWORKS_API_KEY=fw_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. Verifikasi konfigurasi dengan menjalankan aplikasi:
   ```bash
   docker compose up --build
   ```

4. Test API key berfungsi dengan mengakses AI Advisor di http://localhost:8080

### Catatan Penting

- API key Fireworks AI gratis dengan quota terbatas (cukup untuk demo)
- Model yang digunakan: `accounts/fireworks/models/llama-v3p1-8b-instruct`
- Jika API key tidak dikonfigurasi, sistem tetap berjalan dengan fallback response
- Jangan commit API key ke repository (sudah ada di `.gitignore`)
- Referensi: lihat `.env.example` untuk template lengkap

---

## 3. Merekam Demo Video

### Spesifikasi Video

- **Durasi:** 3-5 menit (idealnya 4 menit)
- **Format:** MP4, resolusi minimal 1080p
- **Bahasa:** English (juri internasional)
- **Platform upload:** YouTube (unlisted) atau Google Drive

### Persiapan Sebelum Rekam

1. Pastikan aplikasi berjalan (`docker compose up --build`)
2. Buka browser dengan tabs siap:
   - Tab 1: Frontend (http://localhost:8080)
   - Tab 2: API Health (http://localhost:8000/api/health)
   - Tab 3: GitHub repository
   - Tab 4: Evaluation charts (file manager/preview)
3. Gunakan screen recording software (OBS Studio, Loom, atau QuickTime)
4. Resolusi layar: 1920x1080 atau lebih
5. Tutup notifikasi dan aplikasi yang tidak perlu
6. Siapkan narasi (lihat `docs/VIDEO_SCRIPT.md` untuk script detail)

### Urutan Demo

Ikuti urutan dalam `demo/demo_script.py` yang sudah didesain untuk flow optimal:

1. **Introduction (30 detik)** - Title card, perkenalan tim dan produk
2. **Problem Statement (30 detik)** - Masalah yang diselesaikan
3. **Live Demo - Prediction (60 detik)** - Input data siswa, lihat hasil prediksi
4. **Live Demo - AI Advisor (45 detik)** - Chat dengan AI advisor, tunjukkan multi-turn
5. **AMD Integration (45 detik)** - Tunjukkan training script, evaluation metrics, ROCm
6. **Architecture (30 detik)** - Diagram arsitektur, tech stack
7. **Closing (30 detik)** - Summary, call to action

### Tips Recording

- **Gunakan mock mode** untuk demo yang konsisten: `python demo/demo_script.py --mock`
- Bicara dengan pace yang jelas, jangan terlalu cepat
- Zoom in pada bagian penting (probabilitas, chart, kode)
- Tunjukkan terminal output saat demo API
- Highlight bagian AMD-specific di kode (ROCm detection, GPU parameters)
- Tambahkan background music ringan (opsional)
- Export video di 1080p 30fps minimal

---

## 4. Mengisi Form Submission lablab.ai

### Informasi yang Diperlukan

| Field | Isi |
|-------|-----|
| **Project Name** | LangkahKampus - AI-Powered SNBP Admission Predictor |
| **Short Description** | ML-powered platform predicting Indonesian university admission probabilities using XGBoost trained on AMD Instinct GPUs with AI advisor powered by Fireworks AI |
| **GitHub Repository** | https://github.com/aflahzaki/Lomba-HackatonAMD |
| **Demo URL** | URL deployed app (jika ada) atau link video demo |
| **Video URL** | Link YouTube/Google Drive video demo |
| **Slide Deck** | Link Google Slides/PDF presentasi |
| **Cover Image** | Screenshot menarik dari aplikasi (1200x630 px recommended) |
| **Category/Track** | Unicorn Track |
| **Team Members** | Daftar anggota tim |

### Deskripsi Project (Template)

```
LangkahKampus is an AI-powered SNBP (Seleksi Nasional Berdasarkan Prestasi) 
admission predictor for Indonesian high school students. It uses XGBoost ML 
model trained on AMD Developer Cloud GPU (Instinct MI210) with ROCm for 
accelerated training, achieving R2=0.9457. The AI Advisor feature leverages 
Fireworks AI (Llama 3.1 8B), which leverages AMD GPU infrastructure, for real-time academic 
guidance. The platform covers 3,058 programs across 84 universities.

Key AMD Platform Usage:
- Model training on AMD Instinct MI210/MI250X via ROCm
- XGBoost GPU hist acceleration (5-10x speedup)
- LLM inference via Fireworks AI, which leverages AMD GPU infrastructure
- Full ROCm/HIP compatibility for GPU workloads
```

### AMD Platform Usage Description

Pastikan form submission menjelaskan dengan detail bagaimana AMD platform digunakan. Referensi: `docs/AMD_USAGE.md`

---

## 5. Pre-Submit Checklist

### Repository

- [ ] Repository public di GitHub
- [ ] README.md lengkap dan up-to-date
- [ ] `.env.example` ada (tanpa API key actual)
- [ ] Tidak ada API key atau secret yang ter-commit
- [ ] Semua file yang diperlukan ter-commit
- [ ] Code merged to `main` branch (merge `feat/ai-backend-integration` before submission) and buildable
- [ ] License/attribution jelas

### Dokumentasi

- [ ] `SUBMISSION_GUIDE.md` - panduan ini
- [ ] `docs/VIDEO_SCRIPT.md` - script video
- [ ] `docs/SLIDE_OUTLINE.md` - outline presentasi
- [ ] `docs/AMD_USAGE.md` - dokumentasi AMD platform usage
- [ ] README.md memiliki section "AMD Platform Integration"
- [ ] README.md memiliki section "Submission"

### Demo & Video

- [ ] Video demo terekam (3-5 menit)
- [ ] Video sudah di-upload (YouTube/Google Drive)
- [ ] Video menunjukkan semua fitur utama
- [ ] Video menunjukkan AMD integration
- [ ] Audio jelas dan terdengar

### Presentasi

- [ ] Slide deck dibuat (10 slides)
- [ ] Slide deck mencakup problem, solution, demo, AMD, market
- [ ] Slide deck sudah di-upload/dibagikan

### Teknis

- [ ] Aplikasi bisa di-build dengan `docker compose up --build`
- [ ] Health check endpoint berfungsi (`/api/health`)
- [ ] Prediction endpoint berfungsi (`/api/predict`)
- [ ] AI Advisor berfungsi (dengan atau tanpa API key)
- [ ] Demo script berjalan (`python demo/demo_script.py --mock`)

### Form lablab.ai

- [ ] Project name terisi
- [ ] Short description terisi
- [ ] GitHub link terisi dan accessible (public)
- [ ] Video URL terisi
- [ ] Cover image uploaded
- [ ] Team members terdaftar
- [ ] AMD platform usage dijelaskan di deskripsi

---

## Timeline Recommendation

| Waktu | Aktivitas |
|-------|-----------|
| H-3 | Finalisasi kode, push ke GitHub |
| H-2 | Rekam demo video, buat slide deck |
| H-1 | Review semua material, minta feedback tim |
| H-0 | Submit di lablab.ai, double-check semua link |

---

## Kontak & Resources

- **AMD Developer Cloud:** https://developer.amd.com/
- **Fireworks AI:** https://fireworks.ai/
- **lablab.ai:** https://lablab.ai/
- **ROCm Documentation:** https://rocm.docs.amd.com/
- **XGBoost GPU Guide:** https://xgboost.readthedocs.io/en/latest/gpu/index.html
