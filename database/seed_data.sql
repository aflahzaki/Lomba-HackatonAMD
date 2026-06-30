-- ============================================================
-- LangkahKampus - Seed Data (Demo)
-- Data realistis untuk demonstrasi dan pengembangan
-- ============================================================
-- DEFAULT PASSWORD: 'password123'
-- BCrypt hash: $2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.
-- ============================================================

USE langkahkampus;

-- ============================================================
-- Schools (5 SMA Negeri dari kota-kota besar Indonesia)
-- ============================================================
INSERT INTO schools (id, npsn, name, address, province, city, accreditation, school_type, latitude, longitude, total_students) VALUES
(1, '20100001', 'SMA Negeri 3 Jakarta', 'Jl. Setiabudi No.29, Kuningan, Setia Budi', 'DKI Jakarta', 'Jakarta Selatan', 'A', 'SMA', -6.21462000, 106.83780000, 1200),
(2, '20200002', 'SMA Negeri 3 Bandung', 'Jl. Belitung No.8, Merdeka', 'Jawa Barat', 'Bandung', 'A', 'SMA', -6.90389000, 107.61861000, 1100),
(3, '20300003', 'SMA Negeri 5 Surabaya', 'Jl. Kusuma Bangsa No.21, Ketabang', 'Jawa Timur', 'Surabaya', 'A', 'SMA', -7.27472000, 112.74444000, 1050),
(4, '20400004', 'SMA Negeri 1 Yogyakarta', 'Jl. HOS Cokroaminoto No.10, Pakuncen', 'DI Yogyakarta', 'Yogyakarta', 'A', 'SMA', -7.78278000, 110.36139000, 900),
(5, '20500005', 'SMA Negeri 1 Semarang', 'Jl. Taman Menteri Supeno No.1, Mugassari', 'Jawa Tengah', 'Semarang', 'A', 'SMA', -6.98306000, 110.41083000, 980);

-- ============================================================
-- Universities (10 PTN terkemuka di Indonesia)
-- ============================================================
INSERT INTO universities (id, name, code, type, province, city, accreditation, website, latitude, longitude) VALUES
(1, 'Universitas Indonesia', 'UI', 'PTN', 'DKI Jakarta', 'Depok', 'Unggul', 'https://www.ui.ac.id', -6.36250000, 106.82917000),
(2, 'Institut Teknologi Bandung', 'ITB', 'PTN', 'Jawa Barat', 'Bandung', 'Unggul', 'https://www.itb.ac.id', -6.89139000, 107.61083000),
(3, 'Universitas Gadjah Mada', 'UGM', 'PTN', 'DI Yogyakarta', 'Yogyakarta', 'Unggul', 'https://www.ugm.ac.id', -7.77028000, 110.37778000),
(4, 'Institut Teknologi Sepuluh Nopember', 'ITS', 'PTN', 'Jawa Timur', 'Surabaya', 'Unggul', 'https://www.its.ac.id', -7.28194000, 112.79528000),
(5, 'Universitas Diponegoro', 'UNDIP', 'PTN', 'Jawa Tengah', 'Semarang', 'Unggul', 'https://www.undip.ac.id', -7.04917000, 110.43833000),
(6, 'Universitas Airlangga', 'UNAIR', 'PTN', 'Jawa Timur', 'Surabaya', 'Unggul', 'https://www.unair.ac.id', -7.27000000, 112.76333000),
(7, 'Institut Pertanian Bogor', 'IPB', 'PTN', 'Jawa Barat', 'Bogor', 'Unggul', 'https://www.ipb.ac.id', -6.59472000, 106.80611000),
(8, 'Universitas Padjadjaran', 'UNPAD', 'PTN', 'Jawa Barat', 'Sumedang', 'Unggul', 'https://www.unpad.ac.id', -6.92583000, 107.77389000),
(9, 'Universitas Brawijaya', 'UB', 'PTN', 'Jawa Timur', 'Malang', 'Unggul', 'https://www.ub.ac.id', -7.95278000, 112.61472000),
(10, 'Universitas Hasanuddin', 'UNHAS', 'PTN', 'Sulawesi Selatan', 'Makassar', 'Unggul', 'https://www.unhas.ac.id', -5.13194000, 119.48889000);

