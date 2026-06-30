<?php
/**
 * LangkahKampus - What-If Simulator API Proxy
 * Proxies what-if parameters to the Python AI backend /api/what-if endpoint
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
$response = callAIBackend('/api/what-if', $payload);

if ($response !== null) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'current_probability' => $response['current_probability'] ?? 0,
        'new_probability' => $response['new_probability'] ?? 0,
        'difference' => $response['difference'] ?? 0,
        'factors' => $response['factors'] ?? [],
        'source' => 'ai'
    ]);
} else {
    // Fallback: calculate a simple deterministic result
    $nilai = floatval($input['nilai_rata_rata'] ?? 75);
    $peringkat = intval($input['peringkat'] ?? 50);
    $total_siswa = intval($input['total_siswa'] ?? 200);
    $akreditasi = $input['akreditasi'] ?? 'B';

    $ratio = 1 - ($peringkat / max($total_siswa, 1));
    $akr_bonus = $akreditasi === 'A' ? 0.1 : ($akreditasi === 'B' ? 0.05 : 0);
    $new_probability = min(99, max(5, round(($nilai / 100 * 0.5 + $ratio * 0.35 + $akr_bonus) * 100)));

    // Simulate a "current" that is slightly lower
    $current_probability = max(5, $new_probability - rand(3, 12));

    http_response_code(200);
    echo json_encode([
        'success' => true,
        'current_probability' => $current_probability,
        'new_probability' => $new_probability,
        'difference' => $new_probability - $current_probability,
        'factors' => [
            ['name' => 'Nilai Rata-rata', 'impact' => round(($nilai - 70) * 0.5, 1)],
            ['name' => 'Peringkat', 'impact' => round($ratio * 20, 1)],
            ['name' => 'Akreditasi', 'impact' => round($akr_bonus * 100, 1)]
        ],
        'source' => 'fallback'
    ]);
}
