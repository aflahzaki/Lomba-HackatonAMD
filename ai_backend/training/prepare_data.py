"""
Parse SIDATA SQL file and generate synthetic training data.

Parses database/seed_sidata.sql directly using regex to extract all 3058 study
programs and generates synthetic training data for the ML model.
"""

import os
import re
import sys

import numpy as np
import pandas as pd

# Path to the SQL file
SQL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "database",
    "seed_sidata.sql",
)

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "training_data.csv",
)

# Number of synthetic students per program
STUDENTS_PER_PROGRAM = 10

# Random seed for reproducibility
RANDOM_SEED = 42


def parse_sidata_sql(sql_path: str) -> pd.DataFrame:
    """Parse INSERT statements from seed_sidata.sql."""
    print(f"Reading SQL file: {sql_path}")

    if not os.path.exists(sql_path):
        print(f"ERROR: SQL file not found at {sql_path}")
        sys.exit(1)

    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse INSERT INTO sidata_prodi statements
    pattern = re.compile(
        r"INSERT INTO sidata_prodi \(kode_univ, kode_prodi, nama_prodi, jenjang, "
        r"daya_tampung_2023, peminat_2018, peminat_2019, peminat_2020, peminat_2021, "
        r"peminat_2022, daya_tampung_2018, daya_tampung_2019, daya_tampung_2020, "
        r"daya_tampung_2021, daya_tampung_2022\) VALUES "
        r"\('(\d+)', '(\d+)', '([^']+)', '([^']+)', (\d+), "
        r"(\d+), (\d+), (\d+), (\d+), (\d+), "
        r"(\d+), (\d+), (\d+), (\d+), (\d+)\);",
        re.IGNORECASE,
    )

    records = []
    for match in pattern.finditer(content):
        records.append({
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
        })

    df = pd.DataFrame(records)
    print(f"Parsed {len(df)} study programs from SQL file")
    return df


def compute_program_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived features for each program."""
    # Competition ratio (peminat_2022 / daya_tampung_2022)
    df["competition_ratio"] = df["peminat_2022"] / df["daya_tampung_2022"].clip(lower=1)

    # Applicant trend (growth rate from 2018 to 2022)
    df["applicant_trend"] = (df["peminat_2022"] - df["peminat_2018"]) / df[
        "peminat_2018"
    ].clip(lower=1)

    # Peminat volatility (std of peminat across years)
    peminat_cols = ["peminat_2018", "peminat_2019", "peminat_2020", "peminat_2021", "peminat_2022"]
    df["peminat_volatility"] = df[peminat_cols].std(axis=1) / df[peminat_cols].mean(axis=1).clip(lower=1)

    # Capacity trend
    dt_cols = ["daya_tampung_2018", "daya_tampung_2019", "daya_tampung_2020", "daya_tampung_2021", "daya_tampung_2022"]
    df["capacity_trend"] = (df["daya_tampung_2022"] - df["daya_tampung_2018"]) / df[
        "daya_tampung_2018"
    ].clip(lower=1)

    return df


def deterministic_formula(
    avg_score: float,
    ranking_percentile: float,
    accred_score: float,
    competition_ratio: float,
    applicant_trend: float,
    daya_tampung: int,
) -> float:
    """Replicate the PHP deterministic formula."""
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
    scores = [score_rasio, score_tren, score_nilai, score_peringkat, score_akreditasi, score_daya_tampung]

    probability = sum(w * s for w, s in zip(weights, scores))
    return max(0.05, min(0.95, probability))


def generate_synthetic_data(programs_df: pd.DataFrame, rng: np.random.RandomState) -> pd.DataFrame:
    """
    Generate synthetic training data by simulating students.

    For each program, generate N synthetic students with varying:
    - avg_score (60-100)
    - ranking_percentile (0-1)
    - accreditation (A/B/C)

    Ground truth is the PHP formula + noise + non-linear effects.
    """
    training_records = []

    accred_options = ["A", "B", "C"]
    accred_scores = {"A": 1.0, "B": 0.7, "C": 0.4}
    accred_weights = [0.3, 0.5, 0.2]  # probability distribution

    for _, program in programs_df.iterrows():
        competition_ratio = program["competition_ratio"]
        applicant_trend = program["applicant_trend"]
        daya_tampung = program["daya_tampung_2023"]

        for _ in range(STUDENTS_PER_PROGRAM):
            # Simulate student features
            avg_score = rng.uniform(60, 100)
            ranking_percentile = rng.uniform(0.01, 0.99)
            accred = rng.choice(accred_options, p=accred_weights)
            accred_score = accred_scores[accred]

            # Compute base probability using deterministic formula
            base_prob = deterministic_formula(
                avg_score, ranking_percentile, accred_score,
                competition_ratio, applicant_trend, daya_tampung,
            )

            # Add non-linear effects (interactions)
            # High scores + low ranking = bonus
            interaction1 = 0.03 * max(0, (avg_score - 85) / 15) * max(0, (1 - ranking_percentile - 0.7) / 0.3)
            # High competition + low accreditation = extra penalty
            interaction2 = -0.02 * max(0, (competition_ratio - 10) / 20) * (1 - accred_score)
            # Very low ranking percentile (<10%) gets bonus
            interaction3 = 0.02 if ranking_percentile < 0.1 else 0.0

            # Add random noise
            noise = rng.normal(0, 0.03)

            # Final probability with non-linear effects
            final_prob = base_prob + interaction1 + interaction2 + interaction3 + noise
            final_prob = max(0.05, min(0.95, final_prob))

            training_records.append({
                "avg_score": avg_score,
                "ranking_percentile": ranking_percentile,
                "accred_score": accred_score,
                "competition_ratio": competition_ratio,
                "applicant_trend": applicant_trend,
                "daya_tampung": daya_tampung,
                "probability": final_prob,
            })

    return pd.DataFrame(training_records)


def main():
    """Main entry point for data preparation."""
    print("=" * 60)
    print("LangkahKampus - Training Data Preparation")
    print("=" * 60)

    # Parse SIDATA
    programs_df = parse_sidata_sql(SQL_PATH)
    programs_df = compute_program_features(programs_df)

    print(f"\nProgram statistics:")
    print(f"  Competition ratio - mean: {programs_df['competition_ratio'].mean():.2f}, "
          f"max: {programs_df['competition_ratio'].max():.2f}")
    print(f"  Applicant trend - mean: {programs_df['applicant_trend'].mean():.4f}")
    print(f"  Daya tampung 2023 - mean: {programs_df['daya_tampung_2023'].mean():.0f}")

    # Generate synthetic training data
    print(f"\nGenerating synthetic training data ({STUDENTS_PER_PROGRAM} students per program)...")
    rng = np.random.RandomState(RANDOM_SEED)
    training_df = generate_synthetic_data(programs_df, rng)

    print(f"Generated {len(training_df)} training samples")
    print(f"\nFeature statistics:")
    print(training_df.describe())

    # Save to CSV
    training_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nTraining data saved to: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
