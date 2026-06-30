<?php
$page_title = 'Tentang Kami';
include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header" style="padding-bottom:3rem;">
        <div class="container text-center">
            <img src="<?php echo $base_path; ?>assets/images/logo.png" alt="<?php echo APP_NAME; ?>" 
                 style="width:80px;height:80px;border-radius:var(--radius-md);margin-bottom:1rem;" data-aos="zoom-in">
            <h1 data-aos="fade-up" data-aos-delay="200">Tentang <?php echo APP_NAME; ?></h1>
            <p data-aos="fade-up" data-aos-delay="400" style="max-width:600px;margin:0 auto;">
                Membantu siswa Indonesia meraih impian kuliah melalui teknologi prediksi berbasis Machine Learning
            </p>
        </div>
    </div>

    <div class="container">
        <!-- Mission Section -->
        <div class="card mb-3" data-aos="fade-up">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:center;">
                <div>
                    <h2 class="mb-2"><i class="fas fa-bullseye text-blue"></i> Misi Kami</h2>
                    <p style="line-height:1.8;color:var(--color-text-light);">
                        LangkahKampus hadir untuk mengurangi kesenjangan informasi dalam proses seleksi SNBP. 
                        Kami percaya bahwa setiap siswa berhak mengetahui peluang mereka dan mendapatkan 
                        bimbingan berbasis data untuk memaksimalkan kesempatan diterima di universitas impian.
                    </p>
                    <p style="line-height:1.8;color:var(--color-text-light);margin-top:1rem;">
                        Melalui pendekatan dual-user (siswa + Guru BK), platform ini tidak hanya membantu individu 
                        tetapi juga mendukung ekosistem bimbingan konseling sekolah secara keseluruhan.
                    </p>
                </div>
                <div class="text-center">
                    <div style="background:linear-gradient(135deg,var(--color-accent-blue),var(--color-primary));border-radius:var(--radius-xl);padding:3rem;color:#fff;">
                        <i class="fas fa-graduation-cap" style="font-size:4rem;margin-bottom:1rem;"></i>
                        <h3 style="color:#fff;">Raih Mimpi</h3>
                        <p style="color:rgba(255,255,255,0.8);">dengan keputusan berbasis data</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Technology Section -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="100">
            <h2 class="mb-3"><i class="fas fa-microchip text-blue"></i> Teknologi di Balik LangkahKampus</h2>
            <div class="features-grid" style="grid-template-columns:repeat(auto-fit,minmax(250px,1fr));">
                <div style="padding:1.5rem;background:var(--color-bg);border-radius:var(--radius-md);">
                    <h4 class="mb-1"><i class="fas fa-brain text-blue"></i> Machine Learning</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Gradient Boosting model dilatih dengan data historis penerimaan SNBP untuk menghasilkan prediksi akurat.</p>
                </div>
                <div style="padding:1.5rem;background:var(--color-bg);border-radius:var(--radius-md);">
                    <h4 class="mb-1"><i class="fas fa-lightbulb text-green"></i> DiCE Framework</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Counterfactual explanations untuk memberikan rekomendasi "What-If" yang actionable kepada siswa.</p>
                </div>
                <div style="padding:1.5rem;background:var(--color-bg);border-radius:var(--radius-md);">
                    <h4 class="mb-1"><i class="fas fa-shield-alt text-red"></i> Real-time Monitoring</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Sistem anti-bentrok memantau kuota program studi secara real-time untuk mencegah penumpukan.</p>
                </div>
                <div style="padding:1.5rem;background:var(--color-bg);border-radius:var(--radius-md);">
                    <h4 class="mb-1"><i class="fas fa-map text-blue"></i> Geospatial Analysis</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Peta interaktif dengan filter radius dan provinsi untuk eksplorasi universitas di seluruh Indonesia.</p>
                </div>
            </div>
        </div>

        <!-- Architecture Overview -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="200">
            <h2 class="mb-3"><i class="fas fa-sitemap text-blue"></i> Arsitektur Sistem</h2>
            <p class="text-muted mb-3">Dibangun menggunakan pendekatan TOGAF Architecture Framework</p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;text-align:center;">
                <div class="card-glass-dark" style="background:rgba(26,115,232,0.05);border-color:rgba(26,115,232,0.2);">
                    <i class="fas fa-layer-group text-blue" style="font-size:2rem;margin-bottom:0.5rem;"></i>
                    <h5>Frontend</h5>
                    <small class="text-muted">PHP, HTML5, CSS3, JS</small>
                </div>
                <div class="card-glass-dark" style="background:rgba(39,174,96,0.05);border-color:rgba(39,174,96,0.2);">
                    <i class="fas fa-server text-green" style="font-size:2rem;margin-bottom:0.5rem;"></i>
                    <h5>Backend API</h5>
                    <small class="text-muted">FastAPI (Python)</small>
                </div>
                <div class="card-glass-dark" style="background:rgba(243,156,18,0.05);border-color:rgba(243,156,18,0.2);">
                    <i class="fas fa-brain" style="font-size:2rem;margin-bottom:0.5rem;color:var(--color-warning);"></i>
                    <h5>ML Engine</h5>
                    <small class="text-muted">Scikit-learn, XGBoost</small>
                </div>
                <div class="card-glass-dark" style="background:rgba(192,57,43,0.05);border-color:rgba(192,57,43,0.2);">
                    <i class="fas fa-database text-red" style="font-size:2rem;margin-bottom:0.5rem;"></i>
                    <h5>Database</h5>
                    <small class="text-muted">MySQL, Redis</small>
                </div>
            </div>
        </div>

        <!-- Contact Section -->
        <div class="card mb-4" data-aos="fade-up" data-aos-delay="300">
            <h2 class="mb-3"><i class="fas fa-envelope text-blue"></i> Hubungi Kami</h2>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;">
                <div>
                    <form>
                        <div class="form-group">
                            <label class="form-label">Nama</label>
                            <input type="text" class="form-control" placeholder="Nama Anda">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" placeholder="email@anda.com">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Pesan</label>
                            <textarea class="form-control" rows="4" placeholder="Tulis pesan Anda..."></textarea>
                        </div>
                        <button type="button" class="btn btn-primary btn-ripple" onclick="showToast('success','Pesan terkirim! Kami akan membalas segera.')">
                            <i class="fas fa-paper-plane"></i> Kirim Pesan
                        </button>
                    </form>
                </div>
                <div>
                    <div style="padding:2rem;background:var(--color-bg);border-radius:var(--radius-md);">
                        <h4 class="mb-2">Informasi Kontak</h4>
                        <ul style="line-height:2.5;font-size:0.95rem;color:var(--color-text-light);">
                            <li><i class="fas fa-envelope text-blue" style="width:24px;"></i> info@langkahkampus.id</li>
                            <li><i class="fas fa-phone text-green" style="width:24px;"></i> +62 812-3456-7890</li>
                            <li><i class="fas fa-map-marker-alt text-red" style="width:24px;"></i> Bandung, Jawa Barat, Indonesia</li>
                            <li><i class="fab fa-instagram text-blue" style="width:24px;"></i> @langkahkampus</li>
                        </ul>
                        <div class="mt-3">
                            <h5 class="mb-1">Jam Operasional</h5>
                            <p class="text-muted" style="font-size:0.9rem;">Senin - Jumat: 08:00 - 17:00 WIB<br>Sabtu: 09:00 - 14:00 WIB</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
