<?php
$page_title = 'Peta Universitas';
$use_leaflet = true;
include '../includes/header.php';
?>

<div class="map-page">
    <div class="map-container">
        <!-- Sidebar -->
        <div class="map-sidebar">
            <h3><i class="fas fa-map-marked-alt"></i> Filter Universitas</h3>

            <!-- Radius Filter -->
            <div class="form-group">
                <label class="form-label">Radius: <span id="radiusValue">500 km</span></label>
                <input type="range" id="radiusSlider" min="0" max="500" value="500" class="form-control" style="padding:0;">
            </div>

            <!-- Province Filter -->
            <div class="form-group">
                <label class="form-label">Provinsi</label>
                <select id="provinceFilter" class="form-control">
                    <option value="">Semua Provinsi</option>
                    <option value="DKI Jakarta">DKI Jakarta</option>
                    <option value="Jawa Barat">Jawa Barat</option>
                    <option value="Jawa Tengah">Jawa Tengah</option>
                    <option value="Jawa Timur">Jawa Timur</option>
                    <option value="DI Yogyakarta">DI Yogyakarta</option>
                    <option value="Sumatera Utara">Sumatera Utara</option>
                    <option value="Sulawesi Selatan">Sulawesi Selatan</option>
                </select>
            </div>

            <!-- Type Filter -->
            <div class="form-group">
                <label class="form-label">Tipe Universitas</label>
                <select id="typeFilter" class="form-control">
                    <option value="">PTN & PTS</option>
                    <option value="PTN">PTN</option>
                    <option value="PTS">PTS</option>
                </select>
            </div>

            <!-- Accreditation Filter -->
            <div class="form-group">
                <label class="form-label">Akreditasi</label>
                <select id="accreditationFilter" class="form-control">
                    <option value="">Semua Akreditasi</option>
                    <option value="A">Unggul (A)</option>
                    <option value="B">Baik Sekali (B)</option>
                    <option value="C">Baik (C)</option>
                </select>
            </div>

            <hr style="border-color:var(--color-border);margin:1rem 0;">

            <!-- Results Count -->
            <div class="d-flex align-center justify-between mb-2">
                <span class="text-muted" style="font-size:0.85rem;">Ditemukan:</span>
                <strong id="universityCount">10</strong> <span class="text-muted">universitas</span>
            </div>

            <!-- University List -->
            <div id="universityList" style="max-height:300px;overflow-y:auto;">
                <!-- Populated by JS -->
            </div>
        </div>

        <!-- Map -->
        <div id="map"></div>
    </div>

    <!-- University Detail Panel (shown when a university is selected) -->
    <div id="universityDetail" class="hidden" style="position:fixed;bottom:0;left:0;right:0;background:white;border-top:2px solid var(--color-accent-blue);padding:1.5rem;z-index:1000;box-shadow:0 -4px 20px rgba(0,0,0,0.15);max-height:40vh;overflow-y:auto;">
        <div class="container">
            <div class="d-flex align-center justify-between mb-2">
                <div>
                    <h3 id="detailUniName">Universitas Indonesia</h3>
                    <p class="text-muted" id="detailUniLocation">DKI Jakarta</p>
                </div>
                <button class="btn btn-sm btn-ghost" onclick="closeUniversityDetail()">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem;">
                <div style="background:var(--color-bg);padding:0.75rem;border-radius:var(--radius-sm);text-align:center;">
                    <strong id="detailUniType">PTN</strong>
                    <small class="d-block text-muted">Tipe</small>
                </div>
                <div style="background:var(--color-bg);padding:0.75rem;border-radius:var(--radius-sm);text-align:center;">
                    <strong id="detailUniAccred">A</strong>
                    <small class="d-block text-muted">Akreditasi</small>
                </div>
                <div style="background:var(--color-bg);padding:0.75rem;border-radius:var(--radius-sm);text-align:center;">
                    <strong id="detailUniProdi">45</strong>
                    <small class="d-block text-muted">Program Studi</small>
                </div>
            </div>

            <!-- Program list with predict buttons -->
            <h5 class="mb-2">Program Studi Tersedia:</h5>
            <div id="detailProdiList" style="max-height:150px;overflow-y:auto;">
                <!-- Demo programs -->
                <div class="d-flex align-center justify-between" style="padding:0.5rem 0;border-bottom:1px solid var(--color-border);">
                    <div>
                        <strong style="font-size:0.9rem;">Teknik Informatika</strong>
                        <small class="d-block text-muted">S1 - Akreditasi A</small>
                    </div>
                    <a href="prediksi.php?program_id=1" class="btn btn-sm btn-primary btn-ripple">
                        <i class="fas fa-chart-line"></i> Prediksi Peluang Saya
                    </a>
                </div>
                <div class="d-flex align-center justify-between" style="padding:0.5rem 0;border-bottom:1px solid var(--color-border);">
                    <div>
                        <strong style="font-size:0.9rem;">Sistem Informasi</strong>
                        <small class="d-block text-muted">S1 - Akreditasi A</small>
                    </div>
                    <a href="prediksi.php?program_id=2" class="btn btn-sm btn-primary btn-ripple">
                        <i class="fas fa-chart-line"></i> Prediksi Peluang Saya
                    </a>
                </div>
                <div class="d-flex align-center justify-between" style="padding:0.5rem 0;border-bottom:1px solid var(--color-border);">
                    <div>
                        <strong style="font-size:0.9rem;">Kedokteran</strong>
                        <small class="d-block text-muted">S1 - Akreditasi A</small>
                    </div>
                    <a href="prediksi.php?program_id=3" class="btn btn-sm btn-primary btn-ripple">
                        <i class="fas fa-chart-line"></i> Prediksi Peluang Saya
                    </a>
                </div>
                <div class="d-flex align-center justify-between" style="padding:0.5rem 0;border-bottom:1px solid var(--color-border);">
                    <div>
                        <strong style="font-size:0.9rem;">Farmasi</strong>
                        <small class="d-block text-muted">S1 - Akreditasi A</small>
                    </div>
                    <a href="prediksi.php?program_id=4" class="btn btn-sm btn-primary btn-ripple">
                        <i class="fas fa-chart-line"></i> Prediksi Peluang Saya
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.university-list-item {
    padding: 0.75rem;
    border-bottom: 1px solid var(--color-border);
    cursor: pointer;
    transition: background var(--transition-fast);
}
.university-list-item:hover {
    background: rgba(26,115,232,0.05);
}
.university-list-item strong {
    display: block;
    font-size: 0.85rem;
    color: var(--color-primary);
}
.university-list-item small {
    color: var(--color-text-light);
    font-size: 0.75rem;
}
</style>

<script>
function closeUniversityDetail() {
    document.getElementById('universityDetail').classList.add('hidden');
}

function showUniversityDetail(uniName, location, type, accred, prodiCount) {
    document.getElementById('detailUniName').textContent = uniName;
    document.getElementById('detailUniLocation').textContent = location;
    document.getElementById('detailUniType').textContent = type;
    document.getElementById('detailUniAccred').textContent = accred;
    document.getElementById('detailUniProdi').textContent = prodiCount;
    document.getElementById('universityDetail').classList.remove('hidden');
}
</script>

<?php include '../includes/footer.php'; ?>
