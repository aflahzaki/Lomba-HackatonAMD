# LangkahKampus - Platform Prediksi SNBP

<p align="center">
  <img src="assets/images/logo.png" alt="LangkahKampus Logo" width="120">
</p>

## Tentang

**LangkahKampus** adalah platform prediksi penerimaan SNBP (Seleksi Nasional Berdasarkan Prestasi) berbasis Machine Learning untuk siswa SMA/SMK/MA di Indonesia. Platform ini membantu siswa memprediksi peluang diterima di program studi pilihan mereka berdasarkan data akademik, peringkat sekolah, dan faktor-faktor relevan lainnya.

## Fitur Utama

- **Prediksi SNBP dengan AI** - Analisis probabilitas diterima menggunakan algoritma Gradient Boosting Machine
- **Rekomendasi Program Studi** - Saran program studi yang sesuai dengan profil akademik siswa
- **Peta Universitas Interaktif** - Visualisasi lokasi PTN di seluruh Indonesia dengan Leaflet.js
- **Anti Bentrok** - Validasi kombinasi pilihan prodi agar tidak saling memblokir
- **Validator Dokumen** - Pemeriksaan kelengkapan berkas pendaftaran SNBP
- **Dashboard Guru BK** - Monitoring dan pembimbingan siswa oleh Guru Bimbingan Konseling
- **Sistem Pembayaran** - Fitur premium dengan berbagai metode pembayaran
- **Animasi Interaktif** - Particle background, scroll animations (AOS), dan gauge animasi

## Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Backend | PHP 8.x (Vanilla PHP) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Database | MySQL 5.7+ / MariaDB 10.3+ |
| Web Server | Apache (dengan mod_rewrite) atau Nginx |
| Maps | Leaflet.js |
| Animations | AOS (Animate On Scroll), Custom CSS Animations |
| Icons | Font Awesome 6.x |
| Fonts | Google Fonts (Inter, Poppins) |

## Persyaratan Sistem

- PHP >= 8.0 dengan ekstensi: `pdo`, `pdo_mysql`, `mbstring`, `json`
- MySQL >= 5.7 atau MariaDB >= 10.3
- Apache >= 2.4 dengan `mod_rewrite` aktif, atau Nginx
- Web browser modern (Chrome, Firefox, Edge, Safari)
- XAMPP / WAMP / LAMP / MAMP (untuk pengembangan lokal)

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/your-username/LangkahKampus.git
cd LangkahKampus/website
```

### 2. Setup Database

1. Buka **phpMyAdmin** (`http://localhost/phpmyadmin`)
2. Buat database baru dengan nama `langkahkampus` (atau langsung import file schema)
3. Import file `database/schema.sql`:
   - Klik tab **Import**
   - Pilih file `database/schema.sql`
   - Klik **Go/Execute**
4. Import data demo `database/seed_data.sql`:
   - Klik tab **Import**
   - Pilih file `database/seed_data.sql`
   - Klik **Go/Execute**

### 3. Konfigurasi Database

Edit file `website/config/database.php` sesuai pengaturan MySQL Anda:

```php
define('DB_HOST', 'localhost');
define('DB_PORT', '3306');
define('DB_NAME', 'langkahkampus');
define('DB_USER', 'root');
define('DB_PASS', '');  // Isi password MySQL Anda jika ada
```

### 4. Konfigurasi Web Server

**Menggunakan XAMPP:**
- Salin folder `website/` ke `C:/xampp/htdocs/langkahkampus/`
- Akses via `http://localhost/langkahkampus/`

**Menggunakan PHP Built-in Server:**
```bash
cd website
php -S localhost:8000
```
Akses via `http://localhost:8000`

### 5. Mulai Menggunakan

Buka browser dan akses URL yang telah dikonfigurasi. Gunakan akun demo di bawah untuk login.

## Struktur Direktori

