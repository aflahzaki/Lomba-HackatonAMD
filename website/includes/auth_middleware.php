<?php
/**
 * LangkahKampus - Authentication Middleware
 * Include this file at the top of protected pages
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

/**
 * Require authentication - redirect to login if not logged in
 */
function require_auth()
{
    if (!is_logged_in()) {
        flash_message('warning', 'Silakan login terlebih dahulu.');
        redirect('pages/login.php');
    }
}

/**
 * Require specific role
 */
function require_role($allowed_roles)
{
    require_auth();

    if (!is_array($allowed_roles)) {
        $allowed_roles = [$allowed_roles];
    }

    $user = get_user();
    if (!in_array($user['role'], $allowed_roles)) {
        flash_message('danger', 'Anda tidak memiliki akses ke halaman ini.');
        redirect('pages/dashboard_student.php');
    }
}

/**
 * Require premium subscription
 */
function require_premium()
{
    require_auth();

    $user = get_user();
    if (!$user['is_premium']) {
        flash_message('warning', 'Fitur ini memerlukan langganan Premium.');
        redirect('pages/pembayaran.php');
    }
}

/**
 * Check if current user has a specific role
 */
function has_role($role)
{
    $user = get_user();
    if (!$user) {
        return false;
    }
    return $user['role'] === $role;
}
