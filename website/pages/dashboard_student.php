<?php
$page_title = 'Dashboard';
$page_scripts = ['dashboard.js'];
include '../includes/header.php';
require_once $base_path . 'includes/auth_middleware.php';

// Demo user data (would come from session/database in production)
$user_name = isset($_SESSION['user_name']) ? $_SESSION['user_name'] : 'Anisa Rahmawati';
$user_school = 'SMAN 3 Bandung';
$predictions_count = 2;
$predictions_limit = FREE_PREDICTIONS_LIMIT;
$success_rate = 75;
$is_premium = isset($_SESSION['is_premium']) ? $_SESSION['is_premium'] : false;
$onboarding_complete = isset($_SESSION['onboarding_complete']) ? $_SESSION['onboarding_complete'] : false;

// Demo referral data
$referral_code = 'LK-' . strtoupper(substr(md5($user_name), 0, 6));
$referral_clicks = 3;
$referral_unique = 3;
$referral_unlocked = 0;
?>

<div class="dashboard-page">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
        <div class="container">
            <div class="d-flex align-center justify-between flex-wrap gap-2">
                <div>
                    <h1><i class="fas fa-graduation-cap"></i> Selamat Datang, <?php echo htmlspecialchars($user_name); ?>!</h1>
                    <p><i class="fas fa-school"></i> <?php echo $user_school; ?></p>
                </div>
                <div>
                    <a href="prediksi.php" class="btn btn-primary btn-ripple">
                        <i class="fas fa-plus"></i> Prediksi Baru
                    </a>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <?php if (!$onboarding_complete): ?>
        <!-- Onboarding Wizard -->
        <div class="card mb-3" id="onboardingWizard" data-aos="fade-up">
            <div class="d-flex align-center justify-between mb-3">
                <h3><i class="fas fa-magic"></i> Lengkapi Profil Anda</h3>
                <div class="onboarding-steps">
                    <span class="step-indicator active" id="stepInd1">1</span>
                    <span class="step-indicator" id="stepInd2">2</span>
                    <span class="step-indicator" id="stepInd3">3</span>
                </div>
            </div>

            <!-- Step 1: Data Sekolah -->
            <div id="onboardingStep1" class="onboarding-step">
                <h4 class="mb-2"><i class="fas fa-school text-blue"></i> Step 1: Data Sekolah</h4>
                <p class="text-muted mb-3">Lengkapi informasi sekolah Anda untuk meningkatkan akurasi prediksi</p>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Peringkat di Sekolah</label>
                        <input type="number" id="ob_ranking" class="form-control" placeholder="Contoh: 5" min="1">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Total Siswa (Angkatan)</label>
                        <input type="number" id="ob_total_students" class="form-control" placeholder="Contoh: 320" min="1">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Akreditasi Sekolah</label>
                        <select id="ob_accreditation" class="form-control">
                            <option value="">Pilih Akreditasi</option>
                            <option value="A">A (Unggul)</option>
                            <option value="B">B (Baik)</option>
                            <option value="C">C (Cukup)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Jurusan</label>
                        <select id="ob_major" class="form-control">
                            <option value="IPA">IPA</option>
                            <option value="IPS">IPS</option>
                            <option value="Bahasa">Bahasa</option>
                        </select>
                    </div>
                </div>
                <div class="d-flex justify-between mt-3">
                    <span></span>
                    <button class="btn btn-primary btn-ripple" onclick="nextOnboardingStep(2)">
                        Lanjut <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
            </div>

            <!-- Step 2: Nilai Rapor -->
            <div id="onboardingStep2" class="onboarding-step hidden">
                <h4 class="mb-2"><i class="fas fa-book text-green"></i> Step 2: Nilai Rapor Semester 1-5</h4>
                <p class="text-muted mb-3">Masukkan rata-rata nilai rapor Anda. Bisa diisi nanti jika belum siap.</p>
                <div class="table-responsive">
                    <table class="table" style="font-size:0.85rem;">
                        <thead>
                            <tr>
                                <th>Mata Pelajaran</th>
                                <th>Sem 1</th>
                                <th>Sem 2</th>
                                <th>Sem 3</th>
                                <th>Sem 4</th>
                                <th>Sem 5</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                            $ob_subjects = ['Matematika', 'B. Indonesia', 'B. Inggris', 'Fisika/Ekonomi', 'Kimia/Sosiologi', 'Biologi/Geografi'];
                            foreach ($ob_subjects as $idx => $subj):
                            ?>
                            <tr>
                                <td><strong><?php echo $subj; ?></strong></td>
                                <?php for ($s = 1; $s <= 5; $s++): ?>
                                <td><input type="number" class="form-control" style="width:60px;padding:0.3rem;" min="0" max="100" placeholder="-"></td>
                                <?php endfor; ?>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <div class="d-flex justify-between mt-3">
                    <button class="btn btn-outline btn-ripple" style="border-color:var(--color-border);color:var(--color-text);" onclick="nextOnboardingStep(1)">
                        <i class="fas fa-arrow-left"></i> Kembali
                    </button>
                    <div class="d-flex gap-1">
                        <button class="btn btn-outline btn-ripple" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);" onclick="nextOnboardingStep(3)">
                            <i class="fas fa-forward"></i> Skip, Isi Nanti
                        </button>
                        <button class="btn btn-primary btn-ripple" onclick="nextOnboardingStep(3)">
                            Lanjut <i class="fas fa-arrow-right"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Step 3: Pilih Prodi Impian -->
            <div id="onboardingStep3" class="onboarding-step hidden">
                <h4 class="mb-2"><i class="fas fa-star text-orange"></i> Step 3: Pilih 1-2 Prodi Impian</h4>
                <p class="text-muted mb-3">Pilih program studi target awal Anda sebagai acuan prediksi pertama</p>
                <div class="form-group">
                    <label class="form-label">Program Studi Pilihan 1 (Utama)</label>
                    <input type="text" class="form-control" placeholder="Contoh: Teknik Informatika - ITB">
                </div>
                <div class="form-group">
                    <label class="form-label">Program Studi Pilihan 2 (Opsional)</label>
                    <input type="text" class="form-control" placeholder="Contoh: Sistem Informasi - UI">
                </div>
                <div class="d-flex justify-between mt-3">
                    <button class="btn btn-outline btn-ripple" style="border-color:var(--color-border);color:var(--color-text);" onclick="nextOnboardingStep(2)">
                        <i class="fas fa-arrow-left"></i> Kembali
                    </button>
                    <button class="btn btn-primary btn-ripple" onclick="completeOnboarding()">
                        <i class="fas fa-check"></i> Selesai & Mulai Prediksi
                    </button>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <!-- Quick Stats -->
        <div class="dashboard-grid" data-aos="fade-up">
            <div class="stat-card">
                <div class="stat-card-icon blue">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <div class="stat-card-info">
                    <h3><?php echo $predictions_count; ?>/<?php echo $predictions_limit; ?></h3>
                    <p>Prediksi Gratis</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-card-icon green">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-card-info">
                    <h3><?php echo $success_rate; ?>%</h3>
                    <p>Rata-rata Peluang</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-card-icon orange">
                    <i class="fas fa-share-alt"></i>
                </div>
                <div class="stat-card-info">
                    <h3><?php echo $referral_unique; ?>/<?php echo REFERRAL_CLICKS_REQUIRED; ?></h3>
                    <p>Klik Referral</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-card-icon red">
                    <i class="fas fa-bell"></i>
                </div>
                <div class="stat-card-info">
                    <h3>3</h3>
                    <p>Notifikasi Baru</p>
                </div>
            </div>
        </div>

        <!-- Referral Status Card -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="50">
            <div class="d-flex align-center justify-between mb-2">
                <h4><i class="fas fa-gift text-blue"></i> Status Referral</h4>
                <span class="badge badge-info"><?php echo $referral_unlocked; ?> prediksi di-unlock</span>
            </div>
            <p class="text-muted mb-2">Bagikan link referral Anda. Setiap 5 klik unik = 3 prediksi gratis tambahan!</p>
            <div style="background:rgba(26,115,232,0.05);border-radius:var(--radius-sm);padding:1rem;">
                <div class="d-flex align-center gap-1 flex-wrap">
                    <code style="font-size:0.9rem;padding:0.4rem 0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);flex:1;"><?php echo APP_URL; ?>/ref/<?php echo $referral_code; ?></code>
                    <button onclick="navigator.clipboard.writeText('<?php echo APP_URL; ?>/ref/<?php echo $referral_code; ?>');this.innerHTML='<i class=\'fas fa-check\'></i> Disalin';setTimeout(function(){document.querySelector('.btn-copy-ref').innerHTML='<i class=\'fas fa-copy\'></i> Salin'},2000);" class="btn btn-sm btn-primary btn-copy-ref">
                        <i class="fas fa-copy"></i> Salin
                    </button>
                </div>
                <div class="mt-2">
                    <div class="progress-bar" style="height:8px;">
                        <div class="progress-fill" style="width:<?php echo ($referral_unique / REFERRAL_CLICKS_REQUIRED) * 100; ?>%;background:linear-gradient(90deg,var(--color-accent-blue),var(--color-accent-green));"></div>
                    </div>
                    <small class="text-muted"><?php echo $referral_unique; ?>/<?php echo REFERRAL_CLICKS_REQUIRED; ?> klik unik (butuh <?php echo REFERRAL_CLICKS_REQUIRED - $referral_unique; ?> lagi untuk unlock)</small>
                </div>
            </div>
        </div>

        <!-- Inline Academic Data Edit (Collapsible) -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="100">
            <div class="d-flex align-center justify-between" style="cursor:pointer;" onclick="toggleAcademicEdit()">
                <h4><i class="fas fa-user-edit"></i> Edit Data Akademik</h4>
                <i class="fas fa-chevron-down" id="academicToggleIcon"></i>
            </div>
            <div id="academicEditSection" class="hidden" style="margin-top:1rem;">
                <form>
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Nama Lengkap</label>
                            <input type="text" class="form-control" value="<?php echo htmlspecialchars($user_name); ?>">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Sekolah</label>
                            <input type="text" class="form-control" value="<?php echo $user_school; ?>">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Peringkat</label>
                            <input type="number" class="form-control" value="5" min="1">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Total Siswa</label>
                            <input type="number" class="form-control" value="320" min="1">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Jurusan</label>
                            <select class="form-control">
                                <option value="IPA" selected>IPA</option>
                                <option value="IPS">IPS</option>
                                <option value="Bahasa">Bahasa</option>
                            </select>
                        </div>
                    </div>
                    <h5 class="mb-2">Nilai Rapor (Rata-rata per Semester)</h5>
                    <div class="table-responsive">
                        <table class="table" style="font-size:0.85rem;">
                            <thead>
                                <tr>
                                    <th>Mata Pelajaran</th>
                                    <th>Sem 1</th>
                                    <th>Sem 2</th>
                                    <th>Sem 3</th>
                                    <th>Sem 4</th>
                                    <th>Sem 5</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td><strong>Matematika</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="88"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="90"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="87"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="91"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="89"></td></tr>
                                <tr><td><strong>B. Indonesia</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="85"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="86"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="88"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="87"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="86"></td></tr>
                                <tr><td><strong>B. Inggris</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="82"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="84"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="83"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="85"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="84"></td></tr>
                                <tr><td><strong>Fisika</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="90"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="88"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="92"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="89"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="91"></td></tr>
                                <tr><td><strong>Kimia</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="86"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="87"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="85"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="88"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="87"></td></tr>
                                <tr><td><strong>Biologi</strong></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="84"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="85"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="86"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="84"></td><td><input type="number" class="form-control" style="width:55px;padding:0.3rem;" value="85"></td></tr>
                            </tbody>
                        </table>
                    </div>
                    <button type="button" class="btn btn-primary btn-ripple mt-2" onclick="showToast('success','Data akademik berhasil disimpan')">
                        <i class="fas fa-save"></i> Simpan Perubahan
                    </button>
                </form>
            </div>
        </div>

        <!-- Recent Predictions -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="150">
            <div class="d-flex align-center justify-between mb-3">
                <h3><i class="fas fa-history"></i> Prediksi Terbaru</h3>
                <a href="prediksi.php" class="btn btn-sm btn-primary">Prediksi Baru</a>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Program Studi</th>
                            <th>Universitas</th>
                            <th>Probabilitas</th>
                            <th>Tanggal</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Teknik Informatika</strong></td>
                            <td>Institut Teknologi Bandung</td>
                            <td><span class="badge badge-success">78%</span></td>
                            <td>10 Jan 2025</td>
                            <td><a href="prediksi.php" class="btn btn-sm btn-outline" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);">Detail</a></td>
                        </tr>
                        <tr>
                            <td><strong>Kedokteran</strong></td>
                            <td>Universitas Indonesia</td>
                            <td><span class="badge badge-warning">45%</span></td>
                            <td>8 Jan 2025</td>
                            <td><a href="prediksi.php" class="btn btn-sm btn-outline" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);">Detail</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Undang Guru Section -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="200">
            <h4 class="mb-2"><i class="fas fa-user-plus"></i> Undang Guru</h4>
            <p class="text-muted mb-2">Bagikan kode ini ke guru BK Anda untuk mengundang mereka ke LangkahKampus</p>

            <?php
            $demo_invite_codes = [
                ['code' => 'ABC123', 'is_active' => false, 'used_by' => 'Bu Ratna Sari'],
                ['code' => 'DEF456', 'is_active' => true, 'used_by' => null],
            ];
            $active_codes = array_filter($demo_invite_codes, function($c) { return $c['is_active']; });
            $active_count = count($active_codes);
            ?>

            <div style="background:rgba(26,115,232,0.05);border-radius:var(--radius-sm);padding:1rem;margin-bottom:1rem;">
                <p style="font-size:0.85rem;margin-bottom:0.5rem;"><strong>Kode Aktif (<?php echo $active_count; ?>/2):</strong></p>
                <?php foreach ($demo_invite_codes as $invite): ?>
                <div class="d-flex align-center gap-1 mb-1">
                    <code style="font-size:1.1rem;font-weight:700;letter-spacing:2px;padding:0.25rem 0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);"><?php echo $invite['code']; ?></code>
                    <?php if ($invite['is_active']): ?>
                        <span class="badge badge-success">Aktif</span>
                        <button onclick="navigator.clipboard.writeText('<?php echo $invite['code']; ?>');this.innerHTML='<i class=\'fas fa-check\'></i> Disalin';" class="btn btn-sm btn-outline" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);font-size:0.75rem;">
                            <i class="fas fa-copy"></i> Salin
                        </button>
                    <?php else: ?>
                        <span class="badge badge-warning">Digunakan</span>
                        <small class="text-muted">oleh <?php echo htmlspecialchars($invite['used_by']); ?></small>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>

            <?php if ($active_count < 2): ?>
            <form action="<?php echo $base_path; ?>api/invite.php" method="POST" style="display:inline;">
                <input type="hidden" name="action" value="generate">
                <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
                <button type="submit" class="btn btn-primary btn-sm btn-ripple">
                    <i class="fas fa-plus-circle"></i> Generate Kode Baru
                </button>
            </form>
            <?php else: ?>
            <p class="text-muted" style="font-size:0.85rem;"><i class="fas fa-info-circle"></i> Anda sudah memiliki 2 kode aktif (maksimal).</p>
            <?php endif; ?>
        </div>

        <!-- Quick Actions -->
        <div class="card mb-4" data-aos="fade-up" data-aos-delay="300">
            <h4 class="mb-2"><i class="fas fa-bolt"></i> Aksi Cepat</h4>
            <div class="d-flex flex-wrap gap-2">
                <a href="prediksi.php" class="btn btn-primary btn-ripple"><i class="fas fa-brain"></i> Prediksi Baru</a>
                <a href="peta_universitas.php" class="btn btn-success btn-ripple"><i class="fas fa-map"></i> Peta PTN</a>
                <a href="pembayaran.php" class="btn btn-outline btn-ripple" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);"><i class="fas fa-credit-card"></i> Tambah Prediksi</a>
                <a href="profil.php" class="btn btn-outline btn-ripple" style="border-color:var(--color-border);color:var(--color-text);"><i class="fas fa-user-edit"></i> Profil</a>
            </div>
        </div>
    </div>
