<?php
/**
 * LangkahKampus - Shared Form-POST API Helpers
 *
 * Consolidates the guard boilerplate duplicated in form-based API endpoints
 * (guru.php, invite.php): session init, require includes, POST-only check,
 * authentication, role enforcement, and CSRF verification.
 */

/**
 * Bootstrap a form-post API endpoint.
 *
 * Starts the session, loads app config + helpers, then enforces:
 *   1. POST-only method
 *   2. User is logged in
 *   3. User has an allowed role
 *
 * Terminates with a flash-message redirect on any failure.
 *
 * @param string       $required_role   Required role (e.g. "guru", "student")
 * @param string       $redirect_page   Page to redirect on error (relative to pages/)
 * @return array       The authenticated user array from get_user()
 */
function guard_form_api(string $required_role, string $redirect_page): array
{
    session_start();

    require_once __DIR__ . '/../config/app.php';
    require_once __DIR__ . '/../config/database.php';
    require_once __DIR__ . '/../includes/functions.php';

    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        flash_message('danger', 'Method tidak diizinkan.');
        redirect('../pages/' . $redirect_page);
        exit;
    }

    if (!is_logged_in()) {
        flash_message('warning', 'Silakan login terlebih dahulu.');
        redirect('../pages/login.php');
        exit;
    }

    $user = get_user();
    if ($user['role'] !== $required_role) {
        flash_message('danger', 'Anda tidak memiliki akses ke fitur ini.');
        redirect('../pages/' . $redirect_page);
        exit;
    }

    return $user;
}

/**
 * Verify the CSRF token from $_POST, redirecting on failure.
 *
 * @param string $redirect_page  Page to redirect on failure (relative to pages/)
 */
function require_csrf(string $redirect_page): void
{
    $csrf_token = isset($_POST['csrf_token']) ? $_POST['csrf_token'] : '';
    if (!verify_csrf_token($csrf_token)) {
        flash_message('danger', 'Token keamanan tidak valid. Silakan coba lagi.');
        redirect('../pages/' . $redirect_page);
        exit;
    }
}

/**
 * Obtain a PDO connection or redirect with a flash-message on failure.
 *
 * @param string $redirect_page  Page to redirect on failure (relative to pages/)
 * @return PDO
 */
function require_db_or_redirect(string $redirect_page): PDO
{
    $pdo = getDBConnection();
    if (!$pdo) {
        flash_message('danger', 'Koneksi database gagal. Silakan coba lagi.');
        redirect('../pages/' . $redirect_page);
        exit;
    }
    return $pdo;
}
