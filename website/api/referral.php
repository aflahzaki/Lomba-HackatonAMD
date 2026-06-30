<?php
/**
 * LangkahKampus - Referral API
 * 
 * POST: Generate referral code for logged-in user
 * GET ?code=X: Track referral click (record IP, increment counter)
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

require_once '../config/app.php';
require_once '../includes/functions.php';

header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    // Generate referral code for logged-in user
    if (!is_logged_in()) {
        http_response_code(401);
        echo json_encode(['success' => false, 'error' => 'Unauthorized. Silakan login terlebih dahulu.']);
        exit;
    }

    $user_id = $_SESSION['user_id'];
    $referral_code = 'LK-' . strtoupper(substr(bin2hex(random_bytes(4)), 0, 8));

    // In production: INSERT INTO referral_tracking (user_id, referral_code) VALUES (?, ?)
    // Demo response:
    echo json_encode([
        'success' => true,
        'referral_code' => $referral_code,
        'referral_url' => APP_URL . '/ref/' . $referral_code,
        'message' => 'Referral code berhasil dibuat.'
    ]);
    exit;

} elseif ($method === 'GET' && isset($_GET['code'])) {
    // Track referral click
    $code = sanitize_input($_GET['code']);

    if (empty($code) || strlen($code) > 20) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Kode referral tidak valid.']);
        exit;
    }

    $visitor_ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';

    // In production:
    // 1. SELECT * FROM referral_tracking WHERE referral_code = ?
    // 2. Check if IP already in unique_ips JSON array
    // 3. If new IP: UPDATE click_count, append IP to unique_ips
    // 4. If unique_ips count >= REFERRAL_CLICKS_REQUIRED: UPDATE unlocked_predictions += REFERRAL_UNLOCK_PREDICTIONS

    // Demo response simulating successful tracking:
    $demo_unique_count = 3; // Would come from DB
    $demo_clicks_needed = REFERRAL_CLICKS_REQUIRED;
    $demo_unlocked = 0;

    $is_new_ip = true; // Would check against stored IPs

    if ($is_new_ip) {
        $demo_unique_count++;
    }

    // Check if threshold reached
    if ($demo_unique_count >= $demo_clicks_needed) {
        $demo_unlocked = REFERRAL_UNLOCK_PREDICTIONS;
    }

    echo json_encode([
        'success' => true,
        'code' => $code,
        'is_new_click' => $is_new_ip,
        'unique_clicks' => $demo_unique_count,
        'clicks_required' => $demo_clicks_needed,
        'unlocked_predictions' => $demo_unlocked,
        'message' => $is_new_ip ? 'Klik unik tercatat.' : 'IP sudah pernah tercatat sebelumnya.'
    ]);
    exit;

} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed.']);
    exit;
}
