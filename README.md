# LangkahKampus - AI-Powered SNBP Admission Predictor

LangkahKampus adalah platform prediksi penerimaan SNBP (Seleksi Nasional Berdasarkan Prestasi) berbasis Machine Learning yang membantu siswa SMA/SMK/MA Indonesia dalam merencanakan strategi pendaftaran perguruan tinggi.

## Hackathon

**AMD Hackathon ACT II - Unicorn Track**

Platform ini memanfaatkan AI/ML untuk memberikan prediksi probabilitas penerimaan yang akurat, rekomendasi program studi alternatif, dan AI Advisor berbasis LLM untuk konsultasi strategi SNBP.

## Arsitektur Sistem

```
                    +-----------------+
                    |   PHP Frontend  |
                    |  (Apache:8080)  |
                    +--------+--------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+      +-----------v-----------+
    |    AI Backend      |      |       MySQL           |
    | (FastAPI:8000)     |      |    (port 3306)        |
    +--------------------+      +-----------------------+
```

- **PHP Frontend** (Apache): Antarmuka pengguna dengan form prediksi, visualisasi hasil, dan chat AI Advisor
- **AI Backend** (FastAPI/Python): Model ML (XGBoost/GradientBoosting) untuk prediksi, rekomendasi cerdas, dan integrasi Fireworks AI untuk advisor chatbot
- **MySQL 8.0**: Database dengan data SIDATA PTN (84 universitas, 3058 program studi)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | PHP 8.2, Vanilla JavaScript, CSS3 |
| AI Backend | Python 3.10, FastAPI, scikit-learn, XGBoost |
| Database | MySQL 8.0 |
| LLM Integration | Fireworks AI (Llama 3.1 8B Instruct) |
| Containerization | Docker, Docker Compose |
| Web Server | Apache 2 |

## Fitur Utama

1. **Prediksi ML SNBP** - Model Machine Learning yang memprediksi probabilitas penerimaan berdasarkan 6 variabel (rasio kompetisi, tren peminat, nilai rata-rata, peringkat, akreditasi, daya tampung)
2. **Rekomendasi Cerdas** - Algoritma pencarian program studi alternatif dengan kompetisi lebih rendah
3. **AI Advisor** - Chatbot berbasis LLM (Fireworks AI) untuk konsultasi strategi SNBP
4. **Anti-Bentrok** - Statistik siswa lain yang memilih program studi yang sama
5. **Choice-2 Trap Warning** - Peringatan otomatis untuk program yang memblokir pilihan kedua
6. **Peta Universitas** - Visualisasi interaktif lokasi PTN di Indonesia
7. **Fallback Deterministik** - Jika AI backend tidak tersedia, sistem menggunakan formula deterministik sebagai cadangan

## AMD Platform Integration

LangkahKampus memanfaatkan ekosistem AMD secara menyeluruh - dari training model hingga inference LLM.

### Training on AMD Developer Cloud

Model XGBoost di-training menggunakan **AMD Instinct MI210** (64GB HBM2e) di AMD Developer Cloud dengan ROCm platform:

```python
# ai_backend/training/train_on_amd_cloud.py
model = XGBRegressor(
    tree_method="hist",      # GPU-accelerated histogram method
    device="cuda",           # Works with AMD ROCm via HIP compatibility
    n_estimators=200,
    max_depth=6,
)
```

- **Auto-detection:** Script mendeteksi ROCm via `/opt/rocm`, `HIP_VISIBLE_DEVICES`, dan `rocm-smi`
- **Performance:** 5-10x speedup dibanding CPU training
- **Hardware:** Support MI210 (64GB) dan MI250X (128GB, 3.2 TB/s bandwidth)
- **Compatibility:** `device="cuda"` bekerja di AMD GPU melalui HIP compatibility layer

### LLM Inference via Fireworks AI (AMD GPU Infrastructure)

AI Advisor menggunakan **Fireworks AI**, yang memanfaatkan infrastruktur GPU AMD untuk inference model **Llama 3.1 8B Instruct**:

- Real-time academic guidance chatbot
- Multi-turn conversation dengan context dari hasil prediksi
- Low-latency responses dari Fireworks AI infrastructure

### Model Performance (Trained on AMD)

| Metric | Value |
|--------|-------|
| R2 Score | 0.9457 |
| MAE | 0.0234 |
| RMSE | 0.0312 |

> Dokumentasi teknis lengkap: [docs/AMD_USAGE.md](docs/AMD_USAGE.md)

## Quick Start

### Prasyarat

- Docker dan Docker Compose terinstall
- (Opsional) API key Fireworks AI untuk fitur AI Advisor

### Menjalankan dengan Docker

1. Clone repository:
```bash
git clone https://github.com/aflahzaki/Lomba-HackatonAMD.git
cd Lomba-HackatonAMD
```

2. Buat file `.env` dari template:
```bash
cp .env.example .env
```

3. (Opsional) Edit `.env` dan masukkan API key Fireworks AI:
```
FIREWORKS_API_KEY=your_actual_api_key
```

4. Build dan jalankan semua service:
```bash
docker compose up --build
```

5. Akses aplikasi:
   - Frontend: http://localhost:8080
   - AI Backend API: http://localhost:8000
   - AI Health Check: http://localhost:8000/api/health

### Menghentikan Service

```bash
docker compose down
```

Untuk menghapus data MySQL (reset database):
```bash
docker compose down -v
```

## Environment Variables

| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `MYSQL_ROOT_PASSWORD` | `langkahkampus` | Password root MySQL |
| `MYSQL_DATABASE` | `langkahkampus` | Nama database |
| `FIREWORKS_API_KEY` | (kosong) | API key untuk Fireworks AI (AI Advisor) |
| `AI_BACKEND_URL` | `http://ai-backend:8000` | URL Python backend (untuk PHP) |

## API Documentation

### AI Backend Endpoints

#### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "sidata_loaded": true,
  "programs_count": 3058
}
```

#### `POST /api/predict`
Prediksi probabilitas penerimaan SNBP.

**Request:**
```json
{
  "scores": {
    "Matematika": {"sem1": 85, "sem2": 87, "sem3": 88, "sem4": 90, "sem5": 91},
    "Fisika": {"sem1": 80, "sem2": 82, "sem3": 84, "sem4": 85, "sem5": 86}
  },
  "school_ranking": 5,
  "total_students": 200,
  "school_accreditation": "A",
  "target_program_id": "TEKNIK INFORMATIKA"
}
```

**Response:**
```json
{
  "probability": 72.5,
  "confidence_lower": 0.65,
  "confidence_upper": 0.80,
  "variables": [...],
  "recommendations": [...],
  "input_summary": {...}
}
```

#### `POST /api/recommend`
Rekomendasi program studi alternatif.

**Request:**
```json
{
  "target_program": "TEKNIK INFORMATIKA",
  "scores": {"Matematika": {"sem1": 85}},
  "school_ranking": 5,
  "total_students": 200,
  "school_accreditation": "A",
  "limit": 5
}
```

#### `POST /api/advisor`
AI Advisor chatbot.

**Request:**
```json
{
  "message": "Bagaimana strategi memilih prodi SNBP?",
  "context": {
    "probability": 72.5,
    "target_program": "TEKNIK INFORMATIKA"
  }
}
```

**Response:**
```json
{
  "reply": "Berdasarkan analisis...",
  "suggestions": ["Pertanyaan lanjutan 1", "Pertanyaan lanjutan 2"]
}
```

## Fireworks AI Integration

LangkahKampus menggunakan Fireworks AI platform untuk fitur AI Advisor. Model yang digunakan adalah `accounts/fireworks/models/llama-v3p1-8b-instruct`.

AI Advisor dapat:
- Menjelaskan mengapa probabilitas tinggi/rendah
- Memberikan saran strategis pemilihan prodi
- Menjawab pertanyaan tentang SNBP
- Menganalisis konteks dari hasil prediksi

Jika API key tidak dikonfigurasi atau service tidak tersedia, sistem akan memberikan respons fallback yang informatif.

## Pengembangan Lokal (Tanpa Docker)

### PHP Frontend
Membutuhkan PHP 8.x dengan ekstensi `pdo_mysql` dan `curl`, serta web server (Apache/Nginx).

### AI Backend
```bash
cd ai_backend
pip install -r requirements.txt
python training/prepare_data.py
python training/train_model.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database
Import schema dan seed data ke MySQL:
```bash
mysql -u root -p langkahkampus < database/schema.sql
mysql -u root -p langkahkampus < database/seed_data.sql
mysql -u root -p langkahkampus < database/seed_sidata.sql
```

## Struktur Direktori

```
Lomba-HackatonAMD/
├── ai_backend/           # Python AI Backend (FastAPI)
│   ├── app/              # Application code
│   │   ├── main.py       # FastAPI endpoints
│   │   ├── config.py     # Settings
│   │   ├── models/       # ML predictor
│   │   ├── schemas/      # Pydantic models
│   │   └── services/     # Advisor & recommender
│   ├── models/           # Trained ML model (.joblib)
│   ├── training/         # Model training scripts
│   ├── tests/            # Pytest tests
│   ├── Dockerfile        # AI backend container
│   └── requirements.txt  # Python dependencies
├── database/             # Database SQL files
│   ├── schema.sql        # Table definitions
│   ├── seed_data.sql     # Demo data
│   └── seed_sidata.sql   # SIDATA PTN (3058 programs)
├── website/              # PHP Frontend
│   ├── api/              # Backend API endpoints
│   ├── assets/           # CSS, JS, images
│   ├── config/           # Configuration files
│   ├── includes/         # Shared PHP (header, footer)
│   └── pages/            # Page templates
├── docker-compose.yml    # Multi-container orchestration
├── Dockerfile.php        # PHP frontend container
├── .env.example          # Environment template
└── README.md             # This file
```

## Submission

Dokumentasi lengkap untuk hackathon submission:

| Dokumen | Deskripsi |
|---------|-----------|
| [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) | Panduan step-by-step untuk submission (registrasi, API key, video, form) |
| [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md) | Script detail video demo 3-5 menit (timing, narasi, screen notes) |
| [docs/SLIDE_OUTLINE.md](docs/SLIDE_OUTLINE.md) | Outline presentasi 10 slides dengan talking points |
| [docs/AMD_USAGE.md](docs/AMD_USAGE.md) | Dokumentasi teknis penggunaan AMD platform |

### Quick Links

- **GitHub:** https://github.com/aflahzaki/Lomba-HackatonAMD
- **Demo Script:** `python demo/demo_script.py --mock`
- **AMD Developer Cloud:** https://developer.amd.com/
- **Fireworks AI:** https://fireworks.ai/

## Lisensi

Dibuat untuk AMD Hackathon ACT II - Unicorn Track.
