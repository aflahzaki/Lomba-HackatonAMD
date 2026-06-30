"""
Generate Stage 6: Phase D - Technology Architecture
TOGAF Enterprise Architecture - LangkahKampus EduTech

This script generates the Stage 6 document covering:
- Architecture Definition Document - Technology (Baseline & Target)
- Gap Analysis Matrix - Technology
- Technology Requirements
- Architecture Principles (Updated)
- Statement of Architecture Work (Updated/Final)
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


def generate_stage6():
    """Generate Stage 6: Phase D - Technology Architecture."""
    doc = create_document()

    # Cover Page
    add_cover_page(
        doc,
        title="Phase D: Arsitektur Teknologi",
        stage_name="Stage 6 - Arsitektur Teknologi (Technology Architecture)"
    )

    # Table of Contents
    toc_sections = [
        ("Dokumen Definisi Arsitektur - Teknologi", [
            "Arsitektur Teknologi Baseline",
            "Arsitektur Teknologi Target",
            "Gap Analysis - Teknologi",
            "Tabel Gap dan Solusi",
            "Timeline Transisi",
        ]),
        ("Kebutuhan Teknologi", []),
        ("Prinsip Arsitektur (Diperbarui)", []),
        ("Pernyataan Pekerjaan Arsitektur (Final)", []),
        ("Daftar Pustaka", []),
    ]
    add_table_of_contents(doc, toc_sections)

    # ==========================================================================
    # SECTION 1: ARCHITECTURE DEFINITION DOCUMENT - TECHNOLOGY
    # ==========================================================================
    add_heading(doc, "1. Dokumen Definisi Arsitektur - Teknologi", level=1)

    add_paragraph(doc,
        "Architecture Definition Document pada fase Technology Architecture "
        "mendefinisikan infrastruktur teknologi yang akan mendukung arsitektur "
        "data dan aplikasi LangkahKampus yang telah dirancang pada fase sebelumnya. "
        "Fase ini mencakup pemilihan platform, infrastruktur, tools, dan standar "
        "teknologi yang akan digunakan dalam implementasi."
    )

    # --------------------------------------------------------------------------
    # 1.1 BASELINE TECHNOLOGY ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "1.1 Arsitektur Teknologi Baseline", level=2)

    add_paragraph(doc,
        "Pada kondisi baseline, infrastruktur teknologi untuk proses SNBP "
        "sangat minimal dan bergantung sepenuhnya pada infrastruktur yang "
        "disediakan oleh LTMPT (portal SNBP/PDSS) dan tools generic yang "
        "digunakan sekolah secara terpisah."
    )

    # Technology Standard Catalog (Baseline)
    add_heading(doc, "1.1.1 Technology Standard Catalog (Baseline)", level=3)

    add_table(doc,
        headers=["Kategori Teknologi", "Standard/Platform", "Vendor", "Status", "Keterangan"],
        rows=[
            ["Web Hosting", "Shared hosting / tidak ada", "Beragam", "Legacy", "Sekolah yang punya website menggunakan shared hosting basic"],
            ["Database", "MySQL (SIS sekolah) / Excel files", "Beragam / Microsoft", "Legacy", "Tidak terstandarisasi, setiap sekolah berbeda"],
            ["Operating System", "Windows (desktop Guru BK/Operator)", "Microsoft", "Current", "Standard OS untuk end users"],
            ["Browser", "Chrome / Edge", "Google / Microsoft", "Current", "Akses ke portal LTMPT"],
            ["Office Suite", "Microsoft Office / Google Workspace", "Microsoft / Google", "Current", "Excel untuk data management manual"],
            ["Communication", "WhatsApp, Email", "Meta, Google", "Current", "Komunikasi informal terkait SNBP"],
            ["Network", "Internet sekolah (beragam kualitas)", "ISP lokal", "Variable", "Kualitas tidak merata, beberapa daerah 3G only"],
            ["Security", "Basic (no standard)", "-", "Inadequate", "Tidak ada standar keamanan data siswa yang formal"],
        ],
        title="Technology Standard Catalog (Baseline)",
        table_number=1
    )

    # Application/Technology Matrix (Baseline)
    add_heading(doc, "1.1.2 Application/Technology Matrix (Baseline)", level=3)

    add_table(doc,
        headers=["Application", "Platform", "Runtime", "Database", "Hosting"],
        rows=[
            ["Portal PDSS LTMPT", "Web", "Java/PHP (unknown)", "PostgreSQL (assumed)", "LTMPT Data Center"],
            ["Portal SNBP LTMPT", "Web", "Java/PHP (unknown)", "PostgreSQL (assumed)", "LTMPT Data Center"],
            ["Excel (Guru BK)", "Desktop", "Windows", "File-based (.xlsx)", "Local PC"],
            ["SIS Sekolah (jika ada)", "Web/Desktop", "PHP/Java (beragam)", "MySQL", "Shared hosting / on-premise"],
            ["WhatsApp", "Mobile/Web", "Proprietary", "Cloud (Meta)", "Meta Cloud"],
        ],
        title="Application/Technology Matrix (Baseline)",
        table_number=2
    )

    # Environment and Locations Diagram (Baseline)
    add_heading(doc, "1.1.3 Environment and Locations Diagram (Baseline)", level=3)

    add_paragraph(doc,
        "Pada kondisi baseline, environment sangat sederhana dan tidak redundant:"
    )

    add_paragraph(doc, "Lokasi dan Environment:", bold=True)
    add_bullet_list(doc, [
        "LTMPT Data Center (Jakarta): Hosting portal PDSS dan SNBP - single location, no public DR information",
        "Sekolah (40.000+ lokasi tersebar): PC desktop Guru BK dan operator, koneksi internet beragam (4G-fiber)",
        "Rumah Siswa (jutaan lokasi): Personal device (smartphone/laptop), koneksi mobile data / WiFi",
        "Tidak ada staging/testing environment terpisah",
        "Tidak ada monitoring atau observability infrastructure",
        "Tidak ada disaster recovery plan yang diketahui untuk data sekolah",
    ])

    add_paragraph(doc,
        "Keterbatasan utama baseline: single point of failure pada LTMPT portal, "
        "tidak ada redundancy untuk data sekolah, tidak ada automated backup, "
        "dan tidak ada capacity planning untuk peak period SNBP."
    )

    # --------------------------------------------------------------------------
    # 1.2 TARGET TECHNOLOGY ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading(doc, "1.2 Arsitektur Teknologi Target", level=2)

    add_paragraph(doc,
        "Arsitektur teknologi target LangkahKampus mengadopsi cloud-native approach "
        "dengan emphasis pada scalability, reliability, dan security. Pemilihan "
        "teknologi mempertimbangkan keseimbangan antara kemampuan startup (tim kecil, "
        "budget terbatas) dengan kebutuhan skalabilitas saat peak SNBP period."
    )

    # Technology Standard Catalog (Target)
    add_heading(doc, "1.2.1 Technology Standard Catalog (Target)", level=3)

    add_table(doc,
        headers=["Kategori", "Standar Teknologi", "Versi/Spek", "Rasional", "Fase Adopsi"],
        rows=[
            ["Web Server", "Nginx + PHP-FPM", "Latest stable", "High performance PHP serving, reverse proxy capability, SSL termination", "Fase 1"],
            ["Backend Language", "PHP", "8.x", "Mature ecosystem, vanilla approach untuk simplicity, banyak hosting support", "Fase 1"],
            ["ML Service", "Python + FastAPI", "3.11+ / 0.100+", "ML ecosystem terbaik di Python, FastAPI untuk high-performance API serving", "Fase 1"],
            ["Database (Primary)", "MySQL / PostgreSQL", "8.x / 15+", "Reliable RDBMS, ACID compliance, JSON support untuk flexible data", "Fase 1"],
            ["Database (Cache)", "Redis", "7.x", "In-memory speed untuk session management, caching, dan ML feature store", "Fase 1"],
            ["CDN", "Cloudflare", "Free/Pro", "Global edge caching, DDoS protection, SSL, performance optimization", "Fase 1"],
            ["Payment Gateway", "Midtrans / Xendit", "Latest SDK", "Indonesian payment support, multiple methods (bank transfer, e-wallet, QRIS)", "Fase 1"],
            ["ML Training", "MLflow + XGBoost + LightGBM", "Latest", "Experiment tracking, model versioning, ensemble model management", "Fase 1"],
            ["ML Serving", "FastAPI + ONNX Runtime", "Latest", "Low-latency inference, model optimization untuk production", "Fase 1"],
            ["Hosting", "VPS / Cloud VM", "2-4 vCPU, 8GB RAM", "Cost-effective untuk startup, scalable on demand saat peak SNBP", "Fase 1"],
            ["CI/CD Pipeline", "GitHub Actions", "Current", "Automated testing, deployment, free tier generous untuk open source", "Fase 1"],
            ["Monitoring", "Uptime monitoring + error logging", "Latest", "Basic observability: uptime checks, PHP error logging, ML metrics", "Fase 1"],
            ["SSL/TLS", "Let's Encrypt (via Cloudflare)", "TLS 1.3", "Free certificates, auto-renewal, modern encryption", "Fase 1"],
            ["Version Control", "Git + GitHub", "Latest", "Source code management, code review, CI/CD integration", "Fase 1"],
            ["Secrets Management", "Environment variables + .env", "N/A", "Simple secrets management yang cukup untuk skala startup awal", "Fase 1"],
            ["Containerization", "Docker (opsional)", "24.x", "Reproducible environment untuk ML service, deployment consistency", "Fase 2"],
        ],
        title="Technology Standard Catalog (Target)",
        table_number=3
    )

    # Application/Technology Matrix (Target)
    add_heading(doc, "1.2.2 Application/Technology Matrix (Target)", level=3)

    add_table(doc,
        headers=["Application", "Runtime", "Framework", "Database", "Deployment", "Scaling"],
        rows=[
            ["Landing Page + Frontend", "PHP 8.x", "Vanilla PHP + HTML/CSS/JS", "MySQL/PostgreSQL (read)", "VPS / Shared Hosting", "CDN + Opcache"],
            ["Onboarding Wizard", "PHP 8.x", "Vanilla PHP + Vanilla JS", "MySQL/PostgreSQL", "Same as frontend", "Session-based"],
            ["Prediksi All-in-One", "PHP 8.x + Python 3.11", "PHP (view) + FastAPI (ML)", "MySQL/PostgreSQL + Redis", "VPS + ML Server", "ML horizontal scaling"],
            ["Dashboard Siswa", "PHP 8.x", "Vanilla PHP", "MySQL/PostgreSQL", "Same as frontend", "Server-side rendering"],
            ["Dashboard Guru", "PHP 8.x", "Vanilla PHP", "MySQL/PostgreSQL", "Same as frontend", "Server-side rendering"],
            ["API Referral", "PHP 8.x", "Vanilla PHP (REST)", "MySQL/PostgreSQL", "Same as frontend", "Stateless"],
            ["Pembayaran", "PHP 8.x", "PHP + Midtrans SDK", "MySQL/PostgreSQL", "Same as frontend", "Webhook-based"],
            ["Peta Universitas", "PHP 8.x", "PHP + Leaflet.js", "MySQL/PostgreSQL", "Same as frontend", "Static tiles CDN"],
            ["ML Prediction Service", "Python 3.11", "FastAPI + ONNX Runtime", "Redis (features) + PostgreSQL", "Dedicated ML server", "Horizontal auto-scaling"],
            ["ML Training Pipeline", "Python 3.11", "MLflow + XGBoost + LightGBM", "PostgreSQL + file storage", "Scheduled job server", "On-demand"],
        ],
        title="Application/Technology Matrix (Target)",
        table_number=4
    )

    # Environment and Locations Diagram (Target)
    add_heading(doc, "1.2.3 Environment and Locations Diagram (Target)", level=3)

    add_paragraph(doc,
        "Arsitektur environment target dirancang dengan multi-zone deployment "
        "untuk high availability dan geographic proximity ke pengguna:"
    )

    add_paragraph(doc, "Production Environment (GCP asia-southeast2 - Jakarta):", bold=True)
    add_bullet_list(doc, [
        "GKE Cluster: 3-node minimum (auto-scale to 20+ nodes during peak SNBP)",
        "Node pools: general-purpose (e2-standard-4), ML/GPU (n1-standard-8 + T4 GPU)",
        "Cloud SQL for PostgreSQL: High availability (primary + standby), automated backups",
        "Memorystore for Redis: HA configuration with automatic failover",
        "Cloud Storage: Multi-region for ML models and static assets",
        "Cloud CDN: Edge caching untuk static content dan API responses yang cacheable",
    ])

    add_paragraph(doc, "Staging Environment (GCP asia-southeast2 - Jakarta):", bold=True)
    add_bullet_list(doc, [
        "GKE Cluster: 2-node (scaled down version of production)",
        "Cloud SQL: Single instance (non-HA) with production-like schema",
        "Memorystore: Single instance",
        "Purpose: Pre-production testing, performance testing, UAT",
    ])

    add_paragraph(doc, "Development Environment:", bold=True)
    add_bullet_list(doc, [
        "Local: Docker Compose for local development (all services)",
        "Cloud Dev: GKE namespace per developer for integration testing",
        "CI/CD: GitHub Actions runners (managed) for automated testing",
    ])

    add_paragraph(doc, "Disaster Recovery:", bold=True)
    add_bullet_list(doc, [
        "Database: Automated daily backups to asia-southeast1 (Singapore), point-in-time recovery",
        "Application: Container images stored in Artifact Registry (multi-region)",
        "Configuration: All infrastructure as code in Git, reproducible in < 2 hours",
        "DR Target: RTO < 4 hours, RPO < 1 hour",
    ])

    add_paragraph(doc, "Network Architecture:", bold=True)
    add_bullet_list(doc, [
        "VPC: Custom VPC with private subnets for services, public subnet for ingress only",
        "Firewall Rules: Default deny, explicit allow only for required ports",
        "Cloud NAT: For outbound internet access from private nodes",
        "Cloud Armor: WAF protection for API Gateway (OWASP Top 10 rules)",
        "Private Google Access: Direct connection to GCP services without public internet",
    ])

    # Edge/Client Tier
    add_paragraph(doc, "Edge/Client Tier:", bold=True)
    add_bullet_list(doc, [
        "Cloudflare CDN: 275+ PoPs globally, DDoS mitigation, edge caching",
        "SSL termination at Cloudflare, re-encryption to origin (full strict mode)",
        "Client devices: Mobile (Android/iOS browser), Desktop browser, minimal bandwidth requirement (100kbps for basic prediction)",
    ])

    # --------------------------------------------------------------------------
    # 1.3 GAP ANALYSIS - TECHNOLOGY
    # --------------------------------------------------------------------------
    add_heading(doc, "1.3 Gap Analysis - Arsitektur Teknologi", level=2)

    add_heading(doc, "1.3.1 Gap Analysis Matrix - Technology", level=3)

    add_table(doc,
        headers=["Technology Domain", "Baseline", "Target", "Gap", "Investment Required"],
        rows=[
            ["Cloud Infrastructure", "No cloud (shared hosting if any)", "GCP with GKE, multi-zone, auto-scaling", "Full cloud migration: GCP account, GKE setup, network design, IAM", "Tinggi"],
            ["Containerization", "None", "Docker for all services, Helm charts", "Dockerize all services, create Helm charts, registry setup", "Sedang"],
            ["Orchestration", "None", "Kubernetes (GKE) with HPA and node auto-scaling", "GKE cluster setup, node pool config, HPA policies", "Tinggi"],
            ["CI/CD Pipeline", "None", "GitHub Actions + ArgoCD (GitOps)", "Pipeline design, test automation, deployment automation", "Sedang"],
            ["Database Infrastructure", "Local files / basic MySQL", "Managed PostgreSQL (HA) + Redis (HA)", "Cloud SQL setup, schema migration, backup policies, HA config", "Sedang"],
            ["ML Infrastructure", "None", "MLflow + Vertex AI + ONNX serving", "ML pipeline setup, model registry, GPU node pool, training automation", "Tinggi"],
            ["Monitoring & Observability", "None", "Prometheus + Grafana + Loki + Jaeger", "Full observability stack deployment, dashboard creation, alerting rules", "Sedang"],
            ["Security Infrastructure", "None (basic)", "WAF + Secret Mgr + mTLS + Cloud Armor", "Security stack deployment, policy definition, compliance audit", "Tinggi"],
            ["CDN & Edge", "None", "Cloudflare (Enterprise) with DDoS protection", "Cloudflare setup, DNS migration, caching rules, WAF rules", "Rendah"],
            ["Network Design", "Flat/none", "VPC, private subnets, Cloud NAT, firewall rules", "Network architecture design, segmentation, access control", "Sedang"],
            ["Disaster Recovery", "None", "Cross-region backup, RTO<4h, RPO<1h", "DR strategy, backup automation, failover testing", "Sedang"],
            ["IaC (Infrastructure as Code)", "None", "Terraform + Helm for all infrastructure", "Write Terraform modules, Helm charts, state management", "Sedang"],
        ],
        title="Gap Analysis Matrix - Technology Architecture",
        table_number=5
    )

    # Gap and Solution Table - Technology
    add_heading(doc, "1.3.2 Gap and Solution Table - Technology", level=3)

    add_table(doc,
        headers=["Gap ID", "Gap", "Solution", "Estimated Cost (Monthly)"],
        rows=[
            ["GAP-T01", "No cloud infrastructure", "Setup GCP project, enable APIs, configure billing alerts, create VPC", "$200-500 (Phase 1), $2000-5000 (Peak SNBP)"],
            ["GAP-T02", "No container platform", "Deploy GKE cluster with multiple node pools, setup container registry", "Included in GCP compute cost"],
            ["GAP-T03", "No CI/CD automation", "Configure GitHub Actions workflows, deploy ArgoCD for GitOps, setup environments", "$0-50 (GitHub Actions minutes)"],
            ["GAP-T04", "No managed database", "Deploy Cloud SQL PostgreSQL (HA), Memorystore Redis, configure backups", "$150-400 (standard), $800+ (peak)"],
            ["GAP-T05", "No ML platform", "Deploy MLflow on GKE, configure Vertex AI for training, GPU node pool", "$100-300 (training), $500+ (serving with GPU)"],
            ["GAP-T06", "No monitoring stack", "Deploy Prometheus + Grafana + Loki via Helm charts, create dashboards", "$0 (self-hosted on GKE)"],
            ["GAP-T07", "No security infrastructure", "Deploy Cloud Armor WAF, Secret Manager, configure Istio mTLS", "$50-100 (Cloud Armor), $0 (Secret Manager free tier)"],
            ["GAP-T08", "No CDN/edge protection", "Configure Cloudflare (Pro plan), DNS setup, caching rules, page rules", "$20-200 (Cloudflare Pro/Business)"],
            ["GAP-T09", "No disaster recovery", "Configure cross-region Cloud SQL replica, automated backup verification, runbook creation", "$100-200 (cross-region storage)"],
            ["GAP-T10", "No infrastructure as code", "Write Terraform modules for all GCP resources, Helm charts for all services", "$0 (tooling is free)"],
        ],
        title="Gap and Solution Table - Technology Architecture",
        table_number=6
    )

    # Transition Timeline - Technology
    add_heading(doc, "1.3.3 Transition Timeline - Technology", level=3)

    add_table(doc,
        headers=["Fase", "Periode", "Technology Milestones", "Estimated Monthly Cost"],
        rows=[
            ["Fase 1: Foundation", "Bulan 1-4", "GCP project setup, GKE cluster deployed, CI/CD pipeline operational, PostgreSQL + Redis live, basic monitoring, Cloudflare active, Docker all services", "$500-800"],
            ["Fase 2: Enhancement", "Bulan 5-8", "MLflow deployed, GPU node pool active, Istio service mesh, Jaeger tracing, full observability dashboards, DR setup, IaC complete", "$1000-2000"],
            ["Fase 3: Scale", "Bulan 9-12", "Auto-scaling validated for 500K concurrent, performance tuned, Kafka deployed, multi-zone HA tested, security audit passed, DR drill completed", "$2000-5000 (peak: $8000-12000)"],
        ],
        title="Transition Timeline - Technology Architecture",
        table_number=7
    )

    add_paragraph(doc, "Catatan Biaya:", bold=True)
    add_paragraph(doc,
        "Estimasi biaya mencerminkan model startup yang cost-conscious: menggunakan "
        "preemptible/spot instances untuk non-critical workloads, auto-scaling down "
        "saat off-peak (Maret-November), dan scale-up aggressif hanya selama peak "
        "SNBP period (Desember-Februari). GCP startup credits ($100K dari Google for "
        "Startups program) dapat menutupi sebagian besar biaya Phase 1-2."
    )

    # ==========================================================================
    # SECTION 2: TECHNOLOGY REQUIREMENTS
    # ==========================================================================
    add_heading(doc, "2. Kebutuhan Teknologi", level=1)

    add_paragraph(doc,
        "Technology requirements mendefinisikan standar dan kriteria yang harus "
        "dipenuhi oleh infrastruktur teknologi LangkahKampus."
    )

    add_table(doc,
        headers=["ID", "Kategori", "Kebutuhan", "Metrik Target", "Prioritas"],
        rows=[
            ["TR-001", "Performance", "API response time (p95) harus < 200ms untuk non-ML endpoints", "< 200ms p95", "P1"],
            ["TR-002", "Performance", "ML prediction latency (p95) harus < 2 detik termasuk feature retrieval", "< 2000ms p95", "P1"],
            ["TR-003", "Scalability", "Platform harus auto-scale dari 10K ke 500K concurrent users dalam 15 menit", "15 min scale-up time", "P1"],
            ["TR-004", "Availability", "Uptime SLA 99.9% (max 8.76 jam downtime per tahun)", "99.9% availability", "P1"],
            ["TR-005", "Availability", "Zero-downtime deployment untuk semua services", "0s deployment downtime", "P1"],
            ["TR-006", "Security", "All data encrypted at-rest (AES-256) dan in-transit (TLS 1.3)", "AES-256 + TLS 1.3", "P1"],
            ["TR-007", "Security", "Vulnerability scanning automated dalam CI/CD pipeline", "0 critical/high CVE in production", "P1"],
            ["TR-008", "Security", "WAF must block OWASP Top 10 attack patterns", "100% OWASP Top 10 coverage", "P1"],
            ["TR-009", "Reliability", "Automated failover untuk database dan cache < 30 detik", "< 30s failover time", "P1"],
            ["TR-010", "Reliability", "Automated backup verification (restore test) bulanan", "Monthly restore test pass", "P2"],
            ["TR-011", "Observability", "Log retention minimal 30 hari, metrics 90 hari", "30d logs, 90d metrics", "P2"],
            ["TR-012", "Observability", "Alert response time < 5 menit untuk P1 incidents", "< 5 min MTTA", "P1"],
            ["TR-013", "Cost", "Infrastructure cost tidak melebihi 20% dari revenue", "Infra < 20% revenue", "P2"],
            ["TR-014", "Compliance", "Platform harus lulus security audit tahunan (OWASP ASVS L2)", "ASVS L2 compliance", "P2"],
            ["TR-015", "DR", "Recovery Time Objective (RTO) < 4 jam", "< 4 hours RTO", "P1"],
            ["TR-016", "DR", "Recovery Point Objective (RPO) < 1 jam", "< 1 hour RPO", "P1"],
        ],
        title="Kebutuhan Teknologi",
        table_number=8
    )

    # ==========================================================================
    # SECTION 3: ARCHITECTURE PRINCIPLES (UPDATED)
    # ==========================================================================
    add_heading(doc, "3. Prinsip Arsitektur (Diperbarui)", level=1)

    add_paragraph(doc,
        "Prinsip arsitektur diperbarui dengan prinsip-prinsip spesifik untuk "
        "domain teknologi yang telah divalidasi melalui analisis Phase D."
    )

    tech_principles = [
        {
            "name": "Cloud-Native by Default",
            "statement": "Semua komponen harus dirancang cloud-native: containerized, stateless, horizontally scalable, dan self-healing",
            "rationale": "Platform harus scale 50x selama peak SNBP dan scale down saat off-peak. Cloud-native memungkinkan ini secara cost-effective.",
            "implications": "Docker mandatory, Kubernetes deployment, no local file dependencies, health checks pada semua services, graceful shutdown handling"
        },
        {
            "name": "Infrastructure as Code (IaC) Only",
            "statement": "Semua infrastruktur harus didefinisikan sebagai code (Terraform/Helm). Manual changes dilarang pada production.",
            "rationale": "Reproducibility, auditability, dan disaster recovery bergantung pada kemampuan recreate infrastructure from code.",
            "implications": "Terraform untuk semua GCP resources, Helm charts untuk semua Kubernetes deployments, Git sebagai source of truth, automated drift detection"
        },
        {
            "name": "Shift-Left Security",
            "statement": "Security testing dan enforcement harus dilakukan sedini mungkin dalam development lifecycle, bukan sebagai gates di akhir.",
            "rationale": "Fixing security issues di production 100x lebih mahal dari fixing di development. Platform menangani data sensitif siswa.",
            "implications": "SAST/DAST dalam CI pipeline, dependency vulnerability scanning, container image scanning, security-focused code review checklist, automated compliance checks"
        },
        {
            "name": "Observe Everything",
            "statement": "Setiap komponen harus emit metrics, logs, dan traces. Jika tidak bisa di-observe, jangan deploy ke production.",
            "rationale": "Deteksi dini masalah, root cause analysis cepat, dan capacity planning akurat memerlukan observability menyeluruh.",
            "implications": "OpenTelemetry instrumentation mandatory, structured JSON logging, custom business metrics, SLO-based alerting, error budget policies"
        },
        {
            "name": "Cost-Aware Architecture",
            "statement": "Setiap technology decision harus mempertimbangkan total cost of ownership termasuk operational cost, bukan hanya initial setup.",
            "rationale": "Sebagai startup dengan funding terbatas, cost efficiency merupakan survival factor. Arsitektur harus sustainable secara finansial.",
            "implications": "Spot/preemptible instances untuk non-critical workloads, auto-scaling policies yang aggressive, resource limits per service, regular cost reviews, committed use discounts"
        },
        {
            "name": "Minimal Viable Infrastructure",
            "statement": "Start minimal dan grow incrementally. Jangan over-provision atau over-engineer infrastructure untuk kebutuhan future yang belum tervalidasi.",
            "rationale": "Startup resources terbatas. Better to scale up than to waste budget on unused capacity.",
            "implications": "Right-sized instances, incremental Kubernetes node pool scaling, managed services over self-hosted when cost-effective, evaluate build vs buy for each component"
        },
    ]

    for p in tech_principles:
        add_paragraph(doc, f"Prinsip: {p['name']}", bold=True)
        add_paragraph(doc, f"Pernyataan: {p['statement']}")
        add_paragraph(doc, f"Rasional: {p['rationale']}")
        add_paragraph(doc, f"Implikasi: {p['implications']}")
        doc.add_paragraph()

    # ==========================================================================
    # SECTION 4: STATEMENT OF ARCHITECTURE WORK (FINAL)
    # ==========================================================================
    add_heading(doc, "4. Pernyataan Pekerjaan Arsitektur (Final)", level=1)

    add_paragraph(doc,
        "Statement of Architecture Work ini merupakan versi final yang mencakup "
        "seluruh hasil dari Phase A hingga Phase D, memberikan gambaran lengkap "
        "tentang arsitektur enterprise LangkahKampus yang telah dirancang."
    )

    add_heading(doc, "4.1 Ringkasan Eksekutif", level=2)

    add_paragraph(doc,
        "Proyek Enterprise Architecture LangkahKampus telah berhasil merancang "
        "arsitektur komprehensif untuk platform EduTech yang menyelesaikan "
        "permasalahan prediksi SNBP di Indonesia. Arsitektur yang dirancang "
        "mencakup empat domain utama:"
    )

    add_numbered_list(doc, [
        "Business Architecture: Mendefinisikan proses bisnis baru: onboarding wizard, prediksi all-in-one, monetisasi freemium + referral, dan guru evaluatif pasif",
        "Data Architecture: Merancang data entities termasuk referral_tracking, predictions dengan counter limit, invite_codes, dan guru_comments",
        "Application Architecture: Mendesain arsitektur PHP monolith + FastAPI ML microservice dengan halaman prediksi all-in-one, API referral, dan dashboard guru",
        "Technology Architecture: Memilih PHP 8.x + Nginx sebagai web stack, FastAPI untuk ML serving, MySQL/PostgreSQL untuk database, dan Cloudflare untuk CDN/security",
    ])

    add_heading(doc, "4.2 Ringkasan Keputusan Arsitektur", level=2)

    add_table(doc,
        headers=["Domain", "Keputusan Utama", "Teknologi/Pendekatan"],
        rows=[
            ["Business", "Freemium + referral viral loop", "3 prediksi gratis, lalu bayar (Rp15K-25K) atau referral (5 klik unik = 3 tambahan)"],
            ["Business", "ML as core differentiator", "XGBoost + LightGBM ensemble prediction all-in-one"],
            ["Business", "Guru sebagai evaluator pasif", "Invite via kode 6 karakter, maks 2 per siswa, lihat & komentar"],
            ["Data", "MySQL/PostgreSQL as primary database", "Relational + JSON support, referral_tracking table, predictions counter"],
            ["Data", "Redis for caching & ML features", "Feature store + session management"],
            ["Data", "UU PDP compliance by design", "Encryption, audit trails, data minimization"],
            ["Application", "PHP monolith + ML microservice", "PHP 8.x untuk web app, FastAPI untuk ML serving"],
            ["Application", "All-in-one prediction page", "Gauge + Choice-2 Trap + peer stats + recommendations dalam satu halaman"],
            ["Application", "Referral tracking API", "IP-based unique click detection, automated unlock"],
            ["Technology", "VPS + Cloudflare CDN", "Cost-effective hosting dengan edge caching dan DDoS protection"],
            ["Technology", "PHP 8.x + Nginx", "Mature stack, banyak hosting support, OPcache untuk performa"],
            ["Technology", "GitHub Actions CI/CD", "Automated testing dan deployment"],
            ["Technology", "Cloudflare for edge/CDN", "DDoS protection, global caching, SSL"],
        ],
        title="Ringkasan Keputusan Arsitektur (Semua Fase)",
        table_number=9
    )

    add_heading(doc, "4.3 Ringkasan Roadmap Implementasi", level=2)

    add_table(doc,
        headers=["Fase", "Periode", "Tujuan Bisnis", "Milestone Teknis", "Metrik Keberhasilan"],
        rows=[
            ["Fase 1: Foundation", "Bulan 1-4", "MVP launch, 1000 beta users", "Platform PHP live, ML prediction v1, referral system, payment gateway", "Platform operational, prediction >75%, <2s latency"],
            ["Fase 2: Enhancement", "Bulan 5-8", "10K users, first revenue dari freemium", "DiCE XAI, Peta Universitas, observability, guru dashboard", "Prediction >82%, 10% conversion rate"],
            ["Fase 3: Scale", "Bulan 9-12", "100K users, sustainable revenue", "Performance optimization, ML model v2, analytics, DR tested", "500K concurrent capability, 99.9% uptime, prediction >85%"],
        ],
        title="Ringkasan Roadmap Implementasi",
        table_number=10
    )

    add_heading(doc, "4.4 Ringkasan Risiko", level=2)

    add_table(doc,
        headers=["Risiko", "Probabilitas", "Dampak", "Mitigasi"],
        rows=[
            ["Insufficient historical SNBP data for ML training", "Sedang", "Tinggi", "Crowdsourcing + school partnerships + synthetic data augmentation"],
            ["Peak traffic exceeds capacity planning", "Sedang", "Tinggi", "Aggressive auto-scaling + load testing + graceful degradation"],
            ["UU PDP compliance failure", "Rendah", "Sangat Tinggi", "Privacy by design + legal review + regular compliance audit"],
            ["Key team member leaves", "Sedang", "Tinggi", "Documentation, knowledge sharing, cross-training, competitive compensation"],
            ["Cloud cost overrun during peak", "Sedang", "Sedang", "Budget alerts, reserved instances, auto-scale limits, cost optimization"],
            ["ML model accuracy below target", "Sedang", "Tinggi", "Iterative improvement, A/B testing, ensemble methods, data quality focus"],
        ],
        title="Risiko Utama dan Mitigasi",
        table_number=11
    )

    add_heading(doc, "4.5 Kesimpulan", level=2)

    add_paragraph(doc,
        "Arsitektur enterprise yang telah dirancang untuk LangkahKampus memberikan "
        "fondasi yang kuat untuk membangun platform EduTech yang scalable, secure, "
        "dan sustainable. Dengan pendekatan PHP monolith untuk web application "
        "dikombinasikan dengan FastAPI microservice untuk ML prediction, arsitektur "
        "ini memungkinkan tim kecil (4 orang) untuk mengembangkan dan mengoperasikan "
        "platform yang melayani ratusan ribu siswa secara efisien."
    )

    add_paragraph(doc,
        "Keputusan arsitektur kunci seperti penggunaan PHP 8.x sebagai backend utama, "
        "halaman prediksi all-in-one, sistem referral untuk pertumbuhan organik, "
        "dan FastAPI untuk ML serving telah dipilih berdasarkan pertimbangan teknis, "
        "ekonomis, dan keselarasan dengan kebutuhan bisnis LangkahKampus. Arsitektur "
        "ini juga memperhatikan aspek compliance (UU PDP), validasi referral link, "
        "dan pembatasan prediksi yang esensial untuk monetisasi platform."
    )

    add_paragraph(doc,
        "Dengan implementasi bertahap melalui 3 fase selama 12 bulan, LangkahKampus "
        "dapat memvalidasi asumsi bisnis secara iteratif sambil membangun infrastruktur "
        "yang mampu mendukung pertumbuhan jangka panjang. Arsitektur ini tidak hanya "
        "mendukung kebutuhan saat ini, tetapi juga memberikan fleksibilitas untuk "
        "evolusi di masa depan seiring pertumbuhan platform dan ekspansi ke layanan "
        "pendidikan lainnya."
    )

    # References
    references = [
        "The Open Group. (2022). TOGAF Standard, 10th Edition. The Open Group.",
        "Burns, B., Beda, J., Hightower, K., & Evenson, L. (2022). Kubernetes: Up and Running (3rd ed.). O'Reilly Media.",
        "Morris, K. (2020). Infrastructure as Code (2nd ed.). O'Reilly Media.",
        "Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (2016). Site Reliability Engineering. O'Reilly Media.",
        "Kim, G., Humble, J., Debois, P., & Willis, J. (2016). The DevOps Handbook. IT Revolution Press.",
        "Richardson, C. (2018). Microservices Patterns. Manning Publications.",
        "Newman, S. (2021). Building Microservices (2nd ed.). O'Reilly Media.",
        "Majors, C., Fong-Jones, L., & Miranda, G. (2022). Observability Engineering. O'Reilly Media.",
        "Julien, V. (2021). Learning Helm: Managing Apps on Kubernetes. O'Reilly Media.",
        "Google Cloud. (2024). Google Kubernetes Engine Documentation. https://cloud.google.com/kubernetes-engine/docs",
        "HashiCorp. (2024). Terraform Documentation. https://www.terraform.io/docs",
        "Cloudflare. (2024). Cloudflare Documentation. https://developers.cloudflare.com",
        "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi.",
        "OWASP Foundation. (2021). OWASP Top Ten 2021. https://owasp.org/Top10/",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.",
    ]

    add_references(doc, references)

    # Save document
    save_document(doc, "Stage6_Technology_Architecture.docx")
    print("Stage 6: Dokumen berhasil di-generate!")
    print(f"Total paragraphs: {len(doc.paragraphs)}")
    print(f"Total tables: {len(doc.tables)}")


if __name__ == "__main__":
    generate_stage6()
