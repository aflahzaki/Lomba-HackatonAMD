"""
Generate Stage 5: Phase C - IS Architecture (Data + Application)
TOGAF Enterprise Architecture - LangkahKampus EduTech

This script generates the Stage 5 document covering:
- Phase C-1: Data Architecture (Baseline, Target, Gap Analysis)
- Phase C-2: Application Architecture (Baseline, Target, Gap Analysis)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx_utils import (
    create_document,
    add_cover_page,
    add_table_of_contents,
    add_heading,
    add_paragraph,
    add_bullet_list,
    add_numbered_list,
    add_table,
    add_references,
    save_document,
)


def generate_stage5():
    """Generate Stage 5: Phase C - IS Architecture (Data + Application)."""
    doc = create_document()

    # Cover Page
    add_cover_page(
        doc,
        title="Phase C: Arsitektur Sistem Informasi",
        stage_name="Stage 5 - Arsitektur SI (Data & Aplikasi)"
    )

    # Table of Contents
    toc_sections = [
        ("Phase C-1: Arsitektur Data", [
            "Arsitektur Data Baseline",
            "Arsitektur Data Target",
            "Gap Analysis - Data",
            "Kebutuhan Data",
            "Prinsip Data (Diperbarui)",
        ]),
        ("Phase C-2: Arsitektur Aplikasi", [
            "Arsitektur Aplikasi Baseline",
            "Arsitektur Aplikasi Target",
            "Gap Analysis - Aplikasi",
            "Kebutuhan Aplikasi",
            "Prinsip Aplikasi (Diperbarui)",
        ]),
        ("Pernyataan Pekerjaan Arsitektur (Diperbarui)", []),
        ("Daftar Pustaka", []),
    ]
    add_table_of_contents(doc, toc_sections)

    # ==========================================================================
    # PHASE C-1: DATA ARCHITECTURE
    # ==========================================================================
    add_heading(doc, "1. Phase C-1: Arsitektur Data", level=1)

    add_paragraph(doc,
        "Phase C-1 mendefinisikan arsitektur data yang mendukung kebutuhan bisnis "
        "dan aplikasi LangkahKampus. Arsitektur data mencakup struktur data, "
        "mekanisme pengelolaan data, dan kebijakan governance yang memastikan "
        "kualitas, keamanan, dan ketersediaan data untuk operasional platform "
        "dan machine learning pipeline."
    )

    # --------------------------------------------------------------------------
    # 1.1 BASELINE DATA ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "1.1 Arsitektur Data Baseline", level=2)

    add_paragraph(doc,
        "Arsitektur data baseline menggambarkan kondisi pengelolaan data SNBP "
        "sebelum implementasi platform LangkahKampus. Data tersebar di berbagai "
        "lokasi tanpa standarisasi format dan tanpa integrasi sistem."
    )

    # Data Entity/Component Catalog (Baseline)
    add_heading(doc, "1.1.1 Data Entity/Component Catalog (Baseline)", level=3)

    add_table(doc,
        headers=["Data Entity", "Format", "Lokasi Penyimpanan", "Owner", "Kualitas Data"],
        rows=[
            ["Nilai Rapor Siswa", "Paper/Excel", "Masing-masing sekolah (tidak terpusat)", "Sekolah (Wali Kelas)", "Rendah - inkonsisten antar sekolah"],
            ["Data Profil Siswa", "Paper/SIS sekolah", "Database sekolah (jika ada) atau buku induk", "Sekolah (Tata Usaha)", "Sedang - sering tidak update"],
            ["Data Penerimaan SNBP Historis", "Tidak dipublikasikan resmi", "LTMPT (tertutup)", "LTMPT", "Tidak diketahui - tidak accessible"],
            ["Informasi Program Studi", "Website, brosur", "Tersebar di website masing-masing PT", "Perguruan Tinggi", "Sedang - sering outdated"],
            ["Data Kuota SNBP", "PDF/website LTMPT", "Website LTMPT (per tahun)", "LTMPT", "Tinggi - tapi akses terbatas"],
            ["Catatan Konseling Guru BK", "Buku catatan/notes", "Personal Guru BK", "Guru BK", "Rendah - tidak terstruktur"],
            ["Data PDSS", "Digital (portal LTMPT)", "Server LTMPT", "LTMPT/Sekolah", "Tinggi - tervalidasi"],
        ],
        title="Data Entity/Component Catalog (Baseline)",
        table_number=1
    )

    # Application/Data Matrix (Baseline)
    add_heading(doc, "1.1.2 Application/Data Matrix (Baseline)", level=3)

    add_table(doc,
        headers=["Aplikasi/Tool", "Nilai Rapor", "Profil Siswa", "Info Prodi", "Kuota SNBP", "Catatan BK"],
        rows=[
            ["Portal PDSS LTMPT", "Read/Write", "Read/Write", "-", "-", "-"],
            ["Portal SNBP LTMPT", "-", "Read", "-", "Read", "-"],
            ["Spreadsheet Guru BK", "Read (manual input)", "Read (manual)", "-", "-", "Read/Write"],
            ["SIS Sekolah (jika ada)", "Read/Write", "Read/Write", "-", "-", "-"],
            ["Browser/Google", "-", "-", "Read", "Read", "-"],
        ],
        title="Application/Data Matrix (Baseline)",
        table_number=2
    )

    # ER Diagram Description (Baseline)
    add_heading(doc, "1.1.3 Entity Relationship Diagram (Baseline)", level=3)

    add_paragraph(doc,
        "Pada kondisi baseline, tidak terdapat database terpusat yang menghubungkan "
        "entitas-entitas data. Relasi antar data bersifat implisit dan manual. "
        "Berikut adalah entitas utama yang ada (tanpa relasi formal):"
    )

    add_bullet_list(doc, [
        "SISWA (NIS, nama, kelas, sekolah) - tersimpan di SIS sekolah atau buku induk",
        "NILAI_RAPOR (NIS, semester, mata_pelajaran, nilai) - tersimpan di rapor fisik",
        "SEKOLAH (NPSN, nama, alamat, akreditasi) - data referensi Kemendikbud",
        "PROGRAM_STUDI (kode, nama, universitas, daya_tampung) - tersebar di berbagai sumber",
        "Tidak ada relasi formal: data dihubungkan secara manual oleh operator saat input PDSS",
    ])

    # --------------------------------------------------------------------------
    # 1.2 TARGET DATA ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "1.2 Arsitektur Data Target", level=2)

    add_paragraph(doc,
        "Arsitektur data target menggambarkan pengelolaan data pada platform "
        "LangkahKampus yang terintegrasi, dengan database terpusat, data governance "
        "yang ketat, dan pipeline data yang mendukung ML model training dan inference."
    )

    # Data Entity/Component Catalog (Target)
    add_heading(doc, "1.2.1 Data Entity/Component Catalog (Target)", level=3)

    add_table(doc,
        headers=["Data Entity", "Format", "Storage", "Owner", "Classification"],
        rows=[
            ["users", "Relational (PostgreSQL)", "Primary Database", "Platform Engineering", "PII - Confidential"],
            ["student_profiles", "Relational + JSON", "Primary Database", "Data Engineering", "PII - Confidential"],
            ["academic_records (nilai rapor)", "Relational", "Primary Database", "Data Engineering", "PII - Restricted"],
            ["schools", "Relational", "Primary Database", "Data Engineering", "Public"],
            ["programs (program studi)", "Relational", "Primary Database", "Data Engineering", "Public"],
            ["universities", "Relational", "Primary Database", "Data Engineering", "Public"],
            ["predictions", "Relational + JSON", "Primary Database + Cache", "ML Engineering", "PII - Restricted"],
            ["recommendations", "JSON", "Cache (Redis) + DB", "ML Engineering", "PII - Restricted"],
            ["referral_tracking", "Relational + JSON", "Primary Database", "Platform Engineering", "Internal"],
            ["admission_history", "Relational", "Data Warehouse", "Data Engineering", "Aggregated - Internal"],
            ["ml_features", "Parquet/Feature Store", "Feature Store (Redis)", "ML Engineering", "Internal"],
            ["ml_models", "Binary (pickle/ONNX)", "Model Registry (MLflow)", "ML Engineering", "Internal - IP"],
            ["payments", "Relational", "Primary Database", "Finance", "PII - Confidential"],
            ["guru_comments", "Relational", "Primary Database", "Platform Engineering", "PII - Restricted"],
            ["invite_codes", "Relational", "Primary Database", "Platform Engineering", "Internal"],
            ["analytics_events", "JSON (streaming)", "Data Warehouse", "Data Engineering", "Internal"],
            ["audit_logs", "Append-only log", "Separate audit DB", "Security", "Internal - Compliance"],
        ],
        title="Data Entity/Component Catalog (Target)",
        table_number=3
    )

    # Application/Data Matrix (Target)
    add_heading(doc, "1.2.2 Application/Data Matrix (Target)", level=3)

    add_table(doc,
        headers=["Application", "users", "student_profiles", "predictions", "referral_tracking", "payments", "guru_comments"],
        rows=[
            ["Landing Page", "R (login)", "-", "-", "-", "-", "-"],
            ["Onboarding Wizard", "R", "CRU", "-", "-", "-", "-"],
            ["Dashboard Siswa", "R", "RU", "R", "R", "R", "R"],
            ["Prediksi All-in-One", "RU (counter)", "R", "CRW", "-", "-", "-"],
            ["Peta Universitas", "R", "-", "-", "-", "-", "-"],
            ["Pembayaran/Referral", "RU", "-", "-", "CRU", "CRW", "-"],
            ["API Referral", "R", "-", "-", "CRU", "-", "-"],
            ["Dashboard Guru", "R", "R", "R", "-", "-", "CRW"],
            ["ML Prediction Service", "-", "R", "W", "-", "-", "-"],
            ["ML Training Pipeline", "-", "R", "-", "-", "-", "-"],
        ],
        title="Application/Data Matrix (Target) - C=Create, R=Read, U=Update, W=Write",
        table_number=4
    )

    # ER Diagram Description (Target)
    add_heading(doc, "1.2.3 Entity Relationship Diagram (Target)", level=3)

    add_paragraph(doc,
        "Entity Relationship Diagram target menggambarkan model data relasional "
        "lengkap untuk platform LangkahKampus. Berikut adalah entitas utama "
        "beserta relasinya:"
    )

    add_paragraph(doc, "Entitas Core dan Relasi:", bold=True)
    add_bullet_list(doc, [
        "users (1) --- (1) student_profiles: Setiap user siswa memiliki satu profil lengkap",
        "student_profiles (1) --- (N) academic_records: Setiap siswa memiliki banyak catatan nilai",
        "student_profiles (N) --- (1) schools: Banyak siswa terdaftar di satu sekolah",
        "programs (N) --- (1) universities: Banyak prodi di satu universitas",
        "student_profiles (1) --- (N) predictions: Setiap siswa dapat memiliki banyak prediksi",
        "predictions (N) --- (1) programs: Setiap prediksi ditujukan untuk satu prodi",
        "predictions (1) --- (N) recommendations: Setiap prediksi menghasilkan rekomendasi counterfactual",
        "users (1) --- (N) payments: Setiap user dapat memiliki banyak transaksi",
        "users (1) --- (1) referral_tracking: Setiap siswa memiliki satu record referral",
        "users (1) --- (N) invite_codes: Setiap siswa dapat membuat kode undangan untuk guru",
        "users (N) --- (N) guru_comments: Guru memberikan komentar pada prediksi siswa",
        "admission_history (N) --- (1) programs: Data historis penerimaan per prodi",
    ])

    add_paragraph(doc, "Entitas ML dan Relasi:", bold=True)
    add_bullet_list(doc, [
        "ml_features (derived from) student_profiles + academic_records + admission_history",
        "ml_models (1) --- (N) predictions: Setiap model versi menghasilkan banyak prediksi",
        "predictions (1) --- (1) counterfactual_explanations: Setiap prediksi punya XAI explanation",
    ])

    add_paragraph(doc, "Key Attributes per Entity:", bold=True)
    add_paragraph(doc,
        "users: id (PK), email, phone, password_hash, role (siswa/guru), "
        "predictions_used INT DEFAULT 0, predictions_limit INT DEFAULT 3, "
        "created_at, last_login"
    )
    add_paragraph(doc,
        "student_profiles: id (PK), user_id (FK), school_id (FK), full_name, "
        "birth_date, gender, ranking_in_school, total_students, grade_level, "
        "major_track (IPA/IPS/Bahasa)"
    )
    add_paragraph(doc,
        "academic_records: id (PK), student_id (FK), semester (1-5), subject, score, "
        "verified_at"
    )
    add_paragraph(doc,
        "predictions: id (PK), student_id (FK), program_id (FK), model_version, "
        "probability_score, choice2_trap_warning BOOLEAN, peer_count INT, "
        "feature_importances (JSON), created_at"
    )
    add_paragraph(doc,
        "referral_tracking: id (PK), user_id (FK) UNIQUE, referral_code VARCHAR(20) UNIQUE, "
        "click_count INT DEFAULT 0, unique_ips JSON, unlocked_predictions INT DEFAULT 0, "
        "created_at TIMESTAMP"
    )

    # --------------------------------------------------------------------------
    # 1.3 GAP ANALYSIS - DATA
    # --------------------------------------------------------------------------
    add_heading(doc, "1.3 Gap Analysis - Arsitektur Data", level=2)

    add_heading(doc, "1.3.1 Gap Analysis Matrix - Data", level=3)

    add_table(doc,
        headers=["Data Domain", "Baseline", "Target", "Gap Description", "Effort"],
        rows=[
            ["Student Data", "Fragmented across schools, paper/Excel", "Centralized PostgreSQL with validation", "Full data model design, migration tools, validation pipeline", "Tinggi"],
            ["Academic Records", "Manual entry, no standardization", "Structured relational with verification workflow", "Schema design, OCR integration, verification process", "Tinggi"],
            ["Admission History", "Not accessible (LTMPT closed)", "Data warehouse with 5+ years historical data", "Data partnership/crowdsourcing strategy needed", "Sangat Tinggi"],
            ["ML Feature Store", "Non-existent", "Redis/BigQuery feature store for real-time inference", "Feature engineering pipeline, store infrastructure", "Tinggi"],
            ["Geospatial Data", "Non-existent", "PostGIS with school/university locations", "GIS data collection, geocoding integration", "Sedang"],
            ["Payment Data", "Non-existent", "PCI-DSS compliant payment records", "Payment gateway integration, compliance", "Sedang"],
            ["Analytics Data", "Non-existent", "Event-driven analytics in data warehouse", "Event schema design, streaming pipeline", "Sedang"],
            ["Audit/Compliance", "Non-existent", "Append-only audit logs with UU PDP compliance", "Audit infrastructure, retention policies", "Sedang"],
        ],
        title="Gap Analysis Matrix - Data Architecture",
        table_number=5
    )

    # Gap and Solution Table - Data
    add_heading(doc, "1.3.2 Gap and Solution Table - Data", level=3)

    add_table(doc,
        headers=["Gap ID", "Gap", "Solution", "Technology", "Timeline"],
        rows=[
            ["GAP-D01", "No centralized student database", "Design and implement PostgreSQL schema with proper normalization and indexing", "PostgreSQL 15, Alembic migrations", "Fase 1 (Bulan 1-2)"],
            ["GAP-D02", "No data validation pipeline", "Implement data quality checks, deduplication, and anomaly detection", "Great Expectations, custom validators", "Fase 1 (Bulan 2-3)"],
            ["GAP-D03", "No historical admission data", "Crowdsourcing from users + data partnerships with schools + web scraping public data", "Scrapy, user contribution system", "Fase 1-2 (Bulan 1-6)"],
            ["GAP-D04", "No ML feature store", "Implement feature store for real-time and batch feature serving", "Feast/Redis, BigQuery", "Fase 1 (Bulan 3-4)"],
            ["GAP-D05", "No data governance framework", "Implement data classification, access controls, retention policies per UU PDP", "Custom policies, automated enforcement", "Fase 1 (Bulan 2-3)"],
            ["GAP-D06", "No geospatial capability", "Add PostGIS extension, geocode all schools/universities, build proximity queries", "PostGIS, Google Maps API", "Fase 2 (Bulan 5-6)"],
            ["GAP-D07", "No event streaming", "Implement event-driven architecture for real-time analytics and dashboard updates", "Apache Kafka / Redis Streams", "Fase 2 (Bulan 5-7)"],
            ["GAP-D08", "No backup/DR for data", "Implement automated backups, point-in-time recovery, cross-region replication", "pg_dump, WAL archiving, cloud DR", "Fase 1 (Bulan 3-4)"],
        ],
        title="Gap and Solution Table - Data Architecture",
        table_number=6
    )

    # Transition Timeline - Data
    add_heading(doc, "1.3.3 Transition Timeline - Data Architecture", level=3)

    add_table(doc,
        headers=["Fase", "Periode", "Data Milestones"],
        rows=[
            ["Fase 1", "Bulan 1-4", "PostgreSQL schema deployed, data validation pipeline operational, feature store v1, backup automated, initial historical data collected (10K+ records)"],
            ["Fase 2", "Bulan 5-8", "Event streaming operational, geospatial data complete, analytics warehouse live, 100K+ historical records, data governance fully enforced"],
            ["Fase 3", "Bulan 9-12", "Full data platform maturity, 500K+ records, real-time ML feature serving, cross-region DR tested, compliance audit passed"],
        ],
        title="Transition Timeline - Data Architecture",
        table_number=7
    )

    # Data Requirements
    add_heading(doc, "1.4 Kebutuhan Data", level=2)

    add_table(doc,
        headers=["ID", "Kebutuhan", "Rasional", "Prioritas"],
        rows=[
            ["DR-001", "Data harus dienkripsi saat tersimpan (AES-256) dan saat ditransmisikan (TLS 1.3)", "Kepatuhan UU PDP, melindungi data pribadi siswa", "P1"],
            ["DR-002", "Kebijakan retensi data: data aktif 3 tahun, diarsipkan 7 tahun, lalu dihapus", "Kepatuhan regulasi dan optimasi penyimpanan", "P1"],
            ["DR-003", "Semua perubahan data harus menghasilkan jejak audit dengan pelaku, waktu, dan detail perubahan", "Kepatuhan, debugging, akuntabilitas", "P1"],
            ["DR-004", "Data pelatihan ML harus dianonimkan/dipseudonymkan sebelum digunakan", "Perlindungan privasi untuk pelatihan model", "P1"],
            ["DR-005", "Database harus mendukung pemulihan titik waktu dengan RPO < 1 jam", "Kelangsungan bisnis, perlindungan data", "P1"],
            ["DR-006", "Feature store harus menyajikan fitur dengan latensi < 50ms untuk inferensi real-time", "SLA prediksi ML (< 2 detik total)", "P1"],
            ["DR-007", "Skor kualitas data harus > 95% untuk semua entitas kritis (siswa, nilai)", "Akurasi model ML bergantung pada kualitas data", "P2"],
            ["DR-008", "Pengguna harus dapat mengekspor dan menghapus data pribadinya (hak untuk dilupakan)", "UU PDP Pasal 8 - hak untuk dilupakan", "P1"],
        ],
        title="Kebutuhan Data",
        table_number=8
    )

    # Data Principles Updated
    add_heading(doc, "1.5 Prinsip Data (Diperbarui)", level=2)

    data_principles = [
        {
            "name": "ML-Ready Data Design",
            "statement": "Data schemas harus dirancang untuk mendukung ML feature engineering secara native, tidak hanya untuk transactional queries",
            "rationale": "Core value proposition LangkahKampus adalah ML prediction. Data yang tidak ML-ready menyebabkan complex ETL dan latency.",
            "implications": "Denormalized views untuk ML, feature store integration, versioned feature definitions"
        },
        {
            "name": "Data Minimization",
            "statement": "Hanya data yang benar-benar diperlukan untuk layanan yang boleh dikumpulkan dan disimpan",
            "rationale": "UU PDP mengharuskan data minimization. Mengumpulkan data berlebih meningkatkan risiko dan biaya.",
            "implications": "Review setiap data collection point, regular data purging, consent-based collection"
        },
    ]

    for p in data_principles:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # ==========================================================================
    # PHASE C-2: APPLICATION ARCHITECTURE
    # ==========================================================================
    add_heading(doc, "2. Phase C-2: Arsitektur Aplikasi", level=1)

    add_paragraph(doc,
        "Phase C-2 mendefinisikan arsitektur aplikasi yang menerjemahkan kebutuhan "
        "bisnis dan data menjadi komponen-komponen aplikasi yang terstruktur. "
        "Arsitektur aplikasi LangkahKampus mengadopsi microservices pattern untuk "
        "memungkinkan skalabilitas independen per komponen dan pengembangan paralel "
        "oleh tim yang kecil."
    )

    # --------------------------------------------------------------------------
    # 2.1 BASELINE APPLICATION ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "2.1 Arsitektur Aplikasi Baseline", level=2)

    add_paragraph(doc,
        "Pada kondisi baseline, tidak terdapat platform digital khusus untuk "
        "proses SNBP. Tools yang digunakan bersifat generic dan tidak terintegrasi."
    )

    # Application Portfolio Catalog (Baseline)
    add_heading(doc, "2.1.1 Application Portfolio Catalog (Baseline)", level=3)

    add_table(doc,
        headers=["Aplikasi", "Tipe", "Vendor/Platform", "Fungsi", "Pengguna"],
        rows=[
            ["Portal PDSS LTMPT", "Web Application", "LTMPT", "Input data siswa dan nilai rapor ke sistem LTMPT", "Operator Sekolah"],
            ["Portal SNBP LTMPT", "Web Application", "LTMPT", "Registrasi dan pemilihan prodi oleh siswa", "Siswa"],
            ["Microsoft Excel", "Desktop Application", "Microsoft", "Rekap nilai, daftar pilihan siswa (oleh Guru BK)", "Guru BK"],
            ["WhatsApp", "Mobile Application", "Meta", "Komunikasi informal tentang SNBP", "Semua"],
            ["Google Search", "Web Application", "Google", "Pencarian informasi prodi dan universitas", "Siswa, Orang Tua"],
            ["SIS Sekolah (opsional)", "Web/Desktop App", "Beragam vendor", "Manajemen data siswa (jika sekolah memiliki)", "Operator Sekolah"],
        ],
        title="Application Portfolio Catalog (Baseline)",
        table_number=9
    )

    # App/Organization Matrix (Baseline)
    add_heading(doc, "2.1.2 Application/Organization Matrix (Baseline)", level=3)

    add_table(doc,
        headers=["Aplikasi", "Siswa", "Guru BK", "Operator", "Kepala Sekolah", "Orang Tua"],
        rows=[
            ["Portal PDSS", "-", "-", "Primary User", "Approver", "-"],
            ["Portal SNBP", "Primary User", "-", "-", "-", "-"],
            ["Excel", "-", "Primary User", "Occasional", "-", "-"],
            ["WhatsApp", "User", "User", "User", "User", "User"],
            ["Google", "User", "Occasional", "-", "-", "User"],
        ],
        title="Application/Organization Matrix (Baseline)",
        table_number=10
    )

    # App/Function Matrix (Baseline)
    add_heading(doc, "2.1.3 Application/Function Matrix (Baseline)", level=3)

    add_table(doc,
        headers=["Aplikasi", "Data Entry", "Prediksi", "Rekomendasi", "Koordinasi", "Komunikasi"],
        rows=[
            ["Portal PDSS", "Ya", "Tidak", "Tidak", "Tidak", "Tidak"],
            ["Portal SNBP", "Ya (pilihan)", "Tidak", "Tidak", "Tidak", "Tidak"],
            ["Excel", "Ya (manual)", "Tidak", "Tidak", "Parsial", "Tidak"],
            ["WhatsApp", "Tidak", "Tidak", "Informal", "Informal", "Ya"],
            ["Google", "Tidak", "Tidak", "Tidak", "Tidak", "Tidak"],
        ],
        title="Application/Function Matrix (Baseline)",
        table_number=11
    )

    # App Interaction Matrix (Baseline)
    add_heading(doc, "2.1.4 Application Interaction Matrix (Baseline)", level=3)

    add_paragraph(doc,
        "Pada kondisi baseline, interaksi antar aplikasi sangat minimal dan "
        "bersifat manual (copy-paste data antar sistem):"
    )

    add_table(doc,
        headers=["", "Portal PDSS", "Portal SNBP", "Excel", "WhatsApp", "SIS"],
        rows=[
            ["Portal PDSS", "-", "Data siswa (manual)", "Sumber data", "-", "Copy data manual"],
            ["Portal SNBP", "Referensi PDSS", "-", "-", "-", "-"],
            ["Excel", "Export manual", "-", "-", "Share file", "Copy-paste"],
            ["WhatsApp", "-", "-", "Share screenshot", "-", "-"],
            ["SIS", "Manual transfer", "-", "Export", "-", "-"],
        ],
        title="Application Interaction Matrix (Baseline) - Semua interaksi manual",
        table_number=12
    )

    # App Communication Diagram Description (Baseline)
    add_heading(doc, "2.1.5 Application Communication Diagram (Baseline)", level=3)
    add_paragraph(doc,
        "Pada kondisi baseline, tidak ada communication pattern yang formal antar "
        "aplikasi. Semua transfer data dilakukan secara manual oleh pengguna "
        "(human-mediated integration). Operator sekolah secara manual meng-copy data "
        "dari SIS/Excel ke portal PDSS. Siswa secara manual mencari informasi dari "
        "berbagai sumber yang tidak terhubung. Tidak ada API, tidak ada event-driven "
        "communication, dan tidak ada shared database antar aplikasi."
    )

    # --------------------------------------------------------------------------
    # 2.2 TARGET APPLICATION ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "2.2 Arsitektur Aplikasi Target", level=2)

    add_paragraph(doc,
        "Arsitektur aplikasi target LangkahKampus mengadopsi microservices architecture "
        "pattern dengan API Gateway sebagai entry point, event-driven communication "
        "antar services, dan clear separation of concerns."
    )

    # Application Portfolio Catalog (Target)
    add_heading(doc, "2.2.1 Application Portfolio Catalog (Target)", level=3)

    add_table(doc,
        headers=["Aplikasi", "Tipe", "Teknologi", "Deskripsi", "Strategi Scaling"],
        rows=[
            ["Landing Page", "Frontend", "PHP 8.x + HTML/CSS/JS", "Halaman depan public: beranda, informasi, CTA registrasi", "CDN caching"],
            ["Registrasi + Onboarding Wizard", "Web Page", "PHP 8.x + Vanilla JS", "Multi-step onboarding: data sekolah, nilai rapor, pilihan prodi", "Session-based state"],
            ["Dashboard Siswa", "Web Page", "PHP 8.x + Vanilla JS", "Profil terintegrasi, edit data akademik inline, status referral, quick actions", "Server-side rendering"],
            ["Halaman Prediksi All-in-One", "Web Page", "PHP 8.x + JS (gauge, charts)", "Form input + hasil terpadu: gauge, Choice-2 Trap, peer stats, rekomendasi", "API call ke ML service"],
            ["Peta Universitas", "Web Page", "PHP 8.x + Leaflet.js", "Exploration mode dengan detail prodi dan tombol Prediksi Langsung", "Static map tiles + CDN"],
            ["Halaman Pembayaran/Referral", "Web Page", "PHP 8.x + Payment SDK", "Status kuota, opsi bayar atau bagikan referral link, progress tracker", "Server-side + webhook"],
            ["API Referral", "API Endpoint", "PHP 8.x", "POST: generate referral code, GET: track klik unik (IP validation)", "Stateless PHP"],
            ["API Prediksi", "API Endpoint", "PHP 8.x (proxy) + FastAPI ML", "Proxy request ke ML microservice, handle prediction limit checking", "ML service scaling"],
            ["Dashboard Guru", "Web Page", "PHP 8.x", "Lihat profil siswa yang invite, lihat prediksi, beri komentar", "Server-side rendering"],
            ["ML Prediction Service", "Microservice", "FastAPI + Python", "Model inference: XGBoost + LightGBM ensemble, feature computation", "Horizontal scaling"],
            ["ML Training Pipeline", "Batch Application", "Python + MLflow", "Model training, evaluation, versioning", "On-demand (scheduled)"],
        ],
        title="Application Portfolio Catalog (Target)",
        table_number=13
    )

    # App/Organization Matrix (Target)
    add_heading(doc, "2.2.2 Application/Organization Matrix (Target)", level=3)

    add_table(doc,
        headers=["Application", "Siswa", "Guru", "Platform Admin", "ML Team"],
        rows=[
            ["Landing Page", "Visitor", "Visitor", "-", "-"],
            ["Onboarding Wizard", "Primary", "-", "-", "-"],
            ["Dashboard Siswa", "Primary", "-", "-", "-"],
            ["Prediksi All-in-One", "Primary", "-", "Monitor", "Owner"],
            ["Peta Universitas", "Primary", "-", "-", "-"],
            ["Pembayaran/Referral", "Primary", "-", "Monitor", "-"],
            ["Dashboard Guru", "-", "Primary", "-", "-"],
            ["API Referral", "Indirect", "-", "Monitor", "-"],
            ["ML Prediction Service", "Consumer", "Consumer (indirect)", "Monitor", "Owner"],
        ],
        title="Application/Organization Matrix (Target)",
        table_number=14
    )

    # App/Function Matrix (Target)
    add_heading(doc, "2.2.3 Application/Function Matrix (Target)", level=3)

    add_table(doc,
        headers=["Application", "Auth", "Prediction", "Recommendation", "Anti-Bentrok", "Payment", "Notification", "Analytics"],
        rows=[
            ["User Service", "Primary", "-", "-", "-", "-", "-", "-"],
            ["Prediction Service", "-", "Primary", "-", "-", "-", "-", "Emit events"],
            ["Recommendation Service", "-", "Consume", "Primary", "-", "-", "-", "Emit events"],
            ["School Dashboard Service", "-", "Consume", "Consume", "Primary", "-", "Trigger", "Emit events"],
            ["Payment Service", "Verify", "-", "-", "-", "Primary", "Trigger", "Emit events"],
            ["Notification Service", "Verify", "-", "-", "-", "-", "Primary", "-"],
            ["Analytics Service", "-", "Consume", "Consume", "Consume", "Consume", "-", "Primary"],
        ],
        title="Application/Function Matrix (Target)",
        table_number=15
    )

    # App Interaction Matrix (Target)
    add_heading(doc, "2.2.4 Application Interaction Matrix (Target)", level=3)

    add_table(doc,
        headers=["", "API GW", "User Svc", "Predict Svc", "Recom Svc", "School Svc", "Payment", "Notif Svc"],
        rows=[
            ["API Gateway", "-", "REST", "REST", "REST", "REST", "REST", "-"],
            ["User Service", "-", "-", "-", "-", "-", "-", "Event"],
            ["Prediction Svc", "-", "REST (auth)", "-", "gRPC", "-", "-", "Event"],
            ["Recommendation", "-", "REST (auth)", "gRPC", "-", "-", "-", "Event"],
            ["School Dashboard", "-", "REST (auth)", "REST", "REST", "-", "-", "Event"],
            ["Payment Svc", "-", "REST (auth)", "-", "-", "-", "-", "Event"],
            ["Notification Svc", "-", "REST (user info)", "-", "-", "-", "-", "-"],
            ["ML Pipeline", "-", "-", "Model deploy", "-", "-", "-", "-"],
        ],
        title="Application Interaction Matrix (Target) - REST/gRPC/Event",
        table_number=16
    )

    # App Communication Diagram Description (Target)
    add_heading(doc, "2.2.5 Application Communication Diagram (Target)", level=3)

    add_paragraph(doc,
        "Arsitektur komunikasi target menggunakan dua pattern utama:"
    )

    add_paragraph(doc, "1. Synchronous Communication (Request/Response):", bold=True)
    add_bullet_list(doc, [
        "Client (Next.js) -> API Gateway -> Microservices: REST over HTTPS untuk semua user-facing requests",
        "Inter-service calls: gRPC untuk high-performance internal communication (Prediction <-> Recommendation)",
        "API Gateway handles: JWT validation, rate limiting (100 req/min per user), request routing, load balancing",
    ])

    add_paragraph(doc, "2. Asynchronous Communication (Event-Driven):", bold=True)
    add_bullet_list(doc, [
        "Event Bus (Kafka/Redis Streams): Untuk notifikasi, analytics, dan eventual consistency antar services",
        "Events published: prediction.completed, payment.success, user.registered, alert.bentrok_detected",
        "Background workers (Celery): Email sending, report generation, ML model retraining triggers",
        "WebSocket: Real-time updates untuk Anti-Bentrok dashboard (bidirectional communication)",
    ])

    add_paragraph(doc, "3. Data Flow Pattern:", bold=True)
    add_bullet_list(doc, [
        "CQRS pattern: Separate read (optimized views) dan write (transactional) paths untuk high-traffic endpoints",
        "Cache-aside pattern: Redis caching untuk frequently accessed data (program info, school data)",
        "Saga pattern: Untuk distributed transactions (payment + premium activation + notification)",
    ])

    # --------------------------------------------------------------------------
    # 2.3 GAP ANALYSIS - APPLICATION
    # --------------------------------------------------------------------------
    add_heading(doc, "2.3 Gap Analysis - Arsitektur Aplikasi", level=2)

    add_heading(doc, "2.3.1 Gap Analysis Matrix - Application", level=3)

    add_table(doc,
        headers=["Application Capability", "Baseline", "Target", "Gap", "Complexity"],
        rows=[
            ["User Authentication & Management", "No digital platform", "OAuth + JWT + RBAC across services", "Build from scratch: auth service, user management, role system", "Sedang"],
            ["ML Prediction Engine", "Non-existent", "Real-time ensemble prediction (<2s)", "Build complete: model training, serving, monitoring, A/B testing", "Sangat Tinggi"],
            ["XAI Recommendation", "Non-existent", "DiCE counterfactual explanations", "Build: DiCE integration, explanation generation, ranking algorithm", "Tinggi"],
            ["Real-time Dashboard", "Excel spreadsheet", "WebSocket-powered Anti-Bentrok dashboard", "Build: real-time service, conflict detection, WebSocket server", "Tinggi"],
            ["Payment Processing", "Non-existent", "Integrated payment gateway (freemium + B2B)", "Build: payment service, gateway integration, subscription management", "Sedang"],
            ["API Gateway", "Non-existent", "Kong/Nginx with auth, rate limiting, routing", "Deploy and configure: Kong, JWT plugin, rate limiting rules", "Sedang"],
            ["Frontend Platform", "No platform", "PHP 8.x responsive web app", "Build complete: student dashboard, prediksi all-in-one, guru dashboard", "Tinggi"],
            ["Notification System", "WhatsApp (informal)", "Multi-channel automated notifications", "Build: notification service, template engine, scheduling, delivery", "Sedang"],
            ["Analytics & Monitoring", "Non-existent", "Full observability + business analytics", "Build: event pipeline, metrics collection, dashboards", "Sedang"],
            ["Background Processing", "Non-existent", "Celery workers for async tasks", "Deploy: Celery, Redis broker, task definitions, monitoring", "Rendah"],
        ],
        title="Gap Analysis Matrix - Application Architecture",
        table_number=17
    )

    # Gap and Solution Table - Application
    add_heading(doc, "2.3.2 Gap and Solution Table - Application", level=3)

    add_table(doc,
        headers=["Gap ID", "Gap", "Solution", "Technology Stack"],
        rows=[
            ["GAP-A01", "No user management platform", "Build User Service with OAuth2, JWT tokens, RBAC", "FastAPI, PostgreSQL, python-jose, passlib"],
            ["GAP-A02", "No ML serving infrastructure", "Build Prediction Service with model registry and inference optimization", "FastAPI, XGBoost, LightGBM, MLflow, ONNX"],
            ["GAP-A03", "No explainable AI capability", "Build Recommendation Service integrating DiCE framework", "FastAPI, DiCE-ML, SHAP, custom ranking"],
            ["GAP-A04", "No real-time capability", "Build School Dashboard with WebSocket support and conflict detection", "FastAPI, WebSocket, Redis Pub/Sub, Next.js"],
            ["GAP-A05", "No payment infrastructure", "Build Payment Service with Midtrans/Xendit SDK integration", "FastAPI, Midtrans SDK, webhook handlers"],
            ["GAP-A06", "No API management", "Deploy Kong API Gateway with plugins for auth, rate limiting", "Kong, Docker, PostgreSQL (Kong DB)"],
            ["GAP-A07", "No frontend platform", "Build Next.js application with SSR, PWA, responsive design", "Next.js 14, React 18, TailwindCSS, SWR"],
            ["GAP-A08", "No async processing", "Deploy Celery workers with Redis as broker", "Celery, Redis, Flower (monitoring)"],
            ["GAP-A09", "No event streaming", "Implement event bus for inter-service communication", "Redis Streams / Apache Kafka"],
            ["GAP-A10", "No notification system", "Build Notification Service with multi-channel support", "FastAPI, FCM, SendGrid, Twilio"],
        ],
        title="Gap and Solution Table - Application Architecture",
        table_number=18
    )

    # Transition Timeline - Application
    add_heading(doc, "2.3.3 Transition Timeline - Application", level=3)

    add_table(doc,
        headers=["Fase", "Periode", "Application Milestones"],
        rows=[
            ["Fase 1", "Bulan 1-4", "API Gateway deployed, User Service live, Prediction Service v1 (basic model), Next.js frontend MVP, PostgreSQL operational"],
            ["Fase 2", "Bulan 5-8", "Recommendation Service (DiCE) live, School Dashboard with Anti-Bentrok, Payment Service integrated, Notification Service operational, WebSocket real-time updates"],
            ["Fase 3", "Bulan 9-12", "Full analytics pipeline, ML model v2 (improved accuracy), Admin panel complete, B2B multi-tenant fully operational, Performance optimized for 500K concurrent"],
        ],
        title="Transition Timeline - Application Architecture",
        table_number=19
    )

    # Application Requirements
    add_heading(doc, "2.4 Kebutuhan Aplikasi", level=2)

    add_table(doc,
        headers=["ID", "Kebutuhan", "Rasional", "Prioritas"],
        rows=[
            ["AR-001", "Semua layanan harus menyediakan endpoint health check (/health, /ready)", "Kubernetes liveness/readiness probes untuk pemulihan otomatis", "P1"],
            ["AR-002", "Semua API harus mengikuti spesifikasi OpenAPI 3.0 dengan dokumentasi otomatis", "Pengalaman developer, desain berbasis kontrak, pengujian", "P1"],
            ["AR-003", "Layanan harus stateless (tanpa state lokal, gunakan Redis/DB untuk state)", "Skalabilitas horizontal, kompatibilitas orkestrasi kontainer", "P1"],
            ["AR-004", "Semua layanan harus mengimplementasi structured logging (format JSON)", "Logging terpusat, parsing otomatis, efisiensi debugging", "P1"],
            ["AR-005", "Autentikasi antar-layanan harus menggunakan mTLS atau identitas service mesh", "Keamanan zero trust antar microservices", "P2"],
            ["AR-006", "Frontend harus mencapai skor performa Lighthouse > 90", "Pengalaman pengguna, SEO, performa mobile", "P2"],
            ["AR-007", "Semua layanan harus mengimplementasi pola circuit breaker untuk panggilan eksternal", "Isolasi kegagalan, degradasi yang terkendali", "P1"],
            ["AR-008", "Deployment model ML harus mendukung canary releases (pembagian traffic 10%)", "Deployment model yang aman, kemampuan A/B testing", "P2"],
        ],
        title="Kebutuhan Aplikasi",
        table_number=20
    )

    # Application Principles Updated
    add_heading(doc, "2.5 Prinsip Aplikasi (Diperbarui)", level=2)

    app_principles = [
        {
            "name": "Independently Deployable Services",
            "statement": "Setiap microservice harus dapat di-deploy secara independen tanpa mempengaruhi service lain",
            "rationale": "Tim kecil (4 orang) memerlukan kemampuan deploy frequent tanpa koordinasi rumit antar service.",
            "implications": "Backward compatible APIs, database per service, feature flags, blue-green deployment"
        },
        {
            "name": "Failure Isolation",
            "statement": "Kegagalan pada satu service tidak boleh menyebabkan cascade failure ke service lain",
            "rationale": "Saat peak SNBP, individual service failure tidak boleh membuat seluruh platform down.",
            "implications": "Circuit breakers, bulkhead pattern, timeout policies, fallback responses, async communication preference"
        },
    ]

    for p in app_principles:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # ==========================================================================
    # STATEMENT OF ARCHITECTURE WORK (UPDATED)
    # ==========================================================================
    add_heading(doc, "3. Pernyataan Pekerjaan Arsitektur (Diperbarui)", level=1)

    add_paragraph(doc,
        "Statement of Architecture Work diperbarui setelah penyelesaian Phase C "
        "untuk mencerminkan keputusan arsitektur IS yang telah dibuat."
    )

    add_heading(doc, "3.1 Keputusan Utama dari Arsitektur SI", level=2)

    add_table(doc,
        headers=["Keputusan", "Pilihan", "Rasional"],
        rows=[
            ["Primary Database", "PostgreSQL 15 with PostGIS extension", "Open source, strong JSON support, geospatial capability, proven scalability"],
            ["Cache Layer", "Redis 7", "In-memory speed for feature store, session, and pub/sub capability"],
            ["ML Framework", "XGBoost + LightGBM ensemble with ONNX inference", "Best accuracy for tabular data, ONNX for optimized inference"],
            ["XAI Framework", "DiCE (Diverse Counterfactual Explanations)", "Generates actionable what-if scenarios, integrates with sklearn-compatible models"],
            ["API Framework", "FastAPI (Python)", "High performance async, auto OpenAPI docs, type safety, Python ML ecosystem"],
            ["Frontend Framework", "Next.js 14 (React)", "SSR for SEO, PWA support, great developer experience, large ecosystem"],
            ["Event Streaming", "Redis Streams (initial) -> Kafka (scale)", "Redis Streams for simplicity at start, migrate to Kafka when throughput demands"],
            ["API Gateway", "Kong", "Open source, plugin ecosystem, Kubernetes-native, performance"],
        ],
        title="Keputusan Teknologi Utama dari Arsitektur SI",
        table_number=21
    )

    add_heading(doc, "3.2 Pekerjaan yang Tersisa", level=2)
    add_paragraph(doc,
        "Setelah Phase C (IS Architecture), pekerjaan yang tersisa dalam siklus ADM:"
    )
    add_bullet_list(doc, [
        "Phase D (Technology Architecture): Infrastruktur cloud, containerization, CI/CD, monitoring stack",
        "Phase E (Opportunities & Solutions): Prioritisasi implementasi dan resource allocation",
        "Phase F (Migration Planning): Detail migration plan dan deployment strategy",
        "Phase G (Implementation Governance): Monitoring implementasi dan compliance",
    ])

    # References
    references = [
        "The Open Group. (2022). TOGAF Standard, 10th Edition. The Open Group.",
        "Richards, M., & Ford, N. (2020). Fundamentals of Software Architecture. O'Reilly Media.",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems (2nd ed.). O'Reilly Media.",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.",
        "Richardson, C. (2018). Microservices Patterns. Manning Publications.",
        "Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.",
        "Hohpe, G., & Woolf, B. (2003). Enterprise Integration Patterns. Addison-Wesley.",
        "Chen, L., Ali Babar, M., & Nuseibeh, B. (2013). Characterizing Architecturally Significant Requirements. IEEE Software, 30(2).",
        "Bass, L., Clements, P., & Kazman, R. (2021). Software Architecture in Practice (4th ed.). Addison-Wesley.",
        "Mothukuri, V., et al. (2021). A Survey on Security and Privacy of Federated Learning. Future Generation Computer Systems.",
        "Molnar, C. (2022). Interpretable Machine Learning. Leanpub.",
        "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi.",
        "Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. KDD '16.",
        "Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. NeurIPS 2017.",
        "Mothilal, R. K., Sharma, A., & Tan, C. (2020). Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations. FAT* '20.",
    ]

    add_references(doc, references)

    # Save document
    save_document(doc, "Stage5_IS_Architecture.docx")
    print("Stage 5: Dokumen berhasil di-generate!")
    print(f"Total paragraphs: {len(doc.paragraphs)}")
    print(f"Total tables: {len(doc.tables)}")


if __name__ == "__main__":
    generate_stage5()
