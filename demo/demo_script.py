"""
LangkahKampus End-to-End Demo Script.

Demonstrates the complete AI prediction pipeline:
1. Health check - verify system status
2. Predict - ML-based SNBP admission probability
3. Advisor - AI-powered academic guidance (single turn)
4. Advisor - Multi-turn conversation with history
5. Recommend - Alternative program suggestions

Usage:
    # Mock mode (no server required, for demo recording)
    python demo/demo_script.py --mock

    # Live mode (requires running backend)
    python demo/demo_script.py --base-url http://localhost:8000
"""

import argparse
import json
import sys
import time

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
DIM = "\033[2m"


def color(text, code):
    """Wrap text with ANSI color code."""
    return f"{code}{text}{RESET}"


def header(title):
    """Print a section header."""
    print()
    print(color("=" * 60, CYAN))
    print(color(f"  {title}", BOLD + CYAN))
    print(color("=" * 60, CYAN))
    print()


def step_header(num, title):
    """Print a step header."""
    print()
    print(color(f"--- Step {num}: {title} ---", BOLD + YELLOW))
    print()


def print_json(data, indent=2):
    """Pretty-print JSON data with colors."""
    formatted = json.dumps(data, indent=indent, ensure_ascii=False)
    # Simple syntax highlighting
    for line in formatted.split("\n"):
        if '": ' in line:
            key_part = line.split('": ')[0] + '"'
            val_part = '": '.join(line.split('": ')[1:])
            print(f"  {color(key_part, BLUE)}: {color(val_part, GREEN)}")
        else:
            print(f"  {color(line, DIM)}")


def elapsed(start):
    """Format elapsed time."""
    ms = (time.time() - start) * 1000
    return color(f"({ms:.0f}ms)", DIM)


# --- Mock Responses ---

MOCK_HEALTH = {
    "status": "healthy",
    "model_loaded": True,
    "sidata_loaded": True,
    "sidata_programs": 4500,
    "sidata_universities": 98,
    "advisor_configured": True,
}

MOCK_PREDICT = {
    "success": True,
    "probability": 72.5,
    "confidence_lower": 0.65,
    "confidence_upper": 0.80,
    "variables": [
        {"name": "Rasio Kompetisi", "weight": 0.30, "raw_value": 8.5, "normalized_score": 0.72, "description": "Perbandingan pendaftar vs daya tampung"},
        {"name": "Nilai Rata-rata", "weight": 0.25, "raw_value": 88.5, "normalized_score": 0.85, "description": "Rata-rata nilai rapor semester 1-5"},
        {"name": "Peringkat Sekolah", "weight": 0.20, "raw_value": "5/200", "normalized_score": 0.90, "description": "Posisi peringkat di sekolah"},
        {"name": "Akreditasi", "weight": 0.15, "raw_value": "A", "normalized_score": 1.0, "description": "Akreditasi sekolah (A/B/C)"},
        {"name": "Daya Tampung", "weight": 0.05, "raw_value": 60, "normalized_score": 0.65, "description": "Kuota penerimaan program studi"},
        {"name": "Tren Pendaftar", "weight": 0.05, "raw_value": 0.1, "normalized_score": 0.45, "description": "Perubahan jumlah pendaftar YoY"},
    ],
    "recommendations": [
        {"name": "TEKNIK SIPIL", "university": "Universitas Indonesia", "ratio": 6.2, "daya_tampung": 80, "comparison": "Lebih mudah", "predicted_probability": 78.2},
        {"name": "TEKNIK INFORMATIKA", "university": "Universitas Brawijaya", "ratio": 7.1, "daya_tampung": 70, "comparison": "Setara", "predicted_probability": 74.5},
    ],
    "input_summary": {
        "avg_score": 88.5,
        "ranking": "5/200",
        "school_accreditation": "A",
        "target_program": "TEKNIK INFORMATIKA",
        "target_university": "Institut Teknologi Bandung",
    },
    "timestamp": "2024-01-15T10:30:00",
}

MOCK_ADVISOR_1 = {
    "reply": (
        "Berdasarkan prediksi, peluang Anda diterima di Teknik Informatika ITB adalah 72.5% "
        "(kategori tinggi). Ini adalah hasil yang sangat baik!\n\n"
        "**Faktor pendukung utama:**\n"
        "- Nilai rata-rata 88.5 sangat kompetitif\n"
        "- Peringkat 5 dari 200 siswa menunjukkan konsistensi akademik\n"
        "- Akreditasi sekolah A memberikan bobot tambahan\n\n"
        "**Saran untuk memaksimalkan peluang:**\n"
        "1. Pertahankan nilai di semester 5\n"
        "2. Lengkapi portofolio prestasi non-akademik\n"
        "3. Siapkan pilihan kedua sebagai cadangan strategis"
    ),
    "suggestions": [
        "Apa program studi alternatif yang cocok?",
        "Bagaimana strategi pilihan kedua SNBP?",
        "Apa yang harus dipersiapkan sekarang?",
    ],
}

