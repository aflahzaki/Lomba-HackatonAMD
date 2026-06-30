<?php
$page_title = 'Prediksi SNBP';
$page_scripts = ['predictions.js'];
include '../includes/header.php';

// Check if program_id is pre-filled from peta_universitas
$prefill_program_id = isset($_GET['program_id']) ? htmlspecialchars($_GET['program_id']) : '';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-brain"></i> Prediksi SNBP</h1>
            <p>Masukkan data akademik dan pilih program studi target. Hasil prediksi mencakup probabilitas, breakdown variabel, peringatan Choice-2, statistik anti-bentrok, dan rekomendasi alternatif.</p>
        </div>
    </div>

    <div class="container">
        <div style="display:grid;grid-template-columns:1fr 420px;gap:2rem;align-items:start;">
            <!-- Prediction Form -->
            <div class="card" data-aos="fade-up">
                <h3 class="mb-3"><i class="fas fa-edit"></i> Data Akademik</h3>

                <form id="predictionForm">
                    <!-- School Info -->
                    <div class="form-row mb-3">
                        <div class="form-group">
                            <label class="form-label">Peringkat di Sekolah</label>
                            <input type="number" name="school_ranking" class="form-control" placeholder="Peringkat Anda" min="1" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Total Siswa (Angkatan)</label>
                            <input type="number" name="total_students" class="form-control" placeholder="Jumlah siswa" min="1" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Akreditasi Sekolah</label>
                            <select name="school_accreditation" class="form-control" required>
                                <option value="">Pilih</option>
                                <option value="A">A (Unggul)</option>
                                <option value="B">B (Baik)</option>
                                <option value="C">C (Cukup)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Jurusan Selector -->
                    <h4 class="mb-2">Jurusan / Program Keahlian</h4>
                    <div class="form-group mb-3">
                        <label class="form-label">Pilih Jurusan</label>
                        <select name="jurusan" id="jurusanSelector" class="form-control" required>
                            <option value="">-- Pilih Jurusan --</option>
                            <optgroup label="SMA / MA">
                                <option value="IPA">IPA (Ilmu Pengetahuan Alam)</option>
                                <option value="IPS">IPS (Ilmu Pengetahuan Sosial)</option>
                                <option value="Bahasa">Bahasa</option>
                            </optgroup>
                            <optgroup label="SMK">
                                <option value="TKJ">TKJ (Teknik Komputer & Jaringan)</option>
                                <option value="RPL">RPL (Rekayasa Perangkat Lunak)</option>
                                <option value="Multimedia">Multimedia</option>
                                <option value="AKL">AKL (Akuntansi & Keuangan Lembaga)</option>
                                <option value="TBSM">TBSM (Teknik Bisnis Sepeda Motor)</option>
                                <option value="OTKP">OTKP (Otomatisasi Tata Kelola Perkantoran)</option>
                                <option value="BDP">BDP (Bisnis Daring & Pemasaran)</option>
                                <option value="Farmasi">Farmasi</option>
                                <option value="Keperawatan">Keperawatan</option>
                                <option value="DKV">DKV (Desain Komunikasi Visual)</option>
                                <option value="Teknik Kendaraan Ringan">Teknik Kendaraan Ringan</option>
                                <option value="Teknik Instalasi Tenaga Listrik">Teknik Instalasi Tenaga Listrik</option>
                                <option value="Tata Busana">Tata Busana</option>
                                <option value="Tata Boga">Tata Boga</option>
                                <option value="Animasi">Animasi</option>
                            </optgroup>
                        </select>
                    </div>

                    <!-- Dynamic Subject Scores -->
                    <h4 class="mb-2">Nilai Rapor (Semester 1-5)</h4>
                    <p class="text-muted mb-2" style="font-size:0.85rem;">Masukkan nilai rata-rata per mata pelajaran untuk setiap semester</p>

                    <div id="subjectsContainer">
                        <!-- Dynamically populated by JavaScript based on jurusan selection -->
                        <p class="text-muted" style="font-style:italic;">Pilih jurusan terlebih dahulu untuk menampilkan mata pelajaran.</p>
                    </div>

                    <!-- Add Custom Subject Button -->
                    <button type="button" id="addCustomSubjectBtn" class="btn btn-outline mt-2 mb-3" style="font-size:0.85rem;display:none;" onclick="addCustomSubject()">
                        <i class="fas fa-plus"></i> Tambah Mata Pelajaran Lain
                    </button>

                    <!-- Target Program -->
                    <h4 class="mb-2 mt-3">Target Program Studi</h4>
                    <div class="form-group" style="position:relative;">
                        <label class="form-label">Cari Program Studi & Universitas</label>
                        <input type="text" id="programSearch" class="form-control" 
                               placeholder="Ketik nama program studi atau universitas...">
                        <input type="hidden" name="target_program" value="<?php echo $prefill_program_id; ?>">
                        <div id="programResults" class="hidden" style="position:absolute;top:100%;left:0;right:0;background:white;border:1px solid var(--color-border);border-radius:var(--radius-sm);max-height:200px;overflow-y:auto;z-index:100;box-shadow:var(--shadow-md);"></div>
                    </div>

                    <button type="submit" class="btn btn-primary btn-lg btn-block btn-ripple mt-3">
                        <i class="fas fa-magic"></i> Prediksi Sekarang
                    </button>
                </form>
            </div>

            <!-- Combined Prediction Results -->
            <div>
                <div class="card hidden" id="predictionResult" data-aos="zoom-in">
                    <div class="prediction-result">
                        <h3 class="mb-2">Hasil Prediksi</h3>

                        <!-- Gauge -->
                        <div class="gauge-container">
                            <svg class="gauge-svg" width="220" height="220" viewBox="0 0 220 220">
                                <circle class="gauge-bg" cx="110" cy="110" r="90"/>
                                <circle class="gauge-fill" id="gaugeCircle" cx="110" cy="110" r="90"
                                        stroke-dasharray="565.48" stroke-dashoffset="565.48"/>
                            </svg>
                            <div class="gauge-text">
                                <div class="gauge-percentage" id="gaugePercentage">0%</div>
                                <div class="gauge-label">Probabilitas</div>
                            </div>
                        </div>

                        <div id="predictionStatus" style="font-size:1.2rem;font-weight:700;margin-bottom:1rem;"></div>

                        <!-- Confidence Interval -->
                        <h5 class="mb-1">Interval Kepercayaan</h5>
                        <div class="confidence-bar">
                            <div class="confidence-range" id="confidenceRange"></div>
                            <div class="confidence-point" id="confidencePoint"></div>
                        </div>
                        <div class="d-flex justify-between text-muted" style="font-size:0.8rem;">
                            <span id="confidenceLower">0%</span>
                            <span id="confidenceUpper">100%</span>
                        </div>

                        <!-- Variable Breakdown -->
                        <h5 class="mt-3 mb-2">Breakdown Detail Variabel</h5>
                        <div id="variableBreakdown"></div>
                    </div>
                </div>

                <!-- Admission History -->
                <div class="card hidden mt-2" id="admissionHistorySection">
                    <h4 class="mb-2"><i class="fas fa-history text-blue"></i> Info Historis Penerimaan</h4>
                    <p class="text-muted mb-2" style="font-size:0.85rem;">Data historis penerimaan dari sekolah Anda ke program studi target:</p>
                    <div id="admissionHistoryContent"></div>
                </div>

                <!-- Choice-2 Trap Warning -->
                <div class="card hidden mt-2" id="choice2TrapWarning" style="border-left:4px solid #C0392B;">
                    <div class="d-flex align-center gap-1 mb-1">
                        <i class="fas fa-exclamation-triangle" style="color:#C0392B;font-size:1.3rem;"></i>
                        <h4 style="color:#C0392B;">Peringatan Choice-2 Trap!</h4>
                    </div>
                    <p style="font-size:0.9rem;color:var(--color-text-light);">
                        Program studi ini <strong>memblokir pilihan kedua (Choice-2)</strong>. 
                        Jika Anda memilih prodi ini sebagai pilihan 1 dan tidak diterima, pilihan 2 Anda tidak akan diproses.
                    </p>
                    <div style="background:rgba(192,57,43,0.05);border-radius:var(--radius-sm);padding:0.75rem;margin-top:0.5rem;">
                        <small><i class="fas fa-info-circle"></i> Pertimbangkan dengan matang sebelum menjadikan ini pilihan utama Anda.</small>
                    </div>
                </div>

                <!-- Anti-Bentrok Statistics -->
                <div class="card hidden mt-2" id="antiBentrokStats" style="border-left:4px solid #F39C12;">
                    <div class="d-flex align-center gap-1 mb-1">
                        <i class="fas fa-users" style="color:#F39C12;font-size:1.2rem;"></i>
                        <h4 style="color:#F39C12;">Statistik Anti-Bentrok</h4>
                    </div>
                    <p id="peerStatText" style="font-size:0.9rem;"></p>
                    <div style="background:rgba(243,156,18,0.05);border-radius:var(--radius-sm);padding:0.75rem;margin-top:0.5rem;">
                        <div class="d-flex align-center justify-between">
                            <span style="font-size:0.85rem;"><i class="fas fa-user-friends"></i> Siswa dari sekolahmu:</span>
                            <strong id="peerCountValue" style="font-size:1.2rem;color:#F39C12;">0</strong>
                        </div>
                        <div class="progress-bar mt-1" style="height:6px;">
                            <div class="progress-fill" id="peerProgressBar" style="width:0%;background:#F39C12;"></div>
                        </div>
                        <small class="text-muted" id="peerRiskText">Semakin banyak pesaing, semakin kecil peluang lolos dari sekolah yang sama.</small>
                    </div>
                </div>

                <!-- Recommendations -->
                <div class="card hidden mt-2" id="recommendationsSection">
                    <h4 class="mb-2"><i class="fas fa-lightbulb text-blue"></i> Rekomendasi Alternatif</h4>
                    <p class="text-muted mb-2" style="font-size:0.85rem;">Program studi serupa dengan tingkat kompetisi lebih rendah:</p>
                    <div id="recommendationCards"></div>
                </div>

                <!-- What-If Simulator -->
                <div class="card hidden mt-2" id="whatIfSimulator">
                    <h4 class="mb-2"><i class="fas fa-sliders-h text-blue"></i> Simulator What-If</h4>
                    <p class="text-muted mb-2" style="font-size:0.85rem;">Geser slider untuk melihat dampak perubahan nilai</p>
                    <div class="form-group">
                        <label class="form-label">Jika rata-rata naik: <strong id="whatIfValue">+0</strong> poin</label>
                        <input type="range" min="0" max="15" value="0" class="form-control" style="padding:0;" id="whatIfSlider"
                               oninput="updateWhatIf(this.value)">
                    </div>
                    <div class="d-flex align-center justify-between" style="background:var(--color-bg);padding:0.75rem;border-radius:var(--radius-sm);">
                        <span>Prediksi baru:</span>
                        <strong id="whatIfResult" style="font-size:1.2rem;color:var(--color-accent-blue);">-</strong>
                    </div>
                </div>

                <!-- Tips Card -->
                <div class="card mt-2" data-aos="fade-up" data-aos-delay="300">
                    <h4 class="mb-2"><i class="fas fa-lightbulb text-blue"></i> Tips</h4>
                    <ul style="font-size:0.9rem;color:var(--color-text-light);line-height:2;">
                        <li><i class="fas fa-check text-green"></i> Masukkan nilai sesuai rapor resmi</li>
                        <li><i class="fas fa-check text-green"></i> Peringkat dihitung dari kelas 10-12</li>
                        <li><i class="fas fa-check text-green"></i> Akreditasi mempengaruhi bobot prediksi</li>
                        <li><i class="fas fa-check text-green"></i> Hasil mencakup analisis Choice-2 otomatis</li>
                        <li><i class="fas fa-check text-green"></i> Formula menggunakan data SIDATA PTN resmi</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
