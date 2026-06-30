"""ML model loading, prediction, and SIDATA data management."""

import os
import re
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np

from ..config import settings


class SIDATAStore:
    """In-memory store for SIDATA program data parsed from SQL file."""

    def __init__(self):
        self.programs: Dict[str, Dict[str, Any]] = {}  # keyed by kode_prodi
        self.programs_by_name: Dict[str, List[Dict[str, Any]]] = {}  # keyed by nama_prodi
        self.universities: Dict[str, str] = {}  # kode_univ -> nama_univ
        self._loaded = False

    def load(self, sql_path: Optional[str] = None):
        """Parse seed_sidata.sql and load all program data into memory."""
        if sql_path is None:
            sql_path = settings.SIDATA_SQL_PATH

        if not os.path.exists(sql_path):
            print(f"WARNING: SIDATA SQL file not found at {sql_path}")
            self._loaded = True
            return

        with open(sql_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse universities
        univ_pattern = re.compile(
            r"INSERT INTO sidata_universitas \(kode_univ, nama_univ, portal_univ\) "
            r"VALUES \('(\d+)', '([^']+)', '([^']*?)'\);",
            re.IGNORECASE,
        )
        for match in univ_pattern.finditer(content):
            kode_univ = match.group(1)
            nama_univ = match.group(2)
            self.universities[kode_univ] = nama_univ

        # Parse study programs
        prodi_pattern = re.compile(
            r"INSERT INTO sidata_prodi \(kode_univ, kode_prodi, nama_prodi, jenjang, "
            r"daya_tampung_2023, peminat_2018, peminat_2019, peminat_2020, peminat_2021, "
            r"peminat_2022, daya_tampung_2018, daya_tampung_2019, daya_tampung_2020, "
            r"daya_tampung_2021, daya_tampung_2022\) VALUES "
            r"\('(\d+)', '(\d+)', '([^']+)', '([^']+)', (\d+), "
            r"(\d+), (\d+), (\d+), (\d+), (\d+), "
            r"(\d+), (\d+), (\d+), (\d+), (\d+)\);",
            re.IGNORECASE,
        )

        for match in prodi_pattern.finditer(content):
            program = {
                "kode_univ": match.group(1),
                "kode_prodi": match.group(2),
                "nama_prodi": match.group(3),
                "jenjang": match.group(4),
                "daya_tampung_2023": int(match.group(5)),
                "peminat_2018": int(match.group(6)),
                "peminat_2019": int(match.group(7)),
                "peminat_2020": int(match.group(8)),
                "peminat_2021": int(match.group(9)),
                "peminat_2022": int(match.group(10)),
                "daya_tampung_2018": int(match.group(11)),
                "daya_tampung_2019": int(match.group(12)),
                "daya_tampung_2020": int(match.group(13)),
                "daya_tampung_2021": int(match.group(14)),
                "daya_tampung_2022": int(match.group(15)),
                "nama_univ": self.universities.get(match.group(1), ""),
            }

            self.programs[program["kode_prodi"]] = program

            name_key = program["nama_prodi"].upper()
            if name_key not in self.programs_by_name:
                self.programs_by_name[name_key] = []
            self.programs_by_name[name_key].append(program)

        self._loaded = True
        print(
            f"SIDATA loaded: {len(self.programs)} programs, "
            f"{len(self.universities)} universities"
        )

    def find_program(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Find a program by kode_prodi or name."""
        # Try kode_prodi first
        if identifier in self.programs:
            return self.programs[identifier]

        # Try exact name match (case-insensitive)
        name_upper = identifier.upper().strip()
        if name_upper in self.programs_by_name:
            # Return the one with highest peminat_2022
            programs = self.programs_by_name[name_upper]
            return max(programs, key=lambda p: p["peminat_2022"])

        # Try partial match
        for name_key, programs in self.programs_by_name.items():
            if name_upper in name_key or name_key in name_upper:
                return max(programs, key=lambda p: p["peminat_2022"])

        return None

    def find_similar_programs(
        self, program: Dict[str, Any], limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar programs with lower competition."""
        # Extract main keyword from program name
        words = program["nama_prodi"].split()
        main_keywords = [w for w in words if len(w) > 3]

        if not main_keywords:
            return []

        keyword = main_keywords[0].upper()
        target_ratio = (
            program["peminat_2022"] / max(program["daya_tampung_2022"], 1)
        )

        similar = []
        for kode, p in self.programs.items():
            if kode == program["kode_prodi"]:
                continue
            if keyword in p["nama_prodi"].upper() and p["daya_tampung_2022"] > 0:
                ratio = p["peminat_2022"] / p["daya_tampung_2022"]
                if ratio < target_ratio:
                    similar.append((p, ratio))

        # Sort by ratio ascending (easiest first)
        similar.sort(key=lambda x: x[1])
        return [p for p, _ in similar[:limit]]

    @property
    def is_loaded(self) -> bool:
        return self._loaded


class Predictor:
    """ML model predictor with fallback to deterministic formula."""

    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.sidata = SIDATAStore()

    def load_model(self, model_path: Optional[str] = None):
        """Load the trained ML model from disk."""
        if model_path is None:
            model_path = settings.MODEL_PATH

        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                self.model_loaded = True
                print(f"ML model loaded from {model_path}")
            except Exception as e:
                print(f"WARNING: Failed to load model: {e}")
                self.model_loaded = False
        else:
            print(f"WARNING: Model file not found at {model_path}")
            self.model_loaded = False

    def load_sidata(self, sql_path: Optional[str] = None):
        """Load SIDATA data from SQL file."""
        self.sidata.load(sql_path)

    def predict(
        self,
        avg_score: float,
        ranking_percentile: float,
        accreditation: str,
        program: Optional[Dict[str, Any]] = None,
    ) -> Tuple[float, float, float]:
        """
        Predict acceptance probability.

        Returns: (probability, confidence_lower, confidence_upper)
        """
        # Compute program features
        if program:
            competition_ratio = program["peminat_2022"] / max(
                program["daya_tampung_2022"], 1
            )
            peminat_2018 = max(program["peminat_2018"], 1)
            applicant_trend = (program["peminat_2022"] - peminat_2018) / peminat_2018
            daya_tampung = program["daya_tampung_2023"]
        else:
            competition_ratio = 15.0
            applicant_trend = 0.0
            daya_tampung = 50

        # Encode accreditation
        accred_map = {"A": 1.0, "B": 0.7, "C": 0.4}
        accred_score = accred_map.get(accreditation.upper(), 0.2)

        if self.model_loaded and self.model is not None:
            # Use ML model
            features = np.array(
                [
                    [
                        avg_score,
                        ranking_percentile,
                        accred_score,
                        competition_ratio,
                        applicant_trend,
                        daya_tampung,
                    ]
                ]
            )
            probability = float(self.model.predict(features)[0])
            probability = max(0.05, min(0.95, probability))

            # Confidence interval based on model uncertainty
            ci_width = 0.06 + (abs(probability - 0.5) * 0.08)
        else:
            # Fallback: deterministic formula matching PHP logic
            probability = self._deterministic_predict(
                avg_score,
                ranking_percentile,
                accred_score,
                competition_ratio,
                applicant_trend,
                daya_tampung,
            )
            ci_width = 0.08 + (abs(probability - 0.5) * 0.1)

        confidence_lower = max(0.01, probability - ci_width)
        confidence_upper = min(0.99, probability + ci_width)

        return probability, confidence_lower, confidence_upper

    def _deterministic_predict(
        self,
        avg_score: float,
        ranking_percentile: float,
        accred_score: float,
        competition_ratio: float,
        applicant_trend: float,
        daya_tampung: int,
    ) -> float:
        """Deterministic formula matching predict.php logic."""
        # Variable 1: Rasio Kompetisi (weight 0.30)
        score_rasio = max(0, 1 - (competition_ratio / 30))

        # Variable 2: Tren Peminat (weight 0.10)
        score_tren = max(0, 1 - max(0, applicant_trend))

        # Variable 3: Nilai Rata-rata (weight 0.25)
        score_nilai = max(0, min(1, (avg_score - 60) / 40))

        # Variable 4: Peringkat Siswa (weight 0.20)
        score_peringkat = max(0, min(1, 1 - ranking_percentile))

        # Variable 5: Akreditasi Sekolah (weight 0.10)
        score_akreditasi = accred_score

        # Variable 6: Daya Tampung Absolut (weight 0.05)
        score_daya_tampung = min(1, daya_tampung / 200)

        # Weighted sum
        weights = [0.30, 0.10, 0.25, 0.20, 0.10, 0.05]
        scores = [
            score_rasio,
            score_tren,
            score_nilai,
            score_peringkat,
            score_akreditasi,
            score_daya_tampung,
        ]

        probability = sum(w * s for w, s in zip(weights, scores))
        return max(0.05, min(0.95, probability))

    def get_variable_breakdown(
        self,
        avg_score: float,
        ranking: int,
        total_students: int,
        accreditation: str,
        program: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Get detailed breakdown of each prediction variable."""
        if program:
            competition_ratio = program["peminat_2022"] / max(
                program["daya_tampung_2022"], 1
            )
            peminat_2018 = max(program["peminat_2018"], 1)
            peminat_2022 = program["peminat_2022"]
            daya_tampung_2022 = program["daya_tampung_2022"]
            daya_tampung_2023 = program["daya_tampung_2023"]
            growth = (peminat_2022 - peminat_2018) / peminat_2018
        else:
            competition_ratio = 15.0
            peminat_2022 = 0
            daya_tampung_2022 = 1
            daya_tampung_2023 = 50
            growth = 0.0

        accred_map = {"A": 1.0, "B": 0.7, "C": 0.4}
        accred_score = accred_map.get(accreditation.upper(), 0.2)

        score_rasio = max(0, 1 - (competition_ratio / 30))
        score_tren = max(0, 1 - max(0, growth))
        score_nilai = max(0, min(1, (avg_score - 60) / 40))
        score_peringkat = (
            max(0, min(1, 1 - (ranking / total_students))) if total_students > 0 else 0.5
        )
        score_akreditasi = accred_score
        score_daya_tampung = min(1, daya_tampung_2023 / 200)

        variables = [
            {
                "name": "Rasio Kompetisi",
                "weight": 0.30,
                "raw_value": round(competition_ratio, 2),
                "normalized_score": round(score_rasio, 4),
                "description": (
                    f"{peminat_2022} peminat / {daya_tampung_2022} daya tampung "
                    f"(rasio {competition_ratio:.1f}:1)"
                ),
            },
            {
                "name": "Tren Peminat",
                "weight": 0.10,
                "raw_value": round(growth, 4),
                "normalized_score": round(score_tren, 4),
                "description": (
                    f"Peminat {'naik' if growth > 0 else 'turun'} "
                    f"{abs(growth) * 100:.1f}% sejak 2018"
                ),
            },
            {
                "name": "Nilai Rata-rata",
                "weight": 0.25,
                "raw_value": round(avg_score, 2),
                "normalized_score": round(score_nilai, 4),
                "description": f"Rata-rata nilai: {avg_score:.1f} dari 100",
            },
            {
                "name": "Peringkat Siswa",
                "weight": 0.20,
                "raw_value": f"{ranking}/{total_students}",
                "normalized_score": round(score_peringkat, 4),
                "description": f"Peringkat {ranking} dari {total_students} siswa",
            },
            {
                "name": "Akreditasi Sekolah",
                "weight": 0.10,
                "raw_value": accreditation,
                "normalized_score": round(score_akreditasi, 4),
                "description": f"Akreditasi {accreditation}",
            },
            {
                "name": "Daya Tampung Absolut",
                "weight": 0.05,
                "raw_value": daya_tampung_2023,
                "normalized_score": round(score_daya_tampung, 4),
                "description": f"Daya tampung 2023: {daya_tampung_2023} kursi",
            },
        ]

        return variables


# Global predictor instance
predictor = Predictor()
