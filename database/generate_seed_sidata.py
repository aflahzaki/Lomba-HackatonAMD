#!/usr/bin/env python3
"""
Generate seed_sidata.sql from Kaggle CSV files.
Reads daftar_universitas.csv and daftar_prodi.csv and outputs SQL INSERT statements.
"""
import csv
import os

CSV_DIR = "/projects/sandbox/PRE-AIAgentJarvis/Dataset Data Sistem Informasi Daya Tampung (SIDATA) PTN/"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_sidata.sql")


def escape_sql(value):
    """Escape single quotes for SQL string values."""
    if value is None or value == '':
        return 'NULL'
    return "'" + value.replace("'", "''") + "'"


def int_or_null(value):
    """Convert value to int or NULL if empty."""
    if value is None or value.strip() == '':
        return 'NULL'
    try:
        return str(int(value))
    except ValueError:
        return 'NULL'


def main():
    lines = []
    lines.append("-- ============================================================")
    lines.append("-- LangkahKampus - SIDATA PTN Seed Data")
    lines.append("-- Generated from Kaggle Dataset: Sistem Informasi Daya Tampung PTN")
    lines.append("-- 84 Universities and 3058 Study Programs")
    lines.append("-- ============================================================")
    lines.append("")
    lines.append("USE langkahkampus;")
    lines.append("")
    lines.append("-- ============================================================")
    lines.append("-- Seed: sidata_universitas (84 rows)")
    lines.append("-- ============================================================")
    lines.append("")

    # Read universities
    univ_file = os.path.join(CSV_DIR, "daftar_universitas.csv")
    univ_count = 0
    with open(univ_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kode_univ = escape_sql(row['kode_univ'].strip())
            nama_univ = escape_sql(row['nama_univ'].strip())
            portal_univ = escape_sql(row['portal_univ'].strip())
            lines.append(
                f"INSERT INTO sidata_universitas (kode_univ, nama_univ, portal_univ) "
                f"VALUES ({kode_univ}, {nama_univ}, {portal_univ});"
            )
            univ_count += 1

    lines.append("")
    lines.append(f"-- Total universities inserted: {univ_count}")
    lines.append("")
    lines.append("-- ============================================================")
    lines.append("-- Seed: sidata_prodi (3058 rows)")
    lines.append("-- ============================================================")
    lines.append("")

    # Read prodi
    prodi_file = os.path.join(CSV_DIR, "daftar_prodi.csv")
    prodi_count = 0
    with open(prodi_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kode_univ = escape_sql(row['kode_univ'].strip())
            kode_prodi = escape_sql(row['kode_prodi'].strip())
            nama_prodi = escape_sql(row['nama_prodi'].strip())
            jenjang = escape_sql(row['jenjang'].strip())
            daya_tampung_2023 = int_or_null(row['daya_tampung_2023'])
            peminat_2018 = int_or_null(row['peminat_2018'])
            peminat_2019 = int_or_null(row['peminat_2019'])
            peminat_2020 = int_or_null(row['peminat_2020'])
            peminat_2021 = int_or_null(row['peminat_2021'])
            peminat_2022 = int_or_null(row['peminat_2022'])
            daya_tampung_2018 = int_or_null(row['daya_tampung_2018'])
            daya_tampung_2019 = int_or_null(row['daya_tampung_2019'])
            daya_tampung_2020 = int_or_null(row['daya_tampung_2020'])
            daya_tampung_2021 = int_or_null(row['daya_tampung_2021'])
            daya_tampung_2022 = int_or_null(row['daya_tampung_2022'])

            lines.append(
                f"INSERT INTO sidata_prodi (kode_univ, kode_prodi, nama_prodi, jenjang, "
                f"daya_tampung_2023, peminat_2018, peminat_2019, peminat_2020, peminat_2021, peminat_2022, "
                f"daya_tampung_2018, daya_tampung_2019, daya_tampung_2020, daya_tampung_2021, daya_tampung_2022) "
                f"VALUES ({kode_univ}, {kode_prodi}, {nama_prodi}, {jenjang}, "
                f"{daya_tampung_2023}, {peminat_2018}, {peminat_2019}, {peminat_2020}, {peminat_2021}, {peminat_2022}, "
                f"{daya_tampung_2018}, {daya_tampung_2019}, {daya_tampung_2020}, {daya_tampung_2021}, {daya_tampung_2022});"
            )
            prodi_count += 1

    lines.append("")
    lines.append(f"-- Total prodi inserted: {prodi_count}")
    lines.append("")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Generated {OUTPUT_FILE}")
    print(f"  Universities: {univ_count}")
    print(f"  Prodi: {prodi_count}")


if __name__ == '__main__':
    main()
