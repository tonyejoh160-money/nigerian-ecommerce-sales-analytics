from pathlib import Path
import subprocess
import sys
import time


PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"


PIPELINE_STEPS = [
    "generate_data.py",
    "check_data.py",
    "validate_data.py",
    "analyze_status.py",
    "clean_data.py",
    "validate_clean_data.py",
    "eda.py",
    "monthly_sales.py",
    "monthly_revenue_chart.py",
    "product_performance_chart.py",
    "state_sales_chart.py",
    "category_performance_chart.py",
    "product_profitability.py",
    "payment_analysis.py",
    "customer_analysis.py",
    "order_status_analysis.py",
    "executive_summary.py",
    "revenue_growth_analysis.py",
    "customer_segmentation.py",
    "repeat_purchase_analysis.py",
    "data_quality_report.py",
    "master_analytics_report.py",
    "create_database.py",
    "inspect_database.py",
    "run_sql_analysis.py",
    "run_advanced_sql.py",
]


def run_pipeline():
    start_time = time.time()

    print("=" * 65)
    print("NIGERIAN E-COMMERCE SALES ANALYTICS PIPELINE")
    print("=" * 65)
    print(f"Project directory: {PROJECT_DIR}")
    print(f"Python executable: {sys.executable}")
    print(f"Scripts to run: {len(PIPELINE_STEPS)}")

    missing_scripts = [
        name for name in PIPELINE_STEPS
        if not (SRC_DIR / name).is_file()
    ]

    if missing_scripts:
        print("\nERROR: Missing pipeline scripts:")

        for name in missing_scripts:
            print(f"  - {SRC_DIR / name}")

        return 1

    for number, name in enumerate(PIPELINE_STEPS, start=1):
        script_path = SRC_DIR / name

        print("\n" + "-" * 65)
        print(f"STEP {number}/{len(PIPELINE_STEPS)}: {name}")
        print("-" * 65)

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(PROJECT_DIR),
                check=False,
            )
        except OSError as error:
            print(f"\nERROR starting {name}: {error}")
            return 1

        if result.returncode != 0:
            print(f"\nPIPELINE FAILED: {name}")
            print(f"Exit code: {result.returncode}")
            return result.returncode or 1

        print(f"COMPLETED: {name}")

    elapsed = time.time() - start_time

    print("\n" + "=" * 65)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Scripts completed: {len(PIPELINE_STEPS)}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print(f"Reports: {PROJECT_DIR / 'reports'}")
    print(f"Visualizations: {PROJECT_DIR / 'visualizations'}")
    print(f"Database: {PROJECT_DIR / 'database'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(run_pipeline())