from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


REQUIRED_FILES = [
    "requirements.txt",
    "README.md",
    ".gitignore",
    "docs/data_dictionary.md",
    "data/ecommerce_sales.csv",
    "data/ecommerce_sales_clean.csv",
    "data/customers.csv",
    "src/generate_data.py",
    "src/clean_data.py",
    "src/eda.py",
    "src/monthly_sales.py",
    "src/create_database.py",
    "src/run_sql_analysis.py",
    "src/run_advanced_sql.py",
    "src/run_pipeline.py",
    "tests/test_data_quality.py",
    "tests/test_financial_metrics.py",
]


REQUIRED_DIRECTORIES = [
    "data",
    "database",
    "docs",
    "reports",
    "sql",
    "src",
    "tests",
    "visualizations",
]


def main():
    print("=" * 60)
    print("PROJECT STRUCTURE VERIFICATION")
    print("=" * 60)

    missing_files = []
    missing_directories = []

    for relative_path in REQUIRED_FILES:
        full_path = PROJECT_DIR / relative_path

        if full_path.is_file():
            print(f"[OK] File: {relative_path}")
        else:
            print(f"[MISSING] File: {relative_path}")
            missing_files.append(relative_path)

    print()

    for relative_path in REQUIRED_DIRECTORIES:
        full_path = PROJECT_DIR / relative_path

        if full_path.is_dir():
            print(f"[OK] Directory: {relative_path}")
        else:
            print(f"[MISSING] Directory: {relative_path}")
            missing_directories.append(relative_path)

    print()
    print("=" * 60)

    if missing_files or missing_directories:
        print("VERIFICATION FAILED")
        print(f"Missing files: {len(missing_files)}")
        print(f"Missing directories: {len(missing_directories)}")

        return 1

    print("PROJECT STRUCTURE VERIFIED")
    print(f"Files checked: {len(REQUIRED_FILES)}")
    print(f"Directories checked: {len(REQUIRED_DIRECTORIES)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())