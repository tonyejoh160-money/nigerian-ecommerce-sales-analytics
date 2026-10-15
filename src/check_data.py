from pathlib import Path

import pandas as pd


# Locate the dataset.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales.csv"

# Load the dataset.
df = pd.read_csv(DATA_FILE)

print("=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

# Dataset dimensions.
print("\n1. DATASET DIMENSIONS")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# Column names.
print("\n2. COLUMN NAMES")
print(df.columns.tolist())

# Data types.
print("\n3. DATA TYPES")
print(df.dtypes)

# Missing values.
print("\n4. MISSING VALUES")
print(df.isnull().sum())

# Duplicate rows.
print("\n5. DUPLICATE ROWS")
print(f"Duplicate rows: {df.duplicated().sum()}")

# Duplicate order IDs.
print("\n6. DUPLICATE ORDER IDS")
print(f"Duplicate IDs: {df['Order_ID'].duplicated().sum()}")

print("\nDATA QUALITY CHECK COMPLETED.")
df = pd.read_csv(DATA_FILE)
# Convert the order date to a proper datetime type.
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print("\nDATE TYPE CHECK")
print("Order_Date type:", df["Order_Date"].dtype)

# Check for invalid dates.
print(
    "Invalid dates:",
    df["Order_Date"].isna().sum()
)