"""
Master script to generate all 6 TOGAF Enterprise Architecture DOCX documents
for LangkahKampus EduTech - Arsitektur Integrasi Sistem course.

Usage: python3 generate_all_stages.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 70)
    print("TOGAF Enterprise Architecture Document Generator")
    print("LangkahKampus EduTech - Arsitektur Integrasi Sistem")
    print("=" * 70)
    print()

    stages = [
        ("Stage 1", "generate_stage1", "Stage1_Proposal_Tugas_Besar.docx"),
        ("Stage 2", "generate_stage2", "Stage2_Methodology_and_Project_Planning.docx"),
        ("Stage 3", "generate_stage3", "Stage3_Preliminary_Requirement_Architecture_Vision.docx"),
        ("Stage 4", "generate_stage4", "Stage4_Business_Architecture.docx"),
        ("Stage 5", "generate_stage5", "Stage5_IS_Architecture.docx"),
        ("Stage 6", "generate_stage6", "Stage6_Technology_Architecture.docx"),
    ]

    results = []
    total_start = time.time()

    for stage_name, module_name, expected_file in stages:
        print(f"\n{'─' * 50}")
        print(f"Generating {stage_name}...")
        print(f"{'─' * 50}")

        start = time.time()
        try:
            module = __import__(module_name)
            # Each module has a generate function named generate_stageN
            func_name = f"generate_{module_name.replace('generate_', '')}"
            func = getattr(module, func_name, None)
            if func is None:
                # Try alternate naming
                for attr in dir(module):
                    if attr.startswith("generate_"):
                        func = getattr(module, attr)
                        break

            if func:
                func()
                elapsed = time.time() - start

                # Verify file exists
                output_dir = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(output_dir, expected_file)
                if os.path.exists(filepath):
                    size_kb = os.path.getsize(filepath) / 1024
                    results.append((stage_name, "SUCCESS", f"{elapsed:.1f}s", f"{size_kb:.0f} KB"))
                else:
                    results.append((stage_name, "FAILED", f"{elapsed:.1f}s", "File not found"))
            else:
                results.append((stage_name, "FAILED", "0s", "No generate function found"))

        except Exception as e:
            elapsed = time.time() - start
            results.append((stage_name, "FAILED", f"{elapsed:.1f}s", str(e)[:50]))
            print(f"ERROR: {e}")

    total_elapsed = time.time() - total_start

    # Summary
    print("\n")
    print("=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)
    print(f"\n{'Stage':<12} {'Status':<10} {'Time':<8} {'Details'}")
    print("-" * 60)
    for stage_name, status, elapsed, details in results:
        status_icon = "OK" if status == "SUCCESS" else "FAIL"
        print(f"{stage_name:<12} {status_icon:<10} {elapsed:<8} {details}")

    success_count = sum(1 for _, status, _, _ in results if status == "SUCCESS")
    print(f"\n{'─' * 50}")
    print(f"Total: {success_count}/{len(stages)} documents generated successfully")
    print(f"Total time: {total_elapsed:.1f} seconds")
    print(f"{'─' * 50}")

    if success_count == len(stages):
        print("\nAll documents generated successfully!")
        print(f"\nOutput directory: {os.path.dirname(os.path.abspath(__file__))}")
        print("\nGenerated files:")
        for _, _, expected_file in stages:
            print(f"  - {expected_file}")
        return 0
    else:
        print(f"\nWARNING: {len(stages) - success_count} document(s) failed to generate.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
