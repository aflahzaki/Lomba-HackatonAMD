<?php
/**
 * LangkahKampus - Prediction API (Deterministic Multi-Variable Formula)
 * POST: Receives student data + target program, returns prediction with breakdown
 *
 * 6-Variable Formula (weights sum to 1.0):
 *   1. Rasio Kompetisi (0.30)
 *   2. Tren Peminat (0.10)
 *   3. Nilai Rata-rata (0.25)
 *   4. Peringkat Siswa (0.20)
 *   5. Akreditasi Sekolah (0.10)
 *   6. Daya Tampung Absolut (0.05)
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use POST.']);
    exit;
}

// Get input data
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON input']);
    exit;
}

// Validate required fields
$required = ['scores', 'school_ranking', 'total_students', 'school_accreditation', 'target_program_id'];
foreach ($required as $field) {
    if (!isset($input[$field])) {
        http_response_code(400);
        echo json_encode(['error' => "Missing required field: $field"]);
        exit;
    }
}

require_once '../config/database.php';

$pdo = getDBConnection();
if (!$pdo) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Calculate prediction
$prediction = calculatePrediction($input, $pdo);

http_response_code(200);
echo json_encode($prediction);

/**
 * Deterministic prediction calculation with 6 variables
 */
function calculatePrediction($input, $pdo)
{
    $scores = $input['scores'];
    $ranking = (int)$input['school_ranking'];
    $totalStudents = (int)$input['total_students'];
    $accreditation = $input['school_accreditation'];
    $targetProgramId = $input['target_program_id'];
    $jurusan = isset($input['jurusan']) ? $input['jurusan'] : '';

    // Look up target program info from programs table
    $programName = '';
    $programUniversity = '';
    $programBlocksChoice2 = false;
    $programId = null;

    if (is_numeric($targetProgramId)) {
        $programId = (int)$targetProgramId;
        try {
            $stmt = $pdo->prepare('
                SELECT p.name, p.blocks_choice2, u.name as university_name
                FROM programs p
                JOIN universities u ON p.university_id = u.id
                WHERE p.id = ?
            ');
            $stmt->execute([$programId]);
            $program = $stmt->fetch();
            if ($program) {
                $programName = $program['name'];
                $programUniversity = $program['university_name'];
                $programBlocksChoice2 = (bool)$program['blocks_choice2'];
            }
        } catch (PDOException $e) {
            error_log('predict.php - program lookup error: ' . $e->getMessage());
        }
    }

    // === VARIABLE 1: RASIO KOMPETISI (weight 0.30) ===
    $sidataProdi = null;
    $rasioKompetisi = 15; // default ratio if not found
    $peminat2022 = 0;
    $dayaTampung2022 = 0;
    $dayaTampung2023 = 0;

    if (!empty($programName)) {
        try {
            // Try exact match first to prevent "KIMIA" from matching "TEKNIK KIMIA INDUSTRI"
            $stmt = $pdo->prepare('
                SELECT * FROM sidata_prodi
                WHERE nama_prodi = ?
                ORDER BY peminat_2022 DESC
                LIMIT 1
            ');
            $stmt->execute([$programName]);
            $sidataProdi = $stmt->fetch();

            // Fall back to LIKE search only if exact match returns nothing
            if (!$sidataProdi) {
                $escapedName = str_replace(['%', '_'], ['\\%', '\\_'], $programName);
                $stmt = $pdo->prepare('
                    SELECT * FROM sidata_prodi
                    WHERE nama_prodi LIKE ?
                    ORDER BY peminat_2022 DESC
                    LIMIT 1
                ');
                $stmt->execute(['%' . $escapedName . '%']);
                $sidataProdi = $stmt->fetch();
            }
        } catch (PDOException $e) {
            error_log('predict.php - sidata lookup error: ' . $e->getMessage());
        }
    }

    if ($sidataProdi) {
        $peminat2022 = (int)($sidataProdi['peminat_2022'] ?: 0);
        $dayaTampung2022 = (int)($sidataProdi['daya_tampung_2022'] ?: 1);
        $dayaTampung2023 = (int)($sidataProdi['daya_tampung_2023'] ?: 0);
        $rasioKompetisi = $dayaTampung2022 > 0 ? $peminat2022 / $dayaTampung2022 : 15;
    }

    // Score: max(0, 1 - (ratio/30)). Ratio of 30+ = 0 score, ratio 0 = 1.0
    $scoreRasio = max(0, 1 - ($rasioKompetisi / 30));

    // === VARIABLE 2: TREN PEMINAT (weight 0.10) ===
    $peminat2018 = 0;
    $growth = 0;

    if ($sidataProdi) {
        $peminat2018 = (int)($sidataProdi['peminat_2018'] ?: 0);
        $denominator = max($peminat2018, 1);
        $growth = ($peminat2022 - $peminat2018) / $denominator;
    }

    // Score: max(0, 1 - max(0, growth)). Increasing trend = lower score
    $scoreTren = max(0, 1 - max(0, $growth));

    // === VARIABLE 3: NILAI RATA-RATA (weight 0.25) ===
    $totalScore = 0;
    $scoreCount = 0;

    foreach ($scores as $subject => $semesters) {
        foreach ($semesters as $sem => $score) {
            $scoreVal = (float)$score;
            if ($scoreVal > 0) {
                $totalScore += $scoreVal;
                $scoreCount++;
            }
        }
    }

    $avgScore = $scoreCount > 0 ? $totalScore / $scoreCount : 75;
    // Score: (avg - 60) / 40, clamp 0-1
    $scoreNilai = max(0, min(1, ($avgScore - 60) / 40));

    // === VARIABLE 4: PERINGKAT SISWA (weight 0.20) ===
    // Score: 1 - (ranking / total_students), clamp 0-1
    $scorePeringkat = 0.5; // default
    if ($totalStudents > 0) {
        $scorePeringkat = max(0, min(1, 1 - ($ranking / $totalStudents)));
    }

    // === VARIABLE 5: AKREDITASI SEKOLAH (weight 0.10) ===
    $accreditationMap = ['A' => 1.0, 'B' => 0.7, 'C' => 0.4];
    $scoreAkreditasi = isset($accreditationMap[$accreditation]) ? $accreditationMap[$accreditation] : 0.2;

    // === VARIABLE 6: DAYA TAMPUNG ABSOLUT (weight 0.05) ===
    // Score: min(1, daya_tampung_2023 / 200)
    $scoreDayaTampung = min(1, $dayaTampung2023 / 200);

    // === FINAL CALCULATION ===
    $weights = [0.30, 0.10, 0.25, 0.20, 0.10, 0.05];
    $variableScores = [$scoreRasio, $scoreTren, $scoreNilai, $scorePeringkat, $scoreAkreditasi, $scoreDayaTampung];

    $probability = 0;
    for ($i = 0; $i < 6; $i++) {
        $probability += $variableScores[$i] * $weights[$i];
    }

    // Clamp to 0.05 - 0.95
    $probability = max(0.05, min(0.95, $probability));

    // Confidence interval (deterministic, based on distance from center)
    $ciWidth = 0.08 + (abs($probability - 0.5) * 0.1);
    $confidenceLower = max(0.01, $probability - $ciWidth);
    $confidenceUpper = min(0.99, $probability + $ciWidth);

    // Build variable breakdown
    $variables = [
        [
            'name' => 'Rasio Kompetisi',
            'weight' => 0.30,
            'raw_value' => round($rasioKompetisi, 2),
            'normalized_score' => round($scoreRasio, 4),
            'description' => $peminat2022 . ' peminat / ' . $dayaTampung2022 . ' daya tampung (rasio ' . round($rasioKompetisi, 1) . ':1)'
        ],
        [
            'name' => 'Tren Peminat',
            'weight' => 0.10,
            'raw_value' => round($growth, 4),
            'normalized_score' => round($scoreTren, 4),
            'description' => $growth > 0 ? 'Peminat naik ' . round($growth * 100, 1) . '% sejak 2018' : 'Peminat turun ' . round(abs($growth) * 100, 1) . '% sejak 2018'
        ],
        [
            'name' => 'Nilai Rata-rata',
            'weight' => 0.25,
            'raw_value' => round($avgScore, 2),
            'normalized_score' => round($scoreNilai, 4),
            'description' => 'Rata-rata nilai: ' . round($avgScore, 1) . ' dari 100'
        ],
        [
            'name' => 'Peringkat Siswa',
            'weight' => 0.20,
            'raw_value' => $ranking . '/' . $totalStudents,
            'normalized_score' => round($scorePeringkat, 4),
            'description' => 'Peringkat ' . $ranking . ' dari ' . $totalStudents . ' siswa'
        ],
        [
            'name' => 'Akreditasi Sekolah',
            'weight' => 0.10,
            'raw_value' => $accreditation,
            'normalized_score' => round($scoreAkreditasi, 4),
            'description' => 'Akreditasi ' . $accreditation
        ],
        [
            'name' => 'Daya Tampung Absolut',
            'weight' => 0.05,
            'raw_value' => $dayaTampung2023,
            'normalized_score' => round($scoreDayaTampung, 4),
            'description' => 'Daya tampung 2023: ' . $dayaTampung2023 . ' kursi'
        ]
    ];

    // === ADMISSION HISTORY ===
    $admissionHistory = [];
    if ($programId) {
        try {
            $stmt = $pdo->prepare('
                SELECT year, applicants, accepted, min_score, avg_score
                FROM admission_history
                WHERE program_id = ?
                ORDER BY year DESC
                LIMIT 5
            ');
            $stmt->execute([$programId]);
            $admissionHistory = $stmt->fetchAll();
        } catch (PDOException $e) {
            error_log('predict.php - admission history error: ' . $e->getMessage());
        }
    }

    // === RECOMMENDATIONS (top 3 similar programs with lower ratios) ===
    $recommendations = [];
    if ($sidataProdi && !empty($programName)) {
        try {
            // Find similar programs by keyword in name with lower competition
            $keywords = explode(' ', $programName);
            $mainKeyword = '';
            foreach ($keywords as $kw) {
                if (strlen($kw) > 3) {
                    $mainKeyword = $kw;
                    break;
                }
            }

            if (!empty($mainKeyword)) {
                $escapedKeyword = str_replace(['%', '_'], ['\\%', '\\_'], $mainKeyword);
                $stmt = $pdo->prepare('
                    SELECT sp.nama_prodi, sp.peminat_2022, sp.daya_tampung_2022, sp.daya_tampung_2023,
                           su.nama_univ
                    FROM sidata_prodi sp
                    JOIN sidata_universitas su ON sp.kode_univ = su.kode_univ
                    WHERE sp.nama_prodi LIKE ?
                      AND sp.daya_tampung_2022 > 0
                      AND sp.kode_prodi != ?
                    ORDER BY (sp.peminat_2022 / sp.daya_tampung_2022) ASC
                    LIMIT 3
                ');
                $stmt->execute([
                    '%' . $escapedKeyword . '%',
                    $sidataProdi['kode_prodi']
                ]);
                $altPrograms = $stmt->fetchAll();

                foreach ($altPrograms as $alt) {
                    $altRatio = $alt['daya_tampung_2022'] > 0
                        ? round($alt['peminat_2022'] / $alt['daya_tampung_2022'], 1)
                        : 0;
                    $recommendations[] = [
                        'name' => $alt['nama_prodi'],
                        'university' => $alt['nama_univ'],
                        'ratio' => $altRatio,
                        'daya_tampung' => (int)$alt['daya_tampung_2023'],
                        'comparison' => 'Rasio ' . $altRatio . ':1 vs ' . round($rasioKompetisi, 1) . ':1'
                    ];
                }
            }
        } catch (PDOException $e) {
            error_log('predict.php - recommendations error: ' . $e->getMessage());
        }
    }

    // === PEER COUNT (anti-bentrok) ===
    $peerCount = 0;
    if ($programId) {
        try {
            $stmt = $pdo->prepare('
                SELECT COUNT(*) as cnt FROM predictions
                WHERE program_id = ?
                  AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ');
            $stmt->execute([$programId]);
            $row = $stmt->fetch();
            $peerCount = (int)($row['cnt'] ?? 0);
        } catch (PDOException $e) {
            // Non-critical, continue
        }
    }

    return [
        'success' => true,
        'probability' => round($probability * 100, 1),
        'confidence_lower' => round($confidenceLower, 4),
        'confidence_upper' => round($confidenceUpper, 4),
        'variables' => $variables,
        'admission_history' => $admissionHistory,
        'recommendations' => $recommendations,
        'blocks_choice2' => $programBlocksChoice2,
        'peer_count' => $peerCount,
        'input_summary' => [
            'avg_score' => round($avgScore, 2),
            'ranking' => $ranking . '/' . $totalStudents,
            'school_accreditation' => $accreditation,
            'target_program' => $programName,
            'target_university' => $programUniversity,
            'jurusan' => $jurusan
        ],
        'timestamp' => date('c')
    ];
}