-- ============================================================
-- Programs (30 program studi populer di berbagai PTN)
-- ============================================================
INSERT INTO programs (id, university_id, name, code, faculty, degree, accreditation, capacity, competition_ratio, min_score_avg, blocks_choice2) VALUES
-- UI (6 prodi)
(1, 1, 'Teknik Informatika', 'TI-UI', 'Fakultas Ilmu Komputer', 'S1', 'Unggul', 80, 15.50, 85.00, FALSE),
(2, 1, 'Kedokteran', 'FK-UI', 'Fakultas Kedokteran', 'S1', 'Unggul', 150, 25.00, 92.00, TRUE),
(3, 1, 'Hukum', 'FH-UI', 'Fakultas Hukum', 'S1', 'Unggul', 200, 12.30, 82.00, FALSE),
(4, 1, 'Ekonomi Pembangunan', 'EP-UI', 'Fakultas Ekonomi dan Bisnis', 'S1', 'Unggul', 120, 10.80, 80.00, FALSE),
(5, 1, 'Psikologi', 'PSI-UI', 'Fakultas Psikologi', 'S1', 'Unggul', 100, 18.20, 84.00, FALSE),
(6, 1, 'Ilmu Komunikasi', 'IKOM-UI', 'Fakultas Ilmu Sosial dan Ilmu Politik', 'S1', 'Unggul', 80, 20.50, 83.00, FALSE),

-- ITB (5 prodi)
(7, 2, 'Teknik Informatika', 'TI-ITB', 'Sekolah Teknik Elektro dan Informatika', 'S1', 'Unggul', 90, 22.00, 88.00, TRUE),
(8, 2, 'Teknik Elektro', 'TE-ITB', 'Sekolah Teknik Elektro dan Informatika', 'S1', 'Unggul', 100, 14.00, 85.00, FALSE),
(9, 2, 'Arsitektur', 'ARS-ITB', 'Sekolah Arsitektur, Perencanaan dan Pengembangan Kebijakan', 'S1', 'Unggul', 60, 16.50, 84.00, FALSE),
(10, 2, 'Teknik Sipil', 'TS-ITB', 'Fakultas Teknik Sipil dan Lingkungan', 'S1', 'Unggul', 120, 11.00, 83.00, FALSE),
(11, 2, 'Matematika', 'MAT-ITB', 'Fakultas Matematika dan Ilmu Pengetahuan Alam', 'S1', 'Unggul', 80, 8.50, 82.00, FALSE),

-- UGM (5 prodi)
(12, 3, 'Kedokteran', 'FK-UGM', 'Fakultas Kedokteran, Kesehatan Masyarakat, dan Keperawatan', 'S1', 'Unggul', 160, 23.00, 90.00, TRUE),
(13, 3, 'Teknik Informatika', 'TI-UGM', 'Departemen Teknik Elektro dan Teknologi Informasi', 'S1', 'Unggul', 75, 18.00, 86.00, FALSE),
(14, 3, 'Manajemen', 'MAN-UGM', 'Fakultas Ekonomika dan Bisnis', 'S1', 'Unggul', 150, 14.50, 83.00, FALSE),
(15, 3, 'Farmasi', 'FAR-UGM', 'Fakultas Farmasi', 'S1', 'Unggul', 100, 12.00, 84.00, FALSE),
(16, 3, 'Ilmu Hukum', 'FH-UGM', 'Fakultas Hukum', 'S1', 'Unggul', 180, 11.50, 81.00, FALSE),

-- ITS (4 prodi)
(17, 4, 'Teknik Informatika', 'TI-ITS', 'Fakultas Teknologi Elektro dan Informatika Cerdas', 'S1', 'Unggul', 100, 16.00, 84.00, FALSE),
(18, 4, 'Teknik Perkapalan', 'TK-ITS', 'Fakultas Teknologi Kelautan', 'S1', 'Unggul', 80, 9.00, 80.00, FALSE),
(19, 4, 'Desain Produk Industri', 'DPI-ITS', 'Fakultas Desain Kreatif dan Bisnis Digital', 'S1', 'A', 60, 13.00, 79.00, FALSE),
(20, 4, 'Teknik Mesin', 'TM-ITS', 'Fakultas Teknologi Industri dan Rekayasa Sistem', 'S1', 'Unggul', 120, 10.50, 82.00, FALSE),

-- UNDIP (3 prodi)
(21, 5, 'Kedokteran', 'FK-UNDIP', 'Fakultas Kedokteran', 'S1', 'Unggul', 140, 20.00, 88.00, TRUE),
(22, 5, 'Teknik Informatika', 'TI-UNDIP', 'Fakultas Teknik', 'S1', 'A', 90, 12.00, 82.00, FALSE),
(23, 5, 'Akuntansi', 'AKT-UNDIP', 'Fakultas Ekonomika dan Bisnis', 'S1', 'Unggul', 130, 11.00, 80.00, FALSE),

-- UNAIR (2 prodi)
(24, 6, 'Kedokteran', 'FK-UNAIR', 'Fakultas Kedokteran', 'S1', 'Unggul', 150, 22.00, 89.00, TRUE),
(25, 6, 'Psikologi', 'PSI-UNAIR', 'Fakultas Psikologi', 'S1', 'A', 80, 15.00, 82.00, FALSE),

