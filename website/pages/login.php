<?php
$page_title = 'Masuk';
$base_path = '../';
require_once $base_path . 'config/app.php';
require_once $base_path . 'includes/functions.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Redirect if already logged in
if (is_logged_in()) {
    if (isset($_SESSION['user_role']) && $_SESSION['user_role'] === 'guru') {
        redirect('dashboard_guru.php');
    } else {
        redirect('dashboard_student.php');
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $page_title . ' - ' . APP_NAME; ?></title>
    <link rel="icon" type="image/png" href="<?php echo $base_path; ?>assets/images/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/style.css">
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/animations.css">
</head>
<body>
    <div class="auth-page">
        <canvas id="particleCanvas" class="particles-canvas"></canvas>

        <div class="auth-container">
            <div class="auth-card">
                <div class="auth-logo">
                    <img src="<?php echo $base_path; ?>assets/images/logo.png" alt="<?php echo APP_NAME; ?>">
                    <h2><?php echo APP_NAME; ?></h2>
                    <p class="text-muted">Masuk ke akun Anda</p>
                </div>

                <?php
                $flash = get_flash_message();
                if ($flash):
                ?>
                <div class="toast toast-<?php echo $flash['type']; ?>" style="position:relative;top:auto;right:auto;margin-bottom:1rem;">
                    <i class="fas fa-info-circle"></i>
                    <span><?php echo $flash['message']; ?></span>
                </div>
                <?php endif; ?>

                <form id="loginForm" method="POST" action="<?php echo $base_path; ?>api/auth.php">
                    <input type="hidden" name="action" value="login">
                    <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">

                    <div class="form-group">
                        <label class="form-label" for="email">Email</label>
                        <input type="email" id="email" name="email" class="form-control" 
                               placeholder="nama@email.com" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="password">Password</label>
                        <input type="password" id="password" name="password" class="form-control" 
                               placeholder="Masukkan password" required>
                    </div>

                    <div class="form-group" style="display:flex;justify-content:space-between;align-items:center;">
                        <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;cursor:pointer;">
                            <input type="checkbox" name="remember" value="1"> Ingat saya
                        </label>
                        <a href="#" style="font-size:0.85rem;">Lupa password?</a>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block btn-lg btn-ripple">
                        <i class="fas fa-sign-in-alt"></i> Masuk
                    </button>
                </form>

                <div class="text-center mt-3">
                    <p class="text-muted" style="font-size:0.9rem;">
                        Belum punya akun? <a href="register.php"><strong>Daftar sekarang</strong></a>
                    </p>
                </div>

                <div class="text-center mt-2">
                    <a href="<?php echo $base_path; ?>index.php" style="font-size:0.85rem;color:var(--color-text-muted);">
                        <i class="fas fa-arrow-left"></i> Kembali ke Beranda
                    </a>
                </div>
            </div>
        </div>
    </div>

    <script src="<?php echo $base_path; ?>assets/js/main.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        initParticleBackground();
    });
    </script>
</body>
</html>
