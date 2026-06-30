<?php
/**
 * LangkahKampus - Program Search API
 * GET: Search programs by name or university name (autocomplete)
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
        'SELECT p.id, p.name, u.name AS university, p.degree 
         FROM programs p 
         INNER JOIN universities u ON p.university_id = u.id 
         WHERE p.name LIKE :query1 OR u.name LIKE :query2 
         ORDER BY p.name ASC 
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
    error_log('Search programs error: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}
