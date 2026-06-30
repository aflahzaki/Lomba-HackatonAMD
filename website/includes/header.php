<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Determine relative path to root
$current_dir = basename(dirname($_SERVER['SCRIPT_NAME']));
$base_path = ($current_dir === 'pages' || $current_dir === 'api') ? '../' : '';

require_once $base_path . 'config/app.php';
require_once $base_path . 'includes/functions.php';
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="<?php echo APP_DESCRIPTION; ?>">
    <title><?php echo isset($page_title) ? $page_title . ' - ' . APP_NAME : APP_NAME . ' - ' . APP_TAGLINE; ?></title>

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="<?php echo $base_path; ?>assets/images/logo.png">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- AOS Animation Library -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

    <!-- Leaflet CSS (for map pages) -->
    <?php if (isset($use_leaflet) && $use_leaflet): ?>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <?php endif; ?>

    <!-- Custom CSS -->
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/style.css">
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/animations.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="<?php echo $base_path; ?>index.php" class="nav-logo">
                <img src="<?php echo $base_path; ?>assets/images/logo.png" alt="<?php echo APP_NAME; ?>" class="nav-logo-img">
                <span class="nav-logo-text"><?php echo APP_NAME; ?></span>
            </a>

            <ul class="nav-menu" id="navMenu">
                <?php if (is_logged_in()): ?>
                    <?php $nav_user = get_user(); ?>
                    <?php if ($nav_user['role'] === 'guru'): ?>
                        <!-- Guru Navigation -->
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>index.php" class="nav-link">Beranda</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/dashboard_guru.php" class="nav-link">Siswa Saya</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/profil.php" class="nav-link">Profil</a>
                        </li>
                    <?php else: ?>
                        <!-- Student Navigation -->
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>index.php" class="nav-link">Beranda</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/prediksi.php" class="nav-link">Prediksi</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/rekomendasi.php" class="nav-link">Rekomendasi</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/peta_universitas.php" class="nav-link">Peta Universitas</a>
                        </li>
                        <li class="nav-item">
                            <a href="<?php echo $base_path; ?>pages/pembayaran.php" class="nav-link">Pembayaran</a>
                        </li>
                    <?php endif; ?>
                <?php else: ?>
                    <!-- Guest Navigation -->
                    <li class="nav-item">
                        <a href="<?php echo $base_path; ?>index.php" class="nav-link">Beranda</a>
                    </li>
                    <li class="nav-item">
                        <a href="<?php echo $base_path; ?>pages/tentang.php" class="nav-link">Tentang</a>
                    </li>
                    <li class="nav-item">
                        <a href="<?php echo $base_path; ?>pages/login.php" class="nav-link">Login</a>
                    </li>
                    <li class="nav-item">
                        <a href="<?php echo $base_path; ?>pages/register.php" class="nav-link">Daftar</a>
                    </li>
                <?php endif; ?>
            </ul>

            <div class="nav-actions">
                <?php if (is_logged_in()): ?>
                    <?php $action_user = get_user(); ?>
                    <?php $dashboard_link = ($action_user['role'] === 'guru') ? $base_path . 'pages/dashboard_guru.php' : $base_path . 'pages/dashboard_student.php'; ?>
                    <a href="<?php echo $dashboard_link; ?>" class="btn btn-outline btn-sm">
                        <i class="fas fa-user-circle"></i> <?php echo htmlspecialchars($action_user['full_name']); ?>
                    </a>
                    <a href="<?php echo $base_path; ?>api/auth.php?action=logout" class="btn btn-sm btn-ghost">Keluar</a>
                <?php else: ?>
                    <a href="<?php echo $base_path; ?>pages/login.php" class="btn btn-outline btn-sm">Masuk</a>
                    <a href="<?php echo $base_path; ?>pages/register.php" class="btn btn-primary btn-sm">Daftar</a>
                <?php endif; ?>
            </div>

            <!-- Mobile Menu Toggle -->
            <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </nav>

    <!-- Flash Messages -->
    <?php
    $flash = get_flash_message();
    if ($flash):
    ?>
    <div class="toast toast-<?php echo $flash['type']; ?>" id="flashToast">
        <i class="fas fa-<?php echo $flash['type'] === 'success' ? 'check-circle' : ($flash['type'] === 'danger' ? 'exclamation-circle' : 'info-circle'); ?>"></i>
        <span><?php echo $flash['message']; ?></span>
        <button class="toast-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    </div>
    <?php endif; ?>

    <!-- Main Content Wrapper -->
    <main class="main-content">