-- IPB (2 prodi)
(26, 7, 'Teknologi Pangan', 'TP-IPB', 'Fakultas Teknologi Pertanian', 'S1', 'Unggul', 100, 10.00, 81.00, FALSE),
(27, 7, 'Ilmu Komputer', 'IK-IPB', 'Fakultas Matematika dan Ilmu Pengetahuan Alam', 'S1', 'A', 70, 13.50, 83.00, FALSE),

-- UNPAD (2 prodi)
(28, 8, 'Kedokteran', 'FK-UNPAD', 'Fakultas Kedokteran', 'S1', 'Unggul', 160, 21.00, 89.00, TRUE),
(29, 8, 'Ilmu Komunikasi', 'IKOM-UNPAD', 'Fakultas Ilmu Komunikasi', 'S1', 'Unggul', 100, 17.00, 82.00, FALSE),

-- UB (1 prodi)
(30, 9, 'Teknik Informatika', 'TI-UB', 'Fakultas Ilmu Komputer', 'S1', 'Unggul', 110, 14.00, 82.00, FALSE);

-- ============================================================
-- Users (8 pengguna demo dengan berbagai role)
-- Password: password123 (BCrypt hash)
-- ============================================================
INSERT INTO users (id, email, phone, password_hash, full_name, role, is_premium, subscription_expires_at, last_login, is_active) VALUES
(1, 'ahmad.faiz@student.sman3jkt.sch.id', '081234567890', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Ahmad Faiz Pratama', 'student', TRUE, '2025-12-31 23:59:59', '2024-11-15 08:30:00', TRUE),
(2, 'siti.nurhaliza@student.sman3bdg.sch.id', '081345678901', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Siti Nurhaliza Putri', 'student', FALSE, NULL, '2024-11-14 14:20:00', TRUE),
(3, 'bu.ratna@sman3jkt.sch.id', '081456789012', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Dr. Ratna Sari Dewi', 'guru', FALSE, NULL, '2024-11-15 07:45:00', TRUE),
(4, 'pak.bambang@sman3bdg.sch.id', '081567890123', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Bambang Supriyanto, M.Pd.', 'guru', FALSE, NULL, '2024-11-13 16:00:00', TRUE),
(7, 'superadmin@langkahkampus.id', '081890123456', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Muhammad Rizki Fauzan', 'platform_admin', TRUE, NULL, '2024-11-15 09:00:00', TRUE),
(8, 'dewi.anggraeni@student.sman5sby.sch.id', '081901234567', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Dewi Anggraeni', 'student', TRUE, '2025-06-30 23:59:59', '2024-11-14 19:15:00', TRUE),
(9, 'budi.santoso@student.sman1yk.sch.id', '082012345678', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Budi Santoso', 'student', FALSE, NULL, '2024-11-12 11:45:00', TRUE),
(10, 'rina.wulandari@student.sman1smg.sch.id', '082123456789', '$2y$12$Jw6aPnGiY.AF7p8SealmaufrC7dQXpV.wwTeNh.bIVyMlrgZGS.2.', 'Rina Wulandari', 'student', FALSE, NULL, '2024-11-10 15:30:00', TRUE);

-- ============================================================
-- Student Profiles (5 siswa dengan profil lengkap)
-- ============================================================
INSERT INTO student_profiles (id, user_id, school_id, nis, grade_level, major_track, ranking_in_school, total_students, preference_vector, cognitive_profile) VALUES
(1, 1, 1, '12001', 12, 'IPA', 5, 400, '{"technical": 0.85, "medical": 0.60, "social": 0.40, "business": 0.55, "arts": 0.30}', '{"analytical": 88, "verbal": 75, "numerical": 90, "spatial": 72}'),
(2, 2, 2, '12045', 12, 'IPA', 12, 380, '{"technical": 0.50, "medical": 0.90, "social": 0.70, "business": 0.45, "arts": 0.35}', '{"analytical": 82, "verbal": 85, "numerical": 78, "spatial": 65}'),
(3, 8, 3, '12102', 12, 'IPA', 3, 350, '{"technical": 0.75, "medical": 0.55, "social": 0.60, "business": 0.80, "arts": 0.45}', '{"analytical": 85, "verbal": 80, "numerical": 87, "spatial": 70}'),
(4, 9, 4, '12078', 12, 'IPS', 8, 300, '{"technical": 0.30, "medical": 0.20, "social": 0.85, "business": 0.75, "arts": 0.60}', '{"analytical": 72, "verbal": 88, "numerical": 70, "spatial": 78}'),
(5, 10, 5, '12033', 12, 'IPA', 15, 330, '{"technical": 0.65, "medical": 0.70, "social": 0.55, "business": 0.50, "arts": 0.40}', '{"analytical": 78, "verbal": 76, "numerical": 80, "spatial": 68}');

-- ============================================================
-- Academic Records (5 siswa x 5 semester x 6 mata pelajaran)
-- ============================================================

-- Student 1: Ahmad Faiz (IPA - excellent in math/physics)
INSERT INTO academic_records (student_id, semester, subject, score) VALUES
(1, 1, 'Matematika', 90.00), (1, 1, 'Fisika', 88.00), (1, 1, 'Kimia', 85.00),
(1, 1, 'Biologi', 82.00), (1, 1, 'Bahasa Indonesia', 80.00), (1, 1, 'Bahasa Inggris', 85.00),
(1, 2, 'Matematika', 92.00), (1, 2, 'Fisika', 90.00), (1, 2, 'Kimia', 86.00),
(1, 2, 'Biologi', 83.00), (1, 2, 'Bahasa Indonesia', 82.00), (1, 2, 'Bahasa Inggris', 87.00),
(1, 3, 'Matematika', 93.00), (1, 3, 'Fisika', 91.00), (1, 3, 'Kimia', 87.00),
(1, 3, 'Biologi', 84.00), (1, 3, 'Bahasa Indonesia', 83.00), (1, 3, 'Bahasa Inggris', 88.00),
(1, 4, 'Matematika', 94.00), (1, 4, 'Fisika', 92.00), (1, 4, 'Kimia', 88.00),
(1, 4, 'Biologi', 85.00), (1, 4, 'Bahasa Indonesia', 84.00), (1, 4, 'Bahasa Inggris', 89.00),
(1, 5, 'Matematika', 95.00), (1, 5, 'Fisika', 93.00), (1, 5, 'Kimia', 89.00),
(1, 5, 'Biologi', 86.00), (1, 5, 'Bahasa Indonesia', 85.00), (1, 5, 'Bahasa Inggris', 90.00);

-- Student 2: Siti Nurhaliza (IPA - strong in biology/chemistry)
INSERT INTO academic_records (student_id, semester, subject, score) VALUES
(2, 1, 'Matematika', 82.00), (2, 1, 'Fisika', 80.00), (2, 1, 'Kimia', 88.00),
(2, 1, 'Biologi', 90.00), (2, 1, 'Bahasa Indonesia', 85.00), (2, 1, 'Bahasa Inggris', 83.00),
(2, 2, 'Matematika', 83.00), (2, 2, 'Fisika', 81.00), (2, 2, 'Kimia', 89.00),
(2, 2, 'Biologi', 91.00), (2, 2, 'Bahasa Indonesia', 86.00), (2, 2, 'Bahasa Inggris', 84.00),
(2, 3, 'Matematika', 84.00), (2, 3, 'Fisika', 82.00), (2, 3, 'Kimia', 90.00),
(2, 3, 'Biologi', 92.00), (2, 3, 'Bahasa Indonesia', 87.00), (2, 3, 'Bahasa Inggris', 85.00),
(2, 4, 'Matematika', 85.00), (2, 4, 'Fisika', 83.00), (2, 4, 'Kimia', 91.00),
(2, 4, 'Biologi', 93.00), (2, 4, 'Bahasa Indonesia', 87.00), (2, 4, 'Bahasa Inggris', 86.00),
(2, 5, 'Matematika', 86.00), (2, 5, 'Fisika', 84.00), (2, 5, 'Kimia', 92.00),
(2, 5, 'Biologi', 94.00), (2, 5, 'Bahasa Indonesia', 88.00), (2, 5, 'Bahasa Inggris', 87.00);

-- Student 3: Dewi Anggraeni (IPA - well-rounded)
INSERT INTO academic_records (student_id, semester, subject, score) VALUES
(3, 1, 'Matematika', 87.00), (3, 1, 'Fisika', 85.00), (3, 1, 'Kimia', 84.00),
(3, 1, 'Biologi', 83.00), (3, 1, 'Bahasa Indonesia', 86.00), (3, 1, 'Bahasa Inggris', 88.00),
(3, 2, 'Matematika', 88.00), (3, 2, 'Fisika', 86.00), (3, 2, 'Kimia', 85.00),
(3, 2, 'Biologi', 84.00), (3, 2, 'Bahasa Indonesia', 87.00), (3, 2, 'Bahasa Inggris', 89.00),
(3, 3, 'Matematika', 89.00), (3, 3, 'Fisika', 87.00), (3, 3, 'Kimia', 86.00),
(3, 3, 'Biologi', 85.00), (3, 3, 'Bahasa Indonesia', 88.00), (3, 3, 'Bahasa Inggris', 90.00),
(3, 4, 'Matematika', 90.00), (3, 4, 'Fisika', 88.00), (3, 4, 'Kimia', 87.00),
(3, 4, 'Biologi', 86.00), (3, 4, 'Bahasa Indonesia', 89.00), (3, 4, 'Bahasa Inggris', 91.00),
(3, 5, 'Matematika', 91.00), (3, 5, 'Fisika', 89.00), (3, 5, 'Kimia', 88.00),
(3, 5, 'Biologi', 87.00), (3, 5, 'Bahasa Indonesia', 90.00), (3, 5, 'Bahasa Inggris', 92.00);

-- Student 4: Budi Santoso (IPS - strong in social sciences)
INSERT INTO academic_records (student_id, semester, subject, score) VALUES
(4, 1, 'Ekonomi', 88.00), (4, 1, 'Sosiologi', 85.00), (4, 1, 'Geografi', 83.00),
(4, 1, 'Sejarah', 86.00), (4, 1, 'Bahasa Indonesia', 87.00), (4, 1, 'Bahasa Inggris', 80.00),
(4, 2, 'Ekonomi', 89.00), (4, 2, 'Sosiologi', 86.00), (4, 2, 'Geografi', 84.00),
(4, 2, 'Sejarah', 87.00), (4, 2, 'Bahasa Indonesia', 88.00), (4, 2, 'Bahasa Inggris', 81.00),
(4, 3, 'Ekonomi', 90.00), (4, 3, 'Sosiologi', 87.00), (4, 3, 'Geografi', 85.00),
(4, 3, 'Sejarah', 88.00), (4, 3, 'Bahasa Indonesia', 89.00), (4, 3, 'Bahasa Inggris', 82.00),
(4, 4, 'Ekonomi', 91.00), (4, 4, 'Sosiologi', 88.00), (4, 4, 'Geografi', 86.00),
(4, 4, 'Sejarah', 89.00), (4, 4, 'Bahasa Indonesia', 90.00), (4, 4, 'Bahasa Inggris', 83.00),
(4, 5, 'Ekonomi', 92.00), (4, 5, 'Sosiologi', 89.00), (4, 5, 'Geografi', 87.00),
(4, 5, 'Sejarah', 90.00), (4, 5, 'Bahasa Indonesia', 91.00), (4, 5, 'Bahasa Inggris', 84.00);

-- Student 5: Rina Wulandari (IPA - balanced, leaning towards medical)
INSERT INTO academic_records (student_id, semester, subject, score) VALUES
(5, 1, 'Matematika', 80.00), (5, 1, 'Fisika', 78.00), (5, 1, 'Kimia', 83.00),
(5, 1, 'Biologi', 85.00), (5, 1, 'Bahasa Indonesia', 82.00), (5, 1, 'Bahasa Inggris', 79.00),
(5, 2, 'Matematika', 81.00), (5, 2, 'Fisika', 79.00), (5, 2, 'Kimia', 84.00),
(5, 2, 'Biologi', 86.00), (5, 2, 'Bahasa Indonesia', 83.00), (5, 2, 'Bahasa Inggris', 80.00),
(5, 3, 'Matematika', 82.00), (5, 3, 'Fisika', 80.00), (5, 3, 'Kimia', 85.00),
(5, 3, 'Biologi', 87.00), (5, 3, 'Bahasa Indonesia', 84.00), (5, 3, 'Bahasa Inggris', 81.00),
(5, 4, 'Matematika', 83.00), (5, 4, 'Fisika', 81.00), (5, 4, 'Kimia', 86.00),
(5, 4, 'Biologi', 88.00), (5, 4, 'Bahasa Indonesia', 85.00), (5, 4, 'Bahasa Inggris', 82.00),
(5, 5, 'Matematika', 84.00), (5, 5, 'Fisika', 82.00), (5, 5, 'Kimia', 87.00),
(5, 5, 'Biologi', 89.00), (5, 5, 'Bahasa Indonesia', 86.00), (5, 5, 'Bahasa Inggris', 83.00);

-- ============================================================
-- Predictions (sample AI predictions for students)
-- ============================================================
INSERT INTO predictions (id, student_id, program_id, probability_score, confidence_lower, confidence_upper, model_version, scenario_type, feature_importances) VALUES
-- Ahmad Faiz predictions (strong in STEM)
(1, 1, 1, 0.8750, 0.8200, 0.9300, 'v2.1-snbp', 'base', '{"math_avg": 0.35, "physics_avg": 0.25, "ranking_percentile": 0.20, "school_accreditation": 0.10, "competition_ratio": 0.10}'),
(2, 1, 7, 0.7200, 0.6500, 0.7900, 'v2.1-snbp', 'base', '{"math_avg": 0.30, "physics_avg": 0.28, "ranking_percentile": 0.18, "school_accreditation": 0.12, "competition_ratio": 0.12}'),
(3, 1, 13, 0.8100, 0.7500, 0.8700, 'v2.1-snbp', 'base', '{"math_avg": 0.32, "physics_avg": 0.22, "ranking_percentile": 0.22, "school_accreditation": 0.12, "competition_ratio": 0.12}'),

-- Siti Nurhaliza predictions (strong in biology/medical)
(4, 2, 2, 0.5500, 0.4800, 0.6200, 'v2.1-snbp', 'base', '{"biology_avg": 0.30, "chemistry_avg": 0.25, "ranking_percentile": 0.20, "school_accreditation": 0.15, "competition_ratio": 0.10}'),
(5, 2, 12, 0.6200, 0.5500, 0.6900, 'v2.1-snbp', 'base', '{"biology_avg": 0.28, "chemistry_avg": 0.25, "ranking_percentile": 0.22, "school_accreditation": 0.15, "competition_ratio": 0.10}'),
(6, 2, 15, 0.7800, 0.7100, 0.8500, 'v2.1-snbp', 'base', '{"biology_avg": 0.30, "chemistry_avg": 0.28, "ranking_percentile": 0.18, "school_accreditation": 0.14, "competition_ratio": 0.10}'),

-- Dewi Anggraeni predictions (well-rounded)
(7, 3, 17, 0.8300, 0.7700, 0.8900, 'v2.1-snbp', 'base', '{"math_avg": 0.28, "overall_avg": 0.25, "ranking_percentile": 0.25, "school_accreditation": 0.12, "competition_ratio": 0.10}'),
(8, 3, 4, 0.7100, 0.6400, 0.7800, 'v2.1-snbp', 'base', '{"math_avg": 0.25, "overall_avg": 0.30, "ranking_percentile": 0.20, "school_accreditation": 0.13, "competition_ratio": 0.12}'),

-- Budi Santoso predictions (IPS student)
(9, 4, 3, 0.6500, 0.5800, 0.7200, 'v2.1-snbp', 'base', '{"economy_avg": 0.25, "bahasa_avg": 0.20, "ranking_percentile": 0.22, "school_accreditation": 0.18, "competition_ratio": 0.15}'),
(10, 4, 16, 0.7000, 0.6300, 0.7700, 'v2.1-snbp', 'base', '{"economy_avg": 0.22, "bahasa_avg": 0.22, "ranking_percentile": 0.25, "school_accreditation": 0.16, "competition_ratio": 0.15}'),

-- Rina Wulandari predictions
(11, 5, 21, 0.4500, 0.3800, 0.5200, 'v2.1-snbp', 'base', '{"biology_avg": 0.28, "chemistry_avg": 0.25, "ranking_percentile": 0.18, "school_accreditation": 0.17, "competition_ratio": 0.12}'),
(12, 5, 22, 0.7500, 0.6800, 0.8200, 'v2.1-snbp', 'base', '{"math_avg": 0.30, "overall_avg": 0.25, "ranking_percentile": 0.20, "school_accreditation": 0.13, "competition_ratio": 0.12}');

-- What-if scenario for Ahmad Faiz
INSERT INTO predictions (id, student_id, program_id, probability_score, confidence_lower, confidence_upper, model_version, scenario_type, feature_importances) VALUES
(13, 1, 7, 0.8100, 0.7500, 0.8700, 'v2.1-snbp', 'what_if', '{"math_avg_improved": 0.32, "physics_avg": 0.28, "olympiad_bonus": 0.15, "ranking_percentile": 0.15, "competition_ratio": 0.10}');

-- ============================================================
-- Recommendations (alternative program suggestions)
-- ============================================================
INSERT INTO recommendations (id, prediction_id, recommended_program_id, reason, probability_if_switched, changes_needed, rank_order) VALUES
(1, 2, 13, 'Teknik Informatika UGM memiliki rasio persaingan lebih rendah dari ITB dengan kualitas yang setara. Peluang Anda lebih tinggi berdasarkan profil akademik.', 0.8100, '{"note": "Tidak perlu perubahan signifikan, fokus pada rapor semester 5"}', 1),
(2, 2, 17, 'ITS memiliki program Teknik Informatika unggulan dengan rasio persaingan moderat. Cocok sebagai pilihan cadangan yang kuat.', 0.8300, '{"note": "Pertimbangkan sebagai pilihan 2 di SNBP"}', 2),
(3, 4, 15, 'Farmasi UGM memiliki peluang lebih tinggi dibanding Kedokteran UI. Bidang farmasi masih terkait kesehatan dan sesuai minat Anda di biologi/kimia.', 0.7800, '{"note": "Fokus tingkatkan nilai Kimia ke rata-rata 90+"}', 1),
(4, 4, 12, 'Kedokteran UGM sedikit lebih achievable dibanding FK UI karena perbedaan cutoff score. Kualitas pendidikan setara.', 0.6200, '{"improve_subjects": ["Matematika", "Fisika"], "target_increase": 3}', 2),
(5, 11, 22, 'Teknik Informatika UNDIP memiliki peluang jauh lebih tinggi. Pertimbangkan sebagai pilihan realistis dengan prospek karir yang baik.', 0.7500, '{"note": "Bidang IT masih sesuai minat teknis Anda"}', 1);

-- ============================================================
-- Payments (sample transaction history)
-- ============================================================
INSERT INTO payments (id, user_id, amount, currency, payment_method, status, package_type, transaction_id, paid_at) VALUES
(1, 1, 49000.00, 'IDR', 'gopay', 'success', 'basic_prediction', 'TXN-2024-001-GOPAY', '2024-09-15 10:30:00'),
(2, 1, 149000.00, 'IDR', 'bank_transfer_bca', 'success', 'monthly_premium', 'TXN-2024-002-BCA', '2024-10-01 14:00:00'),
(3, 8, 1490000.00, 'IDR', 'bank_transfer_mandiri', 'success', 'yearly_premium', 'TXN-2024-003-MANDIRI', '2024-07-20 09:15:00'),
(4, 2, 49000.00, 'IDR', 'ovo', 'success', 'basic_prediction', 'TXN-2024-004-OVO', '2024-11-10 16:45:00'),
(5, 9, 49000.00, 'IDR', 'dana', 'pending', 'basic_prediction', 'TXN-2024-005-DANA', NULL),
(6, 10, 99000.00, 'IDR', 'shopeepay', 'failed', 'deep_recommendation', 'TXN-2024-006-SPAY', NULL),
(7, 2, 149000.00, 'IDR', 'gopay', 'expired', 'monthly_premium', 'TXN-2024-007-GOPAY', NULL);

-- ============================================================
-- Invite Codes (kode undangan siswa untuk guru)
-- ============================================================
INSERT INTO invite_codes (id, student_id, code, used_by_guru_id, created_at, used_at, is_active) VALUES
(1, 1, 'ABC123', 3, '2024-09-01 10:00:00', '2024-09-01 14:30:00', FALSE),
(2, 2, 'XYZ789', 4, '2024-09-02 08:00:00', '2024-09-02 11:15:00', FALSE),
(3, 8, 'DEF456', NULL, '2024-11-10 09:00:00', NULL, TRUE);

-- ============================================================
-- Guru Comments (komentar guru tentang siswa)
-- ============================================================
INSERT INTO guru_comments (id, guru_id, student_id, comment_text, created_at) VALUES
(1, 3, 1, 'Ahmad memiliki potensi besar di bidang STEM. Sangat direkomendasikan untuk Teknik Informatika UI/ITB.', '2024-10-15 10:30:00'),
(2, 4, 2, 'Siti menunjukkan minat yang kuat di bidang kesehatan. Perlu pertimbangkan alternatif selain FK UI.', '2024-10-16 14:00:00'),
(3, 3, 8, 'Dewi memiliki kemampuan yang seimbang dan cocok untuk program teknik di ITS.', '2024-11-01 09:00:00');

-- ============================================================
-- Notifications (sample notifications)
-- ============================================================
INSERT INTO notifications (id, user_id, type, title, message, is_read) VALUES
(1, 1, 'prediction_ready', 'Hasil Prediksi Siap!', 'Prediksi peluang masuk Teknik Informatika UI sudah tersedia. Klik untuk melihat detail.', TRUE),
(2, 1, 'recommendation', 'Rekomendasi Baru', 'Berdasarkan analisis AI, kami menemukan 2 program studi alternatif yang cocok untuk Anda.', FALSE),
(3, 1, 'payment_success', 'Pembayaran Berhasil', 'Paket Premium Bulanan berhasil diaktifkan. Berlaku hingga 1 November 2024.', TRUE),
(4, 2, 'prediction_ready', 'Hasil Prediksi Siap!', 'Prediksi peluang masuk Kedokteran UI, Kedokteran UGM, dan Farmasi UGM sudah tersedia.', TRUE),
(5, 2, 'system', 'Selamat Datang di LangkahKampus!', 'Lengkapi profil akademik Anda untuk mendapatkan prediksi yang lebih akurat.', TRUE),
(6, 3, 'system', 'Laporan Siswa Tersedia', '3 siswa bimbingan Anda telah menerima hasil prediksi. Klik untuk review.', FALSE),
(7, 7, 'system', 'Platform Update', 'Sistem telah diperbarui ke versi terbaru. Fitur baru: guru comments dan invite codes.', FALSE),
(8, 8, 'prediction_ready', 'Hasil Prediksi Siap!', 'Prediksi peluang masuk Teknik Informatika ITS sudah tersedia dengan confidence level tinggi.', TRUE),
(9, 9, 'warning', 'Pembayaran Pending', 'Pembayaran Anda sebesar Rp49.000 belum dikonfirmasi. Silakan selesaikan pembayaran.', FALSE),
(10, 10, 'system', 'Tingkatkan Akurasi', 'Masukkan nilai rapor semester 5 untuk mendapatkan prediksi terbaru.', FALSE);

-- ============================================================
-- Audit Logs (sample activity logs)
-- ============================================================
INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details, ip_address) VALUES
(1, 'login', 'user', 1, '{"method": "email_password", "device": "Chrome/Windows"}', '103.28.12.45'),
(1, 'view_prediction', 'prediction', 1, '{"program": "Teknik Informatika UI"}', '103.28.12.45'),
(1, 'purchase_package', 'payment', 2, '{"package": "monthly_premium", "amount": 149000}', '103.28.12.45'),
(2, 'login', 'user', 2, '{"method": "email_password", "device": "Safari/iOS"}', '180.244.33.78'),
(2, 'input_academic_record', 'academic_record', NULL, '{"semester": 5, "subjects_count": 6}', '180.244.33.78'),
(3, 'login', 'user', 3, '{"method": "email_password", "device": "Chrome/MacOS"}', '36.68.102.15'),
(3, 'view_student_report', 'student_profile', 1, '{"viewed_student": "Ahmad Faiz Pratama"}', '36.68.102.15'),
(7, 'login', 'user', 7, '{"method": "email_password", "device": "Firefox/Linux"}', '10.0.0.1'),
(7, 'platform_config_update', 'system', NULL, '{"action": "enable_guru_comments_feature"}', '10.0.0.1'),
(NULL, 'system_backup', 'system', NULL, '{"type": "automated_daily", "size_mb": 125}', '127.0.0.1');

-- ============================================================
-- Admission History (historical data for model training)
-- ============================================================
INSERT INTO admission_history (program_id, school_id, year, applicants, accepted, min_score, avg_score) VALUES
-- Teknik Informatika UI from various schools
(1, 1, 2022, 15, 3, 88.50, 91.20),
(1, 1, 2023, 18, 4, 87.80, 90.50),
(1, 2, 2022, 12, 2, 89.00, 90.80),
(1, 2, 2023, 14, 3, 88.20, 91.00),
(1, 3, 2023, 10, 2, 87.50, 89.80),

-- Kedokteran UI
(2, 1, 2022, 25, 2, 93.00, 94.50),
(2, 1, 2023, 28, 3, 92.50, 94.00),
(2, 2, 2022, 20, 2, 92.80, 94.20),
(2, 2, 2023, 22, 2, 93.20, 94.80),

-- Teknik Informatika ITB
(7, 1, 2022, 20, 2, 90.00, 92.30),
(7, 1, 2023, 22, 3, 89.50, 91.80),
(7, 2, 2022, 18, 3, 89.80, 91.50),
(7, 3, 2023, 12, 2, 88.00, 90.20),

-- Kedokteran UGM
(12, 3, 2022, 18, 2, 91.00, 93.00),
(12, 3, 2023, 20, 3, 90.50, 92.50),
(12, 4, 2022, 15, 2, 91.50, 93.20),
(12, 4, 2023, 16, 2, 91.00, 92.80),

-- Teknik Informatika ITS
(17, 3, 2022, 14, 4, 85.00, 87.50),
(17, 3, 2023, 16, 5, 84.50, 87.00),
(17, 4, 2022, 10, 3, 84.00, 86.50),
(17, 5, 2023, 8, 2, 83.50, 86.00),

-- Kedokteran UNDIP
(21, 5, 2022, 12, 2, 89.00, 91.00),
(21, 5, 2023, 14, 2, 88.50, 90.80),

-- Teknik Informatika UNDIP
(22, 5, 2022, 10, 4, 82.00, 84.50),
(22, 5, 2023, 12, 5, 81.50, 84.00),

-- Hukum UI
(3, 1, 2022, 20, 5, 83.00, 85.50),
(3, 1, 2023, 22, 5, 82.50, 85.00),
(3, 4, 2023, 8, 2, 82.00, 84.50);
