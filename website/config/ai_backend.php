<?php
/**
 * LangkahKampus - AI Backend Configuration
 * Configuration and helper function for communicating with the Python AI backend.
 */

// AI Backend URL - uses environment variable with fallback
define('AI_BACKEND_URL', getenv('AI_BACKEND_URL') ?: 'http://ai-backend:8000');
define('AI_BACKEND_TIMEOUT', 5); // seconds
define('AI_BACKEND_CONNECT_TIMEOUT', 3); // seconds

/**
 * Call the AI Backend via cURL
 *
 * @param string $endpoint The API endpoint path (e.g., '/api/predict')
 * @param array $data The request body data
 * @return array|null Returns decoded JSON response or null on failure
 */
function callAIBackend($endpoint, $data)
{
    $url = AI_BACKEND_URL . $endpoint;

    $ch = curl_init();

    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($data),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Accept: application/json',
        ],
        CURLOPT_TIMEOUT => AI_BACKEND_TIMEOUT,
        CURLOPT_CONNECTTIMEOUT => AI_BACKEND_CONNECT_TIMEOUT,
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        error_log("AI Backend error ({$endpoint}): cURL error - {$error}");
        return null;
    }

    if ($httpCode < 200 || $httpCode >= 300) {
        error_log("AI Backend error ({$endpoint}): HTTP {$httpCode} - {$response}");
        return null;
    }

    $decoded = json_decode($response, true);
    if ($decoded === null) {
        error_log("AI Backend error ({$endpoint}): Invalid JSON response");
        return null;
    }

    return $decoded;
}
