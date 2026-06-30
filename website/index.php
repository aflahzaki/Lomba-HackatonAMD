<?php
$page_title = 'Beranda';
include 'includes/header.php';
?>

<!-- Hero Section -->
<section class="hero">
    <canvas id="particleCanvas" class="hero-canvas"></canvas>
    <div class="hero-content">
        <img src="assets/images/logo.png" alt="LangkahKampus" class="hero-logo" data-aos="zoom-in">
        <h1 class="hero-title" data-aos="fade-up" data-aos-delay="200"><?php echo APP_NAME; ?></h1>
        <div class="hero-typing" id="heroTyping" data-aos="fade-up" data-aos-delay="400"></div>
        <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="600">
            Platform prediksi penerimaan SNBP berbasis Machine Learning yang membantu siswa SMA/SMK/MA 
            memaksimalkan peluang diterima di universitas impian.
        </p>
        <div class="hero-buttons" data-aos="fade-up" data-aos-delay="800">
            <a href="pages/prediksi.php" class="btn btn-primary btn-lg btn-ripple">
                <i class="fas fa-rocket"></i> Mulai Prediksi
            </a>
            <a href="#fitur" class="btn btn-outline btn-lg">
                <i class="fas fa-info-circle"></i> Pelajari Fitur
            </a>
        </div>
        <div class="hero-stats-row" data-aos="fade-up" data-aos-delay="1000">
            <div class="hero-stat">
                <div class="hero-stat-number" data-counter="40000" data-suffix="+">0</div>
                <div class="hero-stat-label">Sekolah Terdaftar</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-number" data-counter="500000" data-suffix="+">0</div>
                <div class="hero-stat-label">Siswa Pengguna</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-number" data-counter="95" data-suffix="%">0</div>
                <div class="hero-stat-label">Akurasi Prediksi</div>
            </div>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="section" id="fitur">
    <div class="container">
        <div class="section-header" data-aos="fade-up">
            <h2>Fitur Unggulan</h2>
            <p>Didukung teknologi Machine Learning terdepan untuk membantu keputusan akademik Anda</p>
        </div>

        <div class="features-grid">
            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="100">
                <div class="feature-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h3>Prediksi ML</h3>
                <p>Prediksi peluang penerimaan SNBP menggunakan model Gradient Boosting dengan akurasi tinggi berdasarkan data historis.</p>
            </div>

            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="200">
                <div class="feature-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3>Anti-Bentrok</h3>
                <p>Lihat berapa banyak siswa dari sekolahmu yang memilih program studi yang sama. Informasi statistik untuk strategi SNBP.</p>
            </div>

            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="300">
                <div class="feature-icon">
                    <i class="fas fa-lightbulb"></i>
                </div>
                <h3>Rekomendasi What-If</h3>
                <p>Temukan alternatif program studi terbaik dengan analisis counterfactual berbasis DiCE framework.</p>
            </div>

            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="400">
                <div class="feature-icon">
                    <i class="fas fa-map-marked-alt"></i>
                </div>
                <h3>Peta Universitas</h3>
                <p>Visualisasi interaktif seluruh PTN di Indonesia dengan filter radius, provinsi, dan akreditasi.</p>
            </div>

            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="500">
                <div class="feature-icon">
                    <i class="fas fa-check-double"></i>
                </div>
                <h3>Hard-Rule Validator</h3>
                <p>Validasi pilihan 1 dan 2 secara instan. Deteksi blocking rules dan persyaratan akreditasi otomatis.</p>
            </div>

            <div class="feature-card hover-lift" data-aos="fade-up" data-aos-delay="600">
                <div class="feature-icon">
                    <i class="fas fa-chalkboard-teacher"></i>
                </div>
                <h3>Evaluasi Guru</h3>
                <p>Guru BK terhubung dapat memberikan evaluasi dan saran langsung kepada siswa melalui kode undangan.</p>
            </div>
        </div>
    </div>
</section>

