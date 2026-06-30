<?php
$page_title = 'Rekomendasi Program Studi';
include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-lightbulb"></i> Rekomendasi Program Studi</h1>
            <p>Cari program studi target Anda, lalu temukan alternatif dengan rasio kompetisi lebih rendah di bidang yang sama. Data berdasarkan Sistem Informasi Daya Tampung (SIDATA) PTN.</p>
        </div>
    </div>

    <div class="container">
        <!-- Search Form Section -->
        <div class="card" data-aos="fade-up" style="max-width:700px;margin:0 auto 2rem;">
            <h3 class="mb-2"><i class="fas fa-search"></i> Cari Program Studi Target</h3>
            <p class="text-muted mb-3">Ketik nama program studi atau universitas untuk mencari di database SIDATA PTN.</p>

            <form id="rekomendasiForm">
                <div class="form-group mb-2" style="position:relative;">
                    <label class="form-label">Program Studi Target</label>
                    <input type="text" id="sidataSearchInput" class="form-control" placeholder="Contoh: Teknik Informatika, Kedokteran, Manajemen..." autocomplete="off">
                    <input type="hidden" id="selectedKodeProdi" name="target_kode_prodi" value="">
                    <div id="sidataSearchResults" class="autocomplete-dropdown" style="display:none;position:absolute;top:100%;left:0;right:0;background:#fff;border:1px solid var(--color-border);border-radius:0.5rem;max-height:280px;overflow-y:auto;z-index:100;box-shadow:0 4px 12px rgba(0,0,0,0.1);"></div>
                </div>

                <!-- Selected program preview -->
                <div id="selectedProgramPreview" class="mb-3" style="display:none;">
                    <div style="padding:0.75rem 1rem;background:linear-gradient(135deg,rgba(52,152,219,0.08),rgba(46,204,113,0.08));border-radius:0.5rem;border:1px solid rgba(52,152,219,0.2);">
                        <div style="display:flex;align-items:center;gap:0.5rem;">
                            <i class="fas fa-check-circle" style="color:var(--color-accent-green);"></i>
                            <span id="selectedProgramText" style="font-weight:500;"></span>
                            <button type="button" id="clearSelectionBtn" style="margin-left:auto;background:none;border:none;color:#999;cursor:pointer;font-size:1.1rem;" title="Hapus pilihan"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary btn-ripple" id="submitRekomendasi" disabled>
                    <i class="fas fa-magic"></i> Cari Rekomendasi
                </button>
            </form>
        </div>

        <!-- Results Section (hidden until search) -->
        <div id="rekomendasiResults" style="display:none;">
            <!-- Target Program Card -->
            <div id="targetProgramCard" class="card" data-aos="fade-up" style="max-width:700px;margin:0 auto 1.5rem;border-left:4px solid var(--color-accent-blue);">
            </div>

            <!-- Recommendations List -->
            <div id="recommendationsList" style="max-width:700px;margin:0 auto;">
                <h3 class="mb-2" data-aos="fade-up"><i class="fas fa-list-ol"></i> Alternatif dengan Kompetisi Lebih Rendah</h3>
                <p class="text-muted mb-3" data-aos="fade-up">Program studi berikut memiliki rasio kompetisi lebih rendah dari target Anda, diurutkan dari yang paling mudah.</p>
                <div id="recommendationCards"></div>
            </div>

            <!-- No Results Message -->
            <div id="noResultsMessage" style="display:none;max-width:700px;margin:0 auto;">
                <div class="card" style="text-align:center;" data-aos="fade-up">
                    <i class="fas fa-info-circle" style="font-size:2.5rem;color:var(--color-accent-blue);margin-bottom:1rem;"></i>
                    <h3 class="mb-2">Tidak Ada Rekomendasi</h3>
                    <p class="text-muted">Tidak ditemukan program studi serupa dengan rasio kompetisi lebih rendah. Coba cari program lain atau program target Anda sudah memiliki rasio kompetisi terendah di bidangnya.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    initSidataSearch();
    initRekomendasiForm();
});