MOCK_ADVISOR_2 = {
    "reply": (
        "Untuk pilihan kedua SNBP, dengan profil Anda yang kuat, saya sarankan:\n\n"
        "**Strategi pilihan kedua:**\n"
        "1. **Teknik Sipil UI** - Rasio kompetisi lebih rendah (6.2), peluang ~78%\n"
        "2. **Teknik Informatika UB** - Setara kompetisinya, peluang ~74%\n\n"
        "**Tips penting:**\n"
        "- Pilihan 2 sebaiknya memiliki rasio kompetisi lebih rendah\n"
        "- Pertimbangkan PTN di provinsi yang sama untuk prioritas\n"
        "- Pastikan pilihan 2 tetap sesuai minat Anda\n\n"
        "Dengan peluang 72.5% di pilihan 1, Anda sudah dalam posisi baik. "
        "Pilihan 2 yang strategis akan memperkuat peluang keseluruhan."
    ),
    "suggestions": [
        "Jelaskan lebih detail tentang Teknik Sipil UI",
        "Bagaimana cara memilih PTN terdekat?",
        "Kapan pengumuman SNBP?",
    ],
}

MOCK_RECOMMEND = {
    "success": True,
    "target_program": "TEKNIK INFORMATIKA",
    "recommendations": [
        {"name": "TEKNIK SIPIL", "university": "Universitas Indonesia", "ratio": 6.2, "daya_tampung": 80, "comparison": "Rasio 27% lebih rendah", "predicted_probability": 78.2},
        {"name": "TEKNIK INFORMATIKA", "university": "Universitas Brawijaya", "ratio": 7.1, "daya_tampung": 70, "comparison": "Rasio 16% lebih rendah", "predicted_probability": 74.5},
        {"name": "SISTEM INFORMASI", "university": "Institut Teknologi Bandung", "ratio": 5.8, "daya_tampung": 50, "comparison": "Rasio 32% lebih rendah", "predicted_probability": 80.1},
        {"name": "TEKNIK ELEKTRO", "university": "Institut Teknologi Bandung", "ratio": 7.5, "daya_tampung": 90, "comparison": "Rasio 12% lebih rendah", "predicted_probability": 73.0},
        {"name": "ILMU KOMPUTER", "university": "Universitas Gadjah Mada", "ratio": 6.8, "daya_tampung": 65, "comparison": "Rasio 20% lebih rendah", "predicted_probability": 76.3},
    ],
}


# --- Demo Flow ---

SAMPLE_STUDENT = {
    "scores": {
        "Matematika": {"sem1": 87, "sem2": 88, "sem3": 89, "sem4": 90, "sem5": 91},
        "Fisika": {"sem1": 85, "sem2": 86, "sem3": 87, "sem4": 88, "sem5": 90},
        "Kimia": {"sem1": 83, "sem2": 84, "sem3": 86, "sem4": 87, "sem5": 88},
        "Biologi": {"sem1": 82, "sem2": 83, "sem3": 85, "sem4": 86, "sem5": 87},
        "BahasaIndonesia": {"sem1": 88, "sem2": 89, "sem3": 90, "sem4": 91, "sem5": 92},
        "BahasaInggris": {"sem1": 86, "sem2": 87, "sem3": 88, "sem4": 89, "sem5": 90},
    },
    "school_ranking": 5,
    "total_students": 200,
    "school_accreditation": "A",
    "target_program_id": "TEKNIK INFORMATIKA",
    "jurusan": "IPA",
}


