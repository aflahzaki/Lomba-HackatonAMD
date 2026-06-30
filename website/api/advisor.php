<?php
/**
 * LangkahKampus - AI Advisor API Proxy
 * Proxies chat messages to the Python AI backend /api/advisor endpoint
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

if (!$input || !isset($input['message'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required field: message']);
    exit;
}

require_once '../config/ai_backend.php';

// Build request payload for the Python backend
$payload = [
    'message' => $input['message'],
];

// Include prediction context if available
if (isset($input['context'])) {
    $payload['context'] = $input['context'];
}

// Include conversation history if available
if (isset($input['history']) && is_array($input['history'])) {
    $payload['history'] = $input['history'];
}

// Call AI Backend
$response = callAIBackend('/api/advisor', $payload);

if ($response !== null) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'reply' => $response['reply'] ?? 'Maaf, saya tidak dapat memberikan jawaban saat ini.',
        'suggestions' => $response['suggestions'] ?? [],
        'source' => 'ai'
    ]);
} else {
    // Fallback response when AI backend is unavailable
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'reply' => 'Maaf, layanan AI Advisor sedang tidak tersedia. Silakan coba beberapa saat lagi. ' .
                   'Sementara itu, Anda dapat menggunakan fitur Prediksi untuk menganalisis peluang SNBP Anda.',
        'suggestions' => [
            'Coba fitur Prediksi SNBP',
            'Lihat Rekomendasi Program Studi',
            'Cek Peta Universitas'
        ],
        'source' => 'fallback'
    ]);
}