<!-- Statistics Section -->
<section class="stats-section">
    <div class="container">
        <div class="stats-grid">
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="100">
                <div class="stat-number" data-counter="40000" data-suffix="+">0</div>
                <div class="stat-label">Sekolah Partner</div>
            </div>
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="200">
                <div class="stat-number" data-counter="500000" data-suffix="+">0</div>
                <div class="stat-label">Siswa Terdaftar</div>
            </div>
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="300">
                <div class="stat-number" data-counter="95" data-suffix="%">0</div>
                <div class="stat-label">Akurasi Prediksi</div>
            </div>
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="400">
                <div class="stat-number" data-counter="4500" data-suffix="+">0</div>
                <div class="stat-label">Program Studi</div>
            </div>
        </div>
    </div>
</section>

<!-- How It Works Section -->
<section class="section">
    <div class="container">
        <div class="section-header" data-aos="fade-up">
            <h2>Cara Kerja</h2>
            <p>Tiga langkah mudah untuk mengetahui peluang SNBP Anda</p>
        </div>

        <div class="steps-grid">
            <div class="step-card" data-aos="fade-up" data-aos-delay="100">
                <div class="step-number">1</div>
                <h3>Masukkan Data Akademik</h3>
                <p>Input nilai rapor semester 1-5, peringkat sekolah, dan akreditasi. Sistem akan menganalisis profil akademik Anda.</p>
            </div>

            <div class="step-card" data-aos="fade-up" data-aos-delay="200">
                <div class="step-number">2</div>
                <h3>Pilih Program Studi</h3>
                <p>Cari dan pilih program studi serta universitas yang Anda targetkan dari database lengkap PTN se-Indonesia.</p>
            </div>

            <div class="step-card" data-aos="fade-up" data-aos-delay="300">
                <div class="step-number">3</div>
                <h3>Lihat Hasil Prediksi</h3>
                <p>Dapatkan probabilitas penerimaan, confidence interval, dan rekomendasi alternatif dalam hitungan detik.</p>
            </div>
        </div>
    </div>
</section>

<!-- Pricing Section -->
<section class="section" id="harga" style="background: var(--color-bg);">
    <div class="container">
        <div class="section-header" data-aos="fade-up">
            <h2>Pilihan Paket</h2>
            <p>Mulai gratis atau upgrade untuk fitur prediksi dan rekomendasi yang lebih mendalam</p>
        </div>

        <div class="pricing-grid">
            <div class="pricing-card" data-aos="fade-up" data-aos-delay="100">
                <div class="pricing-name">Prediksi Dasar</div>
                <div class="pricing-price">Rp15.000 <span>/prediksi</span></div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> 1x prediksi probabilitas</li>
                    <li><i class="fas fa-check"></i> Confidence interval</li>
                    <li><i class="fas fa-check"></i> Feature importance chart</li>
                    <li><i class="fas fa-check"></i> Peta universitas</li>
                    <li class="disabled"><i class="fas fa-times"></i> Rekomendasi What-If</li>
                    <li class="disabled"><i class="fas fa-times"></i> Anti-Bentrok Dashboard</li>
                </ul>
                <a href="pages/pembayaran.php" class="btn btn-outline btn-block" style="border-color: var(--color-accent-blue); color: var(--color-accent-blue);">
                    Pilih Paket
                </a>
            </div>

            <div class="pricing-card popular" data-aos="fade-up" data-aos-delay="200">
                <div class="pricing-name">Rekomendasi Mendalam</div>
                <div class="pricing-price">Rp25.000 <span>/prediksi</span></div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> Semua fitur Prediksi Dasar</li>
                    <li><i class="fas fa-check"></i> 5 rekomendasi alternatif</li>
                    <li><i class="fas fa-check"></i> Analisis What-If interaktif</li>
                    <li><i class="fas fa-check"></i> Hard-Rule Validator</li>
                    <li><i class="fas fa-check"></i> Simpan riwayat prediksi</li>
                    <li class="disabled"><i class="fas fa-times"></i> Anti-Bentrok Dashboard</li>
                </ul>
                <a href="pages/pembayaran.php" class="btn btn-primary btn-block">
                    Pilih Paket
                </a>
            </div>

            <div class="pricing-card" data-aos="fade-up" data-aos-delay="300">
                <div class="pricing-name">Premium Bulanan</div>
                <div class="pricing-price">Rp49.000 <span>/bulan</span></div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> Prediksi unlimited</li>
                    <li><i class="fas fa-check"></i> Rekomendasi unlimited</li>
                    <li><i class="fas fa-check"></i> Anti-Bentrok Dashboard</li>
                    <li><i class="fas fa-check"></i> Priority support</li>
                    <li><i class="fas fa-check"></i> Export data</li>
                    <li><i class="fas fa-check"></i> Dashboard analytics</li>
                </ul>
                <a href="pages/pembayaran.php" class="btn btn-outline btn-block" style="border-color: var(--color-accent-blue); color: var(--color-accent-blue);">
                    Pilih Paket
                </a>
            </div>
        </div>
    </div>
