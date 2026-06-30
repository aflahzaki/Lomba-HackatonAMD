<?php
/**
 * LangkahKampus - Guru API
 * Handles guru-specific actions like adding comments
 */

session_start();

require_once __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/functions.php';

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    flash_message('danger', 'Method tidak diizinkan.');
    redirect('../pages/dashboard_guru.php');
    exit;
}

// Check authentication
if (!is_logged_in()) {
    flash_message('warning', 'Silakan login terlebih dahulu.');
    redirect('../pages/login.php');
    exit;
}

// Check role - only guru can access
$user = get_user();
if ($user['role'] !== 'guru') {
    flash_message('danger', 'Anda tidak memiliki akses ke fitur ini.');
    redirect('../pages/dashboard_student.php');
    exit;
}

$action = isset($_POST['action']) ? sanitize_input($_POST['action']) : '';

switch ($action) {
    case 'add_comment':
        handleAddComment();
        break;
    case 'claim_code':
        handleClaimCode();
        break;
    default:
        flash_message('danger', 'Aksi tidak valid.');
        redirect('../pages/dashboard_guru.php');
        break;
}

/**
 * Add a comment/evaluation for a student
 */
function handleAddComment()
{
    // CSRF verification
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    $guru_id = $_SESSION['user_id'];
    $student_id = isset($_POST['student_id']) ? (int) $_POST['student_id'] : 0;
    $comment_text = isset($_POST['comment_text']) ? trim($_POST['comment_text']) : '';

    // Validate inputs
    if ($student_id <= 0) {
        flash_message('danger', 'ID siswa tidak valid.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    if (empty($comment_text)) {
        flash_message('danger', 'Komentar tidak boleh kosong.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    if (strlen($comment_text) > 1000) {
        flash_message('danger', 'Komentar terlalu panjang (maksimal 1000 karakter).');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    // Connect to database
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    try {
        // Validate that guru is linked to this student via invite_codes
        $linkStmt = $pdo->prepare(
            'SELECT id FROM invite_codes WHERE student_id = :student_id AND used_by_guru_id = :guru_id LIMIT 1'
        );
        $linkStmt->execute([
            ':student_id' => $student_id,
            ':guru_id' => $guru_id,
        ]);

        if (!$linkStmt->fetch()) {
            flash_message('danger', 'Anda tidak terhubung dengan siswa ini.');
            redirect('../pages/dashboard_guru.php');
            return;
        }

        // Insert comment
        $insertStmt = $pdo->prepare(
            'INSERT INTO guru_comments (guru_id, student_id, comment_text, created_at) VALUES (:guru_id, :student_id, :comment_text, NOW())'
        );
        $insertStmt->execute([
            ':guru_id' => $guru_id,
            ':student_id' => $student_id,
            ':comment_text' => $comment_text,
        ]);

        flash_message('success', 'Komentar berhasil ditambahkan.');
        redirect('../pages/dashboard_guru.php');

    } catch (PDOException $e) {
        error_log('Guru comment error: ' . $e->getMessage());
        flash_message('danger', 'Terjadi kesalahan sistem. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
    }
}

/**
 * Claim an invite code to link guru with an additional student (post-registration)
 */
function handleClaimCode()
{
    // CSRF verification
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    $guru_id = $_SESSION['user_id'];
    $invite_code = isset($_POST['invite_code']) ? strtoupper(trim($_POST['invite_code'])) : '';

    // Validate invite code format
    if (empty($invite_code) || strlen($invite_code) !== 6) {
        flash_message('danger', 'Kode undangan harus 6 karakter.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    // Connect to database
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
        return;
    }

    try {
        // Look up the invite code - must be active and unclaimed
        $codeStmt = $pdo->prepare(
            'SELECT id, student_id FROM invite_codes WHERE code = :code AND is_active = TRUE AND used_by_guru_id IS NULL LIMIT 1'
        );
        $codeStmt->execute([':code' => $invite_code]);
        $inviteRecord = $codeStmt->fetch();

        if (!$inviteRecord) {
            flash_message('danger', 'Kode undangan tidak valid, sudah digunakan, atau sudah tidak aktif.');
            redirect('../pages/dashboard_guru.php');
            return;
        }

        // Check if guru is already linked to this student via another code
        $existingLink = $pdo->prepare(
            'SELECT id FROM invite_codes WHERE student_id = :student_id AND used_by_guru_id = :guru_id LIMIT 1'
        );
        $existingLink->execute([
            ':student_id' => $inviteRecord['student_id'],
            ':guru_id' => $guru_id,
        ]);

        if ($existingLink->fetch()) {
            flash_message('warning', 'Anda sudah terhubung dengan siswa ini.');
            redirect('../pages/dashboard_guru.php');
            return;
        }

        // Claim the invite code - link guru to the student
        $updateStmt = $pdo->prepare(
            'UPDATE invite_codes SET used_by_guru_id = :guru_id, used_at = NOW(), is_active = FALSE WHERE id = :id'
        );
        $updateStmt->execute([
            ':guru_id' => $guru_id,
            ':id' => $inviteRecord['id'],
        ]);

        flash_message('success', 'Kode undangan berhasil diklaim. Siswa baru telah ditambahkan ke daftar Anda.');
        redirect('../pages/dashboard_guru.php');

    } catch (PDOException $e) {
        error_log('Guru claim code error: ' . $e->getMessage());
        flash_message('danger', 'Terjadi kesalahan sistem. Silakan coba lagi.');
        redirect('../pages/dashboard_guru.php');
    }
}