</div>

<style>
.step-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--color-border);
    color: var(--color-text-light);
    font-size: 0.8rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
.step-indicator.active {
    background: var(--color-accent-blue);
    color: #fff;
}
.step-indicator.completed {
    background: var(--color-accent-green);
    color: #fff;
}
</style>

<script>
function nextOnboardingStep(step) {
    document.querySelectorAll('.onboarding-step').forEach(function(el) {
        el.classList.add('hidden');
    });
    document.getElementById('onboardingStep' + step).classList.remove('hidden');

    // Update step indicators
    for (var i = 1; i <= 3; i++) {
        var ind = document.getElementById('stepInd' + i);
        ind.className = 'step-indicator';
        if (i < step) ind.classList.add('completed');
        if (i === step) ind.classList.add('active');
    }
}

function completeOnboarding() {
    showToast('success', 'Profil berhasil dilengkapi! Anda siap melakukan prediksi pertama.');
    var wizard = document.getElementById('onboardingWizard');
    if (wizard) {
        wizard.style.opacity = '0';
        setTimeout(function() { wizard.style.display = 'none'; }, 300);
    }
}

function toggleAcademicEdit() {
    var section = document.getElementById('academicEditSection');
    var icon = document.getElementById('academicToggleIcon');
    if (section.classList.contains('hidden')) {
        section.classList.remove('hidden');
        icon.className = 'fas fa-chevron-up';
    } else {
        section.classList.add('hidden');
        icon.className = 'fas fa-chevron-down';
    }
}
</script>

<?php include '../includes/footer.php'; ?>
