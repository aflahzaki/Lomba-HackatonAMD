<?php
/**
 * LangkahKampus - Program Search API
 * GET: Search programs by name or university name (autocomplete)
 */

require_once __DIR__ . '/api_helpers.php';

send_cors_headers('GET');
enforce_method('GET');

$query = isset($_GET['q']) ? trim($_GET['q']) : '';

if (strlen($query) < 2) {
    echo json_encode(['programs' => []]);
    exit;
}

$pdo = require_db();

try {
    $searchTerm = '%' . escape_like($query) . '%';

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