```
LangkahKampus/
├── database/
│   ├── schema.sql              # Skema database (tabel, index, relasi)
│   └── seed_data.sql           # Data demo untuk pengembangan
├── website/
│   ├── index.php               # Halaman beranda
│   ├── api/
│   │   ├── auth.php            # API autentikasi (login/register/logout)
│   │   ├── predict.php         # API prediksi SNBP
│   │   ├── recommend.php       # API rekomendasi prodi
│   │   └── search_programs.php # API pencarian program studi
│   ├── assets/
│   │   ├── css/
│   │   │   ├── style.css       # Stylesheet utama
│   │   │   └── animations.css  # Animasi dan transisi
│   │   ├── js/
│   │   │   ├── main.js         # JavaScript utama
│   │   │   ├── predictions.js  # Logika prediksi dan search
│   │   │   ├── dashboard.js    # Fungsi dashboard
│   │   │   └── maps.js         # Peta interaktif
│   │   └── images/
│   │       └── logo.png        # Logo LangkahKampus
│   ├── config/
│   │   ├── app.php             # Konfigurasi aplikasi
│   │   └── database.php        # Konfigurasi koneksi database
│   ├── includes/
│   │   ├── header.php          # Template header
│   │   ├── footer.php          # Template footer
│   │   ├── functions.php       # Fungsi-fungsi utilitas
│   │   └── auth_middleware.php # Middleware autentikasi
│   └── pages/
│       ├── login.php           # Halaman login
│       ├── register.php        # Halaman pendaftaran
│       ├── dashboard_student.php # Dashboard siswa
│       ├── prediksi.php        # Halaman prediksi SNBP
│       ├── rekomendasi.php     # Halaman rekomendasi prodi
│       ├── anti_bentrok.php    # Validator anti bentrok
│       ├── peta_universitas.php # Peta universitas
│       ├── validator.php       # Validator dokumen
│       ├── pembayaran.php      # Halaman pembayaran
│       ├── profil.php          # Profil pengguna
│       ├── dashboard_guru.php  # Dashboard guru
│       └── tentang.php         # Halaman tentang
└── README.md
```

## Kredensial Demo

Semua akun demo menggunakan password yang sama: **`password123`**

| Email | Nama | Peran |
|-------|------|-------|
| `ahmad.faiz@student.sman3jkt.sch.id` | Ahmad Faiz Pratama | Siswa (Premium) |
| `siti.nurhaliza@student.sman3bdg.sch.id` | Siti Nurhaliza Putri | Siswa |
| `dewi.anggraeni@student.sman5sby.sch.id` | Dewi Anggraeni | Siswa (Premium) |
| `budi.santoso@student.sman1yk.sch.id` | Budi Santoso | Siswa |
| `rina.wulandari@student.sman1smg.sch.id` | Rina Wulandari | Siswa |
| `bu.ratna@sman3jkt.sch.id` | Dr. Ratna Sari Dewi | Guru BK |
| `pak.bambang@sman3bdg.sch.id` | Bambang Supriyanto, M.Pd. | Guru BK |
| `admin.sman3jkt@sman3jkt.sch.id` | Hendra Wijaya | Admin Sekolah |
| `admin.sman3bdg@sman3bdg.sch.id` | Rina Marlina | Admin Sekolah |
| `superadmin@langkahkampus.id` | Muhammad Rizki Fauzan | Platform Admin |

## Fitur dan Deskripsi

### Prediksi SNBP
Siswa memasukkan nilai rapor semester 1-5, peringkat sekolah, dan akreditasi. Sistem menghitung probabilitas diterima di program studi pilihan menggunakan model Gradient Boosting Machine dengan visualisasi gauge animasi dan confidence interval.

### Rekomendasi Program Studi
Berdasarkan profil kognitif dan preferensi siswa, sistem memberikan rekomendasi program studi yang cocok dari 10 PTN terkemuka dengan penjelasan faktor kecocokan.

### Peta Universitas
Peta interaktif Indonesia yang menampilkan lokasi 10 PTN terkemuka. Klik marker untuk melihat detail universitas, program studi, dan informasi akreditasi.

### Anti Bentrok
Fitur validasi yang memeriksa apakah kombinasi pilihan 1 dan pilihan 2 SNBP saling memblokir. Beberapa program studi (terutama Kedokteran) hanya bisa dipilih di pilihan 1.

### Dashboard Siswa
Ringkasan profil akademik, riwayat prediksi, progress kelengkapan berkas, dan notifikasi. Dilengkapi grafik perkembangan nilai per semester.

### Sistem Pembayaran
Integrasi pembayaran untuk fitur premium dengan opsi: transfer bank, e-wallet (GoPay, OVO, DANA), dan QRIS.

## Lisensi

Hak cipta (c) 2024 LangkahKampus. Seluruh hak dilindungi.

---

<p align="center">
  Dibuat dengan untuk siswa Indonesia
</p>
