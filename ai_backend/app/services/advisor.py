"""Fireworks AI integration for SNBP advisor chatbot."""

import re
from typing import Any, Dict, List, Optional

import httpx

from ..config import settings


# Maximum allowed message length (characters)
MAX_MESSAGE_LENGTH = 2000

# Patterns that may indicate prompt injection attempts
INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?)",
    r"(?i)you\s+are\s+now\s+",
    r"(?i)system\s*:\s*",
    r"(?i)new\s+instructions?\s*:",
    r"(?i)forget\s+(everything|all|your\s+instructions)",
    r"(?i)disregard\s+(all\s+)?(previous|prior|above)",
]


SYSTEM_PROMPT = """Kamu adalah penasihat akademik AI untuk LangkahKampus, platform prediksi penerimaan SNBP (Seleksi Nasional Berdasarkan Prestasi) di Indonesia.

Tugasmu:
1. Jelaskan hasil prediksi penerimaan mahasiswa dalam Bahasa Indonesia yang mudah dipahami
2. Berikan saran strategis untuk meningkatkan peluang SNBP
3. Jawab pertanyaan tentang strategi SNBP, pemilihan program studi, dan persiapan

Panduan:
- Gunakan Bahasa Indonesia yang ramah dan mendukung
- Berikan saran yang spesifik dan actionable
- Jika peluang rendah, jangan mematahkan semangat tapi berikan alternatif
- Jelaskan faktor-faktor yang mempengaruhi peluang (rasio kompetisi, nilai, peringkat, akreditasi)
- Sebutkan bahwa prediksi adalah estimasi, bukan jaminan

Konteks SNBP:
- SNBP menggunakan nilai rapor semester 1-5
- Peringkat di sekolah sangat penting
- Akreditasi sekolah berpengaruh
- Setiap siswa bisa memilih 2 program studi
- Pilihan 1 harus dari PTN terdekat (provinsi yang sama atau lintas provinsi berdasarkan ketentuan)
"""


def _sanitize_message(message: str) -> str:
    """
    Sanitize user message to mitigate basic prompt injection attacks.

    - Truncates messages that exceed MAX_MESSAGE_LENGTH
    - Strips patterns that attempt to override system prompt
    """
    # Truncate overly long messages
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH] + "..."

    # Remove potential prompt injection patterns
    for pattern in INJECTION_PATTERNS:
        message = re.sub(pattern, "[filtered]", message)

    return message.strip()


async def get_advisor_response(
    message: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Get AI advisor response using Fireworks AI API.

    Returns dict with 'reply' and 'suggestions' keys.
    """
    # Sanitize user message to mitigate prompt injection
    message = _sanitize_message(message)

    if not settings.FIREWORKS_API_KEY:
        return _fallback_response(message, context)

    # Build context message if prediction results are available
    context_msg = ""
    if context:
        if "probability" in context:
            context_msg += f"\nHasil prediksi: {context['probability']}% peluang diterima."
        if "variables" in context:
            context_msg += "\nBreakdown variabel:"
            for var in context["variables"]:
                context_msg += (
                    f"\n- {var.get('name', '')}: {var.get('normalized_score', 0):.2f} "
                    f"(bobot {var.get('weight', 0):.0%})"
                )
        if "input_summary" in context:
            summary = context["input_summary"]
            if "target_program" in summary:
                context_msg += f"\nProgram target: {summary['target_program']}"
            if "avg_score" in summary:
                context_msg += f"\nNilai rata-rata: {summary['avg_score']}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    if context_msg:
        messages.append(
            {"role": "system", "content": f"Data prediksi siswa:{context_msg}"}
        )

    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.FIREWORKS_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.FIREWORKS_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.FIREWORKS_MODEL,
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            data = response.json()

            reply = data["choices"][0]["message"]["content"]

            # Generate follow-up suggestions
            suggestions = _generate_suggestions(context)

            return {"reply": reply, "suggestions": suggestions}

    except Exception as e:
        print(f"Fireworks AI API error: {e}")
        return _fallback_response(message, context)


def _fallback_response(
    message: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Provide a fallback response when Fireworks AI is not available."""
    if not context or "probability" not in context:
        reply = (
            "Maaf, layanan AI advisor belum dikonfigurasi. "
            "Silakan lakukan prediksi terlebih dahulu untuk mendapatkan analisis "
            "peluang SNBP Anda. Setelah itu, saya dapat membantu menjelaskan hasilnya."
        )
    else:
        prob = context.get("probability", 0)
        if prob >= 70:
            level = "tinggi"
            advice = (
                "Pertahankan nilai dan peringkat Anda. "
                "Pastikan portofolio dan prestasi non-akademik juga lengkap."
            )
        elif prob >= 40:
            level = "sedang"
            advice = (
                "Tingkatkan nilai di semester 5 dan pertimbangkan "
                "pilihan kedua dengan rasio kompetisi lebih rendah."
            )
        else:
            level = "rendah"
            advice = (
                "Pertimbangkan program studi alternatif dengan persaingan lebih rendah, "
                "atau fokus pada jalur SNBT sebagai cadangan."
            )

        reply = (
            f"Berdasarkan prediksi, peluang Anda {prob}% (kategori {level}). "
            f"{advice}\n\n"
            "Catatan: AI advisor tidak terkonfigurasi sepenuhnya. "
            "Untuk analisis lebih detail, hubungi admin untuk mengaktifkan fitur ini."
        )

    suggestions = _generate_suggestions(context)
    return {"reply": reply, "suggestions": suggestions}


def _generate_suggestions(context: Optional[Dict[str, Any]] = None) -> List[str]:
    """Generate follow-up question suggestions."""
    base_suggestions = [
        "Bagaimana cara meningkatkan peluang saya?",
        "Apa program studi alternatif yang cocok?",
        "Jelaskan strategi pemilihan SNBP",
    ]

    if context and "probability" in context:
        prob = context.get("probability", 0)
        if prob < 50:
            base_suggestions.insert(0, "Kenapa peluang saya rendah?")
        elif prob >= 70:
            base_suggestions.insert(0, "Apa yang harus saya persiapkan sekarang?")

    return base_suggestions[:4]
