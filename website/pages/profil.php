<?php
$page_title = 'Profil Saya';
include '../includes/header.php';

// Demo user data
$user_data = [
    'full_name' => 'Anisa Rahmawati',
    'email' => 'anisa@example.com',
    'phone' => '081234567890',
    'school' => 'SMAN 3 Bandung',
    'province' => 'Jawa Barat',
    'major_track' => 'IPA',
    'ranking' => 5,
    'total_students' => 320,
    'is_premium' => false
];
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-user-circle"></i> Profil Saya</h1>
            <p>Ringkasan informasi akun Anda</p>
        </div>
    </div>

    <div class="container">
        <div style="max-width:600px;margin:0 auto;">
            <!-- Profile Card -->
            <div class="card text-center mb-3" data-aos="fade-up">
                <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,var(--color-accent-blue),var(--color-primary));display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;color:#fff;font-size:2rem;">
                    <i class="fas fa-user"></i>
                </div>
                <h3><?php echo $user_data['full_name']; ?></h3>
                <p class="text-muted" style="font-size:0.9rem;"><?php echo $user_data['email']; ?></p>
                <span class="badge <?php echo $user_data['is_premium'] ? 'badge-success' : 'badge-info'; ?> mt-1">
                    <?php echo $user_data['is_premium'] ? 'Premium' : 'Gratis'; ?>
                </span>
            </div>

            <!-- Info Summary -->
            <div class="card mb-3" data-aos="fade-up" data-aos-delay="100">
                <h4 class="mb-2"><i class="fas fa-info-circle text-blue"></i> Informasi</h4>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                    <div>
                        <small class="text-muted">Sekolah</small>
                        <p style="font-weight:600;"><?php echo $user_data['school']; ?></p>
                    </div>
                    <div>
                        <small class="text-muted">Provinsi</small>
                        <p style="font-weight:600;"><?php echo $user_data['province']; ?></p>
                    </div>
                    <div>
                        <small class="text-muted">Jurusan</small>
                        <p style="font-weight:600;"><?php echo $user_data['major_track']; ?></p>
                    </div>
                    <div>
                        <small class="text-muted">Peringkat</small>
                        <p style="font-weight:600;"><?php echo $user_data['ranking']; ?>/<?php echo $user_data['total_students']; ?></p>
                    </div>
                    <div>
                        <small class="text-muted">No. Telepon</small>
                        <p style="font-weight:600;"><?php echo $user_data['phone']; ?></p>
                    </div>
                </div>
            </div>

            <!-- Action -->
            <div class="card text-center" data-aos="fade-up" data-aos-delay="200">
                <p class="text-muted mb-2">Untuk mengedit data akademik dan informasi profil, silakan gunakan Dashboard.</p>
                <a href="dashboard_student.php" class="btn btn-primary btn-ripple">
                    <i class="fas fa-edit"></i> Edit di Dashboard
                </a>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
