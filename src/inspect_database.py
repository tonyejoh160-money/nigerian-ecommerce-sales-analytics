from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = (
    PROJECT_DIR
    / "database"
    / "nigerian_ecommerce.db"
)

if not DATABASE_FILE.exists():
    raise FileNotFoundError(
        "Database not found. Run "
        "python src/create_database.py first."
    )

with sqlite3.connect(DATABASE_FILE) as connection:

    print("=" * 55)
    print("DATABASE INSPECTION")
    print("=" * 55)

    # List all tables.
    print("\n1. DATABASE TABLES")

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """,
        connection
    )

    print(tables.to_string(index=False))

    # Inspect sales columns.
    print("\n2. SALES TABLE STRUCTURE")

    sales_columns = pd.read_sql_query(
        "PRAGMA table_info(sales)",
        connection
    )

    print(
        sales_columns[
            ["name", "type"]
        ].to_string(index=False)
    )

    # Inspect customer columns.
    print("\n3. CUSTOMERS TABLE STRUCTURE")

    customer_columns = pd.read_sql_query(
        "PRAGMA table_info(customers)",
        connection
    )

    print(
        customer_columns[
            ["name", "type"]
        ].to_string(index=False)
    )

    # Preview five records.
    print("\n4. FIRST FIVE SALES RECORDS")

    preview = pd.read_sql_query(
        """
        SELECT
            Order_ID,
            Order_Date,
            State,
            Product,
            Net_Revenue,
            Order_Status
        FROM sales
        LIMIT 5
        """,
        connection
    )

    print(preview.to_string(index=False))

    # Count records.
    print("\n5. RECORD COUNTS")

    result = pd.read_sql_query(
        """
        SELECT
            (SELECT COUNT(*) FROM sales) AS Sales_Records,
            (SELECT COUNT(*) FROM customers) AS Customer_Records
        """,
        connection
    )

    print(result.to_string(index=False))