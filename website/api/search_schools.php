<?php
/**
 * LangkahKampus - School Search API
 * GET: Search schools by name (autocomplete)
 * Returns up to 10 matching schools from the schools table
 */

require_once __DIR__ . '/api_helpers.php';

send_cors_headers('GET');
enforce_method('GET');

$query = isset($_GET['q']) ? trim($_GET['q']) : '';

if (strlen($query) < 2) {
    echo json_encode(['schools' => []]);
    exit;
}

$pdo = require_db();

try {
    $searchTerm = '%' . escape_like($query) . '%';

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