/* === SIDATA Program Search Autocomplete === */
function initSidataSearch() {
    var input = document.getElementById('sidataSearchInput');
    var dropdown = document.getElementById('sidataSearchResults');
    var hiddenInput = document.getElementById('selectedKodeProdi');
    var preview = document.getElementById('selectedProgramPreview');
    var previewText = document.getElementById('selectedProgramText');
    var clearBtn = document.getElementById('clearSelectionBtn');
    var submitBtn = document.getElementById('submitRekomendasi');
    var debounceTimer = null;

    if (!input || !dropdown) return;

    input.addEventListener('input', function() {
        var query = this.value.trim();

        if (debounceTimer) clearTimeout(debounceTimer);

        if (query.length < 2) {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(function() {
            ajaxRequest('../api/search_sidata.php?q=' + encodeURIComponent(query), 'GET', null, function(error, response) {
                if (error || !response || !response.programs) {
                    dropdown.style.display = 'none';
                    return;
                }

                var programs = response.programs;
                if (programs.length === 0) {
                    dropdown.innerHTML = '<div style="padding:0.75rem 1rem;color:#999;font-size:0.9rem;">Tidak ditemukan program studi.</div>';
                    dropdown.style.display = 'block';
                    return;
                }

                var html = '';
                programs.forEach(function(prog) {
                    var ratio = (prog.daya_tampung_2023 > 0 && prog.peminat_2022 > 0)
                        ? (prog.peminat_2022 / prog.daya_tampung_2023).toFixed(1)
                        : '-';
                    html += '<div class="autocomplete-item" style="padding:0.75rem 1rem;cursor:pointer;border-bottom:1px solid #f0f0f0;transition:background 0.2s;" ' +
                        'data-kode="' + escapeHtml(prog.kode_prodi) + '" ' +
                        'data-nama="' + escapeHtml(prog.nama_prodi) + '" ' +
                        'data-univ="' + escapeHtml(prog.nama_univ) + '">' +
                        '<div style="font-weight:500;font-size:0.95rem;">' + escapeHtml(prog.nama_prodi) + ' (' + escapeHtml(prog.jenjang) + ')</div>' +
                        '<div style="font-size:0.8rem;color:#666;">' + escapeHtml(prog.nama_univ) +
                        ' &bull; Daya Tampung: ' + (prog.daya_tampung_2023 || '-') +
                        ' &bull; Peminat: ' + (prog.peminat_2022 || '-') +
                        ' &bull; Rasio: ' + ratio + 'x</div>' +
                        '</div>';
                });

                dropdown.innerHTML = html;
                dropdown.style.display = 'block';

                // Add click handlers
                var items = dropdown.querySelectorAll('.autocomplete-item');
                items.forEach(function(item) {
                    item.addEventListener('mouseenter', function() {
                        this.style.background = '#f5f9ff';
                    });
                    item.addEventListener('mouseleave', function() {
                        this.style.background = '';
                    });
                    item.addEventListener('click', function() {
                        var kode = this.getAttribute('data-kode');
                        var nama = this.getAttribute('data-nama');
                        var univ = this.getAttribute('data-univ');

                        hiddenInput.value = kode;
                        input.value = nama + ' - ' + univ;
                        previewText.textContent = nama + ' - ' + univ;
                        preview.style.display = 'block';
                        dropdown.style.display = 'none';
                        submitBtn.disabled = false;
                    });
                });
            });
        }, 300);
    });

    // Close dropdown on outside click
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });

    // Clear selection
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            hiddenInput.value = '';
            input.value = '';
            previewText.textContent = '';
            preview.style.display = 'none';
            submitBtn.disabled = true;
            document.getElementById('rekomendasiResults').style.display = 'none';
        });
    }
}

/* === Rekomendasi Form Submit === */
function initRekomendasiForm() {
    var form = document.getElementById('rekomendasiForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        var kodeProdi = document.getElementById('selectedKodeProdi').value;
        if (!kodeProdi) return;

        var submitBtn = document.getElementById('submitRekomendasi');
        var originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<div class="spinner" style="width:20px;height:20px;margin:0 auto;border-width:2px;"></div>';
        submitBtn.disabled = true;

        var postData = { target_kode_prodi: kodeProdi };

        ajaxRequest('../api/recommend.php', 'POST', postData, function(error, response) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;

            if (error) {
                showToast('danger', 'Gagal memuat rekomendasi: ' + error);
                return;
            }

            if (!response.success) {
                showToast('danger', response.error || 'Terjadi kesalahan');
                return;
            }

            displayRecommendationResults(response);
        });
    });
}

