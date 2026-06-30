<?php
$page_title = 'Dashboard Guru';
$page_scripts = ['dashboard.js'];

// Auth middleware must run before any HTML output to avoid "headers already sent" issues
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../includes/functions.php';
require_once __DIR__ . '/../includes/auth_middleware.php';
require_role(['guru']);

include '../includes/header.php';

// Current guru info
$guru_name = isset($_SESSION['user_name']) ? $_SESSION['user_name'] : 'Bu Ratna';
$guru_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 3;

// Demo data: Students linked to this guru via invite codes
$linked_students = [
    [
        'id' => 1,
        'name' => 'Ahmad Rizki Pratama',
        'school' => 'SMAN 3 Bandung',
        'last_prediction' => '78%',
        'prediction_program' => 'Teknik Informatika - ITB',
        'prediction_color' => 'success',
    ],
    [
        'id' => 8,
        'name' => 'Rizky Maulana',
        'school' => 'SMAN 3 Bandung',
        'last_prediction' => '65%',
        'prediction_program' => 'Sistem Informasi - ITB',
        'prediction_color' => 'warning',
    ],
];

// Demo data: Comments for each student
$student_comments = [
    1 => [
        ['text' => 'Ahmad memiliki potensi besar di bidang STEM. Sangat direkomendasikan untuk Teknik Informatika UI/ITB.', 'date' => '2025-01-08 10:30:00'],
    ],
    8 => [
        ['text' => 'Rizky perlu meningkatkan nilai Matematika untuk memperkuat peluang di program studi pilihan.', 'date' => '2025-01-10 14:15:00'],
    ],
];

$total_students = count($linked_students);
?>

<div class="dashboard-page">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
        <div class="container">
            <div class="d-flex align-center justify-between flex-wrap gap-2">
                <div>
                    <h1><i class="fas fa-chalkboard-teacher"></i> Selamat Datang, <?php echo htmlspecialchars($guru_name); ?>!</h1>
                    <p><i class="fas fa-users"></i> Panel Guru - Evaluasi & Bimbingan Siswa</p>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Stats -->
        <div class="dashboard-grid" data-aos="fade-up">
            <div class="stat-card">
                <div class="stat-card-icon blue">
                    <i class="fas fa-user-graduate"></i>
                </div>
                <div class="stat-card-info">
                    <h3><?php echo $total_students; ?></h3>
                    <p>Siswa Terhubung</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-card-icon green">
                    <i class="fas fa-comments"></i>
                </div>
                <div class="stat-card-info">
                    <h3><?php echo array_sum(array_map('count', $student_comments)); ?></h3>
                    <p>Total Evaluasi</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-card-icon orange">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="stat-card-info">
                    <h3>72%</h3>
                    <p>Rata-rata Peluang Siswa</p>
                </div>
            </div>
        </div>

        <!-- Claim Invite Code -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="50">
            <h3 class="mb-2"><i class="fas fa-key"></i> Klaim Kode Undangan</h3>
            <p class="text-muted mb-2">Masukkan kode undangan dari siswa untuk menambahkan mereka ke daftar bimbingan Anda.</p>
            <form action="<?php echo $base_path; ?>api/guru.php" method="POST" class="d-flex align-center gap-2 flex-wrap">
                <input type="hidden" name="action" value="claim_code">
                <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
                <div class="form-group" style="margin-bottom:0;flex:1;min-width:200px;">
                    <input type="text" name="invite_code" class="form-control" placeholder="Masukkan 6 karakter kode" maxlength="6" pattern="[A-Za-z0-9]{6}" required style="text-transform:uppercase;">
                </div>
                <button type="submit" class="btn btn-primary btn-sm btn-ripple">
                    <i class="fas fa-plus-circle"></i> Klaim Kode
                </button>
            </form>
        </div>

        <!-- Student List Table -->
        <div class="card mb-3" data-aos="fade-up" data-aos-delay="100">
            <div class="d-flex align-center justify-between mb-3">
                <h3><i class="fas fa-list"></i> Daftar Siswa Saya</h3>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Nama Siswa</th>
                            <th>Sekolah</th>
                            <th>Prediksi Terakhir</th>
                            <th>Program Studi</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($linked_students as $student): ?>
                        <tr>
                            <td><strong><?php echo htmlspecialchars($student['name']); ?></strong></td>
                            <td><?php echo htmlspecialchars($student['school']); ?></td>
                            <td><span class="badge badge-<?php echo $student['prediction_color']; ?>"><?php echo $student['last_prediction']; ?></span></td>
                            <td><?php echo htmlspecialchars($student['prediction_program']); ?></td>
                            <td>
                                <a href="#student-<?php echo $student['id']; ?>" class="btn btn-sm btn-primary">
                                    <i class="fas fa-comment"></i> Evaluasi
                                </a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Comment Sections per Student -->
        <?php foreach ($linked_students as $student): ?>
        <div class="card mb-3" data-aos="fade-up" id="student-<?php echo $student['id']; ?>">
            <h3 class="mb-2">
                <i class="fas fa-user-circle"></i> Evaluasi: <?php echo htmlspecialchars($student['name']); ?>
            </h3>
            <p class="text-muted mb-2"><?php echo htmlspecialchars($student['school']); ?> | Prediksi: <?php echo htmlspecialchars($student['prediction_program']); ?> (<?php echo $student['last_prediction']; ?>)</p>

            <!-- Existing Comments -->
            <?php if (isset($student_comments[$student['id']]) && !empty($student_comments[$student['id']])): ?>
                <?php foreach ($student_comments[$student['id']] as $comment): ?>
                <div style="background:rgba(26,115,232,0.05);border-radius:var(--radius-sm);padding:1rem;margin-bottom:0.75rem;border-left:4px solid var(--color-accent-blue);">
                    <p style="font-size:0.9rem;margin-bottom:0.25rem;"><?php echo htmlspecialchars($comment['text']); ?></p>
                    <small class="text-muted"><i class="fas fa-clock"></i> <?php echo format_date_id($comment['date']); ?></small>
                </div>
                <?php endforeach; ?>
            <?php else: ?>
                <p class="text-muted mb-2"><em>Belum ada evaluasi untuk siswa ini.</em></p>
            <?php endif; ?>

            <!-- Add Comment Form -->
            <form action="<?php echo $base_path; ?>api/guru.php" method="POST" style="margin-top:1rem;">
                <input type="hidden" name="action" value="add_comment">
                <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
                <input type="hidden" name="student_id" value="<?php echo $student['id']; ?>">
                <div class="form-group">
                    <label for="comment_<?php echo $student['id']; ?>">Tambah Evaluasi / Komentar:</label>
                    <textarea 
                        id="comment_<?php echo $student['id']; ?>" 
                        name="comment_text" 
                        class="form-control" 
                        rows="3" 
                        placeholder="Tulis evaluasi atau saran untuk siswa ini..."
                        required
                    ></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-sm btn-ripple">
                    <i class="fas fa-paper-plane"></i> Kirim Evaluasi
                </button>
            </form>
        </div>
        <?php endforeach; ?>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
