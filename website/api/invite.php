<?php
/**
 * LangkahKampus - Invite Code API
 * Handles invite code generation for students
 */

session_start();

require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/functions.php';

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    flash_message('danger', 'Method tidak diizinkan.');
    redirect('../pages/dashboard_student.php');
    exit;
}

// Check authentication
if (!is_logged_in()) {
    flash_message('warning', 'Silakan login terlebih dahulu.');
    redirect('../pages/login.php');
    exit;
}

// Check role - only students can generate invite codes
$user = get_user();
if ($user['role'] !== 'student') {
    flash_message('danger', 'Hanya siswa yang dapat membuat kode undangan.');
    redirect('../pages/dashboard_student.php');
    exit;
}

$action = isset($_POST['action']) ? sanitize_input($_POST['action']) : '';

switch ($action) {
    case 'generate':
        handleGenerateCode();
        break;
    default:
        flash_message('danger', 'Aksi tidak valid.');
        redirect('../pages/dashboard_student.php');
        break;
}

/**
 * Generate a new invite code for the current student
 */
function handleGenerateCode()
{
    // CSRF verification
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/dashboard_student.php');
        return;
    }

    $student_id = $_SESSION['user_id'];

    // Connect to database
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/dashboard_student.php');
        return;
    }

    try {
        // Check current active codes count (max 2)
        $countStmt = $pdo->prepare('SELECT COUNT(*) as total FROM invite_codes WHERE student_id = :student_id AND is_active = TRUE');
        $countStmt->execute([':student_id' => $student_id]);
        $result = $countStmt->fetch();

        if ($result['total'] >= 2) {
            flash_message('warning', 'Anda sudah memiliki 2 kode undangan aktif. Maksimal 2 kode aktif per siswa.');
            redirect('../pages/dashboard_student.php');
            return;
        }

        // Generate unique 6-character alphanumeric code
        $code = generateUniqueCode($pdo);

        // Insert new code
        $insertStmt = $pdo->prepare(
            'INSERT INTO invite_codes (student_id, code, is_active, created_at) VALUES (:student_id, :code, TRUE, NOW())'
        );
        $insertStmt->execute([
            ':student_id' => $student_id,
            ':code' => $code,
        ]);

        // Code is safe to display directly (alphanumeric only from controlled charset)
        flash_message('success', 'Kode undangan berhasil dibuat: ' . htmlspecialchars($code, ENT_QUOTES, 'UTF-8'));
        redirect('../pages/dashboard_student.php');

    } catch (RuntimeException $e) {
        error_log('Invite code generation error: ' . $e->getMessage());
        flash_message('danger', 'Gagal membuat kode undangan. Silakan coba lagi.');
        redirect('../pages/dashboard_student.php');
    } catch (PDOException $e) {
        error_log('Invite code generation error: ' . $e->getMessage());
        flash_message('danger', 'Terjadi kesalahan sistem. Silakan coba lagi.');
        redirect('../pages/dashboard_student.php');
    }
}

/**
 * Generate a unique 6-character code using cryptographically secure randomness
 */
function generateUniqueCode($pdo)
{
    $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $chars_len = strlen($chars);
    $max_attempts = 20;

    for ($i = 0; $i < $max_attempts; $i++) {
        $code = '';
        for ($j = 0; $j < 6; $j++) {
            $code .= $chars[random_int(0, $chars_len - 1)];
        }

        // Check uniqueness
        $checkStmt = $pdo->prepare('SELECT id FROM invite_codes WHERE code = :code LIMIT 1');
        $checkStmt->execute([':code' => $code]);

        if (!$checkStmt->fetch()) {
            return $code;
        }
    }

    // If all attempts collide, throw an exception rather than returning an unchecked code
    throw new RuntimeException('Unable to generate a unique invite code after ' . $max_attempts . ' attempts.');
}