</section>

<!-- Testimonials Section -->
<section class="section">
    <div class="container">
        <div class="section-header" data-aos="fade-up">
            <h2>Apa Kata Mereka</h2>
            <p>Ribuan siswa sudah merasakan manfaat LangkahKampus</p>
        </div>

        <div class="testimonials-container" data-aos="fade-up" data-aos-delay="200">
            <div class="testimonial-slide active">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "Berkat LangkahKampus, saya bisa tahu peluang saya di Teknik Informatika ITB. Prediksinya akurat dan saya akhirnya diterima! Terima kasih LangkahKampus!"
                    </div>
                    <div class="testimonial-author">Anisa Rahmawati</div>
                    <div class="testimonial-role">Siswa SMAN 3 Bandung - Diterima di ITB</div>
                </div>
            </div>

            <div class="testimonial-slide">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "Fitur Anti-Bentrok sangat membantu saya memahami berapa banyak teman sekolah yang juga memilih prodi yang sama. Jadi saya bisa menyusun strategi pilihan SNBP dengan lebih baik."
                    </div>
                    <div class="testimonial-author">Budi Santoso</div>
                    <div class="testimonial-role">Siswa SMAN 1 Jakarta - Diterima di UI</div>
                </div>
            </div>

            <div class="testimonial-slide">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "Rekomendasi What-If nya keren banget! Saya jadi tahu kalau nilai Matematika saya naik 5 poin, peluang di UI meningkat 20%. Sangat memotivasi!"
                    </div>
                    <div class="testimonial-author">Dimas Pratama</div>
                    <div class="testimonial-role">Siswa SMAN 5 Surabaya - Diterima di UNAIR</div>
                </div>
            </div>

            <div class="testimonial-slide">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "Sebagai guru BK, fitur evaluasi di LangkahKampus memudahkan saya memberikan bimbingan langsung ke siswa. Saya bisa melihat prediksi mereka dan menambahkan komentar."
                    </div>
                    <div class="testimonial-author">Ibu Sari Dewi</div>
                    <div class="testimonial-role">Guru BK SMAN 2 Semarang</div>
                </div>
            </div>

            <div class="testimonial-dots">
                <span class="testimonial-dot active" data-index="0"></span>
                <span class="testimonial-dot" data-index="1"></span>
                <span class="testimonial-dot" data-index="2"></span>
                <span class="testimonial-dot" data-index="3"></span>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="cta-section">
    <div class="container">
        <h2 data-aos="fade-up">Mulai Prediksi Sekarang</h2>
        <p data-aos="fade-up" data-aos-delay="200">
            Jangan biarkan ketidakpastian menghalangi impian kuliah Anda. 
            Gunakan LangkahKampus untuk mengetahui peluang dan memaksimalkan pilihan SNBP Anda.
        </p>
        <a href="pages/register.php" class="btn btn-lg btn-ripple" data-aos="zoom-in" data-aos-delay="400">
            <i class="fas fa-user-plus"></i> Daftar Gratis Sekarang
        </a>
    </div>
</section>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize typing effect for hero
    var typingEl = document.getElementById('heroTyping');
    if (typingEl) {
        initTypingEffect(typingEl, [
            'Prediksi Peluang SNBP Anda dengan AI',
            'Rekomendasi Program Studi Terbaik',
            'Pantau Kuota Real-Time',
            'Raih Universitas Impian Anda'
        ], 80);
    }
});
</script>

<?php include 'includes/footer.php'; ?>
