<?php
/**
 * LangkahKampus - SHAP Explanation API Proxy
 * Proxies prediction data to the Python AI backend /api/explain endpoint
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use POST.']);
    exit;
}

// Get input data
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON body']);
    exit;
}

require_once '../config/ai_backend.php';

// Build request payload
$payload = $input;

// Call AI Backend
$response = callAIBackend('/api/explain', $payload);

if ($response !== null) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'features' => $response['features'] ?? [],
        'base_value' => $response['base_value'] ?? 0.5,
        'prediction' => $response['prediction'] ?? 0,
        'source' => 'ai'
    ]);
} else {
    // Fallback response when AI backend is unavailable
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'features' => [
            ['name' => 'Nilai Rata-rata', 'contribution' => 0.15],
            ['name' => 'Peringkat Sekolah', 'contribution' => 0.10],
            ['name' => 'Akreditasi', 'contribution' => 0.08],
            ['name' => 'Rasio Peringkat', 'contribution' => -0.05],
            ['name' => 'Daya Tampung', 'contribution' => -0.03],
            ['name' => 'Kompetisi Prodi', 'contribution' => -0.07]
        ],
        'base_value' => 0.5,
        'prediction' => 0.68,
        'source' => 'fallback'
    ]);
}
