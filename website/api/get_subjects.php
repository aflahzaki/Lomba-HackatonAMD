<?php
/**
 * LangkahKampus - Get Subjects API
 * GET: Returns subject list for a given jurusan
 * ?jurusan=IPA|IPS|Bahasa|<smk_jurusan_name>
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use GET.']);
    exit;
}

$jurusan = isset($_GET['jurusan']) ? trim($_GET['jurusan']) : '';

if (empty($jurusan)) {
    http_response_code(400);
    echo json_encode(['error' => 'Parameter jurusan is required']);
    exit;
}

// Hardcoded subjects for SMA/MA tracks
$smaSubjects = [
    'IPA' => [
        'Matematika',
        'Fisika',
        'Kimia',
        'Biologi',
        'Bahasa Indonesia',
        'Bahasa Inggris'
    ],
    'IPS' => [
        'Ekonomi',
        'Sosiologi',
        'Geografi',
        'Sejarah',
        'Bahasa Indonesia',
        'Bahasa Inggris'
    ],
    'Bahasa' => [
        'Bahasa Indonesia',
        'Bahasa Inggris',
        'Sastra Indonesia',
        'Sastra Inggris',
        'Antropologi',
        'Bahasa Asing Lain'
    ]
];

// Check if it's a standard SMA/MA track
if (isset($smaSubjects[$jurusan])) {
    echo json_encode([
        'success' => true,
        'jurusan' => $jurusan,
        'type' => 'SMA',
        'subjects' => $smaSubjects[$jurusan]
    ]);
    exit;
}

// Otherwise query smk_subjects table
require_once '../config/database.php';

$pdo = getDBConnection();
if (!$pdo) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

try {
    $stmt = $pdo->prepare('SELECT subject_name FROM smk_subjects WHERE jurusan = ? ORDER BY is_core DESC, id ASC');
    $stmt->execute([$jurusan]);
    $rows = $stmt->fetchAll(PDO::FETCH_COLUMN);

    if (empty($rows)) {
        // Return empty list with a message
        echo json_encode([
            'success' => true,
            'jurusan' => $jurusan,
            'type' => 'SMK',
            'subjects' => [],
            'message' => 'Tidak ada data mata pelajaran untuk jurusan ini. Silakan tambahkan secara manual.'
        ]);
    } else {
        echo json_encode([
            'success' => true,
            'jurusan' => $jurusan,
            'type' => 'SMK',
            'subjects' => $rows
        ]);
    }
} catch (PDOException $e) {
    error_log('get_subjects.php error: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Database query failed']);
}
