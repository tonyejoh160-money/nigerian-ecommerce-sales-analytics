from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = (
    PROJECT_DIR
    / "database"
    / "nigerian_ecommerce.db"
)

SQL_FILE = PROJECT_DIR / "sql" / "advanced_analysis.sql"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATABASE_FILE.exists():
    raise FileNotFoundError(
        "Database not found. Run "
        "python src/create_database.py first."
    )

if not SQL_FILE.exists():
    raise FileNotFoundError(
        f"SQL file not found: {SQL_FILE}"
    )

sql_text = SQL_FILE.read_text(encoding="utf-8")

queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

with sqlite3.connect(DATABASE_FILE) as connection:

    print("=" * 60)
    print("ADVANCED SQL ANALYSIS")
    print("=" * 60)

    for index, query in enumerate(queries, start=1):

        cleaned_query = "\n".join(
            line
            for line in query.splitlines()
            if line.strip()
            and not line.strip().startswith("--")
        ).strip()

        if not cleaned_query:
            continue

        result = pd.read_sql_query(
            cleaned_query,
            connection
        )

        print(f"\nADVANCED QUERY {index}")
        print("-" * 60)
        print(result.to_string(index=False))

        output_file = (
            OUTPUT_DIR
            / f"advanced_sql_query_{index:02d}.csv"
        )

        result.to_csv(
            output_file,
            index=False
        )

        print(f"\nSaved result: {output_file}")

print("\nAdvanced SQL analysis completed.")