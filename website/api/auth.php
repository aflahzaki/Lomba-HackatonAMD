<?php
/**
 * LangkahKampus - Authentication API
 * Handles login, register, and logout actions
 */

session_start();

require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/functions.php';

// Determine action from POST or GET
$action = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = isset($_POST['action']) ? sanitize_input($_POST['action']) : '';
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = isset($_GET['action']) ? sanitize_input($_GET['action']) : '';
}

switch ($action) {
    case 'login':
        handleLogin();
        break;
    case 'register':
        handleRegister();
        break;
    case 'logout':
        handleLogout();
        break;
    default:
        flash_message('danger', 'Aksi tidak valid.');
        redirect('../pages/login.php');
        break;
}

/**
 * Handle user login
 */
function handleLogin()
{
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        flash_message('danger', 'Method tidak diizinkan.');
        redirect('../pages/login.php');
        return;
    }

    // CSRF verification
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/login.php');
        return;
    }

    // Validate input
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';

    if (empty($email) || empty($password)) {
        flash_message('danger', 'Email dan password wajib diisi.');
        redirect('../pages/login.php');
        return;
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        flash_message('danger', 'Format email tidak valid.');
        redirect('../pages/login.php');
        return;
    }

    // Database lookup
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/login.php');
        return;
    }

    try {
        $stmt = $pdo->prepare('SELECT id, email, password_hash, full_name, role, is_premium, is_active FROM users WHERE email = :email LIMIT 1');
        $stmt->execute([':email' => $email]);
        $user = $stmt->fetch();

        if (!$user) {
            flash_message('danger', 'Email atau password salah.');
            redirect('../pages/login.php');
            return;
        }

        // Check if user is active
        if (!$user['is_active']) {
            flash_message('danger', 'Akun Anda telah dinonaktifkan. Hubungi administrator.');
            redirect('../pages/login.php');
            return;
        }

        // Verify password
        if (!password_verify($password, $user['password_hash'])) {
            flash_message('danger', 'Email atau password salah.');
            redirect('../pages/login.php');
            return;
        }

        // Set session variables
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_email'] = $user['email'];
        $_SESSION['user_name'] = $user['full_name'];
        $_SESSION['user_role'] = $user['role'];
        $_SESSION['is_premium'] = (bool) $user['is_premium'];

        // Update last login timestamp
        $updateStmt = $pdo->prepare('UPDATE users SET last_login = NOW() WHERE id = :id');
        $updateStmt->execute([':id' => $user['id']]);

        // Regenerate session ID to prevent fixation
        session_regenerate_id(true);

        // Clear CSRF token after successful login
        unset($_SESSION['csrf_token']);

        flash_message('success', 'Selamat datang kembali, ' . htmlspecialchars($user['full_name']) . '!');

        // Role-based redirect
        switch ($user['role']) {
            case 'guru':
                redirect('../pages/dashboard_guru.php');
                break;
            case 'platform_admin':
            case 'student':
            default:
                redirect('../pages/dashboard_student.php');
                break;
        }

    } catch (PDOException $e) {
        error_log('Login error: ' . $e->getMessage());
        flash_message('danger', 'Terjadi kesalahan sistem. Silakan coba lagi.');
        redirect('../pages/login.php');
    }
}

/**
 * Handle user registration
 */
