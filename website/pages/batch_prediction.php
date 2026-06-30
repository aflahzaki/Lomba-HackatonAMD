<?php
$page_title = 'Batch Prediction';
$page_scripts = ['batch_prediction.js'];

// Auth middleware must run before any HTML output
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../includes/functions.php';
require_once __DIR__ . '/../includes/auth_middleware.php';
require_role(['guru']);

include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-users"></i> Batch Prediction</h1>
            <p>Upload data siswa dalam format CSV untuk melakukan prediksi massal sekaligus. Ideal untuk Guru BK yang perlu menganalisis peluang banyak siswa.</p>
        </div>
    </div>

    <div class="container">
        <!-- Upload Section -->
        <div class="card" data-aos="fade-up" style="margin-bottom:2rem;">
            <h3 class="mb-3"><i class="fas fa-file-csv"></i> Upload Data CSV</h3>

            <div style="background:var(--color-bg);border-radius:var(--radius-sm);padding:1.5rem;margin-bottom:1.5rem;">
                <h5 class="mb-1">Format CSV yang Dibutuhkan:</h5>
                <p style="font-size:0.85rem;color:var(--color-text-light);margin-bottom:0.5rem;">
                    File CSV harus memiliki kolom berikut (header wajib di baris pertama):
                </p>
                <code style="display:block;background:var(--color-card);padding:0.75rem;border-radius:var(--radius-sm);font-size:0.8rem;overflow-x:auto;">
                    nama,nilai_rata_rata,peringkat,total_siswa,akreditasi,target_prodi
                </code>
                <p style="font-size:0.8rem;color:var(--color-text-light);margin-top:0.5rem;">
                    Contoh: <code>Ahmad,85.5,3,200,A,Teknik Informatika - ITB</code>
                </p>
            </div>

            <!-- File Upload Area -->
            <div id="uploadArea" style="border:2px dashed var(--color-border);border-radius:var(--radius-md);padding:2rem;text-align:center;cursor:pointer;transition:all 0.3s ease;">
                <i class="fas fa-cloud-upload-alt" style="font-size:3rem;color:var(--color-accent-blue);margin-bottom:1rem;"></i>
                <p style="font-size:1rem;font-weight:600;margin-bottom:0.5rem;">Klik atau drag file CSV ke sini</p>
                <p style="font-size:0.85rem;color:var(--color-text-light);">Maksimal 500 baris data siswa</p>
                <input type="file" id="csvFileInput" accept=".csv" style="display:none;">
            </div>

            <!-- File Info -->
            <div id="fileInfo" class="hidden" style="margin-top:1rem;padding:0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:space-between;">
                <div>
                    <i class="fas fa-file-csv" style="color:#27AE60;margin-right:0.5rem;"></i>
                    <span id="fileName" style="font-weight:600;"></span>
                    <span id="fileRows" style="font-size:0.85rem;color:var(--color-text-light);margin-left:0.5rem;"></span>
                </div>
                <button type="button" class="btn btn-outline" style="font-size:0.8rem;" onclick="clearFile()">
                    <i class="fas fa-times"></i> Hapus
                </button>
            </div>

            <!-- Submit Button -->
            <button type="button" id="batchSubmitBtn" class="btn btn-primary btn-lg btn-block btn-ripple mt-3" onclick="submitBatch()" disabled>
                <i class="fas fa-magic"></i> Proses Prediksi Batch
            </button>
        </div>

        <!-- Results Section -->
        <div class="card hidden" id="batchResults" data-aos="fade-up">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">
                <h3><i class="fas fa-table"></i> Hasil Prediksi</h3>
                <div>
                    <span id="resultSummary" style="font-size:0.85rem;color:var(--color-text-light);margin-right:1rem;"></span>
                    <button type="button" class="btn btn-outline" onclick="exportCSV()">
                        <i class="fas fa-download"></i> Export CSV
                    </button>
                </div>
            </div>

            <!-- Summary Cards -->
            <div id="summaryCards" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;">
                <div style="background:rgba(39,174,96,0.1);border-radius:var(--radius-sm);padding:1rem;text-align:center;">
                    <div style="font-size:1.5rem;font-weight:800;color:#27AE60;" id="highCount">0</div>
                    <div style="font-size:0.8rem;color:var(--color-text-light);">Peluang Tinggi (&gt;70%)</div>
                </div>
                <div style="background:rgba(243,156,18,0.1);border-radius:var(--radius-sm);padding:1rem;text-align:center;">
                    <div style="font-size:1.5rem;font-weight:800;color:#F39C12;" id="medCount">0</div>
                    <div style="font-size:0.8rem;color:var(--color-text-light);">Peluang Sedang (40-70%)</div>
                </div>
                <div style="background:rgba(192,57,43,0.1);border-radius:var(--radius-sm);padding:1rem;text-align:center;">
                    <div style="font-size:1.5rem;font-weight:800;color:#C0392B;" id="lowCount">0</div>
                    <div style="font-size:0.8rem;color:var(--color-text-light);">Peluang Rendah (&lt;40%)</div>
                </div>
            </div>

            <!-- Results Table -->
            <div style="overflow-x:auto;">
                <table id="resultsTable" style="width:100%;border-collapse:collapse;font-size:0.85rem;">
                    <thead>
                        <tr style="border-bottom:2px solid var(--color-border);text-align:left;">
                            <th style="padding:0.75rem 0.5rem;">No</th>
                            <th style="padding:0.75rem 0.5rem;">Nama</th>
                            <th style="padding:0.75rem 0.5rem;">Nilai</th>
                            <th style="padding:0.75rem 0.5rem;">Peringkat</th>
                            <th style="padding:0.75rem 0.5rem;">Akreditasi</th>
                            <th style="padding:0.75rem 0.5rem;">Target Prodi</th>
                            <th style="padding:0.75rem 0.5rem;">Probabilitas</th>
                            <th style="padding:0.75rem 0.5rem;">Status</th>
                        </tr>
                    </thead>
                    <tbody id="resultsBody"></tbody>
                </table>
            </div>
        </div>

        <!-- Loading State -->
        <div class="card hidden" id="batchLoading" style="text-align:center;padding:3rem;">
            <div class="spinner" style="width:40px;height:40px;margin:0 auto 1rem;"></div>
            <p style="font-weight:600;">Memproses prediksi batch...</p>
            <p style="font-size:0.85rem;color:var(--color-text-light);">Mohon tunggu, ini mungkin memakan waktu beberapa detik.</p>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