def do_request_live(base_url, method, path, payload=None):
    """Make a live HTTP request to the backend."""
    try:
        import httpx
    except ImportError:
        try:
            import requests as httpx
        except ImportError:
            print(color("ERROR: Neither httpx nor requests is installed.", RED))
            print("Install with: pip install httpx")
            sys.exit(1)

    url = f"{base_url}{path}"
    start = time.time()

    try:
        if method == "GET":
            if hasattr(httpx, "Client"):
                with httpx.Client(timeout=30.0) as client:
                    resp = client.get(url)
            else:
                resp = httpx.get(url, timeout=30)
        else:
            if hasattr(httpx, "Client"):
                with httpx.Client(timeout=30.0) as client:
                    resp = client.post(url, json=payload)
            else:
                resp = httpx.post(url, json=payload, timeout=30)

        duration = time.time() - start
        print(f"  {color('Status:', DIM)} {color(str(resp.status_code), GREEN)} {elapsed(start)}")

        if resp.status_code == 200:
            return resp.json(), duration
        else:
            print(color(f"  Error: {resp.text[:200]}", RED))
            return None, duration
    except Exception as e:
        duration = time.time() - start
        print(color(f"  Connection error: {e}", RED))
        return None, duration


def do_request_mock(method, path, payload=None):
    """Simulate an API response in mock mode."""
    time.sleep(0.3)  # Simulate network delay
    start = time.time()

    if path == "/api/health":
        result = MOCK_HEALTH
    elif path == "/api/predict":
        result = MOCK_PREDICT
    elif path == "/api/advisor":
        # Check if this is a multi-turn request
        if payload and payload.get("history"):
            result = MOCK_ADVISOR_2
        else:
            result = MOCK_ADVISOR_1
    elif path == "/api/recommend":
        result = MOCK_RECOMMEND
    else:
        result = {"error": "Unknown endpoint"}

    duration = time.time() - start + 0.3
    print(f"  {color('Status:', DIM)} {color('200 (mock)', GREEN)} {elapsed(start)}")
    return result, duration


