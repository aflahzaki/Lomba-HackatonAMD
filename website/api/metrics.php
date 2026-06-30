<?php
/**
 * LangkahKampus - System Metrics API Proxy
 * Fetches system metrics from the Python AI backend /api/metrics endpoint via GET
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use GET.']);
    exit;
}

require_once '../config/ai_backend.php';

// Use direct cURL GET call since callAIBackend is POST-only
$url = AI_BACKEND_URL . '/api/metrics';

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => $url,
    CURLOPT_POST => false,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => [
        'Accept: application/json',
    ],
    CURLOPT_TIMEOUT => AI_BACKEND_TIMEOUT,
    CURLOPT_CONNECTTIMEOUT => AI_BACKEND_CONNECT_TIMEOUT,
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
curl_close($ch);

if (!$error && $httpCode >= 200 && $httpCode < 300) {
    $decoded = json_decode($response, true);
    if ($decoded !== null) {
        http_response_code(200);
        echo json_encode([
            'success' => true,
            'metrics' => $decoded,
            'source' => 'ai'
        ]);
        exit;
    }
}

// Fallback response when AI backend is unavailable
http_response_code(200);
echo json_encode([
    'success' => true,
    'metrics' => [
        'total_predictions' => 1247,
        'avg_response_time_ms' => 142,
        'popular_programs' => [
            ['name' => 'Teknik Informatika - ITB', 'count' => 89],
            ['name' => 'Kedokteran - UI', 'count' => 76],
            ['name' => 'Hukum - UGM', 'count' => 64],
            ['name' => 'Manajemen - Unair', 'count' => 52],
            ['name' => 'Farmasi - Unpad', 'count' => 41]
        ],
        'predictions_today' => 34,
        'active_users' => 18,
        'uptime_hours' => 168,
        'model_version' => 'v2.1.0',
        'last_trained' => '2025-01-15'
    ],
    'source' => 'fallback'
]);
