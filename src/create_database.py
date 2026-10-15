from pathlib import Path
import sqlite3
import pandas as pd

# Locate project directories.
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
DATABASE_DIR = PROJECT_DIR / "database"

SALES_FILE = DATA_DIR / "ecommerce_sales_clean.csv"
CUSTOMERS_FILE = DATA_DIR / "customers.csv"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "nigerian_ecommerce.db"

# Check that the source files exist.
if not SALES_FILE.exists():
    raise FileNotFoundError(
        f"Sales dataset not found: {SALES_FILE}"
    )

if not CUSTOMERS_FILE.exists():
    raise FileNotFoundError(
        f"Customer dataset not found: {CUSTOMERS_FILE}"
    )

# Load the datasets.
sales_df = pd.read_csv(SALES_FILE)
customers_df = pd.read_csv(CUSTOMERS_FILE)

# Convert dates into a consistent format.
sales_df["Order_Date"] = pd.to_datetime(
    sales_df["Order_Date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

# Connect to SQLite.
with sqlite3.connect(DATABASE_FILE) as connection:

    # Replace the tables so repeated runs do not duplicate rows.
    sales_df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    customers_df.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )

    # Create useful indexes for common queries.
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_order_date "
        "ON sales(Order_Date)"
    )

    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_customer_id "
        "ON sales(Customer_ID)"
    )

    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_state "
        "ON sales(State)"
    )

    # Display database information.
    sales_count = connection.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    customers_count = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    print("=" * 50)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 50)

    print(f"Sales records: {sales_count:,}")
    print(f"Customer records: {customers_count:,}")
    print(f"Database location: {DATABASE_FILE}")

    print("\nDatabase tables:")

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()

    for table in tables:
        print(f"- {table[0]}")