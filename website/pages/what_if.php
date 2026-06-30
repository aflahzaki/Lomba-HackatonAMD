<?php
$page_title = 'What-If Simulator';
$page_scripts = ['what_if.js'];
include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-sliders-h"></i> What-If Simulator</h1>
            <p>Simulasikan perubahan nilai akademik dan lihat dampaknya terhadap peluang SNBP secara real-time. Geser slider untuk melihat bagaimana perubahan mempengaruhi probabilitas Anda.</p>
        </div>
    </div>

    <div class="container">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start;">
            <!-- Simulator Controls -->
            <div class="card" data-aos="fade-up">
                <h3 class="mb-3"><i class="fas fa-cogs"></i> Parameter Simulasi</h3>

                <form id="whatIfForm">
                    <!-- Nilai Rata-rata Slider -->
                    <div class="form-group mb-3">
                        <label class="form-label">Nilai Rata-rata: <strong id="nilaiDisplay">75</strong></label>
                        <input type="range" id="nilaiSlider" min="60" max="100" value="75" step="0.5" class="form-control" style="padding:0;">
                        <div class="d-flex justify-between text-muted" style="font-size:0.75rem;">
                            <span>60</span>
                            <span>100</span>
                        </div>
                    </div>

                    <!-- Peringkat Slider -->
                    <div class="form-group mb-3">
                        <label class="form-label">Peringkat di Sekolah: <strong id="peringkatDisplay">25</strong></label>
                        <input type="range" id="peringkatSlider" min="1" max="500" value="25" step="1" class="form-control" style="padding:0;">
                        <div class="d-flex justify-between text-muted" style="font-size:0.75rem;">
                            <span>1 (Terbaik)</span>
                            <span>500</span>
                        </div>
                    </div>

                    <!-- Total Siswa -->
                    <div class="form-group mb-3">
                        <label class="form-label">Total Siswa (Angkatan)</label>
                        <input type="number" id="totalSiswaInput" class="form-control" value="200" min="1" max="1000" placeholder="Jumlah siswa angkatan">
                    </div>

                    <!-- Akreditasi Dropdown -->
                    <div class="form-group mb-3">
                        <label class="form-label">Akreditasi Sekolah</label>
                        <select id="akreditasiSelect" class="form-control">
                            <option value="A">A (Unggul)</option>
                            <option value="B" selected>B (Baik)</option>
                            <option value="C">C (Cukup)</option>
                        </select>
                    </div>

                    <!-- Target Program Search -->
                    <div class="form-group mb-3" style="position:relative;">
                        <label class="form-label">Target Program Studi</label>
                        <input type="text" id="programSearch" class="form-control" 
                               placeholder="Ketik nama program studi atau universitas...">
                        <input type="hidden" id="targetProgramId" value="">
                        <div id="programResults" class="hidden" style="position:absolute;top:100%;left:0;right:0;background:white;border:1px solid var(--color-border);border-radius:var(--radius-sm);max-height:200px;overflow-y:auto;z-index:100;box-shadow:var(--shadow-md);"></div>
                    </div>
                </form>

                <!-- Factor Impact Summary -->
                <div id="factorImpact" class="hidden" style="margin-top:1.5rem;">
                    <h4 class="mb-2"><i class="fas fa-chart-bar"></i> Dampak Faktor</h4>
                    <div id="factorList"></div>
                </div>
            </div>

            <!-- Results Visualization -->
            <div class="card" data-aos="fade-up" data-aos-delay="100">
                <h3 class="mb-3"><i class="fas fa-chart-pie"></i> Hasil Simulasi</h3>

                <!-- Comparison Gauges -->
                <div id="comparisonSection" style="text-align:center;">
                    <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;">
                        <!-- Current Probability -->
                        <div>
                            <p style="font-size:0.85rem;color:var(--color-text-light);margin-bottom:0.5rem;">Probabilitas Saat Ini</p>
                            <div class="gauge-container" style="margin:0 auto;">
                                <svg class="gauge-svg" width="160" height="160" viewBox="0 0 160 160">
                                    <circle class="gauge-bg" cx="80" cy="80" r="65" fill="none" stroke="var(--color-border)" stroke-width="10"/>
                                    <circle class="gauge-fill" id="currentGaugeCircle" cx="80" cy="80" r="65"
                                            fill="none" stroke="var(--color-accent-blue)" stroke-width="10" stroke-linecap="round"
                                            stroke-dasharray="408.41" stroke-dashoffset="408.41"
                                            transform="rotate(-90 80 80)"/>
                                </svg>
                                <div class="gauge-text" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);">
                                    <div class="gauge-percentage" id="currentPercentage" style="font-size:1.8rem;">--%</div>
                                </div>
                            </div>
                        </div>

                        <!-- Arrow -->
                        <div style="font-size:2rem;color:var(--color-accent-blue);">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- New Probability -->
                        <div>
                            <p style="font-size:0.85rem;color:var(--color-text-light);margin-bottom:0.5rem;">Probabilitas Baru</p>
                            <div class="gauge-container" style="margin:0 auto;">
                                <svg class="gauge-svg" width="160" height="160" viewBox="0 0 160 160">
                                    <circle class="gauge-bg" cx="80" cy="80" r="65" fill="none" stroke="var(--color-border)" stroke-width="10"/>
                                    <circle class="gauge-fill" id="newGaugeCircle" cx="80" cy="80" r="65"
                                            fill="none" stroke="#27AE60" stroke-width="10" stroke-linecap="round"
                                            stroke-dasharray="408.41" stroke-dashoffset="408.41"
                                            transform="rotate(-90 80 80)"/>
                                </svg>
                                <div class="gauge-text" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);">
                                    <div class="gauge-percentage" id="newPercentage" style="font-size:1.8rem;">--%</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Difference Badge -->
                    <div id="differenceBadge" class="hidden" style="margin-top:1.5rem;padding:1rem;background:var(--color-bg);border-radius:var(--radius-sm);text-align:center;">
                        <span style="font-size:0.85rem;color:var(--color-text-light);">Perubahan Peluang</span>
                        <div id="differenceValue" style="font-size:2rem;font-weight:800;color:#27AE60;">+0%</div>
                        <span id="differenceLabel" style="font-size:0.8rem;color:var(--color-text-light);">Geser slider untuk mulai simulasi</span>
                    </div>
                </div>

                <!-- Tips -->
                <div style="margin-top:1.5rem;background:var(--color-bg);border-radius:var(--radius-sm);padding:1rem;">
                    <h5 class="mb-1"><i class="fas fa-lightbulb text-blue"></i> Tips Simulator</h5>
                    <ul style="font-size:0.85rem;color:var(--color-text-light);line-height:1.8;padding-left:1.2rem;">
                        <li>Geser slider untuk melihat dampak perubahan secara real-time</li>
                        <li>Kombinasikan peningkatan nilai dengan peringkat lebih baik</li>
                        <li>Akreditasi A memberikan bonus signifikan</li>
                        <li>Pilih program studi target untuk hasil lebih akurat</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