function handleRegister()
{
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        flash_message('danger', 'Method tidak diizinkan.');
        redirect('../pages/register.php');
        return;
    }

    // CSRF verification
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/register.php');
        return;
    }

    // Collect and validate input
    $full_name = isset($_POST['full_name']) ? trim($_POST['full_name']) : '';
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $phone = isset($_POST['phone']) ? trim($_POST['phone']) : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';
    $confirm_password = isset($_POST['confirm_password']) ? $_POST['confirm_password'] : '';
    $role = isset($_POST['role']) ? trim($_POST['role']) : 'student';

    // Validate required fields
    if (empty($full_name) || empty($email) || empty($password)) {
        flash_message('danger', 'Nama, email, dan password wajib diisi.');
        redirect('../pages/register.php');
        return;
    }

    // Validate email format
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        flash_message('danger', 'Format email tidak valid.');
        redirect('../pages/register.php');
        return;
    }

    // Validate password length
    if (strlen($password) < 8) {
        flash_message('danger', 'Password minimal 8 karakter.');
        redirect('../pages/register.php');
        return;
    }

    // Validate password confirmation
    if ($password !== $confirm_password) {
        flash_message('danger', 'Konfirmasi password tidak cocok.');
        redirect('../pages/register.php');
        return;
    }

    // Validate role
    $allowed_roles = ['student', 'guru'];
    if (!in_array($role, $allowed_roles)) {
        $role = 'student';
    }

    // Validate invite code for guru role
    $invite_code = '';
    if ($role === 'guru') {
        $invite_code = isset($_POST['invite_code']) ? strtoupper(trim($_POST['invite_code'])) : '';
        if (empty($invite_code) || strlen($invite_code) !== 6) {
            flash_message('danger', 'Kode undangan wajib diisi (6 karakter) untuk pendaftaran guru.');
            redirect('../pages/register.php?type=guru');
            return;
        }
    }

    // Validate full name length
    if (strlen($full_name) > 100) {
        flash_message('danger', 'Nama terlalu panjang (maksimal 100 karakter).');
        redirect('../pages/register.php');
        return;
    }

    // Database operations
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/register.php');
        return;
    }

    try {
        // Check if email already exists
        $checkStmt = $pdo->prepare('SELECT id FROM users WHERE email = :email LIMIT 1');
        $checkStmt->execute([':email' => $email]);

        if ($checkStmt->fetch()) {
            flash_message('danger', 'Email sudah terdaftar. Silakan gunakan email lain atau login.');
            redirect('../pages/register.php');
            return;
        }

        // Validate invite code in database for guru role
        if ($role === 'guru') {
            $codeStmt = $pdo->prepare('SELECT id, student_id FROM invite_codes WHERE code = :code AND is_active = TRUE AND used_by_guru_id IS NULL LIMIT 1');
            $codeStmt->execute([':code' => $invite_code]);
            $inviteRecord = $codeStmt->fetch();

            if (!$inviteRecord) {
                flash_message('danger', 'Kode undangan tidak valid atau sudah digunakan.');
                redirect('../pages/register.php?type=guru');
                return;
            }
        }

        // Hash password
        $password_hash = password_hash($password, PASSWORD_BCRYPT);

        // Insert new user
        $insertStmt = $pdo->prepare(
            'INSERT INTO users (email, phone, password_hash, full_name, role, is_premium, is_active, created_at) 
             VALUES (:email, :phone, :password_hash, :full_name, :role, FALSE, TRUE, NOW())'
        );

        $insertStmt->execute([
            ':email' => $email,
            ':phone' => $phone ?: null,
            ':password_hash' => $password_hash,
            ':full_name' => $full_name,
            ':role' => $role,
        ]);

        $userId = $pdo->lastInsertId();

        // Update invite code for guru registration
        if ($role === 'guru') {
            $updateInvite = $pdo->prepare('UPDATE invite_codes SET used_by_guru_id = :guru_id, used_at = NOW(), is_active = FALSE WHERE id = :id');
            $updateInvite->execute([':guru_id' => $userId, ':id' => $inviteRecord['id']]);
        }

        // Create student_profiles row for siswa registration
        if ($role === 'student') {
            $school_id = isset($_POST['school_id']) ? trim($_POST['school_id']) : '';
            $school_name_manual = isset($_POST['school_name_manual']) ? trim($_POST['school_name_manual']) : '';
            $school_type_manual = isset($_POST['school_type_manual']) ? trim($_POST['school_type_manual']) : '';
            $school_province_manual = isset($_POST['school_province_manual']) ? trim($_POST['school_province_manual']) : '';
            $school_city_manual = isset($_POST['school_city_manual']) ? trim($_POST['school_city_manual']) : '';
            $major_track = isset($_POST['major_track']) ? trim($_POST['major_track']) : '';

            // Determine school_id: use autocomplete selection if provided, otherwise NULL for manual entry
            $final_school_id = null;
            if (!empty($school_id) && is_numeric($school_id)) {
                // Validate that school_id exists in the database
                $schoolCheck = $pdo->prepare('SELECT id FROM schools WHERE id = :id LIMIT 1');
                $schoolCheck->execute([':id' => (int) $school_id]);
                if ($schoolCheck->fetch()) {
                    $final_school_id = (int) $school_id;
                }
            }

            // Default major_track if empty
            if (empty($major_track)) {
                $major_track = 'IPA';
            }

            // Validate major_track against allowed values
            $allowed_major_tracks = [
                'IPA', 'IPS', 'Bahasa',
                'TKJ', 'RPL', 'Multimedia', 'AKL', 'TBSM', 'OTKP', 'BDP',
                'Farmasi', 'Keperawatan', 'DKV',
                'Teknik Kendaraan Ringan', 'Teknik Instalasi Tenaga Listrik',
                'Tata Busana', 'Tata Boga', 'Animasi'
            ];

            if (!in_array($major_track, $allowed_major_tracks)) {
                flash_message('danger', 'Jurusan/peminatan yang dipilih tidak valid.');
                redirect('../pages/register.php');
                return;
            }

            $profileStmt = $pdo->prepare(
                'INSERT INTO student_profiles (user_id, school_id, major_track, grade_level, school_name_manual, school_type_manual, school_province_manual, school_city_manual) 
                 VALUES (:user_id, :school_id, :major_track, 12, :school_name_manual, :school_type_manual, :school_province_manual, :school_city_manual)'
            );
            $profileStmt->execute([
                ':user_id' => $userId,
                ':school_id' => $final_school_id,
                ':major_track' => $major_track,
                ':school_name_manual' => $school_name_manual ?: null,
                ':school_type_manual' => $school_type_manual ?: null,
                ':school_province_manual' => $school_province_manual ?: null,
                ':school_city_manual' => $school_city_manual ?: null,
            ]);
        }

        // Set session variables (auto-login after registration)
        $_SESSION['user_id'] = $userId;
        $_SESSION['user_email'] = $email;
        $_SESSION['user_name'] = $full_name;
        $_SESSION['user_role'] = $role;
        $_SESSION['is_premium'] = false;

        // Regenerate session ID
        session_regenerate_id(true);

        // Clear CSRF token
        unset($_SESSION['csrf_token']);

        flash_message('success', 'Pendaftaran berhasil! Selamat datang di LangkahKampus.');

        // Role-based redirect after registration
        if ($role === 'guru') {
            redirect('../pages/dashboard_guru.php');
        } else {
            redirect('../pages/dashboard_student.php');
        }

    } catch (PDOException $e) {
        error_log('Registration error: ' . $e->getMessage());
        flash_message('danger', 'Terjadi kesalahan sistem. Silakan coba lagi.');
        redirect('../pages/register.php');
    }
}

/**
 * Handle user logout
 */
function handleLogout()
{
    // Clear all session data
    $_SESSION = [];

    // Destroy session cookie
    if (ini_get('session.use_cookies')) {
        $params = session_get_cookie_params();
        setcookie(
            session_name(),
            '',
            time() - 42000,
            $params['path'],
            $params['domain'],
            $params['secure'],
            $params['httponly']
        );
    }

    // Destroy session
    session_destroy();

    // Redirect to homepage
    header('Location: ../index.php');
    exit;
}
