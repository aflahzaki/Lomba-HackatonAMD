<?php
/**
 * LangkahKampus - CORS Configuration
 * Restricts cross-origin requests to the configured application origin.
 */

function set_cors_headers()
{
    $allowed_origin = rtrim(defined('APP_URL') ? APP_URL : 'http://localhost', '/');

    $origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';

    if ($origin === $allowed_origin) {
        header('Access-Control-Allow-Origin: ' . $allowed_origin);
    } else {
        header('Access-Control-Allow-Origin: ' . $allowed_origin);
    }

    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
    header('Vary: Origin');
}