def run_demo(base_url, mock_mode):
    """Run the complete demo flow."""
    header("LangkahKampus - AI-Powered SNBP Prediction")
    print(f"  {color('Platform:', BOLD)} LangkahKampus")
    print(f"  {color('Mode:', BOLD)} {'Mock (simulated)' if mock_mode else 'Live'}")
    if not mock_mode:
        print(f"  {color('Backend:', BOLD)} {base_url}")
    print(f"  {color('AI Stack:', BOLD)} XGBoost (AMD GPU) + Fireworks AI LLM")
    print(f"  {color('Hardware:', BOLD)} Trained on AMD Instinct MI210 (ROCm)")

    def request(method, path, payload=None):
        if mock_mode:
            return do_request_mock(method, path, payload)
        return do_request_live(base_url, method, path, payload)

    # Step 1: Health Check
    step_header(1, "System Health Check")
    print(f"  {color('GET', MAGENTA)} /api/health")
    result, _ = request("GET", "/api/health")
    if result:
        print()
        print(f"  {color('System Status:', BOLD)}")
        print(f"    Model Loaded:     {color('Yes' if result.get('model_loaded') else 'No', GREEN if result.get('model_loaded') else RED)}")
        print(f"    SIDATA Loaded:    {color('Yes' if result.get('sidata_loaded') else 'No', GREEN if result.get('sidata_loaded') else RED)}")
        print(f"    Programs:         {color(str(result.get('sidata_programs', 0)), CYAN)}")
        print(f"    Universities:     {color(str(result.get('sidata_universities', 0)), CYAN)}")
        print(f"    Advisor Ready:    {color('Yes' if result.get('advisor_configured') else 'Fallback', GREEN if result.get('advisor_configured') else YELLOW)}")

    # Step 2: Prediction
    step_header(2, "SNBP Admission Prediction")
    print(f"  {color('POST', MAGENTA)} /api/predict")
    print(f"  {color('Student:', BOLD)} Ranking 5/200, Akreditasi A, Target: Teknik Informatika ITB")
    print()
    result, _ = request("POST", "/api/predict", SAMPLE_STUDENT)
    if result and result.get("success"):
        prob = result["probability"]
        prob_color = GREEN if prob >= 60 else (YELLOW if prob >= 40 else RED)
        print()
        print(f"  {color('Prediction Result:', BOLD)}")
        print(f"    Probability:      {color(f'{prob}%', BOLD + prob_color)}")
        print(f"    Confidence:       [{result.get('confidence_lower', 0):.0%} - {result.get('confidence_upper', 0):.0%}]")
        print()
        print(f"  {color('Variable Breakdown:', BOLD)}")
        for var in result.get("variables", [])[:6]:
            bar_len = int(var["normalized_score"] * 20)
            bar = color("█" * bar_len, CYAN) + color("░" * (20 - bar_len), DIM)
            print(f"    {var['name']:25s} {bar} {var['normalized_score']:.2f} (weight: {var['weight']:.0%})")

    prediction_context = None
    if result and result.get("success"):
        prediction_context = {
            "probability": result["probability"],
            "variables": result.get("variables", []),
            "input_summary": result.get("input_summary", {}),
        }

    # Step 3: AI Advisor (single turn)
    step_header(3, "AI Advisor - Single Turn")
    advisor_message = "Jelaskan hasil prediksi saya dan berikan saran untuk meningkatkan peluang"
    print(f"  {color('POST', MAGENTA)} /api/advisor")
    print(f"  {color('User:', BOLD)} {advisor_message}")
    print()

    advisor_payload = {
        "message": advisor_message,
        "context": prediction_context,
    }
    result, _ = request("POST", "/api/advisor", advisor_payload)
    if result and result.get("reply"):
        print(f"  {color('AI Advisor:', BOLD + GREEN)}")
        for line in result["reply"].split("\n"):
            print(f"    {line}")
        if result.get("suggestions"):
            print()
            print(f"  {color('Suggestions:', DIM)}")
            for s in result["suggestions"]:
                print(f"    - {s}")

    # Step 4: AI Advisor (multi-turn with history)
    step_header(4, "AI Advisor - Multi-turn Conversation")
    follow_up = "Bagaimana strategi pilihan kedua SNBP saya?"
    print(f"  {color('POST', MAGENTA)} /api/advisor (with conversation history)")
    print(f"  {color('User:', BOLD)} {follow_up}")
    print(f"  {color('History:', DIM)} 1 previous exchange included")
    print()

    history = [
        {"role": "user", "content": advisor_message},
        {"role": "assistant", "content": result["reply"] if result else ""},
    ]

    advisor_payload_2 = {
        "message": follow_up,
        "context": prediction_context,
        "history": history,
    }
    result2, _ = request("POST", "/api/advisor", advisor_payload_2)
    if result2 and result2.get("reply"):
        print(f"  {color('AI Advisor:', BOLD + GREEN)}")
        for line in result2["reply"].split("\n"):
            print(f"    {line}")
        if result2.get("suggestions"):
            print()
            print(f"  {color('Suggestions:', DIM)}")
            for s in result2["suggestions"]:
                print(f"    - {s}")

    # Step 5: Recommendations
    step_header(5, "Smart Program Recommendations")
    print(f"  {color('POST', MAGENTA)} /api/recommend")
    print()

    recommend_payload = {
        "scores": SAMPLE_STUDENT["scores"],
        "school_ranking": SAMPLE_STUDENT["school_ranking"],
        "total_students": SAMPLE_STUDENT["total_students"],
        "school_accreditation": SAMPLE_STUDENT["school_accreditation"],
        "target_program_id": SAMPLE_STUDENT["target_program_id"],
        "limit": 5,
    }
    result3, _ = request("POST", "/api/recommend", recommend_payload)
    if result3 and result3.get("success"):
        print(f"  {color('Target:', BOLD)} {result3.get('target_program', 'N/A')}")
        print(f"  {color('Alternative Programs:', BOLD)}")
        print()
        for i, rec in enumerate(result3.get("recommendations", []), 1):
            prob_str = f"{rec.get('predicted_probability', 0):.1f}%" if rec.get("predicted_probability") else "N/A"
            print(f"    {color(str(i) + '.', CYAN)} {color(rec['name'], BOLD)} - {rec['university']}")
            print(f"       Ratio: {rec['ratio']} | Daya Tampung: {rec['daya_tampung']} | Predicted: {color(prob_str, GREEN)}")
            print(f"       {color(rec['comparison'], DIM)}")

    # Summary
    header("Demo Complete!")
    print(f"  {color('LangkahKampus AI Platform:', BOLD)}")
    print(f"    - XGBoost ML model trained on AMD Instinct MI210 GPU")
    print(f"    - Fireworks AI LLM for contextual academic advising")
    print(f"    - Multi-turn conversation for deeper guidance")
    print(f"    - Smart recommendations based on student profile")
    print()
    print(f"  {color('Powered by AMD Developer Cloud', BOLD + RED)}")
    print(f"  {color('ROCm | AMD Instinct MI210 | XGBoost GPU Acceleration', DIM)}")
    print()


def main():
    """Parse arguments and run demo."""
    parser = argparse.ArgumentParser(
        description="LangkahKampus End-to-End Demo Script"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode (simulated responses, no server needed)",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the AI backend (default: http://localhost:8000)",
    )

    args = parser.parse_args()

    # If no base-url override and not mock mode, default to live
    mock_mode = args.mock

    run_demo(args.base_url, mock_mode)


if __name__ == "__main__":
    main()
