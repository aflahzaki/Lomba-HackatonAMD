"""
Generate Stage 3: Preliminary Phase, Requirement Management, Phase A: Architecture Vision
TOGAF Enterprise Architecture - LangkahKampus EduTech

This script generates the Stage 3 document covering:
- Preliminary Phase (Organizational Model, Architecture Repository)
- Requirements Management (Functional & Non-Functional)
- Phase A: Architecture Vision
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


def generate_stage3():
    """Generate Stage 3: Preliminary Phase, Requirement Management, Architecture Vision."""
    doc = create_document()

    # Cover Page
    add_cover_page(
        doc,
        title="Fase Preliminary, Manajemen Kebutuhan & Visi Arsitektur",
        stage_name="Stage 3 - Preliminary Phase, Manajemen Kebutuhan, Phase A: Architecture Vision"
    )

    # Table of Contents
    toc_sections = [
        ("Preliminary Phase", [
            "Model Organisasi untuk Enterprise Architecture",
            "Architecture Repository",
        ]),
        ("Manajemen Kebutuhan (Requirements Management)", [
            "Kebutuhan Fungsional",
            "Kebutuhan Non-Fungsional",
        ]),
        ("Phase A: Architecture Vision", [
            "Visi Arsitektur",
            "Rencana Komunikasi",
            "Prinsip Arsitektur",
            "Prinsip Bisnis, Tujuan, dan Pendorong",
            "Pernyataan Pekerjaan Arsitektur",
        ]),
        ("Daftar Pustaka", []),
    ]
    add_table_of_contents(doc, toc_sections)

    # ==========================================================================
    # PART I: PRELIMINARY PHASE
    # ==========================================================================
    add_heading(doc, "1. Preliminary Phase", level=1)

    add_paragraph(doc,
        "Preliminary Phase merupakan tahap persiapan awal dalam siklus TOGAF ADM yang "
        "bertujuan untuk mendefinisikan kerangka kerja dan prinsip-prinsip yang akan "
        "menjadi panduan dalam pengembangan arsitektur enterprise LangkahKampus. Pada "
        "fase ini, tim arsitektur menetapkan struktur organisasi yang terlibat, "
        "mendefinisikan peran dan tanggung jawab, serta membangun fondasi governance "
        "yang diperlukan untuk memastikan keberhasilan proyek arsitektur enterprise."
    )

    # 1.1 Organizational Model for EA
    add_heading(doc, "1.1 Model Organisasi untuk Enterprise Architecture", level=2)

    add_paragraph(doc,
        "Model organisasi untuk Enterprise Architecture pada LangkahKampus dirancang "
        "untuk mengakomodasi kebutuhan startup EduTech yang beroperasi dalam ekosistem "
        "pendidikan Indonesia. Struktur ini mempertimbangkan keterlibatan berbagai "
        "pemangku kepentingan mulai dari tim internal pengembangan hingga mitra "
        "sekolah dan pengguna akhir."
    )

    # Impacted Organization Units
    add_heading(doc, "1.1.1 Unit Organisasi yang Terdampak", level=3)

    add_paragraph(doc,
        "Diagram unit organisasi yang terdampak dalam inisiatif Enterprise Architecture "
        "LangkahKampus dikelompokkan menjadi empat kategori berdasarkan tingkat "
        "keterlibatan dan dampak yang diterima:"
    )

    add_paragraph(doc, "A. Core (Inti):", bold=True)
    add_bullet_list(doc, [
        "Product Development Division - Tim pengembangan produk yang bertanggung jawab atas desain dan implementasi platform LangkahKampus",
        "Machine Learning Engineering - Tim yang mengembangkan dan memelihara model prediksi (XGBoost + LightGBM ensemble) dan sistem rekomendasi DiCE XAI",
        "Data Engineering - Tim yang mengelola pipeline data, integrasi data sekolah, dan infrastructure data warehouse",
        "Platform Engineering - Tim yang mengelola infrastruktur teknis termasuk deployment, monitoring, dan DevOps",
    ])

    add_paragraph(doc, "B. Soft (Pendukung):", bold=True)
    add_bullet_list(doc, [
        "Marketing & Growth - Tim pemasaran yang mengelola akuisisi pengguna B2C dan B2B",
        "Customer Success - Tim yang memastikan kepuasan pengguna dan retensi pelanggan sekolah",
        "Business Development - Tim yang mengembangkan kemitraan dengan sekolah dan institusi pendidikan",
        "Finance & Operations - Tim yang mengelola keuangan, pembayaran, dan operasional perusahaan",
    ])

    add_paragraph(doc, "C. Extended (Diperluas):", bold=True)
    add_bullet_list(doc, [
        "Penyedia Data Pendidikan - LTMPT, Kemendikbudristek, dan BPS sebagai sumber data SNBP",
        "Payment Gateway Partners - Mitra pembayaran (Midtrans, Xendit) untuk transaksi freemium",
        "Cloud Service Providers - Penyedia infrastruktur hosting dan ML serving",
    ])

    add_paragraph(doc, "D. Communities (Komunitas):", bold=True)
    add_bullet_list(doc, [
        "Siswa SMA/MA/SMK - Pengguna utama layanan prediksi dan rekomendasi SNBP",
        "Guru - Evaluator pasif yang di-invite siswa untuk melihat profil dan memberikan komentar",
        "Orang Tua/Wali - Pemangku kepentingan yang berkepentingan terhadap keberhasilan pendidikan anak",
    ])

    # Description of Impacts Table
    add_heading(doc, "1.1.2 Deskripsi Dampak", level=3)

    add_paragraph(doc,
        "Tabel berikut menjelaskan dampak yang diterima oleh setiap unit organisasi "
        "akibat implementasi Enterprise Architecture pada LangkahKampus:"
    )

    add_table(doc,
        headers=["Unit Organisasi", "Kategori", "Dampak", "Tingkat Dampak"],
        rows=[
            ["Product Development", "Core", "Restrukturisasi proses pengembangan sesuai arsitektur target, adopsi halaman prediksi all-in-one", "Tinggi"],
            ["ML Engineering", "Core", "Standarisasi pipeline ML, implementasi MLOps, integrasi model serving dengan platform PHP", "Tinggi"],
            ["Data Engineering", "Core", "Migrasi ke arsitektur data terpusat, implementasi data governance, referral tracking", "Tinggi"],
            ["Platform Engineering", "Core", "Pengelolaan infrastruktur PHP hosting, CI/CD pipeline, observability stack", "Tinggi"],
            ["Marketing & Growth", "Soft", "Integrasi dengan referral system untuk pertumbuhan organik, kampanye viral loop", "Sedang"],
            ["Customer Success", "Soft", "Akses ke monitoring pengguna, dukungan onboarding wizard, panduan referral", "Sedang"],
            ["Penyedia Data", "Extended", "Standardisasi format data exchange, compliance terhadap data governance", "Rendah"],
            ["Siswa", "Communities", "Pengalaman pengguna yang lebih baik melalui all-in-one prediction dan onboarding yang intuitif", "Rendah"],
            ["Guru", "Communities", "Akses evaluatif ke profil dan prediksi siswa yang mengundang mereka", "Sedang"],
        ],
        title="Deskripsi Dampak per Unit Organisasi",
        table_number=1
    )

    # List of Roles
    add_heading(doc, "1.1.3 Daftar Peran", level=3)

    add_paragraph(doc,
        "Berikut adalah daftar peran yang terlibat dalam pengembangan dan pengelolaan "
        "Enterprise Architecture LangkahKampus beserta tanggung jawab masing-masing:"
    )

    add_table(doc,
        headers=["Peran/Kelompok", "Tanggung Jawab"],
        rows=[
            ["Chief Executive Officer (CEO)", "Memberikan arahan strategis, menyetujui visi arsitektur, memastikan keselarasan dengan tujuan bisnis"],
            ["Chief Technology Officer (CTO)", "Memimpin inisiatif EA, mengambil keputusan teknis strategis, mengelola tim teknologi"],
            ["Enterprise Architect", "Merancang dan memelihara arsitektur enterprise, memastikan konsistensi dan kepatuhan terhadap standar"],
            ["ML Engineering Lead", "Mengelola arsitektur ML pipeline, model governance, dan MLOps practices"],
            ["Data Architect", "Merancang arsitektur data, data governance, dan standar integrasi data"],
            ["Solution Architect", "Menerjemahkan kebutuhan bisnis menjadi solusi teknis, merancang komponen sistem"],
            ["Frontend Lead (Next.js)", "Memimpin pengembangan UI/UX platform, memastikan responsiveness dan accessibility"],
            ["Backend Lead (FastAPI)", "Memimpin pengembangan API dan microservices, memastikan skalabilitas"],
            ["DevOps Engineer", "Mengelola infrastruktur cloud, CI/CD, monitoring, dan deployment"],
            ["Product Manager", "Mendefinisikan roadmap produk, memprioritaskan fitur berdasarkan kebutuhan pengguna"],
            ["Quality Assurance Lead", "Memastikan kualitas produk melalui testing strategy dan automation"],
            ["Security Officer", "Memastikan kepatuhan terhadap standar keamanan dan regulasi PDPA"],
            ["Guru BK Liaison", "Menjembatani kebutuhan guru evaluator dengan tim pengembangan"],
        ],
        title="Daftar Peran dalam Enterprise Architecture",
        table_number=2
    )

    # RACI Matrix
    add_heading(doc, "1.1.4 RACI Matrix", level=3)

    add_paragraph(doc,
        "RACI Matrix berikut mendefinisikan tingkat keterlibatan setiap peran dalam "
        "aktivitas Enterprise Architecture. R = Responsible (pelaksana), A = Accountable "
        "(penanggung jawab), C = Consulted (dikonsultasikan), I = Informed (diinformasikan)."
    )

    add_table(doc,
        headers=["Aktivitas EA", "CEO", "CTO", "EA", "ML Lead", "Data Arch", "Sol. Arch", "Product Mgr", "DevOps"],
        rows=[
            ["Definisi Visi Arsitektur", "A", "R", "R", "C", "C", "C", "C", "I"],
            ["Pengembangan Architecture Principles", "I", "A", "R", "C", "C", "C", "C", "I"],
            ["Business Architecture Design", "C", "A", "R", "I", "I", "C", "R", "I"],
            ["Data Architecture Design", "I", "A", "R", "C", "R", "C", "C", "I"],
            ["Application Architecture Design", "I", "A", "R", "R", "C", "R", "C", "C"],
            ["Technology Architecture Design", "I", "A", "R", "C", "C", "R", "I", "R"],
            ["Gap Analysis", "I", "A", "R", "C", "C", "C", "C", "C"],
            ["Migration Planning", "A", "R", "R", "C", "C", "C", "C", "R"],
            ["Governance Review", "A", "R", "R", "I", "I", "I", "I", "I"],
            ["Stakeholder Communication", "R", "R", "R", "I", "I", "I", "R", "I"],
            ["Security & Compliance", "I", "A", "C", "C", "C", "C", "I", "R"],
            ["ML Model Governance", "I", "A", "C", "R", "C", "C", "C", "I"],
        ],
        title="RACI Matrix Enterprise Architecture LangkahKampus",
        table_number=3
    )

    # Governance Structure
    add_heading(doc, "1.1.5 Struktur Governance", level=3)

    add_paragraph(doc,
        "Struktur governance Enterprise Architecture LangkahKampus dirancang untuk "
        "memastikan bahwa keputusan arsitektur dibuat secara terstruktur, transparan, "
        "dan selaras dengan tujuan strategis organisasi. Governance structure terdiri "
        "dari beberapa tingkatan:"
    )

    add_paragraph(doc, "Tingkat 1: Architecture Board (Strategic)", bold=True)
    add_paragraph(doc,
        "Architecture Board terdiri dari CEO, CTO, dan Enterprise Architect yang "
        "bertanggung jawab atas keputusan strategis arsitektur. Board ini melakukan "
        "review triwulanan terhadap keselarasan arsitektur dengan strategi bisnis, "
        "menyetujui perubahan major pada arsitektur, dan mengelola resource allocation "
        "untuk inisiatif arsitektur."
    )

    add_paragraph(doc, "Tingkat 2: Architecture Review Committee (Tactical)", bold=True)
    add_paragraph(doc,
        "Komite review terdiri dari Solution Architect, ML Lead, Data Architect, "
        "dan DevOps Lead yang melakukan review mingguan terhadap proposal perubahan "
        "arsitektur. Komite ini memastikan bahwa setiap perubahan sesuai dengan "
        "prinsip arsitektur yang telah ditetapkan dan tidak menimbulkan technical debt "
        "yang tidak terkelola."
    )

    add_paragraph(doc, "Tingkat 3: Implementation Teams (Operational)", bold=True)
    add_paragraph(doc,
        "Tim implementasi terdiri dari developer, data engineer, dan ML engineer "
        "yang melaksanakan perubahan sesuai dengan panduan arsitektur. Tim ini "
        "melaporkan compliance terhadap standar arsitektur melalui automated checks "
        "dalam CI/CD pipeline dan code review processes."
    )

    add_paragraph(doc, "Mekanisme Governance:", bold=True)
    add_bullet_list(doc, [
        "Architecture Decision Records (ADR) - Dokumentasi setiap keputusan arsitektur signifikan",
        "Architecture Compliance Review - Review berkala terhadap kepatuhan implementasi",
        "Exception Management Process - Proses formal untuk deviasi dari standar arsitektur",
        "Architecture Maturity Assessment - Evaluasi tahunan tingkat kematangan arsitektur",
        "Continuous Improvement Cycle - Feedback loop untuk perbaikan berkelanjutan",
    ])

    # 1.2 Architecture Repository
    add_heading(doc, "1.2 Architecture Repository", level=2)

    add_paragraph(doc,
        "Architecture Repository LangkahKampus berfungsi sebagai tempat penyimpanan "
        "terpusat untuk semua artefak arsitektur yang dihasilkan selama siklus ADM. "
        "Repository ini dikelompokkan ke dalam enam kelas dokumen sesuai dengan "
        "standar TOGAF:"
    )

    add_table(doc,
        headers=["Kelas Dokumen", "Deskripsi", "Contoh Dokumen LangkahKampus"],
        rows=[
            ["Architecture Metamodel", "Mendefinisikan struktur dan hubungan antara berbagai jenis artefak arsitektur", "LangkahKampus EA Metamodel, Entity Relationship definitions, Artifact taxonomy"],
            ["Architecture Capability", "Mendokumentasikan kemampuan organisasi dalam melaksanakan EA", "EA Team Skills Matrix, EA Tools & Infrastructure, EA Maturity Assessment Report"],
            ["Architecture Landscape", "Menyimpan arsitektur baseline dan target di semua domain", "Business Architecture Models, Data Architecture Diagrams, Application Portfolio, Technology Standards Catalog"],
            ["Standards Information Base (SIB)", "Berisi standar teknis dan regulasi yang harus dipatuhi", "API Design Standards, Security Standards (PDPA), Coding Standards, Cloud Architecture Standards"],
            ["Reference Library", "Menyimpan referensi, template, dan best practices", "TOGAF ADM Templates, Industry Best Practices (EduTech), Design Patterns Library, ML Pipeline Templates"],
            ["Governance Log", "Mencatat semua keputusan governance dan compliance", "Architecture Decision Records (ADR), Compliance Assessment Reports, Exception Logs, Change Requests"],
        ],
        title="Kelas Dokumen Architecture Repository",
        table_number=4
    )

    # ==========================================================================
    # PART II: REQUIREMENTS MANAGEMENT
    # ==========================================================================
    add_heading(doc, "2. Manajemen Kebutuhan (Requirements Management)", level=1)

    add_paragraph(doc,
        "Requirements Management dalam konteks TOGAF ADM merupakan proses yang "
        "berjalan secara kontinyu sepanjang siklus arsitektur. Pada LangkahKampus, "
        "pengelolaan kebutuhan mencakup identifikasi, dokumentasi, dan prioritisasi "
        "kebutuhan fungsional dan non-fungsional yang menjadi dasar perancangan "
        "arsitektur enterprise."
    )

    # 2.1 Functional Requirements
    add_heading(doc, "2.1 Kebutuhan Fungsional", level=2)

    add_paragraph(doc,
        "Kebutuhan fungsional mendefinisikan apa yang harus dilakukan oleh sistem "
        "LangkahKampus. Berikut adalah kebutuhan fungsional yang diidentifikasi "
        "berdasarkan analisis kebutuhan pengguna dan tujuan bisnis:"
    )

    add_table(doc,
        headers=["ID", "Kategori", "Kebutuhan Fungsional", "Prioritas", "Stakeholder"],
        rows=[
            ["FR-001", "Autentikasi", "Sistem harus menyediakan registrasi dan login menggunakan email atau nomor telepon dengan pilihan peran Siswa atau Guru", "Tinggi", "Siswa, Guru"],
            ["FR-002", "Onboarding", "Sistem harus menyediakan onboarding wizard bertahap (3 langkah: data sekolah, nilai rapor, pilihan prodi impian) setelah registrasi siswa", "Tinggi", "Siswa"],
            ["FR-003", "Prediksi All-in-One", "Sistem harus menampilkan hasil prediksi terintegrasi: probabilitas (gauge), peringatan Choice-2 Trap, statistik Anti-Bentrok peer, dan rekomendasi alternatif dalam satu halaman", "Tinggi", "Siswa"],
            ["FR-004", "Model Freemium", "Sistem harus membatasi prediksi gratis sebanyak 3 kali per siswa, lalu menampilkan opsi pembayaran atau referral", "Tinggi", "Siswa"],
            ["FR-005", "Referral System", "Sistem harus mampu menghasilkan referral link unik per siswa dan melacak 5 klik IP unik untuk membuka 3 prediksi tambahan", "Tinggi", "Siswa"],
            ["FR-006", "Guru (Invite Code)", "Sistem harus memungkinkan siswa mengundang guru via kode 6 karakter (maks 2 guru per siswa), dan guru dapat melihat profil + prediksi siswa serta memberikan komentar", "Tinggi", "Siswa, Guru"],
            ["FR-007", "Payment Gateway", "Sistem harus mengintegrasikan pembayaran untuk pembelian paket prediksi (Rp15.000-25.000 per prediksi)", "Tinggi", "Siswa"],
            ["FR-008", "Peta Universitas", "Sistem harus menyediakan mode eksplorasi Peta Universitas dengan tombol 'Prediksi Langsung' di setiap detail program studi", "Sedang", "Siswa"],
            ["FR-009", "What-If Analysis", "Sistem harus memungkinkan siswa melakukan simulasi skenario dengan mengubah parameter input dan melihat dampaknya terhadap prediksi", "Sedang", "Siswa"],
            ["FR-010", "Dashboard Profil", "Sistem harus menyediakan profil terintegrasi di dashboard siswa dengan kemampuan edit data akademik inline", "Sedang", "Siswa"],
            ["FR-011", "Visualisasi Data", "Sistem harus menampilkan visualisasi statistik penerimaan dan perbandingan antar program studi/universitas", "Sedang", "Siswa"],
            ["FR-012", "Notifikasi", "Sistem harus mampu mengirimkan notifikasi terkait status referral, batas prediksi, dan update platform", "Rendah", "Siswa, Guru"],
        ],
        title="Daftar Kebutuhan Fungsional",
        table_number=5
    )

    # 2.2 Non-Functional Requirements
    add_heading(doc, "2.2 Kebutuhan Non-Fungsional", level=2)

    add_paragraph(doc,
        "Kebutuhan non-fungsional mendefinisikan kualitas dan batasan yang harus "
        "dipenuhi oleh sistem LangkahKampus untuk memastikan pengalaman pengguna "
        "yang optimal dan operasional yang andal."
    )

    add_table(doc,
        headers=["ID", "Kategori", "Kebutuhan Non-Fungsional", "Metrik Target", "Prioritas"],
        rows=[
            ["NFR-001", "Performance", "Response time untuk prediksi ML harus kurang dari 2 detik end-to-end", "< 2 detik (p95)", "Tinggi"],
            ["NFR-002", "Scalability", "Sistem harus mampu melayani 500.000 concurrent users saat peak SNBP season (Januari-Februari)", "500K concurrent users", "Tinggi"],
            ["NFR-003", "Availability", "Platform harus tersedia 99.9% uptime (max downtime 8.76 jam/tahun)", "99.9% SLA", "Tinggi"],
            ["NFR-004", "Security", "Sistem harus comply dengan UU PDP (Perlindungan Data Pribadi) Indonesia dan standar keamanan OWASP Top 10", "Zero critical vulnerabilities", "Tinggi"],
            ["NFR-005", "Data Privacy", "Data pribadi siswa harus dienkripsi at-rest dan in-transit, dengan retention policy yang jelas", "AES-256, TLS 1.3", "Tinggi"],
            ["NFR-006", "Usability", "Platform harus mencapai SUS (System Usability Scale) score minimal 80 untuk target pengguna siswa SMA", "SUS >= 80", "Sedang"],
            ["NFR-007", "Reliability", "ML model prediction accuracy harus di atas 85% berdasarkan historical validation", "> 85% accuracy", "Tinggi"],
            ["NFR-008", "Maintainability", "Codebase harus memiliki test coverage minimal 80% dan dokumentasi API lengkap", ">= 80% coverage", "Sedang"],
            ["NFR-009", "Portability", "Sistem harus deployable di multiple cloud providers tanpa vendor lock-in signifikan", "Container-based deployment", "Rendah"],
            ["NFR-010", "Disaster Recovery", "RPO (Recovery Point Objective) < 1 jam dan RTO (Recovery Time Objective) < 4 jam", "RPO < 1hr, RTO < 4hr", "Sedang"],
        ],
        title="Daftar Kebutuhan Non-Fungsional",
        table_number=6
    )

    # ==========================================================================
    # PART III: PHASE A - ARCHITECTURE VISION
    # ==========================================================================
    add_heading(doc, "3. Phase A: Architecture Vision", level=1)

    add_paragraph(doc,
        "Phase A dalam TOGAF ADM bertujuan untuk mengembangkan visi arsitektur "
        "tingkat tinggi yang akan menjadi panduan seluruh pengembangan arsitektur "
        "enterprise LangkahKampus. Visi ini mencakup identifikasi masalah, "
        "penetapan tujuan, analisis stakeholder, dan perancangan konsep solusi."
    )

    # 3.1 Architecture Vision
    add_heading(doc, "3.1 Visi Arsitektur", level=2)

    # Problem Descriptions
    add_heading(doc, "3.1.1 Deskripsi Permasalahan", level=3)

    add_paragraph(doc, "A. Latar Belakang Masalah:", bold=True)
    add_paragraph(doc,
        "Seleksi Nasional Berdasarkan Prestasi (SNBP) merupakan jalur penerimaan "
        "mahasiswa baru yang menggunakan nilai rapor sebagai dasar seleksi. Setiap "
        "tahunnya, lebih dari 1,5 juta siswa SMA/MA/SMK di Indonesia bersaing "
        "memperebutkan kuota SNBP yang terbatas. Permasalahan fundamental yang dihadapi "
        "adalah adanya 'Choice-2 Trap' di mana siswa yang tidak optimal dalam memilih "
        "pilihan kedua justru mengurangi peluang keseluruhan mereka untuk diterima."
    )
    add_paragraph(doc,
        "Selain itu, terdapat asimetri informasi yang signifikan antara siswa di "
        "kota besar dengan siswa di daerah terpencil. Siswa di kota besar memiliki "
        "akses ke bimbingan belajar dan informasi yang lebih baik, sementara siswa "
        "di daerah seringkali membuat keputusan berdasarkan informasi yang tidak "
        "lengkap atau bahkan keliru. Guru BK di sekolah juga menghadapi tantangan "
        "dalam mengelola rekomendasi untuk ratusan siswa tanpa tools yang memadai, "
        "sering kali mengakibatkan bentrokan pilihan dalam satu sekolah."
    )

    add_paragraph(doc, "B. Pendorong Perubahan (Change Drivers):", bold=True)
    add_bullet_list(doc, [
        "Digitalisasi Pendidikan - Kebijakan Kemendikbudristek yang mendorong transformasi digital di sektor pendidikan",
        "Peningkatan Jumlah Peserta SNBP - Pertumbuhan 12% per tahun dalam jumlah pendaftar SNBP memerlukan solusi scalable",
        "Ketersediaan Data Historis - Akumulasi data penerimaan SNBP selama bertahun-tahun memungkinkan prediksi berbasis ML",
        "Ekspektasi Digital Native - Generasi Z mengharapkan layanan digital yang personal dan real-time",
        "Regulasi PDP - UU Perlindungan Data Pribadi Indonesia mendorong pengelolaan data siswa yang lebih baik",
        "Kompetisi Pasar - Munculnya berbagai platform edukasi memerlukan diferensiasi melalui teknologi advanced",
    ])

    add_paragraph(doc, "C. Peluang (Opportunities):", bold=True)
    add_bullet_list(doc, [
        "Total Addressable Market (TAM) lebih dari 3 juta siswa SMA per tahun yang berpotensi menggunakan SNBP",
        "Belum ada platform yang secara khusus menyelesaikan masalah Choice-2 Trap dengan pendekatan ML",
        "Potensi B2B yang besar dengan lebih dari 40.000 SMA/MA/SMK di Indonesia",
        "Kemampuan ML dan XAI (Explainable AI) yang masih jarang diaplikasikan di sektor EduTech Indonesia",
        "Peluang ekspansi ke jalur seleksi lain (SNBT, mandiri) dan jenjang pendidikan lain",
    ])

    # Architecture Objectives
    add_heading(doc, "3.1.2 Tujuan Arsitektur", level=3)

    add_paragraph(doc, "A. Tujuan Bisnis:", bold=True)
    add_numbered_list(doc, [
        "Menyediakan platform prediksi SNBP all-in-one yang akurat (>85%) dan terpercaya untuk siswa SMA/MA/SMK di seluruh Indonesia",
        "Menghilangkan asimetri informasi dalam pemilihan program studi melalui rekomendasi berbasis data dan XAI",
        "Membangun pertumbuhan organik melalui viral referral loop yang memberikan insentif prediksi gratis",
        "Mencapai 100.000 pengguna aktif pada tahun pertama melalui model freemium dengan 3 prediksi gratis",
        "Menghasilkan revenue yang sustainable melalui konversi freemium ke pembayaran dan referral engagement",
    ])

    add_paragraph(doc, "B. Kebutuhan Arsitektur:", bold=True)
    add_numbered_list(doc, [
        "Arsitektur PHP monolith yang bersih dengan pemisahan concerns antara halaman, API, dan ML service",
        "Skalabilitas untuk menghadapi traffic spike saat peak season SNBP",
        "Sistem referral tracking dengan validasi IP unik yang tahan terhadap penyalahgunaan",
        "ML model serving infrastructure yang mendukung prediksi all-in-one dalam satu request",
        "Data architecture yang mendukung compliance terhadap UU PDP Indonesia",
        "Onboarding wizard yang intuitif dengan state management yang persisten",
    ])

    add_paragraph(doc, "C. Diagram Konsep Solusi:", bold=True)
    add_paragraph(doc,
        "Solution Concept Diagram LangkahKampus menggambarkan arsitektur tingkat "
        "tinggi yang terdiri dari beberapa layer utama: (1) Presentation Layer - "
        "PHP 8.x web application yang responsive untuk siswa dan guru; (2) API "
        "Layer - endpoint PHP untuk autentikasi, referral tracking, dan business "
        "logic; (3) ML Integration Layer - FastAPI microservice untuk model inference "
        "yang dipanggil oleh backend PHP; (4) Data Layer - MySQL/PostgreSQL untuk "
        "transactional data termasuk referral_tracking, predictions, dan user "
        "profiles; (5) Payment Layer - integrasi dengan Midtrans/Xendit untuk "
        "pemrosesan pembayaran freemium."
    )

    # Stakeholders Table
    add_heading(doc, "3.1.3 Stakeholder", level=3)

    add_paragraph(doc,
        "Identifikasi stakeholder merupakan langkah krusial untuk memastikan bahwa "
        "arsitektur yang dirancang memenuhi kebutuhan semua pihak yang berkepentingan. "
        "Berikut adalah daftar stakeholder LangkahKampus:"
    )

    add_table(doc,
        headers=["Peran/Kelompok", "Nama", "Tanggung Jawab", "Perhatian Utama", "Kelas", "Deliverables"],
        rows=[
            ["CEO/Founder", "Aflah Rafilah Zaki", "Strategi bisnis, visi produk, fundraising", "ROI, market penetration, competitive advantage", "Key Player", "Business strategy document, investor reports"],
            ["CTO", "Azka Fathir Syarif", "Keputusan teknis, arsitektur sistem, tim engineering", "Scalability, technical debt, team productivity", "Key Player", "Architecture documents, technical roadmap"],
            ["ML Lead", "Daffa Rizky Herdiawan", "Model development, MLOps, prediction accuracy", "Model accuracy, training data quality, inference speed", "Key Player", "ML pipeline docs, model performance reports"],
            ["Product Manager", "Muhammad Arifin Ilham", "Product roadmap, user research, feature prioritization", "User satisfaction, feature adoption, market fit", "Key Player", "Product requirements, user stories"],
            ["Siswa SMA", "1.5 juta+ siswa SNBP per tahun", "Menggunakan platform untuk prediksi dan rekomendasi", "Akurasi prediksi, kemudahan penggunaan, harga terjangkau", "Subject", "User guides, prediction results"],
            ["Guru", "Guru yang di-invite siswa via kode unik", "Melihat profil dan prediksi siswa, memberikan komentar evaluatif", "Kemudahan akses, informasi yang relevan, tidak membebani waktu", "Subject", "Notifikasi invite, panduan penggunaan"],
            ["Orang Tua", "Orang tua/wali siswa", "Mendampingi dan membiayai proses SNBP anak", "Transparansi, keamanan data anak, value for money", "Interested", "Information reports"],
            ["Kemendikbudristek", "Regulator pendidikan", "Regulasi dan kebijakan SNBP", "Compliance, fairness, data privacy", "Context Setter", "Compliance reports"],
            ["Investor", "Angel investor / VC", "Pendanaan dan mentoring", "Growth metrics, unit economics, scalability", "Interested", "Financial reports, growth dashboards"],
        ],
        title="Tabel Stakeholder",
        table_number=7
    )

    # Stakeholder Contact Table
    add_heading(doc, "3.1.4 Tabel Kontak Stakeholder", level=3)

    add_table(doc,
        headers=["Stakeholder", "Nama Kontak", "Peran", "Metode Komunikasi", "Frekuensi"],
        rows=[
            ["CEO/Founder", "Aflah Rafilah Zaki", "Sponsor Proyek", "Meeting langsung, email", "Mingguan"],
            ["CTO", "Azka Fathir Syarif", "Architecture Owner", "Daily standup, Slack", "Harian"],
            ["ML Lead", "Daffa Rizky Herdiawan", "Technical Lead ML", "Sprint review, Slack", "Mingguan"],
            ["Product Manager", "Muhammad Arifin Ilham", "Requirements Owner", "Sprint planning, email", "Mingguan"],
            ["Perwakilan Siswa", "Focus Group (10 siswa)", "User Representative", "User interview, survey", "Bulanan"],
            ["Perwakilan Guru", "Guru pilot (evaluator)", "School User Rep", "Workshop, video call", "Dua mingguan"],
            ["Investor", "TBD", "Financial Stakeholder", "Board meeting, report", "Triwulanan"],
        ],
        title="Tabel Kontak Stakeholder",
        table_number=8
    )

    # Constraints on Architecture Work
    add_heading(doc, "3.1.5 Batasan Pekerjaan Arsitektur", level=3)

    add_paragraph(doc,
        "Berikut adalah batasan-batasan yang mempengaruhi pekerjaan arsitektur "
        "pada proyek LangkahKampus:"
    )

    add_table(doc,
        headers=["No", "Batasan", "Deskripsi", "Dampak"],
        rows=[
            ["1", "Budget Terbatas", "Sebagai startup early-stage, budget pengembangan terbatas pada seed funding", "Harus memilih solusi cost-effective, prioritas fitur berbasis MVP"],
            ["2", "Timeline SNBP", "Sistem harus siap sebelum periode pendaftaran SNBP (Januari-Februari)", "Development cycle harus mengikuti calendar akademik"],
            ["3", "Regulasi PDP", "Harus comply dengan UU PDP No. 27/2022 tentang Perlindungan Data Pribadi", "Arsitektur harus include data protection by design"],
            ["4", "Keterbatasan Data Historis", "Data penerimaan SNBP tidak dipublikasikan secara resmi oleh LTMPT", "Perlu strategi crowdsourcing dan data partnership"],
            ["5", "Tim Kecil", "Tim engineering terdiri dari 4 orang multi-fungsi", "Arsitektur harus manageable, hindari over-engineering"],
            ["6", "Konektivitas Pengguna", "Banyak siswa di daerah memiliki koneksi internet terbatas", "Platform harus lightweight dan progressive web app ready"],
            ["7", "Integrasi Beragam", "Sistem informasi sekolah sangat bervariasi (dari manual hingga digital)", "Arsitektur integrasi harus fleksibel dan multi-mode"],
        ],
        title="Batasan Pekerjaan Arsitektur",
        table_number=9
    )

    # 3.2 Communication Plan
    add_heading(doc, "3.2 Rencana Komunikasi", level=2)

    add_heading(doc, "3.2.1 Kebutuhan Komunikasi Stakeholder", level=3)

    add_paragraph(doc,
        "Rencana komunikasi bertujuan untuk memastikan bahwa semua stakeholder "
        "mendapatkan informasi yang tepat, pada waktu yang tepat, melalui media "
        "yang tepat. Kebutuhan komunikasi diidentifikasi berdasarkan class "
        "stakeholder dan tingkat keterlibatan mereka."
    )

    add_bullet_list(doc, [
        "Key Players (CEO, CTO, ML Lead, PM) - Membutuhkan update detail tentang progress arsitektur, keputusan teknis, dan blockers secara real-time",
        "Subjects (Siswa, Guru) - Membutuhkan informasi tentang fitur baru, perubahan platform, dan panduan penggunaan",
        "Interested Parties (Orang Tua, Investor) - Membutuhkan laporan periodik tentang progress dan milestone achievements",
        "Context Setters (Regulator) - Membutuhkan compliance reports dan dokumentasi kebijakan data",
    ])

    # Communication Matrix
    add_heading(doc, "3.2.2 Matriks Komunikasi", level=3)

    add_table(doc,
        headers=["Stakeholder", "Informasi yang Dikomunikasikan", "Media", "Frekuensi", "Penanggung Jawab"],
        rows=[
            ["Architecture Board", "Architecture decisions, progress report, risk updates", "Meeting tatap muka / video call", "Mingguan", "Enterprise Architect"],
            ["Development Team", "Sprint backlog, technical decisions, architecture guidelines", "Daily standup, Slack, Confluence", "Harian", "CTO"],
            ["Siswa (End User)", "Feature updates, maintenance schedule, tips penggunaan", "In-app notification, email, social media", "Per release / bulanan", "Product Manager"],
            ["Guru", "Panduan penggunaan, notifikasi undangan siswa", "Email, in-app notification", "Per release", "Product Manager"],
            ["Investor", "KPI dashboard, financial report, milestone progress", "Board meeting, investor deck", "Triwulanan", "CEO"],
            ["Regulator", "Compliance status, data protection measures", "Formal report", "Tahunan / on-demand", "Security Officer"],
        ],
        title="Matriks Komunikasi",
        table_number=10
    )

    # Delivery Vehicles
    add_heading(doc, "3.2.3 Sarana Penyampaian (Delivery Vehicles)", level=3)

    add_paragraph(doc,
        "Sarana penyampaian menentukan saluran dan format yang digunakan untuk "
        "menyampaikan informasi arsitektur kepada berbagai stakeholder:"
    )

    add_table(doc,
        headers=["Sarana", "Deskripsi", "Target Audiens", "Format"],
        rows=[
            ["Architecture Wiki", "Dokumentasi arsitektur terpusat menggunakan Confluence/Notion", "Internal team", "Web-based, diagrams, text"],
            ["Sprint Review", "Demo progress dan review arsitektur setiap 2 minggu", "Development team, PM", "Presentasi, live demo"],
            ["Architecture Decision Record", "Dokumentasi formal setiap keputusan arsitektur signifikan", "All technical stakeholders", "Structured document (template)"],
            ["Newsletter Platform", "Update bulanan tentang fitur dan perubahan platform", "Siswa, Guru BK, Orang Tua", "Email HTML, in-app"],
            ["API Documentation Portal", "Dokumentasi teknis API untuk integrasi sekolah", "Developer sekolah, partners", "Swagger/OpenAPI, web portal"],
            ["Board Report", "Laporan formal progress dan keuangan", "Investor, Board", "PDF presentation"],
            ["Training Workshop", "Sesi pelatihan penggunaan dashboard untuk Guru BK", "Guru BK", "Video call, hands-on"],
            ["Status Dashboard", "Real-time monitoring system health dan KPI", "CTO, DevOps", "Grafana dashboard"],
        ],
        title="Sarana Penyampaian",
        table_number=11
    )

    # 3.3 Architecture Principles
    add_heading(doc, "3.3 Prinsip Arsitektur", level=2)

    add_paragraph(doc,
        "Architecture Principles merupakan aturan dan pedoman umum yang menginformasikan "
        "dan mendukung cara organisasi memenuhi misinya. Prinsip-prinsip berikut "
        "dikelompokkan berdasarkan domain arsitektur TOGAF."
    )

    # Business Principles
    add_heading(doc, "3.3.1 Prinsip Bisnis", level=3)

    principles_business = [
        {
            "name": "Democratize Education Access",
            "statement": "Platform harus mendemokratisasi akses informasi pendidikan tinggi untuk semua siswa tanpa memandang lokasi geografis atau status ekonomi",
            "rationale": "Asimetri informasi merupakan masalah utama yang ingin diselesaikan LangkahKampus. Prinsip ini memastikan bahwa arsitektur mendukung akses yang setara.",
            "implications": "Desain UI harus accessible, pricing harus terjangkau, platform harus bekerja di koneksi rendah"
        },
        {
            "name": "Data-Driven Decision Making",
            "statement": "Setiap keputusan bisnis dan rekomendasi kepada pengguna harus didasarkan pada analisis data yang valid dan dapat dipertanggungjawabkan",
            "rationale": "Kepercayaan pengguna bergantung pada akurasi dan transparansi prediksi yang diberikan platform.",
            "implications": "ML model harus di-validate secara berkala, perlu XAI untuk transparansi, data quality harus terjaga"
        },
        {
            "name": "User-Centric Innovation",
            "statement": "Pengembangan fitur harus selalu dimulai dari kebutuhan nyata pengguna (siswa dan Guru BK) yang tervalidasi",
            "rationale": "Sebagai startup, product-market fit merupakan prioritas utama yang hanya dicapai melalui pemahaman mendalam tentang pengguna.",
            "implications": "Diperlukan continuous user research, feedback loop, A/B testing infrastructure"
        },
        {
            "name": "Sustainable Growth",
            "statement": "Pertumbuhan bisnis harus dilakukan secara berkelanjutan dengan menjaga keseimbangan antara akuisisi pengguna dan kualitas layanan",
            "rationale": "Pertumbuhan yang tidak terkendali tanpa infrastruktur yang memadai akan merusak reputasi dan kepercayaan pengguna.",
            "implications": "Capacity planning harus proaktif, feature release harus bertahap, monitoring harus real-time"
        },
    ]

    for p in principles_business:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()  # spacing

    # Data Principles
    add_heading(doc, "3.3.2 Prinsip Data", level=3)

    principles_data = [
        {
            "name": "Data as a Strategic Asset",
            "statement": "Data merupakan aset strategis organisasi yang harus dikelola dengan standar kualitas tinggi dan governance yang ketat",
            "rationale": "Bisnis LangkahKampus bergantung pada kualitas data untuk menghasilkan prediksi yang akurat. Data yang buruk menghasilkan rekomendasi yang salah.",
            "implications": "Diperlukan data quality framework, data cataloging, ownership assignment, regular data audits"
        },
        {
            "name": "Privacy by Design",
            "statement": "Perlindungan data pribadi harus diintegrasikan ke dalam setiap aspek arsitektur sejak tahap perancangan",
            "rationale": "UU PDP Indonesia mewajibkan perlindungan data pribadi. Data siswa merupakan data sensitif yang memerlukan perlindungan ekstra.",
            "implications": "Encryption at-rest dan in-transit wajib, data minimization, consent management, right to be forgotten implementation"
        },
        {
            "name": "Single Source of Truth",
            "statement": "Setiap entitas data harus memiliki satu sumber kebenaran yang otoritatif untuk menghindari inkonsistensi",
            "rationale": "Duplikasi data menyebabkan inkonsistensi yang dapat menghasilkan prediksi keliru dan keputusan bisnis yang salah.",
            "implications": "Master data management, event-driven sync, clear data ownership, referential integrity"
        },
        {
            "name": "Data Accessibility with Governance",
            "statement": "Data harus dapat diakses oleh stakeholder yang berwenang sesuai dengan kebijakan governance yang telah ditetapkan",
            "rationale": "Keseimbangan antara aksesibilitas dan keamanan data diperlukan untuk mendukung operasional dan analitik.",
            "implications": "Role-based access control, audit trails, data classification, access request workflow"
        },
    ]

    for p in principles_data:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # Application Principles
    add_heading(doc, "3.3.3 Prinsip Aplikasi", level=3)

    principles_app = [
        {
            "name": "Loosely Coupled Microservices",
            "statement": "Aplikasi harus dirancang sebagai kumpulan microservices yang loosely coupled sehingga setiap layanan dapat dikembangkan, di-deploy, dan di-scale secara independen",
            "rationale": "Microservices memungkinkan tim kecil bekerja secara paralel, mempercepat development cycle, dan memungkinkan scaling per komponen sesuai kebutuhan.",
            "implications": "API contract harus jelas, service discovery diperlukan, eventual consistency harus ditangani, monitoring per service"
        },
        {
            "name": "API-First Design",
            "statement": "Setiap layanan harus didefinisikan melalui API yang jelas sebelum implementasi dimulai",
            "rationale": "API-first memungkinkan parallel development antara frontend dan backend, serta memudahkan integrasi dengan pihak ketiga (sekolah).",
            "implications": "OpenAPI specification wajib, API versioning strategy, backward compatibility, API documentation otomatis"
        },
        {
            "name": "Explainable AI (XAI)",
            "statement": "Setiap prediksi dan rekomendasi ML harus dapat dijelaskan kepada pengguna dalam bahasa yang mudah dipahami",
            "rationale": "Kepercayaan pengguna terhadap sistem prediksi bergantung pada kemampuan sistem menjelaskan mengapa suatu rekomendasi diberikan.",
            "implications": "DiCE counterfactual integration, SHAP values visualization, recommendation reasoning UI, model interpretability testing"
        },
        {
            "name": "Progressive Enhancement",
            "statement": "Platform harus memberikan pengalaman dasar yang berfungsi di semua kondisi jaringan dan device, dengan fitur enhanced untuk kondisi optimal",
            "rationale": "Pengguna LangkahKampus tersebar di seluruh Indonesia dengan kondisi infrastruktur internet yang beragam.",
            "implications": "PWA implementation, offline-first untuk fitur kritis, lazy loading, adaptive UI berdasarkan network speed"
        },
    ]

    for p in principles_app:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # Technology Principles
    add_heading(doc, "3.3.4 Prinsip Teknologi", level=3)

    principles_tech = [
        {
            "name": "Cloud-Native First",
            "statement": "Seluruh infrastruktur harus dirancang cloud-native menggunakan containers dan orchestration untuk memaksimalkan skalabilitas dan resilience",
            "rationale": "Traffic LangkahKampus sangat seasonal (peak saat SNBP). Cloud-native architecture memungkinkan auto-scaling yang cost-effective.",
            "implications": "Docker containerization wajib, Kubernetes orchestration, stateless services, infrastructure as code"
        },
        {
            "name": "Automation Over Manual Process",
            "statement": "Setiap proses berulang harus diotomasi termasuk testing, deployment, monitoring, dan incident response",
            "rationale": "Dengan tim kecil, automasi merupakan multiplier yang memungkinkan operasional efisien tanpa menambah headcount.",
            "implications": "CI/CD pipeline wajib, automated testing, infrastructure as code, auto-remediation untuk incident umum"
        },
        {
            "name": "Security by Default",
            "statement": "Keamanan harus menjadi default, bukan add-on. Setiap komponen harus aman secara default tanpa konfigurasi tambahan",
            "rationale": "Platform menangani data sensitif siswa. Security breach akan menghancurkan kepercayaan dan dapat melanggar UU PDP.",
            "implications": "Zero trust architecture, secrets management, automated vulnerability scanning, security-focused code review, WAF"
        },
        {
            "name": "Observability as a First-Class Concern",
            "statement": "Setiap komponen sistem harus observable melalui metrics, logs, dan traces yang terstruktur",
            "rationale": "Deteksi dini masalah dan root cause analysis yang cepat merupakan kunci reliability untuk platform yang digunakan ratusan ribu siswa.",
            "implications": "Structured logging, distributed tracing (OpenTelemetry), metric collection (Prometheus), alerting rules, SLO-based monitoring"
        },
    ]

    for p in principles_tech:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # 3.4 Business Principles, Goals, Drivers
    add_heading(doc, "3.4 Prinsip Bisnis, Tujuan, dan Pendorong", level=2)

    add_heading(doc, "3.4.1 Misi", level=3)
    add_paragraph(doc,
        "Misi LangkahKampus adalah mendemokratisasi akses terhadap informasi dan "
        "alat bantu pengambilan keputusan pendidikan tinggi bagi seluruh siswa SMA/MA/SMK "
        "di Indonesia melalui teknologi prediktif dan kecerdasan buatan yang transparan "
        "dan terpercaya. Kami berkomitmen untuk menghilangkan asimetri informasi dalam "
        "proses SNBP dan membantu setiap siswa membuat keputusan yang optimal berdasarkan "
        "data, bukan asumsi."
    )

    add_heading(doc, "3.4.2 Tujuan (Goals)", level=3)
    add_numbered_list(doc, [
        "Menjadi platform prediksi SNBP nomor satu di Indonesia dengan akurasi prediksi tertinggi (>85%)",
        "Menjangkau 500.000 siswa aktif dalam 3 tahun pertama operasional",
        "Mencapai konversi 10% dari pengguna gratis ke pengguna berbayar atau aktif referral",
        "Mencapai Net Promoter Score (NPS) minimal 60 dari pengguna siswa",
        "Membangun sustainable business model dengan break-even pada tahun ketiga",
        "Berkontribusi pada pemerataan akses pendidikan tinggi di Indonesia, terutama untuk siswa di daerah 3T",
    ])

    add_heading(doc, "3.4.3 Pendorong (Drivers)", level=3)
    add_paragraph(doc,
        "Berikut adalah faktor-faktor yang mendorong pengembangan arsitektur enterprise "
        "LangkahKampus:"
    )
    add_bullet_list(doc, [
        "Market Demand - Tingginya kebutuhan akan solusi prediksi SNBP yang akurat dan terjangkau",
        "Technology Advancement - Kemajuan dalam ML, cloud computing, dan XAI yang memungkinkan solusi yang sebelumnya tidak feasible",
        "Regulatory Push - UU PDP dan kebijakan digitalisasi pendidikan yang mendorong adopsi teknologi yang compliant",
        "Competitive Pressure - Kemunculan platform edukasi lain yang mengharuskan diferensiasi melalui teknologi advanced",
        "Social Impact - Komitmen untuk mengurangi kesenjangan akses informasi pendidikan antara kota dan daerah",
        "Scalability Need - Kebutuhan untuk melayani jutaan siswa secara bersamaan selama peak period SNBP",
        "Data Availability - Meningkatnya ketersediaan data pendidikan yang dapat dimanfaatkan untuk ML",
    ])

    # 3.5 Statement of Architecture Work
    add_heading(doc, "3.5 Pernyataan Pekerjaan Arsitektur", level=2)

    add_heading(doc, "3.5.1 Latar Belakang Proyek", level=3)
    add_paragraph(doc,
        "Proyek Enterprise Architecture LangkahKampus diinisiasi untuk memberikan "
        "landasan arsitektur yang kokoh bagi pengembangan platform EduTech yang "
        "menyelesaikan permasalahan prediksi SNBP di Indonesia. Proyek ini merupakan "
        "bagian dari strategi jangka panjang untuk membangun ekosistem teknologi "
        "pendidikan yang scalable, secure, dan sustainable."
    )
    add_paragraph(doc,
        "Kebutuhan akan EA muncul karena kompleksitas sistem yang meningkat seiring "
        "dengan pertumbuhan fitur (dari prediksi sederhana menjadi ekosistem lengkap "
        "dengan Anti-Bentrok, XAI, dan multi-tenant B2B), pertumbuhan pengguna yang "
        "diproyeksikan eksponensial selama periode SNBP, serta kebutuhan untuk "
        "memastikan alignment antara strategi bisnis dan implementasi teknologi."
    )

    add_heading(doc, "3.5.2 Ringkasan Proyek", level=3)
    add_paragraph(doc,
        "Proyek EA LangkahKampus mencakup perancangan arsitektur di empat domain "
        "TOGAF (Business, Data, Application, Technology) untuk mendukung transformasi "
        "dari arsitektur monolitik sederhana menjadi arsitektur microservices yang "
        "cloud-native. Scope proyek meliputi:"
    )
    add_bullet_list(doc, [
        "Business Architecture: Definisi proses bisnis, capability model, dan value stream LangkahKampus",
        "Data Architecture: Perancangan data model, data flow, dan data governance framework",
        "Application Architecture: Desain arsitektur microservices, API, dan integration patterns",
        "Technology Architecture: Pemilihan technology stack, infrastructure design, dan deployment architecture",
    ])

    add_heading(doc, "3.5.3 Diagram Konsep Solusi", level=3)
    add_paragraph(doc,
        "Solution Concept Diagram menggambarkan high-level view dari solusi arsitektur "
        "LangkahKampus yang terdiri dari komponen-komponen utama berikut:"
    )
    add_paragraph(doc,
        "Layer 1 - Client Layer: Next.js Progressive Web App yang diakses oleh siswa "
        "melalui browser (mobile-first design) dan Guru BK melalui desktop dashboard. "
        "Aplikasi menggunakan React dengan server-side rendering untuk SEO dan initial "
        "load performance."
    )
    add_paragraph(doc,
        "Layer 2 - API Gateway: Kong API Gateway yang menangani authentication, "
        "rate limiting, dan request routing ke microservices yang sesuai. Gateway "
        "ini juga berfungsi sebagai security perimeter dan traffic management."
    )
    add_paragraph(doc,
        "Layer 3 - Application Services: Kumpulan FastAPI microservices yang masing-masing "
        "menangani domain spesifik - User Service, Prediction Service, Recommendation "
        "Service, School Dashboard Service, Payment Service, dan Notification Service."
    )
    add_paragraph(doc,
        "Layer 4 - ML Platform: Infrastructure khusus untuk ML workflow termasuk "
        "model training pipeline, feature store, model registry, dan inference "
        "serving. Mendukung A/B testing dan gradual rollout untuk model baru."
    )
    add_paragraph(doc,
        "Layer 5 - Data Layer: PostgreSQL sebagai primary database, Redis untuk "
        "caching dan session management, dan data warehouse (BigQuery/Redshift) "
        "untuk analytics. Event streaming menggunakan Apache Kafka untuk real-time "
        "data synchronization."
    )
    add_paragraph(doc,
        "Layer 6 - Infrastructure: Kubernetes cluster pada cloud provider (GCP/AWS) "
        "dengan auto-scaling, service mesh (Istio), dan comprehensive observability "
        "stack (Prometheus, Grafana, Jaeger)."
    )

    add_heading(doc, "3.5.4 Peta Stakeholder", level=3)
    add_paragraph(doc,
        "Stakeholders map memposisikan setiap stakeholder berdasarkan dua dimensi: "
        "tingkat pengaruh (influence) dan tingkat kepentingan (interest) terhadap "
        "proyek arsitektur enterprise LangkahKampus."
    )

    add_table(doc,
        headers=["Kuadran", "Kategori", "Stakeholder", "Strategi"],
        rows=[
            ["High Influence, High Interest", "Manage Closely", "CEO, CTO, ML Lead, Product Manager", "Kolaborasi aktif, involve dalam setiap keputusan arsitektur"],
            ["High Influence, Low Interest", "Keep Satisfied", "Investor, Regulator (Kemendikbudristek)", "Update berkala, compliance reports, escalation path jelas"],
            ["Low Influence, High Interest", "Keep Informed", "Siswa, Guru BK, Orang Tua", "Newsletter, release notes, feedback channels terbuka"],
            ["Low Influence, Low Interest", "Monitor", "Komunitas Developer, Media", "Monitoring sentimen, engagement minimal"],
        ],
        title="Peta Stakeholder - Matriks Pengaruh/Kepentingan",
        table_number=12
    )

    # References
    references = [
        "The Open Group. (2022). TOGAF Standard, 10th Edition. The Open Group.",
        "Harrison, R. (2018). TOGAF 9 Foundation Study Guide (4th ed.). Van Haren Publishing.",
        "Lankhorst, M. (2017). Enterprise Architecture at Work: Modelling, Communication and Analysis (4th ed.). Springer.",
        "Richards, M. (2015). Software Architecture Patterns. O'Reilly Media.",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems (2nd ed.). O'Reilly Media.",
        "Bass, L., Clements, P., & Kazman, R. (2021). Software Architecture in Practice (4th ed.). Addison-Wesley.",
        "Kementerian Pendidikan dan Kebudayaan. (2023). Panduan Sistem SNBP 2024. Kemendikbudristek.",
        "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi.",
        "Fowler, M. (2019). Refactoring: Improving the Design of Existing Code (2nd ed.). Addison-Wesley.",
        "Kim, G., Humble, J., Debois, P., & Willis, J. (2016). The DevOps Handbook. IT Revolution Press.",
        "Molnar, C. (2022). Interpretable Machine Learning: A Guide for Making Black Box Models Explainable. Leanpub.",
        "Richardson, C. (2018). Microservices Patterns: With Examples in Java. Manning Publications.",
        "Hohpe, G., & Woolf, B. (2003). Enterprise Integration Patterns. Addison-Wesley.",
        "Skelton, M., & Pais, M. (2019). Team Topologies: Organizing Business and Technology Teams for Fast Flow. IT Revolution Press.",
    ]

    add_references(doc, references)

    # Save document
    save_document(doc, "Stage3_Preliminary_Requirement_Architecture_Vision.docx")
    print("Stage 3: Dokumen berhasil di-generate!")
    print(f"Total paragraphs: {len(doc.paragraphs)}")
    print(f"Total tables: {len(doc.tables)}")


if __name__ == "__main__":
    generate_stage3()
