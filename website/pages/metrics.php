<?php
$page_title = 'System Metrics';
$page_scripts = ['metrics.js'];

// Auth middleware - require admin role
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../includes/functions.php';
require_once __DIR__ . '/../includes/auth_middleware.php';
require_role(['admin']);

include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-chart-line"></i> System Metrics</h1>
            <p>Dashboard monitoring performa sistem LangkahKampus. Data diperbarui secara otomatis setiap 30 detik.</p>
        </div>
    </div>

    <div class="container">
        <!-- Auto-refresh indicator -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span id="refreshIndicator" style="width:8px;height:8px;border-radius:50%;background:#27AE60;display:inline-block;animation:pulse 2s infinite;"></span>
                <span style="font-size:0.85rem;color:var(--color-text-light);">Auto-refresh aktif (30 detik)</span>
            </div>
            <div>
                <span id="lastUpdate" style="font-size:0.8rem;color:var(--color-text-light);">Terakhir diperbarui: -</span>
                <button type="button" class="btn btn-outline" style="font-size:0.8rem;margin-left:0.5rem;" onclick="refreshMetrics()">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
        </div>

        <!-- Main Stat Cards -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;margin-bottom:2rem;" id="statCards">
            <!-- Total Predictions -->
            <div class="card" data-aos="fade-up" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"><i class="fas fa-brain" style="color:var(--color-accent-blue);"></i></div>
                <div id="totalPredictions" style="font-size:2rem;font-weight:800;color:var(--color-text);">--</div>
                <div style="font-size:0.85rem;color:var(--color-text-light);">Total Prediksi</div>
            </div>

            <!-- Avg Response Time -->
            <div class="card" data-aos="fade-up" data-aos-delay="100" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"><i class="fas fa-tachometer-alt" style="color:#27AE60;"></i></div>
                <div id="avgResponseTime" style="font-size:2rem;font-weight:800;color:var(--color-text);">--</div>
                <div style="font-size:0.85rem;color:var(--color-text-light);">Rata-rata Response Time</div>
            </div>

            <!-- Predictions Today -->
            <div class="card" data-aos="fade-up" data-aos-delay="200" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"><i class="fas fa-calendar-day" style="color:#F39C12;"></i></div>
                <div id="predictionsToday" style="font-size:2rem;font-weight:800;color:var(--color-text);">--</div>
                <div style="font-size:0.85rem;color:var(--color-text-light);">Prediksi Hari Ini</div>
            </div>

            <!-- Active Users -->
            <div class="card" data-aos="fade-up" data-aos-delay="300" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"><i class="fas fa-users" style="color:#9B59B6;"></i></div>
                <div id="activeUsers" style="font-size:2rem;font-weight:800;color:var(--color-text);">--</div>
                <div style="font-size:0.85rem;color:var(--color-text-light);">User Aktif</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;">
            <!-- Popular Programs -->
            <div class="card" data-aos="fade-up">
                <h3 class="mb-3"><i class="fas fa-trophy" style="color:#F39C12;"></i> Program Studi Populer</h3>
                <div id="popularPrograms">
                    <p class="text-muted">Memuat data...</p>
                </div>
            </div>

            <!-- System Info -->
            <div class="card" data-aos="fade-up" data-aos-delay="100">
                <h3 class="mb-3"><i class="fas fa-server" style="color:var(--color-accent-blue);"></i> Info Sistem</h3>
                <div id="systemInfo">
                    <div style="display:grid;gap:1rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);">
                            <span style="font-size:0.85rem;color:var(--color-text-light);"><i class="fas fa-clock"></i> Uptime</span>
                            <strong id="uptime" style="font-size:0.9rem;">--</strong>
                        </div>
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);">
                            <span style="font-size:0.85rem;color:var(--color-text-light);"><i class="fas fa-code-branch"></i> Model Version</span>
                            <strong id="modelVersion" style="font-size:0.9rem;">--</strong>
                        </div>
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);">
                            <span style="font-size:0.85rem;color:var(--color-text-light);"><i class="fas fa-graduation-cap"></i> Last Trained</span>
                            <strong id="lastTrained" style="font-size:0.9rem;">--</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