/* === Display Recommendation Results === */
function displayRecommendationResults(response) {
    var resultsSection = document.getElementById('rekomendasiResults');
    var targetCard = document.getElementById('targetProgramCard');
    var recCards = document.getElementById('recommendationCards');
    var noResults = document.getElementById('noResultsMessage');
    var recList = document.getElementById('recommendationsList');

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Render target program card
    var target = response.target;
    targetCard.innerHTML =
        '<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;">' +
            '<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--color-accent-blue),var(--color-accent-green));display:flex;align-items:center;justify-content:center;color:#fff;font-size:1rem;">' +
                '<i class="fas fa-crosshairs"></i>' +
            '</div>' +
            '<div>' +
                '<h4 style="margin:0;">' + escapeHtml(target.nama_prodi) + ' (' + escapeHtml(target.jenjang) + ')</h4>' +
                '<span class="text-muted" style="font-size:0.85rem;">' + escapeHtml(target.universitas) + '</span>' +
            '</div>' +
        '</div>' +
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;text-align:center;">' +
            '<div>' +
                '<div style="font-size:1.5rem;font-weight:700;color:var(--color-accent-blue);">' + target.daya_tampung_2023 + '</div>' +
                '<div style="font-size:0.75rem;color:#666;">Daya Tampung 2023</div>' +
            '</div>' +
            '<div>' +
                '<div style="font-size:1.5rem;font-weight:700;color:var(--color-accent-blue);">' + target.peminat_2022 + '</div>' +
                '<div style="font-size:0.75rem;color:#666;">Peminat 2022</div>' +
            '</div>' +
            '<div>' +
                '<div style="font-size:1.5rem;font-weight:700;color:#e74c3c;">' + target.ratio + 'x</div>' +
                '<div style="font-size:0.75rem;color:#666;">Rasio Kompetisi</div>' +
            '</div>' +
        '</div>';

    // Render recommendations
    var recommendations = response.recommendations || [];

    if (recommendations.length === 0) {
        recList.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }

    recList.style.display = 'block';
    noResults.style.display = 'none';
    recCards.innerHTML = '';

    recommendations.forEach(function(rec, index) {
        var ratioPercent = (target.ratio > 0) ? Math.min((rec.ratio / target.ratio) * 100, 100) : 0;
        var targetBarPercent = 100;

        var card = document.createElement('div');
        card.className = 'card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', (index * 100).toString());
        card.style.marginBottom = '1rem';
        card.style.borderLeft = '4px solid var(--color-accent-green)';

        card.innerHTML =
            '<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:0.75rem;">' +
                '<div style="flex:1;">' +
                    '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">' +
                        '<span style="width:24px;height:24px;border-radius:50%;background:var(--color-accent-green);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">' + (index + 1) + '</span>' +
                        '<h4 style="margin:0;font-size:1rem;">' + escapeHtml(rec.nama_prodi) + '</h4>' +
                    '</div>' +
                    '<div style="font-size:0.85rem;color:#666;margin-left:2rem;">' + escapeHtml(rec.universitas) + '</div>' +
                '</div>' +
                '<div style="text-align:right;">' +
                    '<div style="font-size:1.3rem;font-weight:700;color:var(--color-accent-green);">' + rec.ratio + 'x</div>' +
                    '<div style="font-size:0.75rem;color:var(--color-accent-green);font-weight:500;">-' + rec.ratio_difference_percent + '%</div>' +
                '</div>' +
            '</div>' +
            '<div style="display:flex;gap:1.5rem;font-size:0.85rem;color:#555;margin-bottom:0.75rem;">' +
                '<span><i class="fas fa-users" style="color:var(--color-accent-blue);margin-right:0.25rem;"></i> Daya Tampung: ' + rec.daya_tampung_2023 + '</span>' +
                '<span><i class="fas fa-user-graduate" style="color:var(--color-accent-blue);margin-right:0.25rem;"></i> Peminat: ' + rec.peminat_2022 + '</span>' +
                '<span><i class="fas fa-chart-line" style="color:var(--color-accent-green);margin-right:0.25rem;"></i> Rasio: ' + rec.ratio + 'x</span>' +
            '</div>' +
            '<div style="margin-top:0.5rem;">' +
                '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.35rem;">' +
                    '<span style="font-size:0.7rem;color:#999;width:55px;">Target:</span>' +
                    '<div style="flex:1;height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden;">' +
                        '<div style="width:' + targetBarPercent + '%;height:100%;background:linear-gradient(90deg,#e74c3c,#c0392b);border-radius:4px;"></div>' +
                    '</div>' +
                    '<span style="font-size:0.7rem;color:#e74c3c;width:35px;text-align:right;">' + target.ratio + 'x</span>' +
                '</div>' +
                '<div style="display:flex;align-items:center;gap:0.5rem;">' +
                    '<span style="font-size:0.7rem;color:#999;width:55px;">Alternatif:</span>' +
                    '<div style="flex:1;height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden;">' +
                        '<div style="width:' + ratioPercent.toFixed(1) + '%;height:100%;background:linear-gradient(90deg,var(--color-accent-green),#27ae60);border-radius:4px;"></div>' +
                    '</div>' +
                    '<span style="font-size:0.7rem;color:var(--color-accent-green);width:35px;text-align:right;">' + rec.ratio + 'x</span>' +
                '</div>' +
            '</div>';

        recCards.appendChild(card);
    });

    // Reinitialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

/* === Utility: Escape HTML === */
function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

/* === Utility: Show Toast === */
function showToast(type, message) {
    // Check if showToast exists globally from main.js
    var container = document.body;
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.innerHTML = '<i class="fas fa-' + (type === 'success' ? 'check-circle' : 'exclamation-circle') + '"></i> ' +
        '<span>' + message + '</span>' +
        '<button class="toast-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>';
    container.appendChild(toast);
    setTimeout(function() {
        if (toast.parentNode) toast.remove();
    }, 5000);
}
</script>

<?php include '../includes/footer.php'; ?>
