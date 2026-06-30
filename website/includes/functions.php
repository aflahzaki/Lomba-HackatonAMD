<?php
/**
 * LangkahKampus - Utility Functions
 */

/**
 * Sanitize user input
 */
function sanitize_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

/**
 * Redirect to a URL
 */
function redirect($url)
{
    header("Location: $url");
    exit();
}

/**
 * Check if user is logged in
 */
function is_logged_in()
{
    return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
}

/**
 * Get current logged-in user data
 */
function get_user()
{
    if (!is_logged_in()) {
        return null;
    }

    return [
        'id' => $_SESSION['user_id'] ?? null,
        'email' => $_SESSION['user_email'] ?? '',
        'full_name' => $_SESSION['user_name'] ?? '',
        'role' => $_SESSION['user_role'] ?? 'student',
        'is_premium' => $_SESSION['is_premium'] ?? false,
    ];
}

/**
 * Set flash message
 */
function flash_message($type, $message)
{
    $_SESSION['flash'] = [
        'type' => $type,
        'message' => $message
    ];
}

/**
 * Get and clear flash message
 */
function get_flash_message()
{
    if (isset($_SESSION['flash'])) {
        $flash = $_SESSION['flash'];
        unset($_SESSION['flash']);
        return $flash;
    }
    return null;
}

/**
 * Format number as Indonesian Rupiah
 */
function format_rupiah($amount)
{
    return 'Rp' . number_format($amount, 0, ',', '.');
}

/**
 * Get prediction color class based on probability
 */
function calculate_prediction_color($probability)
{
    if ($probability >= 70) {
        return 'success';
    } elseif ($probability >= 40) {
        return 'warning';
    }
    return 'danger';
}

/**
 * Generate CSRF token
 */
function generate_csrf_token()
{
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify CSRF token
 */
function verify_csrf_token($token)
{
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Get base URL for the application
 */
function base_url($path = '')
{
    $base = rtrim(APP_URL, '/');
    if (!empty($path)) {
        $base .= '/' . ltrim($path, '/');
    }
    return $base;
}

/**
 * Get asset URL
 */
function asset_url($path)
{
    return 'assets/' . ltrim($path, '/');
}

/**
 * Format date in Indonesian
 */
function format_date_id($datetime)
{
    $months = [
        1 => 'Januari', 2 => 'Februari', 3 => 'Maret', 4 => 'April',
        5 => 'Mei', 6 => 'Juni', 7 => 'Juli', 8 => 'Agustus',
        9 => 'September', 10 => 'Oktober', 11 => 'November', 12 => 'Desember'
    ];

    $timestamp = strtotime($datetime);
    $day = date('d', $timestamp);
    $month = $months[(int)date('m', $timestamp)];
    $year = date('Y', $timestamp);

    return "$day $month $year";
}

/**
 * Truncate text with ellipsis
 */
function truncate_text($text, $length = 100)
{
    if (strlen($text) <= $length) {
        return $text;
    }
    return substr($text, 0, $length) . '...';
}
