<?php
/**
 * LangkahKampus - SIDATA Program Search API
 * GET: Search sidata_prodi by nama_prodi keyword, returns top 10 with university info
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
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

require_once __DIR__ . '/../config/database.php';

// Get search query parameter
$query = isset($_GET['q']) ? trim($_GET['q']) : '';

if (strlen($query) < 2) {
    echo json_encode(['programs' => []]);
    exit;
}

$pdo = getDBConnection();
if (!$pdo) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

try {
    // Escape LIKE wildcard characters in user input to prevent wildcard injection
    $escapedQuery = str_replace(['%', '_'], ['\\%', '\\_'], $query);
    $searchTerm = '%' . $escapedQuery . '%';

    $stmt = $pdo->prepare(
        'SELECT sp.kode_prodi, sp.nama_prodi, sp.jenjang, 
                sp.daya_tampung_2023, sp.peminat_2022,
                su.nama_univ
         FROM sidata_prodi sp
         INNER JOIN sidata_universitas su ON sp.kode_univ = su.kode_univ
         WHERE sp.nama_prodi LIKE :query1 OR su.nama_univ LIKE :query2
         ORDER BY sp.nama_prodi ASC
         LIMIT 10'
    );

    $stmt->execute([
        ':query1' => $searchTerm,
        ':query2' => $searchTerm,
    ]);

    $programs = $stmt->fetchAll();

    echo json_encode([
        'programs' => $programs
    ]);

} catch (PDOException $e) {
    error_log('Search SIDATA error: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}
