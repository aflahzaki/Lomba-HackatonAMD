<?php
/**
 * LangkahKampus - School Search API
 * GET: Search schools by name (autocomplete)
 * Returns up to 10 matching schools from the schools table
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
    echo json_encode(['schools' => []]);
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
        'SELECT id, npsn, name, province, city, accreditation, school_type 
         FROM schools 
         WHERE name LIKE :query 
         ORDER BY name ASC 
         LIMIT 10'
    );

    $stmt->execute([
        ':query' => $searchTerm,
    ]);

    $schools = $stmt->fetchAll();

    echo json_encode([
        'schools' => $schools
    ]);

} catch (PDOException $e) {
    error_log('Search schools error: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}
