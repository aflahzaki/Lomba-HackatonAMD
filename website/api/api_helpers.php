<?php
/**
 * LangkahKampus - Shared API Helpers
 *
 * Consolidates boilerplate duplicated across JSON API endpoints:
 *   - CORS headers
 *   - HTTP method enforcement
 *   - JSON input parsing
 *   - Database connection with error response
 *   - LIKE wildcard escaping
 */

/**
 * Send standard CORS headers for a JSON API endpoint.
 *
 * @param string $methods  Comma-separated allowed methods (e.g. "GET" or "POST, OPTIONS")
 */
function send_cors_headers(string $methods = 'GET'): void
{
    header('Content-Type: application/json');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: ' . $methods);
    header('Access-Control-Allow-Headers: Content-Type');
}

/**
 * Enforce a single HTTP method.  Handles OPTIONS preflight automatically.
 * Terminates with 405 if the method does not match.
 *
 * @param string $allowed  The allowed method (e.g. "GET" or "POST")
 */
function enforce_method(string $allowed): void
{
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit;
    }

    if ($_SERVER['REQUEST_METHOD'] !== $allowed) {
        http_response_code(405);
        echo json_encode(['error' => "Method not allowed. Use $allowed."]);
        exit;
    }
}

/**
 * Read and decode JSON from the request body.
 * Terminates with 400 if the body is not valid JSON.
 *
 * @return array  The decoded associative array.
 */
function read_json_body(): array
{
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON input']);
        exit;
    }
    return $input;
}

/**
 * Obtain a PDO connection or terminate with a 500 JSON error.
 *
 * @return PDO
 */
function require_db(): PDO
{
    require_once __DIR__ . '/../config/database.php';
    $pdo = getDBConnection();
    if (!$pdo) {
        http_response_code(500);
        echo json_encode(['error' => 'Database connection failed']);
        exit;
    }
    return $pdo;
}

/**
 * Escape LIKE wildcard characters in user input to prevent wildcard injection.
 *
 * @param string $value  Raw user input
 * @return string  Escaped value safe for use in LIKE clauses
 */
function escape_like(string $value): string
{
    return str_replace(['%', '_'], ['\\%', '\\_'], $value);
}
