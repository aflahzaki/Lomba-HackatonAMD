"""
Generate Stage 2: Methodology and Project Planning
TOGAF Enterprise Architecture - LangkahKampus EduTech

This script generates the Stage 2 document covering:
- Deskripsi ADM TOGAF dan aplikasinya pada proyek
- Metodologi yang disusun khusus untuk proyek
- Rencana proyek detail
- Analisis risiko dan strategi mitigasi
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


def generate_stage2():
    """Generate Stage 2: Methodology and Project Planning document."""
    doc = create_document()

    # Cover Page
    add_cover_page(
        doc,
        title="Metodologi dan Perencanaan Proyek",
        stage_name="Stage 2 - Metodologi dan Perencanaan Proyek"
    )

    # Table of Contents
    toc_sections = [
        ("Deskripsi ADM TOGAF", [
            "Pengantar TOGAF ADM",
            "Fase-fase ADM TOGAF",
            "Aplikasi ADM pada Proyek LangkahKampus",
        ]),
        ("Metodologi Proyek", [
            "Pendekatan Metodologi",
            "Adaptasi untuk Konteks Startup EduTech",
            "Kerangka Integrasi: TOGAF + Agile",
        ]),
        ("Rencana Proyek Detail", [
            "Ruang Lingkup Proyek",
            "Sumber Daya",
            "Jadwal dan Timeline Proyek",
            "Milestones",
        ]),
        ("Analisis Risiko dan Strategi Mitigasi", [
            "Identifikasi Risiko",
            "Matriks Risiko",
            "Strategi Mitigasi Detail",
        ]),
        ("Daftar Pustaka", []),
    ]
    add_table_of_contents(doc, toc_sections)

    # ==========================================================================
    # Section 1: Deskripsi ADM TOGAF
    # ==========================================================================
    add_heading(doc, "1. Deskripsi ADM TOGAF", level=1)

    # 1.1 Pengantar TOGAF ADM
    add_heading(doc, "1.1 Pengantar TOGAF ADM", level=2)
    add_paragraph(doc,
        "TOGAF (The Open Group Architecture Framework) merupakan framework arsitektur "
        "enterprise yang paling banyak digunakan secara global untuk merancang, "
        "merencanakan, mengimplementasikan, dan mengelola arsitektur informasi enterprise. "
        "TOGAF dikembangkan dan dipelihara oleh The Open Group, sebuah konsorsium industri "
        "yang beranggotakan ratusan organisasi dari berbagai sektor. Versi terkini, TOGAF "
        "Standard 10th Edition (2022), menyediakan pendekatan komprehensif yang dapat "
        "diadaptasi untuk berbagai jenis dan skala organisasi."
    )
    add_paragraph(doc,
        "Komponen inti dari TOGAF adalah Architecture Development Method (ADM), sebuah "
        "metode iteratif dan siklikal yang menyediakan panduan langkah demi langkah untuk "
        "mengembangkan arsitektur enterprise. ADM terdiri dari serangkaian fase yang "
        "saling terkait, dimulai dari penetapan visi arsitektur hingga pengelolaan "
        "perubahan arsitektur secara berkelanjutan. Setiap fase menghasilkan artifak "
        "(deliverables) yang menjadi input bagi fase berikutnya, menciptakan alur kerja "
        "yang terstruktur dan traceable."
    )
    add_paragraph(doc,
        "ADM bersifat generik dan modular, yang berarti organisasi dapat mengadaptasi "
        "dan menyesuaikan penerapannya sesuai dengan konteks, kebutuhan, dan tingkat "
        "kematangan organisasi. Untuk LangkahKampus sebagai startup EduTech, ADM akan "
        "diadaptasi dengan pendekatan yang lebih agile dan iteratif, tetap mempertahankan "
        "rigor arsitektural namun dengan siklus yang lebih pendek dan fleksibel."
    )

    # 1.2 Fase-fase ADM TOGAF
    add_heading(doc, "1.2 Fase-fase ADM TOGAF", level=2)
    add_paragraph(doc,
        "ADM TOGAF terdiri dari fase Preliminary dan delapan fase utama (A hingga H) "
        "yang membentuk siklus pengembangan arsitektur. Berikut adalah deskripsi setiap "
        "fase beserta relevansinya terhadap proyek LangkahKampus:"
    )

    add_paragraph(doc, "Preliminary Phase: Framework and Principles", bold=True)
    add_paragraph(doc,
        "Fase ini menetapkan konteks organisasi, mendefinisikan prinsip-prinsip "
        "arsitektur, dan menyiapkan tools serta metodologi yang akan digunakan. Pada "
        "konteks LangkahKampus, fase ini mencakup penetapan prinsip-prinsip seperti "
        "privacy-by-design, scalability-first, dan pengambilan keputusan berbasis data "
        "sebagai landasan seluruh pengembangan arsitektur.",
        indent=0.5
    )

    add_paragraph(doc, "Phase A: Architecture Vision", bold=True)
    add_paragraph(doc,
        "Fase ini mendefinisikan visi tingkat tinggi dari arsitektur target, "
        "mengidentifikasi stakeholder, dan memperoleh persetujuan untuk "
        "melanjutkan proses pengembangan. Untuk LangkahKampus, Architecture Vision "
        "menggambarkan bagaimana platform EduTech akan beroperasi secara holistik, "
        "melayani siswa dan sekolah dengan sistem prediksi berbasis AI yang terintegrasi.",
        indent=0.5
    )

    add_paragraph(doc, "Phase B: Business Architecture", bold=True)
    add_paragraph(doc,
        "Fase ini mengembangkan arsitektur bisnis yang menggambarkan proses bisnis, "
        "fungsi organisasi, dan bagaimana bisnis beroperasi untuk memenuhi tujuan "
        "strategis. Pada LangkahKampus, ini mencakup pemetaan proses bisnis untuk "
        "layanan B2C (prediksi individual) dan B2B (dashboard sekolah), serta "
        "rantai nilai dari pengumpulan data hingga penyampaian insight.",
        indent=0.5
    )

    add_paragraph(doc, "Phase C: Information Systems Architecture", bold=True)
    add_paragraph(doc,
        "Fase ini terbagi menjadi dua sub-fase: Data Architecture dan Application "
        "Architecture. Data Architecture mendefinisikan struktur data, aliran data, "
        "dan pengelolaan data. Application Architecture mendefinisikan komponen aplikasi "
        "dan interaksi antar komponen. Untuk LangkahKampus, fase ini sangat krusial "
        "mengingat kompleksitas pipeline ML, data dari 40.000+ sekolah, dan arsitektur "
        "microservices yang digunakan.",
        indent=0.5
    )

    add_paragraph(doc, "Phase D: Technology Architecture", bold=True)
    add_paragraph(doc,
        "Fase ini mendefinisikan infrastruktur teknologi yang mendukung deployment "
        "komponen-komponen yang telah didefinisikan di fase sebelumnya. Pada LangkahKampus, "
        "ini mencakup arsitektur cloud, containerization strategy, database infrastructure, "
        "ML serving infrastructure, dan monitoring stack.",
        indent=0.5
    )

    add_paragraph(doc, "Phase E: Opportunities and Solutions", bold=True)
    add_paragraph(doc,
        "Fase ini mengidentifikasi peluang implementasi dan menentukan solusi-solusi "
        "yang akan diimplementasikan. Termasuk evaluasi keputusan membangun atau membeli, "
        "prioritisasi paket pekerjaan, dan perencanaan arsitektur transisi.",
        indent=0.5
    )

    add_paragraph(doc, "Phase F: Migration Planning", bold=True)
    add_paragraph(doc,
        "Fase ini mengembangkan rencana migrasi detail dari arsitektur saat ini (baseline) "
        "menuju arsitektur target. Untuk LangkahKampus sebagai startup, fokusnya lebih "
        "pada rencana implementasi bertahap daripada migrasi dari sistem lama.",
        indent=0.5
    )

    add_paragraph(doc, "Phase G: Implementation Governance", bold=True)
    add_paragraph(doc,
        "Fase ini menyediakan pengawasan arsitektural selama implementasi untuk "
        "memastikan bahwa implementasi sesuai dengan arsitektur yang telah dirancang. "
        "Pada LangkahKampus, ini diintegrasikan dengan CI/CD pipeline dan proses "
        "code review untuk memastikan kepatuhan.",
        indent=0.5
    )

    add_paragraph(doc, "Phase H: Architecture Change Management", bold=True)
    add_paragraph(doc,
        "Fase ini mengelola perubahan arsitektur secara berkelanjutan, memastikan bahwa "
        "arsitektur tetap relevan seiring dengan perubahan bisnis dan teknologi. Untuk "
        "LangkahKampus, ini mencakup mekanisme untuk mengakomodasi perubahan regulasi "
        "SNBP, evolusi model ML, dan perubahan kebutuhan pasar.",
        indent=0.5
    )

    add_paragraph(doc, "Requirements Management (Pusat Siklus ADM)", bold=True)
    add_paragraph(doc,
        "Requirements Management bukan merupakan fase tersendiri melainkan proses "
        "berkelanjutan yang berjalan di tengah seluruh fase ADM. Proses ini memastikan "
        "bahwa requirements dari stakeholder ditangkap, dikelola, dan dipenuhi secara "
        "konsisten di setiap fase pengembangan arsitektur.",
        indent=0.5
    )

    # 1.3 Aplikasi ADM pada Proyek LangkahKampus
    add_heading(doc, "1.3 Aplikasi ADM pada Proyek LangkahKampus", level=2)
    add_paragraph(doc,
        "Penerapan ADM TOGAF pada proyek LangkahKampus dilakukan dengan mempertimbangkan "
        "karakteristik unik dari organisasi sebagai startup EduTech. Berikut adalah "
        "pemetaan penerapan setiap fase ADM dalam konteks Tugas Besar ini:"
    )

    adm_headers = ["Fase ADM", "Deliverable Utama", "Stage Tugas Besar"]
    adm_rows = [
        ("Preliminary", "Prinsip Arsitektur, Peta Stakeholder", "Stage 3"),
        ("Phase A: Architecture Vision", "Dokumen Visi Arsitektur, Rantai Nilai", "Stage 3"),
        ("Requirements Management", "Katalog Kebutuhan, Kebutuhan Terprioritisasi", "Stage 3"),
        ("Phase B: Business Architecture", "Model Proses Bisnis, Peta Organisasi", "Stage 4"),
        ("Phase C: IS Architecture (Data)", "Model Entitas Data, Diagram Aliran Data", "Stage 5"),
        ("Phase C: IS Architecture (App)", "Portofolio Aplikasi, Peta Integrasi", "Stage 5"),
        ("Phase D: Technology Architecture", "Standar Teknologi, Diagram Infrastruktur", "Stage 6"),
    ]
    add_table(doc, adm_headers, adm_rows,
              title="Pemetaan Fase ADM ke Stage Tugas Besar", table_number=1)

    add_paragraph(doc,
        "Penerapan ADM pada LangkahKampus menggunakan pendekatan iteratif dimana setiap "
        "stage menghasilkan deliverables yang menjadi input untuk stage berikutnya. Hal "
        "ini memastikan konsistensi dan traceability dari visi arsitektur tingkat tinggi "
        "hingga detail implementasi teknologi."
    )

    # ==========================================================================
    # Section 2: Metodologi Proyek
    # ==========================================================================
    add_heading(doc, "2. Metodologi Proyek", level=1)

    # 2.1 Pendekatan Metodologi
    add_heading(doc, "2.1 Pendekatan Metodologi", level=2)
    add_paragraph(doc,
        "Metodologi yang digunakan dalam proyek ini merupakan adaptasi dari TOGAF ADM "
        "yang disesuaikan dengan konteks startup EduTech dan keterbatasan waktu akademik. "
        "Pendekatan ini mengombinasikan kerangka kerja TOGAF untuk rigor arsitektural "
        "dengan prinsip-prinsip Agile untuk fleksibilitas dan kecepatan iterasi."
    )
    add_paragraph(doc,
        "Pendekatan metodologi yang dipilih adalah Lean Enterprise Architecture yang "
        "mengadopsi prinsip arsitektur minimum yang layak. Berbeda dengan penerapan TOGAF "
        "tradisional yang cenderung berat dan membutuhkan waktu berbulan-bulan, "
        "pendekatan lean ini fokus pada deliverables yang memberikan nilai nyata dan "
        "wawasan yang dapat ditindaklanjuti bagi organisasi studi kasus."
    )
    add_paragraph(doc,
        "Metodologi ini terdiri dari empat tahapan utama yang masing-masing "
        "menghasilkan artefak arsitektur yang spesifik dan terukur:"
    )
    add_numbered_list(doc, [
        "Fase Penemuan (Discovery): Pemahaman konteks bisnis, identifikasi stakeholder, dan pengumpulan kebutuhan",
        "Fase Perancangan (Design): Perancangan arsitektur pada keempat domain (bisnis, data, aplikasi, teknologi)",
        "Fase Validasi (Validation): Validasi arsitektur terhadap kebutuhan dan batasan yang telah didefinisikan",
        "Fase Dokumentasi (Documentation): Dokumentasi formal seluruh artefak arsitektur dalam format akademik",
    ])

    # 2.2 Adaptasi untuk Konteks Startup EduTech
    add_heading(doc, "2.2 Adaptasi untuk Konteks Startup EduTech", level=2)
    add_paragraph(doc,
        "Penerapan TOGAF ADM pada LangkahKampus memerlukan beberapa adaptasi mengingat "
        "karakteristik unik startup dibandingkan dengan enterprise besar yang menjadi "
        "target utama framework TOGAF. Berikut adalah adaptasi-adaptasi yang dilakukan:"
    )

    add_paragraph(doc, "Adaptasi 1: Governance yang Disederhanakan", bold=True)
    add_paragraph(doc,
        "Startup tidak memiliki architecture board formal atau struktur governance yang "
        "kompleks. Oleh karena itu, governance dalam proyek ini disederhanakan menjadi "
        "peer review antar anggota tim dan validasi oleh dosen pengampu sebagai "
        "architecture governance board.",
        indent=0.5
    )

    add_paragraph(doc, "Adaptasi 2: Greenfield vs Brownfield", bold=True)
    add_paragraph(doc,
        "Berbeda dengan enterprise besar yang umumnya memiliki sistem lama (brownfield), "
        "LangkahKampus sebagai startup memulai dari greenfield. Ini berarti fase Migration "
        "Planning (Phase F) lebih berfokus pada strategi implementasi bertahap daripada "
        "migrasi dari sistem lama. Namun, integrasi dengan sistem eksternal (SNPMB/LTMPT) "
        "tetap menjadi pertimbangan brownfield yang relevan.",
        indent=0.5
    )

    add_paragraph(doc, "Adaptasi 3: Iteratif dan Terikat Waktu", bold=True)
    add_paragraph(doc,
        "Setiap stage dalam tugas besar ini dibatasi waktu sesuai jadwal perkuliahan. "
        "Meskipun ADM bersifat iteratif, dalam konteks akademik ini setiap iterasi "
        "diselesaikan dalam satu stage submission. Umpan balik dari dosen pada setiap stage "
        "menjadi input untuk penyempurnaan di stage berikutnya.",
        indent=0.5
    )

    add_paragraph(doc, "Adaptasi 4: Fokus pada Domain Inti", bold=True)
    add_paragraph(doc,
        "Mengingat skala startup dan keterbatasan waktu, lingkup arsitektur difokuskan "
        "pada domain inti LangkahKampus yaitu layanan prediksi all-in-one, "
        "onboarding wizard, sistem referral, dan dashboard evaluatif guru. Domain pendukung seperti HR, keuangan, "
        "dan pengadaan tidak termasuk dalam lingkup arsitektur ini.",
        indent=0.5
    )

    # 2.3 Framework Integrasi
    add_heading(doc, "2.3 Kerangka Integrasi: TOGAF + Agile", level=2)
    add_paragraph(doc,
        "Integrasi antara TOGAF dan pendekatan Agile dilakukan melalui konsep "
        "\"Architecture Runway\" dimana arsitektur dikembangkan secukupnya (just enough) "
        "untuk mendukung pengembangan fitur dalam sprint-sprint mendatang, tanpa terlalu "
        "jauh ke depan (over-architecting) yang berisiko menjadi usang."
    )

    add_paragraph(doc,
        "Model integrasi yang digunakan adalah sebagai berikut:"
    )
    add_bullet_list(doc, [
        "Arsitektur Intentional (TOGAF): Mendefinisikan panduan dan standar yang harus diikuti",
        "Arsitektur Emergent (Agile): Memungkinkan detail arsitektur berkembang organis melalui implementasi",
        "Architecture Decision Records (ADR): Mendokumentasikan keputusan arsitektur kunci beserta rasionalnya",
        "Fungsi Kesesuaian (Fitness Functions): Metrik terukur yang memvalidasi apakah implementasi sesuai dengan arsitektur",
    ])

    add_paragraph(doc,
        "Dengan pendekatan hybrid ini, proyek mendapatkan manfaat dari kedua sisi: "
        "struktur dan ketelitian dari TOGAF untuk memastikan arsitektur yang koheren dan "
        "terdokumentasi dengan baik, serta fleksibilitas dan responsivitas dari Agile untuk "
        "mengakomodasi perubahan dan pembelajaran yang terjadi selama proses pengembangan."
    )

    # ==========================================================================
    # Section 3: Rencana Proyek Detail
    # ==========================================================================
    add_heading(doc, "3. Rencana Proyek Detail", level=1)

    # 3.1 Ruang Lingkup
    add_heading(doc, "3.1 Ruang Lingkup Proyek", level=2)
    add_paragraph(doc,
        "Ruang lingkup proyek arsitektur enterprise LangkahKampus mencakup keempat "
        "domain arsitektur yang didefinisikan dalam TOGAF, dengan fokus khusus pada "
        "core business platform. Berikut adalah definisi ruang lingkup untuk setiap domain:"
    )

    add_paragraph(doc, "Business Architecture (Dalam Lingkup):", bold=True)
    add_bullet_list(doc, [
        "Proses bisnis inti: prediksi all-in-one, onboarding wizard, referral tracking",
        "Model operasional B2C freemium (siswa individual) dengan referral viral loop",
        "Peran guru sebagai evaluator pasif yang di-invite oleh siswa",
        "Rantai nilai dari registrasi, prediksi, hingga monetisasi",
        "Katalog layanan bisnis dan alur konversi pengguna",
    ])

    add_paragraph(doc, "Data Architecture (Dalam Lingkup):", bold=True)
    add_bullet_list(doc, [
        "Model data logis untuk entitas utama (siswa, guru, prediksi, referral_tracking)",
        "Diagram aliran data untuk pipeline prediksi dan pelacakan referral",
        "Kerangka kerja tata kelola data dan standar kualitas data",
        "Manajemen data master untuk data referensi (PTN, program studi, kuota)",
        "Manajemen siklus hidup data dan kebijakan retensi",
    ])

    add_paragraph(doc, "Application Architecture (Dalam Lingkup):", bold=True)
    add_bullet_list(doc, [
        "Arsitektur halaman prediksi all-in-one (PHP backend + Vanilla JS frontend)",
        "Arsitektur onboarding wizard bertahap",
        "Sistem referral link generation dan unique IP tracking",
        "Integrasi API prediksi dengan ML microservice",
        "Desain API endpoint dan strategi pembatasan akses (paywall logic)",
    ])

    add_paragraph(doc, "Technology Architecture (Dalam Lingkup):", bold=True)
    add_bullet_list(doc, [
        "Arsitektur infrastruktur hosting (PHP 8.x, web server, database)",
        "Integrasi ML microservice (FastAPI) dengan backend PHP",
        "Infrastruktur database (MySQL/PostgreSQL, caching)",
        "Arsitektur keamanan (autentikasi, otorisasi, validasi referral)",
        "Monitoring, logging, dan observability dasar",
    ])

    add_paragraph(doc, "Di Luar Lingkup:", bold=True)
    add_bullet_list(doc, [
        "Fungsi bisnis pendukung (HR, keuangan, legal, pengadaan)",
        "Arsitektur kantor/fasilitas fisik",
        "Desain UX/UI detail (hanya lanskap aplikasi tingkat tinggi)",
        "Kode sumber detail atau implementasi teknis per fitur",
        "Evaluasi vendor pihak ketiga dan proses pengadaan",
    ])

    # 3.2 Sumber Daya
    add_heading(doc, "3.2 Sumber Daya", level=2)
    add_paragraph(doc,
        "Proyek ini dilaksanakan oleh tim beranggotakan empat orang mahasiswa dengan "
        "pembagian tanggung jawab berdasarkan domain arsitektur dan keahlian masing-masing. "
        "Berikut adalah alokasi sumber daya untuk proyek:"
    )

    resource_headers = ["Anggota", "Domain Arsitektur", "Deliverables Utama"]
    resource_rows = [
        ("Aflah Rafilah Zaki", "Business Architecture\n+ Ketua Proyek",
         "Model Proses Bisnis, Rantai Nilai,\nManajemen Stakeholder, Koordinasi Proyek"),
        ("Azka Fathir Syarif", "Technology Architecture\n+ Arsitektur ML",
         "Diagram Infrastruktur, Standar Teknologi,\nArsitektur Pipeline ML, Arsitektur Keamanan"),
        ("Daffa Rizky Herdiawan", "Application Architecture",
         "Lanskap Aplikasi, Peta Integrasi,\nDesain API, Arsitektur Frontend/Backend"),
        ("Muhammad Arifin Ilham", "Data Architecture\n+ Kebutuhan",
         "Model Data, Diagram Aliran Data,\nKatalog Kebutuhan, Tata Kelola Data"),
    ]
    add_table(doc, resource_headers, resource_rows,
              title="Alokasi Sumber Daya Proyek", table_number=2)

    add_paragraph(doc,
        "Selain sumber daya manusia, proyek ini didukung oleh perangkat dan teknologi berikut:"
    )
    add_bullet_list(doc, [
        "ArchiMate / Draw.io: Pemodelan arsitektur dan diagram",
        "Microsoft Office / Google Docs: Dokumentasi dan presentasi",
        "Git/GitHub: Kontrol versi untuk artefak arsitektur",
        "TOGAF Standard 10th Edition: Referensi framework utama",
        "Python + python-docx: Pembuatan dokumen otomatis",
    ])

    # 3.3 Jadwal dan Timeline
    add_heading(doc, "3.3 Jadwal dan Timeline Proyek", level=2)
    add_paragraph(doc,
        "Jadwal proyek disusun mengikuti timeline perkuliahan Arsitektur Integrasi Sistem "
        "semester genap 2023/2024. Setiap stage memiliki durasi 2 minggu dengan submission "
        "deadline yang telah ditentukan. Berikut adalah timeline detail proyek:"
    )

    timeline_headers = ["Stage", "Periode", "Aktivitas Utama", "Deliverable"]
    timeline_rows = [
        ("Stage 1", "Minggu 1-2", "Proposal, identifikasi organisasi,\nanalisis awal",
         "Proposal Tugas Besar"),
        ("Stage 2", "Minggu 3-4", "Penyusunan metodologi,\nperencanaan proyek",
         "Metodologi & Rencana Proyek"),
        ("Stage 3", "Minggu 5-6", "Preliminary, Requirements,\nArchitecture Vision",
         "Dokumen Preliminary & Vision"),
        ("Stage 4", "Minggu 7-8", "Analisis proses bisnis,\npemetaan organisasi",
         "Dokumen Business Architecture"),
        ("Stage 5", "Minggu 9-10", "Perancangan arsitektur\nData & Aplikasi",
         "Dokumen IS Architecture"),
        ("Stage 6", "Minggu 11-12", "Perancangan infrastruktur\n& platform teknologi",
         "Dokumen Technology Architecture"),
    ]
    add_table(doc, timeline_headers, timeline_rows,
              title="Timeline Proyek Tugas Besar", table_number=3)

    add_paragraph(doc,
        "Setiap stage memiliki internal milestones yang memastikan progress yang terukur "
        "dan memungkinkan deteksi dini terhadap potensi keterlambatan. Tim menggunakan "
        "pertemuan sinkronisasi mingguan setiap hari Senin untuk review progress dan penyelesaian hambatan."
    )

    # 3.4 Milestones
    add_heading(doc, "3.4 Milestones", level=2)
    add_paragraph(doc,
        "Berikut adalah milestones utama proyek beserta kriteria keberhasilan (success "
        "criteria) yang terukur untuk setiap milestone:"
    )

    milestone_headers = ["No.", "Milestone", "Target", "Kriteria Keberhasilan"]
    milestone_rows = [
        ("M1", "Proposal Disetujui", "Akhir Minggu 2",
         "Proposal diterima, organisasi disetujui dosen"),
        ("M2", "Metodologi Ditetapkan", "Akhir Minggu 4",
         "Metodologi dan rencana proyek tervalidasi"),
        ("M3", "Visi Arsitektur Selesai", "Akhir Minggu 6",
         "Dokumen visi, prinsip, dan katalog kebutuhan selesai"),
        ("M4", "Business Architecture Selesai", "Akhir Minggu 8",
         "Model proses dan peta organisasi tervalidasi stakeholder"),
        ("M5", "IS Architecture Selesai", "Akhir Minggu 10",
         "Model data dan lanskap aplikasi terintegrasi"),
        ("M6", "Technology Architecture Selesai", "Akhir Minggu 12",
         "Diagram infrastruktur dan roadmap teknologi final"),
        ("M7", "Pengumpulan Final", "Minggu 13",
         "Seluruh dokumen terkonsolidasi dan dipresentasikan"),
    ]
    add_table(doc, milestone_headers, milestone_rows,
              title="Milestones Proyek", table_number=4)

    add_paragraph(doc,
        "Monitoring milestone dilakukan melalui checklist review pada setiap pertemuan "
        "sinkronisasi mingguan. Jika sebuah milestone berisiko terlambat, tim akan melakukan perencanaan ulang "
        "dan alokasi ulang sumber daya untuk memastikan tenggat waktu utama tetap terpenuhi."
    )

    # ==========================================================================
    # Section 4: Analisis Risiko dan Strategi Mitigasi
    # ==========================================================================
    add_heading(doc, "4. Analisis Risiko dan Strategi Mitigasi", level=1)

    # 4.1 Identifikasi Risiko
    add_heading(doc, "4.1 Identifikasi Risiko", level=2)
    add_paragraph(doc,
        "Identifikasi risiko dilakukan menggunakan pendekatan brainstorming terstruktur "
        "yang mempertimbangkan tiga kategori utama risiko: risiko proyek (terkait "
        "pelaksanaan tugas besar), risiko teknis (terkait kompleksitas arsitektur), dan "
        "risiko bisnis (terkait validitas arsitektur terhadap konteks nyata LangkahKampus)."
    )
    add_paragraph(doc,
        "Setiap risiko dinilai berdasarkan dua dimensi: probabilitas terjadinya "
        "(kemungkinan) dan dampak terhadap keberhasilan proyek. Kedua dimensi "
        "menggunakan skala 1-5 dimana 1 adalah sangat rendah dan 5 adalah sangat tinggi. "
        "Skor risiko dihitung sebagai perkalian probabilitas dan dampak."
    )

    # 4.2 Matriks Risiko
    add_heading(doc, "4.2 Matriks Risiko", level=2)

    risk_headers = ["ID", "Risiko", "Prob.", "Dampak", "Skor", "Level"]
    risk_rows = [
        ("R01", "Keterbatasan waktu per stage (2 minggu)", "4", "4", "16", "Tinggi"),
        ("R02", "Kurangnya akses ke data riil SNBP", "3", "4", "12", "Tinggi"),
        ("R03", "Kompleksitas arsitektur ML sulit dimodelkan", "3", "3", "9", "Sedang"),
        ("R04", "Inkonsistensi antar stage karena paralel work", "3", "3", "9", "Sedang"),
        ("R05", "Ketidaktersediaan expert review untuk validasi", "2", "3", "6", "Sedang"),
        ("R06", "Perubahan requirement di tengah proyek", "2", "4", "8", "Sedang"),
        ("R07", "Tool/teknologi modeling mengalami kendala", "2", "2", "4", "Rendah"),
        ("R08", "Anggota tim berhalangan (sakit/kegiatan lain)", "3", "3", "9", "Sedang"),
        ("R09", "Scope creep pada domain arsitektur", "3", "3", "9", "Sedang"),
        ("R10", "Feedback dosen memerlukan rework signifikan", "2", "4", "8", "Sedang"),
    ]
    add_table(doc, risk_headers, risk_rows,
              title="Matriks Risiko Proyek", table_number=5)

    add_paragraph(doc,
        "Berdasarkan matriks risiko di atas, terdapat dua risiko dengan level Tinggi "
        "(R01 dan R02) yang memerlukan strategi mitigasi prioritas, serta tujuh risiko "
        "level Sedang yang perlu dimonitor secara aktif."
    )

    # 4.3 Strategi Mitigasi Detail
    add_heading(doc, "4.3 Strategi Mitigasi Detail", level=2)

    add_paragraph(doc, "R01 - Keterbatasan Waktu per Stage (Level Risiko: Tinggi)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Implementasi manajemen waktu yang ketat dengan tenggat internal "
        "3 hari sebelum tenggat resmi pengumpulan. Pembagian kerja yang jelas "
        "sejak awal setiap stage dengan checkpoint mingguan. Penggunaan template dokumen "
        "terstandar (pembuatan dokumen otomatis) untuk mengurangi waktu pemformatan. "
        "Waktu cadangan dialokasikan untuk review dan revisi.",
        indent=0.5
    )
    add_paragraph(doc,
        "Rencana Kontingensi: Jika waktu tidak mencukupi, tim akan melakukan prioritisasi "
        "berdasarkan rubrik penilaian dan fokus pada deliverables dengan bobot tertinggi. "
        "Konten yang bersifat pelengkap akan ditandai untuk dikembangkan di iterasi "
        "berikutnya.",
        indent=0.5
    )

    add_paragraph(doc, "R02 - Kurangnya Akses ke Data Riil SNBP (Level Risiko: Tinggi)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Penggunaan data publik yang tersedia dari sumber resmi "
        "(laman SNPMB, data statistik Kemendikbudristek) sebagai basis. Pelengkapan "
        "dengan data simulasi yang representatif untuk model arsitektur. Fokus pada "
        "pola arsitektural yang tidak bergantung pada data spesifik sehingga arsitektur tetap valid "
        "terlepas dari sumber data spesifik.",
        indent=0.5
    )
    add_paragraph(doc,
        "Rencana Kontingensi: Jika data publik tidak tersedia, tim akan menggunakan "
        "data sintetis yang dibuat berdasarkan parameter statistik yang masuk akal "
        "dan asumsi yang didokumentasikan dengan jelas.",
        indent=0.5
    )

    add_paragraph(doc, "R03 - Kompleksitas Arsitektur ML (Level Risiko: Sedang)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Referensi ke pola arsitektur ML yang telah mapan "
        "(Google MLOps Maturity Model, Microsoft ML Architecture). Konsultasi dengan "
        "literatur akademis tentang arsitektur sistem ML. Dekomposisi sistem ML "
        "menjadi komponen-komponen yang lebih mudah dikelola (training, serving, monitoring).",
        indent=0.5
    )

    add_paragraph(doc, "R04 - Inkonsistensi Antar Stage (Level Risiko: Sedang)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Penggunaan repositori arsitektur bersama (Git) dimana "
        "semua artefak arsitektur tersimpan secara terpusat. Review silang antar anggota "
        "tim sebelum pengumpulan. Matriks ketelusuran yang menghubungkan kebutuhan "
        "dengan setiap artefak arsitektur di semua stage.",
        indent=0.5
    )

    add_paragraph(doc, "R08 - Anggota Tim Berhalangan (Level Risiko: Sedang)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Sistem pendamping dimana setiap anggota memiliki satu cadangan "
        "yang familiar dengan domain pekerjaannya. Dokumentasi progress yang konsisten "
        "di ruang kerja bersama sehingga anggota lain dapat melanjutkan pekerjaan jika "
        "diperlukan. Minimal 2 hari waktu cadangan sebelum tenggat untuk mengakomodasi ketidakhadiran.",
        indent=0.5
    )

    add_paragraph(doc, "R09 - Perluasan Lingkup (Scope Creep) (Level Risiko: Sedang)", bold=True)
    add_paragraph(doc,
        "Strategi Mitigasi: Definisi lingkup yang jelas dan tertulis di awal setiap "
        "stage (didokumentasikan dalam bagian 3.1). Permintaan perubahan harus disetujui oleh "
        "minimal 2 anggota tim sebelum ditambahkan ke lingkup. Fokus pada \"minimum "
        "viable architecture\" yang memenuhi rubrik penilaian tanpa over-engineering.",
        indent=0.5
    )

    # ==========================================================================
    # Daftar Pustaka
    # ==========================================================================
    references = [
        "The Open Group. (2022). TOGAF Standard, 10th Edition. The Open Group.",
        "Harrison, R. (2018). TOGAF 9 Foundation Study Guide (4th ed.). Van Haren Publishing.",
        "Lankhorst, M. (2017). Enterprise Architecture at Work: Modelling, Communication and Analysis (4th ed.). Springer.",
        "Josey, A. (2018). TOGAF 9.2 - A Pocket Guide. Van Haren Publishing.",
        "Leffingwell, D. (2020). SAFe 5.0 Distilled: Achieving Business Agility with the Scaled Agile Framework. Addison-Wesley.",
        "Ford, N., Parsons, R., & Kua, P. (2017). Building Evolutionary Architectures: Support Constant Change. O'Reilly Media.",
        "Richards, M. (2015). Software Architecture Patterns. O'Reilly Media.",
        "Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., ... & Dennison, D. (2015). Hidden Technical Debt in Machine Learning Systems. Advances in Neural Information Processing Systems, 28.",
        "Google Cloud. (2021). MLOps: Continuous Delivery and Automation Pipelines in Machine Learning. Google Cloud Architecture Center.",
        "Project Management Institute. (2021). A Guide to the Project Management Body of Knowledge (PMBOK Guide) (7th ed.). PMI.",
        "Hillson, D. (2009). Managing Risk in Projects. Routledge.",
        "Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi. (2024). Panduan Seleksi Nasional Berdasarkan Prestasi (SNBP) Tahun 2024. Kemendikbudristek.",
    ]
    add_references(doc, references)

    # Save document
    save_document(doc, "Stage2_Methodology_and_Project_Planning.docx")
    print("Stage 2: Metodologi dan Perencanaan Proyek - Berhasil di-generate!")


if __name__ == "__main__":
    generate_stage2()
