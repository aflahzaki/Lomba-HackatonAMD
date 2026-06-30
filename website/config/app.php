<?php
/**
 * LangkahKampus - Application Configuration
 */

// Application Info
define('APP_NAME', 'LangkahKampus');
define('APP_VERSION', '1.0.0');
define('APP_TAGLINE', 'Prediksi Peluang SNBP Anda dengan AI');
define('APP_DESCRIPTION', 'Platform prediksi penerimaan SNBP berbasis Machine Learning untuk siswa SMA/SMK/MA di Indonesia');
define('APP_URL', 'http://localhost');

// Brand Colors
define('COLOR_PRIMARY', '#2E4057');
define('COLOR_ACCENT_BLUE', '#1A73E8');
define('COLOR_ACCENT_RED', '#C0392B');
define('COLOR_ACCENT_GREEN', '#27AE60');
define('COLOR_LIGHT', '#F8F9FA');
define('COLOR_DARK', '#1A1A2E');

// Pricing (in IDR)
define('PRICE_BASIC_PREDICTION', 15000);
define('PRICE_DEEP_RECOMMENDATION', 25000);

// Freemium Model
define('FREE_PREDICTIONS_LIMIT', 3);
define('REFERRAL_CLICKS_REQUIRED', 5);
define('REFERRAL_UNLOCK_PREDICTIONS', 3);

// Feature Flags
define('FEATURE_MAP_ENABLED', true);
define('FEATURE_PAYMENT_ENABLED', true);

// Session Configuration
define('SESSION_LIFETIME', 3600); // 1 hour
define('SESSION_NAME', 'langkahkampus_session');

// Pagination
define('ITEMS_PER_PAGE', 20);
