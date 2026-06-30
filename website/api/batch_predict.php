<?php
/**
 * LangkahKampus - Batch Prediction API Proxy
 * Proxies array of student records to the Python AI backend /api/predict/batch endpoint
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

if (!$input || !isset($input['students']) || !is_array($input['students'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required field: students (array)']);
    exit;
}

require_once '../config/ai_backend.php';

// Build request payload
$payload = [
    'students' => $input['students']
];

// Call AI Backend
$response = callAIBackend('/api/predict/batch', $payload);

if ($response !== null) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'results' => $response['results'] ?? [],
        'total' => $response['total'] ?? count($input['students']),
        'source' => 'ai'
    ]);
} else {
    // Fallback: generate deterministic results for each student
    $results = [];
    foreach ($input['students'] as $student) {
        $nama = $student['nama'] ?? 'Unknown';
        $nilai = floatval($student['nilai_rata_rata'] ?? 75);
        $peringkat = intval($student['peringkat'] ?? 10);
        $total_siswa = intval($student['total_siswa'] ?? 100);
        $akreditasi = $student['akreditasi'] ?? 'B';
        $target_prodi = $student['target_prodi'] ?? '-';

        // Simple deterministic formula for fallback
        $ratio = 1 - ($peringkat / max($total_siswa, 1));
        $akr_bonus = $akreditasi === 'A' ? 0.1 : ($akreditasi === 'B' ? 0.05 : 0);
        $probability = min(99, max(5, round(($nilai / 100 * 0.5 + $ratio * 0.35 + $akr_bonus) * 100)));

        $results[] = [
            'nama' => $nama,
            'nilai_rata_rata' => $nilai,
            'peringkat' => $peringkat,
            'total_siswa' => $total_siswa,
            'akreditasi' => $akreditasi,
            'target_prodi' => $target_prodi,
            'probability' => $probability,
            'status' => $probability >= 70 ? 'Tinggi' : ($probability >= 40 ? 'Sedang' : 'Rendah')
        ];
    }

    http_response_code(200);
    echo json_encode([
        'success' => true,
        'results' => $results,
        'total' => count($results),
        'source' => 'fallback'
    ]);
}
